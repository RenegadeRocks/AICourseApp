---
type: synthesis
block: block-0-basecamp
week: week-03
day_of_cycle: 7
day_name: sun
title: 'Week 3 Synthesis — The four-step pipeline, applied twice'
study_date: 2026-05-17
date_due: 2026-05-17
tags: [synthesis, quiz, flashcards, jtbd, fit-rubric, scoping, pricing, klarna, decagon, cursor, claude-code, devin, metr, rice, eval-gates, unit-economics]
last_verified: 2026-04-15
word_count_target: 3800
---

# Week 3 Synthesis — The four-step pipeline, applied twice

## The one-sentence thesis of this week

The six topics you covered this week — JTBD and problem discovery, AI fit evaluation, project scoping with kill criteria, pricing with margin math, and two end-to-end case-study teardowns (customer support and coding agents) — all decompose into a single operator pipeline: **discovery → fit → scoping → pricing**. Weeks 0–2 gave you the substrate and the techniques. Week 3 is the week you learn to refuse projects before you build them, scope the survivors ruthlessly, and price them in a way that survives a 30% token-cost swing.

---

## The unifying frame: project selection is a four-step pipeline, not a vibe

Week 0 installed the substrate (how models work, how your tooling remembers, how context economics and git worktrees work). Week 1 installed the primitives (prompting, RAG, vibe coding). Week 2 installed runtime selection (MCP, voice, n8n, agent fundamentals). Week 3 moves up another floor: **how do you decide what to build with all of this, for whom, at what scope, and at what price?**

The silent thread across Mon–Sat is that every AI project decision you will be asked to make in 2026 is really a decision about where you are in the four-step pipeline, and whether you have done the previous step honestly:

- **Mon — Problem discovery.** The decision is not "what AI opportunity list do we pick from?" but "have we run five switch interviews and identified the actual job, the hidden competitor (often a non-AI substitute), and the underserved Ulwick-style outcome?"
- **Tue — Fit evaluation.** The decision is not "which model?" but "does this problem *partition* into AI + deterministic code + human, and which sub-task belongs to which substrate on the five axes (failure cost, volume, ambiguity, consistency, auditability)?"
- **Wed — Scoping.** The decision is not "build an MVP" but "build a *walking skeleton with eval harness* — the thinnest system that still runs *and* measures itself — and pre-commit to the metric, threshold, and decision that kills the project."
- **Thu — Pricing.** The decision is not "what do competitors charge?" but "which of the three axes (value / seat / usage) encodes the failure mode I can actually underwrite, given that my COGS moves on a timescale shorter than my contract length?"
- **Fri — Support case study.** The four-step pipeline run end-to-end on Klarna / Intercom Fin / Decagon / Sierra, with real numbers and a public walk-back.
- **Sat — Coding case study.** The pipeline run end-to-end on Cursor / Claude Code / Copilot / Devin, with a live controversy (METR slowdown) and a benchmark-vs-production gap (SWE-bench Verified vs SWE-bench Pro).

Frame it that way and the week snaps into focus. Project selection is the discipline of refusing to skip the previous step — of refusing to scope a project whose job hasn't been validated, pricing a project whose margin model hasn't been sensitivity-tested, shipping an AI where the deterministic partition would strictly dominate.

---

## Where each day's content goes forward

| This week's lesson | Underwrites in later weeks |
|---|---|
| Mon — JTBD and problem discovery | Every client engagement in Blocks 2–4; every PRD you write; every "why this, why now" conversation with a sponsor |
| Tue — AI fit rubric + RICE-AI | Every portfolio-prioritization meeting; Week 7 evals; Weeks 19–22 client-project scoping |
| Wed — Walking-skeleton MVP + eval gates + kill criteria | Every project after today; Week 7–9 evals; any retrospective on "why did we ship that?" |
| Thu — Pricing trilemma + margin math | Every pricing conversation with a CFO or client; Block 4 commercial negotiations; your own consulting / product rate cards |
| Fri — Support-agent teardown (Klarna, Intercom, Decagon, Sierra) | Block 2 voice-first products; any CX/CS client engagement; vendor teardowns of any agent category |
| Sat — Coding-agent teardown (Cursor, Claude Code, Devin) | Every tool-selection conversation; Weeks 13–14 on agent evaluation; your own stack choices this year |

Week 3 is not a survey. It is the layer of **commercial and project-selection judgment** that Weeks 5, 13, and 20 will silently assume you have internalized. When Block 2 asks you to scope a client voice product, you will re-open Wednesday's kill-criterion template. When a CFO in Block 4 asks "what's our margin on this," you will re-open Thursday's sensitivity table. When anyone in the program says "we should use Devin," you will re-open Saturday's METR section.

---

## The week's key moves — the mental-move table

Fourteen highest-leverage operational moves drawn from the six lessons. Each row: the move, the mechanism that explains why, when to apply it, when not to.

| # | Move | Mechanism | Apply when | Do NOT apply when |
|---|------|-----------|------------|-------------------|
| 1 | Run Moesta-style switch interviews first, Ulwick-style outcome decomposition second | Switch interviews surface whether a real struggle exists; outcome maps tell you what to build and how to measure it. Skipping either produces the Humane Pin | Any new AI project before a PRD is written | Rapid-iteration work on a product whose JTBD is already validated |
| 2 | Push past the first three "why's" in every interview, and map all four forces (push / pull / anxiety / habit) | Goal-level narration ("I wanted to close the deal") is not the job; the job is three layers down. Anxiety is usually the dominant AI-specific force and the one interviewers ignore | Every discovery interview for an AI product | Concept-validation interviews where you're not testing a switch |
| 3 | Name the non-AI competitor explicitly. If your customer loses your AI tomorrow, what do they reach for? | Non-AI substitutes (a checklist, a colleague, a policy) are the competitors that silently win; benchmarking only against other AIs is the trap | Every candidate AI project | Purely technical model-comparison exercises |
| 4 | Score every candidate problem on five fit axes — failure cost, volume, ambiguity, consistency, auditability — and partition | A production system is almost always a partition across AI + deterministic + human, not a pure play. The monolithic answer (Klarna 2024) violates multiple axes at once | Scoping any candidate problem | Throwaway prototypes where the cost of a wrong architecture is an afternoon |
| 5 | Use RICE-AI: split Confidence into C_est (estimate confidence) and C_eval (probability eval bar is cleared) | Classic RICE conflates "well-specified estimates" with "will the model actually be accurate enough." A project with big R and I but unknown C_eval has a fat left tail of "six months, no ship" | Portfolio prioritization across >3 AI candidates | Single-project decisions where you're already committed |
| 6 | Ship a walking skeleton with a runnable eval harness in the first week, not a prototype | Capability variance dominates market variance in months 0–6. Five customers trying a demo tell you about idea resonance, not about p90 tail quality where the system lives or dies | Any project you expect to run >4 weeks | Genuinely throwaway spikes where "does the idea resonate" is the only variable |
| 7 | Write kill criteria as metric + threshold + pre-committed decision, before building | "If it's not working we'll figure it out" is a feeling, not a criterion. Husain / Anthropic Applied AI pattern: no named refutation condition, no project | Any scoped project with a named customer or sponsor | Research spikes with open-ended success criteria |
| 8 | Gate RAG on chunk-level P@5 ≥ 0.8, Recall@20 ≥ 0.95, grounding rate ≥ 0.9 at week 4 | Document-level precision lies — a retriever that finds the right doc but wrong chunk still produces hallucinations. MIT NANDA's 95% pilot-failure figure is dominated by teams who never gated retrieval before generation | Any RAG-based project | Non-retrieval generation (pure summarization, drafting, classification) |
| 9 | Gate agents on per-call tool success ≥ 0.97, trajectory completion ≥ 0.7, recovery-after-error ≥ 0.5 | Tool-call failures compound: 0.92^10 ≈ 43% end-to-end. Recovery rate separates demo agents from production agents | Any multi-step agentic project | Single-call tool augmentation that doesn't loop |
| 10 | Calibrate LLM-as-judge to human labels (Cohen's κ ≥ 0.7) before using the judge as a gate | Shankar's *criteria drift*: the criteria depend on the outputs observed. A judge at κ = 0.4 is noise, not evaluation. Re-calibrate every 4 weeks or it silently decays | Any project using LLM-as-judge for gating | One-shot vibes evaluation not tied to a funding decision |
| 11 | Pick pricing by which failure mode you can underwrite — not by what competitors charge | Every pricing axis insures one failure mode and exposes another. Value-based risks model-price collapse; seat-based risks power-law usage; usage-based risks procurement rejection. The axis choice is the risk choice | Any pricing conversation with a CFO or board | Quick-and-dirty pricing on a prototype product with no real customers |
| 12 | Build the margin model with COGS = token + infra + HITL + error remediation; run sensitivity at today / +30% / −50% token cost | HITL cost ($0.60/conversation in the Klarna range) usually dominates token cost in year one and falls only when autonomous resolution rises. A pricing model insensitive to HITL is hostage to it | Before committing to any published price | Before running the minimum eval — without C_eval you can't estimate autonomous resolution |
| 13 | Demand return-within-7-days, post-resolution CSAT, and escalation-request rate alongside any "deflection" or "resolution" number | Deflection punishes good AI and rewards bad AI: a bot that closes the conversation with "sorry I can't help" gets counted as resolved. Ada and Fini Labs have both publicly sounded the alarm | Evaluating any outcome-priced vendor (Fin, Decagon, Sierra) | Head-of-funnel metrics where definitional purity doesn't affect the bill |
| 14 | Discount SWE-bench Verified by 20–30 points when predicting in-codebase performance, and assume the agent runs at 50–60% in your messy reality | SWE-bench Pro (Scale AI's follow-up) runs ~27 points below Verified on the same model tier; contamination, environment simplicity, and "resolved = tests pass" are the three gaps. METR's 2025 RCT found a 19% *slowdown* on senior devs' own repos | Any coding-agent procurement or client recommendation | Triage — headline benchmark is still a reasonable first filter |

---

## 20 quiz questions

*Span: Mon–Sat. Mix: 8 recall, 8 apply, 4 controversy-defense. Answers at end.*

---

**Q1 (Recall)** — State Christensen's job-story format verbatim, and give Ulwick's four-part outcome-statement format.

**Q2 (Recall)** — Name the five axes of the Tuesday fit rubric, and state which axis Klarna's 2024 deployment violated most clearly.

**Q3 (Recall)** — What are the three components of a well-formed kill criterion, per Wednesday's Husain-derived frame?

**Q4 (Recall)** — State the three-threshold RAG eval gate from Wednesday (P@k, Recall@k, grounding rate) and the three-threshold agent eval gate (per-call success, trajectory completion, recovery).

**Q5 (Recall)** — Give the full COGS-per-unit formula for an AI product from Thursday, and name the line item that typically dominates in year one.

**Q6 (Recall)** — State Intercom Fin's headline pricing and its 50% resolution-rate guarantee.

**Q7 (Recall)** — Give Decagon's published pricing floor and approximate per-conversation rate.

**Q8 (Recall)** — State the exact finding of the METR July 2025 RCT on developer speedup with AI tools.

**Q9 (Apply)** — A founder asks you to ship "an AI agent for our inbound sales team." Walk through Monday's discovery checklist in five bullets — what you would demand before writing a PRD.

**Q10 (Apply)** — A CFO wants to greenlight a customer-service agent project, pitched as "80% deflection." Apply the Tuesday fit rubric and propose the partition between AI, deterministic routing, and human escalation.

**Q11 (Apply)** — Write a well-formed kill criterion for an internal-enterprise RAG assistant over a 500k-doc corpus, with a week-6 checkpoint.

**Q12 (Apply)** — Compute gross margin on a customer-service agent at $0.99/resolution with COGS of $0.10 token + $0.05 infra + $0.60 HITL + 3% error-remediation-of-revenue. Now redo it at 50% HITL reduction.

**Q13 (Apply)** — A client wants to price a legal-drafting AI at $2,000/seat/month. Name the three cost surfaces you must model for margin and state the one that usually breaks the model.

**Q14 (Apply)** — Given the Klarna walk-back, sketch the hybrid architecture a fintech CX lead should propose for a 2026 deployment. Cite the three contract clauses you'd add vs. a naive 2024-style AI-first spec.

**Q15 (Apply)** — Your CTO wants to deploy Devin org-wide. State the three specific pushbacks from Saturday's reviewer lens (CTO / Husain / Cognition founder) and the scoped pilot that would test each.

**Q16 (Apply)** — Run the RICE-AI calculation on two candidate projects: (A) R=1000, I=2, C_est=0.8, C_eval=0.3, E=6; (B) R=300, I=1, C_est=0.9, C_eval=0.85, E=2. Which should you staff next quarter?

**Q17 (Controversy-defense)** — Position: "JTBD is a retrofit that smuggles yesterday's product thinking into AI-native categories; the breakout AI products (Cursor, Character.AI, Replit) are capability-first and only find their JTBD post-launch." Take a side.

**Q18 (Controversy-defense)** — Position: "Classic RICE is fine for AI project prioritization — adding C_eval is over-engineering for executives." Take a side, using at least one real failure pattern from Wednesday or from your own experience.

**Q19 (Controversy-defense)** — Position: "Klarna's walk-back in May 2025 is prima facie evidence that pure-AI support cannot work at scale." Defend or refute, citing three specific numbers from Friday's lesson.

**Q20 (Controversy-defense)** — Position: "The METR July 2025 study proves that coding agents make senior developers slower, and any vendor claim of 25–55% speedup is marketing." Take a side, being specific about task type and developer context.

---

## Answers

**Q1** — Christensen: *When I [situation], help me [motivation], so I can [expected outcome]*. Ulwick: *direction (minimize/maximize) + metric + object of control + contextual clarifier* (e.g., "minimize the time it takes to cut the grass without damaging the lawn").

**Q2** — Failure cost asymmetry, volume, ambiguity tolerance, consistency requirements, auditability. Klarna 2024 violated axes 1 (failure cost — refunds in front of angry customers), 3 (ambiguity — long tail of emotionally loaded tickets), and 5 (auditability — monolithic deployment with no human review on the expensive slice). The walk-back in May 2025 was not an indictment of AI in CX; it was an indictment of *unpartitioned* AI in CX.

**Q3** — (1) A metric measurable on a named data slice with a named evaluator; (2) a threshold the metric must exceed (or fall below, for cost/latency) by a named checkpoint; (3) a pre-committed decision if the threshold is missed (pivot, defund, hand back to human workflow). "If it's not working we'll figure it out" satisfies none of the three.

**Q4** — RAG: P@5 ≥ 0.8 at chunk level, Recall@20 ≥ 0.95, grounding rate ≥ 0.9 (LLM-judge calibrated against humans), measured at week 4. Agents: per-call tool success ≥ 0.97, trajectory-level task completion ≥ 0.7 at fixed step/$ budget, recovery-after-error rate ≥ 0.5. Miss any threshold → rescope or kill.

**Q5** — COGS per unit = token_cost + infra + HITL + error_remediation. HITL (human-in-the-loop escalation and QA) usually dominates in year one and only falls when autonomous resolution rate rises. Klarna's per-transaction cost fell from $0.32 (Q1 2023) to $0.19 (Q1 2025) — a 40% labor reduction, not 40% token deflation.

**Q6** — Intercom Fin charges $0.99 per resolution (conversation ends without user reopening or human escalation within ~24h). Intercom publishes ~60% average resolution rate and offers a 50% guaranteed-resolution-rate refund: if Fin resolves fewer than 50% of conversations it touches, Intercom credits back the shortfall.

**Q7** — Decagon: approximately $50k annual platform floor + ~$0.99/conversation with volume discounts. Industry-reported ACV range $95k–$590k, median ~$400k. The per-conversation denominator (not per-resolution) is the definitional move — it avoids the "what counts as resolution" arbitrage that plagues outcome-pricing.

**Q8** — Sixteen experienced OSS developers, ~5 years of prior experience on their own repos, completed 246 tasks, randomly assigned AI-allowed (mostly Cursor Pro + Claude 3.5/3.7 Sonnet) or AI-disallowed. Pre-study forecast: 24% speedup. Post-study self-estimate: 20% speedup. **Measured result: 19% slowdown.** Everyone — developers, ML researchers, economists — predicted in the wrong direction.

**Q9** — (1) Name the job in Christensen format (not "use GPT for sales" — "when [sales situation], help [rep] do [outcome]"). (2) Five real switch interviews — reps who actually switched from a prior approach to AI for the adjacent job. (3) 10–30 Ulwick outcome statements with importance/satisfaction data. (4) Named non-AI competitor (probably a SDR doing manual research, a checklist, or a well-run CRM). (5) Pre-committed kill criterion at 90 days. If you can't answer all five, the project isn't ready.

**Q10** — Decompose. Route ~60–70% head-of-distribution tickets (order status, payment-plan changes, refund status) through AI with deterministic handoff patterns. Route ambiguous / regulated / emotionally loaded tickets (fraud claims, disputes, hardship) to humans with AI-drafted suggestions attached. Sample-based QA across both paths. The "80% deflection" number is almost certainly computed against a denominator that excludes the tail — demand return-within-7-days and post-resolution CSAT on the AI-resolved slice separately before signing.

**Q11** — "By week 6 post-kickoff, against a 100-query labeled eval set, chunk-level P@5 ≥ 0.80 AND Recall@20 ≥ 0.95 AND LLM-judge grounding rate ≥ 0.90 (judge calibrated to human labels at Cohen's κ ≥ 0.7). Miss any threshold → rescope retrieval (chunker, embedding, hybrid search, query rewriter) for 2 weeks. If week-8 check fails any threshold → kill and hand back to current Confluence search."

**Q12** — Current: COGS = 0.10 + 0.05 + 0.60 + 0.03×0.99 ≈ $0.7797. GM = (0.99 − 0.78)/0.99 ≈ **21%**. Redo at HITL halved to $0.30: COGS ≈ 0.48. GM = (0.99 − 0.48)/0.99 ≈ **52%**. This is the central Thursday insight: in mature AI products, HITL (autonomous resolution rate) is the margin lever, not token price.

**Q13** — (1) Token cost × expected per-seat usage (power-law: top 5% of users can drive 40% of inference). (2) HITL / review cost — even seat-priced legal tools have a review loop. (3) Model-price volatility over contract length (a16z LLMflation: 10× annual decline, but premium-tier models can spike +30% on launch). The one that usually breaks the model is (1) — power-law usage at 50–150× the mean, which is what Harvey's 20-seat minimums and the Claude Code Max 20x subsidy pattern silently address.

**Q14** — Hybrid: AI owns the FAQ head (~60–66% of volume), deterministic routing handles unambiguous paths (order-status API lookup, payment-plan change API), humans own the regulated/emotional tail with AI-drafted suggestions rather than auto-sent. "Press 9 for a human" as a brand promise. Contract clauses: (a) model-price adjustment clause (25–40% margin of safety over 12-month contract); (b) return-within-7-days + post-resolution CSAT on AI-resolved conversations separately reported; (c) escalation-request-rate transparency — how often customers ask for a human mid-conversation whether or not they get one.

**Q15** — (1) **CTO pushback — SWE-bench discount**: Verified scores overstate production by 20–30 points (Pro is ~27 points below Verified on same tier; contamination, environment simplicity, test-pass ≠ correctness). Pilot: 20 real tickets from your backlog, human-graded, track accept-without-edit and time-to-merge. (2) **Husain pushback — measurement first**: binary pass/fail per ticket type in your workflow, N≥20 per type, judge calibrated to expert shadowing before trust. Pilot: define pass criteria *before* running any tool. (3) **Cognition pushback — right denominator**: compare tickets-completed-autonomously-with-acceptable-quality, not developer-minutes-saved. Pilot: well-scoped tickets only (Job C), measure autonomous completion rate not pair-programming speedup.

**Q16** — A: (1000 × 2 × 0.8 × 0.3) / 6 = 80. B: (300 × 1 × 0.9 × 0.85) / 2 = 114.75. **Staff B first.** B's higher eval-confidence and smaller effort mean a near-certain shippable win; A's fat left tail (30% C_eval) means a 70% chance of spending six months and shipping nothing. Classic RICE without the C_eval split would have ranked A higher and mis-staffed the quarter.

**Q17** — Either side is defensible, but the synthesis from Monday is: Position A (JTBD is evergreen) is right *for selection* — capability-first selection at the portfolio level produces the McKinsey/BCG hit rate (single-digit percent realizing material value). Position B (capability-first) is right *for expansion* — once JTBD is validated, capability-first experimentation finds the product surface. Cursor is the case study: initial JTBD was "help me write code faster with fewer lookups"; only after PMF did agent-mode, background tasks, and codebase-wide refactors unlock the $500M→$1B→$2B ARR run. Flipping the order produces Humane Pin / Rabbit R1.

**Q18** — Position defense: *C_eval is necessary, not over-engineering.* Real failure pattern from Wednesday: team forecasts R=10k users × I=3 impact, scopes a 6-month build, skips the minimum eval; at month 4 they discover frontier-model accuracy on their hard slice is 55% and no prompt/retrieval changes close the gap. Classic RICE folded this risk into either Effort (badly) or Confidence (worse). Splitting C_eval out forces the team to run a day-of-work minimum eval before the sheet is filled in, which kills ~half of candidate AI projects before a PRD is written. That is not over-engineering; that is how BCG's 5% of companies actually realizing value are operating.

**Q19** — Refute (stronger). Three numbers: (1) Klarna's 2024 handled two-thirds of chat volume, 2.3M conversations in month one, $40M projected 2024 profit improvement — the headline was real, not fabricated. (2) Per-transaction CX cost fell from $0.32 (Q1 2023) to $0.19 (Q1 2025) — 40% labor reduction *was realized* and survived the walk-back. (3) The May 2025 hiring-back was positioned as *VIP support* (400 SEK/shift Uber-style model, premium path) and by Q4 2025 earnings Klarna reported 40% workforce shrinkage over three years alongside the new hybrid architecture. The correct read is not "pure-AI failed" but "pure-AI-without-partition failed and the hybrid endpoint was the right architecture all along." The failure was communications (Siemiatkowski's "AI can perform all human jobs" framing) not economics.

**Q20** — Split by task type. Position "agents slow seniors" is right for Job B (pair-programming) *on mature codebases the developer already knows deeply* — this is exactly METR's experimental setup and the 19% slowdown is the honest measure. Position "25–55% speedup" is right for Job C (delegated tickets) on well-scoped novel work where the agent isn't competing against existing context in the developer's head. Cursor's 170%+ NDR and Claude Code's $2.5B annualized ramp (Feb 2026) reflect real willingness-to-pay, but willingness-to-pay is not measurable-throughput-gain — the gap is subjective felt-productivity, which lags objective throughput by years in every tool category. Honest 2026 briefing: expect subjective acceleration, measurable gains on novel work, null-to-negative on deep-context mature-codebase work. The second category is most of the upside.

---

## 30 flashcards

*Format: front ↔ back. Anki-importable.*

1. Q: Christensen JTBD format? → A: *When I [situation], help me [motivation], so I can [expected outcome].*
2. Q: Ulwick outcome-statement format? → A: Direction (min/max) + metric + object of control + contextual clarifier.
3. Q: Moesta's four forces of switching? → A: Push (pain of old), pull (attraction of new), anxiety (fear of switching), habit (inertia).
4. Q: The operator rule for order of JTBD schools? → A: Moesta switch interviews first (is there a real struggle?); Ulwick outcome decomposition second (what do we build and measure?).
5. Q: Five fit-rubric axes? → A: Failure cost asymmetry, volume, ambiguity tolerance, consistency requirements, auditability.
6. Q: Sixth fit-rubric axis (added for agents)? → A: Agent-compatibility — task decomposes into <5 reversible steps with per-step success criteria and controlled tools.
7. Q: Moffatt v. Air Canada (Feb 2024) lesson? → A: Airline liable for its chatbot's hallucinated bereavement-fare policy; damages small ($812 CAD) but precedent = company owns every word its AI speaks on its behalf about refundable commitments.
8. Q: RICE-AI formula? → A: (Reach × Impact × C_est × C_eval) / Effort. Split classic RICE Confidence into estimate-confidence and eval-confidence.
9. Q: Three parts of a kill criterion? → A: Metric (on named slice with named evaluator) + threshold (by named checkpoint) + pre-committed decision.
10. Q: RAG eval gate thresholds? → A: Chunk-level P@5 ≥ 0.8, Recall@20 ≥ 0.95, grounding rate ≥ 0.9 at week 4.
11. Q: Agent eval gate thresholds? → A: Per-call tool success ≥ 0.97, trajectory completion ≥ 0.7 at fixed budget, recovery-after-error ≥ 0.5.
12. Q: LLM-as-judge calibration threshold? → A: Cohen's κ ≥ 0.7 vs human labels on a 100-example calibration set before the judge can be a gate.
13. Q: Shankar's "criteria drift"? → A: Evaluation criteria partly depend on outputs observed; escape is iterative grade→extract→refine→re-grade. UIST 2024 paper *Who Validates the Validators?*
14. Q: MIT NANDA State of AI in Business 2025 headline? → A: ~95% of enterprise GenAI pilots produce zero measurable P&L impact; failure traces to scope + integration, not model quality.
15. Q: COGS formula for an AI product? → A: token_cost + infra + HITL + error_remediation. HITL usually dominates in year 1.
16. Q: The three pricing axes? → A: Value-based (per outcome), time/seat-based (per user), usage-based (per token/credit).
17. Q: Intercom Fin pricing? → A: $0.99 per resolution; ~60% average resolution rate; 50% guaranteed-resolution-rate refund if Fin falls below.
18. Q: Decagon pricing? → A: ~$50k annual platform floor + ~$0.99/conversation with volume discounts; $95k–$590k ACV range, median ~$400k. Per-conversation (not per-resolution) to dodge definitional arbitrage.
19. Q: Harvey pricing? → A: $1,200/lawyer/month, 20-seat minimum, ~$288k ACV floor. Anchored to customer billing rate not Harvey COGS. Post-LexisNexis premium bundles project to $3k/seat.
20. Q: Cursor June 2025 pricing episode? → A: Shifted Pro from "500 fast + unlimited slow" to "$20 of API credits at list." New agent models burned credits 3–10× faster; backlash → CEO apology + refunds. Revenue hit $1B Dec 2025; ~$2B annualized by April 2026.
21. Q: Claude Code unit economics? → A: ~$13/active-dev/active-day; $150–$250/active-dev/month average; Max 20x at $200/mo. One dev used 10B tokens in 8 months = would have been ~$15k on API, was $1.6k flat. Hit ~$2.5B annualized Feb 2026.
22. Q: Klarna 2024 headline numbers? → A: 2.3M conversations in month 1; two-thirds of chat volume; workload-equivalent of 700 FTE; $40M projected 2024 profit improvement; CSAT parity with humans; time-to-resolution 11 min → <2 min.
23. Q: Klarna 2025 walk-back? → A: May 2025 — hiring humans back, "Uber-style" flexible remote-agent model (400 SEK/shift). Positioned June 2025 as VIP premium path. Q4 2025 earnings: 40% workforce shrinkage over 3 years alongside hybrid architecture.
24. Q: Klarna CX per-transaction cost trajectory? → A: $0.32 (Q1 2023) → $0.19 (Q1 2025). 40% labor reduction over 24 months — HITL, not token deflation, drove margin.
25. Q: Sierra's outcome-pricing twist? → A: Charge only when AI resolves; human escalation free. Voice-native support (ADT, Sonos). Series C at $10B valuation Sep 2025; $100M ARR reported Nov 2025.
26. Q: Deflection-rate trap (Ada / Fini alarm)? → A: A bot that terminates with "sorry I can't help" gets counted as a successful resolution. Demand return-within-7-days + post-resolution CSAT + escalation-request rate alongside any deflection number.
27. Q: METR July 2025 RCT finding? → A: 16 senior devs, 246 tasks, own repos, Cursor Pro + Claude 3.5/3.7. Pre-study forecast: 24% speedup; post-study self-estimate: 20% speedup; **measured: 19% slowdown**.
28. Q: SWE-bench Verified vs Pro gap? → A: SWE-bench Pro (Scale AI) scores run ~27 points below Verified on same model tier. Causes: contamination (post-June-2024 training sees solutions), environment simplicity (single-repo Python), and "resolved = tests pass" ≠ correctness.
29. Q: Devin 2.0 pricing (Apr 2025)? → A: Starts $20/mo with pay-as-you-go at $2.25/ACU (1 ACU ≈ 15 min of Devin active work). Enterprise VPC custom-priced. Reset from original $500/250-ACU tier that under-adopted.
30. Q: The one-line rule for whether "Week 3" is installed in a practitioner? → A: Before any AI project, they've run switch interviews, scored the fit rubric, pre-committed kill criteria, and sensitivity-tested the margin at ±30% token cost — and they'd rather refuse the project than ship a monolithic AI into a problem that partitions.

---

## Further reading

The six lessons carry the full URL trails. This section points at the must-reads a reviewer would expect you to have internalized.

**Must-read (≤5):**
- Christensen Institute analysis of AI disruption (2024) — business-model framing of AI, not the technology. (Mon)
- Ulwick, *What Customers Want / ODI Handbook* (Strategyn, updated 2024) — outcome-statement discipline. (Mon)
- *Prediction Machines*, Agrawal / Gans / Goldfarb (Stanford AI Coop updated edition, 2022) — the prediction / judgment / action / outcome frame. (Tue)
- Hamel Husain, *Field Guide to Rapidly Improving AI Products* (2025) and *Evals FAQ* (2026) — the eval-first operating position. (Wed, Thu, Sat)
- Anthropic, *Building Effective Agents* (2024-12-20) — workflow vs agent, the five patterns, the "don't build an agent" discipline. (Tue, Wed)

**Recommended:**
- Shankar et al., *Who Validates the Validators?* (UIST 2024) — criteria drift, judge calibration. (Wed)
- METR, *Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity* (July 2025). (Sat)
- Bessemer, *State of AI 2025 (BVP Atlas)* — Supernova / Shooting Star margin cohorts. (Thu)
- a16z LLMflation analysis (2024–2025) — 10×/year inference cost decline. (Thu)
- Intercom Fin resolution-pricing page + 50%-guarantee help docs. (Thu, Fri)
- Decagon Stripe case study + Series C announcement (June 2025, $131M at $1.5B). (Fri)
- Sierra (Bret Taylor) outcome-pricing thesis — CNBC $4.5B (2024) → TechCrunch $10B (Sep 2025) → $100M ARR (Nov 2025). (Fri)
- SWE-bench Pro (Scale AI, arXiv 2509.16941, 2025) and SWE-bench illusion paper (arXiv 2506.*, 2025). (Sat)
- Cognition Devin technical report + Devin 2.0 pricing post (April 2025). (Sat)
- Gartner forecast: >40% of agentic AI projects will be cancelled by end of 2027. (Wed)

**Optional / supplementary:**
- Humane AI Pin post-mortem (Engadget 2024, Inc. 2024); Rabbit R1 post-mortem (Digitalapplied 2026). (Mon)
- Cagan, *Transformed* (March 2024) — product operating model for AI-era PM. (Mon, Tue)
- Torres, *Continuous Discovery Habits* (2021) + 2025 AI update. (Mon)
- BCG *AI at Work 2025* + *AI Radar 2025* — the 5% measurable-value figure. (Mon, Tue)
- Klarna primary sources: Feb 2024 press release, OpenAI case study, Pragmatic Engineer Apr 2024 teardown, Bloomberg May 2025 walk-back, Q4 2025 earnings. (Fri)
- McKinsey *State of AI 2025* + *Seizing the Agentic AI Advantage*. (Tue, Wed)
- Microsoft Foundry fine-tuning pricing (Ignite 2025). (Wed)

---

## Where you'd still lose points (reviewer lens)

A Christensen institute researcher, a Husain, a Ulwick, a skeptical CFO, and a senior enterprise CTO all re-read this synthesis and push back. Here is where they would, and where your own read is probably still thin:

1. **The "four-step pipeline" is a didactic simplification.** A Christensen researcher would point out that in practice, discovery and fit interact — the fit rubric sometimes reveals that the job hypothesis from discovery was mis-framed, and you loop. Scoping and pricing interact too: a kill criterion that triggers at week 6 may require a pricing clause that didn't exist at kickoff. If your mental model treats the four steps as a one-way waterfall, you haven't shipped enough of them. The pipeline is a checklist, not a Gantt chart.

2. **You probably have not actually run a switch interview.** Moesta would call this out immediately. Everyone nods at JTBD vocabulary; few have sat across from a specific customer and pushed past the first three why's until the spring-dug-into-my-back moment surfaced. If you cannot point to a transcript from the last 30 days, you are running an opinion poll, not a discovery practice. Spend one afternoon this week.

3. **Your C_eval estimate is probably a guess.** Husain would hold you to the bit: C_eval without a minimum eval is vibes, and vibes-based C_eval reintroduces exactly the failure mode that splitting it from C_est was supposed to fix. Rule: if your RICE-AI sheet has C_eval values you didn't measure with ≥20 labeled examples, write "NOT ESTIMATED" in the column and go run the day-of-work eval before the sheet leaves the building.

4. **You waved at "HITL" without decomposing it.** Thursday's $0.60/conversation HITL estimate is a blended number from the Klarna per-transaction data. A CFO would ask: what fraction is first-line escalation, QA sampling, eval labor, content-ops, incident response? Each decays on a different curve as autonomous resolution rises. A margin model that treats HITL as a single line item is a margin model that cannot tell you which investment moves gross margin next quarter.

5. **Klarna, Intercom, Decagon, Sierra numbers are vendor-favorable.** A skeptical CTO would note: every deflection / resolution / cost figure cited on Friday is vendor-reported, vendor-measured, or vendor-adjacent. The Ada/Fini "sounding the alarm on containment" line applies to every number in the lesson. Your teardown is *as good as* the contract clauses you add (return-within-7-days, post-resolution CSAT separately reported, escalation-request rate transparency, model-price adjustment). If your teardown lacks those clauses it is decoration.

6. **You took SWE-bench Verified at face value somewhere.** The Saturday reviewer lens named the 20–30 point discount and the contamination / environment / scoring gaps, but a sharper version asks: when OpenAI publicly stopped reporting Verified scores and shifted to Pro, that was a signal, not an announcement. If your client is still quoting Verified in 2026, they are reading a 2024 benchmark. Push them to Pro + their own 20-ticket eval or refuse to evaluate.

7. **The METR study does not "prove" what most people think it proves.** A sharp reader would push back that METR studied pair-programming on senior devs' own repos (Job B, mature codebase) and the finding generalizes narrowly. If you cite it against Devin (Job C, delegated tickets), you are overreaching. If you cite it against a junior dev onboarding to a new codebase (Job B but with no existing deep context), you are also overreaching. The correct citation is: "on Job B in mature codebases with senior devs, the measured effect was −19%."

8. **"Pick by use case" is true and also a cop-out.** A senior engagement lead would ask: write down, right now, the three specific signals in a stakeholder ask that swing you from value-based to usage-based pricing, or from a wrap to a buy. If you can't name them in two minutes, "pick by use case" is a rhetorical escape hatch. The mental-move table above is a start; your operator notebook should have your own version with your own engagements in it by the end of this block.

If any of the above felt uncomfortable, it should. That discomfort is the calibrated judgment you are building in this program. Return to the source lessons when you want to close the specific gap.

---

_last_verified: 2026-04-15_
