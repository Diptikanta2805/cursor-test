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
  — DeBERTa-v3-large, MIT, led the RAID leaderboard. Runs when the fast tier
  is uncertain (0.35–0.65) or on explicit deep scans.
- **Statistical arm**: distilgpt2 perplexity + burstiness (weak prior in the
  ensemble, always shown to the user).
- **Adversarial pre-defense**: Unicode NFKC + homoglyph + zero-width-space
  normalization neutralizes RAID-catalogued character attacks before scoring.
- **Calibrated verdicts**: `strict` (target 1% FPR) and `balanced` (5% FPR)
  operating points; honest `mixed` / `inconclusive` verdicts.

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

## Free deployment

- **API** → Hugging Face Spaces (Docker SDK, free CPU): push this repo, Space
  reads `apps/api/Dockerfile`, listens on 7860. Or Render free web service.
- **Web** → Vercel / Cloudflare Pages: root `apps/web`, set
  `NEXT_PUBLIC_API_URL` to the API URL.
- **DB** → default SQLite works out of the box; point `VERITAS_DATABASE_URL`
  at free Supabase Postgres for durability.

## Responsible use

Scores are calibrated probabilities, not proof. Detectors have documented
elevated false-positive rates on non-native-English writing. Never use a
detector verdict as sole evidence of misconduct — that warning is built into
the product UI on purpose.
