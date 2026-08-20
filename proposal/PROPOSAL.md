# Doppel: Analysis-Preserving Synthetic Twins for Restricted Organizational Data

**Stage 1 proposal — *Organization Science*, "AI-Enabled Frontiers in Organizational Science"**
Repository: `doppel`. Licence: Apache-2.0. Models: open-weight only. No API keys anywhere.

---

### The idea in one sentence

`doppel` is reusable research infrastructure that takes a confidential organizational
dataset and a paper's analysis code, and emits a shareable synthetic twin plus a
machine-readable certificate that the paper's published tables recover on the twin
while membership-inference risk stays below a declared threshold.

### The currently-binding constraint

Organizational science does not mainly fail reproducibility because code will not run.
It fails because the data cannot leave the author's machine.

Fišar, Greiner, Huber, Katok, Ozkes and the Management Science Reproducibility
Collaboration (2024) assessed nearly 500 *Management Science* articles. When data
access was not an obstacle, more than 95 percent of articles under the 2019 disclosure
policy could be fully or largely reproduced. For 29 percent, at least part of the
dataset was inaccessible, dropping the overall rate to 68 percent; 88 percent of
failures were data-access failures. The journal's Code and Data Disclosure Policy then
compounds the problem: downloaders must certify that files will be used only to verify
the paper's main results. A package that cannot be reused is not research
infrastructure.

The pattern is older and wider than one journal. Bergh, Sharp, Aguinis and Li (2017)
could not retest about 70 percent of 88 *Strategic Management Journal* articles from
the numbers printed in them. Miske and 127 co-authors (2026), in SCORE's *Nature*
reproducibility study, obtained author-supplied data for only 24 percent of 600 papers
across 62 journals. The special issue's FAQ asks "What if my data cannot be shared?"
and answers that synthetic data may serve if the insights can be reproduced. That is
the door this proposal walks through.

Journals already ask for sample or synthetic files so that code can be smoke-tested.
Those files are almost always schema dummies: they let a script execute, and they do
not let another scholar ask a new question. Wang, Loignon, Shrestha, Banks and Oswald
(2025) showed that generative adversarial networks can approximate the moments of
organizational datasets — and then could not share even the synthetic files, because
data-management agreements had no object they were allowed to release. The field knows
synthetic data is possible. It does not have a certified artifact that a data editor,
an IRB, and a replicator can all treat as a substitute.

### How it works, in plain language

A researcher points `doppel` at two things they already have: the analysis file that
produces the paper's tables, and the confidential table that file reads. Three things
then happen, in order, and the third can veto the first two.

First, an open-weight language model is fine-tuned on a text encoding of the table —
each row written as a short sentence of the form `tenure is 4, voice is 3.2, unit is
sales` — which is the GReaT approach of Borisov, Seßler, Leemann, Pawelczyk and Kasneci
(2023). Language models handle mixed types and free-text columns without the brittle
preprocessing that CART synthesizers (Nowok, Raab & Dibben, 2016) and tabular GANs
(Xu, Skoularidou, Cuesta-Infante & Veeramachaneni, 2019) require. The fitted model
writes new rows. No original row is copied.

Second, an independent *recovery* module re-runs the author's analysis on the new rows
and scores the result against the published tables: signed change in each headline
coefficient in original-standard-error units, a significance-call match, and a
conclusion-level match. Recovery is the primary metric, not a Kullback–Leibler
divergence on the margins. A twin that matches means but reverses a hypothesis test
has failed.

Third, an independent *attack* module tries to determine whether any real record was
in the training table, using membership inference of the kind introduced by Shokri,
Stronati, Song and Shmatikov (2017) and shown by Hyeong, Kim, Park and Jajodia (2022)
to bite tabular synthesizers. If attack success clears a pre-declared bar, `doppel`
refuses to emit the twin. A pretty table that leaks is not a deliverable.

Only a twin that clears both bars is written to the replication package, together with
a certificate stating the recovery scores, the attack scores, the model revision hash,
the seeds, and the refusal rule. If the bars cannot be met jointly, the harness
returns a refusal and a Pareto plot. That refusal is a result, not a crash.

### Why this is infrastructure

Who uses it, before and after:

**Authors of restricted-data papers.** Today they ship log files, dummy CSVs, or an
access protocol a replicator at a non-WRDS institution cannot follow. After, they run
`doppel certify` as the last step of the analysis. The confidential file never leaves
their machine.

**Journal data editors.** Today they can check that code runs on a dummy. After, they
have a machine-readable claim — these tables recover, this attack failed — that they
can accept, send back, or refuse. *Management Science* has already started asking for
sample or synthetic files; `doppel` gives that request a standard object.

**Other scholars.** Today they cannot reanalyze the restricted corpus. After, they can
change a control or try a different estimator on the twin, with the certificate
telling them how far to trust the exercise.

Bail (2024), an editor of this issue, argued that social scientists need open-source
infrastructure they own rather than corporate models they rent. `doppel` is that kind
of object: local, open-weight, refuse-capable, and sitting in a workflow authors
already have.

### Why this is not incremental

"Use a synthesizer on management data" is a methods note, and Wang et al. (2025)
already wrote it. Three things make `doppel` a different object.

It changes the estimand. Census synthetic products such as the Synthetic Longitudinal
Business Database (Kinney, Reiter, Reznek, Miranda, Jarmin & Abowd, 2011) optimize
analytical validity for a statistical agency's canned queries. `synthpop` produces
test files that, by the authors' own statement, should not be used for final
inference (Nowok et al., 2016). Dummy files in finance replication packages preserve
schema so that merges execute. `doppel` asks whether *this paper's claims* survive,
and whether a determined reader can pull a real person or firm out of the substitute.
That is a joint test the field has not had.

It produces a refusal. Every prior organisational demonstration reports where
synthesis worked. `doppel`'s product includes the region where it will not sign.
Gartenberg, Hasan, Murray and Pierce (2026) warned that AI will produce more, not
better. A tool that will not emit a twin when the twin would mislead is a direct
answer to that warning.

It is aimed at reuse, not resemblance. A log file lets you watch the author work. A
dummy lets you watch the code work. A certified twin lets you work. That is the
frontier expansion: inferential reproducibility without the original data.

### What the Stage 1 prototype looks like

By 1 November 2026 the repository contains a working harness on four open datasets
treated as if they were confidential, so the prototype itself can be redistributed: a
public-survey workplace extract (standing in for OB employee surveys); one openly
licensed AEA labour or organizations package (standing in for a vendor-restricted firm
panel); a person-by-meeting table from the CC BY 4.0 AMI corpus; and a
contributor-by-project panel from permissively licensed open-source repositories.

The synthesizer is a GReaT-style fine-tune of Qwen3 (Apache-2.0) with OLMo 2
(Apache-2.0, open training data) as the auditable robustness arm. Baselines are
`synthpop` and CTGAN, run on the same files. Every twin ships with recovery and attack
reports. One notebook walks a data editor through accept / send-back / refuse. No
Compustat, WRDS, earnings-call vendor, or proprietary model.

### How we know it is correct

Correctness is not a vibe about realistic-looking rows. Four tests are pre-specified.

*Recovery on the author's spec.* The published (or, on stand-in data, the
pre-registered) tables are the target. We report the distribution of coefficient
shifts in original-SE units, not a single "close enough" flag.

*Held-out specifications.* We freeze a set of analyses the synthesizer is not
tuned against — extra controls, subsample splits, an alternative estimator — and
ask whether they recover too. A twin that only reproduces the specification it was
optimized on is a data-generating version of HARKing, and we will say so.

*Attack success.* Membership-inference AUC and true-positive rate at a low
false-positive operating point, on hold-out records the attack is not trained on.
Following Hyeong et al. (2022), we treat a synthesizer that can be attacked as not
shareable, however pretty its recovery scores.

*Baseline dominance, with an honest null.* If `synthpop` or CTGAN jointly clears
the same bars on a dataset, the language-model arm is not a contribution on that
dataset and will not be sold as one.

### Honest risks, and what would falsify it

The ethical failure mode is **false privacy assurance**: shipping a twin that looks
certified and is not. Mitigation is architectural — the attack module can veto
release — not documentary. Residual risk remains: membership inference is an
evolving attack, and a twin that fails today's attack may fail tomorrow's. Every
certificate therefore states the attack used, not "this data is safe."

Three results would falsify the proposal as infrastructure. If recovering published
coefficients requires a twin that membership inference can crack, the joint
utility–privacy set is empty for this field's analyses and `doppel` should not be
adopted. If twins recover in-sample tables and fail held-out specifications, they
are overfit to the author's garden of forking paths. If they work only on small
survey tables and not on firm panels, the user base collapses to a corner of OB
and the adoption claim is wrong.

Two further limits are not bugs; they are scope. Some vendor licences may forbid
even synthetic derivatives of the licensed extract; `doppel` cannot launder
Compustat. Stage 1 uses open stand-ins, so it does not prove that an IRB will
accept a twin of truly identifiable employee data. Both will be stated in the
certificate language rather than discovered by a reviewer.

### Why this is a strong Stage 1 fit

**Novelty.** Synthetic data is old. A certified, refuse-capable twin aimed at the
paper's own tables, sitting in the replication-package slot journals already have,
is not. Wang et al. (2025) reached the policy wall; this is the object on the other
side of it.

**Feasibility.** Every component exists. The scientific risk is the joint bar, not
missing parts.

**Stage of development.** This pass is idea development. The design, corpora,
licences, and falsifiers are specified. The harness is not yet built.

**Ethicality.** The purpose is to share less identifiable data. Public stand-ins
only at Stage 1. The remaining hazard is over-trust in a certificate, which is why
the certificate names the attack.

**Reproducibility.** Open weights, pinned revisions, open stand-in data, seeds,
one-command regeneration. The twins are shareable by construction.

**Scalability.** Typical analysis files are thousands to hundreds of thousands of
rows; fine-tuning a small open model on that scale is a lab-cluster job. New
datasets are a drop-in.

**Potential use and adoption.** This is the load-bearing cell for an infrastructure
submission. The user is already filling in a replication package. Journals are
already asking for synthetic files. A tool that produces the object they have
started to request, with a standard for when to refuse it, has a home in an
existing workflow.

**Frontier expansion.** It converts the restricted corpus from a dead end into a
reanalyzable object, and it makes the utility–privacy frontier a measured fact. If
the frontier is empty, the field learns that synthetic substitutes will not save
restricted-data science — the kind of boundary the call invites.

---

## References

Bail, C. A. (2024). Can generative AI improve social science? *Proceedings of the
National Academy of Sciences*, 121(21), e2314021121.
https://doi.org/10.1073/pnas.2314021121

Bergh, D. D., Sharp, B. M., Aguinis, H., & Li, M. (2017). Is there a credibility
crisis in strategic management research? Evidence on the reproducibility of study
findings. *Strategic Organization*, 15(3), 423–436.
https://doi.org/10.1177/1476127017701076

Borisov, V., Seßler, K., Leemann, T., Pawelczyk, M., & Kasneci, G. (2023). Language
models are realistic tabular data generators. *International Conference on Learning
Representations*. https://openreview.net/forum?id=cEygmQNOeI

Fišar, M., Greiner, B., Huber, C., Katok, E., Ozkes, A. I., & the Management Science
Reproducibility Collaboration (2024). Reproducibility in Management Science.
*Management Science*, 70(3), 1343–1356. https://doi.org/10.1287/mnsc.2023.03556

Gartenberg, C., Hasan, S., Murray, F., & Pierce, L. (2026). More versus better:
Artificial intelligence, incentives, and the emerging crisis in peer review.
*Organization Science*, 37(3), 795–812.
https://doi.org/10.1287/orsc.2026.ed.v37.n3

Hyeong, J., Kim, J., Park, N., & Jajodia, S. (2022). An empirical study on the
membership inference attack against tabular data synthesis models. *Proceedings of
the 31st ACM International Conference on Information and Knowledge Management*,
4064–4068. https://doi.org/10.1145/3511808.3557546

Kinney, S. K., Reiter, J. P., Reznek, A. P., Miranda, J., Jarmin, R. S., & Abowd,
J. M. (2011). Towards unrestricted public use business microdata: The Synthetic
Longitudinal Business Database. *International Statistical Review*, 79(3), 362–384.
https://doi.org/10.1111/j.1751-5823.2011.00153.x

Miske, O., Abatayo, A. L., Daley, M., et al. (2026). Investigating the
reproducibility of the social and behavioural sciences. *Nature*, 652(8108),
126–134. https://doi.org/10.1038/s41586-026-10203-5

Nowok, B., Raab, G. M., & Dibben, C. (2016). synthpop: Bespoke creation of synthetic
data in R. *Journal of Statistical Software*, 74(11), 1–26.
https://doi.org/10.18637/jss.v074.i11

Shokri, R., Stronati, M., Song, C., & Shmatikov, V. (2017). Membership inference
attacks against machine learning models. *2017 IEEE Symposium on Security and
Privacy*, 3–18. https://doi.org/10.1109/SP.2017.41

Wang, P., Loignon, A. C., Shrestha, S., Banks, G. C., & Oswald, F. L. (2025).
Advancing organizational science through synthetic data: A path to enhanced data
sharing and collaboration. *Journal of Business and Psychology*, 40(4), 771–797.
https://doi.org/10.1007/s10869-024-09997-w

Xu, L., Skoularidou, M., Cuesta-Infante, A., & Veeramachaneni, K. (2019). Modeling
tabular data using conditional GAN. *Advances in Neural Information Processing
Systems*, 32. https://arxiv.org/abs/1907.00503

Full verification status for every citation is in `REFERENCES.md`. Design detail is
in `TECHNICAL_APPENDIX.md`. The comparison against the other infrastructure-stream
candidates is in `LITERATURE.md`.
