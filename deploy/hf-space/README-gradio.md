---
title: VeritasAI API
emoji: 🔍
colorFrom: blue
colorTo: indigo
sdk: gradio
sdk_version: 5.50.0
app_file: app.py
python_version: "3.12"
pinned: false
license: mit
short_description: Open AI-text detection API (RAID-trained ensemble)
startup_duration_timeout: 30m
---

# VeritasAI API

Production FastAPI service for AI-generated text detection (free cpu-basic tier).

- Ensemble: RAID fine-tuned classifiers + style retrieval + Binoculars + RAIDAR (deep scan)
- Endpoints: `/v1/scan`, `/v1/scan/file`, `/v1/health`, OpenAPI at `/docs`
- Set secrets: `VERITAS_ADMIN_TOKEN` for API-key minting

```bash
curl -X POST https://dipu2805-veritas-ai-api.hf.space/v1/scan \
  -H "Content-Type: application/json" \
  -d '{"text": "...50+ words...", "mode": "deep"}'
```
