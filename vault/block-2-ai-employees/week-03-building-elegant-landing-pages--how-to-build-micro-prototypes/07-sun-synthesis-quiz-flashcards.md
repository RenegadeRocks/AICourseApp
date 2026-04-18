---
type: synthesis
block: block-2-ai-employees
week: week-03
day_of_cycle: 7
day_name: sun
session_slug: week-03-synthesis
title: 'Week 3 Synthesis — The landing-page × prototype pipeline'
study_date: 2026-06-07
date_due: 2026-06-07
tags: [synthesis, quiz, flashcards, landing-pages, prototypes, v0, lovable, bolt, replit, claude-code, shadcn, pretotyping, posthog, conversion, validation]
sources:
  - unbounce-conversion-benchmark-report-2024-25
  - shapiro-startup-handbook-landing-pages
  - anthropic-claude-code-agent-teams
  - anthropic-advanced-tool-use-programmatic-2025
  - anthropic-multi-agent-research-system
  - shadcn-ui-v0-integration
  - refactoring-ui-wathan-schoger
  - savoia-pretotyping-techniques
  - pretotyping-org
  - torres-producttalk-ost
  - fitzpatrick-mom-test
  - posthog-pricing-2025
  - microsoft-clarity-docs
  - kohavi-trustworthy-online-experiments
  - morgan-lewis-ai-contracts-2026
last_verified: 2026-04-17
word_count_target: 3800
---

# Week 3 Synthesis — The landing-page × prototype pipeline

## The one-sentence thesis of this week

The six topics you covered this week — the anatomy of a landing page as a measurable conversion function (Mon), how v0/Lovable/Bolt/Replit actually translate prompts into UI and where each fails (Tue), the seven taste-layer variables that separate a Vercel template from a Linear page (Wed), the six-rung validation ladder from pretotype to MVP (Thu), the 4–8 hour Claude-Code-orchestrated prototype pipeline (Fri), and the measurement layer that decides whether a prototype actually validated anything (Sat) — all decompose into a single operator pipeline: **hypothesis → conversion anatomy → tool pick → taste brief → rung choice → 4-hour ship → instrumentation → go/no-go**. Block 1 Week 1 taught you how to *sell* an AI project. Block 2 Week 3 is the first of six weeks teaching you how to *build* one — and the deliverable that almost every first AI engagement ships first is a conversion surface, so this week's competence is load-bearing for everything that follows.

---

## The unifying frame: a prototype is a signed contract with reality, not a demo

Everyone new to shipping AI workers has the same quiet fantasy: you sit down in v0 for an afternoon, the UI is beautiful, the page goes live, a few visitors sign up, and the hypothesis is "validated." What Week 3 documents — with operator numbers — is that this fantasy collapses in four specific places, and each day's lesson is the defence against one of them.

- **Collapse 1 — the page converts badly and you don't know why (Mon).** Unbounce's 2024/25 Conversion Benchmark Report (41,000 landing pages, 464 million visitors, 57 million conversions) pins the cross-industry median at **6.6%**, with SaaS at the floor (~3.8%) and events/entertainment at the ceiling (~12.3%).[^1][^2] Mobile is 83% of traffic but converts ~8% below desktop.[^1] Email traffic converts at 19.3%, Instagram paid social at 17.9%, display near the bottom.[^3] Copy written at 5th–7th-grade reading level hits 11.1% — nearly 2× the "professional/complex" rate of 5.3%, and "difficult words" correlate with a **–24.3%** conversion hit, a sharper negative than 2020's benchmark.[^2][^3] Without an anatomy — Julian Shapiro's hook → promise → proof → action, or Dunford's positioning-to-copy bridge — your "bad conversion" is a single uninterpretable number instead of a five-module diagnosis.[^4]

- **Collapse 2 — the tool produces plausible UI but wrong UI (Tue).** v0, Lovable, Bolt, and Replit Agent each translate prompts into UI through a specific pipeline. v0 leans on shadcn/ui + Tailwind + Vercel deploys (ui.shadcn.com explicitly ships "Open in v0" for every component)[^5][^6]; Lovable runs a plan → scaffold → iterate loop with Supabase integration[^7]; Bolt.new executes in-browser via StackBlitz WebContainers[^8]; Replit Agent uses a checkpoint-diff-commit loop.[^9] Each has a design-default gravity well ("Vercel-template aesthetic") and each has failure zones — v0 weakens on complex routing and multi-component state; Lovable weakens on nuanced taste; Bolt leaks context on larger codebases[^10]; Replit Agent struggles with bespoke design systems. If you pick the tool on brand rather than on task, you pay for the mismatch in iteration time.

- **Collapse 3 — the page looks AI-generated and the champion won't share it (Wed).** Refactoring UI's seven variables (typography, color, spacing, density, motion, imagery, voice — Wathan + Schoger, 2018 book, continuously updated)[^11], plus WCAG 2.2 (2024 Recommendation) on motion and contrast[^12], plus the shadcn/ui default model[^6], plus Rauno Freiberg's motion-as-medium writing[^13], give you enough variable-level vocabulary to audit a page and push it from "Vercel template" toward a specific aesthetic. Without that vocabulary, "make it more like Linear" is a vibe and your AI-gen tool bounces off it.

- **Collapse 4 — the prototype "validates" something the hypothesis didn't ask (Thu, Sat).** Alberto Savoia's pretotyping (Google, formalized in *Pretotype It*, 2014, still maintained at pretotyping.org) is a ladder of experiments ordered by cost: pretotype (paper / would-you-yourself), smoke-test landing, fake-door, Mechanical Turk / concierge / Wizard-of-Oz, painted-door, MVP.[^14] Each rung measures a different thing. Teresa Torres's Opportunity Solution Tree (Continuous Discovery Habits, 2021, updated posts on producttalk.org) imposes the discipline that a solution is only as good as the opportunity it connects to, and an experiment is only as good as the assumption it falsifies.[^15] Rob Fitzpatrick's *The Mom Test* is the script discipline that keeps interview signal from decaying into compliments.[^16] Without these three layers — ladder, tree, script — you get a page that hit 8% signup and you still don't know whether that's "validate" or "noise."

The pipeline below is how the six days chain. **Hypothesis** (from your Block 0 Week 3 JTBD work or Block 1 Week 2 niche) → **anatomy** (Mon: Shapiro modules + Unbounce industry baseline) → **tool** (Tue: v0/Lovable/Bolt/Replit/Claude Code, chosen on task profile not brand) → **taste brief** (Wed: the seven variables specified enough that three tools produce visually similar output) → **rung** (Thu: where on Savoia's ladder the hypothesis actually sits, and what the cheapest valid experiment is) → **ship** (Fri: Claude Code as orchestrator, v0/Lovable as UI shop, n8n or Cloudflare Workers as glue, Vercel as deploy, 4–8 hours wall-clock)[^17] → **measurement** (Sat: PostHog event model, session replay, AI-moderated interviews, binomial CIs, kill/level-up/iterate thresholds).[^18][^19] The pipeline is not a linear waterfall. The measurement layer feeds back into the anatomy (which module underperformed); the tool pick feeds back into the taste brief (which override the tool refuses); the rung choice disciplines the anatomy (a smoke test has no pricing module because the product doesn't exist).

The operator move this week installs: **a prototype is a signed contract with reality**. You tell it the hypothesis, the threshold, the kill-criterion, and the instrumentation *before* you ship. The prototype's job is to return a verdict, not to be a portfolio piece.

---

## Where each day's content goes forward

| This week's lesson | Underwrites in later weeks |
|---|---|
| Mon — The landing page as conversion machine | Every landing page you ship for yourself or a client in Blocks 2–4; every "why isn't my funnel converting" diagnosis; the copy layer for Block 2 Week 4 sales-agent outbound pages |
| Tue — How v0/Lovable/Bolt/Replit actually work | Every "which tool do I reach for" decision for the rest of Block 2; Block 2 Week 6 RAG-UI frontends; any tool-stack recommendation to a client or teammate |
| Wed — Design system literacy | Every brief you write to an AI-code-gen tool; every "this looks AI-generated" override; Block 2 Week 5 document-understanding UIs; Block 4 portfolio and brand work |
| Thu — The micro-prototype ladder | Every new product or feature validation you run; Block 2 Week 4 sales-agent concierge mode; any "should we build this" conversation with a client or cofounder |
| Fri — The 4–8 hour prototype pipeline | Every first-engagement deliverable in Blocks 2–4; the "discovery phase" artifact from Block 1 Week 1's four-phase SOW; any internal team capability demo |
| Sat — Validation instrumentation | Every prototype in Blocks 2–6; every "did this actually work" post-mortem; the measurement half of every SOW's kill-criterion gate (Block 1 Thu) |

Week 3 is the **build-and-measure skeleton** of Block 2. Week 4 will layer the sales-agent worker on top; Week 5 the document-understanding worker; Week 6 the RAG-driven knowledge worker. All three assume you can ship a conversion surface with instrumented measurement in one workday. If anyone asks "why did my AI-services discovery engagement feel like busywork," the answer is almost always a Week 3 rung they skipped.

---

## The week's key moves — the mental-move table

Thirteen highest-leverage moves drawn from the six lessons. Each row: the move, the mechanism, when to apply, when not to.

| # | Move | Mechanism | Apply when | Do NOT apply when |
|---|------|-----------|------------|-------------------|
| 1 | Treat the landing page as a five-module function, not a design canvas | Shapiro anatomy (hook → promise → proof → action) + Dunford positioning + Unbounce 2024/25 module-level benchmark data lets you diagnose which module under-performs instead of "the page doesn't convert" | Any page with a measurable outcome (signup, demo, purchase, waitlist) | Brand or narrative sites where the outcome is awareness, not conversion |
| 2 | Anchor your conversion target to an industry median, not a vanity number | Unbounce 2024/25 medians: overall 6.6%, SaaS ~3.8%, events ~12.3%, email traffic 19.3%, Instagram paid 17.9%, mobile 8% below desktop. Without the anchor, "our page converts at 4%" is meaningless | Planning any paid or owned campaign with a conversion goal | Pre-product smoke tests where the only useful signal is directional (n<200) |
| 3 | Write at 5th–7th-grade reading level for the hero, promise, and CTA | Unbounce 2024/25: 5th–7th grade hits 11.1% median vs 5.3% at college level. "Difficult words" correlate with a –24.3% conversion hit, a 62% stronger negative effect than in 2020 | Any marketing surface aimed at a non-specialist buyer (most ICPs) | Highly technical surfaces where a specialist audience expects the jargon (AI infra APIs, compiler tooling) |
| 4 | Pick the AI-code-gen tool on task profile, not brand | v0 wins on shadcn-aesthetic polish + Vercel deploy; Lovable wins on full-stack scaffold with auth/db; Bolt wins on zero-setup + tight iteration loop on small apps; Replit on collaboration + deploy; Claude Code on orchestrator + bespoke design systems + custom glue | Any time you're starting a new prototype and haven't locked a tool on a prior run | Mid-prototype, where tool-switching cost usually exceeds the speed delta |
| 5 | Write the taste brief as a structured seven-variable specification | Refactoring UI's seven variables (type, color, spacing, density, motion, imagery, voice) — specified enough that three different AI-code-gen tools produce visually similar output. "Make it like Linear" is a vibe; "Inter 15px body, 32px display, 6.6 contrast ratio on body, 8px grid, compact density, zero motion above CTA, no stock photography, declarative voice" is a brief | Any AI-code-gen work where aesthetic coherence matters | Throwaway internal tools or data-heavy dashboards where function dominates |
| 6 | Adopt shadcn/ui wholesale for first-engagement prototypes; plunder for later ones | shadcn/ui ships copy-in-codebase components (you own the source, not an import), integrates with v0's "Open in v0" on every component page, and in late 2025 shipped Shadcn Create for preset-driven scaffolding. Cost of wholesale adoption on engagement #1 is ~0; cost of reinventing a component library is measurable in weeks | First 3–5 engagements, when compounding portfolio velocity matters more than component differentiation | Engagement #10+, where a named visual identity starts to matter as a moat |
| 7 | Place every hypothesis on Savoia's rung-ladder before writing a line of code | Six rungs — pretotype (paper / would-you) → smoke-test → fake-door → concierge / Wizard-of-Oz → painted-door → MVP — each measuring a different assumption (existence of want / clickthrough / willingness-to-action / willingness-to-pay / integration feasibility / scale). Skipping a rung is fine when you have a strong prior; skipping without one is the dominant failure mode | Every new product or feature hypothesis | Hypotheses already validated at a lower rung where the next rung's cost is below decision-reversal threshold |
| 8 | Write a single-sentence hypothesis with a success threshold before building | Torres OST discipline: outcome → opportunity → solution → experiment. An experiment without a numeric threshold can't return a verdict, so it will always "need more data" | Every prototype, every A/B, every paid campaign | Pure aesthetic / UX exploration where the goal is to generate options, not verdict |
| 9 | Run the 4-hour pipeline with Claude Code as orchestrator, not as coder | Boris Cherny / Anthropic's Claude Code documentation frames it as agent + subagents + MCP tools[^20]; Anthropic's 2025 Advanced Tool Use post explicitly positions programmatic tool calling (Claude writes code that calls tools in a loop) as more reliable than round-trip natural-language tool use. Orchestrator = reads hypothesis, scaffolds plan, briefs the UI tool, writes the glue, sets up instrumentation. You don't type components into v0 by hand; you brief Claude Code and let it brief v0 | Any prototype with >3 handoffs (hypothesis → UI → glue → deploy → instrumentation) | Single-file pages or throwaway tests where orchestration overhead exceeds the work |
| 10 | Instrument before you ship — event model first, UI second | PostHog event model (name + properties) + primary funnel + health metrics drafted in Claude Code before the page exists; instrumentation wired into v0/Lovable output during the build, not after launch. PostHog's 2025 free tier (1M events + 5k session replays + 1M feature-flag requests, $0) removes the cost excuse[^18][^21] | Every prototype | Paper pretotypes where no code ships |
| 11 | Read a funnel at N<200 as a Bayesian prior update, not an A/B test | Binomial 95% CI on 6/50 is roughly 4.7%–24.8%. On 12/100 it's 6.4%–20.2%. On 60/500 it's 9.3%–15.2%. Below N≈500 the CIs are too wide for point estimates; you're updating a prior, not measuring an effect. Treating a 6/50 as "12% converts" is how solo operators lie to themselves[^19] | Prototype funnels with <500 visitors | Post-product-market-fit A/B tests with adequate power (Kohavi's *Trustworthy Online Controlled Experiments* is the reference)[^22] |
| 12 | Add 5–10 AI-moderated or human-moderated interviews to any smoke test — quantitative alone is too thin at N<200 | Outset.ai / Maze AI Interviewer / Strella / Listen Labs give you moderated qualitative at N>=5 in hours, not weeks.[^23] Rob Fitzpatrick's Mom Test discipline (past behavior > hypotheticals, no leading questions, specific over general) still governs the script quality.[^16] Torres is explicit: weekly customer conversations are the unit, not one monthly survey[^15] | Early-stage prototypes where N<200 | Large-N later-stage tests where qualitative is a complement, not a primary signal |
| 13 | Define kill / iterate / level-up thresholds before traffic hits the page | A prototype without pre-committed thresholds drifts into "let's run more traffic." Pre-committed thresholds — e.g., "< 2% smoke-test opt-in for 200+ visitors → kill; 2–6% → iterate hero and re-run; >6% → level up to fake-door" — turn the measurement layer from a vibe into a verdict | Every prototype, every phase-gate | Pure research / generative UX where the point is exploration, not verdict |

---

## 20 quiz questions

*Span: Mon–Sat. Mix: 8 recall, 8 apply, 3 prompt/schema completion, 1 controversy-defense. Answers at end.*

---

**Q1 (Recall)** — Name the four components of Julian Shapiro's hero framework and the Unbounce 2024/25 cross-industry median landing page conversion rate.

**Q2 (Recall)** — State the Unbounce 2024/25 device split: mobile share of traffic, desktop vs mobile conversion delta.

**Q3 (Recall)** — What copy reading-grade level produces the highest Unbounce 2024/25 median conversion rate, and what's the conversion rate delta vs college-grade writing?

**Q4 (Recall)** — Name v0, Lovable, Bolt, and Replit Agent's default tech stack or execution model.

**Q5 (Recall)** — Name Refactoring UI's seven taste-layer variables.

**Q6 (Recall)** — List Savoia's six-rung validation ladder from cheapest to most expensive.

**Q7 (Recall)** — State PostHog's 2025 free-tier limits for events, session replays, and feature flags.

**Q8 (Recall)** — Name the four tiers of Teresa Torres's Opportunity Solution Tree.

**Q9 (Apply)** — A mid-market SaaS prototype landing page is converting at 3.1% on 1,800 visitors. The industry median is SaaS ~3.8%. Given the Unbounce 2024/25 module-level breakdown and the Shapiro anatomy, name the single module you would audit first and the specific diagnostic you would run before making any change.

**Q10 (Apply)** — You're briefing Claude Code to generate a hero for an AI-services landing page for fin-services ops leaders. Write the taste-brief sentence (≤60 words) that specifies all seven variables precisely enough that v0, Lovable, and Claude Code would produce visually similar output.

**Q11 (Apply)** — Your hypothesis: "Fin-services ops leaders will pay $2,500 for a 2-week AI pilot-rescue diagnosis." Place this hypothesis on Savoia's ladder and design the cheapest valid experiment for the correct rung (≤150 words: rung, deliverable, success threshold, N required, sunset criteria).

**Q12 (Apply)** — You've shipped a smoke-test landing page. 6 signups out of 47 visitors. Compute the 95% binomial CI (approximate) and write one sentence on what you should infer vs what you should not infer.

**Q13 (Apply)** — For the 4-hour prototype pipeline, specify the exact handoff protocol between Claude Code and v0: what Claude Code produces, what v0 consumes, what Claude Code does with v0's output.

**Q14 (Apply)** — Design the PostHog event model for a smoke-test landing page with the funnel: landing view → hero CTA click → form open → form submit → confirmation page. Name the events, the key properties, and the two health metrics you'd track alongside the funnel.

**Q15 (Apply)** — Write a 7-question AI-moderated interview script for a 15-minute validation call with a fin-services ops director who just signed up to your waitlist. Every question must pass The Mom Test.

**Q16 (Prompt completion)** — Complete this Claude Code orchestrator prompt so it's runnable for a reader who has the Tuesday brief ready:
```
Given this hypothesis: [HYPOTHESIS].
Given this ICP: [ICP].
Build the 4-hour prototype: …
```
Fill in the rest so the prompt specifies the UI tool, the design brief, the glue, the instrumentation, the deploy target, and a stop condition.

**Q17 (Schema completion)** — Complete this JSON schema for a prototype spec that Claude Code can consume:
```json
{
  "hypothesis": "",
  "rung": "",
  "success_threshold": {"metric": "", "value": 0, "N": 0},
  …
}
```
Add ≥6 more fields that make the spec sufficient for a Claude Code build.

**Q18 (Schema completion)** — Write a kill/iterate/level-up threshold rubric as a decision table (4 columns: signal, kill, iterate, level-up) for a smoke-test landing page where the hypothesis is "mid-market ops leaders will opt-in for a waitlist at >6%."

**Q19 (Controversy-defense)** — Position: "In 2026, AI-code-gen tool choice is a commodity question — v0, Lovable, Bolt, and Replit converge within a quarter, and none of them represents a durable moat for a builder." Take a side with two named-operator citations.

**Q20 (Controversy-defense)** — Position: "AI-moderated interviews (Outset, Strella, Listen Labs) produce genuine qualitative signal equivalent to human-moderated sessions at 5× lower cost, and solo operators should default to them." Take a side using the 2024–25 operator evidence.

---

## Answers

**Q1** — Hook, Promise, Proof, Action (Shapiro's hero structure, per julian.com Startup Handbook Landing Pages guide). Unbounce 2024/25 cross-industry median: **6.6%** across 41,000 landing pages, 464M visitors, 57M conversions.

**Q2** — Mobile = **~83%** of traffic. Desktop converts **~8%** higher than mobile. The gap represents >1.3M lost conversions industry-wide per Unbounce's 2024/25 framing. Operator implication: test mobile-first; desktop-first design is a 2015 artifact.

**Q3** — **5th–7th grade** reading level, median conversion **11.1%**. College-grade writing medians at **5.3%**. Delta ≈ 2.1× (or +110% relative). "Difficult words" in copy correlate with a **–24.3%** conversion effect — 62% stronger negative effect than the 2020 benchmark. Practical rule: run the hero, promise, and CTA through a readability check before shipping; cut polysyllables.

**Q4** — v0: Next.js + shadcn/ui + Tailwind, deployed on Vercel. Lovable: plan → scaffold → iterate loop; full-stack with Supabase integration; Vite/React default. Bolt.new: in-browser StackBlitz WebContainer execution (no local env). Replit Agent: checkpoint-diff-commit model with Replit's hosted dev environment, live deploy targets via Replit Deployments.

**Q5** — Typography, color, spacing, component density, motion, imagery, voice. (Refactoring UI, Wathan + Schoger.) Voice is often the one that gets dropped — copy *is* a design surface, not a layer on top of design.

**Q6** — (1) Pretotype — paper / would-you-yourself; (2) Smoke-test — landing page with "coming soon" + email signup; (3) Fake-door — button leads to survey/paywall instead of promised feature; (4) Concierge / Mechanical Turk / Wizard-of-Oz — manual fulfillment masquerading as product; (5) Painted-door — feature ghost-deployed inside an existing product; (6) MVP — functional, stripped-down version. (From Savoia, *Pretotype It* + pretotyping.org techniques summary.)

**Q7** — 1M analytics events / month; 5,000 session replay recordings / month; 1M feature flag requests / month. No credit card required. Above the free tier: $0.00005/event (~$50 per additional 1M events), $0.005 per replay recording. (posthog.com/pricing, 2025.)

**Q8** — Outcome (the goal, measurable); Opportunities (customer needs/pains that, if addressed, move the outcome); Solutions (ideas to address opportunities); Experiments (tests that falsify or support a solution). (Torres, *Continuous Discovery Habits*, producttalk.org OST post.)

**Q9** — Module: the **hero** (H1 + sub + CTA) — because it controls the <5-second comprehension window and every downstream module is gated by whether the hero held attention. Diagnostic: session-replay audit (Microsoft Clarity or PostHog session replay, both free tiers) on 20+ sessions to see scroll depth + rage-click heatmap before the CTA, *then* a Claude.ai buyer-persona critique of the hero copy against Shapiro's hook-promise-proof-action — specifically, does the H1 make a promise? does the sub add proof? Do not rewrite until you've seen the replay; rewriting without observation is guessing.

**Q10** — Example: *"Hero: Inter 16/64px, one display weight (Semibold), neutral cool-gray 950 on paper-white #FAFAFA (WCAG 2.2 AAA body contrast ≥ 7:1 — stricter than the 4.5:1 AA default because fin-services buyers scan under fluorescent light), 8px grid with 96px vertical hero padding, dense single-column composition, zero motion above the CTA (WCAG 2.2 C39 reduced-motion safe), no stock photography, declarative voice with one concrete number in the H1, CTA as solid primary button not ghost."* — ~70 words, specifies all seven variables, produces visually similar output across v0, Lovable, Claude Code. Note: specify the WCAG bar explicitly — AAA (7:1) vs AA (4.5:1) vs AA Large (3:1) — because AI-gen tools default to AA and quietly ship 4.6:1 body text if you don't pin it.

**Q11** — Rung: **concierge / Wizard-of-Oz** (not smoke-test — the question is willingness-to-pay, not willingness-to-signup). Deliverable: a three-page landing page describing the pilot-rescue diagnosis (Shapiro anatomy), a $1 stripe checkout for a "book a diagnosis call" calendar slot, and YOU personally deliver the first 3–5 diagnoses manually with Claude Code assistance. Success threshold: ≥3 paid bookings at $250 (the $2,500 full price is deferred until you've validated the $250 signal) in the first 200 qualified ICP visitors. N required: ~200 from paid LinkedIn + warm outbound (Block 1 Week 1 list). Sunset: if <1/200 book at $250, kill the hypothesis or pivot the offer; if 1–2/200, re-work the hero and re-run; if ≥3/200, level up to a fixed-price $2,500 pilot-rescue engagement for the next 5 bookings.

**Q12** — 6/47 = 12.8%. Approximate 95% Wilson CI ≈ **5.9%–25.2%**. One-sentence read: *"The point estimate sits above any reasonable kill threshold, but the interval spans a factor-of-four range, so I should treat this as a weak positive prior and commit to a second batch of 150–300 visitors before making a go/no-go decision — not as a 12% conversion rate."*

**Q13** — Claude Code produces: (a) the structured design brief (seven taste variables specified), (b) the component tree (hero, proof strip, how-it-works, pricing, CTA stack, footer), (c) the copy — H1, sub, CTAs, proof lines — pre-written and readability-checked. v0 consumes: the brief + component tree + copy, emits a shadcn/ui-based Next.js page with Tailwind tokens. Claude Code then takes v0's output, wires the PostHog instrumentation, adds the n8n / Cloudflare Worker for form submission, runs a readability + WCAG audit, and either commits to main or returns a diff list for the operator to review. Each handoff is a file, not a chat.

**Q14** — Events: `landing_viewed` (props: referrer, utm_source, utm_campaign, device, viewport); `hero_cta_clicked` (props: cta_variant, scroll_depth_at_click, time_on_page); `form_opened` (props: cta_variant, trigger); `form_submitted` (props: email_domain_category, form_variant); `form_errored` (props: error_type, field); `confirmation_viewed`. Health metrics: (1) `bounce_rate` (< 5 s single-event sessions, target < industry median ~40%), (2) `time_to_cta_click` (median seconds from landing_viewed to hero_cta_clicked, target < 30s for mobile).

**Q15** — Example script (Mom Test-compliant: past behavior, no leading, no pitching):
  1. *"Walk me through the last time your team had to triage a failing AI project — what actually happened that week?"*
  2. *"Who flagged it? What did they do first? What did you do?"*
  3. *"What was the cost of waiting a week to fix it, in dollars or hours — as best you can estimate?"*
  4. *"What have you tried so far to prevent this from recurring? What worked, what didn't?"*
  5. *"Who, if anyone, did you pay to help — and what did they charge and deliver?"*
  6. *"If I handed you a 2-week diagnostic pilot that returned a written diagnosis + remediation plan, who else on your team would have to approve the spend?"*
  7. *"What would have to be true in the first 3 days of that engagement for you to recommend it internally?"*

**Q16** — Example completion:

```
Given this hypothesis: mid-market fin-services ops leaders will opt-in to a 2-week AI-pilot-rescue waitlist at ≥6% conversion.
Given this ICP: US fin-services firms $100M–$500M revenue, named AI champion, ≥1 failed AI pilot in last 18 months.
Build the 4-hour prototype:
 - UI: v0 with shadcn/ui, Next.js on Vercel. Brief: [paste the 7-variable taste brief].
 - Copy: H1, sub, three-step how-it-works, one case-study quote, one-line proof, CTA "Join the waitlist — we'll reach out within 48 hrs."
 - Glue: Cloudflare Worker accepting the form POST → Resend email list "pilot-rescue-waitlist" → Slack webhook to #validation → PostHog capture.
 - Instrumentation: PostHog events per the Sat event model (landing_viewed, hero_cta_clicked, form_opened, form_submitted, confirmation_viewed). Microsoft Clarity session replay as secondary.
 - Deploy: Vercel production domain pilot-rescue.[your-domain].com.
 - Stop condition: working URL + 5 test submissions flow end-to-end OR 4 hours elapsed, whichever comes first.
Output: URL, git repo, PostHog dashboard link, deploy log. If stop condition hits on time rather than test, name the single remaining blocker and propose the smallest possible fix.
```

**Q17** — Example:

```json
{
  "hypothesis": "",
  "rung": "",
  "success_threshold": {"metric": "", "value": 0, "N": 0},
  "kill_threshold":    {"metric": "", "value": 0},
  "iterate_threshold": {"metric": "", "value": 0},
  "icp": {"vertical": "", "size_band": "", "ai_maturity_stage": ""},
  "taste_brief": {"type": "", "color": "", "spacing": "", "density": "", "motion": "", "imagery": "", "voice": ""},
  "anatomy": {"hero": "", "proof": "", "objection": "", "pricing": "", "cta": ""},
  "event_model": {"events": [], "funnel": [], "health_metrics": []},
  "deploy_target": "",
  "sunset_date": ""
}
```

**Q18** — Example decision table:

| Signal | Kill (< X) | Iterate (X ≤ signal < Y) | Level-up (≥ Y) |
|---|---|---|---|
| Opt-in rate after N≥200 qualified visitors | < 2% | 2% – 6% | ≥ 6% |
| Time-to-CTA (median seconds mobile) | > 60s | 30s – 60s | < 30s |
| Bounce rate (< 5s single-event) | > 60% | 40% – 60% | < 40% |
| Qualitative (5+ interviews: willingness-to-pay confirmed) | < 1/5 | 1–2/5 | ≥ 3/5 |
| Decision | Kill the hypothesis OR pivot offer | Re-work hero + re-run 150–300 visitors | Fake-door / concierge next rung |

**Q19** — Defensible both sides, but current state leans **partial-moat, not full commodity**. Pro-commodity (Swyx / Shawn Wang on AI dev tools; Andreas Klinger "last-mile taste" thesis): tool features converge fast — v0, Lovable, Bolt, Replit all shipped similar "prompt-to-deployed-app" flows within 12 months; model capability is not owned by any tool vendor. Pro-moat (Guillermo Rauch on Vercel/v0 integration; shadcn/ui's copy-in-codebase model): the moat is design-taste corpus + integration depth. v0's "Open in v0" on every shadcn/ui component page + Shadcn Create (late 2025) + Vercel deploy creates a switching cost that Lovable/Bolt/Replit each have to rebuild. Synthesis: tool *features* are commoditizing; tool *stack integration* (Vercel + shadcn + v0) and tool-specific taste corpora are the durable differentiators, and the builder's moat is the library of taste briefs + prompt patterns + eval harnesses they reuse across tools — not the tool itself.

**Q20** — Refute as default, accept as complement. Named-operator evidence: Outset.ai / Maze AI Interviewer / Strella / Listen Labs customer-published case studies show useful signal at N=5+ in hours not weeks, particularly on structured topics with pre-defined branches. Teresa Torres (Continuous Discovery Habits, producttalk.org) is explicit that weekly human customer conversations are the unit of discovery — she has not endorsed AI-moderated as a replacement. Rob Fitzpatrick (Mom Test) frames the signal-integrity problem as *follow-up quality*: the human move is probing "tell me more about that" when the interviewee skims, and AI moderators in 2025 still demonstrably miss the beat on open-ended follow-up when the response is ambiguous. Operator stance: use AI moderation for structured branch-heavy scripts where the pre-planned follow-ups cover >80% of likely responses; use human moderation for early-stage exploratory interviews where the follow-up is where the insight lives. Cost delta does not justify replacement on the exploratory class.

---

## 40 flashcards

*Format: front ↔ back. Anki-importable. Concepts, numbers, named operators, controversies.*

1. Q: Unbounce 2024/25 cross-industry median landing page conversion? → A: **6.6%**, across 41k pages, 464M visitors, 57M conversions.
2. Q: Unbounce 2024/25 SaaS median conversion rate? → A: ~3.8% — the industry floor.
3. Q: Unbounce 2024/25 events/entertainment median? → A: ~12.3% — the industry ceiling.
4. Q: Mobile traffic share 2024/25? → A: ~83% of landing page traffic; desktop converts ~8% higher.
5. Q: Unbounce 2024/25 reading-grade impact? → A: 5th–7th grade = 11.1% median; college = 5.3%. Difficult words = –24.3% conversion hit, 62% stronger negative effect than 2020.
6. Q: Email traffic conversion rate (Unbounce 2024/25)? → A: 19.3% — highest of all channels. Instagram paid social 17.9%. Google paid search ~11.3%.
7. Q: Julian Shapiro's hero framework? → A: Hook → Promise → Proof → Action. Formula: *Purchase Rate = Desire – (Labor + Confusion)*.
8. Q: Shapiro on attention? → A: Visitors don't have short attention spans — they have short *consideration* spans. Hero must hook quickly to earn further reading.
9. Q: April Dunford's positioning components? → A: Competitive alternatives, unique capabilities, differentiated value, target segment, market category. (Block 1 Wk 1 Tue recap.)
10. Q: v0 default tech stack? → A: Next.js + shadcn/ui + Tailwind, deployed on Vercel. "Open in v0" on every shadcn/ui component page.
11. Q: Lovable's execution model? → A: Plan → scaffold → iterate loop; full-stack with Supabase integration; Vite/React default.
12. Q: Bolt.new's execution model? → A: In-browser StackBlitz WebContainer — no local dev env; pure client-side execution.
13. Q: Replit Agent model? → A: Checkpoint-diff-commit loop with Replit's hosted dev env; live deploy via Replit Deployments.
14. Q: Default aesthetic gravity well for AI-code-gen tools? → A: "Vercel template" — neutral gradient hero, rounded-2xl, medium contrast, sans-serif, blue accent. Override via explicit seven-variable brief.
15. Q: Refactoring UI seven variables? → A: Typography, color, spacing, component density, motion, imagery, voice. (Wathan + Schoger.)
16. Q: shadcn/ui model? → A: Copy-in-codebase components (you own source, not an import). Integrated with v0. Late-2025: Shadcn Create for preset-driven scaffolding.
17. Q: WCAG 2.2 motion rule? → A: Respect `prefers-reduced-motion`; no continuous/auto-playing motion above 5s without user control. 2024 W3C Recommendation.
18. Q: Savoia pretotyping definition? → A: Testing initial appeal + actual usage of a potential product by simulating core experience with smallest possible investment of time/money. Faster, cheaper, more revealing than prototyping.
19. Q: Savoia's six rungs? → A: Pretotype → smoke-test → fake-door → concierge/Mechanical-Turk/Wizard-of-Oz → painted-door → MVP.
20. Q: Mechanical Turk pretotype? → A: Replace the complex/expensive computer or machine with a human (behind the curtain). Wizard-of-Oz variant.
21. Q: Pinocchio pretotype? → A: Non-functional, "lifeless" version of the product — enough to test shape and carrying behavior.
22. Q: Fake-door pretotype? → A: Button / entry point that suggests the product/feature exists; click leads to survey, waitlist, or paywall that measures intent.
23. Q: Concierge pretotype? → A: Manual fulfillment masquerading as product — you deliver the "AI" by hand with Claude Code assistance before automating.
24. Q: Teresa Torres OST tiers? → A: Outcome → Opportunity → Solution → Experiment. From Continuous Discovery Habits.
25. Q: Rob Fitzpatrick Mom Test rule? → A: Talk about the other person's life, not your idea. Ask about past behavior, not hypotheticals. Specific > general. No leading questions.
26. Q: Anthropic Claude Code orchestrator model? → A: Five layers — MCP (connectivity), Skills (task knowledge), Agent (primary worker), Subagents (parallel workers), Agent Teams (coordination). Per Anthropic's "How we built our multi-agent research system" (2025), a multi-agent lead + Sonnet subagents outperformed a single Opus agent by +90.2% on Anthropic's internal research-task evals (the specific eval name is not publicly disclosed; cite as "internal research-task evals" when referenced).
27. Q: Programmatic Tool Calling (Anthropic 2025)? → A: Claude writes code that calls tools in a loop, processes outputs, controls what enters context. More reliable than natural-language tool round-trips.
28. Q: PostHog 2025 free-tier limits? → A: 1M events/mo + 5k session replays/mo + 1M feature-flag requests/mo. No credit card.
29. Q: PostHog post-free-tier pricing? → A: $0.00005 per event (~$50 per additional 1M). $0.005 per replay recording. Hard monthly spend caps available.
30. Q: Microsoft Clarity pricing? → A: Free, unlimited. Session replay + heatmaps. Primary tradeoff: Microsoft telemetry.
31. Q: AI-moderated interview platforms 2024/25? → A: Outset.ai, Maze AI Interviewer, Strella, Listen Labs. Structured branching works; open-ended follow-up lags human moderators.
32. Q: Binomial 95% CI shape for small N? → A: 6/50 ≈ 4.7%–24.8%. 12/100 ≈ 6.4%–20.2%. 60/500 ≈ 9.3%–15.2%. Below N≈500 CIs too wide for point estimates — you're updating a prior, not measuring an effect.
33. Q: Kohavi reference on A/B rigor? → A: Ronny Kohavi (ex-Airbnb / LinkedIn), *Trustworthy Online Controlled Experiments* (2020) — the reference for power calcs, sample size, and experiment design.
34. Q: n8n role in 4-hour pipeline? → A: Visual glue — form submit → email list → Slack webhook → PostHog event. Alternative: 50-line Cloudflare Worker or Vercel Edge Function for ops comfortable with code.
35. Q: 4-hour pipeline handoff order? → A: Hypothesis (Claude Code) → taste brief (Claude Code) → UI (v0/Lovable) → copy (Claude Code) → glue (Cloudflare Worker / n8n) → instrumentation (PostHog / Clarity) → deploy (Vercel).
36. Q: Stop condition for 4-hour ship? → A: Shippable URL + 5 end-to-end test submissions, OR 4 hours elapsed — whichever first. If time hits, name the single blocker and smallest fix.
37. Q: Prototype spec minimum fields (JSON)? → A: hypothesis, rung, success_threshold (metric/value/N), kill_threshold, iterate_threshold, ICP, taste_brief (7 vars), anatomy (5 modules), event_model (events/funnel/health), deploy_target, sunset_date.
38. Q: Kill-rate for AI POCs (IDC 2025)? → A: 88% never reach production. (IDC 2025 enterprise-AI survey, as cited in Block 1 Week 1 Thu lesson "SOW and kill-criteria" — reference, not re-taught here.)
39. Q: MIT NANDA 2025 pilot P&L? → A: ~95% of enterprise GenAI pilots produce zero measurable P&L impact. (MIT Project NANDA "The GenAI Divide" report, 2025; cited in Block 1 Week 1 Mon — reference only.)
40. Q: One-line rule for whether Week 3 is installed? → A: Before any prototype ships, you can name (a) the hypothesis + success threshold, (b) the rung on Savoia's ladder, (c) the 5 Shapiro modules in the anatomy, (d) the 7 taste variables in the brief, (e) the tool pick + why, (f) the PostHog event model with kill/iterate/level-up thresholds, (g) the 4-hour stop condition.

---

## Open questions — what's not settled this week

1. **Does the AI-code-gen taste corpus become the moat, or the commodity?** v0 + shadcn/ui + Vercel has the current lead on integration depth. Lovable's full-stack-with-auth is the rival bet. Bolt and Replit are betting on frictionless dev-env as the durable surface. Whether 2026–27 resolves into a Vercel-stack duopoly, a fragmentation into vertical specialists (e.g., Framer-style design-led, Retool-style internal-tool-led), or a collapse into model-level UX (Claude / GPT ship native UI generation) is unknown. Watch Vercel and Figma Config 2026 announcements.

2. **Does the 4-hour prototype pipeline generalize beyond SaaS landing pages?** The Claude Code → v0 → glue → instrumentation chain works well for conversion surfaces. Whether it extends cleanly to (a) document-understanding UIs with heavy file upload + preview, (b) voice-agent interfaces with real-time audio, (c) multi-step agentic workflows with tool use — is an active question. Week 5 and Week 6 of Block 2 will stress-test this.

3. **AI-moderated interviews at scale — signal or survey theater?** Outset / Strella / Listen Labs customer case studies show useful structured signal at N=5+. But Torres and Fitzpatrick have both (Oct 2024 / Mar 2025 posts on producttalk.org and momtestbook.com respectively) flagged the follow-up-probe gap. The 2026 operator stance: structured for known-branch exploration, human for genuine discovery. Revisit when 2026 customer data publishes.

4. **Fake-door ethics in 2026.** Every "which feature should we build" fake-door increases buyer skepticism of every other fake-door. GoodUI's fake-door pattern documentation notes the tradeoff; consumer trust data (Edelman Trust Barometer 2024/25) shows declining tolerance for "coming soon" that never comes. Operator stance: disclose the research-status in the post-submit state ("we're validating demand — we'll reach out within N days") to preserve trust. The pure fake-door without disclosure is a 2015 move.

5. **Session replay compliance regime.** PostHog / Clarity / Hotjar session replay runs into GDPR, CCPA, and (2025 in force) India DPDP constraints on inferred-consent recording of user interactions. The compliant default in 2026 is explicit opt-in banner + masked-by-default PII + region-specific retention windows. Legal frontier — operators should assume tightening, not loosening.

---

## Reviewer lens — where you'd still lose points

1. **The "5-module anatomy" is a first-hypothesis, not a measured truth for your ICP.** A Peep Laja-style critic ([cxl.com](https://cxl.com/)) would push back on treating Shapiro's anatomy as the answer rather than the opening bid. Wynter-style message testing (wynter.com) would require you to run the hero copy past 15+ ICP respondents *before* shipping the page. If you're writing copy off anatomy + benchmarks without a single ICP conversation, you're back to guessing dressed as rigor.

2. **Your taste brief reads like a Refactoring UI exam answer.** A Rauno Freiberg-style critic ([rauno.me](https://rauno.me/)) would note that specifying seven variables doesn't produce taste — it produces coherent boringness. The *specific* taste move (a single unexpected detail: Linear's dense typographic grid, Raycast's micro-interactions, Vercel's gradient math) is what moves a page from "competent" to "memorable." The brief is a floor, not a ceiling. Week 3 teaches the floor; the ceiling is years.

3. **You skipped the "where does AI-code-gen genuinely fail" section.** A Simon Willison-style critic ([simonwillison.net](https://simonwillison.net/)) would point out that multi-component state, complex routing, and novel design-system tokens are consistent v0/Lovable/Bolt failure zones in 2025–26. A synthesis that treats the tool stack as "pick on task profile" without naming the 3 specific failure zones for each tool is still L2 tool-comparison content.

4. **Your N<200 inference discipline is honest but too narrow.** A Ronny Kohavi-style critic ([Trustworthy Online Controlled Experiments](https://www.amazon.com/Trustworthy-Online-Controlled-Experiments-Practical/dp/1108724264)) would note that CI width is one of several concerns — sequential-peeking bias, novelty effect, day-of-week confound, and survivor bias on "qualified" traffic all matter at small N and are not resolved by wider CIs. The synthesis says "update a prior, don't measure an effect"; the full operator move is "update the prior, name the biases, decide on a second batch before you look at the first."

5. **"4 hours" is aspirational for engagement #1; honest for engagement #5.** A patio11-style critic ([kalzumeus.com](https://www.kalzumeus.com/)) would note that first prototypes take 12–16 hours when you include the stuff nobody counts — domain setup, email sender configuration, Stripe activation, WCAG audit on output, buyer-side NDA if the landing page references a client, git/deploy plumbing. The 4-hour number is a target, not a promise. Missing this sets up a week-one "why am I slow" spiral that the synthesis owes the reader a warning about.

---

## Further reading

**Must-read (≤5):**
- Julian Shapiro, *Startup Handbook: Landing Page Copywriting* ([julian.com/guide/startup/landing-pages](https://www.julian.com/guide/startup/landing-pages)) — hook/promise/proof/action framework + Desire–(Labor+Confusion). (Mon)
- Unbounce, *Conversion Benchmark Report 2024/25* ([unbounce.com/conversion-benchmark-report](https://unbounce.com/conversion-benchmark-report/)) — 41k pages, 464M visitors, module-level and channel-level medians. (Mon)
- Adam Wathan & Steve Schoger, *Refactoring UI* (2018, continuously updated at [refactoringui.com](https://www.refactoringui.com/)) — seven-variable taste-layer literacy. (Wed)
- Alberto Savoia, *Pretotype It* (2014) + Summary of Pretotyping Techniques PDF on [albertosavoia.com](https://www.albertosavoia.com/) + [pretotyping.org](https://www.pretotyping.org/) — rung-ladder reference. (Thu)
- Teresa Torres, *Continuous Discovery Habits* (2021) + [producttalk.org](https://www.producttalk.org/opportunity-solution-trees/) OST post — discovery discipline + OST tiers. (Thu, Sat)

**Recommended:**
- shadcn/ui docs + Vercel Academy "Evolution of Component Libraries" ([ui.shadcn.com](https://ui.shadcn.com/) + [vercel.com/academy](https://vercel.com/academy/shadcn-ui/evolution-of-component-libraries)) — copy-in-codebase model + v0 integration + late-2025 Shadcn Create. (Tue, Wed)
- Rob Fitzpatrick, *The Mom Test* (2013, reference edition at [momtestbook.com](https://www.momtestbook.com/)) — interview-script discipline that still governs AI-moderated scripts. (Sat)
- Anthropic, *Agent Teams* docs ([code.claude.com/docs/en/agent-teams](https://code.claude.com/docs/en/agent-teams)) + *How we built our multi-agent research system* ([anthropic.com/engineering/multi-agent-research-system](https://www.anthropic.com/engineering/multi-agent-research-system)) + *Advanced Tool Use* 2025 ([anthropic.com/engineering/advanced-tool-use](https://www.anthropic.com/engineering/advanced-tool-use)) — orchestrator + subagents + programmatic tool calling. (Fri)
- PostHog pricing + docs ([posthog.com/pricing](https://posthog.com/pricing)) + Microsoft Clarity docs ([clarity.microsoft.com](https://clarity.microsoft.com/)) — free-tier event tracking + session replay. (Sat)
- Ronny Kohavi, Diane Tang, Ya Xu, *Trustworthy Online Controlled Experiments* (Cambridge, 2020) — A/B rigor, power, CIs, sequential-peeking. (Sat)

**Optional / supplementary:**
- Rauno Freiberg essays on motion and interaction design ([rauno.me](https://rauno.me/)) — ceiling-level taste references. (Wed)
- Nielsen Norman Group 2024/25 eye-tracking research ([nngroup.com](https://www.nngroup.com/)) — F-pattern / Z-pattern / reading path data. (Mon)
- Jason Schuller (Pressive) and Rob Hope (One Page Love, Typewolf) — teardown-driven landing-page literacy. (Mon)
- Brian Lovin's brian-lovin.com — Linear design-system commentary. (Wed)
- GoodUI pattern library ([goodui.org](https://www.goodui.org/)) — A/B-tested UX patterns with ethics notes, including fake-door. (Thu)
- Morgan Lewis, *Negotiating AI Provisions in Commercial and Technology Contracts* (April 2026, [morganlewis.com](https://www.morganlewis.com/blogs/sourcingatmorganlewis/2026/04/negotiating-ai-provisions-in-commercial-and-technology-contracts-where-the-market-is-heading)) — reference for when Week 3's prototypes graduate to contracted engagements. (Fri, cross-ref Block 1 Wk 1 Fri)

---

## End-to-end runnable exercise — one real hypothesis, one afternoon

Pick **one specific hypothesis** from your Block 1 Week 2 niche work or Block 0 Week 3 JTBD work. Then, in a single afternoon, run the full Week 3 pipeline end-to-end:

1. **Anatomy + copy (45 min).** Ask Claude Code:

   > *Given this hypothesis: [paste]. Given this ICP: [paste]. Draft the 5-module landing page anatomy (hero / proof / objection / pricing or offer-detail / CTA stack) following Julian Shapiro's hook-promise-proof-action for the hero. Constraint: hero H1 + sub + CTA must pass a 5th–7th grade Flesch-Kincaid readability check. Include one concrete number in the H1. Return as Markdown with per-module word counts.*

   Read it. Rewrite one line you don't believe in your own voice.

2. **Tool pick + taste brief (20 min).** Based on Tuesday: pick v0 (if shadcn-aesthetic SaaS), Lovable (if you need auth + db in the prototype), Bolt (if you want zero local setup), or Claude Code direct (if your design system is bespoke). Write the **60-word, 7-variable taste brief** (Q10 shape) for that tool.

3. **Rung + threshold (15 min).** Place the hypothesis on Savoia's ladder (Q11 shape). Commit to the rung + the kill / iterate / level-up thresholds (Q18 shape) in writing before you build. If you can't write the thresholds, the hypothesis isn't sharp enough yet — stop and refine it.

4. **Build (2–4 hours).** Run the 4-hour pipeline (Q16 Claude Code orchestrator prompt). Start the timer. Stop condition: working URL + 5 end-to-end test submissions OR 4 hours, whichever first.

5. **Instrument (30 min).** Wire PostHog events (Q14 event model) and Microsoft Clarity session replay. Verify events fire end-to-end with a test submission. Add a kill/iterate/level-up dashboard.

6. **Drive 50–200 qualified visitors (next 7 days, outside the afternoon).** Warm outbound from Block 1 Week 1 list + paid LinkedIn ≤ $200 + any earned distribution. Stop when N ≥ your threshold batch.

7. **Post-mortem (30 min).** Write **400 words** on:
   - Where you spent >30 min and what would collapse that to <10 min next time.
   - Which Shapiro module under-performed, identified via session replay + funnel.
   - Whether the hypothesis moved to kill / iterate / level-up, with reference to your pre-committed thresholds.
   - One taste-brief variable you specified that v0/Lovable/Claude Code *refused* — and what prompt pattern would override it next time.
   - One interview insight (if you ran interviews) that the quantitative signal would have missed.

That post-mortem is the most valuable artifact of this week. It's the calibration data for engagement #2. Weeks 4–6 of Block 2 will assume you have it.

---

## Citations

[^1]: Unbounce, *"What is the average landing page conversion rate? (Q4 2024 data)."* https://unbounce.com/average-conversion-rates-landing-pages/. Retrieved 2026-04-17. Claim supported: overall median 6.6% across 41,000 pages / 464M visits / 57M conversions; industry breakdowns (SaaS 3.8%, events 12.3%); mobile share 82.9%; desktop-vs-mobile conversion delta. (Reused from Mon [^1].)

[^2]: Unbounce, *"Average SaaS conversion rate benchmark report."* https://unbounce.com/conversion-benchmark-report/saas-conversion-rate/. Retrieved 2026-04-17. Claim supported: SaaS median 3.8%; top-quartile threshold 11.6%; –24.3% correlation between difficult words and conversion; 62% increase in negative correlation since 2020. (Reused from Mon [^2].)

[^3]: Unbounce / PR Newswire, *"Unbounce's 2024 Conversion Benchmark Report."* September 5, 2024. https://www.prnewswire.com/news-releases/unbounces-2024-conversion-benchmark-report-proves-that-attention-spans-are-declining-and-so-are-conversion-rates-302239407.html. Retrieved 2026-04-17. Claim supported: reading-grade conversion rates (11.1% at 5th–7th grade vs 5.3% at college); channel mix (email 19.3%, Instagram paid 17.9%). (Reused from Mon [^3].)

[^4]: Shapiro, Julian. *"Startup Handbook: Landing Page Copywriting."* https://www.julian.com/guide/startup/landing-pages. Retrieved 2026-04-17. Claim supported: hook → promise → proof → action hero framework; "Purchase Rate = Desire − (Labor + Confusion)." (Reused from Mon [^5].)

[^5]: Vercel Blog, *"Introducing the new v0."* February 3, 2026. https://vercel.com/blog/introducing-the-new-v0. Retrieved 2026-04-17. Claim supported: v0 stack (Next.js + shadcn/ui + Tailwind, Vercel deploy). (Reused from Tue [^2].)

[^6]: shadcn/ui Changelog, *"February 2025 — Tailwind v4."* https://ui.shadcn.com/docs/changelog/2025-02-tailwind-v4. Retrieved 2026-04-17. Claim supported: shadcn/ui copy-in-codebase model, Tailwind v4 / OKLCH migration, "Open in v0" integration on component pages. (Reused from Tue [^8] and Wed [^10].)

[^7]: Lovable Blog, *"The Lovable Prompting Handbook."* January 16, 2025. https://lovable.dev/blog/2025-01-16-lovable-prompting-handbook. Retrieved 2026-04-17. Claim supported: Lovable's plan → scaffold → iterate loop; Supabase integration as first-class backend. (Reused from Tue [^11].)

[^8]: Evil Martians, *"bolt.new from StackBlitz."* 2025. https://evilmartians.com/chronicles/bolt-new-from-stackblitz-how-they-surfed-the-ai-wave-with-no-wipeouts. Retrieved 2026-04-17. Claim supported: Bolt.new's in-browser WebContainer execution primitive. (Reused from Tue [^13].)

[^9]: Y Combinator Library / Wikipedia, *Replit Agent.* https://en.wikipedia.org/wiki/Replit. Retrieved 2026-04-17. Claim supported: Replit Agent's checkpoint-diff-commit model with hosted dev environment. (Reused from Tue [^19].)

[^10]: PostHog Newsletter, *"How bolt.new works."* Lior Neu-ner, 2025. https://newsletter.posthog.com/p/from-0-to-40m-arr-inside-the-tech. Retrieved 2026-04-17. Claim supported: Bolt context-bleed failure mode at larger codebases. (Reused from Tue [^18].)

[^11]: Wathan, Adam and Schoger, Steve. *Refactoring UI.* https://www.refactoringui.com/. Retrieved 2026-04-17. Claim supported: seven-variable taste-layer framework (typography, color, spacing, density, motion, imagery, voice). (Reused from Wed [^1].)

[^12]: W3C WAI, *WCAG 2.2 Recommendation* + *"C39: Using the CSS prefers-reduced-motion query."* https://www.w3.org/TR/WCAG22/ and https://www.w3.org/WAI/WCAG21/Techniques/css/C39. Retrieved 2026-04-17. Claim supported: WCAG 2.2 as 2024 Recommendation; motion and contrast rules. (Reused from Wed [^19].)

[^13]: Freiberg, Rauno. *Devouring Details.* https://devouringdetails.com/. Retrieved 2026-04-17. Claim supported: motion-as-medium interaction-design discipline. (Reused from Wed [^16].)

[^14]: Savoia, Alberto. *Pretotype It* (2nd ed. PDF) + pretotyping.org. https://www.pretotyping.org/. Retrieved 2026-04-17. Claim supported: six-rung pretotyping ladder (paper / smoke-test / fake-door / concierge-Wizard-of-Oz / painted-door / MVP). (Reused from Thu [^1][^4].)

[^15]: Torres, Teresa. *"Opportunity Solution Trees."* Product Talk. https://www.producttalk.org/opportunity-solution-trees/. Retrieved 2026-04-17. Claim supported: outcome → opportunity → solution → experiment/assumption tiers; weekly customer-interview cadence. (Reused from Thu [^16] and Sat [^17].)

[^16]: Fitzpatrick, Rob. *The Mom Test.* https://www.momtestbook.com. Retrieved 2026-04-17. Claim supported: interview discipline (past behavior over hypotheticals, no leading questions, specific over general). (Reused from Thu [^30] and Sat [^18].)

[^17]: Anthropic, *Claude Code subagents docs* + Cherny workflow writeups. https://code.claude.com/docs/en/sub-agents and https://getpushtoprod.substack.com/p/how-the-creator-of-claude-code-actually. Retrieved 2026-04-17. Claim supported: Claude Code as orchestrator (agent + subagents); 4–8 hour shippable-prototype pipeline with v0/Lovable as UI, n8n/Cloudflare Workers as glue, Vercel as deploy. (Reused from Fri [1][9].)

[^18]: PostHog, *"Capturing events"* docs + pricing. https://posthog.com/docs/product-analytics/capture-events and https://posthog.com/pricing. Retrieved 2026-04-17. Claim supported: event model (verb-object naming, properties); 2025 free-tier limits (1M events, 5k session replays, 1M feature-flag requests/month). (Reused from Fri [16] and Sat [^1][^5].)

[^19]: Wikipedia, *"Binomial proportion confidence interval."* https://en.wikipedia.org/wiki/Binomial_proportion_confidence_interval. Retrieved 2026-04-17. Claim supported: Wilson score interval stability; 95% CI widths for 6/50, 12/100, 60/500. (Reused from Thu [^27] and Sat [^19].)

[^20]: Anthropic, *"Equipping agents for the real world with Agent Skills"* + *Advanced Tool Use.* https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills and https://www.anthropic.com/engineering/advanced-tool-use. Retrieved 2026-04-17. Claim supported: programmatic tool calling (Claude writes code that calls tools in a loop) as more reliable than natural-language tool round-trips; Skills/subagents framing. (Reused from Tue citation set and Fri [3].)

[^21]: Microsoft Clarity, *August 2025 recap.* https://clarity.microsoft.com/blog/august-2025-recap/. Retrieved 2026-04-17. Claim supported: Microsoft Clarity free session replay + heatmaps. (Reused from Fri [18].)

[^22]: Kohavi, Ron; Tang, Diane; Xu, Ya. *Trustworthy Online Controlled Experiments.* Cambridge, 2020. https://www.cambridge.org/core/books/trustworthy-online-controlled-experiments/D97B26382EB0EB2DC2019A7A7B518F59. Retrieved 2026-04-17. Claim supported: A/B rigor / power / sample-size / sequential-peeking reference. (Reused from Sat [^21].)

[^23]: Outset.ai Series B announcement + Listen Labs Series B + Strella Series A + Maze Interview Studies. https://www.globenewswire.com/news-release/2025/12/10/3203401/0/en/Outset-Secures-30-Million-Series-B-to-Launch-the-World-s-First-AI-Native-Customer-Experience-Management-Platform.html ; https://www.prnewswire.com/news-releases/listen-labs-raises-69-million-series-b-to-bring-customer-voices-into-every-decision-302661000.html ; https://venturebeat.com/technology/amazon-and-chobani-adopt-strellas-ai-interviews-for-customer-research-as ; https://maze.co/features/interview-studies/. Retrieved 2026-04-17. Claim supported: AI-moderated interview platforms (Outset, Listen Labs, Strella, Maze) providing moderated qualitative at N≥5 in hours. (Reused from Sat [^10][^12][^13][^14].)

_last_verified: 2026-04-17_
