# Paired-Record Substrate Inventory

**Project:** `unsaid` — measuring institutional omission and suppressed dissent from paired
deliberative records.
**Prepared:** August 2026, for the *Organization Science* "AI-Enabled Frontiers" Stage 1 package.

A **paired record** is two documents, published by the same organization (or by a body with formal
authority over it), that describe *the same event* at *two different levels of curation*. The more
verbatim document supplies the population of things that were said; the more curated document
supplies the subset the organization chose to preserve. The difference between them is the
organization's **omission function**, and every pair is a naturally labelled training example of it.

This file records what we verified, what we rejected, and why. Everything below was checked against
a primary source in August 2026; where a figure comes from our own measurement rather than a
published source, we say so and show the method.

---

## 0. Summary and ranking

| Rank | Substrate | Pairing | Volume (verified) | Redistributable? | "Is this an organization?" |
|---|---|---|---|---|---|
| **1** | **SEC filing-review correspondence** (`UPLOAD` / `CORRESP` + amended filing) | Regulator names an omission in a firm's official record → firm's response and amendment | **502,712 documents**, 2004-08 to 2026-07 (our count) | Partially — see §1.4 | **Firms.** Unambiguous. |
| **2** | **NASA ASRS** (reporter Narrative vs. analyst Synopsis) | Frontline employee's own account → one- or two-sentence official synopsis | >1,000,000 reports submitted; database online 1988–present | **No** — build script only | **Workplaces.** Pilots, controllers, mechanics, dispatchers in employment relationships. |
| **3** | **Open-source governance** (Python PEPs, Rust RFCs, Kubernetes KEPs) | Full public deliberation thread → final published specification + `Resolution` | Thousands of proposals; complete threads | **Yes** — CC0 / MIT / Apache-2.0 | **Formal hierarchies.** Steering Council, PEP-Delegate, SIG leads, core teams. |
| 4 | **FOMC** (verbatim transcript vs. minutes) | Same meeting, two records, ~5-year lag | ~200 meetings, 1994– | Public domain (US Gov) | Committee of a formal organization; a management scholar may object. |
| 5 | **Council Data Project** (transcript/audio/video vs. minutes) | Same meeting, multimodal | 350+ meetings seed corpus, horizontally extensible | Yes (open pipeline) | Organizations by structure; not firms. |
| 6 | **Wikipedia Articles for Deletion** (debate vs. closing rationale) | Deliberation → admin's recorded outcome | ~400,000 debates, 2005–2018 | **Yes** — CC BY-SA | Peer-production organization; contested. |
| — | Earnings-call transcripts | Prepared remarks vs. Q&A | large | **No** (proprietary) | Rejected: §7.1 |
| — | 10-K risk factors added later | not same-event | large | Public domain | Reclassified as an *outcome variable*: §7.2 |
| — | NLRB hearing transcript vs. ALJ decision | genuine pairing | large | Transcripts not published | Rejected: §7.3 |
| — | Arbitration awards, union grievances | occasional | small | Mostly confidential/paywalled | Rejected: §7.4 |
| — | Hospital morbidity-and-mortality review | ideal pairing | n/a | Not public | Rejected: §7.5 |
| — | University faculty senate minutes vs. recordings | genuine pairing | institution-by-institution | Mixed | Deferred: §7.6 |

**Headline choice for Stage 1: substrates 1, 2, and 3, with 4 and 5 retained as calibration and
multimodal sites and 6 as the power-analysis corpus.** Substrate 1 answers the "is this an
organization?" objection outright; substrate 2 puts the instrument inside employment relationships;
substrate 3 is the one corpus we can redistribute in full, which is what makes the artifact
reproducible without asking anyone to trust our scraper.

---

## 1. SEC filing-review correspondence — `UPLOAD`, `CORRESP`, and the amendment

### 1.1 What the pairing is

The SEC's Division of Corporation Finance selectively reviews registrant filings. When staff believe
a filing can be materially improved, they issue a comment letter; the registrant responds and, if
appropriate, amends the filing or commits to different disclosure going forward. To increase
transparency of the review process, the Division makes all of this correspondence public on EDGAR
**no sooner than 20 business days** after it completes review of a periodic or current report or
declares a registration statement effective (SEC, *Filing Review Process*; SEC, *How to Search for
EDGAR Correspondence*, reviewed May 2026).

The pairing is unusual and, for our purposes, better than a transcript-versus-minutes pair. It is a
**three-part record**:

1. the firm's official record as originally filed (the 10-K, 10-Q, S-1);
2. an *externally adjudicated omission label* — the staff letter naming something the firm should
   have disclosed and did not (`UPLOAD`);
3. the firm's own account of why, plus the corrected record (`CORRESP`, and the amendment).

The omission label is therefore not a model's opinion and not even the researcher's reading of two
documents. It is a determination by a federal regulator with authority over the record, recorded in
the same public archive as the record itself.

### 1.2 Verified example

We decoded two randomly drawn 2024 `UPLOAD` letters. The first is a near-perfect instance of the
construct — the SEC observes that a firm said something *on its own earnings call* that does not
appear in its 10-K:

> "We note from your most recent earnings call that the pace of dispositions has remained robust and
> that you have almost $750 million of real estate currently either under LOI or in contract
> negotiation. While the disclosure in your Form 10-K notes that you have engaged in significant
> disposition activity in recent periods, it is not clear from your disclosure whether you are
> following a broader strategy to dispose of certain assets… Please tell us what consideration you
> have given to discussing known trends or uncertainties…"
> — SEC staff letter to SITE Centers Corp., April 16, 2024
> (`edgar/data/894315/0000000000-24-004121.txt`; reviewed filing `0000950170-24-019352`)

The second shows the multi-round thread structure and uses the word "omission" directly, in a letter
that reissues a prior comment after an unsatisfactory response:

> "…the accommodations under Item 1303(a)(3) and 1304(a)(2) of Regulation S-K for royalty and
> streaming companies permit the omission of information, including mineral resources and mineral
> reserves, however the accommodations do not permit the substitution of mineral resources and
> mineral reserve prepared under other mineral reporting regimes. Please revise…"
> — SEC staff letter to Royal Gold, Inc., May 22, 2024
> (`edgar/data/85535/0000000000-24-005929.txt`; reviewed filing `0001558370-24-001192`)

### 1.3 Volume — our own measurement

The prior ideation memo and the project brief cited "approximately 600,000 documents." We counted
directly rather than repeating the figure. Method: fetch every quarterly `form.idx` from
`https://www.sec.gov/Archives/edgar/full-index/{year}/{QTR}/form.idx` for 2004–2026 and count exact
matches on the form-type field.

```
2004  UPLOAD=  641  CORRESP=  917      2016  UPLOAD=10450  CORRESP=12882
2005  UPLOAD= 8844  CORRESP= 8923      2017  UPLOAD= 9828  CORRESP=13157
2006  UPLOAD=13289  CORRESP=11777      2018  UPLOAD= 7702  CORRESP=10608
2007  UPLOAD=12302  CORRESP=11582      2019  UPLOAD= 6593  CORRESP= 8902
2008  UPLOAD=13097  CORRESP=10573      2020  UPLOAD= 7380  CORRESP=10833
2009  UPLOAD=15325  CORRESP=15090      2021  UPLOAD= 9337  CORRESP=13614
2010  UPLOAD=17108  CORRESP=17965      2022  UPLOAD= 8521  CORRESP=10854
2011  UPLOAD=17938  CORRESP=17251      2023  UPLOAD= 8210  CORRESP=10323
2012  UPLOAD=15441  CORRESP=15934      2024  UPLOAD= 8532  CORRESP=11349
2013  UPLOAD=16930  CORRESP=16135      2025  UPLOAD= 4964  CORRESP= 8336
2014  UPLOAD=12119  CORRESP=12931      2026  UPLOAD=  939  CORRESP= 1548  (partial)
2015  UPLOAD=13604  CORRESP=12134
                                       TOTAL UPLOAD=239,094  CORRESP=263,618  SUM=502,712
```

So: **roughly half a million documents, not six hundred thousand.** 2004 is short because coverage
starts August 1, 2004; 2026 is short because the year is incomplete and because the 20-business-day
release lag means the most recent reviews are not yet public. The 2010→2019 decline in `UPLOAD`
volume is real and is itself a documented feature of the setting worth studying (Johnston, 2025,
notes the "dramatic decline in 10-K/10-Q Comment Letter cases (2010–2021)" as an open research
question).

### 1.4 Access mechanics — verified, including the parts that are annoying

- **Rate limit.** The SEC caps automated access at **10 requests per second per requester**,
  "regardless of the number of machines used to submit requests," in force since July 27, 2021, and
  requires a descriptive `User-Agent` header giving a name and contact email. Exceeding the limit
  returns HTTP 403 and a short IP block. There is no API key and no paid tier that lifts the cap
  (SEC, *Accessing EDGAR Data*; SEC, *New rate control limits*, July 2021). Our own build scripts
  target 8 req/s with exponential backoff, and we log every request.
- **Thread reconstruction is easier than the literature implies.** Every one of the eight 2024
  `UPLOAD` submissions we sampled carries a `PUBLIC REFERENCE ACCESSION NUMBER` header giving the
  accession number of the *filing under review*. That is a direct machine-readable edge from letter
  to reviewed filing; no file-number heuristic is needed for the modern period. File-number matching
  (which the `edgartools` library implements) remains the fallback for older submissions and for
  linking rounds of a thread to each other.
- **Format asymmetry, and it costs us.** `UPLOAD` letters are shipped as **uuencoded PDFs** inside
  the `.txt` submission wrapper, so a PDF text-extraction step is mandatory. On our 2/2 sample,
  `pypdf` extracted clean, well-ordered text. `CORRESP` submissions are **HTML**, occasionally with
  attached images. So the staff side needs OCR-free PDF extraction and the registrant side needs
  ordinary HTML parsing. Extraction quality must be measured and reported, not assumed.
- **Amendment diffing.** Johnston & Petacchi (2017) report that more than 17% of comment-letter
  cases produce an immediate amended filing, and that financial statements and footnotes are
  frequently revised. Amendments are ordinary EDGAR filings (`10-K/A`, `S-1/A`), so the original and
  the amendment can be aligned section-by-section and the *added* disclosure localised. This makes
  the target of the staff's comment recoverable as text, not just as a binary flag.

### 1.5 Licensing and redistributability — the honest answer

Documents authored by SEC staff (`UPLOAD`) are works of the United States government and are not
subject to domestic copyright. Registrant response letters (`CORRESP`) are third-party documents
filed into a public federal record; they are freely and lawfully *readable and analysable* by anyone,
and the SEC imposes no licence terms, but their copyright status as redistributable bulk text is not
something we are willing to assert. **Our conservative choice: we redistribute no bulk EDGAR text.**
The corpus ships as a build script plus per-document SHA-256 checksums and accession numbers, so any
reader can regenerate a byte-identical corpus, and provenance is exact. We do redistribute derived,
non-substitutive artifacts: proposition-level labels, alignment indices, and aggregate measures.

### 1.6 Prior literature — so we cite correctly and claim narrowly

Accounting and finance have used comment letters for over a decade. What that literature establishes,
and what it leaves open, matters for our novelty claim.

- **Cassell, Dreher & Myers (2013)**, *The Accounting Review* 88(6), 1875–1908 — the foundational
  study of 10-K comment letters and the cost of remediation. **[PARTIAL: pages from a citing
  record, not read off the publisher page.]**
- **Johnston & Petacchi (2017)**, *Contemporary Accounting Research* 34(2), 1128–1155 — content,
  resolution, and consequences; nearly half of comments involve accounting application, financial
  reporting, and disclosure; >17% of cases produce immediate amendments; bid-ask adverse selection
  falls and earnings response coefficients rise after resolution.
- **Bozanic, Dietrich & Johnson (2017)**, *Journal of Accounting and Public Policy* 36(5), 337–357 —
  firms enhance disclosure in response, but Rule 406 confidential-treatment requests and negotiation
  attenuate the effect; high-tech and high-R&D firms are likelier to request confidential treatment.
  This is the closest existing work to our construct, and it is important that we cite it as such:
  it establishes that firms *strategically resist* the disclosure the staff asks for.
- **Cassell, Cunningham & Lisic (2019)**, *Review of Accounting Studies* 24(4), 1252–1276 — the
  readability of company *responses* predicts review outcomes.
- **Li & Luo (2025)**, *Accounting Perspectives* 24, 735–786 — a full review of determinants and
  consequences, which closes by calling for "precise measurement instruments to better understand
  the effects of different types of SEC reviews."
- **Johnston (2025)**, SSRN 4587987, "SEC Comment Letter Research — *Quo Vadis*?" — a critical review
  arguing the literature suffers from "heterogeneity in the significance of letters and comments"
  and that significant outcomes from 10-K/10-Q letters are infrequent. **[PREPRINT]**

**What is new here.** This literature treats the comment letter as a *treatment* (a firm was
reviewed; what happened to its disclosure, cost of capital, insider trading, audit fees?). Nobody
treats it as a *label* for training a general-purpose omission detector that can then be applied to
the ~99% of filings that were never reviewed. The two reviews above name exactly this gap —
heterogeneity in comment significance, and the absence of precise measurement instruments — from
inside accounting. Our contribution is orthogonal to theirs and useful to them.

### 1.7 Weaknesses we must state

- **Selection.** The SEC does not review randomly, and it reviews less than it used to. An
  instrument trained on reviewed filings inherits the staff's attention. Mitigation: model the
  selection explicitly, report performance separately by review-selection propensity, and treat
  transportability to unreviewed filings as an empirical claim to be tested, not assumed.
- **The label is "the regulator thought this was missing," not "the firm knew and withheld."**
  Intent is not observable. We name the construct accordingly (see §8).
- **Confidential treatment.** Bozanic et al. (2017) show firms can and do withhold under Rule 406.
  Those withholdings are, by construction, invisible to us. We under-count.
- **PDF extraction error propagates.** It must be measured against a hand-transcribed sample.

---

## 2. NASA Aviation Safety Reporting System (ASRS)

### 2.1 The pairing

ASRS collects voluntary, confidential safety reports from frontline aviation personnel — pilots,
controllers, mechanics, flight attendants, dispatchers. Two text fields exist for the same event:

- the **Narrative**, "the de-identified and detailed event description provided by the reporter";
- the **Synopsis**, "written by an ASRS Aviation Expert Analyst — a brief 1 or 2 sentence summary of
  the event" (NASA ASRS, *Search Strategies*).

That is a verbatim-versus-curated pair for a single workplace incident, produced inside a formal
reporting system, in an employment context. It is the closest thing in the public domain to the
paired record an organizational scholar actually wants.

### 2.2 Volume, access, licensing

- More than **1,000,000 reports** have been submitted; the online database covers **1988 to the
  present** and is updated monthly (NASA ASRS, *About ASRS Data*).
- Access is via the ASRS Database Online query interface, with export to `.doc`, `.xls`, `.csv`,
  **capped at 10,000 records per download**, so large pulls must be split into date windows. A
  published reproduction package for a four-decade ASRS study documents exactly this workflow
  (splitting 1988–2026 into eight windows).
- **Redistribution is not permitted.** The same reproduction package states plainly: "The ASRS
  reports are public but must be exported by the user; NASA's terms do not permit redistribution of
  the database here." We therefore ship an export recipe and checksums, never the corpus.
  **[PARTIAL: we are relying on a third-party repository's characterisation of NASA's terms; before
  submission we will get this in writing from the ASRS office and quote it directly.]**

### 2.3 Why this substrate is worth its costs

It is the only substrate on this list where the utterance being curated is a **worker's account of a
failure**, which is the exact setting of the organizational-learning-from-failure literature (Tucker
& Edmondson, 2003) and of psychological safety (Edmondson, 1999). It also gives us a validation
target no other substrate does: ASRS assigns structured `Detector`, `When Detected`, and `Result`
codes, so a claim that our instrument detects "suppressed problem-reporting" can be checked against
independently coded outcome fields.

### 2.4 Weaknesses we must state

- **The curator is an intermediary, not the employer.** The Synopsis is written by a NASA analyst,
  not by the airline. So ASRS measures the curation function of a *safety reporting system*, not of
  the employing organization. That is a genuinely different quantity and we will not blur them.
- **De-identification destroys the firm panel.** "All personal and organizational names are removed.
  Dates, times, and related information… are either generalized or eliminated." So no firm-level or
  individual-level panel is possible. Analysis is pooled or stratified by role and operation type.
- **The Synopsis is a summary by design and by mandate.** Length compression is the point. The
  discriminant test that omission is not merely length has to work hardest here.
- **Self-selection into reporting.** ASRS states it does not verify or validate reports.

---

## 3. Open-source software governance — PEPs, RFCs, KEPs

### 3.1 The pairing

Formal proposal processes in large open-source organizations mandate a public deliberation thread
and a separately published final artifact. Python's PEP 1 requires that a discussion thread be
created and linked in the `Discussions-To` header, that the thread be "publicly available on the web
so that all interested parties can participate," that a new thread and a new `Post-History` entry be
created if the proposal is substantially rewritten, and that on acceptance, rejection, or withdrawal
a **`Resolution`** header be added linking to the decision post. Rust RFCs and Kubernetes KEPs follow
the same shape via pull-request review threads and merged specification text.

So for each proposal we have: the verbatim, timestamped, speaker-attributed deliberation; the final
specification, which is a curated statement of what the organization decided; and an explicit
resolution artifact. Objections raised in the thread either appear in the final document (often as a
"Rejected ideas" or "Backwards compatibility" section) or vanish from the organization's memory.

### 3.2 Why these are organizations, not just repositories

Because they have the structural features a management scholar looks for: a formal decision
hierarchy (Python Steering Council, PEP-Delegate, PEP editors; Rust teams; Kubernetes SIG leads and
approvers), delegated authority, codified process documents that are themselves revised through the
process, role transitions and exits that are publicly timestamped, and disputes that escalate.
PEP 1's own revision history — including a Steering Council review issue over how PEP announcement
and resolution should work — is a visible instance of an organization arguing about its own
governance in public.

### 3.3 Licensing — this is the redistributable substrate

- **Python PEPs:** "Each new PEP must be placed under a dual license of public domain and
  CC0-1.0-Universal" (PEP 1, §Copyright/license).
- **Rust RFCs:** the `rust-lang/rfcs` repository is dual-licensed Apache-2.0 / MIT at the user's
  option, formalised by RFC 2044.
- **Kubernetes enhancements:** Apache-2.0.
- Discussion venues differ: GitHub PR threads for Rust and Kubernetes travel with the repository
  licence for content contributed to it, while `discuss.python.org` posts are governed by the forum's
  own terms. **[PARTIAL: we have not yet confirmed the Discourse content licence for
  discuss.python.org, and older PEP discussion lives in python-dev mailing-list archives whose terms
  we also have not confirmed. Before submission we will resolve this and, if it does not clear, we
  will restrict the redistributed thread corpus to Rust and Kubernetes and ship Python threads as a
  fetch script.]**

### 3.4 Weaknesses we must state

- Volume is thousands of proposals, not hundreds of thousands. This is a precision substrate, not a
  scale substrate.
- Deliberation is asynchronous and written, so "what was said" is already a written artifact. That
  removes transcription error but also removes the spoken-versus-written distinction that makes FOMC
  and council data interesting.
- Selection: proposals that die quietly may never get a final document to align against. Withdrawn
  and rejected proposals must be kept in the sample, not dropped, or we condition on the outcome.

---

## 4. FOMC (retained: calibration and natural experiment)

Verbatim transcripts, produced from meeting audio beginning with 1994 meetings, are released with
roughly a five-year lag; minutes in their present form date from February 1993. In December 2004 the
Committee voted to accelerate minutes release to three weeks after the policy decision, and the
minutes of that very meeting record participants worrying that early release "would lead to either
less productive discussions at the meetings or to less comprehensive, and therefore less useful,
minutes." That is a stated mechanism, a sharp date, and paired records on both sides.

**The precedent that makes this an asset rather than a liability.** Hansen, McMahon & Prat (2018),
*Quarterly Journal of Economics* 133(2), 801–870, used the 1993 transcript-release natural experiment
and computational linguistics to identify a positive discipline effect and a negative conformity
effect, concluding that discipline dominates. Their replication data are on Harvard Dataverse
(doi:10.7910/DVN/XAR1WZ — **[PARTIAL: DOI supplied by the project brief; we have not resolved it
ourselves]**). They measured how transparency changed **what was said**. We measure the gap between
what was said and **what was recorded**. Those are different quantities, and having the first one
already published in the *QJE* is the strongest possible evidence that the second is worth measuring.

All FOMC material is US government work; the corpus ships as a build script plus checksums anyway,
for provenance.

**Weakness:** the "is a central bank committee an organization?" objection. This is precisely why it
is now the third-ranked calibration substrate rather than the lead.

## 5. Council Data Project (retained: multimodal)

Verified via the JOSS paper (Brown et al., 2021, *JOSS* 6(68), 3904) and the *Councils in Action*
preprint (Brown & Weber, 2022, arXiv:2204.09110): a proof-of-concept corpus of over 350 meetings from
Seattle, Portland, and King County, each with video, audio, transcript, and full minutes including
legislative items, votes, and attached documents, on an open-source pipeline that scales horizontally
as new municipal instances are deployed. This is the only substrate that exercises the audio front
end, and the only one where roll-call votes give an outcome measured independently of any text.

**Weakness:** municipal councils are not firms, and machine transcription error enters the verbatim
side rather than the curated side, which is the wrong direction for a clean measurement.

## 6. Wikipedia Articles for Deletion (retained: scale and power)

Mayfield & Black (2019), *Proceedings of the ACM on Human-Computer Interaction* 3(CSCW),
doi:10.1145/3359308, built a structured corpus of **402,440 extracted AfD discussions** from
January 1, 2005 to December 31, 2018, containing over 3 million votes and comments, with timestamps,
outcomes, nominations, votes, users, and policy citations. A ConvoKit-formatted version reports
~3,200,000 contributions by ~150,000 editors across ~400,000 debates. Wikipedia content is CC BY-SA
(with GFDL), fully redistributable via the dumps. The pairing is the deliberation versus the
closing administrator's recorded rationale and outcome.

**Weaknesses:** the closing rationale is very short, so the pairing is lopsided; a management scholar
may reasonably decline to treat Wikipedia as an organization; and the corpus derived by Mayfield &
Black is distributed under GPL-3.0, which is a code licence applied to data and creates its own
downstream questions. We use it primarily for statistical power analysis and for stress-testing
robustness at a scale no other substrate reaches, not for headline organizational claims.

---

## 7. Rejected and reclassified

### 7.1 Earnings-call transcripts — rejected on licensing

The pairing is attractive: scripted prepared remarks versus unscripted analyst Q&A on the same call,
or the 8-K earnings press release versus the call. Li et al. (2021) built their corporate-culture
dictionary from 209,480 such transcripts. But the transcripts are proprietary. Refinitiv/LSEG
StreetEvents transcripts carry an explicit notice that "republication or redistribution of Refinitiv
content, including by framing or similar means, is prohibited without the prior written consent of
Refinitiv," and S&P Global Market Intelligence terms prohibit crawling, scraping, indexing, or
extracting web data from the service. A workflow requiring these transcripts violates the call's
reproducibility constraint as squarely as a workflow requiring a closed model does.

Partial workaround, honestly limited: the 8-K and its Exhibit 99.1 earnings release are on EDGAR and
are public; some firms post their own transcripts on their investor-relations sites. Coverage of
firm-hosted transcripts is inconsistent and not a panel. We therefore ship earnings calls as a
*portability target* — the instrument runs on a (prepared remarks, Q&A) pair if the user has one
locally — and build no earnings-call corpus.

### 7.2 Risk-factor disclosure — reclassified as an outcome, not a substrate

A risk factor added to a 10-K after the underlying risk had already materialised is a compelling
signal, and 10-K text is public domain and diffable across years. But it is not a paired record:
it is two records of *different* events at *different* times, so there is no same-event verbatim
counterpart and no supervised omission label. Using it as training data would smuggle the
researcher's judgement back in as the label, which is exactly what this design exists to avoid.

Its correct role is as a **downstream criterion**: if our instrument scores high omission on a firm's
filing at *t*, does that firm add a risk factor, restate, or receive an adverse finding at *t+k*?
That is a genuine predictive validity test using data the instrument never sees.

### 7.3 NLRB — rejected for Stage 1

The pairing exists in principle: an unfair-labour-practice hearing transcript versus the
Administrative Law Judge's decision. ALJ decisions are published and full-text searchable, and
NxGen case data are downloadable in bulk as CSV and XML (we observed 513,668 cases in the advanced
search index). But hearing **transcripts** live in NxGen and are not routinely posted; obtaining them
means per-case FOIA requests. That is not a scalable corpus by November 2026, and pretending
otherwise would fail the feasibility criterion.

The public ALJ-decision → Board-decision chain *is* a two-level curated record and is interesting,
but it is an appellate adjudication chain rather than the curation of a deliberative record. We note
it as an extension, not a Stage 1 substrate.

### 7.4 Arbitration awards and union grievance records — rejected

Labour arbitration awards are frequently confidential by agreement, and the systematic collections
that do exist are behind commercial paywalls. Grievance records are internal. There is no public
paired-record corpus here.

### 7.5 Hospital morbidity-and-mortality review — rejected

This is the theoretically ideal setting — a verbatim clinical discussion of a failure versus the
official incident record — and it is exactly why the construct has never been measured. M&M
proceedings are confidential and in the United States are typically protected by peer-review
privilege. Not public, not shareable, not available. Saying so is part of the contribution: the
places where omission matters most are the places where it is least observable.

### 7.6 Faculty senate minutes versus meeting recordings — deferred

Real, organizational (public universities are formal hierarchies with employment relationships), and
often subject to state open-meeting laws. But there is no common API, recording-retention practice
varies by institution and is often short, and minutes formats are idiosyncratic. This is the same
shape of problem the Council Data Project solved for municipalities, and the right answer is to make
it a community-extensible connector in the released artifact rather than a Stage 1 promise.

---

## 8. Construct naming, given what these substrates can and cannot support

Across all substrates, the primary quantity we can measure is a **recording gap**: a proposition
present in the verbatim record and absent, compressed, or de-attributed in the curated record.
Summarisation is legitimate and necessary; a recording gap is not by itself concealment.

- **Omission Rate** — the share of propositions that do not survive into the curated record, always
  reported conditional on topic, speaker count, and curated-document length.
- **Dissent Suppression Index** — Omission Rate restricted to disagreement-bearing propositions.
  This is the construct closest to Morrison & Milliken's (2000) collective withholding, and it is the
  one where the disagreement label is a model judgement rather than a document-derived fact, so it
  carries the heaviest validation burden.
- **Attribution Stripping Rate** — the proposition survives but the speaker's identity is removed or
  collectivised. Newly named and, we believe, newly measurable.

Only in the SEC substrate does an external authority adjudicate that a specific absence *should not*
have been an absence. That is why it leads.
