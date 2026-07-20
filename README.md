# VeritasAI — Open, Calibrated AI-Text Detection

A production-ready, GPTZero-class AI-generated-text detector built entirely on
free and open resources. Ensemble of RAID-benchmark-leading open models with
transparent, GPTZero-style perplexity/burstiness signals, sentence-level
heat-maps, calibrated operating points, a REST API, and a modern web UI.

See `PLAN.md` for the full architecture and research grounding.

## What's inside

```
apps/api          FastAPI service (scan, batch, file upload, API keys, quotas)
apps/web          Next.js 16 frontend (scanner, heat-map, history, docs)
packages/detection  Detection engine (normalization, ensemble, calibration)
```

## Detection approach

- **Fast tier (default)**: [MayZhou/e5-small-lora-ai-generated-detector](https://huggingface.co/MayZhou/e5-small-lora-ai-generated-detector)
  — 33M params, MIT, ~93.9% accuracy on RAID-test; scores the document plus a
  3-sentence sliding window for the heat-map in a single batched pass.
- **Deep tier (cascade)**: [desklib/ai-text-detector-v1.01](https://huggingface.co/desklib/ai-text-detector-v1.01)
  — DeBERTa-v3-large, MIT, led the RAID leaderboard. Runs when the cheap arms
  disagree or sit near the decision boundary, or on explicit deep scans.
- **Style-retrieval arm (DeTeCtive-style)**: kNN vote over an e5-small-v2
  embedding index of 1.5K human/LLM reference texts (RAID 7 generator
  families + HC3 + news/reviews/wiki). Also yields *generator attribution*
  ("nearest style: ChatGPT-class") and supports training-free adaptation to
  new LLMs — append embeddings, no retraining
  (`packages/training/build_style_index.py`).
- **Statistical arm**: distilgpt2 perplexity + burstiness (weak prior),
  plus GTCL-inspired semantic-trajectory uniformity (informational signal).
- **Boundary detection**: change-point segmentation over sentence scores
  finds the exact human→AI switch points; drives the `mixed` verdict and
  heat-map markers.
- **Conformal calibration**: AI-verdict thresholds are (1 − α) quantiles of
  ensemble scores on a human-only calibration set, stratified by length —
  a distribution-free FPR bound (α = 1% `strict`, 5% `balanced`), not a
  hand-tuned threshold (`packages/training/calibrate.py`).
- **Adversarial pre-defense**: Unicode NFKC + homoglyph + zero-width-space
  normalization neutralizes RAID-catalogued character attacks before scoring.

See `docs/ADVANCED_ROADMAP.md` for the research grounding and the remaining
training-required roadmap (contrastive style encoder, token-level boundary
model, group-DRO fairness training, watermark arm).

## Quickstart (local)

```bash
# API (Python 3.11+)
python3 -m venv .venv && source .venv/bin/activate
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install -r apps/api/requirements.txt
pip install -e packages/detection
cd apps/api && uvicorn app.main:app --port 8000
# First start downloads ~1.8GB of models; set VERITAS_ENABLE_DEEP_TIER=false to skip the big one.

# Web
cd apps/web && npm install
NEXT_PUBLIC_API_URL=http://localhost:8000 npm run dev
```

Or with Docker: `docker compose up --build` (API on :8000, web on :3000).

## Configuration (env vars, prefix `VERITAS_`)

| Variable | Default | Purpose |
|---|---|---|
| `FAST_MODEL_ID` | `MayZhou/e5-small-lora-ai-generated-detector` | Fast-tier classifier |
| `DEEP_MODEL_ID` | `desklib/ai-text-detector-v1.01` | Deep-tier classifier |
| `ENABLE_DEEP_TIER` | `true` | Disable to run light (CPU-poor hosts) |
| `ENABLE_PERPLEXITY` | `true` | Perplexity/burstiness signals |
| `ENABLE_RETRIEVAL` | `true` | Style-retrieval arm + attribution |
| `EMBEDDER_MODEL_ID` | `intfloat/e5-small-v2` | Embedder for retrieval/trajectory |
| `STYLE_INDEX_PATH` | *(packaged)* | Custom style index (.npz) |
| `DATABASE_URL` | `sqlite:///./veritas.db` | Any SQLAlchemy URL (Postgres/Supabase) |
| `ADMIN_TOKEN` | *(empty = disabled)* | Enables `POST /v1/keys` key minting |
| `ANONYMOUS_DAILY_LIMIT` | `50` | Scans/day per anonymous IP |
| `API_KEY_DAILY_LIMIT` | `2000` | Scans/day per API key |
| `CORS_ORIGINS` | `*` | Comma-separated origins |

## API

Interactive OpenAPI docs at `/docs`. Core endpoint:

```bash
curl -X POST http://localhost:8000/v1/scan \
  -H "Content-Type: application/json" \
  -d '{"text": "…at least 50 words…", "mode": "deep", "operating_point": "strict"}'
```

## Tests

```bash
pytest packages/detection/tests          # unit tests (fast, no downloads)
cd apps/api && pytest tests              # API tests (stubbed pipeline)
VERITAS_RUN_MODEL_TESTS=1 pytest packages/detection/tests/test_pipeline_integration.py  # real models
```

## Deploy to Hugging Face Space (permanent free URL)

```bash
export HF_TOKEN=hf_...   # write token from huggingface.co/settings/tokens
pip install huggingface_hub
python deploy/push_space.py
```

This creates **`dipu2805/veritas-ai-api`** as a public Docker Space on free `cpu-basic` hardware. After the build (~10–15 min for model downloads), your API is at:

`https://dipu2805-veritas-ai-api.hf.space`

Point the web app at it: `NEXT_PUBLIC_API_URL=https://dipu2805-veritas-ai-api.hf.space`

## RAID fine-tuning

See [`packages/training/README.md`](packages/training/README.md) for the Kaggle GPU notebook recipe.

## Responsible use

Scores are calibrated probabilities, not proof. Detectors have documented
elevated false-positive rates on non-native-English writing. Never use a
detector verdict as sole evidence of misconduct — that warning is built into
the product UI on purpose.
