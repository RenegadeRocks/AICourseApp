---
type: lesson
block: block-8-wind-up-checklists
week: week-22
session_slug: final-thoughts-recap-checklists-2
day_of_cycle: 7
day_name: sun
date_due: 2026-10-18
tags:
  - capstone
  - synthesis
  - quiz
  - flashcards
  - program-finale
  - send-off
sources:
  - course-refresh-report-2026-07
  - anthropic-building-effective-agents
  - willison-lethal-trifecta
  - anthropic-pricing-2026
last_verified: 2026-07-17
---

# Program capstone: synthesis, final quiz, flashcards, and the send-off

This is the last file of the course. It does three things: pulls the whole
program into one synthesis, tests you across all eight blocks, and closes.

## The whole program in one arc

You learned one capability with a shape: take a real problem, decide whether AI
fits it, build the smallest thing that solves it, prove it works, package and
price it, launch it, monetize it, grow it, and systematize the operation so it
runs without you. Eight blocks, one sentence. [[01-mon-the-whole-map|Monday's map]] draws the wiring; [[02-tue-the-master-build-checklist|Tuesday's checklist]] turns it into a self-audit.

Under the blocks ran five through-lines that did not decay: evidence over vibes,
unit-economics discipline, anti-slop, eval-gating, and canonical-homes. Those,
plus the [[03-wed-the-durable-principles|14 durable principles]], are what you
actually keep. Everything fact-shaped — model names, prices, tool features —
you now treat as a dated claim with a short half-life, re-verified on a cadence
you built in [[04-thu-staying-current-re-verification|Thursday]]. The proof this
matters is that the course itself was refreshed in July 2026 because its
three-month-old facts were already wrong in places, while its frameworks held.[^1]

The forward motion is [[05-fri-the-forward-path-next-90-days|Friday's plan]] and
[[06-sat-build-graduation-audit|Saturday's artifact]]: a scored audit, a dated
three-sprint quarter, a principles one-pager, and a re-verification schedule. If
you did the week, you are not holding notes. You are holding a plan.

## Final quiz (15 questions, across all 8 blocks)

Take it cold. No re-reading first. Answers below.

1. What is the durability test that separates a first-principle from a fashion?
2. Name the five through-lines that ran the entire course.
3. The July 2026 refresh found the course's "skeleton sound, skin three months
   old." Which specific layers decayed, and which held?
4. State Simon Willison's lethal trifecta and the only durable fix.
5. Why is "compute margin under real COGS" a durable principle even though its
   inputs (token prices) change monthly?
6. What is the difference between a growth funnel and a growth loop, and why does
   the distinction matter?
7. Anthropic's agent guidance says to add agentic complexity only when ____.
   Complete and explain.
8. On the master checklist, why should "Validated" gaps usually be closed before
   "Systematized" ones?
9. What is the single highest-leverage action for a business at the "Idea" stage,
   and what is the failure mode it counters?
10. Why is a confident AI answer about a fast-moving fact a lead rather than a
    verification?
11. What is the `_last_verified` habit, and what problem does it solve?
12. State the honest position on agency-vs-product as the 2026 path (not the false
    binary).
13. Retention-first: what does growth compound on top of, and what does that
    compound on top of?
14. Why does eval-gating make a build "shipped" rather than "demoed"?
15. Name three decaying facts every AI operator should re-verify monthly, and one
    that never needs re-verification.

### Answer key

1. Would the claim still be true under a 10× cheaper model, a different vendor,
   and a tool you have never heard of? If yes, principle; if it is an artifact of
   today's prices, limits, or platform rules, fashion.
   ([[03-wed-the-durable-principles|Wed]])
2. Evidence over vibes; unit-economics discipline; anti-slop; eval-gating;
   canonical-homes / no-re-teaching. ([[01-mon-the-whole-map|Mon]])
3. **Decayed:** model names, prices, benchmarks, tool features, commands, API
   surfaces. **Held:** frameworks, failure taxonomies, eval discipline, the
   reasoning.[^1]
4. Private data access + exposure to untrusted content + ability to exfiltrate.
   The durable fix is to remove one leg; you cannot safely keep all three.[^2]
5. The inputs decay but the *discipline of recomputing margin against current
   inputs* does not. The refresh caught cost math 3× off precisely because prices
   moved and no one recomputed.[^3]
6. A funnel is refilled by hand and leaks; a loop's output feeds its own input and
   compounds. It matters because loops are assets and funnels are labor.
   ([[block-6-launch-monetization/week-17-feedback-metrics-setup-retargeting-or-re-engagement--growth-hacking-referral-loops/03-wed-growth-loops-vs-funnels|Week 17]])
7. ...only when it measurably improves the outcome. Start with the simplest thing
   that works and let evidence justify each added layer.[^4]
8. Building and systematizing something no one has validated is expensive
   procrastination; the audit ranks gaps by revenue blocked, and un-validated bets
   block the most. ([[02-tue-the-master-build-checklist|Tue]])
9. Get one person to pay (a payment or a paid pilot). It counters the failure mode
   of building more instead of selling what you have.
   ([[05-fri-the-forward-path-next-90-days|Fri]])
10. The model states facts from training data with full confidence, including
    stale prices and retired model names; on fast-moving facts you must confirm
    against a primary source before acting. ([[04-thu-staying-current-re-verification|Thu]])
11. Dating every decayable claim so trust becomes a function of age against
    half-life. It solves the silent-rot problem: undated facts are the ones that
    quietly go wrong.
12. Not a binary. Start where cash is fastest (services, ~70–80% margin) and
    migrate toward where margin is highest (product, ~90%+); the durable asset is
    the productized IP, and opportunity-size claims are contested projections.[^5]
13. Growth compounds on retention; retention compounds on a product people would
    be genuinely upset to lose.
14. Without a defined pass bar and a measurement, you have shown a demo, not
    shipped a product; evals are what let you claim it works.
15. Monthly: model prices, model names/defaults, platform/compliance rules (also
    fine quarterly). Never: the durable principles (e.g., retention-first).

**Scoring:** 13–15 you own the program; 10–12 reread your weakest block; below 10,
the gap is usually the engineering middle (Blocks 3–5) or the durable principles —
not the recent material.

## Flashcards — the durable core (30 cards)

Q: The one-sentence version of the whole course?
A: Take a real problem, decide if AI fits, build the smallest solution, prove it,
package and price it, launch, monetize, grow, and systematize so it runs without
you.

Q: The durability test?
A: Would it still be true under a 10× cheaper model from a vendor you have never
heard of? Yes → principle. No → fashion.

Q: The five through-lines?
A: Evidence over vibes; unit-economics discipline; anti-slop; eval-gating;
canonical-homes.

Q: Principle 1 (the most valuable skill)?
A: Decide whether AI fits before you build; better models widen the fit but never
remove the judgment.

Q: Why is "margin under real COGS" durable if prices change monthly?
A: The inputs decay; the discipline of recomputing against current inputs does
not.

Q: Price on ____, not ____.
A: Value, not cost. Cost sets the floor; value sets the price.

Q: Retention-first, in one line?
A: Growth compounds on retention; retention compounds on a product people are
upset to lose.

Q: Loops vs funnels?
A: Funnels leak and need hand-refilling (labor); loops feed themselves and
compound (asset).

Q: Context engineering, durably stated?
A: Control what the model sees; deciding what enters the window is the lever at
any window size.

Q: Eval-gating?
A: Define the pass bar before you build, then measure; no eval, no ship.

Q: Simplicity-first rule (Anthropic)?
A: Start with the simplest thing that works; add agentic complexity only when it
measurably improves the outcome.

Q: Human-in-the-loop, where?
A: On the irreversible and expensive; automate the reversible and cheap. Draw the
line by cost-of-error.

Q: The lethal trifecta?
A: Private data + untrusted content + exfiltration ability. Remove a leg; you
cannot keep all three.

Q: Reliability is ____, not ____.
A: Engineering, not prompting. Retries, idempotency, monitoring, graceful
failure.

Q: Canonical homes principle?
A: Every price, procedure, and spec lives in one authoritative place, referenced
everywhere.

Q: Distribution, durably?
A: A first-class problem; owned audience, community, and a lead engine survive
product pivots.

Q: What decays in weeks?
A: Model names, prices, context limits, tool features, commands, platform rules.

Q: What holds for years?
A: Principles, failure taxonomies, threat models, eval discipline, unit-economics
reasoning.

Q: The `_last_verified` habit?
A: Date every decayable claim so trust is a function of age against half-life.

Q: Re-verification cadence by half-life?
A: Prices/models monthly; platform/competitor quarterly; benchmarks ~2 months;
principles never.

Q: Verify against ____, never ____.
A: Primary sources (two for load-bearing claims); never memory or a single
snippet.

Q: A confident AI answer on a fast-moving fact is a ____.
A: Lead to verify, not a verification.

Q: What did the July 2026 refresh prove?
A: Skeleton sound, skin three months old: frameworks held, facts decayed.

Q: The false binary of 2026?
A: Agency vs product. The real answer is the sequence: services first (cash),
product later (margin).

Q: Highest-leverage action at "Idea" stage?
A: Get one person to pay; counters building-instead-of-selling.

Q: Highest-leverage action at "Launched" stage?
A: Systematize yourself out of the bottleneck via SOPs and delegation to
person/agent.

Q: The perpetual-learner trap?
A: Consuming more instead of shipping; the cure is a shipping cadence with a
public deadline.

Q: When to raise (default for a solo AI operator)?
A: Usually don't; raise only if capital-constrained, not validation-constrained.

Q: The honest probability frame?
A: Base rate is low; execution of the discipline moves it materially; the biggest
lever is whether you ship at all.

Q: What is the graduate's real compounding asset?
A: Judgment about what good output looks like — taste, relationships, SOPs,
community — not any model's weights.

## The send-off

You started 26 weeks ago able to prompt a model. You end able to run the whole
motion from problem to systematized business, and — more durably — able to tell
what you know from what you hope, and what is true from what is merely current.

The field will keep moving. Some of what you learned is already wrong; more of it
will be wrong by the time you read this. That is not a failure of the course. It
is the condition of the work, and you now have the one skill that survives it: you
re-verify, you keep the principles, and you ship anyway.

Hold the standard the course held. Evidence over vibes. Margin computed, not
assumed. A pass bar before you ship. One canonical home for every truth. A date
on every fact. If you keep those, you do not need this course again, and that was
the point.

Now close the vault and go get one person to pay.

_Program complete._

## Citations

[^1]: AI Pro-level Course, "July 2026 Content Refresh — Master Findings Report," internal, 2026-07-17 — skeleton sound, skin three months old; decay in model names/prices/benchmarks/tool features, frameworks held. [[00-program/_refresh-2026-07-master-report|Master report]].
[^2]: Simon Willison, "The lethal trifecta for AI agents," simonwillison.net/2025/Jun/16/the-lethal-trifecta/ — remove one leg; all three together is unsafe.
[^3]: Anthropic, "Pricing," platform.claude.com/docs/en/about-claude/pricing — current per-Mtok rates; the refresh caught prior cost math ~3× off after prices moved. (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)
[^4]: Anthropic, "Building effective agents," anthropic.com/research/building-effective-agents, Dec 2024 — add agentic complexity only when it measurably improves outcomes.
[^5]: Agency-vs-SaaS 2026 operator analysis — services ~70–80% margin, product ~90%+; opportunity-size claims contested; reported across fluxio.dev and lootr.io, Jul 2026. (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

_last_verified: 2026-07-17_
