# /// script
# requires-python = ">=3.11"
# dependencies = ["torch", "transformers", "numpy", "pysbd"]
# ///
"""Conformal calibration of the AI-verdict thresholds.

Runs the FULL production pipeline (all arms, deep cascade enabled) over a
human-only calibration set that is disjoint from the style-index data, then
records the (1 - alpha) empirical score quantiles per document-length bucket:
alpha = 0.05 -> "balanced", alpha = 0.01 -> "strict". Under exchangeability
these thresholds bound the false-positive rate by alpha (multiscaled
conformal prediction, ACL 2025).

Usage: python packages/training/calibrate.py
"""

from __future__ import annotations

import json
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "detection"))

from veritas_detection.classifier import DeepClassifier, FastClassifier  # noqa: E402
from veritas_detection.conformal import DEFAULT_CALIBRATION_PATH  # noqa: E402
from veritas_detection.normalize import normalize_text, word_count  # noqa: E402
from veritas_detection.perplexity import PerplexityScorer  # noqa: E402
from veritas_detection.pipeline import DetectionPipeline  # noqa: E402
from veritas_detection.retrieval import StyleEmbedder, StyleRetrieval  # noqa: E402

API = "https://datasets-server.huggingface.co"
MIN_WORDS = 50
BUCKETS = [(50, 100), (100, 200), (200, 100_000)]
# Offsets deliberately disjoint from build_style_index.py fetches.
SOURCES = [
    ("Hello-SimpleAI/HC3", "all", "train", "human_answers", (5000, 5100, 5200)),
    ("stanfordnlp/imdb", "plain_text", "train", "text", (1000, 1100, 1200)),
    ("abisee/cnn_dailymail", "3.0.0", "train", "article", (500, 600)),
    ("rajpurkar/squad", "plain_text", "train", "context", (2000, 2200)),
]


def fetch_rows(dataset: str, config: str, split: str, offset: int) -> list[dict]:
    url = (
        f"{API}/rows?dataset={urllib.parse.quote(dataset)}"
        f"&config={config}&split={split}&offset={offset}&length=100"
    )
    with urllib.request.urlopen(url, timeout=60) as response:
        return [r["row"] for r in json.load(response)["rows"]]


def collect_human_texts(per_source: int = 220) -> list[str]:
    texts: list[str] = []
    seen: set[str] = set()
    for dataset, config, split, column, offsets in SOURCES:
        count = 0
        for offset in offsets:
            for row in fetch_rows(dataset, config, split, offset):
                if count >= per_source:
                    break
                values = row.get(column)
                values = values if isinstance(values, list) else [values]
                for value in values:
                    text = normalize_text(value or "")
                    if word_count(text) < MIN_WORDS or text[:200] in seen:
                        continue
                    seen.add(text[:200])
                    texts.append(text[:8000])
                    count += 1
                    if count >= per_source:
                        break
        print(f"{dataset}: {count}")
    return texts


def main() -> None:
    texts = collect_human_texts()
    print(f"\nCalibration set: {len(texts)} human documents")

    pipeline = DetectionPipeline(
        fast_classifier=FastClassifier("MayZhou/e5-small-lora-ai-generated-detector"),
        deep_classifier=DeepClassifier("desklib/ai-text-detector-v1.01"),
        perplexity_scorer=PerplexityScorer("distilgpt2"),
        style_retrieval=StyleRetrieval(StyleEmbedder()),
    )

    scores_by_bucket: dict[tuple[int, int], list[float]] = {b: [] for b in BUCKETS}
    for i, text in enumerate(texts):
        result = pipeline.scan(text)
        if result.verdict == "too_short":
            continue
        for low, high in BUCKETS:
            if low <= result.word_count < high:
                scores_by_bucket[(low, high)].append(result.ai_probability)
                break
        if (i + 1) % 50 == 0:
            print(f"  scored {i + 1}/{len(texts)}")

    buckets_out = []
    for (low, high), scores in scores_by_bucket.items():
        if len(scores) < 60:
            print(f"bucket {low}-{high}: only {len(scores)} docs, skipping (fallback applies)")
            continue
        arr = np.array(scores)
        thresholds = {
            "balanced": round(float(np.quantile(arr, 0.95)), 4),
            "strict": round(float(np.quantile(arr, 0.99)), 4),
        }
        buckets_out.append(
            {
                "min_words": low,
                "max_words": high,
                "n_docs": len(scores),
                "thresholds": thresholds,
            }
        )
        print(
            f"bucket {low}-{high}: n={len(scores)} "
            f"q95={thresholds['balanced']} q99={thresholds['strict']}"
        )

    DEFAULT_CALIBRATION_PATH.parent.mkdir(parents=True, exist_ok=True)
    DEFAULT_CALIBRATION_PATH.write_text(
        json.dumps(
            {
                "meta": {
                    "created_at": datetime.now(timezone.utc).isoformat(),
                    "n_calibration_docs": sum(len(s) for s in scores_by_bucket.values()),
                    "sources": [s[0] for s in SOURCES],
                    "alphas": {"balanced": 0.05, "strict": 0.01},
                },
                "buckets": buckets_out,
            },
            indent=2,
        )
    )
    print(f"Wrote {DEFAULT_CALIBRATION_PATH}")


if __name__ == "__main__":
    main()
