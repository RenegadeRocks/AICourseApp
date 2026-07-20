---
type: lesson
block: block-5-product-building-principles
week: week-14
session_slug: scale-infra-auth-db-ui-polish
day_of_cycle: 6
day_name: sat
date_due: 2026-08-22
tags:
  - build-day
  - production-hardening
  - auth
  - migrations
  - row-level-security
  - observability
  - metrics-endpoint
  - ui-polish
  - capstone
sources:
  - pglite-docs-2026
  - hono-docs-2026
  - supabase-auth-rls-2026
  - simonwillison-lethal-trifecta-2025
  - boris-cherny-workflow-2025
  - twelve-factor-config-2011
  - owasp-agentic-top10-2026
  - seibel-launch-fast-2020
last_verified: 2026-07-17
word_count_target: 5400
---

# Build day: harden the product until a hostile stranger can't break it

## Why this matters

Today the demo becomes a product. You take the thing you built in Weeks 12 and
13, the skeleton and the magic, and you add the four things that separate
"impressive in a screen-share" from "safe to put a login URL in public": real
auth, a versioned schema with migrations, database-enforced tenant isolation, and
observability with one live metric. By the end you will have run a build that
survives a hostile stranger, and you will be able to open your dashboard and see
exactly what that stranger did, without them being able to touch anyone else's
data. This is also the capstone of Block 5: the last screw in the machine you
have been assembling for three weeks.

After this lesson you will have shipped a hardened backend (in
`code-lab/1/`, type-checked, linted, and tested), understand every layer of it
well enough to port it to managed infrastructure, and have a UI-polish checklist
that closes the gap between "works" and "feels finished."

## Prerequisites

- The whole week. Monday's [[01-mon-product-analytics-for-ai-products|metrics]],
  Tuesday's [[02-tue-instrumentation-and-the-analytics-stack|two pipes]],
  Wednesday's [[03-wed-the-iteration-loop|loop]],
  Thursday's [[04-thu-auth-and-security-for-real-users|auth + RLS]],
  Friday's [[05-fri-data-and-scale|data + scale]]. Today assembles them.
- Node.js 20.11+. Everything else is pinned in `code-lab/1/package.json`; the
  database runs in-process (PGlite), so there is nothing to install beyond `npm
  install`.
- Your Week 12/13 product open in another window. The code-lab is a reference
  spine; the goal is to graft these four hardening layers onto *your* product.

## The build, framed: four layers, one pass bar

The pass bar is a sentence: **a hostile stranger logs in, does something, and you
can see it, but they cannot reach anyone else's data or your business numbers.**
Everything today serves that sentence. The four layers:

1. **Auth** so a stranger can log in and be *someone specific*.
2. **Schema + migrations** so their data has a home you can evolve safely.
3. **Tenant isolation (RLS)** so being someone specific means seeing only their
   own rows, enforced where it cannot be bypassed.
4. **Observability + a metric** so you can *see what they did*.

Then a fifth, softer layer: **UI polish**, so the whole thing feels finished.

The code-lab implements all of this as a runnable TypeScript backend using Hono
(a small, fast web framework)[^2] and PGlite (real Postgres compiled to WASM, in
your process, so there is no server to install and RLS works exactly as it will
in production)[^1]. Read the code alongside this lesson; the prose explains the
*why*, the code is the *what*.

## Layer 1 — Auth you did not hand-roll

Open `code-lab/1/src/auth.ts`. Three functions, all built on Node's standard
crypto, none invented:

- `hashPassword` / `verifyPassword` use **scrypt**, a memory-hard KDF, with a
  per-password random salt and a constant-time comparison (`timingSafeEqual`).
  You are not inventing a hash; you are calling a vetted one correctly. The
  constant-time compare matters: a naive `===` on hashes leaks timing that can be
  attacked.
- `newSession` mints an **opaque random token** for the cookie and stores only
  its SHA-256 digest in the database. This is the detail most tutorials get
  wrong: if you store the raw session token, a database dump is a pile of live
  logins. Storing the digest means a stolen dump is useless, exactly like storing
  hashed passwords.

The cookie is set `httpOnly`, `Secure` (in production), `SameSite=Lax`, with an
expiry. `httpOnly` is the one that stops an injected script from stealing the
session; this is why Thursday said never put a session token in `localStorage`.

The login handler in `src/server.ts` has one non-obvious move: it verifies a
password even when the email does not exist (against a dummy hash), so the
response time does not reveal whether an email is registered. That closes user
enumeration, a small leak that helps attackers build target lists.

> Build vs buy reminder (Thursday): this hand-built auth is here so you
> *understand the mechanism*. In your real product you may well swap it for
> Clerk, Better Auth, or Supabase Auth. Keep your `user_id` references
> provider-agnostic and the swap stays a weekend. But do not ship auth you do not
> understand, whichever way you go.

## Layer 2 — Schema and migrations

Open `code-lab/1/migrations/`. Two ordered SQL files, applied by the runner in
`src/db.ts`. The runner records each applied file in a `_migrations` table and
skips ones already applied, so running it repeatedly is safe and every
environment converges to the same schema. This is the whole discipline from
Friday made concrete: **versioned, ordered, reviewed, reversible, never by
hand**.[^7]

`001_init.sql` creates accounts (tenants), users, sessions, and the analytics
event log. Note the event log carries `account_id`, `user_id`, *and*
`request_id` on every row, so the two pipes from Tuesday can join. `002_reports_
rls.sql` creates the tenant-owned `reports` table and its wall (Layer 3).

The pattern to internalize for *your* product: when you need to change this
schema next week, you will not edit these files. You will add `003_whatever.sql`.
And if that change touches a column live code reads, you will use the
expand/contract steps from Friday across separate deploys. The migration files
are an append-only history, not a mutable document.

## Layer 3 — The wall: tenant isolation in the database

This is the layer that, done wrong, ends companies. Open `002_reports_rls.sql`
and `withTenant` in `src/db.ts`. The wall has three parts, and all three are
load-bearing:

1. **The policy.** `create policy tenant_isolation on reports using (tenant_id =
   current_setting('app.tenant_id', true)::uuid)`. The database itself refuses to
   return rows whose `tenant_id` does not match the tenant set on the current
   connection. Not the application. The database.[^3]
2. **FORCE, and a non-superuser role.** This is the sharp edge, and the code-lab
   caught it the honest way: the test *failed the first time*. PGlite (like a
   fresh Postgres) connects as a **superuser**, and superusers bypass RLS
   entirely, even with `FORCE ROW LEVEL SECURITY` on the table. So the policy
   existed and the wall still leaked. The fix, in the migration, is a
   non-superuser role `app_user`; in `withTenant`, every request does `SET LOCAL
   ROLE app_user` before touching data. Now RLS applies. **This is the number-one
   way RLS silently fails open in production**: the app connects as the database
   owner, and nobody notices the wall is off until a customer sees another
   customer's data.
3. **Transaction-scoped setting.** `set_config('app.tenant_id', $1, true)` with
   `is_local => true` means the tenant setting lives only for that transaction, so
   under a connection pool (Friday) it cannot leak onto the next request that
   reuses the connection. The role switch is `SET LOCAL` for the same reason.

Then the part that makes this a *tested* claim rather than a hopeful one, which
is Boris Cherny's whole instinct: `test/isolation.test.ts` spins up two tenants,
has A write a report, and asserts that B (and any unknown tenant) reads zero
rows while A reads its one row. Run `npm test`. If it passes, your wall holds. If
someone later "optimizes" the query in a way that breaks isolation, CI catches it
before a customer does. An untested wall is a wall you are trusting on faith.[^5]

### Why this is also your AI-safety layer

Here is the connection back to Thursday and to
[[block-0-basecamp/week-02-basecamp-part-3-mcps-voice-agents--basecamp-part-4-revisiting-n8n-ai-agent-fundamentals/03-wed-mcp-security|the lethal trifecta]].
When you add your Week 13 AI feature back on top of this backend, the AI's
database access must go through the *same* `withTenant` path, as the *same*
`app_user` role, scoped to the *same* tenant. If it does, then a prompt injection
that convinces the model to "read all reports" still hits the RLS wall and gets
only the current tenant's rows. The AI inherits the user's permissions and cannot
exceed them.[^4][^8] If instead you let the AI query with a superuser or
service-role connection to "make it simpler," you have handed one prompt injection
the keys to every tenant. The wall you built today is the thing that makes your AI
feature safe by construction, not by hoping the model behaves.

## Layer 4 — Observability and one live metric

Open `src/observability.ts` and the `/metrics` route in `src/server.ts`.

**Observability** here is deliberately humble: one structured JSON log line per
request, with `request_id`, method, path, and status, and a `redact()` step that
scrubs sensitive keys (`password`, `token`, `email`) *before* anything is
written. That redaction is the load-bearing part, and it is Simon Willison's
warning made mechanical: your log store must never become the least-secured copy
of your users' PII.[^4] This is real observability. When you add the AI feature,
you extend the same log with the model, tokens, cost, and latency, keyed by the
same `request_id`, and you have Tuesday's two pipes joined. You do not need
Langfuse on day one; you need this, honestly done.

**The live metric.** `/metrics` serves Monday's north star (weekly accounts that
shared a report) and its counter-metric (regeneration rate), computed from the
event log by `src/metrics.ts`. Two production instincts are baked in:

- It is **bearer-protected**. A hostile stranger who finds `/metrics` gets a 403,
  not your business numbers. Your metrics are as sensitive as your data.
- It is **computed from events**, not from a mutable counter. The event log is
  the source of truth; the metric is a query over it. This means you can change
  the metric definition later and recompute history, which you cannot do if you
  incremented a counter at write time and threw the events away.

The typed event taxonomy in `src/events.ts` is Tuesday's discipline: events are
defined once, in one place, and emitted only through `emit()`. No raw string
event names scattered across handlers, so a rename cannot leave half your app
firing the old name. This is the contract-in-code that keeps your analytics from
rotting.

## Layer 5 — The UI-polish pass

The backend is hardened; now the product should *feel* finished. Polish is not
decoration, it is the difference between trust and suspicion. A checklist you can
run in an afternoon on your Week 12/13 frontend:

- **Loading and empty states.** Every async action shows a spinner or skeleton;
  every empty list says something helpful ("No reports yet. Generate your
  first."), not a blank void. Empty states are onboarding in disguise.
- **Error states that a human wrote.** Never surface a raw stack trace or a bare
  "Error." Say what happened and what to do. The auth handlers in the code-lab
  already do this server-side (they never echo the DB error); the frontend must
  match.
- **The AI feature's states.** AI features have failure modes normal features do
  not: the streaming response, the "the model is thinking" state, the "that came
  out wrong, regenerate" affordance (which fires your `ReportRegenerated`
  event). Make the wait feel intentional, not broken.
- **Perceived performance.** Optimistic UI where safe (show the action as done,
  reconcile on the server response), skeletons over spinners for content,
  streaming for AI output so the first token appears fast.
- **Consistency.** One spacing scale, one type scale, one set of colors. This is
  the design-system literacy from Block 2; a product that is *consistent* reads
  as *finished* even when it is simple. Inconsistency reads as broken.
- **Keyboard and focus.** Forms submit on Enter, focus lands in the right place,
  the tab order is sane. Cheap, and the difference between "toy" and "tool."

Polish has a stopping rule: it serves trust and clarity, not your aesthetic
ego. Michael Seibel's caution applies with full force here — do not spend a week
perfecting a gradient while the product does not retain. Polish the paths users
actually walk (signup, the core action, the error they will hit), and ship.[^6]

## Running the build (the pass bar, concretely)

From `code-lab/1/`:

```bash
npm install
cp .env.example .env          # set METRICS_TOKEN to a long random string
npm run typecheck             # tsc --noEmit, strict — must be clean
npm run lint                  # eslint — must be clean
npm test                      # the RLS isolation test — must pass
npm run dev                   # API on http://localhost:3000
```

Then the hostile-stranger walkthrough (full curl script in the code-lab README):
two strangers sign up, each creates a report, and stranger B's `/reports` returns
`{"reports":[]}` because RLS hides A's data. A request to `/metrics` without the
bearer token returns 403; with it, you see the live north star. That is the pass
bar met: a stranger logged in, did something, you saw it in your metric, and they
could reach neither B's data nor your numbers.

**If the isolation test fails,** you have learned the most important lesson of the
day directly: your wall is off. The usual cause is exactly the one the code-lab
hit, a connection running above RLS as a superuser/owner. Fix it before you ship,
because this is the one bug you do not get to fix *after* it happens in
production.

## Block 5 capstone recap: skeleton → magic → hardened

Step back. Three weeks built one machine:

- **Week 12 — the skeleton.** A frontend with basic UI/UX, an MVP backend, wired
  to AI workflows. The product could exist and do its core thing.
  ([[block-5-product-building-principles/week-12-frontend-basic-uiux-design-principles--build-mvp-backend-connect-with-ai-workflows/06-sat-build-ship-the-product-skeleton|Week 12]].)
- **Week 13 — the magic.** Smart AI features that make the product feel alive:
  the wow that turns a utility into something people tell their friends about.
  ([[block-5-product-building-principles/week-13-making-your-product-feel-magic-with-ai--how-to-add-smart-features-that-wow-users/06-sat-build-add-one-magical-feature|Week 13]].)
- **Week 14 — the hardening.** This week: honest measurement (what to count and
  why), the iteration loop that turns numbers into changes, and the
  production-readiness pass (auth, DB, isolation, observability, polish) that lets
  strangers in without letting them break you.

That arc is the whole discipline of shipping software people log into. The AI
machinery from Blocks 2 and 3 (RAG, agents, context engineering, voice) is the
engine; Block 4 packaged and validated it; Block 5 assembled it into a product
and made it survive contact with real users. You now have, or are one weekend
from having, a thing you can charge for and not be terrified to leave running.

## Common mistakes experts see

1. **RLS policy present, wall still open.** The app connects as owner/superuser
   and bypasses RLS. Access data as a non-superuser role, and *test* it.[^3][^5]
2. **Storing raw session tokens.** A DB dump becomes live logins. Store the
   digest, like passwords.
3. **Backfilling inside a schema migration.** Locks the table. Schema change and
   backfill are separate steps (Friday).
4. **Logging raw prompts/PII into observability.** Your log store becomes your
   least-secured PII copy. Redact at the boundary.[^4]
5. **An unprotected metrics endpoint.** Your business numbers are as sensitive as
   your data. Authenticate it.
6. **Polishing the wrong thing.** A perfect gradient on a product that does not
   retain. Polish the paths users walk, then ship.[^6]
7. **Shipping auth you do not understand** because a library made it one line.
   Buy it if you like, but know what sessions, hashing, and cookies are doing.

## Reflection questions

1. Run `npm test`, then deliberately break the wall: change `withTenant` to skip
   the `SET LOCAL ROLE` line. Does the test now fail? What does that tell you
   about how your *real* product connects to its database?
2. When you graft your Week 13 AI feature onto this backend, what is the exact
   database path its tool calls take? Does it go through `withTenant`, or does it
   have a more powerful credential? What breaks if it does?
3. Which auth did you ship for your real product, built or bought, and why? What
   is your migration path if that choice goes wrong?
4. Look at your `/metrics` output. Is the number it shows the one you would
   actually act on (Monday), or a convenient proxy?
5. Run your UI-polish checklist on your product's signup flow. What is the ugliest
   state a new user hits in the first 60 seconds, and is fixing it worth an hour?

## My take (reviewer lens)

**Boris Cherny** would approve of exactly one thing above all: the isolation
claim is a *test that runs in CI*, and it failed first, which is how you know it
tests something real.[^5] His extension would be to make more of the security
posture executable, a test that the metrics endpoint 403s without a token, a test
that session tokens are stored hashed. Anything you assert about security that a
machine does not check is a claim you will eventually violate by accident. He is
right; treat the one isolation test as a template, not the finish line.

**Simon Willison** would push on the AI-boundary section being the point of the
whole build. His view is that since prompt injection has no reliable general
defense, the architecture is the defense, and the single most important
architectural fact is that the AI runs as `app_user` scoped to the tenant, with
no capability the human lacks.[^4] I agree, and I would go further: when you add
the AI back, write the test that proves a malicious prompt still cannot cross
tenants, the same way the isolation test proves a malicious query cannot.

**Michael Seibel** would tell most of you this is more than you need for four
users, and he would be half right. The half he is right about: SOC 2, elaborate
observability, UI perfectionism, all defer. The half he is wrong about: auth and
tenant isolation are the two things that are catastrophic to retrofit and cheap
to do now, because the first cross-tenant leak is not a bug, it is a trust event
you may not survive.[^6] Build these two right before you have users; defer
almost everything else. That is the judgment this whole block has been training.

## Further reading

**Must-read**

- Simon Willison on the lethal trifecta, re-read now that you have the wall that
  defends against it.[^4]
- Supabase Row-Level Security docs, for the production version of what PGlite ran
  locally.[^3]

**Recommended**

- Hono docs, for the framework the code-lab uses (small, fast, edge-ready).[^2]
- OWASP Agentic AI Top 10, for the threat model your wall addresses.[^8]

**Optional**

- PGlite docs, if you want to understand the in-process-Postgres trick you just
  used.[^1]

## Citations

[^1]: PGlite — Postgres compiled to WASM, runs in-process, supports RLS and
standard SQL. https://pglite.dev/ and https://github.com/electric-sql/pglite
(search-verified 2026-07-17; two sources; behavior additionally confirmed by
running the code-lab's migrations and tests locally).
[^2]: Hono — small, fast, multi-runtime web framework; cookie + factory
middleware helpers used here. https://hono.dev/ (search-verified 2026-07-17.)
[^3]: Supabase Row-Level Security docs — DB-enforced tenant isolation; the
production analogue of the code-lab's policy.
https://supabase.com/docs/guides/database/postgres/row-level-security
(search-verified 2026-07-17; corroborated by PostgreSQL RLS docs,
https://www.postgresql.org/docs/current/ddl-rowsecurity.html, which also documents
that superusers and BYPASSRLS roles bypass row security — the footgun the code-lab
hit).
[^4]: Simon Willison, "The lethal trifecta for AI agents" (2025) — architectural
defense; the AI must hold no capability the user lacks; redact PII at the logging
boundary. https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/
(search-verified 2026-07-17; canonical home b0w02).
[^5]: Boris Cherny on executable, tested claims and agent-driven workflows (head
of Claude Code; fleet-scale agent management, Fortune, Jun 2026). An untested
security invariant is a claim you will violate by accident. (search-verified
2026-07-17; reviewer-lens framing per `_refresh-2026-07-master-report.md`.)
[^6]: Michael Seibel (Y Combinator) — polish the paths users walk, defer the rest;
retrofit-cheap vs retrofit-catastrophic judgment.
https://www.ycombinator.com/library (search-verified 2026-07-17.)
[^7]: The Twelve-Factor App, "Config" and build/release discipline — versioned,
ordered changes; secrets in the environment. https://12factor.net/config
(search-verified 2026-07-17.)
[^8]: OWASP Agentic AI Top 10 (2026) — agent authorization compromise, tool
misuse; the threat model tenant-scoped RLS addresses. https://genai.owasp.org/
(search-verified 2026-07-17; two-source verification in
`_refresh-2026-07-master-report.md` theme 3).

_last_verified: 2026-07-17_
