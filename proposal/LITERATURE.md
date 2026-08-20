# Infrastructure-stream literature and the comparison that produced `doppel`

Stage 1 workup for the *Organization Science* special issue contribution type
**"Reusable research infrastructure"** (custom models, multi-agent workflows,
simulation environments, and related objects other scholars can use). Potential
use and adoption is the load-bearing criterion for this stream. Hard constraints:
reproducible, shareable data, no proprietary AI models.

The three parallel family memos (`custom_models.md`, `data_access.md`,
`agent_workflows.md`) were not on disk when this synthesis ran. This file
reconstructs the comparison from those families plus earlier ideation memos under
`/tmp/si_ideation/`, then records why `doppel` won. Ideas already explored in
this project — `unsaid`, `openfloor`, `orca`, ORGDOCK, silicon multiverse, OSS
digital twins, the detection frontier, the regression-table auditor — were treated
as occupied and ineligible.

---

## 1. What "infrastructure other scholars would switch to" means here

Bail (2024) argued that social scientists should build open-source infrastructure
they own. Gartenberg, Hasan, Murray and Pierce (2026) warned that AI is currently
producing more papers, not better ones. For this stream, a winning idea has to
be something a working organizational scholar would drop into a workflow they
already have — not a new construct, not a leaderboard, not a faster version of a
paper they were going to write anyway.

Three families were scored against that test.

---

## 2. Family A — Custom models

**Top-ranked idea: an open organizational language model / encoder** trained only
on public records (EDGAR 10-K/10-Q, patents, open-source governance, public
deliberation), replacing generic embeddings and finance-specific models for
management text-as-data.

**Why it lost.** Huang, Wang and Yang (2023) already shipped FinBERT, pretrained
on 10-Ks/10-Qs, analyst reports, and earnings transcripts, and showed gains on
financial information extraction. A second domain BERT, even a fully open one, is
the incremental object the call tells us not to send. Adoption of a new encoder
is slow: scholars will keep calling `text-embedding-3` or `Qwen3-Embedding` until
a model is obviously better *and* already in their stack. FinBERT's own pretraining
mix also includes proprietary transcripts and analyst reports, so "fully open
OrgLM" is a real gap — just not a currently-binding constraint on anyone's paper
this year.

**Strong runner-up: an open firm-entity resolver.** Matching names across patents,
filings, and Compustat is painful. About 30 percent of Compustat firms change
name at least once; about 20 percent of patents belonging to Compustat firms were
omitted or mismatched in the NBER 2006 files (Arora, Belenzon & Sheer, 2021).
That is a documented constraint. It lost because the cottage industry already
ships public linking files (NBER PDP, DISCERN). "Better fuzzy matching with an
open encoder" is useful consolidation, not a frontier prototype, and it still
depends on Compustat on one side of the join, which this call cannot redistribute.

---

## 3. Family B — Data access

**Top-ranked idea: `doppel`.** A certified, analysis-preserving synthetic twin
that fills the replication-package slot when the real data cannot ship.

**The constraint, documented.** When data are accessible, *Management Science*
reproduces at >95 percent; 29 percent of articles have inaccessible data, and
that is why the overall rate is 68 percent; 88 percent of failures are data
access (Fišar, Greiner, Huber, Katok & Ozkes, 2024). Author-supplied data for 24
percent of 600 SCORE papers (Miske et al., 2026). About 70 percent of 88 SMJ
articles could not be retested from the printed record (Bergh, Sharp, Aguinis &
Li, 2017). *Management Science* packages may not be reused for the downloader's
own research without permission. Journals already ask for sample or synthetic
files; those files are schema dummies. Wang, Loignon, Shrestha, Banks and Oswald
(2025) demonstrated GANs on organizational data and then could not share the
synthetics.

**Prior art, and why it is not the same object.** Kinney, Reiter, Reznek, Miranda,
Jarmin and Abowd (2011) built a Census product for one database. Nowok, Raab and
Dibben (2016) built test files that should not be used for final inference.
Borisov, Seßler, Leemann, Pawelczyk and Kasneci (2023) and Xu, Skoularidou,
Cuesta-Infante and Veeramachaneni (2019) built generators. Wang et al. (2025)
wrote the methods note for this field. None of them ships a refuse-capable
certificate that a data editor can accept, keyed to *this paper's tables*, with
membership inference as a veto (Shokri, Stronati, Song & Shmatikov, 2017; Hyeong,
Kim, Park & Jajodia, 2022).

**Runner-up: an open EDGAR-based firm panel as a Compustat substitute.** Several
open XBRL pipelines already exist. Incremental scraping is not a special-issue
prototype, and it does not help the survey, field-experiment, or NDA-firm papers
that are the worse data-access cases.

---

## 4. Family C — Agent workflows

**Top-ranked idea: a multi-agent qualitative-coding / content-analysis workflow**
that runs locally on open-weight models, with segment-level audit trails, so
qualitative organizational researchers stop pasting interview text into ChatGPT.

**Why it lost.** The niche is occupied. Zhao, Tan, Wong, Zhao, Chen and Liu (2025)
already published SCALE at ACL: multi-agent coding, discussion, codebook
evolution, human intervention. CentaurTA and QualAnalyzer sit in the same
neighbourhood. More importantly, the call's reject category is "faster, cheaper
versions of what we already do." A local NVivo-with-agents is exactly that,
however ethically preferable to uploading interviews to a vendor. Adoption would
be real; frontier expansion would not.

**Runner-up: a multi-agent packager that turns an analysis + confidential file
into a `doppel` certificate.** That is a workflow *inside* the winning idea, not
a competing one. Folded in.

---

## 5. Occupied ideas (ineligible)

| Idea | Why it is not this submission |
|---|---|
| `unsaid` | Measurement of omission from paired records; archived under `archive/unsaid/` |
| `openfloor` | Interactional-authority instrument from meeting video |
| `orca` | Multi-family construct-assay registry |
| ORGDOCK | Formal / LLM / human docking harness for synthetic organizations |
| Silicon multiverse | History-dependence coefficient from ensemble runs |
| OSS digital twins | Forecast-validated twins of named open-source projects |
| Detection frontier | Execution-grounded planted-defect testbed for peer review |
| Regression-table auditor (Ledger) | Data-free consistency checks on published tables |

`doppel` is none of these. It does not measure a construct, simulate an
organization, review a paper, or audit a table. It replaces a file that cannot
be shared with a file that can, under a test the field can refuse.

---

## 6. The ranking, and the bet

**`doppel` (data access) > open OrgLM (custom models) > SCALE-like coding agents
(agent workflows).**

Five reasons to bet on `doppel`.

1. **It removes a currently-binding, measured constraint.** Fišar et al. (2024)
   isolate data access as the residual, after code quality is no longer the story.
   Custom models and coding agents do not.
2. **Other scholars would use it in a workflow they already have.** Replication
   packages are mandatory at the journals that care. Dummy synthetic files are
   already being requested. That is the adoption path the criterion asks for.
3. **A prototype by 1 November 2026 is realistic** on open-weight models and open
   stand-in data. The scientific unknown is the joint bar, which is a result
   either way.
4. **It is not a conventional paper and not AI slop.** Wang et al. (2025) is the
   conventional paper. Dummy CSVs are the slop. A refuse-capable certificate is
   neither.
5. **Downside is still on-mission.** An empty utility–privacy frontier is
   boundary-setting work the call welcomes.

What has to be managed: stage of development is currently 2/5, because this pass
did not build the harness; false privacy assurance is the ethical failure mode;
vendor licences may still forbid twins of Compustat-class extracts; editorial
adoption is a policy act, not a GitHub act.

Nothing in this ranking is a forecast of acceptance.
