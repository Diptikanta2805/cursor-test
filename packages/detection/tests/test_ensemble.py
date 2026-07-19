from veritas_detection import ensemble


def test_combine_single_signal_is_identity():
    assert abs(ensemble.combine(0.9, None, None) - 0.9) < 1e-6


def test_deep_signal_dominates_fast():
    combined = ensemble.combine(0.5, 0.95, None)
    assert combined > 0.75


def test_statistical_signal_has_small_weight():
    combined = ensemble.combine(0.9, None, 0.1)
    assert combined > 0.75  # weak prior barely moves a confident classifier


def test_uncertain_band():
    assert ensemble.needs_deep_pass(0.5)
    assert not ensemble.needs_deep_pass(0.9)
    assert not ensemble.needs_deep_pass(0.1)


def test_decide_ai_and_human_verdicts():
    assert ensemble.decide(0.95, [0.9] * 10).label == "ai"
    assert ensemble.decide(0.05, [0.1] * 10).label == "human"
    assert ensemble.decide(0.5, [0.5] * 10).label == "inconclusive"


def test_decide_mixed_when_both_regions_confident():
    scores = [0.95] * 5 + [0.05] * 5
    assert ensemble.decide(0.55, scores).label == "mixed"


def test_strict_operating_point_raises_ai_bar():
    assert ensemble.decide(0.8, [0.8] * 10, "balanced").label == "ai"
    assert ensemble.decide(0.8, [0.8] * 10, "strict").label == "inconclusive"
