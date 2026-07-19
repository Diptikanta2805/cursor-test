"""Text normalization that neutralizes common detector-evasion tricks.

Handles the character-level adversarial attacks catalogued by the RAID
benchmark (homoglyphs, zero-width spaces, whitespace injection) before any
model sees the text, so those attacks cannot flip a prediction.
"""

from __future__ import annotations

import re
import unicodedata

# Zero-width and invisible characters used in "zero-width space" attacks.
_INVISIBLE = dict.fromkeys(
    [0x200B, 0x200C, 0x200D, 0x2060, 0xFEFF, 0x00AD, 0x180E, 0x034F],
)

# Common Cyrillic/Greek homoglyphs mapped back to ASCII. This covers the
# characters used by the RAID homoglyph attack and popular "humanizer" tools.
_HOMOGLYPHS = str.maketrans(
    {
        "а": "a", "е": "e", "о": "o", "р": "p", "с": "c", "х": "x", "у": "y",
        "і": "i", "ѕ": "s", "ј": "j", "ԁ": "d", "ɡ": "g", "ո": "n", "ᴏ": "o",
        "А": "A", "В": "B", "Е": "E", "К": "K", "М": "M", "Н": "H", "О": "O",
        "Р": "P", "С": "C", "Т": "T", "Х": "X", "α": "a", "ο": "o", "ν": "v",
        "„": '"', "“": '"', "”": '"', "‘": "'", "’": "'", "‚": "'",
        "–": "-", "—": "-", "…": "...",
    }
)

_WHITESPACE_RE = re.compile(r"[ \t\u00A0\u2000-\u200A\u202F\u205F\u3000]+")
_MULTI_NEWLINE_RE = re.compile(r"\n{3,}")


def normalize_text(text: str) -> str:
    """Return canonicalized text safe to feed to detectors."""
    text = text.translate(_INVISIBLE)
    text = unicodedata.normalize("NFKC", text)
    text = text.translate(_HOMOGLYPHS)
    text = _WHITESPACE_RE.sub(" ", text)
    text = _MULTI_NEWLINE_RE.sub("\n\n", text)
    lines = [line.strip() for line in text.split("\n")]
    return "\n".join(lines).strip()


def word_count(text: str) -> int:
    return len(text.split())
