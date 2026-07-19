"""Style-retrieval detection arm (DeTeCtive-style, training-free).

Detection as authorship verification instead of binary classification: embed
the document with a general-purpose text encoder and vote over its nearest
neighbors in a reference index of human- and LLM-written texts. The index
carries generator labels, so the same lookup yields *attribution* ("nearest
style: ChatGPT-class"). New generators are supported by appending embeddings
to the index — Training-Free Incremental Adaptation, no retraining.

Reference: DeTeCtive (NeurIPS 2024), arXiv:2410.20964.
"""

from __future__ import annotations

import logging
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import torch
from transformers import AutoModel, AutoTokenizer

logger = logging.getLogger(__name__)

DEFAULT_INDEX_PATH = Path(__file__).parent / "assets" / "style_index.npz"


@dataclass
class RetrievalResult:
    ai_probability: float
    attributed_generator: str | None  # e.g. "chatgpt"; None when verdict is human-ish
    attribution_share: float | None  # share of AI neighbors from that generator
    mean_neighbor_similarity: float


class StyleEmbedder:
    """e5-small-v2 mean-pooled embeddings (33M params, MIT, CPU-fast)."""

    def __init__(
        self,
        model_id: str = "intfloat/e5-small-v2",
        device: str = "cpu",
        max_length: int = 512,
    ) -> None:
        self.device = torch.device(device)
        self.max_length = max_length
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.model = AutoModel.from_pretrained(model_id)
        self.model.to(self.device)
        self.model.eval()
        logger.info("Loaded style embedder %s", model_id)

    @torch.inference_mode()
    def embed(self, texts: list[str], batch_size: int = 16) -> np.ndarray:
        """L2-normalized embeddings; e5 expects the 'passage: ' prefix."""
        vectors: list[np.ndarray] = []
        for start in range(0, len(texts), batch_size):
            batch = ["passage: " + t for t in texts[start : start + batch_size]]
            encoded = self.tokenizer(
                batch,
                truncation=True,
                max_length=self.max_length,
                padding=True,
                return_tensors="pt",
            ).to(self.device)
            hidden = self.model(**encoded).last_hidden_state
            mask = encoded["attention_mask"].unsqueeze(-1).float()
            pooled = (hidden * mask).sum(dim=1) / mask.sum(dim=1).clamp(min=1e-9)
            pooled = torch.nn.functional.normalize(pooled, dim=-1)
            vectors.append(pooled.float().cpu().numpy())
        return np.concatenate(vectors, axis=0)


class StyleRetrieval:
    """kNN vote over a labeled reference index of writing-style embeddings."""

    def __init__(
        self,
        embedder: StyleEmbedder,
        index_path: str | Path = DEFAULT_INDEX_PATH,
        k: int = 15,
    ) -> None:
        self.embedder = embedder
        self.k = k
        data = np.load(index_path, allow_pickle=False)
        self.embeddings = data["embeddings"].astype(np.float32)  # (n, d), normalized
        self.labels = data["labels"].astype(np.int8)  # 0 human, 1 ai
        self.generators = data["generators"]  # (n,) unicode
        logger.info(
            "Loaded style index: %d reference texts (%d human / %d AI, %d generators)",
            len(self.labels),
            int((self.labels == 0).sum()),
            int((self.labels == 1).sum()),
            len(set(self.generators[self.labels == 1].tolist())),
        )

    def score(self, text: str, doc_embedding: np.ndarray | None = None) -> RetrievalResult:
        query = (
            doc_embedding
            if doc_embedding is not None
            else self.embedder.embed([text])[0]
        )
        similarities = self.embeddings @ query
        top = np.argsort(-similarities)[: self.k]
        top_sims = similarities[top]
        top_labels = self.labels[top]

        # Sharpen similarities so close neighbors dominate the vote.
        weights = np.exp((top_sims - top_sims.max()) / 0.02)
        p_ai = float((weights * top_labels).sum() / weights.sum())

        attributed, share = None, None
        ai_mask = top_labels == 1
        if ai_mask.any() and p_ai >= 0.5:
            votes: dict[str, float] = defaultdict(float)
            for gen, w in zip(self.generators[top][ai_mask], weights[ai_mask]):
                votes[str(gen)] += float(w)
            total = sum(votes.values())
            attributed, best = max(votes.items(), key=lambda kv: kv[1])
            share = best / total

        return RetrievalResult(
            ai_probability=p_ai,
            attributed_generator=attributed,
            attribution_share=round(share, 3) if share is not None else None,
            mean_neighbor_similarity=round(float(top_sims.mean()), 4),
        )
