"""Change-point detection over sentence scores for mixed-authorship texts.

Finds the exact sentences where authorship switches (human -> AI or back)
using recursive binary segmentation with an SSE-reduction criterion — a
dependency-free variant of classic change-point detection. This upgrades
"some sentences are red" into "AI takes over at sentence 7".
"""

from __future__ import annotations

from dataclasses import dataclass

MIN_SEGMENT = 2  # sentences
MIN_CONTRAST = 0.15  # absolute floor for the mean-score gap between segments
CONTRAST_SIGMA = 1.5  # ...and the gap must exceed this many doc-level stdevs
MIN_GAIN = 0.005  # required per-sentence SSE reduction to accept a split


@dataclass
class Boundary:
    sentence_index: int  # boundary lies BEFORE this sentence
    direction: str  # "human_to_ai" | "ai_to_human"
    contrast: float  # |mean(after) - mean(before)|


def _sse(scores: list[float]) -> float:
    if not scores:
        return 0.0
    mean = sum(scores) / len(scores)
    return sum((s - mean) ** 2 for s in scores)


def _best_split(scores: list[float], start: int, end: int) -> tuple[int, float] | None:
    """Best single change-point in scores[start:end) by SSE reduction."""
    total = _sse(scores[start:end])
    best_gain, best_idx = 0.0, None
    for split in range(start + MIN_SEGMENT, end - MIN_SEGMENT + 1):
        gain = total - _sse(scores[start:split]) - _sse(scores[split:end])
        if gain > best_gain:
            best_gain, best_idx = gain, split
    if best_idx is None or best_gain < MIN_GAIN * (end - start):
        return None
    return best_idx, best_gain


def _segment(scores: list[float], start: int, end: int, splits: list[int]) -> None:
    found = _best_split(scores, start, end)
    if found is None:
        return
    idx, _ = found
    _segment(scores, start, idx, splits)
    splits.append(idx)
    _segment(scores, idx, end, splits)


def find_boundaries(sentence_scores: list[float]) -> list[Boundary]:
    """Return authorship-switch points between contrasting segments.

    A split counts as a boundary when the mean-score gap between adjacent
    segments clears both an absolute floor and an adaptive criterion scaled
    to the document's own score variability (so noisy-but-flat documents do
    not produce spurious boundaries).
    """
    n = len(sentence_scores)
    if n < 2 * MIN_SEGMENT:
        return []
    splits: list[int] = []
    _segment(sentence_scores, 0, n, splits)

    doc_std = (_sse(sentence_scores) / n) ** 0.5
    required = max(MIN_CONTRAST, CONTRAST_SIGMA * doc_std)

    boundaries: list[Boundary] = []
    edges = [0, *splits, n]
    for i in range(1, len(edges) - 1):
        before = sentence_scores[edges[i - 1] : edges[i]]
        after = sentence_scores[edges[i] : edges[i + 1]]
        mean_before = sum(before) / len(before)
        mean_after = sum(after) / len(after)
        contrast = abs(mean_after - mean_before)
        if contrast < required:
            continue
        boundaries.append(
            Boundary(
                sentence_index=edges[i],
                direction="human_to_ai" if mean_after > mean_before else "ai_to_human",
                contrast=round(contrast, 3),
            )
        )
    return boundaries


def is_mixed(sentence_scores: list[float], boundaries: list[Boundary]) -> bool:
    """Mixed authorship: boundary-separated segments with a human-leaning
    region on one side and a confidently-AI region on the other."""
    if not boundaries:
        return False
    edges = [0, *[b.sentence_index for b in boundaries], len(sentence_scores)]
    means = [
        sum(sentence_scores[edges[i] : edges[i + 1]])
        / max(len(sentence_scores[edges[i] : edges[i + 1]]), 1)
        for i in range(len(edges) - 1)
    ]
    return min(means) <= 0.45 and max(means) >= 0.75
