"""End-to-end detection pipeline.

Flow per document:
  normalize -> length check -> sentence split -> full-doc + window scoring
  with the fast classifier -> style-retrieval arm (kNN + attribution) +
  trajectory statistics over window embeddings -> statistical signals ->
  optional deep-tier cascade when the provisional ensemble is uncertain (or
  mode="deep") -> ensemble -> change-point boundary detection -> conformally
  calibrated verdict with sentence-level highlighting.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from typing import Literal

from veritas_detection import ensemble
from veritas_detection.boundary import find_boundaries
from veritas_detection.classifier import DeepClassifier, FastClassifier
from veritas_detection.conformal import ConformalThresholds
from veritas_detection.normalize import normalize_text, word_count
from veritas_detection.perplexity import PerplexityScorer
from veritas_detection.retrieval import StyleRetrieval
from veritas_detection.segment import (
    build_windows,
    sentence_scores_from_windows,
    split_sentences,
)
from veritas_detection.trajectory import trajectory_signals

logger = logging.getLogger(__name__)

MIN_WORDS = 50
MAX_CHARS = 60_000

Mode = Literal["fast", "deep"]


@dataclass
class SentenceResult:
    text: str
    start: int
    end: int
    score: float


@dataclass
class ScanResult:
    verdict: str
    ai_probability: float
    confidence: str
    operating_point: str
    sentences: list[SentenceResult] = field(default_factory=list)
    signals: dict = field(default_factory=dict)
    attribution: dict | None = None
    boundaries: list[dict] = field(default_factory=list)
    mode_used: str = "fast"
    word_count: int = 0
    duration_ms: int = 0
    warning: str | None = None


class DetectionPipeline:
    def __init__(
        self,
        fast_classifier: FastClassifier,
        deep_classifier: DeepClassifier | None = None,
        perplexity_scorer: PerplexityScorer | None = None,
        style_retrieval: StyleRetrieval | None = None,
        conformal: ConformalThresholds | None = None,
        window_size: int = 3,
        window_stride: int = 1,
    ) -> None:
        self.fast = fast_classifier
        self.deep = deep_classifier
        self.perplexity = perplexity_scorer
        self.retrieval = style_retrieval
        self.conformal = conformal or ConformalThresholds()
        self.window_size = window_size
        self.window_stride = window_stride

    def scan(
        self,
        text: str,
        mode: Mode = "fast",
        operating_point: str = "balanced",
    ) -> ScanResult:
        started = time.perf_counter()
        normalized = normalize_text(text)[:MAX_CHARS]
        n_words = word_count(normalized)
        if n_words < MIN_WORDS:
            return ScanResult(
                verdict="too_short",
                ai_probability=0.5,
                confidence="low",
                operating_point=operating_point,
                word_count=n_words,
                duration_ms=int((time.perf_counter() - started) * 1000),
                warning=(
                    f"Document has {n_words} words; at least {MIN_WORDS} are "
                    "required for a reliable verdict."
                ),
            )

        sentences = split_sentences(normalized)
        windows = build_windows(sentences, self.window_size, self.window_stride)

        # One batched call scores the full document plus every window.
        fast_scores = self.fast.score([normalized] + [w.text for w in windows])
        fast_doc_prob = fast_scores[0]
        window_scores = fast_scores[1:]
        sentence_scores = sentence_scores_from_windows(
            windows, window_scores, len(sentences)
        )

        signals: dict = {"fast_classifier": round(fast_doc_prob, 4)}
        attribution: dict | None = None

        # Style-retrieval arm: one batched embed of doc + windows, reused for
        # the kNN vote and the trajectory statistics.
        retrieval_prob = None
        if self.retrieval is not None:
            embeddings = self.retrieval.embedder.embed(
                [normalized] + [w.text for w in windows]
            )
            retrieved = self.retrieval.score(normalized, doc_embedding=embeddings[0])
            retrieval_prob = retrieved.ai_probability
            signals["style_retrieval"] = round(retrieval_prob, 4)
            signals["neighbor_similarity"] = retrieved.mean_neighbor_similarity
            if retrieved.attributed_generator is not None:
                attribution = {
                    "generator": retrieved.attributed_generator,
                    "share": retrieved.attribution_share,
                }
            signals.update(trajectory_signals(embeddings[1:]))

        statistical_prob = None
        if self.perplexity is not None:
            stat_signals = self.perplexity.signals(
                normalized, [s.text for s in sentences]
            )
            statistical_prob = self.perplexity.ai_likelihood(stat_signals)
            signals.update(
                {
                    key: (round(value, 3) if value is not None else None)
                    for key, value in stat_signals.items()
                }
            )
            if statistical_prob is not None:
                signals["statistical_likelihood"] = round(statistical_prob, 4)

        # Cascade decision uses the provisional ensemble (all cheap arms): if
        # they disagree or sit near the boundary, the deep model arbitrates.
        provisional = ensemble.combine(
            fast_doc_prob, None, statistical_prob, retrieval_prob
        )
        deep_prob = None
        mode_used: str = "fast"
        run_deep = self.deep is not None and (
            mode == "deep" or ensemble.needs_deep_pass(provisional)
        )
        if run_deep:
            deep_prob = self.deep.score([normalized])[0]
            signals["deep_classifier"] = round(deep_prob, 4)
            mode_used = "deep"

        ai_probability = ensemble.combine(
            fast_doc_prob, deep_prob, statistical_prob, retrieval_prob
        )
        boundaries = find_boundaries(sentence_scores)
        verdict = ensemble.decide(
            ai_probability,
            sentence_scores,
            operating_point,
            word_count=n_words,
            conformal=self.conformal,
            boundaries=boundaries,
        )

        return ScanResult(
            verdict=verdict.label,
            ai_probability=round(ai_probability, 4),
            confidence=verdict.confidence,
            operating_point=operating_point,
            sentences=[
                SentenceResult(
                    text=s.text, start=s.start, end=s.end, score=round(score, 4)
                )
                for s, score in zip(sentences, sentence_scores)
            ],
            signals=signals,
            attribution=attribution if verdict.label in ("ai", "mixed") else None,
            boundaries=[b.__dict__ for b in boundaries],
            mode_used=mode_used,
            word_count=n_words,
            duration_ms=int((time.perf_counter() - started) * 1000),
        )
