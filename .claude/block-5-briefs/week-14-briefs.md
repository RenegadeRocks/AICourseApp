# Week 14 briefs — Analytics & Iteration (What to Measure) + Scale Infra (Auth, DB, UI Polish)

Curriculum sessions: "Analytics & Iteration - what to measure" + "Scale Infra
(Auth, DB, UI polish)". July-2026 interpretation: the product exists (W12) with
magic features (W13); now measure it honestly, iterate, and harden the infra
from prototype to production. Block 4 taught launch instrumentation (wikilink);
this is ongoing product analytics + the scale/auth/DB/polish work that turns an
MVP into something that survives real users. Closes Block 5.

Day plan:

- **01-mon — Product analytics for AI products: what to measure.** Beyond
  vanity: activation, retention (the real health metric), the AI-specific
  metrics (feature-trust, regeneration rate, fallback rate, containment,
  cost-per-active-user, quality-drift), north-star selection. b4w10 launch
  instrumentation is the launch-day canonical — wikilink; this is steady-state.
  Reviewer: Chip Huyen, Mollick, Hamel.
- **02-tue — Instrumentation & the analytics stack.** Event taxonomy design,
  the 2026 analytics stack (verify: PostHog/Amplitude/etc. current state +
  pricing), session replay ethics/consent, LLM-observability (traces, token/
  cost/latency, eval-in-prod — verify current tools like Langfuse/Braintrust),
  wiring product + AI observability together. Privacy-by-design.
- **03-wed — The iteration loop.** Turning metrics into changes: hypothesis →
  experiment → measure → decide, A/B testing at small scale (Wilson-interval
  discipline — b2w03 canonical wikilink, don't re-derive), when you have too
  few users to A/B (qualitative + funnel + cohort), prompt/model iteration as
  product iteration, avoiding local maxima. Ties to Block 4 validation loop.
- **04-thu — Auth & security for real users.** Auth in 2026 (verify:
  Clerk/Auth.js/Supabase Auth/WorkOS current state + pricing), sessions,
  RBAC, multi-tenancy security, secrets management, the security posture for
  AI products specifically (prompt injection reaching user data — b0w02/b3w08
  canonical wikilink, don't re-teach the attack), PII handling, SOC2-readiness
  basics for selling upmarket (b4w09 wikilink).
- **05-fri — Data & scale.** Database choices at scale (Postgres-first;
  verify current managed-Postgres landscape/pricing), migrations, connection
  pooling, caching layers, vector-store-at-scale (b3w06 retrieval wikilink),
  the cost curve of AI features under load, when to actually worry about scale
  (premature-scaling as the real risk). Honest thresholds.
- **06-sat — BUILD: harden the product.** Take the W12/W13 product to
  production-ready: add real auth, migrate to a proper DB schema, add
  observability + one live product metric, and a UI-polish pass. code-lab:
  auth + schema/migrations + an observability hook + a metrics endpoint,
  lint/type-checked. Pass bar: the product survives a hostile stranger and you
  can see what they did. Also: Block 5 capstone recap (W12 skeleton → W13
  magic → W14 hardened product).
- **07-sun — Synthesis + quiz + flashcards.**

Controversies (verify current): premature scaling vs "build for scale from
day 1"; which auth provider (build vs buy); session replay ethics; how much
observability an indie product actually needs.
