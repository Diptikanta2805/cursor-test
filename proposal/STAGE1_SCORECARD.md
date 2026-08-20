# Stage 1 Self-Assessment Scorecard

**`unsaid` — measuring institutional omission and suppressed dissent from paired organizational
records.** Assessed against the eight criteria published for the *Organization Science* special issue
"AI-Enabled Frontiers in Organizational Science."

**The scale is ours, not the editors'.** They publish criteria, not weights or a rubric. We score
each criterion 1–5 to force ourselves to discriminate between what this package genuinely does well
and what it does not, and we state a residual weakness for every criterion including the ones we
score highest. A scorecard where everything is a 5 is not an assessment; it is a pitch. **No score
here predicts an outcome, and nothing about this package makes acceptance likely or certain.**

| # | Criterion | Score |
|---|---|---|
| 1 | Novelty | 5 / 5 |
| 2 | Feasibility | 4 / 5 |
| 3 | Stage of development | 2 / 5 |
| 4 | Ethicality | 5 / 5 |
| 5 | Reproducibility | 4 / 5 |
| 6 | Scalability | 4 / 5 |
| 7 | Potential use and adoption | 4 / 5 |
| 8 | Potential to expand the research frontier | 5 / 5 |
| | **Total** | **33 / 40** |

The distribution is the honest signal: this is a strong *idea* with a verified data foundation and a
**weak stage of development**, because the pipeline is specified and not yet built. §3 does not soften
that.

---

## 1. Novelty — 5 / 5

**Evidence in the package.**

The construct is 26 years old and has only ever been measured by self-report. Morrison and Milliken
(2000) defined organizational silence as collective withholding; Morrison's (2023) decade-later review
documents how the literature grew without ever counting an omission. Every text-as-data alternative is
structurally incapable of the task: dictionary and embedding measures (Li, Mai, Shen & Yan, 2021)
operate only on surviving text, and LLM annotation (Gilardi, Alizadeh & Kubli, 2023) scores single
documents, not pairs.

The specific novelty is not "use AI on organizational text." It is that **the omission label is
derived from two documents the organization itself published**, which makes the primary construct
supervised and sidesteps the standard construct-validity attack on LLM-based measurement. The closest
published precedent, Hansen, McMahon and Prat (2018) in the *QJE*, measured how transparency changed
*what was said*; nobody has measured the gap between what was said and what was *recorded*.
Attribution Stripping Rate appears to be a genuinely new named construct.

The SEC substrate sharpens this. Accounting and finance have used comment letters for over a decade,
but as a *treatment* (a firm got reviewed; what happened to its cost of capital, audit fees,
disclosure?) — see Cassell, Dreher and Myers (2013), Johnston and Petacchi (2017), Bozanic, Dietrich
and Johnson (2017), Cassell, Cunningham and Lisic (2019). Nobody uses them as a *label* to train a
general omission detector portable to the filings that were never reviewed. Two reviews from inside
that literature name the gap: Li and Luo (2025) call for "precise measurement instruments," and
Johnston (2025) identifies heterogeneity in comment significance as the central unresolved problem.

**Residual weakness.** Cross-document alignment, entailment-based summary-faithfulness scoring, and
omission detection in summarisation are all active NLP research areas. Our novelty is in the
organizational construct, the supervision design, and the substrate discovery — *not* in the
technical primitives, which are standard. A reviewer who reads the appendix as a methods contribution
will correctly find it unremarkable. We should keep the claim where it belongs.

## 2. Feasibility — 4 / 5

**Evidence in the package.**

The parts most likely to be quietly impossible were checked first, and several turned out easier than
the literature implied:

- The EDGAR volume claim was *measured*, not repeated: a complete sweep of the 2004–2026 quarterly
  form indexes gives 502,712 `UPLOAD` + `CORRESP` documents. The brief and prior memo said ~600,000.
- Thread reconstruction is a solved problem for the modern period: all eight sampled 2024 `UPLOAD`
  submissions carry a `PUBLIC REFERENCE ACCESSION NUMBER` header pointing directly at the filing
  under review. No file-number heuristic needed.
- The awkward format problem is handled: staff letters are uuencoded PDFs inside a `.txt` wrapper, and
  we have a working decoder producing clean, well-ordered text on the letters we sampled.
- Rate limits are known and workable: 10 requests/second, no key, no paid tier; our fetcher targets 8
  with backoff and caching.
- Compute is academic-scale: roughly 1,000–1,800 A100-hours for the full Stage 1 build, with the
  released student model runnable on one 24 GB consumer GPU.

Infeasible options were cut rather than finessed. NLRB hearing transcripts would require per-case
FOIA requests, so they are out. Hospital M&M review is confidential and privileged, so it is out.
Earnings-call transcripts are proprietary, so they are out.

**Residual weakness.** Three real risks. The gold-coding burden is the largest single cost and the
one most likely to slip — 1,500–2,500 adjudicated propositions per substrate, two coders plus
adjudication, across three headline substrates. PDF-extraction error is unmeasured beyond a 2-document
sample. And the ASRS pull is rate-limited by a 10,000-record export cap, which makes a full historical
corpus a slow, many-window operation rather than a single job.

## 3. Stage of development — 2 / 5

**This is the weakest criterion in the package and the honest score is low.**

**Evidence in the package.** What exists is verification and design, and it is not trivial: full
substrate verification (access mechanics, licensing, volume) for six substrates plus six documented
rejections; a measured EDGAR document count; a working uuencoded-PDF decoder with clean extraction on
sampled letters; confirmation of the machine-readable letter-to-filing edge; resolution of the Hansen
et al. replication package and its CC0 licence; and licence-and-gating verification of all 17 models
the pipeline names, which produced two substitutions.

**Residual weakness.** The call asks for a research artifact with a working prototype or proof of
concept. **We do not have one yet.** Stages A–E, the distillation, `unsaid-infer`, the gold-coding
protocol, and the synthetic corpus are specified in the technical appendix and unbuilt. The current
instruction to this work was to develop the idea, not the system, so there is deliberately no
placeholder or stub code in this repository — an empty scaffold would misrepresent the state of the
work and we would rather be marked down honestly.

What would close the gap, in priority order: (1) an end-to-end pipeline on one substrate, with the
length-confound test reported, since that single test can invalidate the whole instrument; (2) the
synthetic corpus with planted omissions, which is fully shareable and gives ground truth; (3) the
`unsaid-infer` wrapper, which is small, self-contained, and independently useful to anyone doing
LLM-assisted measurement.

## 4. Ethicality — 5 / 5

**Evidence in the package.**

Every primary source is an already-public organizational record. No human subjects, no private data,
no scraping of workplace communication. Released measures aggregate to the event or organization level
by default, because a transparency-auditing instrument pointed at a named individual becomes a
different and worse thing. ASRS is de-identified at source, which forecloses individual analysis
there entirely.

Construct naming is disciplined: we measure a **recording gap**, not concealment. Summarisation is
legitimate; intent is not observable from a document pair. No output of this instrument licenses a
claim that an organization hid something. The dual-use concern — that scoring organizations on what
they leave out could be used to rank or shame — is documented in the appendix rather than left for a
reviewer to discover.

The ethics also explain the research gap. The obvious version of this project, run on internal Slack,
email, and meeting recordings, is ethically fraught and unshareable. That is part of why the
construct has stayed perceptual for 26 years, and the paired-record design is what makes it
approachable without that trade.

**Residual weakness.** Two. First, the SEC substrate produces firm-level measures that could be read
as accusations of concealment by readers who skip the naming discussion; a measure travels further
than its caveats. Second, aggregation-by-default is a policy, and the code will contain the
speaker-level capability that policy restrains — a governance commitment, not a technical guarantee.

## 5. Reproducibility — 4 / 5

**Evidence in the package.**

Apache-2.0 throughout. Open weights only, no API keys, no commercial model on any code path. Every
model pinned by revision SHA, because "we used Qwen3-8B" is not a reproducible statement. Every
corpus ships as a build script with a `(url, accession, sha256, retrieved_at)` manifest and a
`verify` command that fails loudly on mismatch, so a third party can rebuild a byte-identical corpus
and prove it. One substrate (open-source governance) is redistributable in full, and the synthetic
corpus is fully shareable with known ground truth. A CPU-only smoke test runs end to end in CI.

We are also honest about the limit of determinism: batched GPU inference is not bitwise reproducible
across hardware, so we report run-to-run variance on a fixed sample instead of claiming determinism
we cannot deliver.

**Residual weakness.** Real friction remains. Two of the three headline substrates cannot be
redistributed — SEC registrant letters because we will not assert redistribution rights over
third-party documents in a federal record, and ASRS because NASA's terms do not permit it — so
replication requires re-fetching from source, and the ASRS export path is manual and cap-limited. The
`pyannote` diarisation pipelines are gated (free, but requiring an account and accepted conditions).
And our reading of NASA's redistribution position currently rests on a third party's
characterisation, which we have flagged `PARTIAL` and must confirm in writing.

## 6. Scalability — 4 / 5

**Evidence in the package.**

The design scales on three axes. *Documents:* 502,712 verified SEC documents, >1,000,000 ASRS
reports, ~400,000 Wikipedia AfD debates. *Cost:* the expensive teacher pipeline runs once in our lab,
and the distilled student — the thing other people actually run — fits on a single consumer GPU, which
is a deliberate asymmetry rather than an accident. *Substrates:* the loader interface is a small,
documented contract, and any organization publishing both a verbatim and a curated record of the same
event becomes a measurement site, which is a large and growing set (central banks, councils,
legislatures, courts, standards bodies, university senates, boards, every SEC filer).

**Residual weakness.** Scale is uneven across the interesting dimensions. Open-source governance is a
precision substrate with thousands of proposals, not a scale substrate. ASRS de-identification
destroys the firm panel, so no organization-level time series is possible there. And the SEC corpus
is only large in *documents* — the number of independent review *events* per firm is far smaller,
which is what actually binds statistical power for firm-level claims.

## 7. Potential use and adoption — 4 / 5

**Evidence in the package.**

Three distinct audiences, each with a reason to use it that does not depend on the others. *OB and
management scholars* get behavioural measures of silence and voice suppression to replace or validate
survey instruments. *Accounting and finance scholars* get exactly what their own reviews ask for —
Li and Luo (2025) call for precise measurement instruments; Johnston (2025) identifies comment
heterogeneity as the open problem — and our contribution is orthogonal to, not competitive with,
theirs. *Anyone doing LLM-assisted measurement* can use `unsaid-infer` on its own, independent of
this project's substrates, which is the most likely vector for adoption.

Adoption cost is low by construction: one consumer GPU, no API keys, no licence negotiation, and a
loader contract short enough that adding a substrate is a plausible student project.

**Residual weakness.** Two barriers we should not talk past. The calibration requirement is real
friction — `unsaid-infer` refuses to return a point estimate without a gold sample, which means
adopters must do hand-coding they would rather skip, and some will simply use a different tool that
does not ask. And organizational scholars have not historically worked with regulatory filings or
aviation safety reports, so the substrates that make this scope-proof for *Organization Science* are
also unfamiliar territory for the audience that would use it most.

## 8. Potential to expand the research frontier — 5 / 5

**Evidence in the package.**

Daft and Lewin (1990) asked for work that breaks out of the normal-science straitjacket, and March
(1991) framed exploration as the search for new possibilities. Converting a construct from perceptual
to behavioural is that kind of move: it does not add a variable to an existing model, it changes what
counts as observable. Three questions become askable that were not:

1. **Does an audited firm fix the record, or fix the practice?** When the SEC names something a firm
   knew and did not disclose, the firm closes *that* gap. The attention-based view (Ocasio, 1997) and
   the learning-from-failure literature (Tucker & Edmondson, 2003) make opposite predictions about
   everything else — migration versus general improvement. Both predict local improvement, so the
   whole test lives in unaudited topics, which is precisely what was previously unmeasurable.
2. **Whose contributions survive with their name attached?** Attribution stripping makes voice
   suppression an observable organizational *act* rather than an employee's perception of futility
   (Morrison, 2023; Detert & Edmondson, 2011), and open-source governance supplies public,
   timestamped roles, disputes, and exits to test it against.
3. **Does transparency increase or decrease what is knowable?** Chilling and sanitising have opposite
   policy implications and are currently indistinguishable. Paired records on both sides of the FOMC's
   December 2004 minutes-acceleration decision separate them.

The frontier expansion is also infrastructural: the paired-record trick is not specific to silence.
Any construct defined by what is *absent* from an organizational record becomes approachable the same
way.

**Residual weakness.** The expansion is conditional on transportability. The instrument is trained
where paired records exist and is meant to be used where only one record exists, and that is an
empirical claim we have not yet tested. If it fails, the contribution shrinks to a set of descriptive
findings about a handful of unusual organizations that happen to publish twice. We would report that
as a boundary-setting negative result — which this call explicitly invites, and which is genuinely
worth publishing — but it would be a much smaller contribution than the one described above.

---

## Summary: where this package is strong and where it is thin

**Strong.** The construct and the supervision design (criteria 1, 8). The ethics, which are clean by
construction rather than by mitigation (4). The verification work, which measured rather than
inherited its central numbers and corrected two of them (2, 5).

**Thin.** Stage of development, unambiguously (3). There is no prototype yet, and the call asks for
one.

**The single largest risk to the whole design** is not any criterion above; it is the length
confound. If Omission Rate does not survive controls for curated-document length, topic, and speaker
count, the instrument measures compression rather than silence. That test is cheap, it runs first, and
we have committed in advance to reporting it whichever way it comes out. The second largest is
transportability off the paired-record substrates, per criterion 8.

**On the original scope objection.** The rejection risk this revision was built to address — that an
editor reads the FOMC and city councils as political rather than organizational institutions, putting
the work out of scope — is substantially reduced but not eliminated. Firms now lead through the SEC
substrate, workplaces enter through ASRS, and formal hierarchies through open-source governance,
with the FOMC and councils demoted to calibration and multimodal roles. A reviewer could still
reasonably object that the *firm* substrate is a regulatory-correspondence setting rather than an
internal organizational process, and that the *workplace* substrate is curated by a NASA
intermediary rather than by the employing organization. Both objections are fair. Both are stated in
`SUBSTRATES.md` next to the substrates they apply to.
