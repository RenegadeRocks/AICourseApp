---
type: lesson
block: block-5-product-building-principles
week: week-12
day_of_cycle: 7
day_name: sun
session_slug: build-mvp-backend-connect-with-ai-workflows
date_due: 2026-08-10
tags: [synthesis, quiz, flashcards, recap, week-12, ui-ux, ai-native, frontend-stack, mvp-backend, streaming]
sources:
  - wcag-22-w3c-2024
  - vercel-ai-sdk-5-2025
  - supabase-pricing-2026
  - nextjs-16-release-2025
  - reloadux-ai-uncertainty-framework-2026
last_verified: 2026-07-17
word_count_target: 3500
---

# Week 12 synthesis, quiz, and flashcards — from usable surface to shipped product skeleton

## The week in one arc

You entered the week able to build agents, landing pages, and packaged offers. You leave it able to assemble them into a product a stranger logs into. The arc:

- **Monday** set the usability floor: hierarchy, WCAG 2.2 AA contrast, affordances, Fitts/Hick/Jakob, and the reframe that "looks designed" and "is usable" are different axes. Aesthetics is table stakes; usability is correctness.
- **Tuesday** added the AI-native layer: designing for a slow, probabilistic, sometimes-wrong system. Streaming over spinners, optimistic about the action not the content, confidence as checkable sources not fake scores, graceful failure that preserves input, empty states that teach.
- **Wednesday** built the frontend stack: Next.js 16 on React 19, Tailwind v4, shadcn as a design-system platform, the AI SDK, and the generate-then-own workflow (generate structure and style, own logic and integration).
- **Thursday** built the thin backend: persist, auth, secrets, glue, meter. BaaS (Supabase, Neon) for the MVP, the serverless-versus-long-running decision, and the server-side-key rule that is the whole reason an AI product needs a backend.
- **Friday** wired the loop: SSE streaming for the fast path, job queues and durable workflows for the slow path, React 19 async-state primitives, and rate-limit-plus-cost handling at the product layer.
- **Saturday** composed it all into a shipped skeleton: one workflow, wired end to end, deployed to a URL, where a stranger gets AI value.

The single most important idea of the week: **the backend is thin and the intelligence lives in the AI workflow.** Your product code authenticates, persists, guards secrets, meters, and orchestrates; the agents you already built do the intelligent work. Everything else is in service of getting that composition in front of a real user safely.

## The three controversies, resolved

Each day carried a live debate. The through-line of the resolutions:

1. **Default-good-enough versus taste-as-moat (Mon):** resolved on the task-friction axis. Ship default aesthetics, never ship broken usability. The usability floor (contrast, hierarchy-of-one, labeled controls, teaching empty states) is correctness for an MVP; the taste moat is a later, earned investment.
2. **How much uncertainty to show (Tue):** resolved on stakes and verifiability. Show uncertainty where the stakes are high and the user can act on the signal; prefer checkable sources over abstract confidence scores; frame residual uncertainty as information, never apology; never hide uncertainty to manipulate.
3. **Hand-code versus generate-then-own (Wed), BaaS lock-in (Thu), realtime infra (Fri), backend-required (Sat):** all resolved the same way, on *which part / what exposure*, not a global policy. Generate structure, own logic; take BaaS velocity while isolating the AI-orchestration seam; stream the fast path and queue the slow one based on your core workload's shape; require a backend the instant a stranger can reach your URL.

The meta-lesson: almost every product-building "versus" debate dissolves once you ask *which component* or *what exposure level*, rather than picking a side globally.

## How this connects forward

Next week (Week 13) makes the product *feel magic*: smart features that wow users, built on exactly this skeleton. Week 14 adds analytics, iteration, scale, auth, and polish. The skeleton you shipped Saturday is the substrate both build on. The [[block-4-test-validate-package/week-10-build-landing-page-with-cta-recap--create-ai-generated-launch-creatives/05-fri-launch-day-instrumentation|launch instrumentation]] from Block 4 is what you bolt on to measure it, and the [[block-4-test-validate-package/week-09-packaging-selling-your-ai-agents--create-your-first-sellable-agent-package/05-fri-pricing-the-package|pricing]] work is what your cost-metering makes possible.

---

## Quiz (12 questions)

Take it cold, without reopening the lessons. Answers below.

**1. (MCQ)** WCAG 2.2 AA requires which minimum contrast ratios?
a) 3:1 for all text
b) 4.5:1 normal text, 3:1 large text, 3:1 non-text UI components
c) 7:1 normal text, 4.5:1 large text
d) 4.5:1 for everything including borders

**2. (Short answer)** Explain the aesthetic-usability effect and why it is a trap for a product builder specifically (versus a landing page).

**3. (MCQ)** A user submits an AI generation. Which is the correct application of optimistic UI?
a) Optimistically render a predicted answer, then correct it
b) Optimistically render the user's message and a streaming placeholder, then stream the real content
c) Show a spinner until the full response arrives
d) Render nothing until the server confirms

**4. (Short answer)** Per the 2026 uncertainty-design literature, why does "Limited data available for this recommendation" outperform "AI is unsure," and what failure mode do you risk if you label every output with an uncertainty signal?

**5. (Code completion)** In the Vercel AI SDK v5, name the client hook that manages the streaming chat loop and the two message types the SDK splits messages into.

**6. (MCQ)** Your AI workflow is a multi-step agent that can take 6 minutes and must survive a function restart. Which architecture is correct?
a) A synchronous serverless function that streams
b) A client-side call to the model
c) A background job / durable workflow (Inngest or Vercel Workflows) with the frontend polling for the result
d) A longer spinner

**7. (Short answer)** State the single rule that is the primary reason an AI product needs a backend at all, and the one-line command from the code-lab that verifies you obeyed it.

**8. (MCQ)** Supabase's free tier has which catch that makes it unsuitable for a production app needing 24/7 uptime?
a) It costs $25/month
b) Projects pause after 7 days of inactivity
c) It has no database
d) It caps you at 100 users

**9. (Short answer)** Distinguish an affordance from a signifier, and give one example of an AI-generated UI shipping an affordance without a signifier.

**10. (Short answer)** Apply Fitts's law and Hick's law each to one concrete product-design decision.

**11. (MCQ)** In the generate-then-own workflow, what should you always own rather than let the tool generate unreviewed?
a) The card grid
b) The auth flow, secrets handling, and payment path
c) The color tokens
d) The empty state

**12. (Short answer)** Your product streams beautifully but you have no per-user cost cap. Describe the specific business failure this creates and the two controls that prevent it.

### Answer key

**1.** b. Normal text 4.5:1 (SC 1.4.3), large text 3:1, non-text UI components 3:1 (SC 1.4.11). WCAG 2.2 is current; contrast ratios are unchanged from 2.1.[^1]

**2.** The aesthetic-usability effect is that users judge attractive interfaces as more usable and forgive (and fail to report) minor usability problems. It is a trap for a product because the effect decays under repeated task friction: a landing page's only task is read-and-click-once, so the effect carries it, but a product's user does real work repeatedly, so a problem forgiven on day one becomes a ticket on day thirty. It also masks usability problems during testing.[^1]

**3.** b. Be optimistic about the *action* (the request was accepted, deterministic), not the *content* (non-deterministic). Render the user's message and a streaming placeholder, then stream the real content in. Rendering a guessed answer produces a UI that contradicts itself, worse than a spinner.

**4.** "Limited data available" frames the uncertainty as useful context and keeps the user in control; "AI is unsure" reads as failure and undermines the system's credibility. Same underlying uncertainty, opposite trust effect. Labeling every output risks *over-indication*: users tune out all the signals and lose trust in every output equally.[^5]

**5.** `useChat` (from `@ai-sdk/react`). The two message types are `UIMessage` (the app's source of truth) and `ModelMessage` (the streamlined representation sent to the model).[^2]

**6.** c. It exceeds the serverless timeout (default 5 minutes on Vercel Fluid compute) and must survive failure, so it needs durable background execution with the frontend polling or subscribing. Running it synchronously is the demo-works-production-fails trap.

**7.** Rule: the API key lives server-side only and never reaches the browser; the frontend calls your endpoint, your endpoint calls the model with the key. Verification: `grep -r sk-ant dist public` (or the built client bundle) must find nothing.

**8.** b. Free projects pause after 7 days of inactivity, so a production app that needs continuous uptime must be on Pro ($25/mo) or higher.[^3]

**9.** An affordance is a possible action (a button can be pressed); a signifier is the visible cue that communicates it (the button looks pressable). Example of affordance-without-signifier: a clickable card with no hover state, or an icon-only button whose meaning you must guess, or a text field that looks like a label.

**10.** Fitts's law: make the primary action a large target (e.g., 48px on mobile checkout) and put destructive actions far from safe ones, because time-to-acquire depends on size and distance. Hick's law: reduce first-run choices to one primary path (progressive disclosure) because decision time grows logarithmically with the number of options.

**11.** b. Auth flow, secrets handling, and payment path (and the AI-integration security boundary). Generate structure and style; own logic and integration; never ship unreviewed generated code on a security path, given the ~45% AI-code OWASP-vulnerability finding.

**12.** The model API is metered, so unbounded per-user usage means one power user or one runaway bug can run up a bill that exceeds your revenue, making you unprofitable with no ceiling. The two controls: per-user rate limits (cap requests per window) and per-user cost caps (cap spend, keyed on the tokens/cost you log per call), plus optionally model routing for cheaper tasks.

**Scoring:** 11–12 correct, you are ready for Week 13. 8–10, reread the two weakest days. Below 8, redo Saturday's build with the code-lab open; the concepts land when you wire them.

---

## Flashcards (28)

**Q:** What are the WCAG 2.2 AA contrast minimums?
**A:** 4.5:1 normal text, 3:1 large text (18pt/24px or 14pt bold/19px), 3:1 non-text UI components (borders, focus rings).

**Q:** What is the aesthetic-usability effect?
**A:** Users judge attractive UIs as more usable and forgive/under-report minor usability problems. It masks defects in testing and decays under task friction.

**Q:** "Looks designed" vs "is usable" — which is table stakes?
**A:** Aesthetics is table stakes; usability is correctness. Ship default aesthetics, never ship broken usability.

**Q:** Fitts's law, one product implication.
**A:** Time-to-acquire depends on target size and distance: make primary actions large, put destructive actions far from safe ones, use screen corners (infinite-size targets).

**Q:** Hick's law, one product implication.
**A:** Decision time grows logarithmically with number of choices: minimize first-run options, use progressive disclosure.

**Q:** Jakob's law.
**A:** Users spend most time on other products and prefer yours to work the same way. Be conventional on structure, distinctive on your differentiator.

**Q:** Affordance vs signifier.
**A:** Affordance = a possible action; signifier = the visible cue that communicates it. AI UIs often ship affordances (clickable card) without signifiers (no hover state).

**Q:** The three properties that drive all AI-native UX patterns.
**A:** High/variable latency; non-deterministic output; output can be wrong while looking right.

**Q:** Best latency UX for AI text output?
**A:** Stream token-by-token. It collapses perceived latency to near zero because the user reads as it forms. Skeleton screens for structured output; staged progress for agents; spinner only as last resort.

**Q:** Skeleton screens vs blank spinner panel — the effect?
**A:** Skeletons reduce perceived load time ~40% and near-eliminate the "is this broken?" reload.

**Q:** Optimistic UI for AI — the rule.
**A:** Be optimistic about the action (request accepted, deterministic), not the content (non-deterministic). Render the user's message + streaming placeholder, stream real content in.

**Q:** Best confidence signal for factual AI output?
**A:** A checkable source (inline, clickable citation), not an abstract confidence score. A source is uncertainty the user can resolve.

**Q:** "AI is unsure" vs "Limited data available" — why the latter wins?
**A:** It frames uncertainty as information, not apology, keeping the user in control without undermining credibility.

**Q:** Over-indication failure mode.
**A:** Labeling every output with uncertainty signals makes users tune them all out and lose trust in every output equally. Surface uncertainty selectively.

**Q:** The eight states of an AI feature.
**A:** Idle/empty, submitted, generating, success, low-quality success, refusal, error/timeout, uncertain claim. AI UIs ship success only.

**Q:** The 2026 default frontend stack.
**A:** Next.js 16 (Turbopack default, React Compiler) on React 19.2, Tailwind v4 (OKLCH), shadcn/ui, Vercel AI SDK for streaming.

**Q:** shadcn in 2026 — what changed?
**A:** `shadcn create` (Dec 2025) added five visual styles (Vega/Nova/Maia/Lyra/Mira) that rewrite code; CLI v4 (Mar 2026) added presets — your taste brief as shareable config.

**Q:** The generate-then-own rule.
**A:** Generate structure and style; own logic and integration. Never ship unreviewed generated code on a security path (auth, secrets, payments).

**Q:** RSC "use client" rule.
**A:** Server Components by default; mark `"use client"` only at the interactivity boundary (state, effects, handlers). Over-marking ships unnecessary JS.

**Q:** The thin-backend responsibilities.
**A:** Persist, auth, secrets, orchestration glue, rate/cost control. The intelligence lives in the AI workflow, not the backend.

**Q:** Why does an AI product need a backend at all?
**A:** To hold the API key server-side. The frontend calls your endpoint; your endpoint calls the model. A client-side key is a stranger-can-spend-your-money hole.

**Q:** Supabase free-tier catch.
**A:** Projects pause after 7 days of inactivity; unsuitable for 24/7 production. Pro is $25/mo.

**Q:** Neon in 2026.
**A:** Serverless Postgres, acquired by Databricks (~$1B, May 2025), 80% of its DBs created by AI agents; post-acquisition price cuts (storage ~$0.35/GB, scale-to-zero).

**Q:** Serverless vs long-running for AI — the rule.
**A:** Streams and fits the timeout (5 min default on Vercel Fluid) → serverless streaming. Multi-step/long/must-survive-failure → background job or durable workflow.

**Q:** SSE, in one line.
**A:** Server-Sent Events: a one-way server-to-browser stream over one HTTP connection, native in all browsers; the AI SDK v5 streaming default.

**Q:** React 19 async-state primitives.
**A:** `useOptimistic` (optimistic value with auto-rollback tied to transitions) and `useActionState` (result/error/pending lifecycle). Collapse the loading/error/rollback boilerplate.

**Q:** Job-queue options for the slow loop.
**A:** Inngest (step functions, retries only failed step, 50K runs/mo free), Trigger.dev (AI pipelines), QStash (simple delayed delivery), Vercel Workflows (durable suspend/resume).

**Q:** The Saturday pass bar.
**A:** A stranger hits your public URL and gets streamed AI value; key absent from client; forced failure preserves input; every generation logs tokens and cost.

## Citations

[^1]: W3C WCAG 2.2 and WebAIM contrast guidance. Source for AA contrast minimums and the aesthetic-usability effect context. Cited fully in Monday. (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending.)

[^2]: Vercel AI SDK 5 (vercel.com/blog/ai-sdk-5) and useChat reference. Source for `useChat`, `UIMessage`/`ModelMessage`. Cited fully in Wednesday and Friday. (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending.)

[^3]: Supabase pricing. Source for the 7-day free-tier pause and Pro $25/mo. Cited fully in Thursday. (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending.)

[^4]: Next.js 16 release. Source for the current frontend stack. Cited fully in Wednesday. (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending.)

[^5]: reloadux AI uncertainty framework. Source for information-not-apology and over-indication. Cited fully in Tuesday. (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending.)

_last_verified: 2026-07-17_
