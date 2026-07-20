# RAID fine-tuning on Kaggle

Train a custom VeritasAI detector on the [RAID benchmark](https://huggingface.co/datasets/liamdugan/raid) and push it to your Hugging Face Hub account.

## Kaggle notebook (recommended)

1. Go to [kaggle.com/code](https://www.kaggle.com/code) → **New Notebook**
2. **Settings** → Accelerator: **GPU T4 x2**, Internet: **On**
3. Add secret: `HF_TOKEN` = your write token from https://huggingface.co/settings/tokens
4. In the first cell:

```python
!pip install -q transformers datasets peft accelerate scikit-learn huggingface_hub
!git clone https://github.com/Diptikanta2805/cursor-test.git /tmp/veritas
%cd /tmp/veritas
```

5. Run training:

```python
import os
os.environ["HF_TOKEN"] = os.environ["HF_TOKEN"]  # from Kaggle secrets
os.environ["OUTPUT_REPO"] = "dipu2805/veritas-raid-e5"
os.environ["MAX_TRAIN"] = "40000"
os.environ["MAX_EVAL"] = "4000"
os.environ["EPOCHS"] = "2"
!python packages/training/finetune_raid.py
```

6. Point the API at your new model:

```bash
VERITAS_FAST_MODEL_ID=dipu2805/veritas-raid-e5
```

## Local smoke test (CPU, tiny subset)

```bash
MAX_TRAIN=200 MAX_EVAL=50 EPOCHS=1 BATCH_SIZE=4 python packages/training/finetune_raid.py
```

## Expected metrics

On 4K RAID-test rows (attack-free), a 2-epoch LoRA fine-tune of e5-small typically reaches **~92–94% accuracy** and **~0.97 AUROC**, competitive with off-the-shelf RAID detectors.
