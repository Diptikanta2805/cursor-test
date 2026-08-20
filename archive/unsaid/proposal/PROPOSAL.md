# Counting the Silences

## An Open Instrument for Measuring Institutional Omission and Suppressed Dissent from Paired Organizational Records

**Stage 1 proposal — *Organization Science*, "AI-Enabled Frontiers in Organizational Science"**
Repository: `unsaid`. Licence: Apache-2.0. Models: open-weight only. No API keys anywhere.

---

### An organization is, in large part, its record

What an organization writes down becomes its memory, its accountability surface, and the input to
its next decision. March (1991) modelled organizational learning as mutual adaptation between
individuals and an *organizational code* — a stored representation of what the organization believes.
Ocasio (1997) made the firm's behaviour a function of how its rules, resources, and relationships
channel attention onto some issues and away from others. In both accounts, the thing that enters the
record is the thing that survives to shape action. Everything said and not recorded is, for
organizational purposes, gone.

Morrison and Milliken (2000) named the systematic version of this loss. Organizational silence is
the *collective withholding* of information about problems: not one person's reticence, but a
shared, structurally produced pattern of not saying, and of what is said not counting. It is one of
the most-cited constructs in the study of organizational failure, and Morrison's (2023) decade-later
review documents hundreds of studies built on it.

Twenty-six years on, the construct is still measured by asking people whether they withheld.
Morrison's (2023) review notes that its 2014 predecessor found only two papers measuring silence
empirically at all, and concedes why: silence "by its very nature is not observable." Recent work
shows self-reported silence scores are uninterpretable without knowing whether the employee had
anything to withhold (Dilba & Meyer, 2025). Our field's central account of why organizations fail to
learn from what their members already know rests on a self-report about an absence.

### Why the absence has been unmeasurable

You cannot count utterances that were never recorded. Measuring an absence requires a counterfactual
for what could have been recorded, and the record does not contain it. This is not a limitation of
survey methods specifically; it defeats every text-as-data method in the field. Dictionary and
embedding measures (Li, Mai, Shen & Yan, 2021) operate on surviving text and are structurally
incapable of scoring what is not there. LLM annotation as currently practised (Gilardi, Alizadeh &
Kubli, 2023) scores documents, not document *pairs*, and its guidance literature is explicit that
prompt variation alone shifts labels and downstream regression conclusions (Carlson & Burbano, 2026).
Asking a language model whether something is missing from a document produces exactly the kind of
unfalsifiable model opinion that should not become a dependent variable.

The closest published precedent shows how the ceiling has bound. Hansen, McMahon and Prat (2018) used
the FOMC's 1993 transparency shock and computational linguistics to identify a discipline effect and
a conformity effect in central-bank deliberation. Their dependent variable was **what was said**.
Nobody has measured the gap between what was said and what was **recorded**, because until now
nothing supplied the label.

### The paired-record insight

Some organizations publish two accounts of the same event at two levels of curation. Where they do,
the difference between the accounts is the organization's *omission function*, and every pair is a
naturally labelled training example of it. The label is not a researcher's inference or a model's
judgement. It is derived from two documents the organization itself put on the record.

We have verified three substrates that are unambiguously organizational, and retained two more as
calibration sites (`SUBSTRATES.md` gives volumes, licences, access mechanics, and the substrates we
rejected).

**Firms.** The SEC's Division of Corporation Finance reviews registrant filings and publishes the
resulting correspondence on EDGAR — staff comment letters as form type `UPLOAD`, registrant responses
as `CORRESP` — no sooner than twenty business days after the review closes. Frequently the staff
names a *specific disclosure omission* in a firm's own official record, and the firm then amends the
filing or commits to future disclosure. That is an externally adjudicated omission label attached to
a firm's official record, with the firm's own account of why alongside it. In one 2024 letter the
staff observe that a firm described a disposition strategy on its earnings call that its 10-K does
not disclose, and ask what consideration it gave to reporting the trend. Counting directly from
EDGAR's quarterly form indexes, this substrate contains **502,712 documents from August 2004 to
mid-2026** — a figure we measured rather than repeated. Every modern staff letter carries a
machine-readable pointer to the filing under review.

**Workplaces.** NASA's Aviation Safety Reporting System publishes, for each of more than a million
voluntarily submitted incident reports, both the frontline employee's own Narrative and a NASA
analyst's one- or two-sentence Synopsis of the same event. That is a verbatim-versus-curated pair
for a workplace failure, reported by pilots, controllers, mechanics, and dispatchers inside
employment relationships — the exact setting of the literature on why organizations do not learn
from failure (Tucker & Edmondson, 2003) and on psychological safety (Edmondson, 1999).

**Formal hierarchies with public deliberation.** Python's PEP process, Rust's RFC process, and
Kubernetes' KEP process each mandate a public deliberation thread, a final published specification,
and a recorded resolution. These are organizations with delegated decision authority, codified
process documents, role transitions, and escalating disputes, and their content is dual public-domain
and CC0, or MIT/Apache-2.0. This is the one corpus we can redistribute in full.

**Calibration sites.** The FOMC releases lightly edited verbatim transcripts about five years after
each meeting alongside minutes released within weeks, and its December 2004 decision to accelerate
minutes release was taken over recorded worries that early release would produce "less
comprehensive, and therefore less useful, minutes" — a stated mechanism with a sharp date and paired
records on both sides. The Council Data Project (Brown et al., 2021) supplies municipal meetings with video, audio,
transcript, minutes, and roll-call votes for the same event, and is the only substrate that exercises
an audio front end.

### What exists now, and what the Stage 1 artifact will contain

**Now.** The substrate work is done and is itself the load-bearing result: full verification of
access mechanics, licensing, and volume for each substrate, including a complete sweep of EDGAR's
2004–2026 form indexes, a working decoder for the uuencoded PDF wrapper the SEC uses for staff
letters, confirmation that staff letters carry a direct pointer to the reviewed filing, and clean
text extraction from sampled letters. We also know the constraints: registrant response letters are
third-party documents we will not redistribute in bulk, ASRS forbids redistribution, and earnings-call
transcripts are proprietary and therefore excluded outright.

**By November 1.** A three-layer repository. `unsaid-corpora` ships build scripts and per-document
checksums for each substrate — never redistributed bulk text where licensing is unsettled — plus a
fully redistributable synthetic corpus of deliberations with *planted* omissions of known type and
rate, for power analysis and adversarial testing. `unsaid-core` segments the verbatim record into
propositions with speaker attribution, aligns them against the curated record by embedding retrieval
followed by an entailment pass, and labels each proposition `represented`, `compressed`,
`attribution-stripped`, or `omitted`; the expensive pipeline's labels then distil into a small
fine-tuned scorer that another researcher can run on one consumer GPU. `unsaid-infer` makes
measurement error the default rather than a robustness appendix: it wraps design-based supervised
learning (Egami, Hinck, Stewart & Wei, 2023) and prediction-powered inference (Angelopoulos, Bates,
Fannjiang, Jordan & Zrnic, 2023), and refuses to return a point estimate without a gold calibration
sample of known sampling probability. Egami et al. show that plugging surrogate labels straight into
a downstream regression produces substantial bias and invalid intervals even at 80–90% surrogate
accuracy; a measurement instrument that lets you do that quietly is a liability.

Three instruments come out: **Omission Rate** (share of propositions not surviving, always
conditional on topic, speaker count, and curated-document length), **Dissent Suppression Index**
(Omission Rate restricted to disagreement-bearing propositions), and **Attribution Stripping Rate**
(the proposition survives but its speaker is de-identified or collectivised — newly named, and
newly measurable).

### Three questions that could not previously be asked

**Does an audited firm fix the record, or fix the practice?** When the SEC names something a firm
knew and did not disclose, the firm demonstrably closes that gap (Johnston & Petacchi, 2017). But the attention-based view
(Ocasio, 1997) and the learning-from-failure literature (Tucker & Edmondson, 2003) make opposite
predictions about everything else. Attention re-allocation implies omission *migrates* to unaudited
topics; learning implies it falls generally. Both predict local improvement, so the test lies
entirely in unaudited topics — previously unmeasurable, now the instrument's native output. This also
speaks directly to Bozanic, Dietrich and Johnson's (2017) finding that firms strategically resist
requested disclosure through confidential-treatment requests and negotiation.

**Whose contributions survive with their name attached?** Voice research measures individuals'
beliefs that speaking up is futile (Morrison, 2023). Attribution stripping measures the
organization's observable *act* of de-attributing what was said, which makes voice suppression a
property of the organization rather than a perception of the person. Is survival-with-attribution
predicted by formal position, tenure, and prior dissent — and does high stripping at *t* predict
exit at *t+k*? Open-source governance answers this cleanly, because roles, disputes, and departures
are all public and timestamped.

**Does transparency increase or decrease what is knowable?** Hansen et al. (2018) showed transparency
changes what is said. A transparency shock can also make the record thinner. Chilling and sanitising
have opposite implications for transparency policy and are currently indistinguishable; paired
records on both sides of the FOMC's December 2004 change, and of venue shifts in open-source
governance, separate them.

### What would falsify this

The design's central claim is that the primary construct is *supervised*, so the primary risk is that
the label is not what we say it is. Four ways we could be wrong, each with a pre-specified test.

*Omission is length.* If Omission Rate does not survive controls for curated-document length, topic,
and speaker count, the instrument measures compression, not silence. This is the first test we run,
and it is the one most likely to fail on ASRS, where brevity is mandated.

*Alignment does not work.* If proposition-level alignment F1 against a hand-adjudicated sample is
poor, everything downstream is noise. We report human–human reliability first, because it bounds
achievable agreement.

*Selection is fatal.* The SEC reviews neither randomly nor uniformly, and reviews less than it did in
2010. If instrument performance collapses off the reviewed sample, the firm-level claims do not
transport, and we will say so rather than assume otherwise.

*It is instrument variance.* Given that documented prompt and model choices shift annotations
substantially in comparable management tasks (Carlson & Burbano, 2026), we measure the disagreement
label and the omission label with different model families and publish the full variance
decomposition. If cross-family agreement is low, that is the finding.

Two ethical commitments constrain the artifact rather than excusing it. All primary data are public
records, so there are no human subjects and no scraping of private workplace communication — the
obvious version of this project, run on internal Slack and email, is ethically fraught and
unshareable, which is part of why nobody has built it. And because this is a transparency-auditing
instrument that could be pointed at individuals, released outputs aggregate to the
event-or-organization level by default. We also hold a hard line on naming: a *recording gap* is not
concealment. Summarisation is legitimate; intent is not observable.

### What changes if this works

A construct that has been perceptual for twenty-six years becomes behavioural, at scale, in firms.
Organizational silence stops being something we ask people about and becomes something we count in
the record the organization itself produced. Voice suppression becomes an observable organizational
act rather than an employee's belief. Transparency policy becomes an empirically decomposable
question instead of a debate between two mechanisms nobody can separate. And any organization that
publishes both a verbatim and a summary record of the same event — central banks, councils,
legislatures, courts, standards bodies, university senates, boards, and every firm that files with
the SEC — becomes a measurement site.

If it does not work, the failure is informative and cheap to publish: either omission is mostly
length, or the paired-record label does not transport off the substrates that produce it. Both are
boundary-setting results about the limits of AI-enabled measurement in organizational research, which
this call explicitly invites.

---

## References

Angelopoulos, A. N., Bates, S., Fannjiang, C., Jordan, M. I., & Zrnic, T. (2023). Prediction-powered
inference. *Science*, 382(6671), 669–674. https://doi.org/10.1126/science.adi6000

Bozanic, Z., Dietrich, J. R., & Johnson, B. A. (2017). SEC comment letters and firm disclosure.
*Journal of Accounting and Public Policy*, 36(5), 337–357.

Brown, E. M., Huynh, T., Na, I., Ledbetter, B., Ticehurst, H., Liu, S., Gilles, E., Greene, K. M. F.,
Cho, S., Ragoler, S., & Weber, N. (2021). Council Data Project: Software for municipal data
collection, analysis, and publication. *Journal of Open Source Software*, 6(68), 3904.
https://doi.org/10.21105/joss.03904

Carlson, N. A., & Burbano, V. (2026). The use of LLMs to annotate data in management research:
Foundational guidelines and warnings. *Strategic Management Journal*, 47(3), 699–725.
https://doi.org/10.1002/smj.70023

Dilba, D., & Meyer, B. (2025). Uneventful days? A cautionary tale about the underestimated role of
triggering events in employee silence research. *Journal of Occupational and Organizational
Psychology*, 98(1). https://doi.org/10.1111/joop.12549

Edmondson, A. C. (1999). Psychological safety and learning behavior in work teams. *Administrative
Science Quarterly*, 44(2), 350–383. https://doi.org/10.2307/2666999

Egami, N., Hinck, M., Stewart, B. M., & Wei, H. (2023). Using imperfect surrogates for downstream
inference: Design-based supervised learning for social science applications of large language models.
*Advances in Neural Information Processing Systems*, 36, 68589–68601. https://arxiv.org/abs/2306.04746

Gilardi, F., Alizadeh, M., & Kubli, M. (2023). ChatGPT outperforms crowd workers for text-annotation
tasks. *Proceedings of the National Academy of Sciences*, 120(30), e2305016120.
https://doi.org/10.1073/pnas.2305016120

Hansen, S., McMahon, M., & Prat, A. (2018). Transparency and deliberation within the FOMC: A
computational linguistics approach. *The Quarterly Journal of Economics*, 133(2), 801–870.
https://doi.org/10.1093/qje/qjx045

Johnston, R., & Petacchi, R. (2017). Regulatory oversight of financial reporting: Securities and
Exchange Commission comment letters. *Contemporary Accounting Research*, 34(2), 1128–1155.
https://doi.org/10.1111/1911-3846.12297

Li, K., Mai, F., Shen, R., & Yan, X. (2021). Measuring corporate culture using machine learning.
*The Review of Financial Studies*, 34(7), 3265–3315. https://doi.org/10.1093/rfs/hhaa079

March, J. G. (1991). Exploration and exploitation in organizational learning. *Organization Science*,
2(1), 71–87. https://doi.org/10.1287/orsc.2.1.71

Morrison, E. W. (2023). Employee voice and silence: Taking stock a decade later. *Annual Review of
Organizational Psychology and Organizational Behavior*, 10, 79–107.
https://doi.org/10.1146/annurev-orgpsych-120920-054654

Morrison, E. W., & Milliken, F. J. (2000). Organizational silence: A barrier to change and
development in a pluralistic world. *Academy of Management Review*, 25(4), 706–725.
https://doi.org/10.5465/amr.2000.3707697

Ocasio, W. (1997). Towards an attention-based view of the firm. *Strategic Management Journal*,
18(S1), 187–206. https://doi.org/10.1002/(SICI)1097-0266(199707)18:1+<187::AID-SMJ936>3.0.CO;2-K

Tucker, A. L., & Edmondson, A. C. (2003). Why hospitals don't learn from failures: Organizational and
psychological dynamics that inhibit system change. *California Management Review*, 45(2), 55–72.
https://doi.org/10.2307/41166165

U.S. Securities and Exchange Commission. (2026). *How to search for EDGAR correspondence*.
https://www.sec.gov/search-filings/edgar-search-assistance/how-search-edgar-correspondence

Full verification status for every citation, including items marked `[PARTIAL]` or `[PREPRINT]`, is
in `REFERENCES.md`. Substrate-specific sources are in `SUBSTRATES.md`.
