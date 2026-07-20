"""Lazy wrappers so zero-shot arms load only on the first deep scan."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from veritas_detection.binoculars import BinocularsScorer
    from veritas_detection.raidar import RaidarScorer

logger = logging.getLogger(__name__)


class LazyBinoculars:
    def __init__(
        self,
        observer_id: str,
        performer_id: str,
        device: str = "cpu",
    ) -> None:
        self.observer_id = observer_id
        self.performer_id = performer_id
        self.device = device
        self._inner: BinocularsScorer | None = None

    def score(self, text: str) -> tuple[float, float]:
        if self._inner is None:
            from veritas_detection.binoculars import BinocularsScorer

            logger.info("Lazy-loading Binoculars models (first deep scan)…")
            self._inner = BinocularsScorer(
                self.observer_id, self.performer_id, device=self.device
            )
        return self._inner.score(text)


class LazyRaidar:
    def __init__(self, rewrite_model_id: str, embedder_model_id: str, device: str = "cpu") -> None:
        self.rewrite_model_id = rewrite_model_id
        self.embedder_model_id = embedder_model_id
        self.device = device
        self._inner: RaidarScorer | None = None

    def score(self, text: str) -> tuple[float, float]:
        if self._inner is None:
            from veritas_detection.raidar import RaidarScorer
            from veritas_detection.retrieval import StyleEmbedder

            logger.info("Lazy-loading RAIDAR rewriter (first deep scan)…")
            self._inner = RaidarScorer(
                self.rewrite_model_id,
                embedder=StyleEmbedder(self.embedder_model_id, device=self.device),
                device=self.device,
            )
        return self._inner.score(text)
