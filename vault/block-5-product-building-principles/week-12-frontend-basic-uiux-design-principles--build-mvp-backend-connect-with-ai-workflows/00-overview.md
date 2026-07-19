---
type: week-overview
block: block-5-product-building-principles
week: week-12
title: 'Week 12 — Frontend UI/UX principles + build an MVP backend connected to AI workflows'
live_sessions:
  - '2026-08-08 — Frontend: Basic UI/UX Design Principles'
  - '2026-08-09 — Build: MVP Backend & Connect with AI Workflows'
study_window: 2026-08-03 to 2026-08-09
last_verified: 2026-07-17
---

# Week 12 — From usable surface to shipped product skeleton

## The thesis of this week

You can build agents, landing pages, and packaged offers. This week is the pivot from *selling agents* to *shipping software a stranger logs into and pays for*. The unifying claim: **a 2026 AI product is a thin backend wrapped around an AI workflow, fronted by a usable, AI-native surface, and the whole thing lives or dies on getting that composition in front of a real user safely.** Your product code authenticates, persists, guards secrets, meters, and orchestrates; the agents you already built do the intelligent work; the frontend makes a slow, probabilistic, sometimes-wrong system feel trustworthy.

The field is mid-argument about almost every piece of this. Is the AI-generated default good enough, or is taste a moat? How much of the model's uncertainty should you show? Hand-code or generate-then-own? BaaS velocity or roll-your-own control? This week takes a position on each and resolves them the same way: the "versus" almost always dissolves once you ask *which component* or *what exposure level*, not which side to pick globally.

The Saturday build is where all five weekday lessons pay off as a shipped, deployed URL.

## Who this week is for

You have shipped an agent or a RAG system (Blocks 2 and 3) and packaged or validated an offer (Block 4). You know retrieval is not understanding, evals beat prompts, and unattended reliability is engineered, not hoped for. Now you are looking at the product surface: the thing users see, the backend that serves it, and the wiring between them. You direct Claude Code, can read a CSS variable and a JSON schema, and have shipped at least one page through v0, Lovable, or Bolt. This week gives you the usability floor, the AI-native pattern library, the current build stack, the thin-backend architecture, and the streaming loop that composes them into a product.

## Shape of the week

Seven lessons tracing one path from usable surface to deployed skeleton. Each weekday is roughly 60–120 minutes of reading plus 30–90 minutes hands-on. Saturday is a full build with a runnable, type-checked code-lab.

| Day | Topic | Shape |
|-----|-------|-------|
| Mon | UI/UX first principles — hierarchy, WCAG 2.2 AA contrast, affordances, Fitts/Hick/Jakob, taste as a learnable skill | Deep-dive + five-principle audit |
| Tue | UX patterns for AI-native products — streaming, optimistic action, confidence/citations, graceful failure, teaching empty states, the eight states | Deep-dive + AI state-design experiment |
| Wed | Frontend build stack 2026 — Next.js 16 / React 19 / Tailwind v4 / shadcn / AI SDK, and the generate-then-own workflow | Deep-dive + generate-own-hand-edit drill |
| Thu | MVP backend architecture — thin backend, BaaS (Supabase/Neon), serverless vs long-running, secrets, where the earlier-block agents plug in | Deep-dive + backend-design experiment |
| Fri | Connecting frontend to AI workflows — SSE streaming, job queues, React 19 async state, rate limits and cost at the product layer | Deep-dive + end-to-end streaming wire-up |
| Sat | BUILD: ship the product skeleton — one workflow, wired end to end, deployed to a URL a stranger can use | Full build + code-lab + deploy |
| Sun | Synthesis, 12-question quiz, 28-card flashcard set | Review + cold quiz |

## Why these topics belong together

They are the layers of one product, from the pixel a user sees to the token a model streams. The order is the dependency order: you cannot design AI-native states (Tue) without the usability floor (Mon); you cannot wire the streaming loop (Fri) without the frontend (Wed) and backend (Thu); you cannot ship Saturday without all five. The failures chain, exactly like the pipeline in Block 2 Week 5: a sub-AA focus ring (Mon) fails a real user; a bare spinner (Tue) reads as broken; a client-side key (Thu) drains your budget; a synchronous long agent (Fri) drops jobs in production. The only defense is knowing each layer's failure mode before you compose them Saturday.

Explicitly building on earlier weeks, never re-teaching them: [[block-2-ai-employees/week-03-building-elegant-landing-pages--how-to-build-micro-prototypes/03-wed-design-system-literacy|design-system literacy]] and [[block-2-ai-employees/week-03-building-elegant-landing-pages--how-to-build-micro-prototypes/02-tue-how-ai-code-gen-tools-work|AI code-gen tools]] (b2w03) are the aesthetic and tooling substrate this week extends into interaction design, AI-native UX, and backend. The agents you wire come from [[block-2-ai-employees/week-04-building-a-sales-agent--building-comprehensive-rag-ai-agent/02-tue-agent-architectures|Block 2]] and [[block-3-advanced-topics-voice/week-06-beyond-prompt-engineering-context-engineering--advanced-rags/04-thu-agentic-retrieval|Block 3]].

## What "L3 depth" means this week

Every weekday lesson engages five things:

1. **A live controversy with named positions.** Default-good-enough vs taste-moat (Seibel vs Lovin/Freiberg); how much uncertainty to show (transparency vs confidence); hand-code vs generate-then-own; BaaS lock-in vs roll-your-own; realtime infra now vs later; backend-required-on-exposure.
2. **Current, verified facts.** WCAG 2.2 AA, Next.js 16 / React 19.2, Tailwind v4, shadcn create + CLI-v4 presets, AI SDK v5/v6, Supabase and Neon 2026 pricing, Vercel Fluid-compute timeouts, Inngest/QStash/Trigger.dev. Every fast-moving fact carries a search-verified stamp.
3. **Runnable experiments with explicit pass bars.** A five-principle usability audit; an eight-state AI design; a generate-own-hand-edit cycle that must `tsc --noEmit` clean; a backend design where no key reaches the browser; an end-to-end streaming wire-up; a deployed skeleton a stranger can use.
4. **Operator specifics.** Contrast ratios as constraints; the 5-minute serverless timeout; Supabase's 7-day free-tier pause; per-user cost caps; the server-side-key rule verified by `grep`.
5. **A reviewer lens with named disagreements.** Seibel, Karpathy, Boris Cherny, Simon Willison, Chip Huyen, Jerry Liu, and design voices Rauno Freiberg and Brian Lovin, each with a specific push-back, not five restatements.

## How to study this week

Each day, in priority order if short on time:

1. **Run the experiment.** The audit, the state design, the wire-up, the build. The capability lands in the hands, not the prose.
2. **Read the "Must-read" citations.** Three to five per day. Refactoring UI, WCAG 2.2, the AI SDK docs, and the reloadux uncertainty framework recur; read them once, well.
3. **Do the reflection questions.** They are not Googleable; they force the decision on your specific product.
4. **Read the prose.** It is scaffolding for the first three.

Saturday is not optional. If you study one day, study Saturday, but it only works because Monday through Friday gave you the layers it composes. The `code-lab/1/` skeleton type-checks and lints clean; use it as the reference when yours breaks.

## The live sessions

The cohort meets 2026-08-08 (UI/UX principles) and 2026-08-09 (build the MVP backend). They are bonuses. The vault lessons are the primary instruction, each a standalone masterclass. If you miss the live sessions, nothing here is incomplete.

## Prerequisites from earlier weeks

This week assumes Block 2 Week 3 (landing pages, codegen tools, design-system literacy) and at least one shipped agent or RAG system from Block 2 or 3. Specifically: you can read a CSS variable and a Tailwind class, you have generated a page through v0/Lovable/Bolt, and you have an agent or workflow to wire in. If the design-system literacy is shaky, reread b2w03 Wednesday before Monday; if you have no agent to wire, the Saturday build will feel abstract, so pick the simplest single-turn generation over your own content.

_last_verified: 2026-07-17_
