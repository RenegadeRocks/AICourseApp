---
type: week-overview
block: block-2-ai-employees
week: week-03
title: 'Week 3 — Building Elegant Landing Pages & How to Build Micro-Prototypes'
live_sessions:
  - '2026-06-06 — Building Elegant Landing Pages'
  - '2026-06-07 — How to Build Micro Prototypes'
study_window: 2026-06-01 to 2026-06-07
last_verified: 2026-07-17
---

# Week 3 — Landing pages and micro-prototypes, treated as one pipeline

## The thesis of this week

The cheapest, fastest piece of software you will ever ship this year is a landing page attached to a micro-prototype. Not because it is small, but because it is the one artifact that forces every upstream decision — positioning, desire, audience, mechanism, pricing, channel — to collapse into a single observable event: the visitor either converts or they do not.

Week 3 treats the landing page and the prototype behind it as **one instrument**, not two artifacts. A landing page without a prototype is a brochure. A prototype without a landing page is a demo with no denominator. The operator move is to build both, wire them to an event model, decide the go/no-go threshold *before* traffic arrives, and let the data — not taste — close the loop.

Most builders stop at "looks clean, reads well." That is L2. L3 is knowing the conversion math, the binomial CI math, the specific failure modes of v0 vs Lovable vs Bolt vs Replit, the seven-variable design brief that survives tool handoff, the pretotyping rung that matches your risk, the 4–8 hour shipping pipeline, and the legal envelope around session replay and fake-door pages. That is this week.

## Who this week is for

You have shipped at least one thing using an AI code-gen tool. You have paid for v0 or Lovable or Bolt or Replit (or all four) at some point. You know what a `shadcn` primitive is, even if you haven't named it that. You've stared at a page that "looks fine" and wondered why nobody is clicking. You've also, at some point, built something in 30 minutes that would have taken a 2023 engineering team two sprints — and you've realised that the speed is not the hard part. The hard parts are **what to build**, **how to know it worked**, and **when to kill it**.

This week replaces the vibes answers to those three questions with mechanical ones.

## Shape of the week

Six paired deep-dives plus a synthesis day. Each day is ~90–120 minutes of reading plus ~45–90 minutes of hands-on work (some on paper, some in Claude Code, some across v0/Lovable/Bolt, some in PostHog).

| Day | Topic | One-line payoff |
|-----|-------|-----------------|
| Mon | The landing page as a conversion machine | Read any landing page as seven elements and four layers; compute the revenue ceiling of a 0.5-point lift before writing a line of copy. |
| Tue | How v0, Lovable, Bolt, and Replit actually work | Pick a tool in under 60 seconds on the evidence of four architectural bets — not four flavors of the same thing. |
| Wed | Design-system literacy for operators who don't draw | Compress "make it look like Linear" into a seven-variable brief that survives cross-tool handoff, OKLCH included. |
| Thu | The micro-prototype ladder | Name your rung — smoke, fake-door, concierge, Wizard-of-Oz, MVP — and size the sample with a Wilson interval, not a feeling. |
| Fri | The 4–8 hour shippable-prototype pipeline | Use Claude Code as orchestrator, v0/Lovable as UI shop, Figma Make for assets, n8n for glue, PostHog for truth — with three verbatim-pasteable prompts. |
| Sat | Validation instrumentation | Define the event model, CI threshold, session-replay legal envelope, and AI-moderated-interview script *before* traffic arrives. |
| Sun | Synthesis, quiz, flashcards | Four collapse modes, thirteen mental moves, twenty questions, fifty-plus cards. |

## Why these six topics belong together

They compose into a single operating loop, not a grab-bag of "landing-page tips" and "prototype tips":

1. **Mon** fixes the anatomy and the math of the instrument you will ship.
2. **Tue** fixes the tool you will build it in (and why the commodity-vs-envelope axis matters once the model itself is commoditised).
3. **Wed** fixes the taste brief, so the output of Tuesday's tool stops looking like a Vercel template and starts looking like a considered page.
4. **Thu** fixes the experimental design — which rung of Savoia's ladder you are actually on, and what Torres's assumption map says you should be testing.
5. **Fri** is the integration day — a literal 0:00→4:40 shipping diary that composes Mon + Tue + Wed + Thu into one pipeline with three reusable prompts.
6. **Sat** closes the loop — event model, binomial CI, session-replay legal review, Mom-Test-hardened AI interview script, pre-registered go/no-go.

By Sunday, you have a repeatable artifact: a one-page brief, a pipeline, and a measurement layer that together produce a credible "ship / kill / iterate" decision in under one working day.

## What "L3 depth" means in this week

Every deep-dive this week engages five things:

1. **At least one live controversy in the field.** Shapiro's Desire − (Labor + Confusion) vs Laja's four-layer messaging hierarchy; commodity-vs-envelope between Klinger and Rauch; shadcn wholesale-copy vs plunder-for-primitives; Cagan's "minimum viable product bar" vs Savoia's ladder; AI-moderated interviews (Outset/Nestlé "10× reach, 2× depth") vs NN/g 2024 and Pearson May 2025 methodological critiques.
2. **Citations dated after January 2024.** Unbounce CBR 2024 plus the mid-2026 CRO Intelligence Report (8.1% median), Vercel v0 2026 full-stack rebuild notes, Lovable disclosures ($10M-in-60-days through the 2026 $500M-ARR/$13.2B-talks arc), Anthropic Claude Code / Claude Design metrics, CPPA dark-patterns advisory 2024, Loeb & Loeb session-replay advisory July 2025, Clarity EEA October 2025 enforcement, Strella Series A, Listen Labs Series B, Outset Series B.
3. **Runnable experiments that produce numbers you can see.** A cross-tool bake-off (same brief, four tools, same rubric). A seven-variable design brief scored against a live target page. A 4-hour shipping diary you actually run. A Wilson-interval table for 6/50, 12/100, 60/500.
4. **Operator-level specifics with numbers.** TruckersReport 79.3% lift; NeuroMD 55.3%; Vercel agents driving >50% of deploys (mid-2026); Lovable $500M ARR at ~146 people (2026); Replit ~$525M annualized / $9B (2026, on Agent 3); Bolt's Standard/Max agents and Aug 3 2026 v1 cutoff; 43% AI-code redebug rate; Buffer's 4-day-to-paying-customer two-page smoke test; Superhuman's concierge onboarding (~2 hours per session, tens of thousands of customers); Wilson interval widths (18.2pp at n=50, 5.7pp at n=500).
5. **A reviewer lens with named technical disagreement.** Each lesson names paragraphs that a Julian Shapiro, Peep Laja, Guillermo Rauch, Anton Osika, Adam Wathan, shadcn, Rauno Freiberg, Teresa Torres, Alberto Savoia, Marty Cagan, Rob Fitzpatrick, Ronny Kohavi, Boris Cherny, Erik Schluntz, or Simon Willison would push back on — and what they would specifically argue instead.

## How to study this week

Each day, in priority order if you are short on time:

1. **Run the experiment or the shipping diary.** Mon's conversion-math table, Tue's four-tool bake-off, Wed's seven-variable brief, Thu's rung-selection worksheet, Fri's 4-hour ship, Sat's event-model instantiation. This is where the capability builds.
2. **Read the "Must-read" citations.** Usually three to five primary sources per lesson — Shapiro's handbook, Unbounce CBR, Refactoring UI, Savoia, Torres, Fitzpatrick, Kohavi, the PostHog/Loeb/CPPA compliance triad.
3. **Do the problem set.** Some are diagnostic (score three AI-services pages against the seven-element anatomy). Some are generative (write your three reusable prompts). Some are decision exercises (pick the rung, pre-register the threshold).
4. **Read the lesson prose.** The prose is scaffolding for the first three. Skimming the prose alone is skimming the week.

The mix of mediums is deliberate. Some problems want you in Claude.ai with pen and paper so you *feel* the math. Some want you driving Claude Code through a 4-hour ship. Some want you comparing v0 and Lovable side-by-side. Some want you reading a Series A press release critically. Different kinds of understanding require different kinds of work.

## The Saturday and Sunday live sessions

The cohort has live sessions on 2026-06-06 (landing pages) and 2026-06-07 (micro-prototypes), with a resource drop 2026-06-08 and office hours 2026-06-11. They are bonuses. The lessons in this vault are the primary instruction — each one is a standalone masterclass. If you miss a live session, nothing in the vault is incomplete; the vault is already the course.

## What you will own by Sunday

- A seven-element + four-layer reading of any landing page you encounter, with the revenue-ceiling math to decide whether a 0.5-point lift is worth iterating for.
- A 60-second decision rule for v0 vs Lovable vs Bolt vs Replit, grounded in architectural bet, not vibe.
- A seven-variable design brief that survives handoff between any two of those tools.
- A named rung on Savoia's ladder for your current riskiest assumption, with a Torres-style assumption map behind it.
- Three verbatim-pasteable prompts (SPEC BRIEF, UI BRIEF, GLUE+INSTRUMENTATION BRIEF) and a 0:00→4:40 shipping diary you have run at least once.
- An event model, a Wilson-interval-sized sample plan, a session-replay legal checklist, and a Mom-Test-hardened AI interview script — all pre-registered as a go/no-go rule before your first visitor arrives.

By Monday of Week 4, you should be able to turn any assumption about any audience into a measurable experiment in under a working day, and kill it — or double down on it — with evidence rather than conviction.
