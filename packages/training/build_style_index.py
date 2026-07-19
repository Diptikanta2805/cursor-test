# /// script
# requires-python = ">=3.11"
# dependencies = ["torch", "transformers", "numpy"]
# ///
"""Build the style-retrieval reference index from free public datasets.

Sources (all fetched through the free Hugging Face datasets-server API):
  - RAID (liamdugan/raid): multi-generator AI text (7 LLM families, no
    adversarial attacks) + human references across 8 domains.
  - HC3 (Hello-SimpleAI/HC3): ChatGPT vs human QA pairs.
  - IMDB, CNN/DailyMail, SQuAD contexts: additional human-register diversity
    (reviews, journalism, encyclopedic prose).

Output: veritas_detection/assets/style_index.npz with float16 normalized
embeddings, binary labels, and generator tags for attribution.

Usage: python packages/training/build_style_index.py
"""

from __future__ import annotations

import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "detection"))

from veritas_detection.normalize import normalize_text, word_count  # noqa: E402
from veritas_detection.retrieval import DEFAULT_INDEX_PATH, StyleEmbedder  # noqa: E402

API = "https://datasets-server.huggingface.co"
MIN_WORDS, MAX_CHARS = 50, 2000

RAID_GENERATORS = [
    "chatgpt", "gpt4", "gpt3", "llama-chat", "mistral-chat", "cohere-chat", "mpt-chat",
]


def _get(url: str) -> dict:
    with urllib.request.urlopen(url, timeout=60) as response:
        return json.load(response)


def fetch_rows(dataset: str, config: str, split: str, offset: int, length: int = 100) -> list[dict]:
    url = (
        f"{API}/rows?dataset={urllib.parse.quote(dataset)}"
        f"&config={config}&split={split}&offset={offset}&length={length}"
    )
    return [r["row"] for r in _get(url)["rows"]]


def fetch_filtered(dataset: str, config: str, split: str, where: str, offset: int, length: int = 100) -> list[dict]:
    url = (
        f"{API}/filter?dataset={urllib.parse.quote(dataset)}"
        f"&config={config}&split={split}&where={urllib.parse.quote(where)}"
        f"&offset={offset}&length={length}"
    )
    return [r["row"] for r in _get(url)["rows"]]


def usable(text: str) -> str | None:
    text = normalize_text(text or "")
    if word_count(text) < MIN_WORDS:
        return None
    return text[:MAX_CHARS]


def collect() -> tuple[list[str], list[int], list[str]]:
    texts: list[str] = []
    labels: list[int] = []
    generators: list[str] = []
    seen: set[str] = set()

    def add(text: str | None, label: int, generator: str) -> None:
        if text is None or text[:200] in seen:
            return
        seen.add(text[:200])
        texts.append(text)
        labels.append(label)
        generators.append(generator)

    # --- AI side: RAID generators (attack-free rows) ---
    for generator in RAID_GENERATORS:
        count = 0
        for offset in (0, 100, 200):
            where = f"\"model\"='{generator}' AND \"attack\"='none'"
            try:
                rows = fetch_filtered("liamdugan/raid", "raid", "train", where, offset)
            except Exception as exc:  # noqa: BLE001
                print(f"  ! RAID {generator} offset {offset}: {exc}")
                continue
            for row in rows:
                if count >= 120:
                    break
                text = usable(row.get("generation"))
                if text:
                    add(text, 1, generator)
                    count += 1
        print(f"RAID {generator}: {count}")

    # --- AI side: HC3 ChatGPT answers ---
    count = 0
    for offset in (3000, 3100, 3200, 3300):
        for row in fetch_rows("Hello-SimpleAI/HC3", "all", "train", offset):
            for answer in row.get("chatgpt_answers") or []:
                if count >= 200:
                    break
                text = usable(answer)
                if text:
                    add(text, 1, "chatgpt")
                    count += 1
    print(f"HC3 chatgpt: {count}")

    # --- Human side: RAID human references (spread across domains) ---
    count = 0
    for offset in (0, 100, 200, 300, 400):
        try:
            rows = fetch_filtered(
                "liamdugan/raid", "raid", "train", "\"model\"='human'", offset
            )
        except Exception as exc:  # noqa: BLE001
            print(f"  ! RAID human offset {offset}: {exc}")
            continue
        for row in rows:
            if count >= 400:
                break
            text = usable(row.get("generation"))
            if text:
                add(text, 0, "human")
                count += 1
    print(f"RAID human: {count}")

    # --- Human side: HC3 human answers ---
    count = 0
    for offset in (3000, 3100, 3200, 3300):
        for row in fetch_rows("Hello-SimpleAI/HC3", "all", "train", offset):
            for answer in row.get("human_answers") or []:
                if count >= 200:
                    break
                text = usable(answer)
                if text:
                    add(text, 0, "human")
                    count += 1
    print(f"HC3 human: {count}")

    # --- Human side: register diversity ---
    count = 0
    for offset in (0, 100):
        for row in fetch_rows("stanfordnlp/imdb", "plain_text", "train", offset):
            if count >= 150:
                break
            text = usable(row.get("text"))
            if text:
                add(text, 0, "human")
                count += 1
    print(f"IMDB human: {count}")

    count = 0
    for offset in (0, 100):
        for row in fetch_rows("abisee/cnn_dailymail", "3.0.0", "train", offset):
            if count >= 150:
                break
            text = usable(row.get("article"))
            if text:
                add(text, 0, "human")
                count += 1
    print(f"CNN/DailyMail human: {count}")

    count = 0
    for offset in (0, 200):
        for row in fetch_rows("rajpurkar/squad", "plain_text", "train", offset):
            if count >= 120:
                break
            text = usable(row.get("context"))
            if text:
                add(text, 0, "human")
                count += 1
    print(f"SQuAD contexts human: {count}")

    return texts, labels, generators


def main() -> None:
    texts, labels, generators = collect()
    n_human = labels.count(0)
    n_ai = labels.count(1)
    print(f"\nTotal: {len(texts)} ({n_human} human / {n_ai} AI)")

    embedder = StyleEmbedder()
    print("Embedding…")
    embeddings = embedder.embed(texts, batch_size=32)

    DEFAULT_INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        DEFAULT_INDEX_PATH,
        embeddings=embeddings.astype(np.float16),
        labels=np.array(labels, dtype=np.int8),
        generators=np.array(generators),
    )
    print(f"Wrote {DEFAULT_INDEX_PATH} ({DEFAULT_INDEX_PATH.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
