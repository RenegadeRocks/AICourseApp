---
type: lesson
block: block-5-product-building-principles
week: week-12
day_of_cycle: 6
day_name: sat
session_slug: build-mvp-backend-connect-with-ai-workflows
date_due: 2026-08-09
tags: [build-day, product-skeleton, streaming-endpoint, thin-backend, deploy, end-to-end, mvp, code-lab, ship-it]
sources:
  - vercel-ai-sdk-5-2025
  - supabase-pricing-2026
  - vercel-fluid-compute-2026
  - anthropic-streaming-docs
  - anthropic-building-effective-agents-2024
  - nextjs-16-release-2025
  - seibel-mvp-yc
last_verified: 2026-07-17
word_count_target: 5000
---

# BUILD: ship the product skeleton — frontend, thin backend, one AI workflow, wired end to end, deployed to a URL

## Why this matters (operator framing)

Today you stop describing and start shipping. By the end you will have a working thin-slice product: a frontend a stranger can load, a thin backend that authenticates and meters, and one AI workflow wired end to end, streaming, deployed to a URL. This is the synthesis of the whole week. Monday made it usable, Tuesday made it AI-native, Wednesday built the frontend, Thursday built the backend, Friday wired the loop. Today you compose them into a thing that exists on the internet and delivers AI value to someone who did not build it. The pass bar is deliberately blunt: a stranger hits your URL and gets AI value. Everything else is commentary.

The trap this day exists to prevent: the demo that works on your machine and dies for everyone else. A product skeleton that a stranger can use forces you to solve the real problems (secrets that do not leak, a failure state that recovers, a deploy that actually deploys) that a localhost demo lets you skip. Those are exactly the problems that separate a build-day toy from something you can put in front of a customer next week.

## Prerequisites

- Every lesson this week. Today composes all five. If any is shaky, the composition will expose it.
- The [[block-5-product-building-principles/week-12-frontend-basic-uiux-design-principles--build-mvp-backend-connect-with-ai-workflows/05-fri-connecting-frontend-to-ai-workflows|Friday]] streaming loop and the [[block-5-product-building-principles/week-12-frontend-basic-uiux-design-principles--build-mvp-backend-connect-with-ai-workflows/04-thu-mvp-backend-architecture|Thursday]] backend design.
- One AI workflow from an earlier block you want to wire in. The simplest viable choice is a single-turn generation over your own content; the report generator from b2w05 or a RAG agent from Block 3 are the ambitious choices.
- `code-lab/1/` open. It is the runnable reference for today's build. It type-checks and lints clean; use it as the skeleton or as the thing you read when yours breaks.

## The build philosophy: thin slice, not thin quality

Michael Seibel's MVP framing is the right north star for today: build the smallest thing that delivers the core value to a real user, ship it, and learn.[^7] The discipline that distinguishes a good thin slice from a bad one is *vertical, not horizontal*. A thin slice goes all the way through (frontend to backend to model to deployed URL) for *one* feature, at real quality. A bad MVP goes wide and shallow: five half-built features, none deployed, none usable by a stranger.

So today's scope is one AI workflow, wired completely, deployed. Not five workflows stubbed. The one feature must clear the whole week's bar: usable (Monday), AI-native states (Tuesday), owned code (Wednesday), thin secure backend (Thursday), streaming loop (Friday). Thin slice, full quality, on a URL.

## The build, in six phases

This is a timed build. Block 4 to 6 hours. Keep a build log; it is the artifact you show a prospect.

### Phase 0 — decide the one thing (20 min)

Write one sentence: "A stranger visits my URL, does X, and gets Y AI value." X is the single action. Y is the value. If you cannot write it in one sentence, your scope is too wide. Examples that pass: "A user pastes a job description and gets a tailored cover letter, streamed." "A user asks a question about my uploaded docs and gets a cited answer." "A user describes a bug and gets a triaged reproduction plan." Each is one action, one value, wireable in a day.

Then decide the two architecture calls from this week:

- **Streaming or job-queue?** (Thursday/Friday). If the workflow completes in under the serverless timeout and streams, use the fast loop. If it is a long multi-step agent, use a queue. For a first ship, choose a workflow that fits the fast loop; the queue is a v2 upgrade.
- **BaaS or none?** (Thursday). If the thin slice needs auth and persistence, Supabase. If the thin slice is genuinely stateless (paste in, get out, no login), you can ship without a database and add it next week. Do not add auth you do not need today.

### Phase 1 — the shell (45 min)

Stand up the frontend from Wednesday: Next.js 16 + Tailwind + shadcn, or the `code-lab/1` zero-dependency skeleton if you want to move fast and understand every line. Build the shell with real states from Tuesday's table: an empty state with example prompts, an input, a streaming output area, and an error state. Do not build the success state only; the empty and error states are what a stranger hits first and hits on failure.

Run Monday's five-principle audit on the shell before proceeding. One primary action, AA contrast, visible focus, labeled controls, teaching empty state. Fix any failure now; it is cheaper before the wiring than after.

### Phase 2 — the thin backend (45 min)

Build the streaming endpoint from Friday. The `code-lab/1/src/server.ts` is the reference implementation and it does exactly this: authenticate or identify the caller, rate-limit, validate input, call the model with the *server-side* key, stream SSE back, log tokens and cost. Whether you use Next.js route handlers or the zero-dependency Node server, the responsibilities are identical.

The three non-negotiables this phase:

1. The API key is in `process.env`, used only server-side, provably absent from anything the browser receives. Verify with `grep -r sk-ant dist public` finding nothing (the code-lab README shows this check).
2. Every generation logs tokens and cost. You cannot price what you do not measure.
3. There is a per-caller rate limit, however crude. One user cannot run up your bill.

### Phase 3 — wire the AI workflow (60 min)

Connect your one workflow. For a single-turn generation, this is the model call inside the endpoint. For a RAG agent from Block 3, the endpoint calls your retrieval-plus-generation workflow and streams the answer with citations. For the report generator from b2w05, this is where you would enqueue a durable job instead of streaming.

The wiring test: hit the endpoint with a real prompt and watch tokens stream. If they arrive all at once at the end, you buffered instead of streamed; fix it (Friday's Mistake 1). If the endpoint hangs past the timeout, your workflow is too long for the fast loop and needs the queue (Thursday's rule).

### Phase 4 — the failure and empty paths (30 min)

This is the phase build-days skip and production punishes. Force three failures and confirm each recovers:

1. **Network dies mid-stream.** The UI must show a recoverable error that preserves the user's input, not a blank or a lost prompt (Tuesday's Pattern 5). The `code-lab` client demonstrates the preserve-input-plus-Retry pattern.
2. **Empty/invalid input.** The endpoint returns a clear error, the UI shows it, nothing crashes.
3. **Rate limit hit.** The user sees a "try again in a minute" state, not a raw 429.

If any failure loses the user's input or shows a raw stack trace, you have not passed Phase 4.

### Phase 5 — deploy to a URL (45 min)

The phase that makes it real. Deploy to a host where a stranger can reach it:

- **Vercel** for a Next.js build: `vercel deploy`, set `ANTHROPIC_API_KEY` and any Supabase vars in the project env, confirm the streaming route works in production (streaming has bitten people on some serverless configs; Fluid compute and the AI SDK's SSE handle it).[^1][^3]
- **Any Node host** (Render, Railway, Fly) for the code-lab server: set the env var in the dashboard, build command `npm install && npm run build`, start command `npm start`. The README documents this exactly.

Then the real test: open the URL on your phone, on a network that is not your dev machine, and do the one action. If it streams AI value to you on your phone, a stranger can get it too.

## The pass bar, stated plainly

**A stranger hits your URL and gets AI value.** Concretely, all of these are true:

1. The URL is public and loads without your dev machine running.
2. A first-time visitor understands what to do (teaching empty state, one clear action).
3. The one action streams a real AI response (not a spinner-then-dump).
4. The API key is provably absent from the client.
5. A forced failure (kill network mid-stream) recovers with the user's input preserved.
6. Every generation logs tokens and cost server-side.

If all six hold, you shipped a product skeleton. If any fails, that is your Monday. Do not move on with a broken pass bar; the point of the day is a thing that works for someone who is not you.

## What you deliberately did not build

Naming the cuts is part of the discipline, because a thin slice is defined by what it excludes:

- **Multiple features.** One workflow, wired fully. The second workflow is next week.
- **The durable queue** (unless your one workflow needed it). Most first slices stream and fit the fast loop.
- **Polished taste.** Monday's usability floor is non-negotiable; the taste moat is a later investment once users prove the product is worth crafting for.
- **Analytics and iteration instrumentation.** That is Block 4's [[block-4-test-validate-package/week-10-build-landing-page-with-cta-recap--create-ai-generated-launch-creatives/05-fri-launch-day-instrumentation|launch instrumentation]] and the analytics work ahead. Today is ship, not measure.
- **Auth you did not need.** If the slice is stateless, no login today.

Each cut is a decision you can defend, not a corner you forgot. That is what separates a thin slice from a half-built app.

## Controversy: does a build-day product need a backend at all, or can you ship frontend-only?

A real debate for the fastest possible ship.

**The frontend-only camp.** Tools like Bolt and Lovable can ship a "working" AI app where the model is called from a serverless function the tool manages, and for the very first demo you can even prototype by calling the model from the client with a throwaway key. Fastest possible time to a clickable thing. For a build-day whose only goal is "see it work," skipping the backend design is a legitimate speed move.

**The backend-required camp.** The moment a *stranger* can hit your URL, a client-side key is a stranger-can-spend-your-money vulnerability, and a frontend-only app has no way to authenticate, rate-limit, or meter. The backend is not optional infrastructure, it is the thing that makes the product safe to expose. A frontend-only AI app is a demo, not a product, and the whole point of today is a product a stranger can use.

**The synthesis this lesson commits to:** the backend requirement is a function of *exposure*, not of ambition. A localhost demo you show one person can be frontend-only and it is fine. The instant you deploy to a URL a stranger can reach, the thin backend (server-side key, rate limit, metering) is mandatory, because those are the three things that stand between "a stranger gets AI value" and "a stranger drains your API budget." Today's pass bar requires exposure, so today requires the backend. The camps are really arguing about the exposure boundary, and the operator rule is simple: no public URL touches a model without a server-side key and a rate limit in front of it. Ship the demo frontend-only if you want; ship the *product* with the thin backend.

## Common mistakes experts see

1. **Going wide instead of deep.** Five stubbed features, none deployed, none usable by a stranger. Thin slice means one feature all the way through.
2. **Localhost-only ship.** "It works on my machine" and never deploying, so the real problems (env vars, streaming in production, cold starts) are never surfaced.
3. **Client-side key on a public URL.** The single most expensive build-day mistake. A stranger with your key spends your money.
4. **Buffering instead of streaming.** The endpoint collects the whole response and returns it, so the deployed product has the bare-spinner latency the whole week warned against.
5. **Skipping the failure path.** Shipping the happy path only, so the first stranger who loses network loses their prompt and never comes back.
6. **No metering.** Deploying without logging cost, then being unable to answer "what does a user cost me" when you go to price it.
7. **Auth theater.** Adding a login the thin slice did not need, burning an hour on a flow that delivers no value today.
8. **Deploy-day surprise on streaming.** Discovering at deploy that the streaming route buffers on the host's default config, because it was never tested outside localhost.

## Reflection questions

1. Write your one-sentence scope. Does it name exactly one action and one AI value? If it has an "and," cut it.
2. Which architecture did you choose, streaming or queue, and does the actual duration of your workflow justify it?
3. Prove your API key is absent from the client. What command did you run, and what did it return?
4. Force a mid-stream failure. Did the user's input survive? If not, that is your first fix Monday.
5. What does one generation cost you, from your own logs? At what usage does a user become unprofitable?
6. What did you deliberately not build today, and why is each cut defensible rather than a forgotten corner?
7. You opened the URL on your phone. Did a stranger's experience match what you intended, or did something only work because your dev machine was running?

## My take (reviewer lens)

**Michael Seibel** would mostly endorse today and push on one thing: even a thin slice is too much if you have not confirmed anyone wants it. His likely note: "You built a beautiful skeleton for a product nobody asked for. The build-day should come *after* the validation sprint, not instead of it." He is right that build-before-validate is a classic founder failure, and it is why this block sits after the [[block-4-test-validate-package/week-11-define-your-product-idea-validate-idea-using-ai--market-user-validation-interview-or-poll-potential-users/06-sat-build-run-the-validation-sprint|validation work]] in Block 4. The steelman for building anyway: for an AI product, a working thin slice is often the *best* validation artifact, because "would you use this" is answered better by a real streaming demo than by an interview. Build the slice, but point it at a validated need, not a whim.

**Boris Cherny** would push on the "do it in one Claude Code session" opportunity the lesson under-plays. His likely framing: the entire six-phase build is a single well-specified Claude Code orchestration against a repo, with the agent scaffolding the shell, wiring the endpoint, and writing the failure states while you review diffs, and treating it as six manual phases is slower than it needs to be. Fair, and the code-lab is exactly the kind of artifact an agent produces well. The reason the lesson keeps the phases manual: on your first product skeleton, doing each phase by hand once builds the mental model you need to *review* the agent's version competently later. Automate the second one.

**Chip Huyen** would push on the metering-is-enough framing. Her likely point: logging cost per call is necessary but the build-day should also capture the *inputs* to a cost model, latency percentiles and failure rates, because a product that streams beautifully but fails 8% of the time or costs $0.40 a call has a business problem the pass bar does not catch. Correct, and it is the bridge to the analytics week ahead. Today's pass bar deliberately stays blunt (a stranger gets value) so the day ends with a shipped thing; the measurement discipline is the very next thing you add.

## Further reading

**Must-read (this week):**
1. **`code-lab/1/README.md`** — the runnable reference for today, with the exact pass-bar checks and the Next.js + AI SDK port.
2. **Vercel AI SDK 5 streaming docs** — the production streaming route your Next.js version uses.[^1]
3. **Anthropic streaming docs** — the model-side of the stream.[^4]

**Recommended:**
4. **Supabase quickstart** — if your slice needs auth and persistence today.[^2]
5. **Vercel Fluid compute** — so your deployed streaming route does not surprise you on timeouts.[^3]

**Optional:**
6. **Michael Seibel / YC on the MVP** — the thin-slice-not-thin-quality discipline.[^7]

## Citations

[^1]: Vercel, "AI SDK 5" (vercel.com/blog/ai-sdk-5) and the streaming docs (ai-sdk.dev/docs). Source for the production streaming route (`streamText`, `toUIMessageStreamResponse`) and SSE handling on Vercel. Also cited Wednesday and Friday. (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending.)

[^2]: Supabase pricing and quickstart (supabase.com/pricing, supabase.com/docs). Source for the auth-plus-persistence option and free-tier limits. Also cited Thursday. (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending.)

[^3]: Vercel Fluid compute and streaming-functions docs (vercel.com/docs/fluid-compute). Source for streaming in production and the timeout behavior that can bite an untested deploy. Also cited Thursday and Friday. (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending.)

[^4]: Anthropic API streaming documentation (docs.anthropic.com). Source for the model-side token streaming the endpoint adapts. Also cited Friday. (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending.)

[^5]: Anthropic, "Building Effective Agents" (anthropic.com/research/building-effective-agents), December 2024. Source for the thin-slice orchestrator pattern and start-simple discipline. Also cited Thursday, Friday, b2w05.

[^6]: Next.js 16 release (nextjs.org/blog/next-16). Source for the App Router route-handler and deploy model. Also cited Wednesday. (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending.)

[^7]: Michael Seibel / Y Combinator on the MVP — build the smallest thing that delivers core value to a real user and ship to learn. The thin-slice-not-thin-quality framing (ycombinator.com/library and Seibel's MVP talks). Reviewer lens throughout the vault.

_last_verified: 2026-07-17_
