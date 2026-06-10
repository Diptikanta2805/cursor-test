# Implementation Plan — *DistAgency-Lab*

## A Computational Testbed for Distributed Agency in Human–AI Hybrid Teams

**Goal.** Turn He's purely conceptual *distributed agency* theory into a **formal, executable,
quantitatively evaluated computational model**, and extend it with a **novel adaptive delegation
controller** that *learns* Fidelity–Autonomy–Scope (F-A-S) settings online instead of relying on
manual tuning.

**Form factor.** 100% Python, single self-contained Google Colab notebook
(`distributed_agency_lab.ipynb`), zero extra installs (NumPy / pandas / Matplotlib only — all
pre-installed in Colab). Runtime ≈ 2–4 minutes on a free CPU runtime.

---

## 1. Significant Improvements & Novelty over the Paper

| # | Paper (conceptual) | DistAgency-Lab (this project) | Novelty class |
|---|---|---|---|
| N1 | F, A, S, staleness, novelty, divergence described verbally | **First mathematical formalization**: stochastic context-drift process, epistemic-alignment dynamics, executable Delegation Contracts | Formalization |
| N2 | Propositions asserted, never tested | **Agent-based simulation** testing P1–P5 against controlled baselines (human-only team, single generic copilot) with confidence intervals over seeds | In-silico validation |
| N3 | Human leader hand-tunes F-A-S; the "Update Routine" is left to leader judgment | **Adaptive Delegation Controller**: an evidence-driven feedback law that learns each representation's update rate (fidelity) online from observable decision-log events and *re-adapts after regime shifts* | New algorithm — the paper's open problem |
| N4 | "Divergence Index" named, inverted-U implied | Operationalized Divergence Index + **derived inverted-U curve** for inner-crowd wisdom (diversity sweep) | Quantified mechanism |
| N5 | Staleness gating described in an anecdote | **Shock-recovery event study**: measurable safety value of staleness gating (the "Northstar Tuesday" experiment) | Stress test |
| N6 | Trust "preserved" by etiquette (verbal) | **Endogenous trust dynamics** coupled to errors/disclosure/hand-backs, feeding back into team throughput | Closed-loop extension |
| N7 | — | **Optional LLM bridge**: hook to run pre-negotiation between liaison reps with real LLM agents (skipped gracefully when no API key) | Practice bridge |

---

## 2. Formal Model (to be implemented exactly as specified)

### 2.1 Environment: drifting context

- True context / principal goal vector: \(g_t \in \mathbb{R}^d\) (d = 8).
- Smooth drift: \(g_{t+1} = g_t + \eta_t,\quad \eta_t \sim \mathcal{N}(0, \sigma_{drift}^2 I)\).
- Shocks ("novelty events", e.g. the Legal Guardrails demand): with probability \(p_{shock}\),
  \(g_{t+1} \mathrel{+}= \delta_t\) on a random subset of dimensions, \(\|\delta_t\| \gg \sigma_{drift}\).
- Observable novelty signal: \(N_t = \tanh(\|g_t - g_{t-1}\| / \nu_0)\) (noisy proxy available to contracts).

### 2.2 Tasks (the work to coordinate)

Each step spawns \(K_t \sim \text{Poisson}(\lambda)\) tasks. Task \(j\): scope tag \(z_j\) (which
dimensions matter), impact \(I_j \in \{\text{low, med, high}\}\), reversibility \(r_j \in \{0,1\}\),
deadline \(\Delta_j\). Payoff of an executed action \(a\) on task \(j\):

\[ u_j(a) = V(I_j) \cdot \exp\!\big(- \|a - g_t\|_{z_j}^2 / 2\kappa^2 \big) - C_{exec} \]

Bad irreversible actions (\(u_j < u_{min}\), \(r_j = 0\)) incur an extra penalty \(P_{irr}\) and a
trust hit; bad reversible actions are rolled back at cost \(\rho\) (micro-handoff guardrail).
Missed deadlines score 0 (the cost of coordination overload).

### 2.3 AI representations (the portfolio)

Agent \(i\) has:
- **Fidelity** \(F_i \in (0,1]\): each step the agent resyncs its belief with probability \(F_i\);
  on resync \(\hat g_{i,t} \leftarrow g_t + \epsilon_{sync}\) and staleness \(s_{i,t} \leftarrow 0\),
  otherwise \(s_{i,t} \mathrel{+}= 1\). Resync costs the principal attention \(c_{refresh}\)
  (context-refresh rituals are not free).
- **Epistemic alignment**: \(A_{i,t} = \exp(-\|\hat g_{i,t} - g_t\|^2 / 2\kappa^2)\) — the paper's
  central construct, now measurable.
- **Autonomy** \(a_i \in \{\text{shadow}=0, \text{assist}=1, \text{suggest}=2, \text{act}=3\}\).
- **Scope** \(S_i \subseteq \{1..d\}\): dimension mask; agent can only take tasks with \(z_j \subseteq S_i\).
- Proposal: \(a_{i,j} = \hat g_{i,t} + b_i + \epsilon_{prop}\) restricted to \(z_j\), where \(b_i\) is
  the agent's designed perspective offset (used for inner-crowd diversity).

### 2.4 Executable Delegation Contract (paper Figure 1, made code)

```
may_act(i, j, t)      = (autonomy_i == ACT) ∧ (I_j ≤ impact_cap_i) ∧ r_j ∧ (z_j ⊆ S_i)
must_escalate(i,j,t)  = (N_t > θ_N) ∨ (s_{i,t} > θ_s) ∨ (I_j ≥ θ_I)
staleness_gate        : if must_escalate → effective autonomy = min(a_i, SUGGEST) (or ASSIST)
```

Suggest-mode routes the action to the **human ratification queue**.

### 2.5 The human principal (bottleneck & accountability locus)

- Attention budget \(B\) per step. Reviewing a raw task costs 1.0; ratifying a pre-negotiated
  suggestion costs \(c_{ratify} < 1\) (representations did the heavy lifting); refresh costs
  \(c_{refresh}\). Unprocessed items queue → latency → missed deadlines.
- Human-executed/ratified actions have small error \(\epsilon_h\) (humans are accurate but scarce).

### 2.6 Progressive autonomy & trust

- Per (agent, impact-band) **track record**: promote one autonomy level after \(k_{up}\)
  consecutive successes; demote on any failure or staleness-gate trip (paper's
  shadow→assist→suggest→act ladder).
- Counterparty trust: \(T_{t+1} = \text{clip}(T_t + \alpha \cdot \text{successes}_t - \beta \cdot
  \text{autonomous failures}_t + \gamma \cdot \text{disclosed hand-backs}_t)\);
  team throughput multiplier \(m(T) = 0.5 + 0.5\,T\).

### 2.7 Inner-crowd wisdom & Divergence Index

For "compose" tasks, \(m\) portfolio members each propose an option; the principal ratifies the
best under noisy evaluation (evaluation noise \(\sigma_{eval}\)):

\[ DI_t = \tfrac{2}{m(m-1)} \textstyle\sum_{i<j} \|a_i - a_j\| , \qquad
   \text{quality} = \max_i u(a_i) - c_{recon} \cdot DI_t \]

Diversity knob \(\delta\) scales the spread of perspective offsets \(b_i\). Hypothesis (paper P4):
quality is **inverted-U in \(\delta\)**.

### 2.8 NOVEL — Adaptive Delegation Controller (ADC)

The open problem the paper leaves to "leader judgment": it prescribes an *Update Routine* that
"monitors how out-of-date the representation's understanding is" but never specifies it. The ADC
implements it as a feedback law on **observable Chain-of-Decision evidence only** (no privileged
access to the true context). Per representation \(i\), over evidence windows of \(W\) steps, with
a fidelity ladder \(F \in \{0.05, 0.1, 0.2, 0.4, 0.7, 1.0\}\):

- **strong evidence** (rejected suggestion, rollback, irreversible failure — the rep's picture
  of the principal was *wrong*): jump 3 ladder levels (2+ events → jump to max);
- **weak evidence** (a staleness-gate trip blocked an action — the rep was merely *out of
  date*): move 1 level up;
- **clean window**: decay 1 level (refresh rituals consume principal attention, so staying
  maximally synced is wasteful in calm regimes).

This sharp-increase / gentle-decrease (AIMD-style) law is **non-stationary-aware by
construction**: when the drift regime changes mid-run, evidence reappears and the controller
re-climbs — something no fixed hand-tuned F-A-S profile can do. (A bandit over F-A-S
configurations was evaluated as an alternative and rejected: 10-step reward windows are too
noisy and exploration of high-autonomy arms causes real trust damage; the evidence-driven law
exploits the *structure* of the problem instead of treating it as a black box.)

---

## 3. Architectures Compared (the experimental conditions)

| Condition | Description | Maps to |
|---|---|---|
| `HUMAN_ONLY` | Principal reviews every task personally, budget-limited | Status quo "thicket of meetings" |
| `SINGLE_COPILOT` | One generic full-scope assistant, suggest-only, medium fidelity | "Unitary human + AI assistant" assumption the paper criticizes |
| `DA_FIXED` | Portfolio with hand-set F-A-S, **no** gating, **no** progression | Naive distributed agency |
| `DA_GATED` | + staleness/novelty gates + progressive autonomy + escalation (full paper framework) | The paper's full proposal |
| `DA_ADAPTIVE` | DA_GATED + **Adaptive Delegation Controller** | **Our novel extension** |

---

## 4. Evaluation Metrics (all logged per run, averaged over ≥ 20 seeds)

1. **Cumulative net team utility** (primary).
2. **Decision latency** (task arrival → execution) and **deadline-miss rate**.
3. **Human attention spent** per unit utility (coordination cost).
4. **Epistemic alignment** \(A_{i,t}\) trajectories (mean & during shocks).
5. **Error / rollback / irreversible-failure counts** (accountability).
6. **Escalation precision & recall** vs. ground-truth "should have escalated" labels.
7. **Trust trajectory** \(T_t\) and recovery half-life after shocks.
8. **Divergence Index ↔ option quality** curve (inverted-U test).

---

## 5. Experiments (each = one notebook section, one figure)

- **E1 — Architecture × drift sweep** (tests P1, P3): net utility of the 5 conditions across
  \(\sigma_{drift}\) ∈ {low, …, high}. *Expected:* DA dominates baselines; gating's advantage
  grows with drift.
- **E2 — Inner-crowd diversity sweep** (tests P4): option quality vs. diversity \(\delta\); plot
  the measured Divergence Index. *Expected:* inverted-U.
- **E3 — Progressive autonomy & trust** (tests P5, N6): fixed vs. progressive autonomy; autonomy
  level, error rate, and trust trajectories.
- **E4 — Shock recovery event study** (tests P5/N5, replicates "Northstar Tuesday"): inject a
  large shock at \(t_0\); compare gated vs. ungated alignment, losses, and trust around the event.
- **E5 — Adaptive controller & regime shift** (N3): calm regime (\(\sigma=0.01\)) for 300 steps,
  then turbulent (\(\sigma=0.20\)); compare DA_ADAPTIVE vs. every fixed fidelity profile; show
  the online re-adaptation of the update rate and total-utility comparison.

---

## 6. Step-by-Step Build Plan (Colab notebook sections)

| Step | Notebook section | Contents | Acceptance check |
|---|---|---|---|
| 0 | Setup | Imports (numpy/pandas/matplotlib), global config dataclass, seeding | runs with zero pip installs |
| 1 | Environment | `Context` (drift + shocks + novelty signal), `Task` generator | unit asserts: drift magnitude, shock frequency |
| 2 | Agents & contracts | `Representation` (F-A-S, beliefs, staleness), `DelegationContract.may_act / must_escalate`, staleness gate | asserts: high-F agent has higher alignment than low-F |
| 3 | Principal & team loop | attention budget, ratification queue, trust dynamics, decision log (auditability) | asserts: budget never exceeded; log row count == events |
| 4 | Metrics module | all §4 metrics from the decision log | metrics reproducible from log alone |
| 5 | Baselines & conditions | the 5 architectures of §3 behind one `run_episode(condition, params, seed)` API | identical seeds → identical streams across conditions |
| 6 | E1–E4 experiments | multi-seed sweeps + figures + CI bands | sanity asserts on ordering (e.g., DA_GATED ≥ HUMAN_ONLY) |
| 7 | Adaptive Delegation Controller | evidence-driven AIMD law over the fidelity ladder; E5 regime-shift experiment | ADC total ≥ 95% of best fixed profile, beats mean fixed profile, visibly re-adapts |
| 8 | (Optional) LLM bridge | pre-negotiation demo with real LLM liaisons via `OPENAI_API_KEY`; auto-skips if absent | notebook still runs fully without key |
| 9 | Results summary | results table + interpretation cell mapping findings back to P1–P5 | all asserts green, all figures rendered |

## 7. Risks & Mitigations

- **Toy-model criticism** → every mechanism maps 1:1 to a paper construct (documented in code
  comments + §2 equations); parameters swept, not cherry-picked; ≥ 20 seeds with CI bands.
- **Colab variability** → pure-NumPy implementation, vectorized hot loops, fixed seeds, < 4 min runtime.
- **LLM dependency** → strictly optional, isolated in Step 8.

## 8. Future Extensions (beyond this notebook)

1. Multi-principal meta-team: inter-portfolio pre-negotiation as a graph of intra-personal teams.
2. Replace the bandit with full RL (PPO) over continuous F-A-S settings.
3. Human-subject experiment: use the simulator as an oTree/behavioral backend.
4. LLM-native replication: every representation is an actual LLM agent with a signed contract.
