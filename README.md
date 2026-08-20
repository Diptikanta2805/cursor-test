# `doppel` — Analysis-Preserving Synthetic Twins

**Reusable research infrastructure for the *Organization Science* special issue
"AI-Enabled Frontiers in Organizational Science"** (Stage 1 deadline 1 November 2026).

When an organizational scholar cannot share the data, other scholars currently get a log
file, a dummy table that lets the code run, or nothing. `doppel` emits a **shareable
synthetic twin** of the analysis file plus a **certificate** that the paper's tables
recover on the twin while membership-inference risk stays below a declared threshold.
The twin is what other people actually reanalyze. The certificate is what a journal
data editor can accept or refuse.

Open-weight models only. No proprietary APIs. Stage 1 uses openly licensed datasets
treated as if they were confidential, so the prototype itself is reproducible.

---

## Where to start

| File | What it is |
|---|---|
| [`proposal/PROPOSAL.md`](proposal/PROPOSAL.md) | **Start here.** The Stage 1 proposal (~1,800 words plus references). |
| [`proposal/TECHNICAL_APPENDIX.md`](proposal/TECHNICAL_APPENDIX.md) | Harness, models, certificates, corpora, validation, compute, ethics. |
| [`proposal/STAGE1_SCORECARD.md`](proposal/STAGE1_SCORECARD.md) | Honest scores against the eight Stage 1 criteria. |
| [`proposal/REFERENCES.md`](proposal/REFERENCES.md) | Every citation with DOI and verification status. |
| [`proposal/LITERATURE.md`](proposal/LITERATURE.md) | The three infrastructure families compared, and why this one won. |

A previous measurement idea (`unsaid`) is preserved under [`archive/unsaid/`](archive/unsaid/)
and is not the current proposal.

## What this is, and what it is not

- **It is** reusable infrastructure other scholars drop into an existing replication-package
  workflow, aimed at the constraint that actually binds empirical organizational research:
  data that cannot be shared.
- **It is not** a conventional paper about synthetic data, not a faster version of
  `synthpop`, and not a claim that every restricted dataset can be replaced. If the
  utility–privacy frontier is empty for the analyses this field actually runs, that is a
  publishable negative result, and the harness is built to say so.

## Constraints we hold to

- Open weights only (Apache-2.0 / MIT). No API keys.
- We redistribute only openly licensed stand-in data and the synthetic twins derived from
  them. We do not ship Compustat, WRDS, or any vendor extract.
- A twin that recovers the author's tables but fails the membership-inference bar is
  **refused**, not released with a warning buried in a README.
- A recording of the author's run (a log file) is not a substitute for a twin. The point
  is reanalysis, not spectacle.

## Current state

This repository contains the developed idea, the verified literature foundation, and the
Stage 1 design. **It does not contain prototype code.** The call asked for idea development
in this pass; an empty scaffold would misrepresent the state of the work.

Nothing here should be read as a claim that this submission will be accepted.

Licence for this repository's content: Apache-2.0 (intended for the code and twins to follow).
