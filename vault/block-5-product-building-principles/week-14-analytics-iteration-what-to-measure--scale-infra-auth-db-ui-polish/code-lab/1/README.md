# Harden the product — Week 14 Saturday build

Take the Week 12/13 prototype to production-ready. This lab is a self-contained
TypeScript backend that adds the four things a demo is missing:

1. **Real auth** — password hashing (scrypt), opaque server-side sessions, httpOnly
   cookies. No hand-rolled crypto; no tokens in `localStorage`.
2. **A proper DB schema with migrations** — ordered, versioned SQL files, applied
   by a runner, never hand-edited.
3. **DB-enforced tenant isolation (RLS)** — the wall an app bug or a prompt
   injection cannot walk around. Enforced in Postgres, not in `WHERE` clauses.
4. **Observability + one live product metric** — a structured, redacted log line
   per request, and a bearer-protected `/metrics` endpoint serving the north star.

It runs entirely locally. The database is **PGlite** (real Postgres compiled to
WASM, in-process), so there is no server to install and no cloud account needed.
Everything you learn maps 1:1 to managed Postgres (Neon/Supabase) in production.

## Requirements

- Node.js **>= 20.11** (for the built-in test runner and top-level await).
- Dependencies are pinned in `package.json`.

## Setup

```bash
npm install
cp .env.example .env      # then edit METRICS_TOKEN to a long random string
```

## Run

```bash
npm run dev        # starts the API on http://localhost:3000 (tsx watch)
npm run typecheck  # tsc --noEmit, strict
npm run lint       # eslint
npm test           # the RLS isolation test — the pass bar below
```

## Pass bar

**The product survives a hostile stranger, and you can see what they did.**
Concretely, all of the following must hold:

1. `npm test` passes: the RLS test proves tenant B (and any unknown tenant)
   cannot read tenant A's rows. Note the sharp edge the test encodes: request-time
   access runs as a **non-superuser role** (`app_user`), because a superuser
   connection bypasses RLS entirely — the #1 way RLS silently fails open in
   production.
2. `npm run typecheck` and `npm run lint` are clean.
3. The manual hostile-stranger walkthrough below behaves as described.

## Hostile-stranger walkthrough

Two strangers sign up. Neither can see the other's data, and neither can scrape
your metrics.

```bash
# Stranger A signs up and creates + shares a report.
curl -sc a.txt -X POST localhost:3000/auth/signup \
  -H 'content-type: application/json' \
  -d '{"email":"a@example.com","password":"password-a1"}'
RID=$(curl -sb a.txt -X POST localhost:3000/reports \
  -H 'content-type: application/json' -d '{"title":"A secret"}' | \
  sed -E 's/.*"id":"([^"]+)".*/\1/')
curl -sb a.txt -X POST "localhost:3000/reports/$RID/share"

# Stranger B signs up and lists reports — sees ONLY their own (empty).
curl -sc b.txt -X POST localhost:3000/auth/signup \
  -H 'content-type: application/json' \
  -d '{"email":"b@example.com","password":"password-b1"}'
curl -sb b.txt localhost:3000/reports      # => {"reports":[]}

# Hostile stranger tries to scrape metrics without the token — forbidden.
curl -s localhost:3000/metrics             # => {"error":"forbidden"} (403)

# You, the operator, read the live north star WITH the token.
curl -s localhost:3000/metrics -H "authorization: Bearer $METRICS_TOKEN"
# => {"weeklySharingAccounts":1,"regenerationRate":0,"reportsGenerated":1}
```

If B's `/reports` ever shows A's report, the wall leaked and the build fails.

## What maps to production

- **PGlite → Neon or Supabase Postgres.** Same SQL, same RLS. Swap the connection;
  the migrations and policies are unchanged (Friday).
- **In-app sessions → the same, or a managed provider** (Clerk / Better Auth /
  Supabase Auth) if you'd rather buy it. Keep user-id references provider-agnostic
  so the swap stays a weekend, not a rewrite (Thursday).
- **`console.log` structured logs → your sink** (and pair with an LLM-observability
  tool once you add the AI feature; join on `request_id`) (Tuesday).
- **`set_config(..., is_local => true)` per transaction** is the pooler-safe
  pattern: the tenant setting cannot leak onto the next request that reuses the
  connection (Friday, connection pooling).

## Files

| File | Role |
|---|---|
| `migrations/001_init.sql` | accounts, users, sessions, event log |
| `migrations/002_reports_rls.sql` | the tenant-owned table + RLS policy (the wall) |
| `src/db.ts` | open DB, run migrations, `withTenant` (activates RLS) |
| `src/auth.ts` | scrypt hashing, opaque sessions |
| `src/events.ts` | typed event taxonomy + `emit` |
| `src/metrics.ts` | the north-star computation |
| `src/observability.ts` | redacted structured logging |
| `src/server.ts` | the Hono API wiring it all together |
| `test/isolation.test.ts` | the executable proof the wall holds |

## Note on liveness

Dependency versions are pinned but were verified by search, not by a live
`npm install` in this authoring environment (egress-restricted). If a pinned
version has moved, `npm install` will report it; bump within the same minor and
re-run `npm run typecheck`.
