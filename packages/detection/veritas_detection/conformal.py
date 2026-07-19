"""Conformal calibration: distribution-free FPR bounds for the AI verdict.

Following the multiscaled conformal prediction framework (ACL 2025,
"Reliably Bounding False Positives"), the AI-verdict threshold is the
(1 - alpha) empirical quantile of final ensemble scores on a human-only
calibration set, stratified by document length. Under exchangeability this
bounds the false-positive rate by alpha — a guarantee, not a tuning choice.

The calibration artifact is produced by `packages/training/calibrate.py`
and shipped with the package; when absent, static fallback thresholds apply.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

DEFAULT_CALIBRATION_PATH = Path(__file__).parent / "assets" / "conformal.json"

# Fallbacks when no calibration artifact is available.
FALLBACK_THRESHOLDS = {"strict": 0.90, "balanced": 0.70}


class ConformalThresholds:
    def __init__(self, path: str | Path = DEFAULT_CALIBRATION_PATH) -> None:
        self.buckets: list[dict] = []
        self.meta: dict = {}
        path = Path(path)
        if path.exists():
            data = json.loads(path.read_text())
            self.buckets = data["buckets"]
            self.meta = data.get("meta", {})
            logger.info(
                "Loaded conformal calibration: %d length buckets from %s human docs",
                len(self.buckets),
                self.meta.get("n_calibration_docs", "?"),
            )
        else:
            logger.warning("No conformal calibration artifact; using fallbacks")

    def ai_threshold(self, word_count: int, operating_point: str) -> float:
        """Threshold above which the AI verdict is issued.

        strict -> alpha=0.01 quantile, balanced -> alpha=0.05 quantile.
        """
        for bucket in self.buckets:
            if bucket["min_words"] <= word_count < bucket["max_words"]:
                value = bucket["thresholds"].get(operating_point)
                if value is not None:
                    # Never accuse below coin-flip regardless of calibration.
                    return max(float(value), 0.5)
        return FALLBACK_THRESHOLDS.get(operating_point, 0.70)
