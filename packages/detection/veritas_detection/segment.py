"""Sentence segmentation and sliding-window construction."""

from __future__ import annotations

from dataclasses import dataclass

import pysbd

_SEGMENTER = pysbd.Segmenter(language="en", clean=False)


@dataclass
class Sentence:
    text: str
    start: int  # character offset in the normalized document
    end: int


@dataclass
class Window:
    """A window of consecutive sentences scored as one unit."""

    text: str
    sentence_indices: list[int]


def split_sentences(text: str) -> list[Sentence]:
    sentences: list[Sentence] = []
    cursor = 0
    for raw in _SEGMENTER.segment(text):
        chunk = raw.strip()
        if not chunk:
            continue
        start = text.find(chunk, cursor)
        if start == -1:  # pysbd may alter whitespace; fall back to cursor
            start = cursor
        end = start + len(chunk)
        cursor = end
        sentences.append(Sentence(text=chunk, start=start, end=end))
    return sentences


def build_windows(
    sentences: list[Sentence], size: int = 3, stride: int = 1
) -> list[Window]:
    """Overlapping windows of `size` sentences, advancing by `stride`."""
    if not sentences:
        return []
    if len(sentences) <= size:
        return [
            Window(
                text=" ".join(s.text for s in sentences),
                sentence_indices=list(range(len(sentences))),
            )
        ]
    windows: list[Window] = []
    for start in range(0, len(sentences) - size + 1, stride):
        indices = list(range(start, start + size))
        windows.append(
            Window(
                text=" ".join(sentences[i].text for i in indices),
                sentence_indices=indices,
            )
        )
    return windows


def sentence_scores_from_windows(
    windows: list[Window], window_scores: list[float], n_sentences: int
) -> list[float]:
    """Average overlapping window scores back onto sentences, then smooth."""
    totals = [0.0] * n_sentences
    counts = [0] * n_sentences
    for window, score in zip(windows, window_scores):
        for i in window.sentence_indices:
            totals[i] += score
            counts[i] += 1
    scores = [t / c if c else 0.5 for t, c in zip(totals, counts)]
    return _smooth(scores)


def _smooth(scores: list[float]) -> list[float]:
    """3-tap [0.25, 0.5, 0.25] filter to suppress single-sentence noise."""
    if len(scores) < 3:
        return scores
    smoothed = [scores[0]]
    for i in range(1, len(scores) - 1):
        smoothed.append(0.25 * scores[i - 1] + 0.5 * scores[i] + 0.25 * scores[i + 1])
    smoothed.append(scores[-1])
    return smoothed
