# VeritasAI — Build Plan for a GPTZero-Class AI Text Detector (100% Free Stack)

A detailed, end-to-end engineering plan for a production-ready web app that detects AI-generated text — targeting **higher accuracy** (measured on the public RAID benchmark) and **lower latency/cost** than GPTZero, using only free and open-source resources.

---

## 1. Goal and Success Criteria

Build a web app with feature parity with GPTZero (paste/upload text → AI-probability verdict, sentence-level highlighting, API, dashboard) that is:

| Criterion | Target | How it's measured |
|---|---|---|
| Accuracy | ≥ 90% detection accuracy at 5% false-positive rate (FPR) on the RAID benchmark test set | Official [RAID leaderboard](https://raid-bench.xyz) submission via the `raid-bench` pip package |
| Robustness | Degrade gracefully under RAID's 11 adversarial attacks (paraphrase, homoglyphs, misspellings, etc.) | RAID adversarial splits |
| Low FPR on human text | Explicit calibrated threshold; report TPR@FPR=1% and 5%, never a single "99% accuracy" number | Held-out human corpora incl. non-native-English writing |
| Latency | < 1.5 s p95 for a 500-word document on free CPU hosting | Load test with `locust`/`k6` |
| Cost | $0 infrastructure | Free tiers only (see §8) |

Context for the accuracy bar: on RAID, GPTZero and ZeroGPT are mid-pack; the strongest published open detectors reach ~93–94% accuracy at 5% FPR, while zero-shot Binoculars is the strongest at very low FPR. Beating GPTZero on a public, third-party benchmark is realistic; the plan below is built around that exact evaluation.

---

## 2. What GPTZero Does (Feature Parity Checklist)

- [ ] Paste text or upload files (PDF, DOCX, TXT) for scanning
- [ ] Document-level verdict: human / AI / mixed, with confidence
- [ ] Sentence-level highlighting of likely-AI sentences
- [ ] "Burstiness"/"perplexity"-style explanatory signals shown to the user
- [ ] Batch scanning of multiple documents
- [ ] REST API with API keys and rate limits
- [ ] User accounts, scan history dashboard
- [ ] Shareable scan reports
- [ ] Chrome-extension-friendly API surface (stretch goal)

Where we go beyond GPTZero:

- **Transparent scoring**: show the ensemble's component scores (classifier probability, Binoculars score, perplexity curve) instead of a black-box number.
- **Calibrated thresholds per domain** (essay, news, code comments, creative writing) with explicit FPR settings the user can pick ("strict" = 1% FPR, "balanced" = 5% FPR).
- **Open evaluation**: publish our RAID leaderboard entry and eval harness in the repo.

---

## 3. Detection Science: The Core of the Accuracy Advantage

Use an **ensemble of two complementary families**, which is what the research literature shows wins on robustness:

### 3.1 Supervised fine-tuned classifier (primary signal)

Fine-tuned transformer encoders dominate the RAID leaderboard. Free, openly licensed starting points:

| Model | Base | Params | License | Why it matters |
|---|---|---|---|---|
| ⭐ [desklib/ai-text-detector-v1.01](https://hf.co/desklib/ai-text-detector-v1.01) | DeBERTa-v3-large | 0.4B | MIT | Led the RAID leaderboard at submission; trained on RAID; robust to adversarial attacks |
| [MayZhou/e5-small-lora-ai-generated-detector](https://hf.co/MayZhou/e5-small-lora-ai-generated-detector) | e5-small | 33M | MIT | ~93.9% RAID-test accuracy at a fraction of the size — the efficiency play; runs fast on free CPUs |
| [Oxidane/tmr-ai-text-detector](https://hf.co/Oxidane/tmr-ai-text-detector) | RoBERTa-base | 125M | MIT | Recent (2026), focal-loss trained on RAID; good mid-size candidate |
| [Shushant/adal_v5_raid](https://hf.co/Shushant/adal_v5_raid) | RoBERTa-large (RADAR-style adversarial training) | 0.4B | — | Adversarially trained against 11 evasion attacks; macro AUROC 0.978 |

Plan: benchmark all four on our eval harness (§6), then **fine-tune our own detector** starting from `microsoft/deberta-v3-large` (primary) and `intfloat/e5-small` (efficiency tier) on the training mix in §5. Two deployment tiers:

- **Fast tier (default)**: e5-small-class model, ONNX int8 — ~33M params, CPU-friendly, sub-100ms inference.
- **Accurate tier**: DeBERTa-v3-large detector, ONNX int8 — used for "deep scan" and when fast-tier confidence is in the uncertain band (0.35–0.65). This cascade keeps p95 latency low while preserving top-line accuracy.

### 3.2 Zero-shot statistical detector (secondary signal, generalization insurance)

Fine-tuned classifiers overfit to generators seen in training; zero-shot methods generalize to unseen LLMs. Add:

- **[Binoculars](https://github.com/ahans30/Binoculars)** (ICML 2024): contrasts perplexity vs. cross-perplexity between an "observer" and "performer" LLM pair. State-of-the-art zero-shot; notably the strongest detector at very low FPR on RAID. Default pair is Falcon-7B/Falcon-7B-Instruct; we will validate smaller free pairs (e.g. Qwen2.5-0.5B/-0.5B-Instruct, SmolLM2-1.7B pair) to fit free hardware, keeping the 7B pair for offline/batch scoring.
- **[Fast-DetectGPT](https://github.com/baoguangsheng/fast-detect-gpt)** (ICLR 2024): conditional probability curvature in a single forward pass with a small scoring model (GPT-Neo-2.7B or smaller). ~340× faster than DetectGPT.

### 3.3 Ensemble + sentence-level scoring

- **Document score** = logistic-regression stacker over [classifier prob, Binoculars score, Fast-DetectGPT score, doc length, domain tag], trained on a held-out calibration split. Calibrate with isotonic regression so the displayed percentage is a true probability.
- **Sentence-level highlighting**: run the fast classifier on a sliding window (3-sentence context, 1-sentence stride); smooth scores with a 3-tap filter; highlight sentences above the calibrated threshold. This yields GPTZero-style mixed-text detection.
- **Uncertainty band**: scores in the middle band get the "accurate tier" re-scan; if still uncertain, report "inconclusive" honestly rather than guessing — a key trust differentiator and FPR protection.

### 3.4 Known failure modes and mitigations

| Risk | Mitigation |
|---|---|
| False positives on non-native English writers (documented problem for all detectors) | Include ESL corpora (e.g. TOEFL-style essays, Lang-8) as human class in training; report per-cohort FPR; "inconclusive" band |
| Paraphrase attacks (DIPPER, Quillbot-style) | Train on RAID's paraphrase attack split + generate our own paraphrased positives with open models (Qwen, Llama) |
| Homoglyph/zero-width-space attacks | Unicode normalization + confusables mapping in preprocessing (defeats the attack before the model sees it) |
| Unseen future generators | Zero-shot ensemble arm + periodic retraining pipeline (§5.4) |
| Short texts | Enforce 50-word minimum like GPTZero; below that, refuse with an explanation |

---

## 4. Data (All Free)

| Dataset | Size | Role |
|---|---|---|
| [liamdugan/raid](https://hf.co/datasets/liamdugan/raid) | 10M+ docs, 11 LLMs, 11 genres, 11 attacks, 4 decoding strategies | Primary train/eval; the field's standard benchmark |
| [Hello-SimpleAI/HC3](https://hf.co/datasets/Hello-SimpleAI/HC3) | ~85K QA pairs | ChatGPT-vs-human contrast pairs |
| [yaful/MAGE](https://hf.co/datasets/yaful/MAGE) | 447K, 27 LLMs, 10 domains | Cross-domain generalization |
| M4GT / SemEval-2024 Task 8 | ~65K multilingual | Multilingual stretch goal |
| Self-generated hard negatives | — | Use free open models (Qwen2.5, Llama-3.x, Gemma-3 via Colab/Kaggle or HF free inference credits) to generate 2024–2026-era text RAID lacks: GPT-4o/Claude/Gemini-style RLHF'd prose, "humanized" paraphrases, AI-edited human text |

Data hygiene: dedupe with MinHash, stratify train/val/test by generator+domain+attack, keep RAID's official test split untouched for leaderboard submission.

---

## 5. Training Pipeline (Free GPUs)

### 5.1 Free compute options

- **Google Colab (free)**: T4 16GB — fine for e5-small, RoBERTa-base, LoRA on DeBERTa-large.
- **Kaggle Notebooks**: 2× T4 or P100, 30 GPU-hrs/week — primary training venue; supports background execution up to 12h.
- **HF Spaces ZeroGPU** (free quota): H200-slice bursts for inference experiments.
- Checkpoints and datasets stored free on the Hugging Face Hub (public repos, unlimited).

### 5.2 Training recipe

1. Tokenize to 512 tokens; chunk long docs with overlap, aggregate by max-pooling chunk scores.
2. e5-small: full fine-tune, 3 epochs, lr 5e-5, focal loss (class imbalance + hard-example focus).
3. DeBERTa-v3-large: LoRA (r=16) fine-tune to fit T4 memory, then merge; label smoothing 0.1; adversarial data augmentation (all 11 RAID attack types applied on-the-fly to 30% of batches).
4. Track experiments free with **Trackio** (HF's free experiment tracker) or W&B free tier.
5. Distillation pass: distill the DeBERTa teacher into the e5-small student on soft labels to close the tier gap.

### 5.3 Calibration & stacker

Fit isotonic regression + the logistic stacker on a held-out calibration split, per domain. Store calibration curves as JSON artifacts versioned with the model.

### 5.4 Continuous retraining

Monthly GitHub Actions workflow (free for public repos) that: pulls new generations produced with current open models on Kaggle, retrains the fast tier, runs the eval harness, and opens a PR with the metrics diff. Humans merge only if RAID-dev metrics improve.

---

## 6. Evaluation Harness (Built First, Before the App)

- `evals/` package wrapping `raid-bench` + our own splits.
- Metrics: **TPR@FPR=1% and 5%** (headline), AUROC, F1, ECE (calibration), per-generator/per-domain/per-attack breakdown, per-cohort FPR (incl. ESL human texts).
- CI job runs the harness on a 10K-doc fixed subsample every model PR; full RAID run before each release.
- Publish results to the official RAID leaderboard (public, third-party — this is the "more accurate than GPTZero" proof, since GPTZero's RAID numbers are public).

---

## 7. System Architecture

```
┌────────────┐   ┌─────────────────────┐   ┌──────────────────────────────┐
│  Next.js   │──▶│  FastAPI gateway     │──▶│  Inference service (ONNX RT) │
│  frontend  │   │  auth, rate limits,  │   │  fast tier: e5-small int8    │
│ (Vercel/CF │   │  queue, history      │   │  accurate tier: DeBERTa int8 │
│  Pages)    │   │                      │   │  zero-shot: Binoculars-small │
└────────────┘   └─────────┬───────────┘   └──────────────────────────────┘
                           │
              ┌────────────┴───────────┐
              │ Supabase (Postgres +   │
              │ Auth + storage) — free │
              └────────────────────────┘
```

### 7.1 Backend (Python)

- **FastAPI** + `uvicorn`; async endpoints; `onnxruntime` CPU with int8-quantized models (Optimum export). Quantization gives ~3–4× CPU speedup at <0.5% accuracy loss.
- Pipeline per request: Unicode normalization → language check (fasttext lid) → sentence split (`pysbd`) → sliding-window fast-tier scoring → ensemble/stacker → optional accurate-tier cascade → response.
- File parsing: `pypdf`, `python-docx`; OCR out of scope v1.
- Rate limiting: `slowapi` + Upstash Redis free tier.
- Job queue for batch scans: `arq` on the same Redis.

### 7.2 Frontend

- **Next.js (App Router) + Tailwind + shadcn/ui**, deployed free on Vercel or Cloudflare Pages.
- Views: scanner (paste/upload, live sentence heat-map, component-score breakdown panel), history dashboard, shareable report page (`/r/{id}`), API-keys page, docs.
- Heat-map UX: per-sentence background opacity ∝ AI probability; hover tooltip shows sentence score + which signal drove it.

### 7.3 API design

```
POST /v1/scan            { text | file, mode: fast|deep, fpr: 0.01|0.05 }
  → { verdict: human|ai|mixed|inconclusive, ai_probability, calibrated_at_fpr,
      sentences: [{text, score}], signals: {classifier, binoculars, fastdetect},
      model_version, scan_id }
POST /v1/scan/batch
GET  /v1/scan/{id}
GET  /v1/usage
```

Versioned, documented with the auto-generated OpenAPI page. API keys hashed in Postgres; per-key daily quotas.

### 7.4 Auth, storage, persistence

- **Supabase free tier**: Postgres (scans, users, api_keys, usage), email/OAuth auth, row-level security.
- Model artifacts on the HF Hub (free); pulled at container start, cached on disk.

---

## 8. Free Deployment Topology

| Component | Free host | Notes |
|---|---|---|
| Frontend | Cloudflare Pages or Vercel (free) | Static + edge SSR |
| API gateway + fast-tier inference | **HF Spaces (Docker, free CPU basic: 2 vCPU/16GB)** — primary; Render free web service as fallback | e5-small int8 needs <300MB RAM |
| Accurate tier + Binoculars | Separate HF Space with ZeroGPU free quota; falls back to CPU (slower "deep scan" is acceptable UX) | |
| DB/Auth | Supabase free | 500MB Postgres |
| Redis (rate limit/queue) | Upstash free | 10K cmd/day |
| Object storage (uploads) | Supabase storage / Cloudflare R2 free 10GB | |
| CI/CD | GitHub Actions (free, public repo) | lint, tests, eval subsample, ONNX export, deploy |
| Monitoring | HF Spaces logs + Grafana Cloud free tier + UptimeRobot free | |

Free-tier caveats handled in design: HF Spaces sleep after inactivity (mitigate with UptimeRobot ping within ToS, plus a "warming up" UI state); Supabase free pauses after a week idle (weekly keepalive query in CI); all limits documented in `docs/ops.md` with the paid-upgrade path if traffic outgrows free tiers.

---

## 9. Efficiency Plan (the "faster than GPTZero" half)

1. **Cascade**: ~80% of requests resolved by the 33M-param fast tier (<100ms CPU).
2. **ONNX Runtime int8** everywhere; tokenizer in Rust (`tokenizers`).
3. **Sliding-window batching**: all sentence windows of a doc scored in one padded batch.
4. **Caching**: SHA-256 of normalized text → cached result (Redis), dedupes repeated scans.
5. **Streaming UX**: sentence scores streamed via SSE so the heat-map paints progressively.
6. Zero-shot arm only runs in deep mode or on uncertain docs — keeping the expensive LLM forward passes off the hot path.

---

## 10. Milestones

**M0 — Repo & eval harness.** Monorepo scaffold (`apps/web`, `apps/api`, `packages/evals`, `packages/training`), CI, `raid-bench` harness running against the four candidate off-the-shelf models; pick baseline. *Exit: metrics table in repo.*

**M1 — Detection core.** Fine-tune fast + accurate tiers on Kaggle, build ensemble + calibration, sentence-level scoring. *Exit: ≥90% acc @ 5% FPR on RAID-dev; RAID leaderboard submission.*

**M2 — API service.** FastAPI + ONNX inference, scan/batch endpoints, rate limits, file parsing, tests (pytest + schemathesis). *Exit: p95 < 1.5s on 500-word docs on HF Space CPU.*

**M3 — Web app.** Next.js scanner with heat-map, auth, history, shareable reports, API-key management. *Exit: full user flow deployed on free tiers.*

**M4 — Hardening & launch.** Adversarial red-teaming (paraphrase/humanizer tools), per-cohort FPR audit, docs, monitoring, retraining automation. *Exit: public launch + published eval report.*

---

## 11. Repository Layout

```
veritas-ai/
├── apps/
│   ├── api/            # FastAPI service + Dockerfile (HF Space)
│   └── web/            # Next.js frontend
├── packages/
│   ├── detection/      # ensemble, calibration, windowing (pip package)
│   ├── evals/          # raid-bench harness, metrics, leaderboard submit
│   └── training/       # Kaggle/Colab-ready training scripts (PEP 723 uv scripts)
├── models/             # pointers to HF Hub artifacts + calibration JSONs
├── .github/workflows/  # ci.yml, eval.yml, retrain.yml, deploy.yml
└── docs/               # architecture, ops runbook, eval reports
```

---

## 12. Honest Positioning (Important for a Detector Product)

No detector is infallible; RAID's own findings show every commercial tool (GPTZero included) degrades under attacks and unseen generators. The product must state calibrated FPR, show component signals, expose an "inconclusive" verdict, and warn against using scores as sole evidence for academic-misconduct decisions. This transparency is both an ethical requirement and the clearest product differentiation from GPTZero.

---

## Key References

- RAID benchmark: Dugan et al., ACL 2024 — [arxiv.org/abs/2405.07940](https://arxiv.org/abs/2405.07940), leaderboard at [raid-bench.xyz](https://raid-bench.xyz)
- Binoculars: Hans et al., ICML 2024 — [arxiv.org/abs/2401.12070](https://arxiv.org/abs/2401.12070)
- Fast-DetectGPT: Bao et al., ICLR 2024 — [arxiv.org/abs/2310.05130](https://arxiv.org/abs/2310.05130)
- RADAR (adversarial training): Hu et al., NeurIPS 2023 — [arxiv.org/abs/2307.03838](https://arxiv.org/abs/2307.03838)
