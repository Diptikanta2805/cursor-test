# Stage 1 Self-Assessment Scorecard

**`doppel` — analysis-preserving synthetic twins for restricted organizational data.**
Assessed against the eight criteria used for this Stage 1 package of the
*Organization Science* special issue "AI-Enabled Frontiers in Organizational
Science."

**The scale is ours, not the editors'.** They publish criteria, not weights. We
score 1–5 to force a discrimination between what this package does well and what
it does not, and we state a residual weakness for every cell. A scorecard of
eight 5s is a pitch. **No score here predicts an outcome.**

The live call lists *Auditability* rather than *Stage of development*. We score
stage of development as instructed for this package, and treat auditability as
part of reproducibility and of the certificate contract (see residual notes).

| # | Criterion | Score |
|---|---|---|
| 1 | Novelty | 4 / 5 |
| 2 | Feasibility | 4 / 5 |
| 3 | Stage of development | 2 / 5 |
| 4 | Ethicality | 4 / 5 |
| 5 | Reproducibility | 5 / 5 |
| 6 | Scalability | 4 / 5 |
| 7 | Potential use and adoption | 5 / 5 |
| 8 | Potential to expand the research frontier | 4 / 5 |
| | **Total** | **32 / 40** |

The distribution is the signal: this is a high-adoption infrastructure idea with
a verified constraint and a **weak stage of development**, because the harness is
specified and not built.

---

## 1. Novelty — 4 / 5

Synthetic data is not new. Official statistics have shipped synthetic establishment
files (Kinney, Reiter, Reznek, Miranda, Jarmin & Abowd, 2011). R users have
`synthpop` (Nowok, Raab & Dibben, 2016). Organizational scientists have a GAN
tutorial (Wang, Loignon, Shrestha, Banks & Oswald, 2025). Language models can
write tabular rows (Borisov, Seßler, Leemann, Pawelczyk & Kasneci, 2023).

The novelty is the *object* and the *estimand*. The object is a certified twin
that sits in the replication-package slot journals already have, with a veto for
membership inference (Shokri, Stronati, Song & Shmatikov, 2017; Hyeong, Kim, Park
& Jajodia, 2022). The estimand is whether *this paper's tables* recover, not
whether margins match. Wang et al. reached a policy wall: they could not share
the synthetics. `doppel` is the artifact on the other side of that wall.

**Residual weakness.** A reviewer who collapses "synthetic data" into one
category will read this as a follow-up to Wang et al. or as `synthpop` with a
language model. The proposal has to lead with the joint recovery-and-attack
certificate and with the journal workflow, not with the generator.

## 2. Feasibility — 4 / 5

Every component is off the shelf: GReaT-style fine-tunes on Apache-2.0 models,
`synthpop`, CTGAN, membership-inference attacks, open stand-in datasets, a
one-command certificate. Compute is a couple of hundred GPU-hours, not a
training run. The scientific risk is whether the joint bar can be cleared, which
is a result either way.

**Residual weakness.** Adapter coverage (R/Python now, Stata later) and the
possibility that vendor licences forbid even synthetic derivatives of the
extracts this field actually uses. Feasibility of the *harness* is high;
feasibility of *replacing Compustat in a replication package* is a legal
question we do not control.

## 3. Stage of development — 2 / 5

**This is the weakest cell and the honest score is low.**

What exists is a verified constraint, a verified gap in prior art, a licence
plan, a certificate contract, and falsifiers. What does not exist is the
harness. This pass was idea development; there is no placeholder code, because
an empty scaffold would misrepresent the state of the work.

What would close the gap, in order: (1) end-to-end `certify` on the survey
stand-in, with the joint bar reported whichever way it comes out; (2) the
certificate renderer a data editor can use without reading this appendix; (3)
the AEA-package stand-in, which is the firm-panel stress test.

The live call's *Auditability* criterion is stronger than this cell: the
certificate, hashes, and attack scores are designed so a third party can audit a
claim without the confidential file. That property is specified, not demonstrated.

## 4. Ethicality — 4 / 5

The purpose is to share *less* identifiable data. Stage 1 uses public stand-ins.
The confidential hash never reconstitutes a row. The attack module can veto
release. We refuse the words "anonymized" and "de-identified."

**Residual weakness.** False privacy assurance. A certificate that a later
attack breaks becomes a weapon against the people in the original file. Naming
the attack in the certificate is a mitigation, not a guarantee. Secondarily, a
good synthesizer can fabricate a plausible package for a paper that was never
run; hashing the confidential file reduces that risk and does not eliminate it.

## 5. Reproducibility — 5 / 5

Open weights, pinned revisions, open stand-in data, seeds, containerised
baselines, one-script figure regeneration. The twins are shareable by
construction, which is the constraint the call imposes ("What if my data cannot
be shared?"). No API keys. No vendor extracts in the artifact.

**Residual weakness.** Fine-tunes are not bitwise reproducible across GPU
skus. We report run-to-run variance on a fixed sample rather than claiming
determinism we cannot deliver. The AEA stand-in must be licence-checked
deposit-by-deposit; a single copy-paste from openICPSR would be a mistake.

## 6. Scalability — 4 / 5

Organizational analysis files are typically thousands to hundreds of thousands
of rows. Fine-tuning a 4B–8B model on that scale is routine. New datasets are a
typed-table drop-in. The expensive step (fine-tune + attack grid) runs once per
paper, on the author's machine or cluster; replicators only run the analysis on
the twin.

**Residual weakness.** Very wide tables (hundreds of columns) and very long
free-text fields will strain the sentence-serialisation trick. Nested relational
structures (employees within teams within firms, with a network on the side)
are not a single table; Stage 1 handles a flat analysis file and is honest that
multi-table synthesis is later work.

## 7. Potential use and adoption — 5 / 5

**This is the load-bearing cell for an infrastructure submission, and the reason
this idea beat the rest of its stream.**

The user is not being asked to change fields or learn a new construct. They are
already building a replication package. Journals are already asking for sample
or synthetic files so that code can be smoke-tested. *Management Science*'s data
editors have said as much in public. Fišar et al. (2024) show that when data
*are* accessible, reproduction is 95 percent — so the binding constraint is the
file, not the scholar's willingness to share code. A tool that produces a
standard, refuse-capable object for the slot editors have started to request
has a home in an existing workflow.

Three audiences, each independently sufficient: authors of restricted-data
papers; journal data editors; methods instructors who need shareable demos of
"what a replication package looks like when the real data cannot ship."

**Residual weakness.** Adoption depends on editors accepting certificates.
Authors will not run a tool that journals ignore. Stage 1 therefore includes an
editor-protocol walkthrough, and the proposal should not pretend that a GitHub
star count is the same thing as a policy change. Vendor licences may still
forbid twins of the extracts people actually want to share.

## 8. Potential to expand the research frontier — 4 / 5

The expansion is inferential reproducibility without the original data: other
scholars can ask new questions of the restricted corpus, not merely confirm the
author's numbers. That is a different scientific object from a log file or a
dummy CSV. A second expansion is diagnostic: mapping the utility–privacy
frontier of the datasets this field actually uses. If the frontier is empty,
synthetic substitutes will not save restricted-data organizational science,
which is a boundary the call explicitly invites.

**Residual weakness.** The expansion is conditional on a non-empty feasible set
for at least one important class of study (employee surveys, or firm panels, or
both). If only tiny survey tables clear the joint bar, we have a teaching tool,
not a frontier. Held-out-specification failure would shrink the claim further,
to "the twin replays the author's spec" — useful for computational
reproducibility, not for reanalysis.

---

## Summary

**Strong.** Adoption path (7), reproducibility (5), a documented binding
constraint rather than a hoped-for one (Fišar et al., 2024; Miske et al., 2026;
Bergh et al., 2017).

**Thin.** Stage of development (3), unambiguously.

**The single largest risk to the design** is an empty joint feasible set:
recovery and privacy cannot be had together on the analyses organizational
scholars run. That test is cheap, it runs first, and we have committed to
reporting it whichever way it comes out. The second-largest is editorial
non-adoption: a beautiful certificate that no journal asks for.
