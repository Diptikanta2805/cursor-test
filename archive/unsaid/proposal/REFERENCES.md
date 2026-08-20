# References and Verification Log

Every citation used anywhere in this package, with venue, volume, pages, DOI or URL, and
verification status. Nothing here was taken on trust from the prior ideation memo or from the project
brief; each item was checked in August 2026.

**Verification method.** Journal articles were checked against the Crossref REST API by DOI (and by
bibliographic search where the DOI was uncertain), which returns the registered title, author list,
container title, volume, issue, pages, and publication dates. Data packages were resolved directly.
Models were checked against the Hugging Face Hub API for existence, licence, and gating status.

**Status codes**

| Code | Meaning |
|---|---|
| `VERIFIED` | Title, authors, venue, volume/issue, pages, and DOI all confirmed against the registry record. |
| `PARTIAL` | Exists and is correctly attributed, but one bibliographic detail could not be confirmed from a registry record. |
| `PREPRINT` | Real and locatable, but not peer-reviewed and not in a journal issue. |
| `SOURCE` | Primary institutional or documentary source (regulator page, governance document, dataset) rather than a scholarly citation. |

---

## 1. Cited in the proposal, appendix, or scorecard

**Angelopoulos, A. N., Bates, S., Fannjiang, C., Jordan, M. I., & Zrnic, T. (2023).**
Prediction-powered inference. *Science*, 382(6671), 669–674.
doi:[10.1126/science.adi6000](https://doi.org/10.1126/science.adi6000) — `VERIFIED`

**Bozanic, Z., Dietrich, J. R., & Johnson, B. A. (2017).** SEC comment letters and firm disclosure.
*Journal of Accounting and Public Policy*, 36(5), 337–357.
doi:[10.1016/j.jaccpubpol.2017.07.004](https://doi.org/10.1016/j.jaccpubpol.2017.07.004) — `VERIFIED`

**Brown, E. M., Huynh, T., Na, I., Ledbetter, B., Ticehurst, H., Liu, S., Gilles, E., Greene,
K. M. F., Cho, S., Ragoler, S., & Weber, N. (2021).** Council Data Project: Software for municipal
data collection, analysis, and publication. *Journal of Open Source Software*, 6(68), 3904.
doi:[10.21105/joss.03904](https://doi.org/10.21105/joss.03904) — `VERIFIED`

**Brown, E. M., & Weber, N. (2022).** Councils in Action: Automating the curation of municipal
governance data for research. *Proceedings of the Association for Information Science and
Technology*, 59(1), 23–31. doi:[10.1002/pra2.601](https://doi.org/10.1002/pra2.601);
preprint arXiv:[2204.09110](https://arxiv.org/abs/2204.09110) — `VERIFIED`
*Note: the prior memo cited only the arXiv preprint. The peer-reviewed version exists and is cited
here in preference to it.*

**Carlson, N. A., & Burbano, V. (2026).** The use of LLMs to annotate data in management research:
Foundational guidelines and warnings. *Strategic Management Journal*, 47(3), 699–725.
doi:[10.1002/smj.70023](https://doi.org/10.1002/smj.70023) — `VERIFIED`
*Note: published online 29 October 2025; assigned to the March 2026 print issue. We cite the print
year, so a reader may encounter this as "2025" elsewhere.*

**Cassell, C. A., Cunningham, L. M., & Lisic, L. L. (2019).** The readability of company responses to
SEC comment letters and SEC 10-K filing review outcomes. *Review of Accounting Studies*, 24(4),
1252–1276. doi:[10.1007/s11142-019-09507-x](https://doi.org/10.1007/s11142-019-09507-x) — `VERIFIED`

**Cassell, C. A., Dreher, L. M., & Myers, L. A. (2013).** Reviewing the SEC's review process: 10-K
comment letters and the cost of remediation. *The Accounting Review*, 88(6), 1875–1908.
doi:[10.2308/accr-50538](https://doi.org/10.2308/accr-50538) — `VERIFIED`
*Note: an earlier draft of `SUBSTRATES.md` flagged the pages as unconfirmed and carried the wrong DOI
suffix (`accr-50503`, which belongs to an unrelated tax paper). Corrected.*

**Daft, R. L., & Lewin, A. Y. (1990).** Can organization studies begin to break out of the normal
science straitjacket? An editorial essay. *Organization Science*, 1(1), 1–9.
doi:[10.1287/orsc.1.1.1](https://doi.org/10.1287/orsc.1.1.1) — `VERIFIED`

**Detert, J. R., & Edmondson, A. C. (2011).** Implicit voice theories: Taken-for-granted rules of
self-censorship at work. *Academy of Management Journal*, 54(3), 461–488.
doi:[10.5465/amj.2011.61967925](https://doi.org/10.5465/amj.2011.61967925) — `VERIFIED`

**Dilba, D., & Meyer, B. (2025).** Uneventful days? A cautionary tale about the underestimated role
of triggering events in employee silence research. *Journal of Occupational and Organizational
Psychology*, 98(1). doi:[10.1111/joop.12549](https://doi.org/10.1111/joop.12549) — `PARTIAL`
*Authors, title, venue, volume, issue, and the March 2025 print issue confirmed (online-first
September 2024). Crossref registers no page range for this record, so none is given.*

**Dye, R. A. (1985).** Disclosure of nonproprietary information. *Journal of Accounting Research*,
23(1), 123–145. doi:[10.2307/2490910](https://doi.org/10.2307/2490910) — `PARTIAL`
*The Crossref record registers the start page (123) only; the end page 145 is from the standard
citation and was not confirmed from a registry record.*

**Edmondson, A. C. (1999).** Psychological safety and learning behavior in work teams.
*Administrative Science Quarterly*, 44(2), 350–383.
doi:[10.2307/2666999](https://doi.org/10.2307/2666999) — `VERIFIED`

**Egami, N., Hinck, M., Stewart, B. M., & Wei, H. (2023).** Using imperfect surrogates for downstream
inference: Design-based supervised learning for social science applications of large language models.
*Advances in Neural Information Processing Systems*, 36, 68589–68601.
arXiv:[2306.04746](https://arxiv.org/abs/2306.04746);
Crossref [10.52202/075280-3000](https://doi.org/10.52202/075280-3000) — `VERIFIED`

**Eisenberg, E. M. (1984).** Ambiguity as strategy in organizational communication. *Communication
Monographs*, 51(3), 227–242.
doi:[10.1080/03637758409390197](https://doi.org/10.1080/03637758409390197) — `VERIFIED`

**Gartenberg, C., Hasan, S., Murray, F., & Pierce, L. (2026).** More versus better: Artificial
intelligence, incentives, and the emerging crisis in peer review. *Organization Science*, 37(3),
795–812. doi:[10.1287/orsc.2026.ed.v37.n3](https://doi.org/10.1287/orsc.2026.ed.v37.n3) — `VERIFIED`
*Note: the project brief listed four authors as "Gartenberg, Hasan, Murray & Pierce"; the registry
record confirms this author list, volume, issue, and pages.*

**Gilardi, F., Alizadeh, M., & Kubli, M. (2023).** ChatGPT outperforms crowd workers for
text-annotation tasks. *Proceedings of the National Academy of Sciences*, 120(30), e2305016120.
doi:[10.1073/pnas.2305016120](https://doi.org/10.1073/pnas.2305016120) — `VERIFIED`

**Girotra, K., Terwiesch, C., & Ulrich, K. T. (2010).** Idea generation and the quality of the best
idea. *Management Science*, 56(4), 591–605.
doi:[10.1287/mnsc.1090.1144](https://doi.org/10.1287/mnsc.1090.1144) — `VERIFIED`

**Hansen, S., McMahon, M., & Prat, A. (2018).** Transparency and deliberation within the FOMC: A
computational linguistics approach. *The Quarterly Journal of Economics*, 133(2), 801–870.
doi:[10.1093/qje/qjx045](https://doi.org/10.1093/qje/qjx045) — `VERIFIED`
*Note: Crossref records an online-first date in 2017 and the print issue in May 2018. We cite 2018.*

**Hansen, S., McMahon, M., & Prat, A. (2017).** *Replication data for: "Transparency and deliberation
within the FOMC: A computational linguistics approach."* Harvard Dataverse.
doi:[10.7910/DVN/XAR1WZ](https://doi.org/10.7910/DVN/XAR1WZ) — `SOURCE`, resolved
*We resolved this ourselves via the Dataverse API. Licence: **CC0 1.0**, so the replication measures
can be reused for convergent validity without permission.*

**Johnston, R. (2025).** SEC comment letter research — *quo vadis*? SSRN working paper 4587987.
https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4587987 — `PREPRINT`

**Johnston, R., & Petacchi, R. (2017).** Regulatory oversight of financial reporting: Securities and
Exchange Commission comment letters. *Contemporary Accounting Research*, 34(2), 1128–1155.
doi:[10.1111/1911-3846.12297](https://doi.org/10.1111/1911-3846.12297) — `VERIFIED`

**Li, K., Mai, F., Shen, R., & Yan, X. (2021).** Measuring corporate culture using machine learning.
*The Review of Financial Studies*, 34(7), 3265–3315.
doi:[10.1093/rfs/hhaa079](https://doi.org/10.1093/rfs/hhaa079) — `VERIFIED`
*Note: online-first 2020, print issue 2021. We cite 2021, as the prior memo did.*

**Li, Y., & Luo, Y. (2025).** Determinants and consequences of SEC comment letters: A review.
*Accounting Perspectives*, 24(3), 735–786.
doi:[10.1111/1911-3838.12405](https://doi.org/10.1111/1911-3838.12405) — `VERIFIED`

**March, J. G. (1991).** Exploration and exploitation in organizational learning. *Organization
Science*, 2(1), 71–87. doi:[10.1287/orsc.2.1.71](https://doi.org/10.1287/orsc.2.1.71) — `VERIFIED`

**Mayfield, E., & Black, A. W. (2019).** Analyzing Wikipedia deletion debates with a group
decision-making forecast model. *Proceedings of the ACM on Human-Computer Interaction*, 3(CSCW),
1–26. doi:[10.1145/3359308](https://doi.org/10.1145/3359308) — `VERIFIED`

**Morrison, E. W. (2023).** Employee voice and silence: Taking stock a decade later. *Annual Review
of Organizational Psychology and Organizational Behavior*, 10(1), 79–107.
doi:[10.1146/annurev-orgpsych-120920-054654](https://doi.org/10.1146/annurev-orgpsych-120920-054654)
— `VERIFIED`

**Morrison, E. W., & Milliken, F. J. (2000).** Organizational silence: A barrier to change and
development in a pluralistic world. *Academy of Management Review*, 25(4), 706–725.
doi:[10.5465/amr.2000.3707697](https://doi.org/10.5465/amr.2000.3707697) — `PARTIAL`
*Authors, venue, volume, issue, year, and start page all confirmed. The Crossref record registers the
start page (706) only; the end page 725 comes from the standard citation, which the project brief
also gives.*

**Ocasio, W. (1997).** Towards an attention-based view of the firm. *Strategic Management Journal*,
18(S1), 187–206.
doi:[10.1002/(SICI)1097-0266(199707)18:1+<187::AID-SMJ936>3.0.CO;2-K](https://doi.org/10.1002/(SICI)1097-0266(199707)18:1+%3C187::AID-SMJ936%3E3.0.CO;2-K)
— `VERIFIED`

**Tucker, A. L., & Edmondson, A. C. (2003).** Why hospitals don't learn from failures: Organizational
and psychological dynamics that inhibit system change. *California Management Review*, 45(2), 55–72.
doi:[10.2307/41166165](https://doi.org/10.2307/41166165) — `VERIFIED`

**Verrecchia, R. E. (2001).** Essays on disclosure. *Journal of Accounting and Economics*, 32(1–3),
97–180.
doi:[10.1016/S0165-4101(01)00025-8](https://doi.org/10.1016/S0165-4101(01)00025-8) — `VERIFIED`

---

## 2. Verified at the brief's request, but not used

These were on the re-verification list. All three check out; none is load-bearing for this design, so
they are not cited in the proposal. Listing them here rather than working them into the text is the
honest option: padding a reference list with verified-but-irrelevant work is exactly the failure mode
the special issue is reacting against.

**Bail, C. A. (2024).** Can Generative AI improve social science? *Proceedings of the National Academy
of Sciences*, 121(21), e2314021121.
doi:[10.1073/pnas.2314021121](https://doi.org/10.1073/pnas.2314021121) — `VERIFIED`
*Relevant as general framing (and Bail is a special-issue editor), but the proposal's argument is
about paired-record supervision, not about generative AI's promise in social science generally.*

**Hu, A., & Ma, S. (2025).** Persuading investors: A video-based study. *The Journal of Finance*,
80(5), 2639–2688. doi:[10.1111/jofi.13471](https://doi.org/10.1111/jofi.13471) — `VERIFIED`
*The prior memo cited it as a 2025 *Journal of Finance* article, which is correct. It is a good
precedent for machine-measured constructs from non-text modalities in a top finance journal, but it
does not bear on the omission construct.*

**Woolley, A. W., Chabris, C. F., Pentland, A., Hashmi, N., & Malone, T. W. (2010).** Evidence for a
collective intelligence factor in the performance of human groups. *Science*, 330(6004), 686–688.
doi:[10.1126/science.1193147](https://doi.org/10.1126/science.1193147) — `VERIFIED`
*Cited in the prior memo for the group-process link. We dropped it because equal conversational
turn-taking and recording-gap measurement are related only loosely, and stretching the connection
would weaken rather than strengthen the framing.*

---

## 3. Primary institutional and documentary sources

All accessed August 2026. Status `SOURCE` throughout.

**U.S. Securities and Exchange Commission.** *How to search for EDGAR correspondence.*
https://www.sec.gov/search-filings/edgar-search-assistance/how-search-edgar-correspondence
— basis for the 20-business-day public-release rule and the `UPLOAD` / `CORRESP` form types.

**U.S. Securities and Exchange Commission.** *Filing review process.*
https://www.sec.gov/about/divisions-offices/division-corporation-finance/filing-review-process
— basis for the selective-review description.

**U.S. Securities and Exchange Commission.** *Accessing EDGAR data* / *Developer resources.*
https://www.sec.gov/os/accessing-edgar-data — basis for the 10 requests/second fair-access limit, the
`User-Agent` requirement, and the absence of any API key or paid tier.

**U.S. Securities and Exchange Commission.** EDGAR quarterly full-index files.
`https://www.sec.gov/Archives/edgar/full-index/{year}/{QTR}/form.idx` — the source of our own
502,712-document count for 2004-08 through mid-2026.

**U.S. Securities and Exchange Commission.** Staff comment letter to SITE Centers Corp., 16 April
2024. `edgar/data/894315/0000000000-24-004121.txt` — quoted in `SUBSTRATES.md` §1.2; reviewed filing
`0000950170-24-019352`.

**U.S. Securities and Exchange Commission.** Staff comment letter to Royal Gold, Inc., 22 May 2024.
`edgar/data/85535/0000000000-24-005929.txt` — quoted in `SUBSTRATES.md` §1.2; reviewed filing
`0001558370-24-001192`.

**NASA Aviation Safety Reporting System.** *ASRS database online* and *search strategies /
documentation.* https://asrs.arc.nasa.gov/search/database.html — basis for the `Narrative` versus
analyst-written `Synopsis` pairing, the >1,000,000-report figure, 1988–present coverage, the
10,000-record export cap, and the de-identification policy.
*Redistribution position: `PARTIAL` — currently rests on a third-party reproduction package's
characterisation of NASA's terms; to be confirmed in writing with the ASRS office before submission.*

**Python Software Foundation.** *PEP 1 — PEP purpose and guidelines.*
https://peps.python.org/pep-0001/ — basis for the mandated `Discussions-To` thread, `Post-History`,
the `Resolution` header, and the dual public-domain / CC0-1.0 licence for PEP text.

**Rust project.** `rust-lang/rfcs` repository and RFC 2044.
https://github.com/rust-lang/rfcs — basis for the dual MIT / Apache-2.0 licensing of RFC content and
for PR-thread deliberation.

**Kubernetes project.** `kubernetes/enhancements` repository.
https://github.com/kubernetes/enhancements — basis for KEP structure and Apache-2.0 licensing.

**Board of Governors of the Federal Reserve System.** FOMC minutes, 14 December 2004, and the FOMC
transcript and minutes archives. https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm —
basis for the ~5-year transcript lag, the December 2004 decision to accelerate minutes release, and
the quoted concern about "less comprehensive, and therefore less useful, minutes."

**National Labor Relations Board.** Advanced case search and NxGen bulk data.
https://www.nlrb.gov/search/case — basis for the ~513,668-case figure and for the finding that
hearing transcripts are not routinely posted (see `SUBSTRATES.md` §7.3).

**LSEG / Refinitiv StreetEvents** and **S&P Global Market Intelligence** terms of use — basis for
rejecting earnings-call transcripts on redistribution grounds (`SUBSTRATES.md` §7.1). Cited as
publisher terms, not scholarship.

---

## 4. Models: existence, licence, and gating (Hugging Face Hub, August 2026)

Checked via the Hub API. "Gated" means access requires a free Hugging Face account and acceptance of
user conditions — no payment, but a real reproducibility step that a replicator must take.

| Model | Licence | Gated? | Status |
|---|---|---|---|
| `openai/gpt-oss-20b` | Apache-2.0 | No | `VERIFIED` |
| `Qwen/Qwen3-8B` | Apache-2.0 | No | `VERIFIED` |
| `Qwen/Qwen3-4B-Instruct-2507` | Apache-2.0 | No | `VERIFIED` |
| `Qwen/Qwen3-Embedding-0.6B` | Apache-2.0 | No | `VERIFIED` |
| `Qwen/Qwen3-Reranker-0.6B` | Apache-2.0 | No | `VERIFIED` |
| `microsoft/phi-4` | MIT | No | `VERIFIED` |
| `mistralai/Mistral-Small-3.2-24B-Instruct-2506` | Apache-2.0 | No | `VERIFIED` |
| `allenai/OLMo-2-1124-13B-Instruct` | Apache-2.0 | No | `VERIFIED` |
| `chentong00/propositionizer-wiki-flan-t5-large` | Apache-2.0 | No | `VERIFIED` |
| `BAAI/bge-m3` | MIT | No | `VERIFIED` |
| `BAAI/bge-reranker-v2-m3` | Apache-2.0 | No | `VERIFIED` |
| `MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli` | MIT | No | `VERIFIED` |
| `cross-encoder/nli-deberta-v3-large` | Apache-2.0 | No | `VERIFIED` |
| `openai/whisper-large-v3` | Apache-2.0 | No | `VERIFIED` |
| `nvidia/parakeet-tdt-0.6b-v2` | CC-BY-4.0 | No | `VERIFIED` |
| `pyannote/speaker-diarization-3.1` | MIT | **Yes** | `VERIFIED` |
| `nvidia/diar_streaming_sortformer_4spk-v2` | CC-BY-4.0 | No | `VERIFIED` |

### Models named in the prior memo that we replaced

| Named | What we found | Replacement |
|---|---|---|
| Gemma (`google/gemma-3-12b-it`) | Exists, but the licence is the custom **Gemma Terms of Use** — not OSI-approved, carries use restrictions and obligations on derivatives — and the repo is **gated**. | `microsoft/phi-4` (MIT) and `mistralai/Mistral-Small-3.2-24B-Instruct-2506` (Apache-2.0) |
| `nvidia/diar_sortformer_4spk-v1` (considered) | Exists, but **CC-BY-NC-4.0**; a non-commercial clause is wrong for infrastructure meant to be freely reusable. | `nvidia/diar_streaming_sortformer_4spk-v2` (CC-BY-4.0) |

No model name in the prior memo turned out to be fabricated. The substitutions above are licensing
decisions, not corrections of nonexistent models.

---

## 5. Summary of verification outcomes

- **Scholarly citations checked: 32** — 29 in §1 plus the 3 verified-but-unused items in §2.
  Twenty-eight are `VERIFIED`, three are `PARTIAL` (Morrison & Milliken 2000, Dye 1985, and Dilba &
  Meyer 2025 — in each case because Crossref registers a start page only or no page range at all,
  never because the attribution was in doubt), and one is a `PREPRINT` (Johnston 2025, correctly
  labelled as an SSRN working paper).
- **No citation from the prior memo was found to be fabricated or misattributed.** Two needed
  correction of bibliographic detail: the Cassell, Dreher and Myers DOI suffix was wrong in an
  earlier draft of our own substrate file, and Brown and Weber (2022) has a peer-reviewed version we
  now cite instead of the preprint alone.
- **The one figure we refused to inherit was a volume claim, not a citation.** The brief and the
  prior memo both put SEC correspondence at "approximately 600,000 documents." Our own sweep of the
  EDGAR quarterly indexes gives **502,712**. We report the measured number.
- **All 17 models verified as existing with the stated licence.** One family (Gemma) was replaced on
  licensing grounds and one diarisation checkpoint was rejected for a non-commercial clause.
- **Two documentary items remain `PARTIAL` and are open work items:** NASA's redistribution position
  in writing, and the content licence for `discuss.python.org` and the `python-dev` archives.
