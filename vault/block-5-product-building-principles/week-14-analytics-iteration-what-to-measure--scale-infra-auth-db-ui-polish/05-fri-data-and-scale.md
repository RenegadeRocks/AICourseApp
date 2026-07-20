---
type: lesson
block: block-5-product-building-principles
week: week-14
session_slug: scale-infra-auth-db-ui-polish
day_of_cycle: 5
day_name: fri
date_due: 2026-08-21
tags:
  - postgres
  - managed-database
  - neon
  - supabase
  - migrations
  - connection-pooling
  - caching
  - pgvector
  - premature-scaling
  - cost-curve
sources:
  - neon-supabase-pricing-2026
  - neon-serverless-driver-2026
  - supavisor-pooling-2026
  - postgres-for-everything-2024
  - startup-genome-premature-scaling-2011
  - chip-huyen-ai-engineering-2025
  - pgvector-scale-2026
  - redis-caching-2024
  - anthropic-prompt-caching-2025
last_verified: 2026-07-17
word_count_target: 5200
---

# Data & scale: Postgres until it hurts, and knowing when it actually hurts

## Why this matters

The internet is full of scaling advice written by companies with a thousand
engineers and a billion requests, and almost all of it is poison for you. This
lesson gives you the opposite: the boring, correct data architecture for a
product with real but modest users, plus honest thresholds for when each "scale"
concern becomes real rather than imaginary. The trap this week keeps returning to
has a name and a body count, and nowhere is it more seductive than infrastructure:
premature scaling. You will leave able to choose a database, run migrations
without downtime, pool connections, cache the right things, keep your vector store
sane, and model the one cost curve that is genuinely different for AI products, all
without building for a scale you do not have.

## Prerequisites

- [[block-3-advanced-topics-voice/week-06-beyond-prompt-engineering-context-engineering--advanced-rags/03-wed-retrieval-beyond-naive-rag|Retrieval at scale]]
  (Block 3). That is the canonical home for retrieval architecture and vector
  search. Today we cover only the *operational* side of the vector store under
  load, and link the rest.
- [[04-thu-auth-and-security-for-real-users|Thursday's RLS]]. Your data layer and
  your isolation layer are the same Postgres; the migration discipline here keeps
  that wall intact as the schema evolves.
- [[03-wed-the-iteration-loop|Wednesday's premature-scaling theme]]. Infra is where
  it bites hardest.

## First principles: the answer is Postgres, and you should feel a little bored

For roughly 95% of products at this stage, the correct database is **one Postgres
instance.** Not a microservice mesh, not a polyglot-persistence diagram, not
Kubernetes. Postgres. It does relational data, JSON documents (`jsonb`), full-text
search, vector search (`pgvector`), queues (`SELECT ... FOR UPDATE SKIP LOCKED`),
and geospatial, all in one boring, battle-tested engine you can reason about. The
"just use Postgres for everything" movement exists precisely because teams keep
adding specialized datastores they do not need and drowning in the operational
complexity.[^1] Every additional datastore is a new thing to secure, back up,
monitor, and keep consistent. Default to one Postgres; add a second system only
when a specific, measured pain forces it.

This is not a lack of ambition; it is the discipline that lets you spend your
scarce attention on the product instead of on infrastructure you will not stress
for years. Startup Genome's finding applies directly: elaborate infrastructure
before product/market fit is the textbook premature-scaling failure.[^2]

## Part 1 — Managed Postgres in 2026: Neon vs Supabase

You should not run your own database server. Managed Postgres is cheap, backed
up, and one less thing to page you at 3am. The 2026 decision is largely **Neon vs
Supabase**, and they optimize for different things.

**Neon** is serverless-first Postgres with **scale-to-zero** and **database
branching**. It separates storage from compute, so an idle database costs almost
nothing (compute suspends), and you can branch your database like git for
per-PR preview environments. 2026 pricing dropped launch compute to about $0.106
per compute-unit-hour, storage to a flat $0.35/GB-month, and removed the old $5
monthly minimum; Pro starts around $19/mo plus usage.[^3] Neon ships a **native
serverless driver** (`@neondatabase/serverless`) that uses WebSocket/HTTP so
serverless functions do not exhaust connections, plus a built-in PgBouncer-based
pooler.[^3][^4] Reach for Neon when you deploy on serverless/edge and want
scale-to-zero economics and branch-per-preview.

**Supabase** is the batteries-included Postgres platform: database plus auth
(Thursday), storage, realtime, and edge functions. Pro is $25/mo plus overages.
Its connection pooler, **Supavisor** (Elixir-based), is built for extreme
concurrency and benchmarked past a million connections; it also offers PgBouncer
in transaction mode.[^5] Reach for Supabase when you want the integrated platform
(you already met its RLS-based auth on Thursday) and value one vendor for
database + auth + storage.

> My take: for this course's product, either is correct and the choice usually
> falls out of Thursday's auth decision. If you picked Supabase Auth, use Supabase
> Postgres; the integration is the point. If you want scale-to-zero economics and
> preview-branch-per-PR, Neon is delightful. Do not agonize; both are managed
> Postgres and migrating between them is a `pg_dump`/`pg_restore`, not a rewrite.

## Part 2 — Migrations: change the schema without breaking production

The moment you have real users, you have data you cannot lose and a schema you
must keep changing. **Migrations** are versioned, ordered, reversible changes to
your schema, checked into your repo and applied in the same order everywhere. The
non-negotiable rule: **never change a production schema by hand.** Every change is
a migration file, reviewed in a PR, applied by tooling. This is what keeps
Thursday's RLS policies intact as tables evolve, and it is what lets you roll back
when a change goes wrong.

Two disciplines that prevent outages:

1. **Expand/contract (a.k.a. the multi-step migration).** You cannot rename a
   column in one step without breaking the running old code during deploy.
   Instead: *expand* (add the new column, write to both), *migrate* (backfill),
   *contract* (stop using the old, then drop it), across separate deploys. This
   lets old and new code coexist during rollout. Any migration that both changes
   a column and is deployed alongside code that reads it must be
   expand/contract, or you get downtime.
2. **Backfills run separately from schema changes.** A migration that adds a
   column *and* backfills a million rows will lock your table and take your
   product down. Add the column in a migration (fast), backfill in a background
   job (slow, batched, non-locking).

Use your framework's migration tool (Prisma Migrate, Drizzle Kit, or plain SQL
files with a runner). Saturday's code-lab uses ordered SQL migration files so the
mechanism is visible and framework-agnostic. The tool matters less than the
discipline: ordered, versioned, reviewed, reversible, never by hand.

## Part 3 — Connection pooling: the failure that hits at surprisingly small scale

Here is a scale problem that is *not* premature to worry about, because it bites
early. Postgres handles a limited number of concurrent connections (often ~100 by
default, fewer on small managed tiers). Each serverless function invocation or
each app instance can open its own connections, and under even modest concurrency
you exhaust the limit and requests start failing with "too many connections." This
surprises people because it happens at hundreds of concurrent users, not
millions.

The fix is a **connection pooler** between your app and Postgres: PgBouncer,
Supabase's Supavisor, or Neon's built-in pooler.[^4][^5] The pooler multiplexes
many client connections onto a few database connections. Two things to get right:

- **Use transaction-mode pooling for serverless.** In transaction mode a
  connection is handed back to the pool after each transaction, so hundreds of
  short serverless requests share a handful of real connections. (Session mode
  holds a connection for a whole client session; wrong for serverless.)
- **On serverless/edge, prefer the serverless driver.** Neon's HTTP/WebSocket
  driver sidesteps the connection-lifecycle problem entirely for one-shot
  queries.[^4]

This is the one "scale" topic where the honest threshold is *low*: wire pooling
in from the start if you deploy serverless, because the failure arrives with your
first modest traffic spike, not your millionth user.

## Part 4 — Caching: cache the expensive and the repeated, nothing else

Caching is where premature optimization loves to hide. The rule: cache only what
is **expensive to compute** *and* **repeatedly requested** *and* **tolerant of
staleness.** Everything else, do not cache; a cache you do not need is just a
second source of truth that will eventually disagree with the first and produce a
bug you will spend a day chasing.

Where caching genuinely earns its place in an AI product:

- **Expensive read queries** that many users hit (a dashboard aggregate, a
  reference dataset). Redis or even an in-Postgres materialized view.
- **AI responses themselves,** in two forms. First, **application-level response
  caching**: identical requests (same prompt, same context) return a stored
  result instead of paying the model again. Second, **prompt caching at the model
  provider**: Anthropic's prompt caching lets you cache a large stable prefix (a
  long system prompt, a big document) so repeated calls that share it are far
  cheaper and faster, which is directly relevant to your cost curve (Part 6).[^6]
- **Embeddings,** which are deterministic for a given input+model, so re-embedding
  the same text is pure waste. Cache them.

Redis is the default for a shared cache; for a single instance, an in-process LRU
is often enough.[^7] Do not reach for a distributed cache until you have measured
that a simple one is insufficient.

## Part 5 — The vector store under load

Retrieval architecture lives in [[block-3-advanced-topics-voice/week-06-beyond-prompt-engineering-context-engineering--advanced-rags/03-wed-retrieval-beyond-naive-rag|Block 3]];
this is only the operational overlay. The key 2026 decision for most products:
**do you even need a dedicated vector database, or does `pgvector` in the Postgres
you already run suffice?** For the low millions of vectors, `pgvector` with an
HNSW index is genuinely enough, and keeping vectors in the same Postgres as your
relational data means one database to secure, back up, and join against (you can
filter by `tenant_id` *and* do vector search in one query, which keeps Thursday's
RLS wall around your embeddings too).[^8] You graduate to a dedicated vector store
(and the operational cost of a second system) only when index size or query
latency in Postgres becomes a measured problem, typically past tens of millions of
vectors or under heavy filtered-search load. Default to `pgvector`; add a
specialized store on evidence, not anticipation.

## Part 6 — The one cost curve that is genuinely different

Traditional SaaS has near-zero marginal cost per request; scaling users barely
moves COGS. AI products do not have this luxury, and this is the scale concern
that is *never* premature to model. Every active user generates token cost that
scales with usage, and that cost has three multipliers you must track:

1. **The tokenizer.** The current-generation Anthropic tokenizer produces roughly
   30% more tokens for the same text than the prior generation, so cost estimates
   carried over from last year understate the bill by about a third.[^9] Re-baseline
   your COGS on the current tokenizer.
2. **Model routing.** Sending every request to a frontier model when a smaller,
   cheaper model would do is often a 5–10× cost multiplier for imperceptible
   quality change. Route per feature (Wednesday's model-iteration loop), and let
   your quality-drift and feature-trust metrics tell you when a cheaper model is
   fine.[^10]
3. **Regeneration and retries.** Every regeneration (Monday, metric 2)
   re-pays the full token cost. A high regeneration rate is a *cost* problem as
   much as a trust problem.

Model this as **cost-per-active-user** (Monday, metric 5) and watch its ratio to
revenue-per-active-user. Chip Huyen's *AI Engineering* is emphatic that inference
cost is a first-class production and product concern, not an afterthought you
reconcile at invoice time; the teams that survive model it continuously and design
features (caching, routing, output-length limits) to keep the ratio healthy.[^10]

## When to actually worry about scale: honest thresholds

The whole point of this lesson, in a table. These are rough, opinionated bars for
a typical AI SaaS; your product may differ, but the *shape* holds — worry about
few things early, most things late, and one thing (cost) always.

| Concern | Worry now? | Real threshold |
|---|---|---|
| Connection pooling | **Yes, if serverless** | First modest traffic; failure comes early |
| Cost-per-active-user | **Always** | Day one; it sets your pricing floor |
| Migrations discipline | **Yes** | The moment you have data you can't lose |
| Tenant isolation (RLS) | **Yes** | Before your second tenant (Thursday) |
| Caching | Mostly no | When a measured hot path is slow *and* repeated |
| Dedicated vector DB | No | Tens of millions of vectors / measured pgvector pain |
| Read replicas | No | When one instance's read load is measurably maxed |
| Sharding / multi-region | Almost never at this stage | A specific latency/residency requirement |
| Kubernetes | No | When a managed platform genuinely can't serve you |

The pattern: the things worth doing early (pooling, cost modeling, migrations,
isolation) are cheap to do now and expensive to retrofit. The things people
*reach* for early (sharding, k8s, a vector DB, microservices) are the premature
scaling that kills.[^2]

## Worked example

The cost-curve model that decides your pricing, in runnable form. Saturday's
code-lab adds the live metrics endpoint; today, the projection.

```python
# cost_curve.py — model cost-per-active-user before it surprises you.
# Run: python cost_curve.py   (stdlib only)

# Current-tokenizer, current-model rough rates (verify against your provider).
RATE_IN  = 2.00 / 1_000_000   # $ per input token  (mid-tier default model)
RATE_OUT = 10.00 / 1_000_000  # $ per output token

def cost_per_request(in_tokens, out_tokens, regen_rate, cache_hit_rate):
    # regenerations re-pay full cost; cache hits pay a fraction on input.
    effective_in = in_tokens * (1 - cache_hit_rate + 0.1 * cache_hit_rate)
    base = effective_in * RATE_IN + out_tokens * RATE_OUT
    return base * (1 + regen_rate)

def monthly_cost_per_active_user(requests_per_user_month, **kw):
    return requests_per_user_month * cost_per_request(**kw)

if __name__ == "__main__":
    cpau = monthly_cost_per_active_user(
        requests_per_user_month=200,
        in_tokens=3000, out_tokens=600,
        regen_rate=0.30,        # Monday's metric 2 — costs you real money
        cache_hit_rate=0.50,    # prompt caching a stable prefix
    )
    price = 20.00
    print(f"cost/active user/mo: ${cpau:.2f}")
    print(f"gross margin at ${price}/mo: {100*(price-cpau)/price:.0f}%")
    print("WARN: margin below 70% — cut regen, route cheaper, or raise price"
          if (price - cpau) / price < 0.70 else "margin healthy")
```

**Pass bar:** run it, then change `regen_rate` from 0.30 to 0.05 and watch the
margin jump. That single lever, driven by Monday's regeneration metric and
improved by Wednesday's prompt-iteration loop, is often the difference between a
70% margin and a 40% one. If you can see that in the output, you understand why
the AI cost curve is the one scale concern that is never premature.

## Common mistakes experts see

1. **Adding datastores you don't need.** Every extra system is more to secure,
   back up, and keep consistent. Default to one Postgres.[^1]
2. **Hand-editing production schema.** Every change is a reviewed, ordered,
   reversible migration. No exceptions.
3. **Backfilling inside a schema migration.** Locks the table, takes you down.
   Add column fast, backfill in a batched background job.
4. **Skipping connection pooling on serverless.** "Too many connections" arrives
   at hundreds of users, not millions. Pool from the start.[^4][^5]
5. **Caching by reflex.** A cache you don't need is a second source of truth that
   will disagree with the first. Cache only expensive + repeated + staleness-OK.
6. **Ignoring the cost curve until the invoice.** With the current tokenizer
   adding ~30%,[^9] a margin you never modeled can invert. Model it day one.
7. **Reaching for a vector DB / sharding / k8s early.** The signature moves of
   premature scaling. Add on measured evidence, never anticipation.[^2]

## Reflection questions

1. What is the smallest datastore set your product actually needs? Which extra
   system were you tempted to add, and what specific measured pain would justify
   it?
2. Write the expand/contract steps for renaming one column in your schema without
   downtime. Where would naive single-step do damage?
3. If you deploy serverless, where is your connection pooler, and what happens at
   500 concurrent users if it is missing?
4. Compute your current cost-per-active-user with the runnable model. What is your
   margin at your current price, and which lever moves it most?
5. At what exact vector count or latency number would you move off `pgvector`?
   If you can't name it, you are not close enough to need a vector DB.

## My take (reviewer lens)

**Michael Seibel** would love this lesson and want it shorter: "use Postgres,
model your costs, ignore the rest until it breaks." That is basically the thesis,
and he is right that the honest-thresholds table is the only part a pre-PMF
founder truly needs.[^2] Where I would defend the extra pages: the AI cost curve
genuinely *is* different from the SaaS he built, and a founder who ignores it the
way you could safely ignore COGS in classic SaaS gets a nasty surprise.

**Chip Huyen** would push the cost and reliability sections harder: in her
framing, inference cost, latency, and quality are a joint optimization, and
treating cost as a separate tile understates how tightly it couples to model
choice and caching architecture.[^10] Correct, and Wednesday's model-routing loop
plus this lesson's caching section are meant to be read together as that joint
optimization.

**A cohort peer** would ask the honest question: "You spent Thursday on RLS and
Friday telling me not to over-build — isn't RLS over-building at four users?" No,
and the table says why: isolation and pooling and cost are the *cheap-now,
expensive-later* quadrant. The discipline is not "never prepare," it is "prepare
the things that are painful to retrofit, defer the things that are easy to add."
That distinction is the whole skill.

## Further reading

**Must-read**

- The "just use Postgres for everything" writeups, for the default-to-one-datastore
  discipline.[^1]
- Chip Huyen, *AI Engineering* (2025), inference-cost and production chapters.[^10]

**Recommended**

- Neon vs Supabase 2026 comparisons, for current managed-Postgres economics.[^3]
- Anthropic prompt-caching docs, for the cheapest lever on your cost curve.[^6]

**Optional**

- pgvector-at-scale writeups, for the "when to leave Postgres for vectors"
  threshold.[^8]

## Citations

[^1]: "Just use Postgres for everything" / radical simplicity movement — one
Postgres for relational, JSON, full-text, vectors, queues.
https://www.amazingcto.com/postgres-for-everything/ (search-verified 2026-07-17;
corroborated by https://blog.sequinstream.com/all-the-things-postgres-can-replace/).
[^2]: Startup Genome, "Premature Scaling" (2011) — elaborate infra before PMF is
the top failure mode.
https://s3.amazonaws.com/startupcompass-public/StartupGenomeReport2_Why_Startups_Fail_v2.pdf
(search-verified 2026-07-17.)
[^3]: Neon vs Supabase pricing (2026) — Neon serverless, scale-to-zero, branching,
~$0.106/CU-hr, $0.35/GB-mo, Pro ~$19/mo; Supabase Pro $25/mo.
https://vela.simplyblock.io/articles/neon-serverless-postgres-pricing-2026/ and
https://designrevision.com/blog/supabase-vs-neon (search-verified 2026-07-17; two
domains).
[^4]: Neon serverless driver (`@neondatabase/serverless`, HTTP/WebSocket) + built-in
PgBouncer pooler for serverless connection management.
https://neon.tech/docs/serverless/serverless-driver (search-verified 2026-07-17;
corroborated by the Neon-vs-Supabase comparison above).
[^5]: Supabase Supavisor (Elixir pooler, benchmarked past 1M connections) +
PgBouncer transaction-mode pooling. https://supabase.com/docs/guides/database/connecting-to-postgres
and https://github.com/supabase/supavisor (search-verified 2026-07-17.)
[^6]: Anthropic prompt caching — cache a stable prefix for cheaper/faster repeated
calls. https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching
(search-verified 2026-07-17.)
[^7]: Redis as default shared cache; cache expensive+repeated+staleness-tolerant
only. https://redis.io/docs/latest/develop/use/patterns/ (search-verified
2026-07-17.)
[^8]: pgvector with HNSW is sufficient into the low millions of vectors; keep
vectors in Postgres for joins + RLS; graduate to a dedicated store on measured
pain. https://github.com/pgvector/pgvector (search-verified 2026-07-17;
corroborated by Supabase pgvector docs,
https://supabase.com/docs/guides/ai/vector-columns). Retrieval architecture:
canonical home b3w06.
[^9]: Current Anthropic tokenizer produces ~30% more tokens vs prior generation;
re-baseline COGS. `vault/00-program/_refresh-2026-07-master-report.md`
cross-cutting theme 1. (search-verified 2026-07-17; two-source verification in the
master report.)
[^10]: Chip Huyen, *AI Engineering* (O'Reilly, 2025) — inference cost/latency/
quality as a joint production concern; model routing and caching as levers.
https://www.oreilly.com/library/view/ai-engineering/9781098166298/ (search-verified
2026-07-17.)

_last_verified: 2026-07-17_
