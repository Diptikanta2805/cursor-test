# When the Coattendee Is an Agent

An AMR-style theory paper: one contribution, one tension, a simple model, then simulation to elaborate it.

This replaces the earlier wide HABV sketch. That sketch had too many constructs (coupling, displacement, quality mismatch, interface load, blind-spot inversion, brokerage, fake “we”). An Academy of Management Review theory paper cannot carry that. Kauppila and Vaara (2026) made one move: dyad → triad. Davis, Eisenhardt, and Bingham (2007, AMR) say simulation is for elaborating *simple* theory: a few constructs, a few propositions, a basic tension, then experiments. This plan follows both.

---

## What this paper is about (one sentence)

When an AI agent sits in the coattendee seat of Kauppila and Vaara’s attention triad, people and the agent can both look at the same issue, but they cannot jointly attend in the same way—and treating that as joint attention is the theoretical problem.

---

## 1. Why AMR papers look like this

Kauppila and Vaara (2026) is the template in our literature. They do not review all of attention. They do this:

1. Start from ABV: action follows the issues members attend to.
2. Name one limit: ABV is dyadic (I attend to X).
3. Make one move: triad (I, another person, X).
4. Build a process model from that move.
5. Write propositions that follow in order.
6. State boundary assumptions.

Davis, Eisenhardt, and Bingham (2007, AMR) is the template for the modeling part. They say:

- Begin with a research question that has a **tension** (more vs less, short vs long run).
- Start from **simple theory** (a few constructs, not a whole field).
- Encode only that theory in software.
- **Verify**: the simulation must first reproduce the simple theory.
- **Then experiment** to get new theory (non-obvious, often nonlinear).
- Do not build a toy copy of an entire company. Model the mechanism.

That is the plan below. One gap. One new construct. One mechanism. One tension. A small model. Experiments that produce new propositions.

---

## 2. The research question (the tension)

Kauppila and Vaara define joint attentional engagement as the sustained allocation of cognitive resources on a *joint* object. That requires two things at once:

- both parties attend to the issue, and
- **recursive attention**: I notice that you are noticing (and you can notice that I am noticing).

They state a boundary assumption: people have theory of mind. They can imagine another actor’s attention from that actor’s point of view. They also say the coattendee must be *capable of attending*, which is what makes joint attention interactive and generative.

Now organizations put agentic AI in that coattendee role: monitors, copilots, briefing agents. The agent *can* attend (it notices issues). It does *not* meet the theory-of-mind assumption (it cannot take the human’s situated point of view in the way their model requires).

So the question is not “does AI increase attention?” That is too broad, and it restarts the Seidl–Rhee fight.

The question is:

> When the coattendee is an agent, does joint attentional engagement go up or down?

That is a real tension. In the short run, more noticing and more shared screens look like more joint attention. In the long run, the recursive, human-to-human “we” that Kauppila and Vaara theorize may never form. Simulation is the right method because the tension is longitudinal and likely nonlinear (Davis et al., 2007; March, 1991).

---

## 3. What existing theory already gives us (simple theory, not a literature dump)

We take three ideas only. Everything else is background, not the model.

**From Kauppila and Vaara (2026).** Organizational attention to an issue becomes joint when a triad forms: attendee, coattendee, joint object. Recursive attention is the heart of the triad. Mutual recursion is what turns two people looking at X into a “we” looking at X.

**From Rhee (2026).** Attention is scarce. Time spent on one target is time not spent on another. So recursive attention is also scarce. If I spend my “noticing others’ noticing” on the agent, I have less of it for other people.

**From Seidl et al. (2026), used only as a warrant.** Attending is not one homogeneous thing. An agent’s attending (logs, summaries, pings) is not the same kind of attending as a person in a situation. We do *not* model their five qualities. We use this only to justify why an agent is not a drop-in human coattendee.

Nicolini et al. (2026) sit in the wings: if the agent is loud and always on, it will win the competition for scarce recursive attention. That becomes an assumption in the model, not a second theory.

**The gap, stated sharply.** Kauppila and Vaara changed dyad to triad, but the coattendee is still a human member. ABV work on algorithms (Ocasio, 2025; Seidl’s materiality; Nicolini’s scaffolding) treats AI as a tool, a channel, or a structure. No one theorizes the agent as occupying the *coattendee node* when the theory-of-mind assumption fails.

That is the whole opening of the paper. Stop there.

---

## 4. The one theoretical contribution

Human coattendees come as a bundle. They attend to the issue *and* they recursively attend to each other. Kauppila and Vaara could treat “joint attention” as one thing because, for humans, those two parts travel together.

An agentic coattendee splits the bundle.

- The agent can attend to the issue (often more issues, more often).
- The agent cannot mutually recurse on the human’s situated attending.

So we need a distinction their theory did not need.

### The construct: apparent vs genuine joint attentional engagement

**Co-presence.** Human and agent both put effort on issue X. You can see this in logs: both “attended to X.”

**Mutual recursion.** Each party models the other’s attending to X from the other’s point of view. For two humans, this is Kauppila and Vaara’s recursive attention in both directions. For a human and an agent, recursion is at most one-way: the human can notice that the agent is tracking X; the agent cannot take the human’s situation as a situation.

**Apparent joint attentional engagement** = co-presence (and maybe one-way recursion). It looks like a triad.

**Genuine joint attentional engagement** = co-presence + mutual recursion. This is what their “collective we” actually is. It can only fully exist between parties that can recurse on each other. In this paper, that means humans. The agent can *help* that human–human we form, or it can *stand in for* it.

This is the contribution: **agentic coattending creates apparent joint engagement without automatically creating genuine joint engagement.** Existing theory cannot see the split because it never had a coattendee who can attend but cannot mutually recurse.

### The mechanism: recursive substitution

Humans have a scarce recursion budget (Rhee). They can spend it on:

- other humans (“I see that Sam is on this issue”), or
- the agent (“I see that the system is tracking this issue”).

The agent is always available, fluent, and persistent. In Nicolini’s terms, it is a strong competitor in the attentional arena. So as agentic coattending rises, recursive attention moves from people to the agent.

That is **recursive substitution**.

- Apparent joint engagement with the agent goes up.
- Genuine joint engagement among humans on that issue goes down, unless the agent is used only to notice and then humans still recurse on each other.

One mechanism. Not seven.

---

## 5. How the argument develops (logic, in order)

This is the spine of the paper. Each step uses the previous step. Do not skip.

**Step 1.** Joint attentional engagement, as defined by Kauppila and Vaara, is not “two parties mentioned X.” It is co-presence plus mutual recursion.

**Step 2.** That definition silently assumes a coattendee who can attend *and* recurse. Humans satisfy both. Agentic AI satisfies the first and not the second.

**Step 3.** Therefore an agent in the triad can produce co-presence without producing genuine joint engagement. We name that gap apparent vs genuine.

**Step 4.** Because human recursion is scarce, attending to the agent’s attending trades off against attending to other humans’ attending (Rhee applied to recursion, not to issues in general).

**Step 5.** If the agent is treated as the coattendee, substitution follows. If the agent is treated only as a noticer that feeds human–human recursion, complementarity follows.

**Step 6.** Over time this is not linear. A little agentic coattending can help humans find issues and then invite other humans (more genuine JA). A lot of agentic coattending makes the agent the coattendee (less genuine JA). That inverted-U is the non-obvious claim the simulation must be able to produce. It is the same *shape* of contribution as March (1991) on exploration/exploitation and Rivkin (2000) on complexity: a moderate level is not a compromise slogan; it is the theoretical result.

Stop. Do not add brokerage types, TMT agendas, five qualities, or a full firm. Those are other papers.

---

## 6. Simple theory (what we must verify before any “new” result)

These three propositions are not the contribution. They are the platform. The simulation must reproduce them first (Davis et al., verification step). If it cannot, the software is wrong.

**P1 (from Kauppila and Vaara).** When two humans are co-present on an issue and mutually recurse, genuine joint attentional engagement on that issue is higher than when they are only co-present.

**P2 (from Rhee).** A human’s recursive attention is capacity-constrained. An increase in recursion toward one party decreases recursion toward other parties.

**P3 (agent as noticer).** Agentic coattending increases co-presence on issues the agent can observe.

If P1–P3 do not appear in the baseline runs, we do not experiment yet.

---

## 7. Novel theory (what the experiments are for)

After verification, we vary one thing: how much, and in what role, the agent occupies the coattendee seat. We watch apparent vs genuine joint engagement over time.

**P4.** As agentic coattending increases, apparent joint attentional engagement rises steadily, but genuine joint attentional engagement follows an inverted U: it rises at low-to-moderate levels and falls at high levels.

Why: moderate agent noticing helps humans find issues and then recurse on other humans (P3 helps P1). High agentic coattending triggers recursive substitution (P2), so the human “we” does not build.

**P5.** The fall in genuine joint engagement is produced by recursive substitution: the share of human recursive attention spent on the agent rises, and the share spent on other humans falls.

This is the mechanism test. If genuine JA falls but recursion has not moved toward the agent, P4 is a blob, not a theory.

**P6.** The inverted U is shifted by how the agent is used.

- If the agent is a **noticing aid** (it surfaces X, then humans still spend recursion on other humans), the peak of genuine JA is higher and occurs at a higher level of agent noticing.
- If the agent is a **substitute coattendee** (humans treat “the system is on this” as the joint “we”), the peak is lower and the fall starts sooner.

P6 is the practical implication, but it is still the same theory: the split between apparent and genuine, plus substitution.

That is the whole propositional structure: three inherited, three new, all about one outcome (joint attentional engagement) and one mechanism (recursive substitution).

---

## 8. The model (only what the theory needs)

Davis et al.: the computational representation must *mirror the theoretical logic*. It is not a digital twin of a 2,000-person company. March (1991) did not simulate a firm. He simulated exploration vs exploitation. We simulate apparent vs genuine joint engagement.

### What exists

- A small set of **issues**. Each is either observable by the agent or not. (Agents see documents and metrics. They do not see unmarked situated cues. This is the minimum use of Rhee’s situatedness. One binary is enough.)
- **Humans**, each with two budgets per period: issue-attention and recursive-attention. Both are scarce and add up to a cap (P2).
- **One agentic coattendee** (or a single agent layer). It has a noticing capacity we can turn up. It has no mutual-recursion budget. That is the theoretical point, not a missing feature.

### What happens each period

1. Issues arrive.
2. The agent notices some observable issues (capacity = how many).
3. Humans allocate issue-attention (to the world and/or to agent-surfaced issues).
4. Humans allocate recursive attention: to other humans, or to the agent, or both, under the cap.
5. **Apparent JA** on issue X = human and agent both put issue-attention on X.
6. **Genuine JA** on issue X = at least two humans put issue-attention on X *and* they recurse on each other about X.

No five-quality vectors. No TI/TG. No TMT phase. No chat vs meeting vs cafeteria as separate systems. If we need “situation,” it is only: can the agent observe this issue or not.

### Why stochastic processes (not NK, not system dynamics)

Davis et al.: pick the approach that fits the logic. This is not search on a landscape (NK). It is not stock-and-flow catastrophe (system dynamics). It is allocation under scarcity with a trade-off over time, like March (1991) and Davis, Eisenhardt, and Bingham (2007). Custom stochastic process.

### Verification (must pass)

- Two humans, no agent: more mutual recursion → more genuine JA (P1).
- Raise recursion to one human: recursion to others falls (P2).
- Add agent, raise noticing: co-presence on observable issues rises (P3).
- Genuine JA does *not* automatically rise one-for-one with co-presence. If it does, we have failed to encode the split.

### Experiments (this is where new theory comes from)

Vary only what P4–P6 need:

| Experiment | What we change | What we should see |
|---|---|---|
| E1 | Agent noticing capacity, low → high | Apparent JA up; genuine JA inverted-U (P4) |
| E2 | Track where recursive attention goes | The fall in genuine JA moves with substitution (P5) |
| E3 | Agent as noticing aid vs substitute coattendee | Peak of genuine JA higher in the aid condition (P6) |
| E4 | Time | Short run looks like “more joint attention”; long run shows the drop (the tension) |
| E5 (optional, one moderator) | Share of issues the agent cannot observe | The drop in genuine JA is worse when more of the important issues are unobservable to the agent |

E5 is optional. If the paper is getting busy, cut it. Do not add ten conditions.

### What would surprise us (and therefore count as theory)

The contribution is not “AI can help or hurt.” It is the **shape**: apparent engagement is monotone; genuine engagement is not. If the simulation produces two straight lines, we do not have a paper. If it produces the inverted U *and* E2 shows substitution as the reason, we have a paper.

---

## 9. Paper outline (write it in this order)

Follow Kauppila and Vaara’s AMR shape, then add Davis et al.’s simulation block.

1. **Abstract.** One contribution: agentic coattending splits apparent from genuine joint attentional engagement through recursive substitution.
2. **Introduction.** ABV → triad → theory-of-mind boundary → agents sit in the coattendee seat → the tension (up or down?) → why simulation.
3. **Theoretical background.** Short table only:

   | | Traditional ABV | Kauppila and Vaara | This paper |
   |---|---|---|---|
   | Who attends | Human member | Human + human coattendee | Human + agentic coattendee |
   | What joint attention is | Not theorized as joint | Co-presence + mutual recursion | That bundle splits |
   | Key assumption | Cognitive limits | Theory of mind | Theory of mind does not hold for the agent |
   | Core outcome | Allocation to issues | Buildup of joint engagement | Apparent vs genuine joint engagement |

4. **Theory.** Apparent vs genuine. Recursive substitution. P1–P3 as inherited; then the logic that yields P4–P6 as claims to be elaborated computationally.
5. **Computational representation.** Constructs, algorithm, assumptions, why stochastic processes.
6. **Verification.** P1–P3.
7. **Experiments and new theory.** P4–P6, with figures: monotone apparent JA; inverted-U genuine JA; substitution as the mediator; aid vs substitute-coattendee.
8. **Discussion.** Three contributions only: (i) to ABV, the coattendee can be non-human; (ii) to Kauppila and Vaara, their boundary assumption is now a variable; (iii) to the quality/quantity debate, we do *not* pick a side—we show that more attending (agent noticing) is not the same as more joint engagement. Future research: brokerage, TMT agenda, ethnography of apparent “we.” Those are next papers, not this one.

---

## 10. What we deliberately will not do in this paper

- Will not resolve Seidl vs Rhee vs Nicolini as a whole.
- Will not model five qualities of attending.
- Will not model TI/TG brokerage or a three-phase strategy-initiative process (that is their paper; we stop at joint engagement).
- Will not build a 2,000-person digital twin. That is a different genre. AMR simulation models a mechanism.
- Will not treat “AI adoption” as a yes/no dummy. The variable is agentic coattending (how much, and in which role).

---

## 11. The contribution in the language AMR reviewers look for

Whetten (1989): what is new, and why it matters.

**What is new.** A distinction (apparent vs genuine joint attentional engagement) and a mechanism (recursive substitution) that become necessary only when the coattendee is an agent.

**Why it matters.** Organizations will read co-presence with an agent as “we are jointly attending.” Kauppila and Vaara’s theory says the “we” is mutual recursion among parties who can take each other’s point of view. If we do not split those, ABV will count agent logs as joint attention and will not see why bottom-up engagement still fails.

**What the simulation adds.** Not realism for its own sake. It shows the relationship is inverted-U over time, which armchair theory can guess but cannot pin to substitution. That is exactly the use Davis, Eisenhardt, and Bingham assign to simulation: take simple theory (P1–P3), experiment, return with more precise theory (P4–P6).
