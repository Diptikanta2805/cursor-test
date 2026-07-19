"""Transformer classifiers: fast tier (encoder classifier) and deep tier.

Fast tier: any `AutoModelForSequenceClassification` binary detector, e.g.
`MayZhou/e5-small-lora-ai-generated-detector` (33M params, MIT, ~93.9%
accuracy on RAID-test).

Deep tier: `desklib/ai-text-detector-v1.01` (DeBERTa-v3-large, MIT, led the
RAID leaderboard). Desklib uses a custom mean-pooling + single-logit head,
implemented here exactly as published on its model card.
"""

from __future__ import annotations

import logging
import math

import torch
import torch.nn as nn
from transformers import (
    AutoConfig,
    AutoModel,
    AutoModelForSequenceClassification,
    AutoTokenizer,
)

logger = logging.getLogger(__name__)

_AI_LABEL_HINTS = ("ai", "machine", "generated", "fake", "gpt", "label_1")


def _resolve_ai_label_index(id2label: dict[int, str]) -> int:
    """Find which output index means "AI-generated" from the label names."""
    for idx, label in id2label.items():
        if any(hint in str(label).lower() for hint in _AI_LABEL_HINTS):
            return int(idx)
    return 1


class FastClassifier:
    """Batched binary AI-text classifier used for document and window scores."""

    def __init__(
        self,
        model_id: str,
        device: str = "cpu",
        max_length: int = 512,
        ai_label_index: int | None = None,
        torch_dtype: torch.dtype = torch.float32,
    ) -> None:
        self.model_id = model_id
        self.device = torch.device(device)
        self.max_length = max_length
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_id, torch_dtype=torch_dtype
        )
        self.model.to(self.device)
        self.model.eval()
        id2label = getattr(self.model.config, "id2label", {0: "human", 1: "ai"})
        self.ai_index = (
            ai_label_index
            if ai_label_index is not None
            else _resolve_ai_label_index(id2label)
        )
        logger.info(
            "Loaded fast classifier %s (ai label index=%d, labels=%s)",
            model_id,
            self.ai_index,
            id2label,
        )

    @torch.inference_mode()
    def score(self, texts: list[str], batch_size: int = 16) -> list[float]:
        """Return P(AI-generated) for each text."""
        probs: list[float] = []
        for start in range(0, len(texts), batch_size):
            batch = texts[start : start + batch_size]
            encoded = self.tokenizer(
                batch,
                truncation=True,
                max_length=self.max_length,
                padding=True,
                return_tensors="pt",
            ).to(self.device)
            logits = self.model(**encoded).logits
            if logits.shape[-1] == 1:
                batch_probs = torch.sigmoid(logits.squeeze(-1))
            else:
                batch_probs = torch.softmax(logits, dim=-1)[:, self.ai_index]
            probs.extend(batch_probs.float().cpu().tolist())
        return probs


class DesklibAIDetectionModel(nn.Module):
    """Architecture from the desklib/ai-text-detector-v1.01 model card.

    A plain nn.Module (rather than a PreTrainedModel subclass) so loading is
    robust across transformers versions; weights are read directly from the
    checkpoint's safetensors file. Attribute names (`model`, `classifier`)
    match the published checkpoint's state-dict keys exactly.
    """

    def __init__(self, config):
        super().__init__()
        self.model = AutoModel.from_config(config)
        self.classifier = nn.Linear(config.hidden_size, 1)

    def forward(self, input_ids, attention_mask=None):
        outputs = self.model(input_ids, attention_mask=attention_mask)
        last_hidden_state = outputs[0]
        mask_expanded = (
            attention_mask.unsqueeze(-1).expand(last_hidden_state.size()).float()
        )
        pooled = torch.sum(last_hidden_state * mask_expanded, dim=1) / torch.clamp(
            mask_expanded.sum(dim=1), min=1e-9
        )
        logits = self.classifier(pooled)
        return {"logits": logits}

    @classmethod
    def from_pretrained(cls, model_id: str) -> "DesklibAIDetectionModel":
        from huggingface_hub import hf_hub_download
        from safetensors.torch import load_file

        config = AutoConfig.from_pretrained(model_id)
        instance = cls(config)
        weights_path = hf_hub_download(model_id, "model.safetensors")
        state_dict = load_file(weights_path)
        missing, unexpected = instance.load_state_dict(state_dict, strict=False)
        if any("classifier" in k for k in missing) or unexpected:
            raise RuntimeError(
                f"Checkpoint mismatch for {model_id}: "
                f"missing={missing}, unexpected={unexpected}"
            )
        return instance


class DeepClassifier:
    """Desklib DeBERTa-v3-large detector: slower, RAID-leading accuracy."""

    def __init__(
        self, model_id: str, device: str = "cpu", max_length: int = 768
    ) -> None:
        self.model_id = model_id
        self.device = torch.device(device)
        self.max_length = max_length
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.model = DesklibAIDetectionModel.from_pretrained(model_id)
        self.model.to(self.device)
        self.model.eval()
        logger.info("Loaded deep classifier %s", model_id)

    @torch.inference_mode()
    def score(self, texts: list[str], batch_size: int = 2) -> list[float]:
        probs: list[float] = []
        for start in range(0, len(texts), batch_size):
            batch = texts[start : start + batch_size]
            encoded = self.tokenizer(
                batch,
                truncation=True,
                max_length=self.max_length,
                padding=True,
                return_tensors="pt",
            ).to(self.device)
            logits = self.model(
                input_ids=encoded["input_ids"],
                attention_mask=encoded["attention_mask"],
            )["logits"]
            probs.extend(torch.sigmoid(logits.squeeze(-1)).float().cpu().tolist())
        return probs


def prob_to_logit(p: float, eps: float = 1e-6) -> float:
    p = min(max(p, eps), 1.0 - eps)
    return math.log(p / (1.0 - p))
