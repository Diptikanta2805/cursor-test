"""API test fixtures: stub detection pipeline (no model downloads) + temp DB."""

import os
import sys
from pathlib import Path

os.environ.setdefault("VERITAS_DATABASE_URL", "sqlite:///./test_veritas.db")
os.environ.setdefault("VERITAS_ADMIN_TOKEN", "test-admin-token")
os.environ.setdefault("VERITAS_ANONYMOUS_DAILY_LIMIT", "10")
os.environ.setdefault("VERITAS_RATE_LIMIT", "1000/minute")

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from veritas_detection.pipeline import ScanResult, SentenceResult  # noqa: E402


class StubPipeline:
    """Deterministic pipeline: 'robot' texts read as AI, others as human."""

    def scan(self, text, mode="fast", operating_point="balanced"):
        n_words = len(text.split())
        if n_words < 50:
            return ScanResult(
                verdict="too_short",
                ai_probability=0.5,
                confidence="low",
                operating_point=operating_point,
                word_count=n_words,
                warning="too short",
            )
        is_ai = "robot" in text.lower()
        prob = 0.93 if is_ai else 0.04
        return ScanResult(
            verdict="ai" if is_ai else "human",
            ai_probability=prob,
            confidence="high",
            operating_point=operating_point,
            sentences=[SentenceResult(text=text[:40], start=0, end=40, score=prob)],
            signals={"fast_classifier": prob, "style_retrieval": prob},
            attribution={"generator": "chatgpt", "share": 0.8} if is_ai else None,
            boundaries=(
                [{"sentence_index": 1, "direction": "human_to_ai", "contrast": 0.8}]
                if is_ai
                else []
            ),
            mode_used=mode,
            word_count=n_words,
            duration_ms=5,
        )


@pytest.fixture(scope="session")
def client():
    for db_file in ("test_veritas.db",):
        if os.path.exists(db_file):
            os.remove(db_file)
    from app import engine as engine_module

    engine_module._pipeline = StubPipeline()  # bypass model loading
    from app.main import app

    with TestClient(app) as test_client:
        yield test_client
