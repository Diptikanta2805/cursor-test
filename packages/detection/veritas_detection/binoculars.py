"""Binoculars zero-shot detector (ICML 2024).

Contrasts perplexity under a performer LLM against cross-entropy between an
observer/performer pair. Lower Binoculars scores indicate AI-generated text.
Reference: https://arxiv.org/abs/2401.12070

Uses a small Qwen2.5-0.5B pair by default for CPU-friendly deep scans.
"""

from __future__ import annotations

import logging
import math

import torch
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer

logger = logging.getLogger(__name__)

_ce = torch.nn.CrossEntropyLoss(reduction="none")


def _perplexity(
    input_ids: torch.Tensor,
    attention_mask: torch.Tensor,
    logits: torch.Tensor,
) -> float:
    shifted_logits = logits[..., :-1, :].contiguous()
    shifted_labels = input_ids[..., 1:].contiguous()
    mask = attention_mask[..., 1:].contiguous().float()
    loss = _ce(shifted_logits.transpose(1, 2), shifted_labels)
    return float(((loss * mask).sum() / mask.sum()).exp().item())


def _cross_entropy(
    observer_logits: torch.Tensor,
    performer_logits: torch.Tensor,
    input_ids: torch.Tensor,
    attention_mask: torch.Tensor,
    pad_token_id: int,
) -> float:
    vocab = observer_logits.shape[-1]
    tokens = observer_logits.shape[-2]
    p_probs = F.softmax(observer_logits, dim=-1).view(-1, vocab)
    q_scores = performer_logits.view(-1, vocab)
    ce = _ce(q_scores, p_probs).view(-1, tokens)
    mask = (input_ids != pad_token_id).float()
    return float(((ce * mask).sum() / mask.sum()).item())


def score_to_ai_probability(binoculars_score: float, center: float = 1.0, scale: float = 6.0) -> float:
    """Map Binoculars score to P(AI). Lower score => higher P(AI)."""
    return 1.0 / (1.0 + math.exp((binoculars_score - center) * scale))


class BinocularsScorer:
    def __init__(
        self,
        observer_id: str = "Qwen/Qwen2.5-0.5B",
        performer_id: str = "Qwen/Qwen2.5-0.5B-Instruct",
        device: str = "cpu",
        max_length: int = 512,
    ) -> None:
        self.device = torch.device(device)
        self.max_length = max_length
        self.tokenizer = AutoTokenizer.from_pretrained(observer_id, trust_remote_code=True)
        if not self.tokenizer.pad_token:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        dtype = torch.float32
        self.observer = AutoModelForCausalLM.from_pretrained(
            observer_id, torch_dtype=dtype, trust_remote_code=True
        ).to(self.device).eval()
        self.performer = AutoModelForCausalLM.from_pretrained(
            performer_id, torch_dtype=dtype, trust_remote_code=True
        ).to(self.device).eval()
        logger.info("Loaded Binoculars pair %s / %s", observer_id, performer_id)

    @torch.inference_mode()
    def score(self, text: str) -> tuple[float, float]:
        """Return (raw_binoculars_score, ai_probability)."""
        encoded = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=self.max_length,
            return_token_type_ids=False,
        ).to(self.device)
        observer_logits = self.observer(**encoded).logits
        performer_logits = self.performer(**encoded).logits
        ppl = _perplexity(encoded.input_ids, encoded.attention_mask, performer_logits)
        x_ppl = _cross_entropy(
            observer_logits,
            performer_logits,
            encoded.input_ids,
            encoded.attention_mask,
            self.tokenizer.pad_token_id,
        )
        raw = ppl / max(x_ppl, 1e-9)
        return round(raw, 4), round(score_to_ai_probability(raw), 4)
