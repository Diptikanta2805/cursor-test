# Beyond GPTZero: Novel-Methods Roadmap for VeritasAI

GPTZero's published approach is: supervised binary classifiers trained on a
large human/multi-LLM corpus, a sentence-level classifier, a mixed-content
module, a "paraphraser shield", adversarial retraining loops, ESL debiasing,
and blind-set generalization testing. Every one of those is a 2023-era
supervised-classification idea. This document maps each GPTZero component to
a strictly more novel replacement, all implementable with free resources, and
grounded in 2024–2026 peer-reviewed research.

**Implementation status:** the training-free tier of this roadmap is now
implemented in the app — style-retrieval arm with generator attribution and
TFIA (`retrieval.py` + `build_style_index.py`), conformal FPR calibration
(`conformal.py` + `calibrate.py`), change-point boundary detection
(`boundary.py`), and trajectory statistics (`trajectory.py`, informational).
Items still requiring GPU training: the contrastive style encoder (§1 full
version), the GTCL projection head (§2 full version), the token-level
boundary model (§4), paraphrase-consistency training (§5.1), group-DRO
fairness training (§6), and the self-play red team (§7).

Summary of the upgrade map:

| GPTZero component | VeritasAI upgrade | Core idea | Reference |
|---|---|---|---|
| Binary supervised classifier | Style-space contrastive encoder + kNN retrieval | Detection as authorship verification, not classification | DeTeCtive (NeurIPS 2024), FAID (EACL 2026) |
| Static document features | Latent trajectory discrimination | Classify the *geometry of semantic transitions*, not static embeddings | GTCL (arXiv 2607.14967) |
| "Calibration" (threshold tuning) | Multiscaled conformal prediction | Distribution-free, provable FPR upper bound | MCP (ACL 2025) |
| Sentence-level classifier | Token-level boundary detection (sequence labeling + change-point) | Find the exact human→AI switch point | SemEval-2024 Task 8C |
| Paraphraser shield | Paraphrase-consistency training + retrieval defense + rewrite arm | Invariance by construction, not patching | Krishna et al. (NeurIPS 2023), RAIDAR (ICLR 2024) |
| Adversarial retraining loop | Disagreement-driven active learning + group DRO | Automate hard-example mining; optimize worst-group loss | Sagawa et al. (ICLR 2020) |
| ESL debiasing (retraining) | Cohort-conditional conformal calibration | Per-cohort FPR guarantee instead of hoping the model debiased | conformal + ESL corpora |
| Zero-shot generalization testing | Training-free incremental adaptation + zero-shot statistical arms | Adapt to new LLMs *without retraining* | DeTeCtive TFIA, Binoculars (ICML 2024) |
| — (GPTZero has no equivalent) | Watermark detection arm | Detect SynthID-Text / Kirchenbauer watermarks | Nature 2024 |
| — (GPTZero has no equivalent) | Generator attribution | Report *which* LLM family likely wrote it | FAID |

---

## 1. Detection as style retrieval, not classification (replaces the binary classifier)

**Why it is more novel.** Binary classifiers memorize surface artifacts of the
generators in their training set and degrade on unseen LLMs. DeTeCtive
(NeurIPS 2024) reframes the task: learn a *writing-style embedding space* via
multi-level contrastive learning, where distances encode author relatedness at
several granularities (human vs. AI, LLM family, specific model). Inference is
dense retrieval: embed the query, kNN against a feature database, vote. FAID
(EACL 2026) extends this to three classes (human / AI / human-AI
collaborative) plus LLM-family attribution.

**The killer feature — Training-Free Incremental Adaptation (TFIA):** when a
new LLM ships, you embed a few hundred of its outputs and *add them to the
index*. No retraining. GPTZero needs a full retraining cycle for the same
adaptation.

**Implementation (free):**
- Contrastive fine-tune an open encoder (e5-base or DeBERTa-v3) with the
  multi-level InfoNCE objective on RAID + MAGE + FAIDSet, on Kaggle GPUs.
- Serve with FAISS (CPU, free) inside the existing `packages/detection`
  ensemble as a new arm: `style_retrieval` score = weighted kNN vote.
- Nightly GitHub Actions job generates ~500 samples from newly released open
  models (via HF free inference) and appends embeddings to the index —
  continuous adaptation with zero training compute.

## 2. Latent trajectory discrimination (new signal family)

GTCL (2026) models a document as a *trajectory*: encode overlapping windows,
take consecutive embedding differences, and contrastively learn on the
sequence of semantic transitions. Hypothesis: autoregressive generation leaves
structural regularities in how meaning *moves* sentence-to-sentence, which
survive paraphrasing better than lexical features. We already compute
windowed embeddings for the heat-map, so the marginal cost is one small
transformer projection head over existing vectors.

## 3. Provable FPR control via multiscaled conformal prediction (replaces threshold calibration)

GPTZero tunes thresholds on held-out data — an empirical FPR estimate with no
guarantee. Multiscaled Conformal Prediction (ACL 2025) gives a
**distribution-free, mathematically guaranteed upper bound on FPR**: compute
nonconformity scores on a human-only calibration set, stratified by text
length ("multiscaled"), and derive quantile thresholds per length bucket.

For VeritasAI: replace `OPERATING_POINTS` in `ensemble.py` with conformal
quantiles computed per length bucket *and per cohort* (see §6). The product
claim upgrades from "we target 1% FPR" to "FPR ≤ 1% with statistical
guarantee, per cohort" — something GPTZero cannot claim.

## 4. Exact boundary detection for mixed text (replaces the sliding-window mixed module)

Upgrade sentence-window scoring to true change-point detection:
- **Sequence labeling:** fine-tune a token-classification head (Longformer or
  DeBERTa) on SemEval-2024 Task 8 Subtask C (human→machine boundary
  identification) plus FAIDSet collaborative texts, emitting per-token
  P(AI) with a transition penalty (CRF layer).
- **Statistical change-point:** run PELT/binary segmentation over per-token
  curvature scores from the Fast-DetectGPT arm to find distribution shifts.
- Agreement between the two → "AI takes over at sentence 7" with a confidence
  interval, rendered in the existing heat-map UI as an explicit boundary
  marker.

## 5. Paraphrase robustness by construction (replaces the "paraphraser shield")

Three complementary, more principled mechanisms:
1. **Consistency training:** during contrastive training, treat (document,
   paraphrase-of-document) as positive pairs, generating paraphrases on-the-fly
   with free open models (Qwen2.5, DIPPER). The encoder learns
   paraphrase-invariant style features instead of patching against known tools.
2. **Retrieval defense (Krishna et al., NeurIPS 2023):** keep a corpus of
   embeddings of AI generations we have seen (and of popular humanizer
   outputs); paraphrasing preserves semantics, so semantic-neighbor search
   catches paraphrased versions of known generations.
3. **Rewrite arm (RAIDAR, ICLR 2024):** ask a small open LLM to rewrite the
   input; AI text is modified less than human text under rewriting. Cheap
   (one generation call), zero-shot, and orthogonal to encoder-based arms.

## 6. Fairness with guarantees, not vibes (replaces ESL debiasing)

GPTZero retrained on ESL essays and hoped the bias went away. We do both, and
add a guarantee:
- Include ESL human corpora (TOEFL11, ICNALE, EFCAMDAT, Lang-8) in training
  *and* as separate conformal calibration cohorts.
- **Cohort-conditional conformal thresholds** guarantee FPR ≤ target for each
  cohort independently — the ESL false-positive rate is bounded by
  construction, not by anecdote.
- Train with **group DRO** (minimize worst-group loss across domain × cohort
  groups) so the encoder cannot trade ESL accuracy for aggregate accuracy.
- Publish per-cohort FPR in the eval report; abstain ("inconclusive") when a
  document's cohort cannot be established.

## 7. Automated adversarial loop (upgrades the manual retraining loop)

- **Disagreement sampling:** production documents where the ensemble arms
  disagree strongly (classifier says AI, trajectory/statistical arms say
  human, or vice versa) are the most informative; queue them (anonymized,
  opt-in) for labeling and retraining.
- **Self-play red team:** a scheduled free-GPU job prompts open models to
  *evade the current detector* (humanize, restructure, inject noise), verifies
  evasion against the live ensemble, and feeds successful evasions back as
  labeled hard negatives — GPTZero's loop, but without waiting for users to
  find the exploits.
- Monthly retrain via the existing GitHub Actions pipeline; deploy only if
  RAID-dev + worst-group metrics improve.

## 8. New arms GPTZero does not have

- **Watermark detection:** Google open-sourced SynthID-Text (Nature 2024);
  Kirchenbauer-style green-list watermarks are detectable with published
  statistics. A watermark hit is near-certain provenance evidence and costs
  milliseconds. Report it as a separate signal ("cryptographic watermark
  detected: Gemini family").
- **Generator attribution:** the style-retrieval space (§1) gives us LLM-family
  attribution for free (nearest neighbors carry generator labels). Verdicts
  become explainable: "stylistically nearest to GPT-4-class outputs (0.87
  similarity)".
- **Reasoning-model coverage:** generate training/eval corpora from open
  reasoning models (DeepSeek-R1, QwQ) — the open-weights analogue of
  GPTZero's o1 benchmarking, but we can train on it, not just test on it.

## 9. Architecture fit (what changes in this repo)

- `packages/detection`: add `style_retrieval.py` (FAISS kNN arm),
  `trajectory.py` (GTCL head), `boundary.py` (token-level segmentation),
  `rewrite.py` (RAIDAR arm), `watermark.py`; extend `ensemble.py` to a
  learned stacker over 6+ signals with conformal thresholds from
  `calibration/` artifacts.
- `packages/training`: contrastive training scripts (Kaggle-ready, PEP 723),
  group-DRO trainer, paraphrase-consistency data pipeline, red-team self-play
  job.
- `apps/api`: signals payload grows (attribution, boundary, watermark);
  response schema is already extensible via the `signals` dict.
- `apps/web`: boundary markers in the heat-map, attribution chip, per-cohort
  FPR disclosure in the report.
- Evaluation: unchanged strategy — RAID leaderboard remains the public
  benchmark; add FAIDSet, RealDet, and M4GT-boundary for the new capabilities.

## Key references

- DeTeCtive: multi-level contrastive learning + retrieval — [arxiv.org/abs/2410.20964](https://arxiv.org/abs/2410.20964)
- FAID: fine-grained human/AI/collaborative + family attribution — [aclanthology.org/2026.eacl-long.151](https://aclanthology.org/2026.eacl-long.151/)
- GTCL: latent trajectory discrimination — [arxiv.org/abs/2607.14967](https://arxiv.org/abs/2607.14967)
- Multiscaled Conformal Prediction for MGT detection — [aclanthology.org/2025.acl-long.601](https://aclanthology.org/2025.acl-long.601.pdf)
- RAIDAR: detection via rewriting — [arxiv.org/abs/2401.12970](https://arxiv.org/abs/2401.12970)
- Retrieval defense against paraphrase attacks — [arxiv.org/abs/2303.13408](https://arxiv.org/abs/2303.13408)
- Binoculars: zero-shot LLM-pair contrast — [arxiv.org/abs/2401.12070](https://arxiv.org/abs/2401.12070)
- Group DRO — [arxiv.org/abs/1911.08731](https://arxiv.org/abs/1911.08731)
- SynthID-Text watermarking — [nature.com/articles/s41586-024-08025-4](https://www.nature.com/articles/s41586-024-08025-4)
- SemEval-2024 Task 8 (boundary detection subtask) — [aclanthology.org/2024.semeval-1.279](https://aclanthology.org/2024.semeval-1.279/)
