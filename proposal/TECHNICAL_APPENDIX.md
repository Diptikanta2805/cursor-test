# Technical Appendix

**`doppel` — analysis-preserving synthetic twins for restricted organizational data.**
Stage 1 package for *Organization Science*, "AI-Enabled Frontiers in Organizational
Science."

This appendix specifies the harness, the models and their licences, the certificate
contract, the Stage 1 corpora, the validation design, the compute budget, and the
ethics constraints. Where something has not been built yet, it says so.

---

## 1. Design commitments

Five commitments constrain every downstream choice. They are what the call requires
and what makes the artifact usable by someone else.

1. **Recovery of the paper's claims is the primary metric.** Distributional resemblance
   is reported; it is not the accept/refuse rule. A twin that matches means and
   reverses a hypothesis test has failed.
2. **The attack module can veto release.** A twin that recovers tables and fails
   membership inference is refused, not shipped with a buried caveat.
3. **Open weights only, no API keys.** Every named model is on the Hugging Face Hub
   under Apache-2.0 or MIT. There is no code path that calls a commercial API.
4. **We redistribute only what we clearly may.** Stage 1 stand-in datasets are openly
   licensed. Derived twins are Apache-2.0. We never ship Compustat, WRDS, BoardEx,
   Lightcast, or earnings-call vendor extracts, even as "examples."
5. **Refusal is a first-class output.** `doppel certify` may return `REFUSED` with a
   Pareto plot. That is a result.

---

## 2. Pipeline architecture

Four stages. The user-facing command is `doppel certify --analysis <script> --data
<file> --tables <spec.yaml>`.

### A. Ingest and canonicalise

The confidential file is read into a typed table: column names, types (numeric,
categorical, text, identifier), panel keys, and a data dictionary. Identifiers that
are not needed for the analysis (names, employee IDs, emails) are stripped before
synthesis and are not reconstructed. The analysis script is wrapped so that every
headline estimate is written to a canonical `results.json` (estimate, standard error,
N, *p* or equivalent, table/cell provenance). Stage 1 adapters cover R and Python;
Stata is a documented extension, not a November promise.

### B. Synthesize

Rows are serialised as unordered `key is value` sentences and an autoregressive
open-weight model is fine-tuned on that corpus — the GReaT recipe (Borisov et al.,
2023). Sampling produces a twin of configurable size, defaulting to the original *N*.
Identifiers are newly generated; they do not collide with real keys.

Two baselines run on the same file, with no claim that they are obsolete:

- **CART sequential synthesis** via `synthpop` (Nowok, Raab & Dibben, 2016), the
  official-statistics default.
- **CTGAN** (Xu, Skoularidou, Cuesta-Infante & Veeramachaneni, 2019), the GAN default
  that Wang, Loignon, Shrestha, Banks and Oswald (2025) used to introduce synthetic
  data to organizational scientists.

If a baseline jointly clears the recovery and attack bars, the language-model arm is
not a contribution on that dataset. The comparison is the point.

A third, optional arm encodes free-text columns (open-ended survey items, meeting
utterances) with the same open-weight backbone rather than dropping them, which is
what CART and CTGAN typically force. This is the only place the language-model arm
is allowed to claim an advantage *a priori*.

### C. Recover

The wrapped analysis is re-run on the twin. For each headline cell we store:

| Quantity | Definition |
|---|---|
| Δ / SE | Signed shift of the estimate, in original-standard-error units |
| Sign match | Same sign as the original estimate |
| Significance match | Same reject/retain decision at the paper's α |
| Conclusion match | Same directional claim as the paper's text for that test |

A twin *recovers* a table if every headline cell is inside a pre-declared tolerance
(default: \|Δ / SE\| < 0.5 and significance match) or if the certificate explicitly
lists the cells that miss and still claims only the rest. Partial recovery is
allowed; silent omission of a missed cell is not.

Held-out specifications — extra controls, a subsample split, an alternative
estimator — are declared before synthesis and are not used to train or select the
twin. They are the overfitting check.

### D. Attack and decide

Membership inference (Shokri, Stronati, Song & Shmatikov, 2017; Hyeong, Kim, Park &
Jajodia, 2022) is run in two modes:

- *Holder mode* (the data editor's audit): the attacker has the real table and the
  twin, and tries to separate members from a hold-out of the same population. This
  is an upper bound on leakage.
- *Reader mode* (the plausible adversary): the attacker has the twin and an
  auxiliary sample from a similar public source, not the real table.

Decision rule, pre-declared:

```
if recovery_pass and holder_auc <= 0.60 and reader_tpr@fpr=0.01 <= 0.05:
    emit twin + certificate
else:
    emit REFUSED + Pareto plot over synthesizer hyperparameters
```

The numeric bars above are Stage 1 defaults, not laws of nature. They are fixed
before looking at the stand-in results and will be reported as such. Moving them
after seeing the plots is a finding about us, not about the method.

---

## 3. The certificate

Every released twin is accompanied by a `certificate.json` and a one-page human
render. Required fields:

- provenance of the analysis script (hash) and of the (not released) confidential
  file (hash only);
- synthesizer family, model revision SHA, seeds, and compute;
- per-cell recovery scores;
- held-out specification scores;
- holder-mode and reader-mode attack scores, with the attack implementation's
  revision SHA;
- the decision (`ACCEPTED` / `REFUSED`) and the rule that produced it;
- a plain-language statement that the certificate names the attack used and does
  not claim "this data is safe."

A twin without a certificate is not a `doppel` artifact. Downstream users are
instructed to treat an uncertified lookalike as ordinary, unvalidated synthetic
data, which is to say: not for inference.

---

## 4. Model inventory (open-weight only)

| Role | Model | Licence | Notes |
|---|---|---|---|
| Primary synthesizer | `Qwen/Qwen3-8B` or `Qwen/Qwen3-4B-Instruct-2507` | Apache-2.0 | GReaT-style fine-tune; 4B is the laptop target |
| Fully-open-data arm | `allenai/OLMo-2-1124-13B-Instruct` | Apache-2.0 | Open training data; contamination arguments |
| Small synthesizer | `Qwen/Qwen3-0.6B` | Apache-2.0 | CI smoke tests and low-*n* surveys |
| Optional text column encoder | `Qwen/Qwen3-Embedding-0.6B` | Apache-2.0 | Free-text columns |
| Attack model | logistic / gradient-boosting over distances and densities; no proprietary LLM-as-judge | — | Deterministic given seed |

**Substitutions we will not make.** Gemma is excluded (custom non-OSI terms, gated
repository). Llama Community License is excluded. No OpenAI, Anthropic, or Google
API is used for synthesis, attack, or evaluation.

Every model is pinned by revision SHA. "We used Qwen3" is not a reproducible
statement.

---

## 5. Stage 1 corpora (stand-ins, not the restricted data)

Stage 1 cannot use the confidential files `doppel` is meant to replace, or the
prototype would itself be unreproducible. We therefore treat four *open* datasets
as if they were confidential: the real table stays in a private working directory
during a demo, and only the twin and certificate are "released."

| Stand-in | What it stands for | Licence / access | Honest limit |
|---|---|---|---|
| Public social-survey workplace items (job satisfaction, voice-like items, workplace structure) | The employee survey behind most OB papers | Public-use survey terms; we ship a build script plus checksums, not a bulk dump if the survey forbids redistribution | Not a firm's own employees; no employment relationship |
| One AEA Data and Code Repository package with an organizational or labour design | The vendor-restricted firm panel | AEA prefers CC-BY 4.0 for data and Modified BSD for code; per-deposit licence is checked and recorded | Not Compustat; we will not pretend it is |
| Person-by-meeting table derived from AMI | Instrumented team / meeting data | AMI is **CC BY 4.0** | Lab meetings, not a firm's |
| Contributor-by-project panel from Apache-2.0 / MIT open-source repositories | Internal HRIS / digital-trace organization | Repository licences; we restrict to permissively licensed projects and aggregate | Volunteer communities, not employment |

**Excluded, with reasons.** Compustat / CRSP / BoardEx / Lightcast: proprietary,
and some licences may forbid even synthetic derivatives. NASA ASRS: redistribution
is not permitted. *Management Science* replication packages: downloaders must
certify use only to verify the paper, so a derived benchmark would be a research
use we are not granted. Earnings-call transcripts: vendor terms prohibit
redistribution. These exclusions are findings about the field's auditability, not
inconveniences to work around.

---

## 6. Validation design

Reported in this order, because the early tests can kill the project.

1. **Smoke recovery.** On each stand-in, does any synthesizer recover the
   pre-registered tables inside tolerance? If none do, Stage 1 is a refusal
   result and is written up as such.
2. **Joint bar.** Of those that recover, which also fail membership inference
   in holder mode? The overlap is the feasible set. Empty overlap on a dataset
   is a dataset-level refusal.
3. **Held-out specifications.** Recovery on analyses the synthesizer was not
   tuned against. Collapse here means the twin memorised the author's spec.
4. **Baseline comparison.** Language-model vs. `synthpop` vs. CTGAN on the same
   bars. Claim advantage only where it is measured.
5. **Sensitivity to *n* and to column mix.** A grid over sample size and over
   presence of free-text columns, because that is where the GReaT-style arm is
   supposed to matter.
6. **Editor protocol.** A scripted walkthrough in which a person who is not the
   author applies the accept / send-back / refuse rule using only the certificate
   and the twin. If the protocol is unusable, adoption is a fantasy.

---

## 7. Compute budget

Sizing assumes a single 24–80 GB GPU for fine-tunes and a CPU path for
`synthpop`.

| Job | Scale | Hardware | Estimated GPU-hours |
|---|---|---|---|
| GReaT fine-tune, survey stand-in | ~3k–15k rows | 1×24 GB | 4–12 |
| GReaT fine-tune, AEA package | tens of thousands of rows | 1×80 GB | 12–40 |
| AMI person-meeting table | small | 1×24 GB | 2–6 |
| OSS contributor panel | tens to hundreds of thousands | 1×80 GB | 20–60 |
| OLMo robustness arm, 10% subsample | — | 1×80 GB | 20–40 |
| Attack grid (all twins × 2 modes) | CPU + light GPU | mixed | 10–20 |
| Baseline `synthpop` / CTGAN | CPU / 1×24 GB | mixed | 5–15 |

Stage 1 total: on the order of **100–200 GPU-hours**, academic-cluster scale. A
replicator with one consumer GPU can rerun the survey stand-in and the
certificate renderer end to end. That is the adoption-relevant number.

---

## 8. Ethics and release constraints

- **Stage 1 uses public stand-ins.** No human-subjects file, no employee
  communication, no vendor extract.
- **The confidential file never enters the released artifact.** Only a hash is
  stored, so a data editor can confirm the author ran on a particular file
  without receiving it.
- **Refusal over release.** False privacy assurance is worse than a missing
  twin. The attack veto exists for that reason.
- **Certificates name attacks, not safety.** We will not print "anonymized" or
  "de-identified" on a twin. Those words have legal meanings this method does
  not earn.
- **Vendor scope.** `doppel` does not launder a licence. If a vendor forbids
  derivative files, the author still cannot ship a twin of that extract. The
  tool's honest use in that case is: ship the twin of the *non-vendor* columns
  (surveys, hand-collected, public filings) and document the vendor remainder
  as before.
- **Dual use.** A good synthesizer can also fabricate a plausible-looking
  "replication package" for a paper that was never run. Mitigation: the
  certificate hashes the confidential file and the analysis script; a twin
  without a matching hash is not a `doppel` certificate. This is a mitigation,
  not a guarantee.

---

## 9. What is built, and what is not

**Specified and verified (August 2026).** The constraint (Fišar et al., 2024;
Bergh et al., 2017; Miske et al., 2026); the prior art and its wall (Wang et al.,
2025; Kinney et al., 2011; Nowok et al., 2016); the synthesizer families and
licences; the attack literature (Shokri et al., 2017; Hyeong et al., 2022); the
stand-in corpus plan; the certificate contract; the falsifiers.

**Not built yet.** The harness, the adapters, the certificate renderer, and the
four stand-in runs. There is no placeholder code in this repository. The current
artifact is a verified design, which is what this pass is claiming and no more.

**Open items we will not paper over.** Whether any vendor of the field's core
firm databases will permit synthetic derivatives; whether an IRB will accept a
twin of identifiable employee data (Stage 1 cannot show this); the numerical
location of the joint bar, which is an empirical unknown and the actual
scientific content of the prototype.
