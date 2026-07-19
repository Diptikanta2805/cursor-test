from veritas_detection.boundary import find_boundaries, is_mixed


def test_clean_switch_detected():
    scores = [0.1, 0.12, 0.08, 0.15, 0.9, 0.92, 0.88, 0.95]
    boundaries = find_boundaries(scores)
    assert len(boundaries) == 1
    assert boundaries[0].sentence_index == 4
    assert boundaries[0].direction == "human_to_ai"
    assert boundaries[0].contrast > 0.7


def test_reverse_switch_direction():
    scores = [0.9, 0.95, 0.88, 0.1, 0.05, 0.12]
    boundaries = find_boundaries(scores)
    assert len(boundaries) == 1
    assert boundaries[0].direction == "ai_to_human"


def test_uniform_scores_no_boundary():
    assert find_boundaries([0.9] * 10) == []
    assert find_boundaries([0.1, 0.12, 0.09, 0.11, 0.1, 0.13]) == []


def test_small_fluctuations_ignored():
    scores = [0.4, 0.45, 0.5, 0.55, 0.5, 0.45, 0.42, 0.48]
    assert find_boundaries(scores) == []


def test_too_few_sentences():
    assert find_boundaries([0.1, 0.9]) == []


def test_double_switch():
    scores = [0.1, 0.1, 0.1, 0.9, 0.9, 0.9, 0.1, 0.1, 0.1]
    boundaries = find_boundaries(scores)
    assert len(boundaries) == 2
    assert [b.direction for b in boundaries] == ["human_to_ai", "ai_to_human"]


def test_is_mixed_requires_both_regions():
    switch = [0.1, 0.1, 0.1, 0.9, 0.9, 0.9]
    boundaries = find_boundaries(switch)
    assert is_mixed(switch, boundaries)
    assert not is_mixed([0.9] * 6, [])
