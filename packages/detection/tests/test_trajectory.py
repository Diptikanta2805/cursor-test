import numpy as np

from veritas_detection.trajectory import trajectory_signals


def _normalize(matrix):
    return matrix / np.linalg.norm(matrix, axis=1, keepdims=True)


def test_uniform_trajectory_scores_high_uniformity():
    rng = np.random.default_rng(0)
    base = rng.normal(size=(1, 64))
    # Windows drifting by a constant small step -> very regular trajectory.
    windows = _normalize(
        np.concatenate([base + 0.01 * i * np.ones((1, 64)) for i in range(10)])
    )
    signals = trajectory_signals(windows)
    assert signals["step_uniformity"] > 0.99
    assert signals["step_similarity_mean"] > 0.99


def test_erratic_trajectory_scores_lower_uniformity():
    rng = np.random.default_rng(1)
    windows = _normalize(rng.normal(size=(10, 64)))
    signals = trajectory_signals(windows)
    assert signals["step_uniformity"] < 0.99


def test_too_few_windows_returns_none():
    signals = trajectory_signals(np.ones((2, 8)))
    assert signals["step_similarity_mean"] is None
    assert signals["step_uniformity"] is None
