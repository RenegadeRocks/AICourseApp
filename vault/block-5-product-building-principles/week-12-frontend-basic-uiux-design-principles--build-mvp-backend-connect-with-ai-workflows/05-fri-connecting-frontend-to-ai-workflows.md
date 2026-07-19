---
type: lesson
block: block-5-product-building-principles
week: week-12
day_of_cycle: 5
day_name: fri
session_slug: build-mvp-backend-connect-with-ai-workflows
date_due: 2026-08-09
tags: [streaming, sse, useChat, job-queues, webhooks, async-state, optimistic-ui, rate-limits, cost-handling, inngest, vercel-workflows]
sources:
  - vercel-ai-sdk-5-2025
  - react-useoptimistic-2026
  - inngest-vs-triggerdev-qstash-2026
  - vercel-workflows-2026
  - vercel-fluid-compute-2026
  - anthropic-building-effective-agents-2024
  - mdn-server-sent-events
  - anthropic-streaming-docs
last_verified: 2026-07-17
word_count_target: 5500
---

# Connecting frontend to AI workflows — streaming, job queues, async state, and the full request-to-render loop

## Why this matters (operator framing)

You have a usable AI-native frontend (Mon-Wed) and a thin backend (Thu). This lesson is the wiring between them, the part that makes an AI product feel alive instead of broken. The request-to-agent-to-stream-to-render loop is the beating heart of every AI product, and it is where beginners lose hours: the stream that hangs, the long job that times out, the state that goes stale, the cost that spikes. Get this loop right and a 20-second generation feels instant because it streams; a 5-minute agent run completes reliably because it is queued; a failed request recovers because state is handled. The deliverable: you can wire a streaming AI endpoint to a React UI, offload long runs to a job queue, manage async state without bugs, and handle rate limits and cost at the product layer.

By the end you can (1) stream AI responses to the UI over SSE end to end, (2) decide and wire streaming versus job-queue for a given workload, (3) manage the async state that non-deterministic long-running AI forces, (4) apply optimistic and eventual-consistency patterns correctly, and (5) handle rate limits and cost so the product is economically sane.

## Prerequisites

- [[block-5-product-building-principles/week-12-frontend-basic-uiux-design-principles--build-mvp-backend-connect-with-ai-workflows/04-thu-mvp-backend-architecture|Thursday's]] backend: the thin backend, the timeout decision, secrets. This lesson wires the frontend to that backend.
- [[block-5-product-building-principles/week-12-frontend-basic-uiux-design-principles--build-mvp-backend-connect-with-ai-workflows/02-tue-ux-patterns-for-ai-native-products|Tuesday's]] AI-native UX patterns: streaming, optimistic action, graceful failure. This lesson is the code behind those patterns.
- The AI SDK v5 from Wednesday, installed.

## The full loop, named

Before the parts, the whole. A user asks your AI product to do something, and here is the complete path:

```
user input → optimistic render → POST /api/generate (auth + rate check)
   → backend calls model with server-side key → SSE stream back
   → useChat renders tokens as they arrive → done, persist + log cost
```

For long work, the middle changes:

```
user input → POST /api/jobs (enqueue) → return job ID immediately
   → background worker runs the agent (durable, survives failure)
   → worker writes result + status to DB
   → frontend polls or subscribes → renders when ready
```

Two loops, one for fast-streaming work and one for long-durable work, and the timeout decision from Thursday picks which. Everything below is the implementation of these two loops.

## Streaming: the fast loop, over Server-Sent Events

Streaming is the default for any AI response that completes within the serverless timeout, and it is what makes the latency UX from Tuesday possible. The mechanism is Server-Sent Events (SSE): a one-way stream from server to browser over a single long-lived HTTP connection, natively supported in every browser.[^1][^7] The AI SDK v5 rebuilt its streaming around SSE precisely because it is standard, debuggable with browser devtools, and robust.[^1]

The end-to-end wiring, at the shape level:

**Backend (the streaming route).** A Next.js route handler that authenticates, calls the model with `streamText`, and returns the stream. The Anthropic model streams tokens; the AI SDK adapts them to SSE; the route returns that as the response. The server-side key never leaves the backend (Thursday's rule).[^1][^8]

**Frontend (the streaming UI).** The `useChat` hook from `@ai-sdk/react` manages the whole client side: it POSTs the message, opens the SSE connection, and gives you the streaming messages as reactive state you render. In AI SDK v5, `useChat` is transport-based and no longer manages input state internally, and messages are split into `UIMessage` (your source of truth) and `ModelMessage` (what goes to the model).[^1] You render the `UIMessage` list; tokens stream into the last assistant message; the user reads as it forms.

The reason this matters beyond convenience: streaming collapses perceived latency to near zero for long outputs, because the user starts reading before generation finishes. A non-streamed 20-second generation is a 20-second spinner. A streamed one is a response that starts in under a second and keeps going. Same total time, opposite experience. This is Tuesday's Pattern 1 in code.

## Job queues: the long loop, for work that outlives a request

When the work exceeds the serverless timeout or must survive failure (a multi-step agent, a long document pipeline, a report generator), synchronous streaming is the wrong tool. It will time out and drop the job. You need a background job system. The 2026 options, verified:[^2]

- **Inngest** wins for complex multi-step workflows with state, especially AI agent tasks. Its step-function model runs each step independently and saves its result, so if step 3 fails after 1 and 2 succeeded, it retries only step 3, not the whole workflow. Free tier: 50,000 runs/month.[^2]
- **Trigger.dev** is strong for AI pipelines, batch processing, and any workload where execution time is unpredictable or needs external input. Long-running LLM call chains that break serverless timeouts are its canonical use case.[^2]
- **QStash** (Upstash) is the simplest: "send this HTTP request later with retries," no SDK, just POST to an endpoint. Free tier: 500 messages/day. Right when you need delayed/retried delivery but not step functions or fan-out.[^2]
- **Vercel Workflows** is the durable-execution layer inside the AI SDK ecosystem: it breaks agent tasks into named steps that suspend (persist state to managed storage), wait for external events, and resume exactly where they left off across multiple function invocations, solving the serverless-timeout limit natively.[^3]

The pattern is the same across all of them: the request enqueues a job and returns a job ID immediately; a worker runs the long agent durably; the worker writes the result and status to your database; the frontend polls or subscribes for the result. The key property you are buying is *durability*: the agent's progress survives a function restart, a deploy, or a transient failure, because state is persisted between steps. Anthropic's effective-agents guidance frames this as the difference between a workflow you can trust unattended and a script that dies on the first hiccup.[^4]

The decision rule, restated from Thursday and made concrete: if the work streams and finishes inside 5 minutes, use the fast streaming loop; if it is multi-step, long, or must survive failure, use a queue or durable workflow. Do not run a 4-minute agent synchronously and hope; that is the demo-works-production-fails trap.

## Async state: the hardest part, and how React 19 helps

Non-deterministic, long-running, streaming AI forces async state management that ordinary CRUD apps avoid. The state you must track:

- **Request lifecycle:** idle, submitting, streaming, done, error, and (for jobs) queued and running. Tuesday's eight states are these plus the AI-specific ones.
- **Optimistic vs confirmed:** the user's message shown instantly (optimistic) versus the persisted, confirmed state.
- **Partial results:** a stream that is 60% done is a real, renderable state, not a loading spinner.

React 19 gives you first-class primitives that eliminate most of the boilerplate:[^5]

- **`useOptimistic`** shows an optimistic value while an async action is in flight and automatically rolls back to the canonical value when the action completes or errors, tied to React's transition system.[^5] This is Tuesday's optimistic-action pattern: render the user's message instantly, reconcile when the server confirms.
- **`useActionState`** wraps an action and returns its last result, its error, and a pending flag, managing the form/action lifecycle so you stop hand-rolling loading and error booleans.[^5]

Together these collapse what used to be a wall of manual loading flags, error state, and rollback logic into a handful of declarative lines.[^5] For the streaming loop, `useChat` already manages most of this; for your own non-chat AI actions (a one-shot "improve this text" button), `useOptimistic` and `useActionState` are the tools.

The critical async-state rule: **be optimistic about the action, eventual about the content.** You can optimistically render that the request was accepted (deterministic). You cannot optimistically render the AI's answer (non-deterministic). Reconcile the content when it actually arrives. Getting this backwards produces a UI that contradicts itself, which Tuesday named as worse than a spinner.

## Webhooks and events: closing the async loop

For job-based work, the frontend needs to know when the job finishes. Two approaches:

1. **Polling.** The frontend asks "is job X done?" every few seconds. Simple, works everywhere, slightly wasteful. Fine for an MVP.
2. **Push (webhooks/subscriptions).** The backend notifies the frontend when the job completes, via a webhook to a realtime channel (Supabase Realtime) or a subscription. More efficient, more moving parts. The upgrade when polling becomes a bottleneck.

For the MVP, polling a status column in your database is correct: it is trivial to build, has no extra infrastructure, and works. Move to push when you have enough concurrent long jobs that polling load matters. This is the same premature-optimization discipline as everywhere else this week: build the simple thing, upgrade when a measured need forces it.

Webhooks also flow the other way: your product may *receive* webhooks from services (a payment succeeded, a document finished processing elsewhere). Those hit a backend route that validates the webhook signature (never trust an unsigned webhook) and updates state. The signature validation is the security boundary; an unauthenticated webhook endpoint is an open door.

## Rate limits and cost handling at the product layer

This is where AI products bleed money if you skip it. The model API is metered, and without product-layer controls, one heavy user or one runaway bug can run up a bill that dwarfs your revenue.

The controls, in order of importance:

1. **Per-user rate limits.** Cap requests per user per time window. A user (or a script hitting your API) cannot fire 10,000 generations in an hour. Enforce in the backend before the model call, keyed on the authenticated user.
2. **Per-user cost caps.** Beyond request count, cap spend. Track cost per user (you are logging tokens and cost from Thursday) and refuse or degrade when a user exceeds their tier's budget. This is what makes usage-based pricing sane.
3. **Handle provider rate limits gracefully.** The model provider also rate-limits *you*. When you hit a 429, back off and retry with jitter, and surface a "high demand, retrying" state to the user rather than a raw error. Do not hammer a rate-limited API; that extends the outage.
4. **Model routing for cost.** Route cheap tasks to a cheap model and hard tasks to a frontier model. With Sonnet 5 at intro pricing around $2/$10 per Mtok and frontier tiers far higher, routing the 80% of easy requests to the cheap model is often a 3-5x cost reduction with no quality loss on those requests.[^6] Meter, then route.
5. **Cache where you can.** Prompt caching (reusing a cached system prompt or context across calls) cuts input-token cost substantially for repeated-context workloads. The backend is where you configure it.

The unit-economics point, which connects forward to Block 4's pricing work: you cannot price a product whose per-user cost you do not control. Rate limits and cost caps are not just abuse prevention, they are what make your margins predictable. A product with unbounded per-user AI cost has unbounded downside, and one power user can make you unprofitable.

## Controversy: how much realtime infrastructure does an MVP need?

A genuine architecture debate for AI products.

**The minimalist camp.** Stream single-turn responses, poll for the rare long job, skip queues and realtime until you have a reason. Most AI MVPs are chat or single-shot generation that fits the streaming loop, and adding Inngest, webhooks, and realtime subscriptions on day one is infrastructure for scale you do not have. The simplest thing (SSE streaming plus a status-column poll) ships this week and serves your first hundred users.

**The durable-first camp.** Build on durable job execution from the start, because the moment your product does anything beyond single-turn chat (a multi-step agent, a document pipeline, a scheduled report), synchronous streaming breaks and you are rewriting the core loop under production pressure. The step-function model (Inngest, Vercel Workflows) is cheap to adopt early and expensive to retrofit, and the reliability it buys is exactly what turns a demo into a product a customer trusts.

**The synthesis this lesson commits to:** the discriminator is *the shape of your core workload, not your ambition.* If your product's central action is single-turn generation or chat that fits the timeout and streams, the minimalist loop is correct and durable job infrastructure is premature. If your product's central action is inherently multi-step or long (the report generator, the research agent, anything that composes several model calls with retrieval), then durability is not optional infrastructure, it is the correctness requirement, and building it later means rebuilding the core under load. Look at your *main* AI action and let its duration and step-count decide, exactly as Thursday's timeout rule said. The camps agree more than they appear: both would stream a chat and both would queue a 5-minute agent. The disagreement is only about products on the boundary, and there the honest tiebreaker is "will this run unattended and must it survive failure." If yes, pay for durability now.

## Worked example — the two loops in the Saturday build

The build wires the fast loop and stubs the slow one:

**Fast loop (built):** `/api/generate` authenticates via Supabase, checks a simple per-user rate limit, calls Anthropic with `streamText`, returns SSE. The frontend uses `useChat` to stream tokens into the message list. On completion, the backend persists the generation and its cost. This is the whole request-to-render loop, running.

**Slow loop (understood, stubbed):** the lesson shows where a long agent would enqueue to Inngest and poll a status column, so you know the upgrade path, but the v1 build streams because its generation fits the window. Building the fast loop well and knowing exactly where the slow loop attaches is the correct MVP posture.

## Runnable experiment — wire the streaming loop end to end, with a pass bar

**Setup (15 min).** In your Wednesday project with the AI SDK installed, and your Thursday backend design in hand.

**Phase 1 — the streaming route (30 min).** Write `/api/generate`: authenticate, call the model with `streamText`, return the stream. Confirm with `curl` that the endpoint streams SSE and that the API key is nowhere in the response or the client bundle.

**Phase 2 — the streaming UI (30 min).** Wire `useChat` to the route. Render the streaming message list. Confirm tokens appear as they generate, not all at once at the end.

**Phase 3 — failure and cost (25 min).** Kill your network mid-stream and confirm the UI shows a graceful failure that preserves input (Tuesday's Pattern 5), not a blank error. Add per-call cost logging and a trivial per-user rate limit. Confirm the log shows tokens and cost.

**Pass bar:** Tokens visibly stream into the UI (not a spinner then a dump); the API key is provably absent from the client bundle (grep the built output); a mid-stream network failure shows a recoverable state with the user's input preserved; and every generation logs tokens and cost. If the response arrives as one block, or the key is in the bundle, or a failure loses the input, you have not passed.

## Common mistakes experts see

1. **Buffering then returning instead of streaming.** Collecting the whole response server-side and returning JSON, reintroducing the bare-spinner latency and losing the streaming UX.
2. **Running long agents synchronously.** The demo-works-production-fails trap: a multi-minute agent in a request that times out and drops the job. Queue it.
3. **Optimistic about content, not just action.** Rendering a guessed answer that the model contradicts, a UI that lies. Be optimistic about the action, eventual about the content.
4. **No provider-rate-limit handling.** Hammering a 429'd API with no backoff, extending the outage and surfacing raw errors to users.
5. **No per-user cost cap.** One power user or one bug runs up a bill larger than revenue, because per-user cost is unbounded.
6. **Losing input on failure.** The stream dies and the user's prompt vanishes, the rage-quit generator from Tuesday.
7. **Premature realtime.** Building webhooks, subscriptions, and queues for a single-turn chat product that only needed SSE streaming.
8. **Unsigned webhook endpoints.** Accepting inbound webhooks without validating the signature, an open door into your state.

## Reflection questions

1. Is your product's core action a fast-streaming loop or a long-durable loop? What is the actual duration, and does your architecture match it?
2. Where in your UI are you optimistic about the action, and where would being optimistic about the content actively lie to the user?
3. Your provider returns a 429 under load. What does the user see, and what does your backend do? Write the backoff.
4. What is your per-user cost cap, and what happens (refuse, degrade, upsell) when a user hits it?
5. Which of your requests could be routed to a cheaper model with no quality loss, and how much would that save at 1,000 requests?
6. Your long job finishes. How does the frontend find out, and why did you choose polling versus push for the MVP?

## My take (reviewer lens)

**Jerry Liu** would push on the streaming-versus-queue framing as too binary. His LlamaIndex Workflows work argues that the interesting AI products are *event-driven*, where retrieval, reasoning, and generation are steps that can each stream, retry, and branch, so the clean split between "fast streaming loop" and "slow queue loop" collapses in practice: a good agent product streams *and* is durable, showing staged progress (Tuesday's Pattern 1) while running on a step-function backbone. He is right that the frontier is the hybrid, and it is why the lesson points at Vercel Workflows and Inngest's step model. The reason the lesson keeps the binary for the MVP: a first product rarely needs the hybrid, and teaching the two clean loops first is the right pedagogy before the composition.

**Boris Cherny** would push back that the whole rate-limit-and-cost section is where solo builders under-invest and then get a surprise bill, and that the lesson still treats it as one section among many rather than the thing that determines whether the business survives. Fair escalation. The honest reframe: for a product where the AI cost is a real fraction of revenue (most of them), cost control is not a feature, it is the P&L, and the metering-plus-routing-plus-caps stack should arguably be built before the pretty UI. The lesson foregrounds it in the pass bar for exactly this reason, but Boris would say foreground it more.

**Karpathy** would note that `useChat` and the AI SDK abstractions hide the actual mechanism (the SSE bytes, the token stream, the model's finish reason), and that a builder who only knows the hook does not understand what happens when it breaks. The mitigation: the experiment requires you to `curl` the raw SSE and grep the bundle for the key, so you touch the mechanism under the abstraction at least once. The abstraction is the right default for shipping; the raw loop is the right thing to have seen once so you can debug it.

## Further reading

**Must-read (this week):**
1. **Vercel AI SDK 5 and useChat reference** — vercel.com/blog/ai-sdk-5 and ai-sdk.dev/docs. The streaming loop you are wiring.[^1]
2. **React useOptimistic and useActionState** — react.dev/reference/react. The async-state primitives.[^5]
3. **Inngest vs Trigger.dev vs QStash (2026)** — the job-queue landscape for when you need the slow loop.[^2]

**Recommended:**
4. **Vercel Workflows** — durable execution for agents that outlive a request.[^3]
5. **Anthropic streaming docs** — the model-side of the stream you are adapting.[^8]

**Optional:**
6. **MDN, Server-Sent Events** — the underlying browser mechanism, worth reading once.[^7]

## Citations

[^1]: Vercel, "AI SDK 5" (vercel.com/blog/ai-sdk-5), July 2025, and the useChat reference (ai-sdk.dev/docs/reference/ai-sdk-ui/use-chat). Source for SSE-first streaming, `streamText`, transport-based `useChat`, UIMessage/ModelMessage split, and useChat no longer managing input state. Also cited in b2w03 and Wednesday. (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending.)

[^2]: "Inngest vs Trigger.dev vs QStash: Serverless Jobs 2026" (pkgpulse.com) and buildmvpfast job-queue comparisons. Source for Inngest's step-function model (retry-only-failed-step, 50K runs/mo free), Trigger.dev for AI pipelines, QStash's simple delayed-delivery (500 msg/day free), and the enqueue-worker-poll pattern. (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending.)

[^3]: Vercel Workflows (AI SDK ecosystem, 2026). Source for durable execution: agent tasks as named steps that suspend/persist/resume across invocations, solving serverless timeouts. Also cited Thursday. (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending.)

[^4]: Anthropic, "Building Effective Agents" (anthropic.com/research/building-effective-agents), December 2024. Source for durable workflows vs fragile scripts and the trust-unattended framing. Also cited in b2w05 and Thursday.

[^5]: React, "useOptimistic" and "useActionState" reference (react.dev/reference/react). Source for optimistic updates with automatic rollback tied to transitions, the pending/error/result action lifecycle, and the boilerplate collapse. Also cited Tuesday and Wednesday. (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending.)

[^6]: Anthropic Sonnet 5 intro pricing (~$2/$10 per Mtok through 2026-08-31), recorded in the vault landscape delta. Source for model-routing cost reduction. (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending.)

[^7]: MDN Web Docs, "Server-Sent Events" (developer.mozilla.org/en-US/docs/Web/API/Server-sent_events). Source for SSE as a native, one-way server-to-browser streaming mechanism over a single HTTP connection.

[^8]: Anthropic API streaming documentation (docs.anthropic.com). Source for the model-side token streaming that the AI SDK adapts to SSE. (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending.)

_last_verified: 2026-07-17_
