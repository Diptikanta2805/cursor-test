# `unsaid` — Counting the Silences

**An open instrument for measuring institutional omission and suppressed dissent from paired
organizational records.**

Stage 1 package for the *Organization Science* special issue **"AI-Enabled Frontiers in
Organizational Science"** (Stage 1 deadline 1 November 2026).

---

## The idea in one paragraph

Organizational silence — the collective withholding of information about problems — has been a
central construct in the study of organizational failure since Morrison and Milliken (2000), and for
26 years it has been measured by asking people whether they withheld. You cannot count utterances that
were never recorded. But some organizations publish **two accounts of the same event at two levels of
curation**: a verbatim record and a curated one. Where they do, the difference between the accounts is
the organization's *omission function*, and every pair is a naturally labelled example of it. The
label comes from two documents the organization itself published — not from a model's opinion — which
makes the primary construct supervised. Train open-weight models on those pairs to build three
instruments (Omission Rate, Dissent Suppression Index, Attribution Stripping Rate), then test whether
they port to organizations that publish only one record.

## Where to start

| File | What it is |
|---|---|
| [`proposal/PROPOSAL.md`](proposal/PROPOSAL.md) | **Start here.** The Stage 1 proposal (1,978 words plus references): the unmeasured construct, the paired-record insight, the three instruments, the research questions unlocked, and what would falsify the approach. |
| [`proposal/SUBSTRATES.md`](proposal/SUBSTRATES.md) | The verified substrate inventory. Volume, licensing, redistributability, access mechanics, and an "is this an organization?" assessment for each — plus the six candidates we rejected and why. |
| [`proposal/TECHNICAL_APPENDIX.md`](proposal/TECHNICAL_APPENDIX.md) | Pipeline architecture, the model inventory with licences and gating status, corpus construction per substrate, the measurement-error layer, the validation design, and the compute budget. |
| [`proposal/STAGE1_SCORECARD.md`](proposal/STAGE1_SCORECARD.md) | Honest self-assessment against the eight published Stage 1 criteria, with a residual weakness stated for every one. |
| [`proposal/REFERENCES.md`](proposal/REFERENCES.md) | Every citation with DOI and verification status, plus the model licence audit and the substitutions it forced. |

## The substrates

Three headline substrates, chosen so that the work is unambiguously about organizations:

- **Firms** — SEC filing-review correspondence on EDGAR (`UPLOAD` staff comment letters, `CORRESP`
  registrant responses, and the amended filing). A federal regulator names a *specific disclosure
  omission* in a firm's own official record, and the firm responds on the record. **502,712 documents
  from August 2004 to mid-2026**, a figure we counted ourselves from EDGAR's quarterly form indexes
  rather than inherited.
- **Workplaces** — NASA's Aviation Safety Reporting System, where each of more than a million
  voluntary incident reports carries both the frontline employee's own `Narrative` and a NASA
  analyst's one-or-two-sentence `Synopsis` of the same event.
- **Formal hierarchies** — Python PEPs, Rust RFCs, and Kubernetes KEPs, each with a mandated public
  deliberation thread, a published specification, and a recorded resolution. Dual public-domain/CC0 or
  MIT/Apache-2.0, and the one corpus we can redistribute in full.

Retained as calibration and multimodal sites: the **FOMC** (verbatim transcripts at a ~5-year lag
versus minutes within weeks, plus the December 2004 minutes-acceleration decision as a transparency
shock) and the **Council Data Project** (video, audio, transcript, minutes, and roll-call votes for
the same municipal meeting). **Wikipedia AfD** debates supply scale for power analysis.

## Current state of the work

**This repository currently contains the developed idea and the verified data foundation. It does not
contain the pipeline.**

Done and checked against primary sources (August 2026): verification of six substrates, plus six
further candidates examined and documented — four rejected outright (earnings-call transcripts, NLRB
hearing transcripts, labour arbitration awards, hospital morbidity-and-mortality review), one
reclassified as a downstream outcome rather than a substrate (10-K risk factors), and one deferred
(faculty senate minutes); a complete sweep of EDGAR's 2004–2026 quarterly form indexes; a
working decoder for the uuencoded PDFs the SEC wraps staff letters in, with clean text extraction on
sampled letters; confirmation that modern staff letters carry a machine-readable pointer to the filing
under review; resolution of the Hansen et al. (2018) replication package and its CC0 licence; and
existence, licence, and gating checks on all 17 open-weight models the design names.

Not built yet: the pipeline itself (segmentation, alignment, distillation), the `unsaid-infer`
measurement-error layer, the gold-coding protocol, and the synthetic corpus. These are specified in
the technical appendix. There is **no placeholder or stub code in this repository** — an empty
scaffold would misrepresent the state of the work. The Stage 1 scorecard marks itself down
accordingly (2 / 5 on stage of development).

## Constraints we hold to

- **Open weights only.** No API keys, no commercial models on any code path. Everything the design
  names is Apache-2.0, MIT, or CC-BY-4.0 on the Hugging Face Hub. Gemma was dropped for its custom,
  non-OSI licence; one NVIDIA diarisation checkpoint was dropped for a non-commercial clause.
- **We redistribute only what we clearly may.** SEC registrant letters and ASRS narratives ship as
  build scripts with per-document SHA-256 checksums, never as bulk text.
- **Public records only.** No human subjects, no private workplace communication. Released measures
  aggregate to the event or organization level.
- **A recording gap is not concealment.** Summarisation is legitimate; intent is not observable from a
  document pair.
- **Measurement error is not optional.** The inference layer refuses to return a point estimate
  without a gold calibration sample.

## Honest caveats

The single largest risk is the **length confound**: if Omission Rate does not survive controls for
curated-document length, topic, and speaker count, the instrument measures compression rather than
silence. The second is **transportability** — the instrument is trained where paired records exist and
meant to be used where only one exists, and that is an empirical claim, not an assumption. Two
licensing questions are still open and flagged `PARTIAL`: NASA's redistribution position in writing,
and the content licence for `discuss.python.org` and the `python-dev` archives.

Nothing here should be read as a claim that this submission will be accepted.

Licence for this repository's content: Apache-2.0 (intended for the code and corpora to follow).
