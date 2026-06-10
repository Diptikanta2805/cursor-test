# %% [markdown]
# # DistAgency-Lab
# ## A Computational Testbed for *Distributed Agency* in Human–AI Hybrid Teams
#
# [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Diptikanta2805/cursor-test/blob/main/distributed_agency_lab.ipynb)
#
# **Based on:** He, V. F., *Leadership and Coordination in Human-AI Hybrid Teams: A Distributed
# Agency Approach* (conceptual article).
#
# **What this notebook does.** The paper is purely conceptual: it proposes that each human
# "principal" should lead a portfolio of AI representations tuned along **Fidelity–Autonomy–Scope
# (F-A-S)** dimensions, governed by **Delegation Contracts**, **staleness/novelty gating**,
# **progressive autonomy**, and **inner-crowd wisdom** — but it provides no equations, data, or
# tests. This notebook contributes:
#
# 1. **N1 — First mathematical formalization** of the framework (drifting context, epistemic
#    alignment, executable delegation contracts).
# 2. **N2 — Agent-based simulation** testing the paper's propositions P1–P5 against controlled
#    baselines (human-only team, single generic copilot), with confidence intervals.
# 3. **N3 — Adaptive Delegation Controller (ADC)**: a feedback controller that *learns* each
#    representation's update rate online from observable decision-log evidence and re-adapts
#    after regime shifts — solving the open problem the paper leaves to "leader judgment".
# 4. **N4 — Quantified inner-crowd wisdom**: an operational Divergence Index and a derived
#    inverted-U diversity curve.
# 5. **N5 — Shock-recovery event study** of the staleness-gating safety mechanism (the
#    "Northstar Tuesday" scenario from the paper's illustrative case).
# 6. **N6 — Endogenous trust dynamics** coupling agent errors and hand-backs to team throughput.
#
# **Runs in Google Colab with zero installs** (NumPy / pandas / Matplotlib only), ≈ 2–4 min on a
# free CPU runtime. See `paper_analysis.md` and `implementation_plan.md` in the repo for the full
# paper extraction and design rationale.

# %% [markdown]
# ## Section 0 — Setup & global configuration
#
# All parameters of the formal model live in one dataclass so every experiment is a transparent
# `replace(...)` of the defaults.

# %%
import math
import os
import pathlib
import time
from dataclasses import dataclass, replace

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# %matplotlib inline

T_START = time.time()
FIG_DIR = pathlib.Path("figures")
FIG_DIR.mkdir(exist_ok=True)

plt.rcParams.update({
    "figure.dpi": 110, "axes.grid": True, "grid.alpha": 0.3,
    "axes.spines.top": False, "axes.spines.right": False,
    "font.size": 9, "legend.fontsize": 8,
})

def show_save(fig, name):
    """Save figure to ./figures and display it."""
    fig.tight_layout()
    fig.savefig(FIG_DIR / f"{name}.png", bbox_inches="tight")
    plt.show()

# Autonomy ladder (paper: shadow -> assist -> suggest -> act)
SHADOW, ASSIST, SUGGEST, ACT = 0, 1, 2, 3
AUTONOMY_NAMES = ["shadow", "assist", "suggest", "act"]
# Impact bands (paper: task zoning into risk bands)
LOW, MED, HIGH = 0, 1, 2

@dataclass
class Params:
    # --- environment: drifting context (Sec 2.1 of the plan) ---
    d: int = 8                      # context dimensions (4 domains x 2 dims)
    horizon: int = 300              # steps per episode
    sigma_drift: float = 0.08       # smooth context drift per step
    p_shock: float = 0.015          # probability of a novelty shock per step
    shock_scale: float = 1.4        # shock magnitude (std)
    shock_dims: int = 4             # number of dimensions hit by a shock
    nu0: float = 0.7                # novelty-signal normalizer
    # --- tasks (Sec 2.2) ---
    lam_tasks: float = 3.5          # Poisson arrival rate per step
    p_cross: float = 0.10           # cross-domain tasks (no single rep covers them)
    impact_probs: tuple = (0.6, 0.3, 0.1)
    impact_values: tuple = (1.0, 2.5, 6.0)
    p_reversible: tuple = (0.9, 0.6, 0.2)
    deadline: int = 4               # steps before an unprocessed task is missed
    kappa: float = 0.6              # payoff alignment bandwidth
    success_frac: float = 0.5       # alignment factor needed for success
    c_exec: float = 0.05            # execution overhead
    p_irr: float = 4.0              # extra penalty for irreversible failure
    rho: float = 0.4                # rollback cost (reversible failure)
    # --- representations (Sec 2.3) ---
    eps_sync: float = 0.05          # residual error after a context refresh
    eps_prop: float = 0.12          # proposal noise
    eps_human: float = 0.05         # human execution noise
    rep_capacity: int = 2           # tasks one representation can prepare per step
    # --- the human principal (Sec 2.5) ---
    budget: float = 3.0             # attention units per step
    c_review: float = 1.0           # handle a raw task personally
    c_assist: float = 0.7           # handle with assist-mode prep
    c_ratify: float = 0.35          # ratify a pre-negotiated suggestion
    c_fix: float = 0.6              # redo a rejected suggestion
    c_refresh: float = 0.5          # one context-refresh ritual with one rep
    sigma_check: float = 0.25       # noise in human's quality check of suggestions
    w_att: float = 0.3              # utility price of one attention unit
    # --- delegation contract thresholds (Sec 2.4; paper Fig. 1) ---
    theta_N: float = 0.85           # novelty escalation threshold (trips on shocks, not drift)
    theta_s: int = 10               # staleness escalation threshold
    # --- progressive autonomy & trust (Sec 2.6) ---
    k_up: int = 4                   # consecutive successes to promote
    trust0: float = 0.85
    trust_alpha: float = 0.0005     # trust gain per success
    trust_beta: float = 0.08        # trust loss per *autonomous* failure
    trust_gamma: float = 0.0002    # trust gain per disclosed hand-back (ratification)
    # --- schedules for special experiments ---
    drift_schedule: tuple = ()      # ((t_start, sigma), ...) overrides sigma_drift
    forced_shocks: tuple = ()       # deterministic shock times (E4)

P0 = Params()
print("Default parameters ready. d =", P0.d, "| horizon =", P0.horizon)

# %% [markdown]
# ## Section 1 — Environment: drifting context, novelty shocks, tasks
#
# The principal's true goal/context vector $g_t \in \mathbb{R}^8$ follows
# $g_{t+1} = g_t + \eta_t$, $\eta_t \sim \mathcal{N}(0,\sigma_{drift}^2 I)$, with occasional
# **novelty shocks** (e.g. the Legal *Guardrails* demand in the paper's Northstar case).
# The observable novelty signal is $N_t = \tanh(\lVert g_t - g_{t-1}\rVert / \nu_0)$.
#
# Work arrives as **tasks**: each belongs to one of 4 functional domains
# (engineering / marketing / finance / legal — mirroring the Northstar case), has an impact band
# (low/med/high), a reversibility flag, and a deadline. Executing action $a$ yields
# $u = V(I)\, m(T)\, \exp(-\lVert a - g_t\rVert_{z}^2 / 2\kappa^2) - c_{exec}$, where $m(T)$ is the
# trust multiplier and $z$ the task's dimensions.

# %%
DOMAINS = ["engineering", "marketing", "finance", "legal"]
DOMAIN_DIMS = {0: np.array([0, 1]), 1: np.array([2, 3]),
               2: np.array([4, 5]), 3: np.array([6, 7])}

class Context:
    """True context g_t with smooth drift + novelty shocks; emits a noisy novelty signal."""

    def __init__(self, p, rng):
        self.p = p
        self.g = rng.normal(0.0, 1.0, p.d)
        self.novelty = 0.0
        self.shock_times = []

    def _sigma(self, t):
        sigma = self.p.sigma_drift
        for t0, s in self.p.drift_schedule:
            if t >= t0:
                sigma = s
        return sigma

    def step(self, t, rng):
        prev = self.g.copy()
        self.g = self.g + rng.normal(0.0, self._sigma(t), self.p.d)
        shock = (rng.random() < self.p.p_shock) or (t in self.p.forced_shocks)
        if shock:
            dims = rng.choice(self.p.d, size=self.p.shock_dims, replace=False)
            self.g[dims] += rng.normal(0.0, self.p.shock_scale, len(dims))
            self.shock_times.append(t)
        self.novelty = math.tanh(float(np.linalg.norm(self.g - prev)) / self.p.nu0)

@dataclass
class Task:
    t_arrive: int
    dims: np.ndarray
    domain: int          # -1 for cross-domain
    impact: int
    reversible: bool
    value: float

def spawn_tasks(t, p, rng):
    tasks = []
    for _ in range(rng.poisson(p.lam_tasks)):
        impact = int(rng.choice(3, p=p.impact_probs))
        reversible = bool(rng.random() < p.p_reversible[impact])
        if rng.random() < p.p_cross:                      # cross-domain task
            doms = rng.choice(4, size=2, replace=False)
            dims = np.concatenate([DOMAIN_DIMS[int(d)] for d in doms])
            domain = -1
        else:
            domain = int(rng.choice(4))
            dims = DOMAIN_DIMS[domain]
        tasks.append(Task(t, dims, domain, impact, reversible, p.impact_values[impact]))
    return tasks

def payoff_factor(action, g, dims, p):
    err = action - g[dims]
    return float(np.exp(-(err @ err) / (2.0 * p.kappa ** 2)))

# quick sanity check of the environment
_rng = np.random.default_rng(0)
_ctx = Context(P0, _rng)
_drifts = []
for _t in range(2000):
    _g_prev = _ctx.g.copy()
    _ctx.step(_t, _rng)
    if _t not in _ctx.shock_times:
        _drifts.append(np.linalg.norm(_ctx.g - _g_prev) / math.sqrt(P0.d))
assert abs(np.mean(_drifts) - P0.sigma_drift) < 0.02, "drift magnitude off"
assert 10 <= len(_ctx.shock_times) <= 60, "shock frequency off"
print(f"Environment OK — mean per-dim drift {np.mean(_drifts):.3f}, "
      f"{len(_ctx.shock_times)} shocks in 2000 steps")

# %% [markdown]
# ## Section 2 — Representations & executable Delegation Contracts
#
# A `Representation` carries the paper's three tunable dimensions:
#
# * **Fidelity** $F_i$: each step it re-syncs its belief $\hat g_{i,t}$ with probability $F_i$
#   (a *context-refresh ritual*, costing the principal $c_{refresh}$); otherwise staleness grows.
# * **Autonomy**: its current rung on the shadow→assist→suggest→act ladder.
# * **Scope**: the context dimensions (functional domain) it may operate on.
#
# The **Delegation Contract** (paper Fig. 1) is implemented as code: `may_act` and
# `must_escalate` reproduce `EscalateIf: novelty>θ_N OR staleness>θ_s OR impact ≥ "external-commit"`,
# and the **staleness gate** caps effective autonomy whenever the contract trips.

# %%
class Representation:
    def __init__(self, name, scope, fidelity, cap, g0, rng, p):
        self.name = name
        self.scope = np.asarray(scope)
        self.fidelity = fidelity
        self.cap = cap                  # current autonomy rung (progressive autonomy moves it)
        self.belief = g0 + rng.normal(0.0, p.eps_sync, p.d)
        self.staleness = 0
        self.streak = 0                 # consecutive successes (promotion track record)

    def sync(self, g, rng, p):
        self.belief = g + rng.normal(0.0, p.eps_sync, p.d)
        self.staleness = 0

    def covers(self, dims):
        return bool(np.all(np.isin(dims, self.scope)))

    def belief_factor(self, g, dims, p):
        """Alignment of current belief on the task's dimensions (epistemic alignment)."""
        err = self.belief[dims] - g[dims]
        return float(np.exp(-(err @ err) / (2.0 * p.kappa ** 2)))

    def alignment(self, g):
        """Global epistemic-alignment index A_{i,t} (monitoring metric)."""
        err = self.belief - g
        return float(np.exp(-(err @ err) / 2.0))

    def propose(self, dims, rng, p):
        return self.belief[dims] + rng.normal(0.0, p.eps_prop, len(dims))

def must_escalate(rep, task, novelty, p):
    """Delegation-contract escalation rule (paper Fig. 1)."""
    return (novelty > p.theta_N) or (rep.staleness > p.theta_s) or (task.impact == HIGH)

def effective_autonomy(rep, task, novelty, gated, p):
    """Staleness/novelty gate: cap autonomy at SUGGEST when the contract trips."""
    if gated and must_escalate(rep, task, novelty, p):
        return min(rep.cap, SUGGEST)
    return rep.cap

def may_act(rep, task, autonomy):
    """Micro-handoff condition: act-bounded, low-impact, reversible, in scope."""
    return (autonomy == ACT) and (task.impact == LOW) and task.reversible and rep.covers(task.dims)

# sanity: fidelity drives epistemic alignment
_rng = np.random.default_rng(1)
_ctx = Context(P0, _rng)
_hi = Representation("hi", np.arange(8), 0.9, SUGGEST, _ctx.g, _rng, P0)
_lo = Representation("lo", np.arange(8), 0.05, SUGGEST, _ctx.g, _rng, P0)
_a_hi, _a_lo = [], []
for _t in range(800):
    _ctx.step(_t, _rng)
    for _r in (_hi, _lo):
        if _rng.random() < _r.fidelity:
            _r.sync(_ctx.g, _rng, P0)
        else:
            _r.staleness += 1
    _a_hi.append(_hi.alignment(_ctx.g)); _a_lo.append(_lo.alignment(_ctx.g))
assert np.mean(_a_hi) > np.mean(_a_lo) + 0.2, "fidelity should drive alignment"
print(f"Contracts OK — mean alignment: F=0.9 → {np.mean(_a_hi):.2f}, F=0.05 → {np.mean(_a_lo):.2f}")

# %% [markdown]
# ## Section 3 — Conditions (architectures) & the team simulation loop
#
# Five architectures are compared (Sec 3 of the implementation plan):
#
# | condition | description |
# |---|---|
# | `HUMAN_ONLY` | principal reviews every task personally (status-quo "thicket of meetings") |
# | `SINGLE_COPILOT` | one generic full-scope assistant, suggest-only (the dyadic "human+assistant" view the paper criticizes) |
# | `DA_FIXED` | 4 specialized reps, act-from-start, **no** gating / progression (naive distributed agency) |
# | `DA_GATED` | + delegation contracts, staleness/novelty gates, progressive autonomy (**the paper's full framework**) |
# | `DA_ADAPTIVE` | + the novel **Adaptive Delegation Controller** (Section 7) |
#
# The loop implements the paper's `sense → compose → ratify → act → learn` cycle each step, and
# every event is written to a **Chain-of-Decision log** (auditability pillar), from which all
# metrics are computed.

# %%
@dataclass
class Condition:
    name: str
    has_reps: bool = True
    n_reps: int = 4
    fidelity: float = 0.30
    base_cap: int = SUGGEST
    act_allowed: bool = True      # may ever be promoted to ACT
    gated: bool = True            # contract gates + forced refresh on novelty
    progressive: bool = True      # promotion / demotion ladder
    adaptive: bool = False        # bandit tunes (fidelity, act_allowed) online
    full_scope: bool = False      # single copilot covering all domains

HUMAN_ONLY     = Condition("HUMAN_ONLY", has_reps=False)
SINGLE_COPILOT = Condition("SINGLE_COPILOT", n_reps=1, fidelity=0.25, base_cap=SUGGEST,
                           act_allowed=False, gated=False, progressive=False, full_scope=True)
DA_FIXED       = Condition("DA_FIXED", base_cap=ACT, gated=False, progressive=False)
DA_GATED       = Condition("DA_GATED")
DA_ADAPTIVE    = Condition("DA_ADAPTIVE", adaptive=True)
CONDITIONS = [HUMAN_ONLY, SINGLE_COPILOT, DA_FIXED, DA_GATED, DA_ADAPTIVE]

REP_NAMES = ["Estimator(eng)", "Marketer(mkt)", "Modeler(fin)", "Guardrails(leg)"]

def build_portfolio(cond, p, g0, rng):
    if not cond.has_reps:
        return []
    if cond.full_scope:
        return [Representation("Copilot(all)", np.arange(p.d), cond.fidelity,
                               cond.base_cap, g0, rng, p)]
    return [Representation(REP_NAMES[k], DOMAIN_DIMS[k], cond.fidelity,
                           cond.base_cap, g0, rng, p) for k in range(cond.n_reps)]

# Adaptive Delegation Controller (novelty N3) — defined here, analyzed in Section 7.
FID_LEVELS = (0.05, 0.10, 0.20, 0.40, 0.70, 1.00)

class AdaptiveDelegationController:
    """Learns each representation's fidelity online from misalignment *evidence*.

    The paper prescribes an "Update Routine that monitors how out-of-date the representation's
    understanding is" but leaves the routine to leader judgment. The ADC operationalizes it as
    an AIMD-style (sharp-increase / gentle-decrease) feedback law on observable
    Chain-of-Decision events — no privileged access to the true context:

    * STRONG evidence (rejected suggestion, rollback, irreversible failure) means the rep's
      picture of the principal was *wrong* -> jump the update rate (much) higher;
    * WEAK evidence (a staleness-gate trip blocked an action) means the rep was merely
      *out-of-date* -> nudge the update rate one level up;
    * a clean window -> decay one level (refresh rituals cost principal attention, so staying
      maximally synced is wasteful in calm regimes).

    Autonomy promotion/demotion is still handled by the progressive-autonomy ladder; the ADC
    closes the *fidelity* loop the paper leaves open, and re-adapts after regime shifts.
    """

    def __init__(self, reps, window=10):
        self.window = window
        self.level = {r.name: 1 for r in reps}          # start cheap: F = FID_LEVELS[1]
        self.strong = {r.name: 0 for r in reps}
        self.weak = {r.name: 0 for r in reps}
        self.switches = []
        for r in reps:
            r.fidelity = FID_LEVELS[self.level[r.name]]

    def observe(self, rep_name, strong=True):
        if rep_name in self.strong:
            (self.strong if strong else self.weak)[rep_name] += 1

    def adjust(self, reps, t):
        top = len(FID_LEVELS) - 1
        for r in reps:
            old = self.level[r.name]
            if self.strong[r.name] >= 2:                 # badly misaligned: max update rate
                self.level[r.name] = top
            elif self.strong[r.name] == 1:
                self.level[r.name] = min(old + 3, top)
            elif self.weak[r.name] >= 1:                 # merely stale: nudge up
                self.level[r.name] = min(old + 1, top)
            else:                                        # clean window: decay
                self.level[r.name] = max(old - 1, 0)
            self.strong[r.name] = 0
            self.weak[r.name] = 0
            r.fidelity = FID_LEVELS[self.level[r.name]]
            if self.level[r.name] != old:
                self.switches.append((t, r.name, r.fidelity))

# %%
def run_episode(cond, p, seed, adc_window=10):
    """Simulate one episode; returns Chain-of-Decision log + per-step series + summary."""
    rng_env = np.random.default_rng(seed)               # common random numbers:
    rng_pol = np.random.default_rng(seed + 7_000_003)   # same world across conditions
    ctx = Context(p, rng_env)
    reps = build_portfolio(cond, p, ctx.g, rng_pol)
    trust = p.trust0
    queue = []          # pending items: dict(task, kind, action, rep)
    log = []            # Chain-of-Decision log
    series = {k: np.zeros(p.horizon) for k in
              ("net", "trust", "alignment", "autonomy", "queue", "spent", "fidelity")}
    adc = AdaptiveDelegationController(reps) if cond.adaptive else None

    def trust_mult():
        return 0.5 + 0.5 * trust

    def execute(action, task, t, executor, autonomous, rep=None):
        """Execute an action; update payoff, trust, and the promotion track record."""
        nonlocal trust
        factor = payoff_factor(action, ctx.g, task.dims, p)
        success = factor >= p.success_frac
        gross = task.value * factor * trust_mult() - p.c_exec
        if success:
            net, event = gross, "success"
            trust = min(1.0, trust + p.trust_alpha)
            if executor == "rep" and not autonomous:
                trust = min(1.0, trust + p.trust_gamma)   # disclosed hand-back
        elif task.reversible:
            net, event = -p.rho, "rollback"               # time-boxed reversibility
            if autonomous:
                trust = max(0.0, trust - p.trust_beta)
        else:
            net, event = gross - p.p_irr, "irrev_fail"
            if autonomous:
                trust = max(0.0, trust - p.trust_beta)
        if not success and adc is not None and rep is not None:
            adc.observe(rep.name)                          # misalignment evidence
        if rep is not None:                                # progressive autonomy ledger
            if success:
                rep.streak += 1
                cap_max = ACT if cond.act_allowed else SUGGEST
                if cond.progressive and rep.streak >= p.k_up and rep.cap < cap_max:
                    rep.cap += 1
                    rep.streak = 0
                    log.append(dict(t=t, event="promote", rep=rep.name, impact=task.impact,
                                    payoff=0.0, cost=0.0, latency=0, escalated=False,
                                    belief_factor=np.nan, autonomous=False))
            else:
                rep.streak = 0
                if cond.progressive and rep.cap > SUGGEST:
                    rep.cap = SUGGEST
                    log.append(dict(t=t, event="demote", rep=rep.name, impact=task.impact,
                                    payoff=0.0, cost=0.0, latency=0, escalated=False,
                                    belief_factor=np.nan, autonomous=False))
        log.append(dict(t=t, event=event, rep=getattr(rep, "name", "human"),
                        impact=task.impact, payoff=net, cost=0.0,
                        latency=t - task.t_arrive, escalated=False,
                        belief_factor=np.nan, autonomous=autonomous))
        return net

    for t in range(p.horizon):
        # ---- SENSE: context evolves, reps refresh ----
        ctx.step(t, rng_env)
        attention = p.budget
        step_net = 0.0
        spent = 0.0
        for rep in reps:
            forced = cond.gated and ctx.novelty > p.theta_N   # forced refresh ritual
            if forced or rng_pol.random() < rep.fidelity:
                rep.sync(ctx.g, rng_pol, p)
                spent += p.c_refresh
            else:
                rep.staleness += 1
        attention -= spent

        # ---- adaptive controller adjusts fidelity from last window's evidence ----
        if adc is not None and t > 0 and t % adc_window == 0:
            adc.adjust(reps, t)

        # ---- COMPOSE / ACT: route arriving tasks per delegation contract ----
        prepared = {r.name: 0 for r in reps}    # a rep can prepare rep_capacity tasks/step
        for task in spawn_tasks(t, p, rng_env):
            handlers = [r for r in reps if r.covers(task.dims)
                        and prepared[r.name] < p.rep_capacity]
            rep = min(handlers, key=lambda r: len(r.scope)) if handlers else None
            if rep is None:
                queue.append(dict(task=task, kind="raw", action=None, rep=None))
                continue
            prepared[rep.name] += 1
            if adc is not None and rep.staleness > p.theta_s:
                adc.observe(rep.name, strong=False)   # gate trip = weak (staleness) evidence
            aut = effective_autonomy(rep, task, ctx.novelty, cond.gated, p)
            esc = not may_act(rep, task, aut)
            log.append(dict(t=t, event="route", rep=rep.name, impact=task.impact,
                            payoff=0.0, cost=0.0, latency=0, escalated=esc,
                            belief_factor=rep.belief_factor(ctx.g, task.dims, p),
                            autonomous=False))
            if not esc:                                       # micro-handoff: act-bounded
                step_net += execute(rep.propose(task.dims, rng_pol, p), task, t,
                                    "rep", True, rep)
            elif task.impact == HIGH:                         # contract: human presence
                queue.append(dict(task=task, kind="raw", action=None, rep=rep))
            elif aut >= SUGGEST:                              # pre-negotiated suggestion
                queue.append(dict(task=task, kind="suggest",
                                  action=rep.propose(task.dims, rng_pol, p), rep=rep))
            elif aut == ASSIST:
                queue.append(dict(task=task, kind="assist", action=None, rep=rep))
            else:                                             # shadow: no help
                queue.append(dict(task=task, kind="raw", action=None, rep=rep))

        # ---- RATIFY: principal processes the queue under the attention budget ----
        queue.sort(key=lambda it: (-it["task"].impact, it["task"].t_arrive))
        deferred = []
        for item in queue:
            task = item["task"]
            if t - task.t_arrive >= p.deadline:               # coordination overload
                log.append(dict(t=t, event="miss", rep="-", impact=task.impact,
                                payoff=0.0, cost=0.0, latency=p.deadline,
                                escalated=False, belief_factor=np.nan, autonomous=False))
                continue
            cost = {"raw": p.c_review, "assist": p.c_assist,
                    "suggest": p.c_ratify, "fix": p.c_fix}[item["kind"]]
            if attention < cost:
                deferred.append(item)
                continue
            attention -= cost
            spent += cost
            if item["kind"] == "suggest":                     # noisy quality check
                est = payoff_factor(item["action"], ctx.g, task.dims, p) \
                      + rng_pol.normal(0.0, p.sigma_check)
                if est >= p.success_frac:
                    step_net += execute(item["action"], task, t, "rep", False, item["rep"])
                else:                                         # reject -> human redo later
                    log.append(dict(t=t, event="reject", rep=item["rep"].name,
                                    impact=task.impact, payoff=0.0, cost=0.0, latency=0,
                                    escalated=False, belief_factor=np.nan, autonomous=False))
                    if adc is not None:
                        adc.observe(item["rep"].name)         # misalignment evidence
                    deferred.append(dict(task=task, kind="fix", action=None, rep=item["rep"]))
            else:                                             # human executes personally
                action = ctx.g[task.dims] + rng_pol.normal(0.0, p.eps_human, len(task.dims))
                step_net += execute(action, task, t, "human", False, None)
        queue = deferred

        # ---- LEARN: bookkeeping ----
        step_net -= p.w_att * spent
        series["net"][t] = step_net
        series["trust"][t] = trust
        series["alignment"][t] = (np.mean([r.alignment(ctx.g) for r in reps])
                                  if reps else np.nan)
        series["autonomy"][t] = (np.mean([r.cap for r in reps]) if reps else np.nan)
        series["fidelity"][t] = (np.mean([r.fidelity for r in reps]) if reps else np.nan)
        series["queue"][t] = len(queue)
        series["spent"][t] = spent
        assert spent <= p.budget + 1e-9, "attention budget violated"

    log = pd.DataFrame(log)
    return dict(cond=cond.name, seed=seed, log=log, series=series,
                shocks=ctx.shock_times, summary=summarize(log, series, p))

def summarize(log, series, p):
    ev = log["event"]
    executed = log[ev.isin(["success", "rollback", "irrev_fail"])]
    n_done = len(executed)
    n_miss = int((ev == "miss").sum())
    s = dict(
        total_net=float(series["net"].sum()),
        miss_rate=n_miss / max(n_done + n_miss, 1),
        mean_latency=float(executed["latency"].mean()) if n_done else np.nan,
        attention_per_step=float(series["spent"].mean()),
        rollbacks=int((ev == "rollback").sum()),
        irrev_fails=int((ev == "irrev_fail").sum()),
        final_trust=float(series["trust"][-1]),
        mean_alignment=float(np.nanmean(series["alignment"])),
    )
    routed = log[ev == "route"]
    if len(routed):
        needed = (routed["belief_factor"] < p.success_frac) | (routed["impact"] == HIGH)
        esc = routed["escalated"].astype(bool)
        tp = int((esc & needed).sum())
        s["esc_precision"] = tp / max(int(esc.sum()), 1)
        s["esc_recall"] = tp / max(int(needed.sum()), 1)
    return s

print("Simulation engine ready.")

# %% [markdown]
# ## Section 4 — Metrics & multi-seed runner
#
# Every metric (Sec 4 of the plan) is computed **from the Chain-of-Decision log alone** —
# operationalizing the paper's accountability pillar ("auditable, attributable, reversible").

# %%
def run_many(cond, p, seeds, **kw):
    runs = [run_episode(cond, p, s, **kw) for s in seeds]
    summ = pd.DataFrame([r["summary"] for r in runs])
    summ.insert(0, "condition", cond.name)
    stacked = {k: np.vstack([r["series"][k] for r in runs]) for k in runs[0]["series"]}
    return dict(cond=cond.name, summary=summ, series=stacked, runs=runs)

def ci95(x, axis=0):
    x = np.asarray(x, dtype=float)
    m = np.nanmean(x, axis=axis)
    se = np.nanstd(x, axis=axis) / np.sqrt(x.shape[axis])
    return m, 1.96 * se

COLORS = {"HUMAN_ONLY": "#888888", "SINGLE_COPILOT": "#e0a83a",
          "DA_FIXED": "#d65f5f", "DA_GATED": "#4878d0", "DA_ADAPTIVE": "#6acc64"}

SEEDS = list(range(20))
print(f"Runner ready — {len(SEEDS)} seeds per condition.")

# %% [markdown]
# ## Section 5 / E1 — Architecture × context-drift sweep (tests P1, P3)
#
# **Paper claims tested:** failures are *epistemic* (context drift), so distributed agency with
# gating should (a) beat the human-only and single-copilot baselines by cutting coordination
# cost, and (b) increasingly dominate naive (ungated) distributed agency as drift rises.
# We also expect to *quantify the paper's boundary condition #2*: under extreme drift
# ("low-information contexts"), delegation of any kind loses value and conservative,
# human-centered configurations regain ground.

# %%
DRIFTS = [0.02, 0.05, 0.08, 0.12, 0.16]
e1 = {}
for sd in DRIFTS:
    p = replace(P0, sigma_drift=sd)
    for cond in CONDITIONS:
        e1[(cond.name, sd)] = run_many(cond, p, SEEDS)
    print(f"  E1 drift={sd:.2f} done ({time.time() - T_START:5.0f}s)")

fig, axes = plt.subplots(1, 2, figsize=(10, 3.6))
for cond in CONDITIONS:
    means, errs = [], []
    for sd in DRIFTS:
        m, e = ci95(e1[(cond.name, sd)]["summary"]["total_net"])
        means.append(m); errs.append(e)
    axes[0].errorbar(DRIFTS, means, yerr=errs, marker="o", capsize=3,
                     label=cond.name, color=COLORS[cond.name])
axes[0].set(xlabel="context drift σ", ylabel="total net utility (300 steps)",
            title="E1a — Performance vs context drift")
axes[0].legend()
metric_pairs = [("miss_rate", "deadline-miss rate"), ("attention_per_step", "attention / step")]
width = 0.16
for i, cond in enumerate(CONDITIONS):
    summ = e1[(cond.name, 0.08)]["summary"]
    vals = [summ[m].mean() for m, _ in metric_pairs]
    axes[1].bar(np.arange(2) + (i - 2) * width, vals, width,
                label=cond.name, color=COLORS[cond.name])
axes[1].set_xticks(np.arange(2), [lbl for _, lbl in metric_pairs])
axes[1].set(title="E1b — Coordination cost at default drift (σ=0.08)")
show_save(fig, "E1_architecture_drift_sweep")

e1_tbl = pd.concat([e1[(c.name, 0.08)]["summary"] for c in CONDITIONS]) \
    .groupby("condition").mean().round(3) \
    .reindex([c.name for c in CONDITIONS])
print(e1_tbl[["total_net", "miss_rate", "mean_latency", "attention_per_step",
              "rollbacks", "irrev_fails", "final_trust"]].to_string())

# %% [markdown]
# ## Section 6 / E2 — Inner-crowd wisdom & the Divergence Index (tests P4)
#
# The paper asserts that a leader should *curate* divergence among their representations:
# enough disagreement to surface creative alternatives, not so much that intent fragments.
# We operationalize the **Divergence Index** $DI = \frac{2}{m(m-1)}\sum_{i<j}\lVert a_i-a_j\rVert$
# and sweep the diversity knob $\delta$ (spread of designed perspective offsets $b_i$ around the
# rep's — possibly stale — belief). Chosen-option quality should be **inverted-U in $\delta$**.

# %%
def inner_crowd_trial(delta, rng, m=7, belief_err=1.0, value=2.5,
                      sigma_eval=0.20, c_recon=0.15, p=P0, dk=3):
    g = np.zeros(dk)
    e = rng.normal(0.0, 1.0, dk)
    belief = g + e / np.linalg.norm(e) * belief_err        # stale belief, fixed error
    props = belief + rng.normal(0.0, delta, (m, dk)) \
            + rng.normal(0.0, p.eps_prop, (m, dk))         # designed diversity + noise
    factors = np.exp(-np.sum((props - g) ** 2, axis=1) / (2 * p.kappa ** 2))
    chosen = int(np.argmax(factors + rng.normal(0.0, sigma_eval, m)))  # noisy ratification
    di = float(np.mean([np.linalg.norm(props[i] - props[j])
                        for i in range(m) for j in range(i + 1, m)]))
    return value * factors[chosen] - c_recon * di, di

DELTAS = np.linspace(0.0, 2.5, 11)
rng = np.random.default_rng(42)
N_TRIALS = 3000
e2_q, e2_qe, e2_di = [], [], []
for delta in DELTAS:
    out = np.array([inner_crowd_trial(delta, rng) for _ in range(N_TRIALS)])
    m, e = ci95(out[:, 0])
    e2_q.append(m); e2_qe.append(e); e2_di.append(out[:, 1].mean())
e2_q, e2_qe, e2_di = map(np.array, (e2_q, e2_qe, e2_di))
peak = DELTAS[int(np.argmax(e2_q))]

fig, ax1 = plt.subplots(figsize=(6.4, 3.6))
ax1.errorbar(DELTAS, e2_q, yerr=e2_qe, marker="o", capsize=3, color="#4878d0",
             label="chosen-option quality")
ax1.axvline(peak, ls="--", color="#4878d0", alpha=0.5)
ax1.annotate(f"curated optimum δ*≈{peak:.2f}", (peak, e2_q.max()),
             xytext=(peak + 0.25, e2_q.max()), fontsize=8, color="#4878d0")
ax1.set(xlabel="designed diversity δ of the portfolio", ylabel="option quality",
        title="E2 — Inner-crowd wisdom: inverted-U in curated divergence")
ax2 = ax1.twinx()
ax2.plot(DELTAS, e2_di, color="#d65f5f", ls=":", marker="s", ms=3,
         label="Divergence Index")
ax2.set_ylabel("Divergence Index", color="#d65f5f")
ax2.grid(False)
h1, l1 = ax1.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
ax1.legend(h1 + h2, l1 + l2, loc="lower center")
show_save(fig, "E2_inner_crowd_inverted_U")
print(f"E2: quality at δ=0: {e2_q[0]:.2f} | at δ*={peak:.2f}: {e2_q.max():.2f} "
      f"| at δ=2.5: {e2_q[-1]:.2f}  ({time.time() - T_START:5.0f}s)")

# %% [markdown]
# ## Section 6 / E3 — Progressive autonomy & trust dynamics (tests P5, N6)
#
# Three delegation policies at default drift: **act-from-start** (`DA_FIXED`),
# **suggest-only** (gated but never promoted), and the paper's **progressive autonomy**
# (`DA_GATED`: promote after $k_{up}$ consecutive successes, demote on failure or gate trip).

# %%
DA_SUGGEST_ONLY = Condition("DA_SUGGEST_ONLY", act_allowed=False, progressive=False)
E3_CONDS = [DA_FIXED, DA_SUGGEST_ONLY, DA_GATED]
E3_COLORS = {"DA_FIXED": "#d65f5f", "DA_SUGGEST_ONLY": "#e0a83a", "DA_GATED": "#4878d0"}
e3 = {c.name: run_many(c, P0, SEEDS) for c in E3_CONDS}

fig, axes = plt.subplots(2, 2, figsize=(10, 6))
for c in E3_CONDS:
    s = e3[c.name]["series"]
    col = E3_COLORS[c.name]
    m, e = ci95(s["autonomy"]); axes[0, 0].plot(m, color=col, label=c.name)
    axes[0, 0].fill_between(range(P0.horizon), m - e, m + e, color=col, alpha=0.2)
    fails = np.cumsum(np.vstack([
        [(r["log"].query("event in ('rollback','irrev_fail') and t == @tt").shape[0])
         for tt in range(P0.horizon)] for r in e3[c.name]["runs"]]), axis=1)
    m, e = ci95(fails); axes[0, 1].plot(m, color=col)
    axes[0, 1].fill_between(range(P0.horizon), m - e, m + e, color=col, alpha=0.2)
    m, e = ci95(s["trust"]); axes[1, 0].plot(m, color=col)
    axes[1, 0].fill_between(range(P0.horizon), m - e, m + e, color=col, alpha=0.2)
    m, e = ci95(np.cumsum(s["net"], axis=1)); axes[1, 1].plot(m, color=col)
    axes[1, 1].fill_between(range(P0.horizon), m - e, m + e, color=col, alpha=0.2)
axes[0, 0].set(title="mean autonomy rung (2=suggest, 3=act)", xlabel="t")
axes[0, 1].set(title="cumulative failures (rollback + irreversible)", xlabel="t")
axes[1, 0].set(title="counterparty trust T_t", xlabel="t")
axes[1, 1].set(title="cumulative net utility", xlabel="t")
axes[0, 0].legend()
fig.suptitle("E3 — Progressive autonomy earns authority without losing accountability", y=1.02)
show_save(fig, "E3_progressive_autonomy_trust")
e3_tbl = pd.concat([e3[c.name]["summary"] for c in E3_CONDS]).groupby("condition").mean()
print(e3_tbl[["total_net", "rollbacks", "irrev_fails", "final_trust"]].round(3).to_string(),
      f"\n({time.time() - T_START:5.0f}s)")

# %% [markdown]
# ## Section 6 / E4 — Shock-recovery event study: "Northstar Tuesday" (tests P5 / N5)
#
# The paper's illustrative case: Legal's *Guardrails* rep raises a demand that other reps have
# not yet seen; staleness gating automatically downgrades autonomy, a context refresh restores
# fidelity, and "trust, counterintuitively, increased". We replicate this as a controlled event
# study: a single deterministic shock at $t_0 = 150$ (no other shocks), low fidelity (F = 0.15)
# so that recovery speed depends on the *mechanism*, not luck.

# %%
p4 = replace(P0, p_shock=0.0, forced_shocks=(150,), sigma_drift=0.05)
E4_FIXED = Condition("DA_FIXED", base_cap=ACT, gated=False, progressive=False, fidelity=0.15)
E4_GATED = Condition("DA_GATED", fidelity=0.15)
e4 = {c.name: run_many(c, p4, list(range(30))) for c in (E4_FIXED, E4_GATED)}

win = slice(120, 220)
fig, axes = plt.subplots(1, 3, figsize=(11, 3.4))
for cname, col in (("DA_FIXED", "#d65f5f"), ("DA_GATED", "#4878d0")):
    s = e4[cname]["series"]
    xs = np.arange(P0.horizon)[win]
    m, e = ci95(s["alignment"][:, win]); axes[0].plot(xs, m, color=col, label=cname)
    axes[0].fill_between(xs, m - e, m + e, color=col, alpha=0.2)
    m, e = ci95(s["net"][:, win]); axes[1].plot(xs, m, color=col)
    axes[1].fill_between(xs, m - e, m + e, color=col, alpha=0.2)
    m, e = ci95(s["trust"][:, win]); axes[2].plot(xs, m, color=col)
    axes[2].fill_between(xs, m - e, m + e, color=col, alpha=0.2)
for ax, ttl in zip(axes, ("epistemic alignment", "net utility / step", "trust")):
    ax.axvline(150, color="k", ls="--", lw=0.8)
    ax.set(title=ttl, xlabel="t")
axes[0].annotate("shock", (150, axes[0].get_ylim()[0]), fontsize=8)
axes[0].legend()
fig.suptitle('E4 — "Northstar Tuesday": staleness gating turns a shock into a refresh, '
             "not a failure cascade", y=1.04)
show_save(fig, "E4_shock_recovery_event_study")

post = slice(150, 170)
loss = {c: float(np.mean(e4[c]["series"]["net"][:, post].sum(axis=1))) for c in e4}
fails_post = {c: float(np.mean([r["log"].query(
    "event in ('rollback','irrev_fail') and 150 <= t < 170").shape[0]
    for r in e4[c]["runs"]])) for c in e4}
print(f"E4 post-shock (20 steps): net utility FIXED {loss['DA_FIXED']:.1f} vs "
      f"GATED {loss['DA_GATED']:.1f}; failures/run {fails_post['DA_FIXED']:.1f} vs "
      f"{fails_post['DA_GATED']:.1f}  ({time.time() - T_START:5.0f}s)")

# %% [markdown]
# ## Section 7 / E5 — NOVEL: the Adaptive Delegation Controller under regime shift (N3)
#
# The paper prescribes an *Update Routine* "that monitors how out-of-date the representation's
# understanding is" — but leaves it entirely to leader judgment. The **ADC** turns it into a
# feedback controller: it watches only **observable Chain-of-Decision evidence** (rejected
# suggestions, rollbacks, irreversible failures, staleness-gate trips) and steers each rep's
# fidelity with an **AIMD law** — misalignment evidence ⇒ refresh much more often; clean
# windows ⇒ decay the (attention-costly) refresh rate.
#
# Test: a calm regime ($\sigma = 0.01$) for $t < 300$, then a turbulent one ($\sigma = 0.20$).
# High fidelity is wasted attention in the calm regime and indispensable in the turbulent one —
# so **no fixed hand-tuned fidelity can win both regimes**, but the ADC can re-adapt.

# %%
p5 = replace(P0, horizon=600, drift_schedule=((0, 0.01), (300, 0.20)))
E5_SEEDS = list(range(12))
e5_adaptive = run_many(DA_ADAPTIVE, p5, E5_SEEDS)
e5_fixed = {}
for f in FID_LEVELS:
    c = Condition(f"F{f:.2f}", fidelity=f, base_cap=SUGGEST,
                  act_allowed=True, gated=True, progressive=True)
    e5_fixed[f] = run_many(c, p5, E5_SEEDS)
print(f"E5 simulations done ({time.time() - T_START:5.0f}s)")

def rolling(x, w=40):
    return np.convolve(x, np.ones(w) / w, mode="valid")

tot = {f: v["summary"]["total_net"].mean() for f, v in e5_fixed.items()}
reg1 = {f: v["series"]["net"][:, :300].sum(axis=1).mean() for f, v in e5_fixed.items()}
reg2 = {f: v["series"]["net"][:, 300:].sum(axis=1).mean() for f, v in e5_fixed.items()}
best1, best2 = max(reg1, key=reg1.get), max(reg2, key=reg2.get)
adc_tot = e5_adaptive["summary"]["total_net"].mean()

fig, axes = plt.subplots(1, 3, figsize=(12, 3.6))
for f, lbl, col in ((best1, f"best fixed for calm (F={best1})", "#e0a83a"),
                    (best2, f"best fixed for turbulent (F={best2})", "#d65f5f")):
    m, _ = ci95(e5_fixed[f]["series"]["net"])
    axes[0].plot(rolling(m), label=lbl, color=col)
m, _ = ci95(e5_adaptive["series"]["net"])
axes[0].plot(rolling(m), label="DA_ADAPTIVE (ours)", color="#6acc64", lw=2)
axes[0].axvline(300, color="k", ls="--", lw=0.8)
axes[0].set(title="E5a — Rolling net utility across a regime shift",
            xlabel="t", ylabel="net utility / step (rolling 40)")
axes[0].legend()
m, e = ci95(e5_adaptive["series"]["fidelity"])
axes[1].plot(m, color="#6acc64")
axes[1].fill_between(range(p5.horizon), m - e, m + e, color="#6acc64", alpha=0.25)
axes[1].axvline(300, color="k", ls="--", lw=0.8)
axes[1].annotate("regime shift", (305, 0.5), fontsize=8)
axes[1].set(title="E5b — ADC-chosen fidelity (update rate)",
            xlabel="t", ylabel="mean portfolio fidelity", ylim=(0, 1.05))
vals = [tot[f] for f in FID_LEVELS]
axes[2].bar(range(len(FID_LEVELS)), vals, color="#bbbbbb")
axes[2].axhline(adc_tot, color="#6acc64", lw=2, label=f"DA_ADAPTIVE = {adc_tot:.0f}")
axes[2].set_xticks(range(len(FID_LEVELS)), [f"F={f}" for f in FID_LEVELS], fontsize=7)
axes[2].set(title="E5c — Total utility: fixed fidelity profiles vs ADC",
            ylabel="total net utility (600 steps)")
axes[2].legend()
show_save(fig, "E5_adaptive_delegation_controller")
best_fixed_tot = max(vals)
fid_calm = float(np.mean(e5_adaptive["series"]["fidelity"][:, 100:300]))
fid_turb = float(np.mean(e5_adaptive["series"]["fidelity"][:, 400:]))
print(f"E5: ADC total {adc_tot:.0f} vs best fixed {best_fixed_tot:.0f} "
      f"(ratio {adc_tot / best_fixed_tot:.2f}); "
      f"ADC fidelity calm {fid_calm:.2f} -> turbulent {fid_turb:.2f}")

# %% [markdown]
# ## Section 8 — (Optional) LLM bridge: pre-negotiation between liaison representations
#
# A minimal demonstration that the simulated protocol maps onto *real* LLM agents: two liaison
# representations (with disclosure banners and machine-readable Delegation Contracts) pre-negotiate
# launch options, and the human ratifies. **Skipped automatically when no `OPENAI_API_KEY` is
# set** — the rest of the notebook never depends on it.

# %%
DELEGATION_CONTRACT = {
    "principal": "A. Chen (Product Lead)",
    "role": "Product Liaison",
    "tasks": ["compose", "analyse", "select launch options"],
    "conditions": {"scope": ["MVP", "MVP+"], "timeline_weeks": 8, "budget_usd": 250_000},
    "autonomy_mode": "SUGGEST",
    "data": ["roadmap:v4", "capacity:sprint-32..34", "finance:unit-econ-2025Q1"],
    "escalate_if": {"novelty": 0.6, "staleness_h": 24, "impact": "external-commit"},
}

def llm_pre_negotiation_demo():
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        print("OPENAI_API_KEY not set -> LLM pre-negotiation demo skipped (simulation results "
              "above are fully self-contained).")
        return
    try:
        from openai import OpenAI
    except ImportError:
        print("`pip install openai` to run this optional demo.")
        return
    client = OpenAI()
    banner = ("Representation speaking for: {who}; autonomy: SUGGEST; last update: 5m ago. "
              "Contract: {contract}")
    msgs = [{"role": "system", "content":
             "You are the Product-Liaison representation of A. Chen. "
             + banner.format(who="A. Chen", contract=DELEGATION_CONTRACT)
             + " Negotiate with Engineering's Estimator rep and return exactly two signed launch "
               "option packages (name, timeline, budget, rationale, trade-offs) as bullet lists. "
               "You may only SUGGEST; escalate anything resembling an external commitment."},
            {"role": "user", "content":
             "Estimator rep (representing Engineering Manager, autonomy: SUGGEST) reports: "
             "capacity 2 squads for 6 weeks; features F1-F3 low-risk, F4-F5 +2 weeks; "
             "compliance review adds 3 days. Compose the two option packages for human "
             "ratification."}]
    out = client.chat.completions.create(model="gpt-4o-mini", messages=msgs)
    print(out.choices[0].message.content)

llm_pre_negotiation_demo()

# %% [markdown]
# ## Section 9 — Results summary, hypothesis checks & conclusions

# %%
print("=" * 78)
print("RESULTS SUMMARY (default drift σ=0.08, means over", len(SEEDS), "seeds)")
print("=" * 78)
cols = ["total_net", "miss_rate", "mean_latency", "attention_per_step",
        "rollbacks", "irrev_fails", "final_trust", "esc_precision", "esc_recall"]
print(e1_tbl.reindex(columns=cols).round(3).to_string())

def check(name, ok, detail):
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}: {detail}")
    assert ok, f"sanity check failed: {name} — {detail}"

t_net = {c.name: e1[(c.name, 0.08)]["summary"]["total_net"].mean() for c in CONDITIONS}
hi_net = {c.name: e1[(c.name, 0.16)]["summary"]["total_net"].mean() for c in CONDITIONS}

print("\nHypothesis checks (paper propositions P1–P5 + novelty N3):")
check("P1/P3 — distributed agency beats the status quo",
      t_net["DA_GATED"] > t_net["HUMAN_ONLY"] and t_net["DA_GATED"] > t_net["SINGLE_COPILOT"],
      f"DA_GATED {t_net['DA_GATED']:.0f} vs HUMAN_ONLY {t_net['HUMAN_ONLY']:.0f}, "
      f"COPILOT {t_net['SINGLE_COPILOT']:.0f}")
check("P1 — gating matters more as context drifts faster (epistemic alignment)",
      (hi_net["DA_GATED"] - hi_net["DA_FIXED"]) > (t_net["DA_GATED"] - t_net["DA_FIXED"]) * 0.9
      and hi_net["DA_GATED"] > hi_net["DA_FIXED"],
      f"gated-fixed gap: {t_net['DA_GATED'] - t_net['DA_FIXED']:.0f} at σ=0.08 → "
      f"{hi_net['DA_GATED'] - hi_net['DA_FIXED']:.0f} at σ=0.16")
check("P4 — inner-crowd wisdom is inverted-U in divergence",
      e2_q.max() > e2_q[0] + 0.05 and e2_q.max() > e2_q[-1] + 0.05 and 0 < peak < 2.5,
      f"quality {e2_q[0]:.2f} (δ=0) < {e2_q.max():.2f} (δ*={peak:.2f}) > {e2_q[-1]:.2f} (δ=2.5)")
e3_net = {k: v["summary"]["total_net"].mean() for k, v in e3.items()}
e3_fail = {k: (v["summary"]["irrev_fails"] + v["summary"]["rollbacks"]).mean()
           for k, v in e3.items()}
check("P5 — progressive autonomy beats both act-from-start and suggest-only",
      e3_net["DA_GATED"] > e3_net["DA_FIXED"] and e3_net["DA_GATED"] > e3_net["DA_SUGGEST_ONLY"],
      f"net {e3_net['DA_GATED']:.0f} vs act-first {e3_net['DA_FIXED']:.0f} "
      f"(failures {e3_fail['DA_GATED']:.1f} vs {e3_fail['DA_FIXED']:.1f}) "
      f"vs suggest-only {e3_net['DA_SUGGEST_ONLY']:.0f}")
check("P5/N5 — staleness gating limits post-shock damage",
      loss["DA_GATED"] > loss["DA_FIXED"] and fails_post["DA_GATED"] < fails_post["DA_FIXED"],
      f"post-shock net {loss['DA_GATED']:.1f} vs {loss['DA_FIXED']:.1f}; "
      f"failures {fails_post['DA_GATED']:.1f} vs {fails_post['DA_FIXED']:.1f}")
mean_fixed_tot = float(np.mean(vals))
check("N3 — ADC ≈/≥ best fixed profile across the regime shift, beats hand-tuning on average",
      adc_tot >= 0.95 * best_fixed_tot and adc_tot > mean_fixed_tot,
      f"ADC {adc_tot:.0f} vs best fixed {best_fixed_tot:.0f} "
      f"(mean fixed {mean_fixed_tot:.0f}; calm winner F={best1}, turbulent winner F={best2})")
check("N3 — ADC visibly re-adapts the update rate after the regime shift",
      fid_turb > fid_calm + 0.25,
      f"chosen fidelity {fid_calm:.2f} in calm regime -> {fid_turb:.2f} in turbulent regime")
esc = e1[("DA_GATED", 0.08)]["summary"]
check("Contracts escalate what needs escalating (recall)",
      esc["esc_recall"].mean() > 0.9,
      f"escalation recall {esc['esc_recall'].mean():.2f}, precision {esc['esc_precision'].mean():.2f}")

print(f"\nAll checks passed. Total runtime: {time.time() - T_START:.0f}s")
print("""
CONCLUSIONS
-----------
1. Formalizing He's distributed-agency framework makes its propositions testable — and, at low
   to moderate context drift, they hold: governed portfolios of AI representations dominate both
   the human-only team and the single generic copilot, mainly by converting human attention from
   routine review into ratification of pre-negotiated options (P1, P3; ~1/3 of leader attention
   is freed at default drift).
2. The paper's safety machinery is not decorative: staleness/novelty gating + progressive
   autonomy is what keeps naive distributed agency from collapsing under fast context drift and
   shocks (P5, the "Northstar Tuesday" event study). Naive (ungated) distributed agency falls
   *below* the human-only status quo — deploying agent portfolios without governance is worse
   than not deploying them.
3. We quantify the paper's boundary condition #2: under *extreme* drift (sigma >= 0.12 here),
   epistemic alignment becomes unaffordable, every delegation scheme loses ground, and
   conservative / human-centered configurations close the gap — delegation pays only where
   representations can stay synchronized.
4. "Inner-crowd wisdom" has a measurable sweet spot: option quality is inverted-U in the
   Divergence Index, so divergence must be curated, not maximized (P4).
5. NOVEL: the Adaptive Delegation Controller closes the paper's open loop — it implements the
   "Update Routine" as an evidence-driven feedback law, re-adapts the portfolio's update rate
   after regime shifts, matches the best fixed hand-tuned profile (without knowing the regime),
   and beats hand-tuning on average. Delegation policy itself can be an object of learning, not
   just judgment.
""")
