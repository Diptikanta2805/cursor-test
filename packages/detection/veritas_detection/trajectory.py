"""Semantic-trajectory statistics (GTCL-inspired, training-free variant).

Models the document as a trajectory of window embeddings and measures the
regularity of semantic transitions: autoregressive generation tends to move
through meaning space in uniform steps, while human writing takes irregular
ones. This is the untrained statistical cousin of GTCL (arXiv:2607.14967);
it is surfaced as a transparent signal and validated empirically before
receiving any ensemble weight.
"""

from __future__ import annotations

import numpy as np


def trajectory_signals(window_embeddings: np.ndarray) -> dict[str, float | None]:
    """Statistics over consecutive-window cosine steps.

    Args:
        window_embeddings: (n_windows, dim) L2-normalized embeddings.

    Returns:
        step_similarity_mean: average cosine similarity of consecutive windows.
        step_uniformity: 1 - stdev of consecutive similarities (1.0 = perfectly
            regular semantic progression, lower = burstier trajectory).
    """
    if window_embeddings is None or len(window_embeddings) < 3:
        return {"step_similarity_mean": None, "step_uniformity": None}
    steps = np.sum(window_embeddings[:-1] * window_embeddings[1:], axis=1)
    return {
        "step_similarity_mean": round(float(steps.mean()), 4),
        "step_uniformity": round(float(1.0 - steps.std()), 4),
    }
