"""GPTZero-style statistical signals: perplexity and burstiness.

Uses a small causal LM (distilgpt2, 82M params, Apache-2.0) to compute
document perplexity and per-sentence perplexity variance ("burstiness").
AI text tends to have low perplexity AND uniform sentence perplexity; human
text is higher-perplexity and burstier. These signals are shown to the user
for transparency and contribute a small weight to the ensemble.
"""

from __future__ import annotations

import logging
import math
import statistics

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

logger = logging.getLogger(__name__)


class PerplexityScorer:
    def __init__(
        self, model_id: str = "distilgpt2", device: str = "cpu", max_length: int = 1024
    ) -> None:
        self.device = torch.device(device)
        self.max_length = max_length
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.model = AutoModelForCausalLM.from_pretrained(model_id)
        self.model.to(self.device)
        self.model.eval()
        logger.info("Loaded perplexity scorer %s", model_id)

    @torch.inference_mode()
    def perplexity(self, text: str) -> float | None:
        ids = self.tokenizer(
            text, truncation=True, max_length=self.max_length, return_tensors="pt"
        )["input_ids"].to(self.device)
        if ids.shape[1] < 2:
            return None
        loss = self.model(ids, labels=ids).loss
        return float(torch.exp(loss).item())

    def signals(self, doc_text: str, sentences: list[str]) -> dict[str, float | None]:
        """Return doc perplexity, mean sentence perplexity, and burstiness."""
        doc_ppl = self.perplexity(doc_text)
        sentence_ppls = [
            ppl
            for s in sentences
            if len(s.split()) >= 4 and (ppl := self.perplexity(s)) is not None
        ]
        burstiness = None
        mean_sentence_ppl = None
        if len(sentence_ppls) >= 2:
            mean_sentence_ppl = statistics.mean(sentence_ppls)
            # Coefficient of variation of sentence perplexities.
            burstiness = statistics.stdev(sentence_ppls) / max(mean_sentence_ppl, 1e-9)
        return {
            "perplexity": doc_ppl,
            "mean_sentence_perplexity": mean_sentence_ppl,
            "burstiness": burstiness,
        }

    @staticmethod
    def ai_likelihood(signals: dict[str, float | None]) -> float | None:
        """Map (perplexity, burstiness) to a rough P(AI) in [0, 1].

        Centered on empirical distilgpt2 scales: AI text usually shows
        perplexity < ~30 and burstiness < ~0.5; human text sits above both.
        This is a weak prior, weighted lightly in the ensemble.
        """
        ppl = signals.get("perplexity")
        burst = signals.get("burstiness")
        if ppl is None:
            return None
        ppl_component = 1.0 / (1.0 + math.exp((math.log(ppl) - math.log(32.0)) * 2.2))
        if burst is None:
            return ppl_component
        burst_component = 1.0 / (1.0 + math.exp((burst - 0.55) * 6.0))
        return 0.65 * ppl_component + 0.35 * burst_component
