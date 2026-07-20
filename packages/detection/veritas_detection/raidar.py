"""RAIDAR-style rewrite detector (ICLR 2024).

Ask a small instruct LLM to rewrite the input; AI-generated text changes less
under rewriting than human text. We measure semantic similarity between the
original and the rewrite with the style embedder (e5-small-v2).

Reference: https://arxiv.org/abs/2401.12970
"""

from __future__ import annotations

import logging
import math

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from veritas_detection.retrieval import StyleEmbedder

logger = logging.getLogger(__name__)

_REWRITE_PROMPT = (
    "Rewrite the following text in your own words while preserving the meaning. "
    "Output only the rewritten text.\n\nText:\n{text}\n\nRewritten:"
)


def similarity_to_ai_probability(similarity: float, center: float = 0.88, scale: float = 25.0) -> float:
    """High rewrite similarity => likely AI (text was already machine-like)."""
    return 1.0 / (1.0 + math.exp(-(similarity - center) * scale))


class RaidarScorer:
    def __init__(
        self,
        rewrite_model_id: str = "HuggingFaceTB/SmolLM2-360M-Instruct",
        embedder: StyleEmbedder | None = None,
        device: str = "cpu",
        max_input_length: int = 768,
        max_new_tokens: int = 256,
    ) -> None:
        self.device = torch.device(device)
        self.max_input_length = max_input_length
        self.max_new_tokens = max_new_tokens
        self.embedder = embedder or StyleEmbedder(device=device)
        self.tokenizer = AutoTokenizer.from_pretrained(rewrite_model_id, trust_remote_code=True)
        if not self.tokenizer.pad_token:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        self.model = AutoModelForCausalLM.from_pretrained(
            rewrite_model_id, torch_dtype=torch.float32, trust_remote_code=True
        ).to(self.device).eval()
        logger.info("Loaded RAIDAR rewriter %s", rewrite_model_id)

    @torch.inference_mode()
    def rewrite(self, text: str) -> str:
        prompt = _REWRITE_PROMPT.format(text=text[:4000])
        messages = [{"role": "user", "content": prompt}]
        if hasattr(self.tokenizer, "apply_chat_template"):
            input_text = self.tokenizer.apply_chat_template(
                messages, tokenize=False, add_generation_prompt=True
            )
        else:
            input_text = prompt
        encoded = self.tokenizer(
            input_text, return_tensors="pt", truncation=True, max_length=self.max_input_length
        ).to(self.device)
        output = self.model.generate(
            **encoded,
            max_new_tokens=self.max_new_tokens,
            do_sample=False,
            pad_token_id=self.tokenizer.pad_token_id,
        )
        generated = self.tokenizer.decode(
            output[0][encoded.input_ids.shape[1] :], skip_special_tokens=True
        ).strip()
        return generated or text

    def score(self, text: str) -> tuple[float, float]:
        """Return (rewrite_similarity, ai_probability)."""
        rewritten = self.rewrite(text)
        original_emb, rewrite_emb = self.embedder.embed([text, rewritten])
        similarity = float((original_emb * rewrite_emb).sum())
        return round(similarity, 4), round(similarity_to_ai_probability(similarity), 4)
