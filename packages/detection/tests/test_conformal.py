import json

from veritas_detection.conformal import ConformalThresholds


def _write_calibration(tmp_path):
    path = tmp_path / "conformal.json"
    path.write_text(
        json.dumps(
            {
                "meta": {"n_calibration_docs": 600},
                "buckets": [
                    {
                        "min_words": 50,
                        "max_words": 100,
                        "n_docs": 200,
                        "thresholds": {"balanced": 0.81, "strict": 0.93},
                    },
                    {
                        "min_words": 100,
                        "max_words": 100000,
                        "n_docs": 400,
                        "thresholds": {"balanced": 0.72, "strict": 0.88},
                    },
                ],
            }
        )
    )
    return path


def test_bucket_lookup(tmp_path):
    thresholds = ConformalThresholds(_write_calibration(tmp_path))
    assert thresholds.ai_threshold(80, "balanced") == 0.81
    assert thresholds.ai_threshold(80, "strict") == 0.93
    assert thresholds.ai_threshold(500, "balanced") == 0.72


def test_fallback_when_artifact_missing(tmp_path):
    thresholds = ConformalThresholds(tmp_path / "missing.json")
    assert thresholds.ai_threshold(80, "balanced") == 0.70
    assert thresholds.ai_threshold(80, "strict") == 0.90


def test_threshold_floor_at_half(tmp_path):
    path = tmp_path / "degenerate.json"
    path.write_text(
        json.dumps(
            {
                "buckets": [
                    {
                        "min_words": 50,
                        "max_words": 100000,
                        "thresholds": {"balanced": 0.2},
                    }
                ]
            }
        )
    )
    assert ConformalThresholds(path).ai_threshold(80, "balanced") == 0.5
