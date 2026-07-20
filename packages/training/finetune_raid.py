# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "torch",
#   "transformers>=4.48",
#   "datasets",
#   "accelerate",
#   "peft",
#   "scikit-learn",
#   "huggingface_hub",
# ]
# ///
"""Fine-tune an e5-small RAID detector on Kaggle (or any GPU).

Trains a binary classifier on liamdugan/raid (attack-free rows, balanced
human vs AI), evaluates on a held-out slice of raid_test, and pushes the
best checkpoint to the Hugging Face Hub.

Kaggle usage:
  1. New notebook → Settings → GPU T4 x2, Internet ON
  2. Paste this file or upload as script
  3. Set env: HF_TOKEN, OUTPUT_REPO (default dipu2805/veritas-raid-e5)

Local smoke test (CPU, tiny subset):
  MAX_TRAIN=500 MAX_EVAL=100 python packages/training/finetune_raid.py
"""

from __future__ import annotations

import os
import random
from dataclasses import dataclass

import numpy as np
import torch
from datasets import load_dataset
from peft import LoraConfig, get_peft_model
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    Trainer,
    TrainingArguments,
)

BASE_MODEL = os.environ.get("BASE_MODEL", "intfloat/e5-small-v2")
OUTPUT_REPO = os.environ.get("OUTPUT_REPO", "dipu2805/veritas-raid-e5")
MAX_TRAIN = int(os.environ.get("MAX_TRAIN", "40000"))
MAX_EVAL = int(os.environ.get("MAX_EVAL", "4000"))
EPOCHS = float(os.environ.get("EPOCHS", "2"))
BATCH_SIZE = int(os.environ.get("BATCH_SIZE", "16"))
LR = float(os.environ.get("LR", "3e-5"))
SEED = 42

RAID_GENERATORS = [
    "chatgpt", "gpt4", "gpt3", "llama-chat", "mistral-chat", "cohere-chat", "mpt-chat",
]


@dataclass
class Row:
    text: str
    label: int


def _usable(text: str, min_words: int = 50) -> bool:
    return len((text or "").split()) >= min_words


def build_rows(split: str, max_rows: int, seed: int) -> list[Row]:
    ds = load_dataset("liamdugan/raid", "raid" if split == "train" else "raid_test", split=split)
    rows: list[Row] = []
    rng = random.Random(seed)
    for record in ds:
        model = record["model"]
        if record.get("attack", "none") != "none":
            continue
        text = record.get("generation") or ""
        if not _usable(text):
            continue
        if model == "human":
            label = 0
        elif model in RAID_GENERATORS:
            label = 1
        else:
            continue
        rows.append(Row(text=text[:4000], label=label))
    rng.shuffle(rows)
    return rows[:max_rows]


def main() -> None:
    random.seed(SEED)
    np.random.seed(SEED)
    torch.manual_seed(SEED)

    train_rows = build_rows("train", MAX_TRAIN, SEED)
    eval_rows = build_rows("test", MAX_EVAL, SEED + 1)
    print(f"Train: {len(train_rows)} ({sum(r.label for r in train_rows)} AI)")
    print(f"Eval:  {len(eval_rows)} ({sum(r.label for r in eval_rows)} AI)")

    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(
        BASE_MODEL, num_labels=2, id2label={0: "human", 1: "ai"}, label2id={"human": 0, "ai": 1}
    )
    lora = LoraConfig(
        r=16,
        lora_alpha=32,
        target_modules=["query", "value"],
        lora_dropout=0.05,
        bias="none",
        task_type="SEQ_CLS",
    )
    model = get_peft_model(model, lora)
    model.print_trainable_parameters()

    def tokenize(batch):
        texts = ["query: " + t for t in batch["text"]]
        return tokenizer(texts, truncation=True, max_length=512, padding="max_length")

    from datasets import Dataset

    train_ds = Dataset.from_dict(
        {"text": [r.text for r in train_rows], "label": [r.label for r in train_rows]}
    ).map(tokenize, batched=True)
    eval_ds = Dataset.from_dict(
        {"text": [r.text for r in eval_rows], "label": [r.label for r in eval_rows]}
    ).map(tokenize, batched=True)

    def compute_metrics(pred):
        labels = pred.label_ids
        probs = torch.softmax(torch.tensor(pred.predictions), dim=-1)[:, 1].numpy()
        preds = (probs >= 0.5).astype(int)
        return {
            "accuracy": accuracy_score(labels, preds),
            "f1": f1_score(labels, preds),
            "auroc": roc_auc_score(labels, probs),
        }

    args = TrainingArguments(
        output_dir="./raid-checkpoints",
        num_train_epochs=EPOCHS,
        per_device_train_batch_size=BATCH_SIZE,
        per_device_eval_batch_size=BATCH_SIZE,
        learning_rate=LR,
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="auroc",
        logging_steps=50,
        report_to="none",
        fp16=torch.cuda.is_available(),
    )

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=train_ds,
        eval_dataset=eval_ds,
        compute_metrics=compute_metrics,
    )
    trainer.train()
    metrics = trainer.evaluate()
    print("Eval metrics:", metrics)

    merged = model.merge_and_unload()
    merged.save_pretrained("./raid-model-out")
    tokenizer.save_pretrained("./raid-model-out")

    token = os.environ.get("HF_TOKEN")
    if token:
        merged.push_to_hub(OUTPUT_REPO, token=token)
        tokenizer.push_to_hub(OUTPUT_REPO, token=token)
        print(f"Pushed to https://huggingface.co/{OUTPUT_REPO}")
    else:
        print("Set HF_TOKEN to push to the Hub.")


if __name__ == "__main__":
    main()
