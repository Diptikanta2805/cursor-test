"""Ensemble combination and verdict calibration."""

from __future__ import annotations

import math
from dataclasses import dataclass

from veritas_detection.classifier import prob_to_logit

# Operating points: threshold above which a document is called AI, chosen to
# hit a target false-positive rate on held-out human text. "strict" trades
# recall for a lower FPR (safer for high-stakes use).
OPERATING_POINTS = {
    "strict": {"target_fpr": 0.01, "ai_threshold": 0.90, "human_threshold": 0.25},
    "balanced": {"target_fpr": 0.05, "ai_threshold": 0.70, "human_threshold": 0.30},
}

# Logit-space ensemble weights. The supervised classifiers carry the
# prediction; the statistical arm is a weak prior that helps on generators
# the classifiers never saw.
WEIGHT_FAST = 1.0
WEIGHT_DEEP = 1.6
WEIGHT_STATISTICAL = 0.25

# Fast-tier scores inside this band trigger the deep-tier cascade.
UNCERTAIN_LOW = 0.35
UNCERTAIN_HIGH = 0.65


@dataclass
class Verdict:
    label: str  # human | ai | mixed | inconclusive
    ai_probability: float
    confidence: str  # high | medium | low


def combine(
    fast_prob: float,
    deep_prob: float | None,
    statistical_prob: float | None,
) -> float:
    """Weighted logit-space average of available signals."""
    weighted: list[tuple[float, float]] = [(prob_to_logit(fast_prob), WEIGHT_FAST)]
    if deep_prob is not None:
        weighted.append((prob_to_logit(deep_prob), WEIGHT_DEEP))
    if statistical_prob is not None:
        weighted.append((prob_to_logit(statistical_prob), WEIGHT_STATISTICAL))
    total_weight = sum(w for _, w in weighted)
    logit = sum(v * w for v, w in weighted) / total_weight
    return 1.0 / (1.0 + math.exp(-logit))


def needs_deep_pass(fast_prob: float) -> bool:
    return UNCERTAIN_LOW <= fast_prob <= UNCERTAIN_HIGH


def decide(
    ai_probability: float,
    sentence_scores: list[float],
    operating_point: str = "balanced",
) -> Verdict:
    point = OPERATING_POINTS.get(operating_point, OPERATING_POINTS["balanced"])
    ai_threshold: float = point["ai_threshold"]
    human_threshold: float = point["human_threshold"]

    # Mixed detection: confident AI and confident human regions coexisting.
    if len(sentence_scores) >= 4:
        n_ai = sum(1 for s in sentence_scores if s >= 0.75)
        n_human = sum(1 for s in sentence_scores if s <= 0.25)
        share_ai = n_ai / len(sentence_scores)
        share_human = n_human / len(sentence_scores)
        if share_ai >= 0.2 and share_human >= 0.2:
            return Verdict(label="mixed", ai_probability=ai_probability, confidence="medium")

    if ai_probability >= ai_threshold:
        confidence = "high" if ai_probability >= (ai_threshold + 1.0) / 2 else "medium"
        return Verdict(label="ai", ai_probability=ai_probability, confidence=confidence)
    if ai_probability <= human_threshold:
        confidence = "high" if ai_probability <= human_threshold / 2 else "medium"
        return Verdict(label="human", ai_probability=ai_probability, confidence=confidence)
    return Verdict(label="inconclusive", ai_probability=ai_probability, confidence="low")
