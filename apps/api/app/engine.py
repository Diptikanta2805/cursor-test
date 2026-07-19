"""Detection pipeline singleton, loaded once at startup."""

from __future__ import annotations

import logging

import torch

from app.config import get_settings
from veritas_detection.classifier import DeepClassifier, FastClassifier
from veritas_detection.perplexity import PerplexityScorer
from veritas_detection.pipeline import DetectionPipeline
from veritas_detection.retrieval import (
    DEFAULT_INDEX_PATH,
    StyleEmbedder,
    StyleRetrieval,
)

logger = logging.getLogger(__name__)

_pipeline: DetectionPipeline | None = None


def load_pipeline() -> DetectionPipeline:
    global _pipeline
    if _pipeline is not None:
        return _pipeline
    settings = get_settings()
    torch.set_num_threads(max(torch.get_num_threads(), 4))

    fast = FastClassifier(settings.fast_model_id, device=settings.device)

    deep = None
    if settings.enable_deep_tier:
        try:
            deep = DeepClassifier(settings.deep_model_id, device=settings.device)
        except Exception:  # noqa: BLE001 - degrade to fast tier if download fails
            logger.exception("Deep tier failed to load; continuing with fast tier only")

    perplexity = None
    if settings.enable_perplexity:
        try:
            perplexity = PerplexityScorer(
                settings.perplexity_model_id, device=settings.device
            )
        except Exception:  # noqa: BLE001
            logger.exception("Perplexity scorer failed to load; continuing without it")

    retrieval = None
    if settings.enable_retrieval:
        try:
            embedder = StyleEmbedder(settings.embedder_model_id, device=settings.device)
            retrieval = StyleRetrieval(
                embedder, index_path=settings.style_index_path or DEFAULT_INDEX_PATH
            )
        except Exception:  # noqa: BLE001
            logger.exception("Style retrieval failed to load; continuing without it")

    _pipeline = DetectionPipeline(fast, deep, perplexity, retrieval)
    logger.info("Detection pipeline ready")
    return _pipeline


def get_pipeline() -> DetectionPipeline:
    if _pipeline is None:
        return load_pipeline()
    return _pipeline
