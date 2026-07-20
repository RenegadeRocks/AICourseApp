# Code-lab 1 — Client dashboard backend + productized pricing model

Companion to **Week 19, Saturday**
([[../../06-sat-build-client-dashboard-and-productized-spec]]). Three things in
one small, dependency-light package:

1. **A tenant-scoped client dashboard backend** (`store.py`, `app.py`) — a
   client can log in and see only their own project. Cross-tenant reads fail
   closed.
2. **A grounded AI status-summary endpoint** (`summary.py`) — assembles facts
   deterministically, then phrases them; runs offline with no API key, and
   always returns a *draft* for operator approval.
3. **A productized-service pricing / capacity model** (`pricing.py`) — the
   Thursday capacity math, with verification hours as a required input.

## Run it (zero dependencies)

The core logic runs on the **Python 3.10+ standard library**. No install needed.

```bash
python test_dashboard.py     # 9 tests, all offline
python seed.py               # CLI demo: dashboards, isolation, summary, capacity
```

Expected: `9 tests passed`, and a demo that prints Acme's dashboard, proves
Globex cannot see Acme's data, prints a grounded offline status summary, and
prints the capacity model (12.5 human hours/client, 2 clients/period ceiling).

## Run the HTTP API (optional)

```bash
pip install -r requirements.txt
uvicorn app:app --reload
```

Then, simulating a logged-in client via a header (in production this is a
verified JWT claim, not a header):

```bash
curl -H "X-Client-Id: acme"   localhost:8000/me/dashboard
curl -H "X-Client-Id: acme"   localhost:8000/me/summary
curl -H "X-Client-Id: globex" localhost:8000/me/projects/p_acme   # -> 404, not a leak
curl "localhost:8000/ops/capacity?available_hours=25&target_revenue=60000"
```

## Run the online AI summary (optional)

```bash
export ANTHROPIC_API_KEY=sk-...        # never commit this
curl -H "X-Client-Id: acme" "localhost:8000/me/summary?use_llm=true"
```

Offline mode (the default) needs no key and is also the test oracle and the
production fallback. Model is set via `SUMMARY_MODEL` (default `claude-haiku-4-5`
— a cheap, fast tier is correct for bounded summarization, per the Tuesday
lesson).

## The pass bar (Saturday)

- **A client could log in and see their project.** `GET /me/dashboard` with a
  client id returns that client's four sections and nothing else. Proven by
  `test_tenant_isolation_no_cross_leak` and `test_internal_deliverable_hidden`.
- **The AI summary is grounded and gated.** It mentions only shipped
  (approved) deliverables, never internal drafts, and is returned as a `draft`.
  Proven by `test_summary_is_grounded_and_draft`.
- **The pricing model is honest.** It refuses an offer that claims AI delivery
  with zero verification hours. Proven by `test_capacity_rejects_zero_verification`.

## How this maps to a real production build (Supabase RLS)

This lab enforces tenant isolation in ONE application-layer choke point
(`store._require_same_tenant`) so it is testable with no database. In
production you push the same guarantee **into the database** with PostgreSQL
Row-Level Security, so a forgotten query filter fails closed (Tuesday lesson):

1. Add `client_id` to every table; **enable RLS** on every table exposed
   through the API.
2. Put the tenant in the JWT: on login set a `client_id` custom claim.
3. Policy: `USING (client_id = auth.jwt() ->> 'client_id')`.
4. **Index** `client_id` on every table (top RLS performance killer otherwise).
5. **Test from the client SDK**, not the SQL editor (the editor bypasses RLS).
6. **Never** ship the `service_role` key to the frontend (it bypasses RLS).

The `current_client_id` dependency in `app.py` is the stand-in for step 2's
verified JWT claim.

## Files

| File | Role |
|------|------|
| `store.py` | Tenant-scoped data store; single isolation choke point |
| `summary.py` | Grounded AI status summary (offline template + optional LLM) |
| `pricing.py` | Productized offer + capacity/margin model (verification required) |
| `seed.py` | Demo data + runnable CLI demo |
| `app.py` | FastAPI backend wiring the tenant-scoped endpoints |
| `test_dashboard.py` | 9 offline tests (plain `python` or `pytest`) |
| `requirements.txt` | Optional deps (API + online LLM only) |

_last_verified: 2026-07-17_
