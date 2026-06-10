# Paper Analysis

**Paper:** *Leadership and Coordination in Human-AI Hybrid Teams: A Distributed Agency Approach*
**Author:** Vivianna Fang He (University College London)

> **Important note on paper type.** This is a **conceptual / theory-building article**, not an
> empirical or computational one. It contains **no dataset, no statistical model, no equations,
> and no quantitative evaluation**. The sections below therefore extract (a) what the paper
> explicitly provides, and (b) the *closest conceptual analogue* of each requested element
> (variables, "model architecture", metrics), clearly labeled as such. This gap is precisely the
> opportunity our new project exploits: we **formalize and computationally test** the theory
> (see `implementation_plan.md`).

---

## 1. Research Question

**Core question:** *How can organizations leverage AI technologies to augment — rather than
displace — human collaboration?*

Refined into the paper's specific question: **How should a human "principal" design, govern,
and lead a portfolio of AI representations of themselves ("distributed agency") so that team
coordination and performance improve while authenticity, accountability, and human connection
are preserved?**

Three sub-questions structure the article:

1. What are the **tunable design dimensions** of an AI representation? (→ Fidelity, Autonomy, Scope)
2. **Under what conditions** does the distributed-agency approach improve team coordination and
   performance? (→ coordination patterns, boundary conditions)
3. Which **interventions buffer the loss** of human willingness/capacity to collaborate?
   (→ presence etiquette, hand-backs, governance principles)

## 2. Methodology

| Aspect | What the paper does |
|---|---|
| Research design | **Conceptual theorizing** (organization-design theory development) |
| Methods | Typology construction (3×3 table), framework articulation (F-A-S dimensions + Delegation Contracts), mechanism-based reasoning, an **illustrative hypothetical case** ("Northstar" product launch) |
| Unit of analysis | The **intra-personal team** (one human principal + their portfolio of AI agents); the organization is a "meta-team of intra-personal teams" |
| Theoretical anchors | Information-processing view (Galbraith 1977), principal–agent theory (Jensen & Meckling 1976), team scaffolds (Valentine & Edmondson 2014), transactive memory (Argote & Ren 2012; Lewis 2004), collective intelligence (Woolley & Gupta 2024), wisdom of crowds (Surowiecki 2004), blockchain governance / smart contracts (Lumineau et al. 2021), levels of automation (Parasuraman et al. 2000) |
| Validation | None empirical — the Northstar case is explicitly "an illustration of its operational logic rather than direct empirical evidence" |

## 3. Data

**None.** There is no dataset, no sample, no field or lab study. The only "data-like" material is
the fictional Northstar product-launch vignette (timelines, a $5,000 purchase-order bound, a
$250k budget cap in the example Delegation Contract of Figure 1).

## 4. Variables (Conceptual Constructs)

The paper does not define operationalized variables, but its constructs map cleanly onto a
variable structure:

### Design / independent constructs (the "tunable knobs")
| Construct | Definition in paper | Tuning lever |
|---|---|---|
| **Fidelity (F)** | How closely (and in real time) the AI representation reflects the human's mental/cognitive/physical state | **Update rate** (frequency of context refresh) |
| **Autonomy (A)** | How much decision-making right the representation holds on the human's behalf | Graduated modes: **shadow → assist → suggest → act(-bounded)**; escalation thresholds |
| **Scope (S)** | How many aspects/roles of the principal the agent emulates | Task/role restriction ("task zoning" into risk bands) |
| Delegation Contract | Machine-readable decision-rights rule | `{scope} when {conditions} → {agent} may {suggest/act} using {data} with {counterparty} → escalate if {novelty/impact} > {thresholds}` |
| Progressive autonomy | Promotion/demotion of autonomy based on observed track record | k correct suggestions → promote; error/drift → demote |
| Context refresh rituals | Structured check-ins re-synchronizing agent beliefs with principal goals | Frequency, trigger-on-drift |
| Portfolio diversity | Deliberately heterogeneous agent "perspectives" | Curated via a **Divergence Index** |

### Mediating mechanisms
- **Epistemic alignment** (the central construct): the degree to which representations understand
  the principal's *current* preferences, information, and context. Failures are reframed as
  *epistemic* (stale context, underspecified preferences) rather than *incentive* misalignment.
- **Inner-crowd wisdom** (micro layer): diverse representations of one person generate
  better option sets from shared refreshed premises.
- **Transactive memory / organizational coherence** (macro layer).

### Outcome constructs
- Team **coordination cost** (meetings, calendar load, "calendar ping-pong")
- **Decision latency** and decision quality
- **Trust / human connection / authenticity** (preserved via disclosure banners and hand-backs)
- **Accountability** (auditability, attributability, reversibility — Chain-of-Decision log)
- **Equity of capability** ("agent-rich vs. agent-poor" divide)

### Moderators / boundary conditions
1. **Irreversible, high-impact decisions** → human presence mandatory (no delegation).
2. **Low-information contexts** (novel tasks, sparse feedback) → conservative autonomy, higher update rate.
3. **Cross-boundary transactions** (customers, regulators) → stricter verification, more human involvement.

## 5. Model Architecture / Equations

**No formal model or equations are given.** The closest structural elements are:

1. **The 3×3 typology (Table 1):** Fidelity {low, medium, high} × Autonomy {none, advisory,
   autonomous} → 9 agent types (Static Clone, Reflective Persona, Representative Twin, Guided
   Clone, Adaptive Persona, Assisting Twin, Autonomous Clone, Autonomous Proxy, Autonomous Twin).
2. **The Delegation Contract pseudo-grammar (Figure 1):**
   ```
   DELEGATION CONTRACT: Representing the Product Liaison Role for Aisha
   Tasks:        Compose, analyse, and select launch options
   Conditions:   scope ∈ {MVP, MVP+}, timeline ≤ 8 weeks, budget ≤ $250k
   Autonomy:     SUGGEST
   Data:         roadmap:v4, capacity:sprint-32..34, finance:unit-econ-2025Q1
   EscalateIf:   novelty > 0.6 OR staleness > 24h OR impact ≥ "external-commit"
   ```
3. **The coordination loop:** `sense → compose → ratify → act → learn`, instantiated by three
   patterns: **elastic attendance**, **pre-negotiation by representations**, **micro-handoffs**.
4. **Control rules (verbal):** staleness gating (autonomy ↓ when context lag/novelty ↑),
   escalation triggers, promotion/demotion ladder, Divergence Index monitoring.

## 6. Evaluation Metrics

**None are computed.** The paper *names* measurable quantities without operationalizing them:

- **Divergence Index** — "how far the portfolio's proposals spread on the key dimensions that matter"
- **Staleness / context lag** — time since last context refresh
- **Novelty** and **impact** thresholds (escalation triggers)
- **Track record** of correct suggestions (promotion criterion)
- Implied outcomes: number of meetings, decision latency, rework hours, error/rollback counts, trust

## 7. Main Results (Theoretical Claims / Propositions)

Because the paper is conceptual, the "results" are propositions:

- **P1 — Epistemic (not incentive) alignment is the central design problem.** Since current AI
  agents lack private goals, breakdowns stem from context drift and underspecified preferences;
  the remedy set is *update frequency, reduced autonomy/scope, and human involvement at
  consequential moments* — not incentives or punishment.
- **P2 — Tunable F-A-S + Delegation Contracts make distributed agency tractable and governable.**
  Portfolio design (risk, reversibility, value criteria; task zoning) converts vague AI-use
  guidelines into auditable decision-rights contracts.
- **P3 — Three new coordination patterns reduce coordination cost and decision latency** while
  preserving accountability: elastic attendance, pre-negotiation, micro-handoffs
  (the sense→compose→ratify→act→learn loop).
- **P4 — Inner-crowd wisdom:** curated, *bounded* diversity among one principal's representations
  raises option quality; excessive divergence fragments intent (implied **inverted-U**).
- **P5 — Progressive (gated) autonomy** — promotion on evidence, automatic demotion on
  staleness/novelty — yields adaptability without surrendering accountability; in the Northstar
  case, automatic downgrade after a detected update discrepancy *increased* trust.
- **P6 — Governance pillars** (authenticity, accountability, privacy/data decay, equity of
  capability) plus the three boundary conditions keep the system human-centric.

## 8. Identified Gaps (Opportunities for Our New Project)

1. **No formalization** — F, A, S, staleness, novelty, divergence are never defined mathematically.
2. **No simulation or empirical test** of any proposition (P1–P5 are all testable in silico).
3. **F-A-S settings are hand-tuned by the human leader** — the paper offers no mechanism to
   *learn* optimal settings; this is an open algorithmic problem (our key novelty: an adaptive
   delegation controller).
4. **The inverted-U divergence claim (P4)** is asserted, never derived or measured.
5. **No quantitative comparison** against status-quo baselines (human-only teams, single generic
   copilot).
6. **No stress-test of the staleness-gating safety mechanism** (the paper's Tuesday-shock anecdote
   is fictional).

These gaps define the agenda of the new project in `implementation_plan.md`.
