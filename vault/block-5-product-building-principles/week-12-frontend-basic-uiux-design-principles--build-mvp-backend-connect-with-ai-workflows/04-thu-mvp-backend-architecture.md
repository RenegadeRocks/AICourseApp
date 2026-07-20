---
type: lesson
block: block-5-product-building-principles
week: week-12
day_of_cycle: 4
day_name: thu
session_slug: build-mvp-backend-connect-with-ai-workflows
date_due: 2026-08-09
tags: [mvp-backend, baas, supabase, neon, serverless, edge-functions, ai-endpoints, secrets-management, thin-backend, function-timeouts]
sources:
  - supabase-pricing-2026
  - neon-databricks-acquisition-2025
  - neon-pricing-2026
  - vercel-fluid-compute-2026
  - vercel-function-limits-2026
  - vercel-30-min-functions-2026
  - anthropic-building-effective-agents-2024
  - owasp-agentic-top-10-2026
last_verified: 2026-07-17
word_count_target: 5500
---

# MVP backend architecture — the thin backend, BaaS, and where AI workloads break serverless

## Why this matters (operator framing)

The frontend from Wednesday is the face. This lesson is the body: the backend that stores users, holds secrets, and serves the AI workflows you built in Blocks 2 and 3. The stakes are that AI workloads break the assumptions of ordinary web backends. A normal API call returns in 200ms; an agent run takes 30 seconds to 5 minutes and streams. Serverless functions time out; long agent runs die halfway. Secrets that leak from a frontend become someone else's API bill. Get the backend shape right and your product scales cheaply from one user to a thousand on a free tier. Get it wrong and you either overpay for infrastructure you do not need or lose data and drop AI jobs in production. The deliverable: you can choose a backend stack, design the API surface for AI endpoints, handle the timeout and secrets problems, and know exactly where the agent work from earlier blocks plugs in.

By the end you can (1) choose between BaaS options with current pricing, (2) design the thin-backend-plus-AI-workflow pattern, (3) decide serverless versus long-running for a given AI workload, (4) handle secrets and env correctly, and (5) place the earlier-block agents into the product backend without re-teaching how they work.

## Prerequisites

- [[block-5-product-building-principles/week-12-frontend-basic-uiux-design-principles--build-mvp-backend-connect-with-ai-workflows/03-wed-frontend-build-stack-2026|Wednesday's]] frontend stack. The backend serves that frontend.
- Your agent and automation builds from [[block-3-advanced-topics-voice/week-08-automation-agent-integration-mcps--build-hybrid-agent-scraper-summarizer/05-fri-reliability-engineering-for-unattended-agents|Block 3's reliability engineering]] and the [[block-2-ai-employees/week-04-building-a-sales-agent--building-comprehensive-rag-ai-agent/02-tue-agent-architectures|agent architectures]] work. This lesson does not re-teach agents. It teaches where they sit in a product backend.
- Basic understanding of HTTP, REST, and environment variables.

## The core pattern: thin backend, fat AI workflow

The defining architectural insight for a 2026 AI product: **the backend is thin and the intelligence lives in the AI workflow.** In a traditional SaaS, the backend *is* the product: business logic, data processing, and rules live in server code. In an AI product, much of the "logic" is the model plus the agent plus the prompt, and the backend's job shrinks to a specific, small set of responsibilities:

1. **Persistence.** Store users, their data, their generation history, their settings.
2. **Auth.** Know who the user is and what they can access.
3. **Secrets.** Hold the API keys the frontend must never see.
4. **Orchestration glue.** Receive a request, call the AI workflow, stream or return the result, log it.
5. **Rate and cost control.** Enforce limits so one user cannot run up your API bill.

That is it for the MVP. You are not writing a monolith. You are writing a thin layer that authenticates, persists, guards secrets, and hands the real work to the AI workflows you already built. This is Anthropic's "start simple" guidance applied to the product layer: add backend complexity only when a specific need forces it.[^1] The mistake is building a heavyweight backend for an AI product, duplicating in server code the intelligence that lives in the model.

## The BaaS decision: Supabase, Neon, Firebase, and when to roll your own

Backend-as-a-Service gives you database, auth, and often storage without running servers. For an MVP this is almost always correct: it collapses weeks of backend work into an afternoon. The 2026 options, with current pricing verified.

### Supabase — the Postgres BaaS with batteries

Supabase is Postgres plus auth, storage, realtime, and edge functions. Current pricing:[^2]

- **Free:** 500MB database, 1GB file storage, 5GB egress, 50,000 monthly active users, 500,000 edge-function invocations, 2 active projects. The catch that bites MVPs: **free projects pause after 7 days of inactivity**, so it is not suitable for a production app that needs 24/7 uptime.[^2]
- **Pro: $25/month.** Removes the pause, adds daily backups, 100,000 MAUs included, then $0.00325 per additional MAU.[^2]
- **Team: $599/month** and Enterprise custom, which you will not need for an MVP.[^2]

Supabase wins when you want Postgres with auth and realtime bundled, and it is the default the code-gen tools (especially Lovable and v0) integrate natively, which matters for the generate-then-own workflow.

### Neon — serverless Postgres, now a Databricks company

Neon is serverless Postgres with scale-to-zero and database branching. The material 2026 fact: **Databricks acquired Neon in May 2025 for around $1 billion,** and a striking driver was that over 80% of databases on Neon were being created by AI agents rather than humans.[^3] After the acquisition, Neon cut prices: storage dropped roughly 80% (from about $1.75 to $0.35/GB-month), compute fell 15 to 25%, the old $5/month minimum was removed so paid plans are purely usage-based, and the free plan's compute doubled to 100 CU-hours.[^4] Current pricing runs about $0.106/CU-hour on Launch and $0.222/CU-hour on Scale, storage $0.35/GB-month.[^4]

Neon wins when you want pure usage-based Postgres that scales to zero (you pay nothing when idle), database branching for preview environments, and an agent-friendly provisioning model. The scale-to-zero property is genuinely useful for an early product with bursty traffic.

### Firebase — the document-database option

Firebase (Google) is the incumbent BaaS, document-oriented rather than relational, with strong realtime and mobile SDKs. It wins for mobile-first products and realtime-heavy apps. For a web AI product with relational data (users, generations, relationships between them), Postgres via Supabase or Neon is usually the more natural fit, and the code-gen tools lean Postgres. Firebase is a defensible choice but not the default for this week's product shape.

### When to roll your own

Roll your own backend (a Node/Python server plus a managed Postgres) when you need control the BaaS does not give: custom auth logic the provider cannot express, data-residency requirements, or a scale where the BaaS pricing inverts against you. For an MVP, this is premature almost always. The BaaS lock-in is real but recoverable (Postgres is Postgres; you can migrate the data), and the weeks of setup you save buy you weeks of talking to users. Ship on BaaS, migrate if and when a specific limit forces it.

## The serverless-versus-long-running problem, which AI workloads force

This is the backend decision that AI products get wrong most, because it does not arise for ordinary web apps. Serverless functions are cheap, scale automatically, and are perfect for short requests. But they *time out*, and AI workloads are long.

The concrete limits, verified current on Vercel as the canonical example:[^5][^6][^7]

- With **Fluid compute**, the default function duration is **5 minutes (300 seconds) across all plans.**[^5][^6]
- Setting `maxDuration` above 300 seconds requires Pro or Enterprise, and functions can now run up to **30 minutes** on Node.js/Python runtimes (in beta), more than 2x the previous 800-second cap.[^7]
- Fluid compute lets multiple invocations share one function instance, which is valuable for AI because the waits are I/O-bound (calling the model, querying a vector DB), so one instance can serve several concurrent generations efficiently.[^5]

The decision rule for a given AI workload:

**Use a serverless function (streaming) when:** the AI response completes within the timeout, which covers most single-turn generations and chat. Stream the response so the user sees progress and the connection stays alive. A 20-second streamed generation fits comfortably in the 5-minute default.[^5] This is the Saturday build's shape.

**Use a background job / durable workflow when:** the work exceeds the timeout or must survive failure. A multi-step agent that searches the web, processes documents, and drafts a report can blow past 5 minutes, and if the function dies at minute 4 you lose everything. This is where the [[block-3-advanced-topics-voice/week-08-automation-agent-integration-mcps--build-hybrid-agent-scraper-summarizer/05-fri-reliability-engineering-for-unattended-agents|reliability engineering]] from Block 3 becomes a product-backend concern. The options (detailed Friday): a job queue (Inngest, Trigger.dev, QStash), or a durable-execution layer (Vercel Workflows, which breaks the agent into suspendable steps that persist state and resume across invocations).[^8]

The failure mode to internalize: **running a long agent synchronously inside a serverless request.** It works in the demo (short prompt, fast run) and dies in production (real prompt, function timeout), silently dropping the user's job. The fix is architectural, not a config bump: long work goes to a queue or a durable workflow, and the frontend polls or subscribes for the result.

## API design for AI endpoints

AI endpoints differ from CRUD endpoints in shape, and designing them deliberately saves you pain.

1. **Streaming endpoints return a stream, not JSON.** A generation endpoint should return Server-Sent Events (the AI SDK v5 default) so the frontend can render tokens as they arrive.[^5] Do not buffer the whole response and return it as one JSON blob; that reintroduces the bare-spinner latency Tuesday warned against.
2. **Idempotency for retries.** Non-determinism plus network flakiness means retries happen. A "generate report" endpoint that a retry double-charges or double-creates is a bug. Use an idempotency key so a retried request is safe.
3. **Async endpoints return a job ID, not a result.** For long work, the endpoint accepts the request, enqueues the job, and returns a job ID immediately. A separate endpoint (or a subscription) returns the result when ready. This is the async pattern Friday wires end to end.
4. **Every AI endpoint logs cost and tokens.** The backend is where you meter. Log input tokens, output tokens, model, and cost per call so your unit economics are visible from day one. You cannot price a product whose per-call cost you do not measure.
5. **Validate and sanitize inputs.** User input flows into a prompt, and prompt injection is a real attack surface. The OWASP Agentic Top 10 (2026) names prompt injection and tool-poisoning as top agent risks, and the backend is where you enforce input boundaries.[^9]

## Secrets and environment: the boundary that must not leak

The single most expensive backend mistake for an AI product is leaking an API key. A key exposed in frontend code or a public repo becomes anyone's free access to your metered model, and the bill is yours. The rules:

1. **API keys live in the backend only, in environment variables, never in frontend code.** The frontend calls *your* endpoint; your endpoint calls the model with the key. The key never reaches the browser. This is non-negotiable and it is the primary reason an AI product needs a backend at all rather than calling the model from the client.
2. **Use `.env.local` for development, the platform's env-var UI for production,** and never commit either. A committed `.env` in a public repo is scraped within minutes.
3. **Separate keys per environment.** Development, staging, and production get different keys so a leaked dev key does not expose production, and you can rotate one without breaking the others.
4. **Least-privilege keys.** Where the provider supports scoped keys, scope them. A key that can only do inference cannot also delete your account.
5. **Rotate on any suspicion.** If a key might have leaked, rotate immediately. The cost of rotation is minutes; the cost of a leaked key is your entire API budget.

## Where the Block 2 and 3 agents plug in

You already built the intelligence. This lesson is about *placement*, not re-teaching. The agents and automations from earlier blocks become backend services the thin backend calls:

- A **RAG agent** (Block 2/3) becomes a backend function: request comes in, the function calls the retrieval-plus-generation workflow, streams the answer with citations back. The [[block-3-advanced-topics-voice/week-06-beyond-prompt-engineering-context-engineering--advanced-rags/04-thu-agentic-retrieval|agentic retrieval]] architecture runs inside this function or a durable workflow if it is long.
- An **unattended automation** (Block 3) becomes a scheduled backend job (a cron) or an event-triggered job, not a synchronous request. The report generator from b2w05 is exactly this shape: a scheduled durable workflow, not a request handler.
- A **voice or chat agent** (Block 3) sits behind a streaming endpoint plus a session store in your database.

The mental model: the thin backend is the *dispatcher* and the *persistence layer*; the agents are the *workers*. Your product code routes, authenticates, persists, and meters; the agents do the intelligent work. This is the orchestrator-workers pattern from Anthropic's effective-agents guidance, lifted to the product boundary.[^1]

## Controversy: BaaS lock-in versus roll-your-own

A live debate with real money on both sides.

**The BaaS camp.** Use Supabase or Neon and ship this week. The setup you avoid (auth, database provisioning, connection pooling, backups) is weeks of undifferentiated work that brings you zero closer to product-market fit. Lock-in is overstated: your data is standard Postgres, exportable and migratable, and the auth you would hand-roll is a security liability compared to a provider that has audited theirs. For a solo operator, BaaS is not a compromise, it is leverage.

**The roll-your-own camp.** BaaS lock-in is real and compounds. The auth model, the RLS policies, the realtime channels, the edge-function idioms all bind you to the provider, and migrating a live product off Supabase is not a data export, it is a rewrite of every integration point. Pricing can invert brutally at scale (the $599 Team tier, per-MAU charges, egress fees). And a provider outage is your outage with no recourse. Own your backend and you own your destiny.

**The synthesis this lesson commits to:** ship on BaaS for the MVP, but *architect the seam.* Keep your data access behind a thin data layer in your code rather than sprinkling provider-specific calls through every component, so that if you must migrate, you rewrite one module, not the whole app. Use the BaaS for what is genuinely undifferentiated (auth, persistence, storage) and keep your AI-workflow orchestration in your own code where it is portable. The lock-in that hurts is the lock-in you did not isolate; the lock-in you contained behind an interface is a vendor choice you can revisit. The camps are really arguing about *isolation discipline*, and the operator move is to take BaaS velocity now while keeping the escape hatch cheap. Migrate when a specific limit (price inversion, a feature you cannot get, a compliance requirement) forces it, not preemptively.

## Worked example — the Saturday backend shape

Previewing the build's backend:

1. **Supabase project** for auth and persistence: a `users` table (managed by Supabase Auth), a `generations` table (user_id, prompt, response, tokens, cost, created_at).
2. **A Next.js API route** (`/api/generate`) as the streaming endpoint: authenticates the user via Supabase, checks their rate limit, calls the Anthropic model with the server-side key, streams the response back, and logs the generation to the `generations` table.
3. **Secrets** in Vercel/local env: `ANTHROPIC_API_KEY`, `SUPABASE_URL`, `SUPABASE_SERVICE_KEY`, none in frontend code.
4. **No queue needed for v1** because the generation fits in the 5-minute serverless window and streams. The queue is the v2 move when you add a long multi-step agent.

The point: the backend is genuinely thin. One table, one streaming route, three secrets. The intelligence is the model call; the backend authenticates, meters, and persists around it.

## Runnable experiment — design your backend, with a pass bar

**Setup (10 min).** Take the AI feature you are building Saturday. You will design its backend before writing it.

**Phase 1 — data and auth (20 min).** Sketch the minimal schema: which tables, which columns, which belong to a user. Decide auth (Supabase Auth is the default). Write down where each secret lives and confirm none touch the frontend.

**Phase 2 — the timeout decision (20 min).** For your AI workload, decide serverless-streaming or background-job, and justify it with the actual expected duration. If it fits the 5-minute window and streams, serverless. If it is a multi-step agent that could exceed it or must survive failure, background job. Write the decision and the number behind it.

**Phase 3 — the API surface (20 min).** Design each endpoint: method, input, output (stream or JSON or job-ID), what it logs, how it rate-limits, how it validates input against prompt injection. Name the idempotency strategy for retries.

**Pass bar:** No API key appears anywhere reachable by the frontend; every AI endpoint logs tokens and cost; the timeout decision cites the actual expected duration and matches it to the right architecture; the schema separates per-user data with a clear ownership column; and you named an input-validation strategy for the prompt-injection surface. If a key could reach the browser, or a long agent runs synchronously in a request, you have not passed.

## Common mistakes experts see

1. **API keys in the frontend.** The most expensive mistake. The key must live server-side only; the frontend calls your endpoint, your endpoint calls the model.
2. **Long agents in synchronous requests.** Works in the demo, times out in production, silently drops the job. Long work goes to a queue or durable workflow.
3. **Building a fat backend for an AI product.** Duplicating in server code the intelligence that lives in the model. The backend is thin: persist, auth, secrets, glue, meter.
4. **No cost metering.** Shipping without logging tokens and cost per call, then being unable to price the product or explain the API bill.
5. **Free-tier surprise.** Deploying on Supabase free and discovering the project paused after 7 days of inactivity, taking the product down.[^2]
6. **Committed secrets.** A `.env` in a public repo, scraped and abused within minutes.
7. **Provider-specific calls everywhere.** Sprinkling Supabase SDK calls through every component so migration means a full rewrite instead of one module.
8. **No input validation on prompt paths.** User input flowing straight into a prompt with no boundary, opening the prompt-injection surface OWASP names.[^9]

## Reflection questions

1. For your product, what is genuinely in the thin backend versus in the AI workflow? Draw the line and defend it.
2. Your AI workload takes N seconds in the happy case and could take M seconds in the worst case. Which architecture, and what happens to the user's job if the function dies at the timeout?
3. Where does every secret in your product live, and can you prove none is reachable from the browser?
4. You chose a BaaS. What is the one module you would isolate the provider behind so migration is cheap, and what provider-specific behavior are you deliberately keeping out of your components?
5. What is your rate-limit and cost-cap strategy so one user (or one bug) cannot run up your entire API budget?
6. Where is the prompt-injection surface in your backend, and what boundary do you enforce on user input before it reaches the model?

## My take (reviewer lens)

**Simon Willison** would push hard on the prompt-injection treatment as too light. His position, consistent across his writing, is that prompt injection is unsolved and that any product piping user input into a model with tool access has a real, un-patchable attack surface, not a checkbox you tick with "input validation." He is right, and the lesson understates it deliberately for an MVP scope: the honest position is that for a product where the model has no dangerous tools (just generation over the user's own data), the risk is contained, but the moment you give the agent tools that touch other systems, you are in lethal-trifecta territory (private data, untrusted input, exfiltration channel) and the Block 3 security material becomes load-bearing, not optional. Do not read "validate input" as "problem solved."

**Michael Seibel** would push back on the BaaS-isolation discipline as premature abstraction: "You have no users. Call Supabase directly from wherever you want, ship it, and worry about migration when you have a reason to migrate, which you probably never will." The steelman is strong: most MVPs die before lock-in matters, and building a data-access abstraction layer for a product with zero users is exactly the gold-plating he warns against. The line the lesson holds is softer than a full abstraction: keep the *AI-workflow orchestration* portable (it is your actual product) and do not agonize over isolating every Supabase call. The auth and CRUD lock-in is cheap to accept; the AI-logic lock-in is the one worth keeping in your own code.

**Chip Huyen** would push on the cost-metering framing as necessary but insufficient: logging tokens per call is table stakes, but the real discipline is a cost *model* that ties per-call cost to a per-user unit economic, so you know at what usage level a user becomes unprofitable and can price or rate-limit accordingly. Fair, and it is why the pass bar requires metering and the rate-limit strategy together: metering without a cost model is data you never act on. The product-layer cost model connects forward to the analytics and pricing work in Block 4.

## Further reading

**Must-read (this week):**
1. **Supabase pricing** — supabase.com/pricing. Know the free-tier limits and the 7-day pause before you deploy.[^2]
2. **Vercel Fluid compute and function limits** — vercel.com/docs/fluid-compute and /functions/limitations. The timeout numbers that dictate your architecture.[^5][^6]
3. **Anthropic, "Building Effective Agents"** — the orchestrator-workers and start-simple guidance, applied here to the product boundary.[^1]

**Recommended:**
4. **Databricks acquires Neon** — databricks.com/blog/databricks-neon, plus a 2026 Neon pricing breakdown. The serverless-Postgres option and why agents drove the acquisition.[^3][^4]
5. **OWASP Agentic Top 10 (2026)** — the agent-risk taxonomy your input validation and secrets discipline defend against.[^9]

**Optional:**
6. **Vercel: functions can now run up to 30 minutes** — the changelog on the extended-duration beta for longer AI work.[^7]

## Citations

[^1]: Anthropic, "Building Effective Agents" (anthropic.com/research/building-effective-agents), December 2024. Source for start-simple, orchestrator-workers, and add-complexity-only-when-needed, applied to the thin-backend pattern. Also cited in b2w05.

[^2]: Supabase pricing and free-tier limits (supabase.com/pricing and supabase.com/docs/guides/functions/pricing). Source for Free (500MB db, 50K MAU, 500K edge-function invocations, 2 projects, 7-day inactivity pause), Pro $25/mo (100K MAUs, $0.00325/additional), Team $599/mo. (search-verified 2026-07-17 across supabase.com, uibakery.io, makerkit.dev; fetch egress-blocked — liveness pass pending.)

[^3]: Databricks, "Databricks Agrees to Acquire Neon" (databricks.com/company/newsroom). Source for the ~$1B May 2025 acquisition and the finding that over 80% of Neon databases were created by AI agents. (search-verified 2026-07-17 across databricks.com and tech-insider.org; fetch egress-blocked — liveness pass pending.)

[^4]: Neon 2026 pricing breakdowns (vela.simplyblock.io, vantage.sh/blog/neon-acquisition-new-pricing). Source for post-acquisition price cuts: storage ~80% down to $0.35/GB-month, compute 15-25% down (~$0.106/CU-hour Launch, $0.222 Scale), $5/mo minimum removed, free plan compute doubled to 100 CU-hours. (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending.)

[^5]: Vercel, Fluid compute docs (vercel.com/docs/fluid-compute) and streaming-functions docs. Source for 5-minute (300s) default duration across plans, instance-sharing for I/O-bound AI work, and streaming to keep connections alive. (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending.)

[^6]: Vercel Functions limitations (vercel.com/docs/functions/limitations) and duration configuration docs. Source for maxDuration >300s requiring Pro/Enterprise and per-function configuration above 800s. (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending.)

[^7]: Vercel changelog, "Vercel Functions can now run up to 30 minutes" (vercel.com/changelog). Source for the 30-minute extended-duration beta on Node.js/Python, >2x the prior 800s cap. (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending.)

[^8]: Vercel Workflows (part of the AI SDK ecosystem, 2026). Source for durable execution breaking agent tasks into suspendable/resumable named steps that persist state across invocations, solving the serverless-timeout limit. Detailed in Friday. (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending.)

[^9]: OWASP Agentic Top 10 (2026) and the vault landscape delta's MCP-security section. Source for prompt injection and tool-poisoning as top agent risks and the input-boundary discipline. (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending.)

_last_verified: 2026-07-17_
