"""Ensemble combination and verdict calibration."""

from __future__ import annotations

import math
from dataclasses import dataclass

from veritas_detection.boundary import Boundary, is_mixed
from veritas_detection.classifier import prob_to_logit
from veritas_detection.conformal import ConformalThresholds

# Operating points map to conformal alpha levels: the AI threshold is the
# (1 - alpha) quantile of ensemble scores on human calibration text, giving a
# distribution-free FPR bound (see conformal.py). Human thresholds stay static.
OPERATING_POINTS = {
    "strict": {"alpha": 0.01, "human_threshold": 0.25},
    "balanced": {"alpha": 0.05, "human_threshold": 0.30},
}

# Logit-space ensemble weights. Supervised classifiers carry the prediction;
# the style-retrieval arm adds unseen-generator generalization; the
# statistical arm is a weak prior.
WEIGHT_FAST = 1.0
WEIGHT_DEEP = 1.6
WEIGHT_RETRIEVAL = 0.7
WEIGHT_STATISTICAL = 0.25

# Provisional (pre-deep) scores inside this band trigger the deep-tier
# cascade. The band is wide and asymmetric: any borderline or moderately
# positive score gets deep verification, because a false accusation is the
# most damaging error the product can make.
UNCERTAIN_LOW = 0.30
UNCERTAIN_HIGH = 0.92


@dataclass
class Verdict:
    label: str  # human | ai | mixed | inconclusive
    ai_probability: float
    confidence: str  # high | medium | low


def combine(
    fast_prob: float,
    deep_prob: float | None,
    statistical_prob: float | None,
    retrieval_prob: float | None = None,
) -> float:
    """Weighted logit-space average of available signals."""
    weighted: list[tuple[float, float]] = [(prob_to_logit(fast_prob), WEIGHT_FAST)]
    if deep_prob is not None:
        weighted.append((prob_to_logit(deep_prob), WEIGHT_DEEP))
    if retrieval_prob is not None:
        weighted.append((prob_to_logit(retrieval_prob), WEIGHT_RETRIEVAL))
    if statistical_prob is not None:
        weighted.append((prob_to_logit(statistical_prob), WEIGHT_STATISTICAL))
    total_weight = sum(w for _, w in weighted)
    logit = sum(v * w for v, w in weighted) / total_weight
    return 1.0 / (1.0 + math.exp(-logit))


def needs_deep_pass(provisional_prob: float) -> bool:
    return UNCERTAIN_LOW <= provisional_prob <= UNCERTAIN_HIGH


def decide(
    ai_probability: float,
    sentence_scores: list[float],
    operating_point: str = "balanced",
    word_count: int = 0,
    conformal: ConformalThresholds | None = None,
    boundaries: list[Boundary] | None = None,
) -> Verdict:
    point = OPERATING_POINTS.get(operating_point, OPERATING_POINTS["balanced"])
    human_threshold: float = point["human_threshold"]
    if conformal is not None:
        ai_threshold = conformal.ai_threshold(word_count, operating_point)
    else:
        ai_threshold = ConformalThresholds().ai_threshold(word_count, operating_point)

    # Mixed authorship: change-point boundaries with confident regions on
    # both sides beat any document-level average.
    if boundaries and is_mixed(sentence_scores, boundaries):
        return Verdict(label="mixed", ai_probability=ai_probability, confidence="medium")

    if ai_probability >= ai_threshold:
        confidence = "high" if ai_probability >= (ai_threshold + 1.0) / 2 else "medium"
        return Verdict(label="ai", ai_probability=ai_probability, confidence=confidence)
    if ai_probability <= human_threshold:
        confidence = "high" if ai_probability <= human_threshold / 2 else "medium"
        return Verdict(label="human", ai_probability=ai_probability, confidence=confidence)
    return Verdict(label="inconclusive", ai_probability=ai_probability, confidence="low")
