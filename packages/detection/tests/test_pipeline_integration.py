"""Integration tests with real models. Slow; requires model downloads.

Run with: VERITAS_RUN_MODEL_TESTS=1 pytest packages/detection/tests/test_pipeline_integration.py
"""

import os

import pytest

pytestmark = pytest.mark.skipif(
    os.environ.get("VERITAS_RUN_MODEL_TESTS") != "1",
    reason="set VERITAS_RUN_MODEL_TESTS=1 to run model integration tests",
)

HUMAN_TEXT = """
Look, I don't really know how to explain what happened at the lake that summer.
My cousin Ray swore the fish were biting before dawn, so we dragged ourselves
out of bed at four, stole granddad's thermos, and rowed out in that leaky green
canoe with one paddle between us. The fog sat so thick on the water you
couldn't see the end of your own line. Ray talked the entire time, which he
always does when he's nervous, mostly about a girl from Duluth he'd met twice.
We caught nothing. Not one fish. Around seven the sun burned through and we
just sat there, cold and laughing at ourselves, and honestly it's still one of
the best mornings I can remember.
"""

AI_TEXT = """
Artificial intelligence has fundamentally transformed the landscape of modern
technology, offering unprecedented opportunities for innovation across diverse
industries. From healthcare to finance, organizations are leveraging machine
learning algorithms to streamline operations, enhance decision-making
processes, and deliver personalized experiences to their customers. As these
technologies continue to evolve, it is essential for businesses to adopt a
strategic approach to implementation, ensuring that ethical considerations and
data privacy remain at the forefront of their initiatives. Ultimately, the
successful integration of AI depends on striking a balance between automation
and human oversight, fostering a collaborative environment where technology
augments rather than replaces human expertise.
"""


@pytest.fixture(scope="module")
def pipeline():
    from veritas_detection.classifier import FastClassifier
    from veritas_detection.perplexity import PerplexityScorer
    from veritas_detection.pipeline import DetectionPipeline

    fast = FastClassifier("MayZhou/e5-small-lora-ai-generated-detector")
    perplexity = PerplexityScorer("distilgpt2")
    return DetectionPipeline(fast, None, perplexity)


def test_human_text_scores_low(pipeline):
    result = pipeline.scan(HUMAN_TEXT)
    assert result.ai_probability < 0.5
    assert result.verdict in {"human", "inconclusive"}


def test_ai_text_scores_high(pipeline):
    result = pipeline.scan(AI_TEXT)
    assert result.ai_probability > 0.5
    assert result.verdict in {"ai", "inconclusive"}


def test_homoglyph_attack_does_not_flip_verdict(pipeline):
    attacked = AI_TEXT.replace("a", "\u0430").replace("e", "\u0435")
    clean = pipeline.scan(AI_TEXT)
    adversarial = pipeline.scan(attacked)
    assert abs(clean.ai_probability - adversarial.ai_probability) < 0.15


def test_sentence_scores_present(pipeline):
    result = pipeline.scan(AI_TEXT)
    assert len(result.sentences) >= 4
    assert all(0.0 <= s.score <= 1.0 for s in result.sentences)
