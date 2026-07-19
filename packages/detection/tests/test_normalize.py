from veritas_detection.normalize import normalize_text, word_count


def test_removes_zero_width_characters():
    attacked = "The\u200b quick\u200c brown\ufeff fox"
    assert normalize_text(attacked) == "The quick brown fox"


def test_maps_cyrillic_homoglyphs_to_ascii():
    # 'а', 'е', 'о' below are Cyrillic lookalikes (RAID homoglyph attack).
    attacked = "Th\u0435 c\u0430t s\u043et"
    assert normalize_text(attacked) == "The cat sot"


def test_collapses_injected_whitespace():
    attacked = "word\u00a0\u2009 word   word"
    assert normalize_text(attacked) == "word word word"


def test_normalizes_smart_quotes_and_dashes():
    assert normalize_text("\u201cHi\u201d \u2014 there\u2019s") == '"Hi" - there\'s'


def test_word_count():
    assert word_count("one two three") == 3
