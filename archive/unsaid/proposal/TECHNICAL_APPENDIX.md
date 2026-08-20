# Technical Appendix

**`unsaid` — measuring institutional omission and suppressed dissent from paired organizational
records.** Stage 1 package for *Organization Science*, "AI-Enabled Frontiers in Organizational
Science."

This appendix specifies the pipeline, the models and their licences, corpus construction per
substrate, the measurement-error layer, the validation design, and the compute budget. Everything
named here has been checked against a primary source in August 2026. Where something has not been
built yet, it says so. Where a licence or a term of use is unresolved, it says so.

---

## 1. Design commitments

Four commitments constrain every downstream choice, because they are what the call requires and what
makes the instrument usable by someone else.

1. **The primary label is document-derived, not model-derived.** A proposition is `omitted` because
   it appears in one document the organization published and not in another document the same
   organization published. The model's job is alignment, not judgement. This is what separates the
   design from LLM-as-annotator work and it is why the construct-validity argument is available to us
   at all.
2. **Open weights only, no API keys, no gated-by-payment anything.** Every model below is on the
   Hugging Face Hub under Apache-2.0, MIT, or CC-BY-4.0. There is no code path that calls a
   commercial API. A researcher with one 24 GB consumer GPU can run the released scorer; a researcher
   with no GPU can run it on CPU slowly, or consume the published measures.
3. **Nothing is redistributed that we do not have clear rights to redistribute.** Where licensing is
   settled (open-source governance corpora, FOMC, Wikipedia) we ship text. Where it is not (SEC
   registrant letters, ASRS) we ship a build script plus per-document SHA-256 checksums, so a third
   party can reconstruct a byte-identical corpus and verify it.
4. **The inference layer refuses to hide measurement error.** `unsaid-infer` will not return a point
   estimate for a downstream regression without a gold calibration sample of known sampling
   probability. This is a deliberate ergonomic obstruction, and §6 explains why we would rather
   annoy a user than let them publish a biased coefficient.

---

## 2. Pipeline architecture

Five stages. Stages A–D are text; stage E is the optional audio front end used only where the
verbatim record is spoken.

### A. Ingest and normalise

Per-substrate loaders (§4) emit a common `Record` object: `{event_id, role ∈ {verbatim, curated},
speakers[], segments[], provenance{url, accession, sha256, retrieved_at}}`. Provenance is mandatory
and is what makes the corpus auditable without redistribution. Format-specific work lives here:
uuencoded-PDF decoding plus `pypdf` text extraction for SEC `UPLOAD`, HTML parsing for `CORRESP`,
Markdown/reStructuredText parsing for PEPs, RFCs and KEPs, thread parsing for GitHub and Discourse.

### B. Proposition segmentation

Sentences are the wrong unit: a single spoken sentence often carries a claim, a hedge, and an
attribution, and the curated record may keep one and drop the others. We therefore decompose each
segment into atomic propositions with speaker attribution attached, and score at the proposition
level.

Two segmenters, deliberately: `chentong00/propositionizer-wiki-flan-t5-large` (Apache-2.0, 783M) as
the cheap default, and an instruction-prompted decoder (§3) for a stratified subsample, so we can
measure how much segmentation choice alone moves the final measures. Segmentation is the least
validated step in this literature and the one most likely to be silently load-bearing, so its
variance enters the reported error budget rather than being assumed away.

### C. Cross-document alignment

For each verbatim proposition, decide whether it survives into the curated record. Two passes:

1. **Retrieval.** Embed all propositions from both documents and retrieve top-*k* (default *k*=20)
   curated candidates per verbatim proposition, within event. `Qwen/Qwen3-Embedding-0.6B`
   (Apache-2.0) is the default; `BAAI/bge-m3` (MIT) is the alternate for the model-family robustness
   check. Retrieval is deliberately generous: recall matters far more than precision here, because
   the second pass can reject but cannot recover.
2. **Adjudication.** For each candidate pair, a natural-language-inference pass asks whether the
   curated text entails the verbatim proposition.
   `MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli` (MIT, 435M) is the default;
   `cross-encoder/nli-deberta-v3-large` (Apache-2.0) is the alternate. Reranking with
   `BAAI/bge-reranker-v2-m3` (Apache-2.0) or `Qwen/Qwen3-Reranker-0.6B` (Apache-2.0) is available for
   long curated documents where top-*k* retrieval saturates.

Each verbatim proposition receives one of four labels:

| Label | Definition |
|---|---|
| `represented` | Entailed by curated text with attribution preserved. |
| `compressed` | Entailed only jointly with sibling propositions, or entailed at strictly lower specificity. |
| `attribution-stripped` | Entailed, but the speaker is removed, generalised ("some participants"), or reassigned. |
| `omitted` | Not entailed by any curated candidate. |

`compressed` exists specifically so that legitimate summarisation does not get counted as omission.
Collapsing it into `omitted` is the single easiest way to produce a measure that is really just
document-length ratio, which is the first thing §7 tests.

### D. Scoring and distillation

The stage-C pipeline is too expensive to run at half-a-million-document scale and too heavy to hand
someone as a reusable instrument. So stage C is a **teacher**: its labels train a single small
sequence-classification student that takes a (verbatim proposition, curated document window) pair and
emits the four-way label directly. Target student size 0.6–4B, initialised from
`Qwen/Qwen3-4B-Instruct-2507` (Apache-2.0) or the 0.6B embedding backbone for the encoder variant.
The student is what a third party actually runs. We report teacher–student agreement and the loss in
downstream estimates from using the student, not just classification metrics.

Disagreement detection — needed for the Dissent Suppression Index — is a separate proposition-level
classifier. **This is the one label that is a model judgement rather than a document-derived fact,**
so it carries the full validation burden of §7 including human-coded gold data and inter-coder
reliability, and it is reported separately from the omission measures rather than folded into them.

### E. Audio front end (Council Data Project only)

ASR with `openai/whisper-large-v3` (Apache-2.0) or `nvidia/parakeet-tdt-0.6b-v2` (CC-BY-4.0);
diarisation with `pyannote/speaker-diarization-3.1` (MIT). **Honest constraint:** the pyannote
pipelines are *gated* on the Hub — free, no payment, but requiring a Hugging Face account and
acceptance of user conditions, which is a real if minor reproducibility friction we will document in
the README rather than gloss. `nvidia/diar_streaming_sortformer_4spk-v2` (CC-BY-4.0) is the ungated
fallback. We do **not** use `nvidia/diar_sortformer_4spk-v1`: it is CC-BY-NC-4.0, and a
non-commercial clause is inappropriate for infrastructure other people are meant to reuse freely.

ASR error enters on the verbatim side, which is the wrong direction — it manufactures apparent
omissions. Where a human transcript exists we use it and treat ASR as a robustness arm only.

---

## 3. Model inventory (all verified on the Hugging Face Hub, August 2026)

| Role | Model | Params | Licence | Notes |
|---|---|---|---|---|
| Teacher / segmenter (large) | `openai/gpt-oss-20b` | 21.5B | Apache-2.0 | Primary teacher. MXFP4 weights run in ~16 GB. |
| Teacher family B | `Qwen/Qwen3-8B` | 8.2B | Apache-2.0 | Cross-family variance check. |
| Teacher family C | `microsoft/phi-4` | 14.7B | MIT | Second cross-family check. |
| Teacher family D | `mistralai/Mistral-Small-3.2-24B-Instruct-2506` | 24.0B | Apache-2.0 | Optional third. |
| Fully-open-data check | `allenai/OLMo-2-1124-13B-Instruct` | 13.7B | Apache-2.0 | Open training data; useful for contamination arguments. |
| Student scorer | `Qwen/Qwen3-4B-Instruct-2507` | 4.0B | Apache-2.0 | Distillation target. |
| Proposition segmenter | `chentong00/propositionizer-wiki-flan-t5-large` | 783M | Apache-2.0 | Cheap default. |
| Embeddings | `Qwen/Qwen3-Embedding-0.6B` | 596M | Apache-2.0 | Default retriever. |
| Embeddings (alt) | `BAAI/bge-m3` | — | MIT | Robustness arm. |
| Reranker | `BAAI/bge-reranker-v2-m3` | 568M | Apache-2.0 | Long curated documents. |
| Reranker (alt) | `Qwen/Qwen3-Reranker-0.6B` | 596M | Apache-2.0 | Robustness arm. |
| Entailment | `MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli` | 435M | MIT | Default adjudicator. |
| Entailment (alt) | `cross-encoder/nli-deberta-v3-large` | 435M | Apache-2.0 | Robustness arm. |
| ASR | `openai/whisper-large-v3` | 1.5B | Apache-2.0 | Audio substrate only. |
| ASR (alt) | `nvidia/parakeet-tdt-0.6b-v2` | 0.6B | CC-BY-4.0 | English-only, fast. |
| Diarisation | `pyannote/speaker-diarization-3.1` | — | MIT (**gated**) | Account + accepted conditions required. |
| Diarisation (ungated) | `nvidia/diar_streaming_sortformer_4spk-v2` | — | CC-BY-4.0 | Fallback with no gate. |

**Substitution we made and why.** The prior ideation memo named Gemma as a model family.
`google/gemma-3-12b-it` does exist, but its licence is the custom *Gemma Terms of Use* — not an
OSI-approved licence, carrying use restrictions and a distribution-of-derivatives obligation — and
the repository is gated. For a package whose entire pitch is that other researchers can reasonably
access the workflow, we replaced it with `microsoft/phi-4` (MIT) and
`mistralai/Mistral-Small-3.2-24B-Instruct-2506` (Apache-2.0). No functional loss; a real licensing
gain. We also dropped `nvidia/diar_sortformer_4spk-v1` for its non-commercial clause.

Every model is pinned by revision SHA in a lockfile, because "we used Qwen3-8B" is not a reproducible
statement.

---

## 4. Corpus construction per substrate

Volumes, licences, prior literature, and rejected substrates are in `SUBSTRATES.md`. This section is
the mechanics.

### 4.1 SEC filing-review correspondence (firms)

- **Discovery.** Quarterly `form.idx` files at
  `https://www.sec.gov/Archives/edgar/full-index/{year}/{QTR}/form.idx` enumerate every `UPLOAD` and
  `CORRESP` submission. Our sweep of 2004–2026 counted **239,094 `UPLOAD` + 263,618 `CORRESP` =
  502,712 documents** (not the ~600,000 the brief and prior memo assumed).
- **Thread reconstruction.** Every 2024 `UPLOAD` we sampled (8/8) carries a
  `PUBLIC REFERENCE ACCESSION NUMBER` header pointing at the filing under review — a direct
  machine-readable edge, no heuristic needed for the modern period. File-number matching (as in
  `edgartools`) is the fallback for older submissions and for chaining rounds within a thread.
- **Extraction.** `UPLOAD` letters are uuencoded PDFs inside the `.txt` submission wrapper. We have a
  working decoder (`uu` + `pypdf`); on our 2/2 sampled letters, extraction was clean and
  well-ordered. `CORRESP` is HTML. Extraction quality gets measured against a hand-transcribed
  sample of 100 letters and reported as a number, not asserted.
- **Amendment diffing.** Amendments (`10-K/A`, `S-1/A`) are ordinary filings, so original and
  amendment align section-by-section and the *added* disclosure is localisable as text. Johnston &
  Petacchi (2017) report >17% of cases produce an immediate amendment, which bounds how much of the
  corpus supports this step.
- **Rate limits and politeness.** SEC caps automated access at **10 requests/second per requester**
  and requires a descriptive `User-Agent` with contact email; exceeding it returns HTTP 403 and a
  temporary block. There is no key and no paid tier. Our fetcher runs at 8 req/s with exponential
  backoff, an on-disk cache, and a request log.
- **Redistribution.** Staff letters are US government work. Registrant responses are third-party
  documents in a public federal record — lawfully readable and analysable, but we will not assert a
  right to redistribute them in bulk. **We ship no bulk EDGAR text**: build script, accession
  numbers, SHA-256 per document, plus derived non-substitutive artifacts (proposition labels,
  alignment indices, aggregates).

### 4.2 NASA ASRS (workplaces)

- **Pairing.** Reporter `Narrative` (verbatim, first-person) vs. analyst `Synopsis` (1–2 sentences).
- **Access.** ASRS Database Online query interface, export capped at **10,000 records per download**,
  so pulls are split into date windows (a published four-decade ASRS reproduction package uses eight
  windows for 1988–2026).
- **Redistribution: not permitted.** We ship an export recipe and checksums only. **[PARTIAL: our
  reading of NASA's terms currently rests on a third-party reproduction package's characterisation.
  Before submission we will obtain the position in writing from the ASRS office and quote it.]**
- **Bonus validation surface.** ASRS assigns structured `Detector`, `When Detected`, and `Result`
  codes independently of the narrative text, so instrument output can be checked against
  human-coded fields the model never saw.
- **Known hazard.** The Synopsis is mandated to be short. Length compression is the *design*, so this
  is where the discriminant test of §7.3 has to work hardest, and it is the substrate most likely to
  fail it.

### 4.3 Open-source governance (formal hierarchies; the redistributable corpus)

- **Python PEPs.** `python/peps` repository plus the `Discussions-To` and `Resolution` headers PEP 1
  mandates. PEPs are dual public-domain / CC0-1.0.
- **Rust RFCs.** `rust-lang/rfcs`, dual MIT / Apache-2.0 (RFC 2044); deliberation in the RFC pull
  request thread.
- **Kubernetes KEPs.** `kubernetes/enhancements`, Apache-2.0; deliberation in PR review threads.
- **Discussion-venue licensing.** GitHub PR thread content contributed to a repository travels with
  that repository's licence. `discuss.python.org` is a Discourse instance with its own terms.
  **[PARTIAL: we have not confirmed the content licence for `discuss.python.org`, nor for the older
  `python-dev` mailing-list archives. If it does not clear, we restrict the redistributed thread
  corpus to Rust and Kubernetes and ship Python threads as a fetch script.]**
- **Sampling discipline.** Withdrawn and rejected proposals stay in the sample. Dropping them
  conditions on the outcome and would bias every measure.

### 4.4 FOMC (calibration and the transparency natural experiment)

Transcripts (~5-year lag, from 1994 meetings) and minutes from the Federal Reserve website; all US
government work. The December 2004 acceleration of minutes release gives a dated policy shock with
paired records on both sides, and the minutes of that meeting record the participants' own worry that
early release would produce "less comprehensive, and therefore less useful, minutes" — a stated
mechanism, in the record, with a date. Hansen, McMahon & Prat's (2018) replication data are on
Harvard Dataverse under **CC0 1.0** (doi:10.7910/DVN/XAR1WZ, resolved and checked), so their measures
can be reused directly for convergent validity.

### 4.5 Council Data Project (multimodal)

Open-source pipeline with 350+ meetings from Seattle, Portland, and King County carrying video,
audio, transcript, and minutes with legislative items and roll-call votes for the same event. Only
substrate exercising stage E, and the only one where an outcome (the recorded vote) is measured
independently of any text.

### 4.6 Wikipedia AfD (power analysis and stress testing)

402,440 AfD discussions, 2005–2018, with 3M+ votes and comments (Mayfield & Black, 2019). Wikipedia
content is CC BY-SA and fully redistributable via dumps. Used for statistical power and
large-*n* robustness, not headline organizational claims. Note that Mayfield & Black's *derived*
corpus is distributed under GPL-3.0 — a code licence applied to data, which creates its own
downstream questions, so we rebuild from dumps rather than redistribute theirs.

### 4.7 Synthetic corpus (fully shareable; the one thing with ground truth)

Deliberations generated from templates plus open-weight models, then curated by a *known* omission
policy with planted omissions of known type and rate. This is the only corpus where the true omission
function is known exactly, so it is where we do power analysis, adversarial testing (can the
pipeline be fooled by paraphrase, by reordering, by attribution laundering?), and sensitivity to
segmentation choice. It is Apache-2.0 and shipped in full. It is a *diagnostic*, not evidence about
real organizations, and the appendix will say so wherever a number from it appears.

---

## 5. Reproducibility engineering

- Apache-2.0 repository; `pyproject.toml` with pinned versions; lockfile pinning every model
  revision SHA.
- Every corpus is a build script with a manifest of `(url, accession, sha256, retrieved_at)` and a
  `verify` command that fails loudly on mismatch.
- Configuration-as-data: one YAML per experiment, hashed into the output, so a result carries its own
  provenance.
- Determinism where it exists (fixed seeds, greedy decoding for label generation) and honesty where
  it does not: batched GPU inference is not bitwise reproducible across hardware, so we report
  run-to-run variance on a fixed sample instead of claiming determinism we cannot deliver.
- CPU-only smoke test on the synthetic corpus in CI, so a reader can run *something* end to end in
  minutes without a GPU.

---

## 6. Measurement-error and inference layer (`unsaid-infer`)

The failure mode this layer exists to prevent: a researcher takes our Omission Rate, drops it into a
regression as an outcome or regressor, and reports a coefficient and standard error as if the measure
were the construct. Egami, Hinck, Stewart & Wei (2023) show that plugging surrogate labels straight
into downstream inference yields substantial bias and invalid confidence intervals *even when
surrogate accuracy is 80–90%*. High accuracy does not rescue you, because the errors are
systematically correlated with the covariates of interest.

Three estimation modes:

1. **Design-based supervised learning** (Egami et al., 2023). Requires a gold-labelled random sample
   with **known** sampling probabilities; corrects the downstream estimator for surrogate error.
   Default when the analysis is a regression with our measure on either side.
2. **Prediction-powered inference** (Angelopoulos, Bates, Fannjiang, Jordan & Zrnic, 2023). Combines
   a small labelled sample with a large unlabelled one to get valid intervals for means, quantiles,
   and regression coefficients. Default for descriptive quantities and cross-substrate comparisons.
3. **Naive mode.** Available, loud, and labelled: any output carries a `NAIVE_NO_CALIBRATION` flag,
   and the flag is written into figure captions and exported tables, not just a log line.

The API refuses to return a point estimate without a calibration sample. We expect users to find this
irritating. That is the intended trade: the alternative is a tool that makes it easy to publish a
biased coefficient with a clean-looking standard error, and the peer-review-integrity concern the
special-issue editors themselves raise (Gartenberg, Hasan, Murray & Pierce, 2026) argues for the
friction.

Gold-sample design: stratified by substrate, topic, speaker role, and predicted-omission decile, with
sampling probabilities recorded per stratum, because DSL needs them known rather than estimated.
Target 1,500–2,500 hand-adjudicated propositions per substrate, two independent coders, disagreements
adjudicated by a third.

---

## 7. Validation design

Reported in this order, because the early tests can kill the project and should therefore run first.

### 7.1 Reliability (runs first, bounds everything else)

- **Human–human.** Two independent coders on the same propositions; Krippendorff's α for the
  four-way label and for the disagreement label. **We report this before any model metric**, because
  it is the ceiling. If humans cannot agree on whether a proposition survived, no model number means
  anything.
- **Model–human.** Teacher and student against the adjudicated gold, per label and per substrate.
- **Model–model.** Cross-family agreement (gpt-oss vs. Qwen3 vs. phi-4; two embedding families; two
  entailment models) with a full variance decomposition. Carlson and Burbano (2026) document that
  prompt and model choices shift annotations enough to change downstream conclusions in management
  tasks, so we publish this decomposition whatever it shows. Low cross-family agreement is itself a
  reportable finding about the limits of the method.

### 7.2 Criterion validity

- **SEC.** Does high predicted omission on an original filing predict (a) receiving a staff comment,
  (b) the specific topic of the comment, and (c) subsequent amendment? Held-out by filing year.
- **ASRS.** Do instrument outputs align with independently coded `Detector` / `Result` fields?
- **Council Data Project.** Does omission of a stated position predict the speaker's recorded vote —
  an outcome from outside the text entirely?
- **FOMC.** Convergent validity against Hansen et al.'s (2018) published measures on the same
  meetings, using their CC0 replication data.

### 7.3 Discriminant validity (the test most likely to fail)

- **Omission is not length.** Regress every measure on curated-document length, verbatim length,
  their ratio, topic, and speaker count. If the measures do not survive, we are measuring compression
  and we will report that.
- **Omission is not topic mix.** Within-topic and topic-fixed-effects estimates alongside pooled ones.
- **Attribution stripping is not omission.** The two must not be collinear; if they are, the third
  instrument does not exist and we drop it.
- **Dissent suppression is not overall omission.** If the Dissent Suppression Index is just Omission
  Rate rescaled, the interesting construct is absent and we say so.

### 7.4 Known-groups validity

Pre-registered directional predictions from settings where theory or institutional fact gives a sign:
routine procedural items should show lower omission than contested ones; FOMC meetings after December
2004 should differ from before in a direction we commit to in advance; rejected PEPs should retain
more objection content in their final documents than accepted ones (the "Rejected ideas" section is
literally the mechanism); and SEC-reviewed filings should score higher pre-review than post-amendment.

### 7.5 Transportability (the claim most likely to be wrong)

The instrument is trained where paired records exist and meant to be used where only one record
exists. That is the entire porting premise and it is an empirical claim, not an assumption. Tests:
cross-substrate transfer (train on one, test on another), performance stratified by SEC
review-selection propensity, and honest reporting of degradation. **If the instrument does not
transport, that is a boundary-setting negative result about AI-enabled measurement in organizational
research, and it is worth publishing as such.**

---

## 8. Compute budget

Sizing assumes a single 80 GB A100 or H100 for teacher passes and a 24 GB consumer GPU for the
student, since the second number is what determines whether anyone else can actually use this.

| Job | Scale | Hardware | Estimated GPU-hours |
|---|---|---|---|
| Teacher labelling, SEC pilot | ~10,000 letter/filing pairs | 1×A100 80GB | 250–450 |
| Teacher labelling, ASRS pilot | ~50,000 narrative/synopsis pairs | 1×A100 80GB | 150–300 |
| Teacher labelling, OSS governance | ~3,000 proposals, long threads | 1×A100 80GB | 100–200 |
| FOMC + council pilot | ~250 meetings (long documents) | 1×A100 80GB | 80–160 |
| Cross-family robustness (3 families) | stratified 10% subsample | 1×A100 80GB | 200–350 |
| Student distillation (training) | ~2M labelled propositions | 1×A100 80GB | 60–120 |
| Student inference (what users run) | 1,000 event pairs | 1×24GB consumer GPU | 2–6 |
| ASR + diarisation (councils) | ~250 meetings × ~2h audio | 1×24GB consumer GPU | 60–120 |
| Synthetic corpus generation | ~20,000 synthetic events | 1×A100 80GB | 40–80 |

Stage 1 total: roughly **1,000–1,800 A100-hours**, plus modest consumer-GPU time. That is an
academic-cluster-scale budget, not a frontier-lab budget, and it is deliberately sized so a
replicator with one GPU can rerun the student and the synthetic diagnostics end to end. Storage is
dominated by cached EDGAR documents (low hundreds of GB) and council audio (low TB if the full audio
arm is exercised).

The cost asymmetry is the point of the distillation step: the expensive teacher runs once, in our
lab; the cheap student is what gets released and reused.

---

## 9. Ethics and release constraints

- **No human subjects, no private data, no scraping of workplace communication.** Every primary
  source is an already-public organizational record. The obvious version of this project — run the
  instrument on internal Slack, email, or meeting recordings — is ethically fraught and unshareable,
  and its absence is part of why the construct has stayed unmeasured.
- **Aggregation by default.** This is a transparency-auditing instrument, and pointed at a named
  individual it becomes something else. Released measures aggregate to the event or organization
  level. Speaker-level analysis is possible in the code for research use with justification, but is
  not what we publish, and ASRS de-identification makes it impossible there anyway.
- **Naming discipline.** We measure a **recording gap**. Summarisation is legitimate and necessary.
  Intent is not observable from a document pair, and no output of this instrument licenses a claim
  that an organization concealed something. Only in the SEC substrate does an external authority
  adjudicate that a specific absence should not have been an absence, and even there the label is
  "the staff thought this was missing," not "the firm knew and withheld."
- **Dual-use.** An instrument that scores organizations on what they leave out could be used to rank
  or shame. We think the transparency benefit dominates for public records, but we will document the
  concern in the repository rather than leave it for a reviewer to raise.

---

## 10. What is built, and what is not

**Built and verified (August 2026).** Full substrate verification: access mechanics, licensing, and
volume for each substrate; a complete sweep of EDGAR's 2004–2026 quarterly form indexes yielding the
502,712 figure; a working uuencoded-PDF decoder with clean text extraction on sampled staff letters;
confirmation that modern staff letters carry a machine-readable pointer to the reviewed filing;
resolution of the Hansen et al. Dataverse package and its CC0 licence; and verification of every
model in §3 on the Hub with its licence and gating status.

**Not built yet.** The pipeline itself. Stages A–E, the student distillation, `unsaid-infer`, the
gold-coding protocol, and the synthetic corpus are specified here and are the Stage 1 build. Nothing
in this repository is a stub or a placeholder pretending otherwise; the current artifact is a verified
design and a verified data foundation, which is what we are claiming and no more.

**Open items we will not paper over.** The `discuss.python.org` and `python-dev` content licences;
NASA's redistribution position in writing; measured PDF-extraction error against a hand-transcribed
sample; and whether the paired-record label transports off the substrates that generate it, which is
the question the whole design lives or dies on.

---

*Full citations with DOIs and verification status: `REFERENCES.md`. Substrate volumes, licensing, and
rejected candidates: `SUBSTRATES.md`.*
