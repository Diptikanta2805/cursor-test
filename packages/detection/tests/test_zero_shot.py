from veritas_detection.binoculars import score_to_ai_probability
from veritas_detection.raidar import similarity_to_ai_probability


def test_binoculars_lower_score_means_more_ai():
    assert score_to_ai_probability(0.5) > score_to_ai_probability(1.2)
    assert score_to_ai_probability(0.5) > 0.85


def test_raidar_higher_similarity_means_more_ai():
    assert similarity_to_ai_probability(0.95) > similarity_to_ai_probability(0.7)
    assert similarity_to_ai_probability(0.88) > 0.4
