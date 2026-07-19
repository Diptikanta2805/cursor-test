from veritas_detection.segment import (
    build_windows,
    sentence_scores_from_windows,
    split_sentences,
)

TEXT = (
    "This is the first sentence. Here comes a second one! "
    "A third sentence follows. And now a fourth. Finally the fifth."
)


def test_split_sentences_offsets_match_source():
    sentences = split_sentences(TEXT)
    assert len(sentences) == 5
    for s in sentences:
        assert TEXT[s.start : s.end] == s.text


def test_windows_cover_all_sentences():
    sentences = split_sentences(TEXT)
    windows = build_windows(sentences, size=3, stride=1)
    assert len(windows) == 3
    covered = {i for w in windows for i in w.sentence_indices}
    assert covered == set(range(5))


def test_short_document_yields_single_window():
    sentences = split_sentences("Only one sentence here.")
    windows = build_windows(sentences, size=3, stride=1)
    assert len(windows) == 1
    assert windows[0].sentence_indices == [0]


def test_sentence_scores_average_and_smooth():
    sentences = split_sentences(TEXT)
    windows = build_windows(sentences, size=3, stride=1)
    scores = sentence_scores_from_windows(windows, [0.0, 0.5, 1.0], len(sentences))
    assert len(scores) == 5
    assert all(0.0 <= s <= 1.0 for s in scores)
    assert scores[0] < scores[-1]  # rising window scores -> rising sentence scores
