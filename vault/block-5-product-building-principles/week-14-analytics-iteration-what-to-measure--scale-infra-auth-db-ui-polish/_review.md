---
type: review
phase: 2
week: week-14
reviewer: multi-persona 13-lens
date: 2026-07-17
---

# Week 14 — Phase 2 Multi-Persona Review (+ surgical polish applied)

Scale 1–10. Weights: Karpathy / Hamel / Simon = 1.0; the other ten personas = 0.8
(total 11.0). Reviewed cold against `quality-standard.md`,
`.claude/block-5-briefs/_generator-base.md` (anti-slop + canonical-home map +
amended verification protocol), and `week-14-briefs.md`.

Mechanical checks run this session (Bash):

- **code-lab/1:** `npm install --no-audit --no-fund` (127 pkgs, clean) →
  `npm run typecheck` (tsc strict, clean) → `npm run lint` (eslint, clean) →
  `npm test` (**RLS isolation test passes**).
- **RLS test is real, not theater.** Removed `set local role app_user` from
  `withTenant`, re-ran: the test **failed** (`tenant B leaked into tenant A data,
  1 !== 0`). So the wall is genuinely asserted — a superuser/owner connection
  leaks and the test catches it. Restored the line; test passes again. The
  generator's "the test failed the first time on the superuser-bypass footgun"
  claim is legitimate.
- **curl hostile-stranger walkthrough** (via `npm start`, after both fixes below):
  two strangers sign up, A creates+shares a report, **B's `/reports` returns
  `{"reports":[]}`** (isolation holds), `/metrics` without token → **403
  forbidden**, `/metrics` with token → **`{"weeklySharingAccounts":1,
  "reportsGenerated":1,"regenerationRate":0}`** — exactly the README's documented
  output.
- **In-lesson Python snippets** (Mon/Tue/Wed/Fri) executed: Mon prints north-star
  1, activation 0.5, regen 0.5 (matches pass bar); Tue prints four JSON lines
  sharing one `request_id` (matches); Fri cost model runs; **Wed contradicts its
  own prose — see 03-wed and Unresolved #1.**
- **All 14 distinct wikilink targets resolve** (script-checked against the vault).
  The two Week-12/13 links carried `(pending)` and pointed at folders; both
  upgraded (see fixes).
- **Anti-slop:** em-dash density 3.6–6.7/1k across all files (well under ~12);
  "load-bearing" 0–2/file; "operator" 0; "would push back" ≤1/file; contrast
  scaffolds ≤1/file. Clean throughout.
- **WebSearch verification** of the one named non-core-roster person + the
  load-bearing 2026 auth facts: **Bereket Engida / Better Auth** confirmed real —
  self-taught Ethiopian dev, **$5M seed led by Peak XV + YC** (TechCrunch
  2025-06-25), ~150k weekly npm downloads, YC spring batch; **Clerk free tier
  raised to 50k MRU on 2026-02-05** (from 10k) confirmed across clerk.com +
  saasprices.net. (Currency note: Vercel **acquired Better Auth ~2026-07-09**;
  the lesson predates/omits this but no claim is invalidated — see Unresolved #3.)
- **No re-teaching:** the lethal trifecta (04-thu, 06-sat) is one-line-recapped
  and wikilinked to b0w02, "we do not re-explain the mechanism"; Wilson (03-wed)
  wikilinks b2w03, "we will not re-derive it"; retrieval-at-scale (05-fri)
  wikilinks b3w06 for architecture, covers only the operational overlay; launch
  instrumentation defers to b4w10. Compliant.

---

## 00-overview

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | "Measure honestly, then harden" is the mechanism; day table maps to concrete leave-withs. |
| Chip Huyen | 8 | Steady-state vs launch-photograph framing is the right distinction. |
| Jerry Liu | 8 | Retrieval-at-scale correctly subordinated to b3w06. |
| Hamel Husain | 8 | Pass bar is behavioral (hand a stranger a URL, watch the dashboard). |
| Simon Willison | 8 | Controversies named, not hyped; no overclaims. |
| Seibel | 9 | Sells the week in two paragraphs; "the build was the easy part." |
| Boris Cherny | 8 | Points at the four hardening layers without teaching them. |
| Cohort peer | 8 | "die quietly in month three" is honest and motivating. |
| Mira Murati | 8 | Commercial framing restrained. |
| swyx | 8 | Build-vs-buy-auth controversy signals the week won't be naive. |
| Ethan Mollick | 8 | Retention-as-truth is the correct behavioral anchor. |
| Lilian Weng | 8 | Terminology consistent with the dailies. |
| Jeremy Howard | 8 | Links carry the cross-block load. |

**Weighted average: 8.1**

---

## 01-mon — Product analytics for AI products

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | Metric hierarchy (vanity/activation/retention/north-star) decomposed by "can it decrement," a real mechanism. |
| Chip Huyen | 9 | The six AI-specific metrics and quality-drift-as-first-class match her production framing; her own lens concedes drift is undersold as a tile. |
| Jerry Liu | 8 | North-star-per-account discipline is correctly upstream of Tuesday's taxonomy. |
| Hamel Husain | 9 | His lens ("read 50 transcripts, dashboards are procrastination") argues against the lesson and changes the emphasis. |
| Simon Willison | 8 | Deflection-vs-containment distinction is exactly the kind of relabeling he flags. |
| Seibel | 8 | "Six tiles you act on beats ninety you admire" is his instinct. |
| Boris Cherny | 8 | Metrics-definition-in-code (north_star.py) is the anti-drift move. |
| Cohort peer | 8 | Activation-sentence deliverable is directly doable. |
| Mira Murati | 8 | Trust-as-fragile is a genuine AI-product insight. |
| swyx | 8 | Containment benchmarks current and sourced. |
| Ethan Mollick | 9 | Time-to-trust / incremental-trust is his research, correctly applied. |
| Lilian Weng | 8 | Metric definitions internally consistent with Sunday's cards. |
| Jeremy Howard | 8 | b4w10 launch home recapped one line, not re-taught. |

**Weighted average: 8.3**

---

## 02-tue — Instrumentation & the analytics stack

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | Object-Action + typed events is the correct low-drift architecture. |
| Chip Huyen | 8 | Two-pipes-one-id is the join that makes cost/quality debuggable. |
| Jerry Liu | 8 | LLM-observability decision (Langfuse/Braintrust/OTel) is current and evidence-based. |
| Hamel Husain | 9 | "Read twenty traces before buying" is his lens, and the Postgres-log-first path honors it. |
| Simon Willison | 9 | His PII-in-the-observability-store footgun is named and wired into the wrapper (prompt hashed). |
| Seibel | 8 | "Start on PostHog, don't run two taxonomies" resists tool sprawl. |
| Boris Cherny | 8 | Contract-test-the-emitted-shape critique points forward to Saturday's typed emit(). |
| Cohort peer | 8 | dual_pipe.py runs and demonstrates the join concretely. |
| Mira Murati | 7 | Little on how observability shifts across model generations. |
| swyx | 8 | OTel GenAI conventions correctly flagged as the portability hedge. |
| Ethan Mollick | 8 | Session-replay ethics framed as a design choice, not a tool default. |
| Lilian Weng | 8 | Pricing figures consistent with citations. |
| Jeremy Howard | 8 | b3w08 reliability home linked for the tracing mindset, not re-taught. |

**Weighted average: 8.3**

Notes: EU AI Act 2 Aug 2026 date and the deployer-vs-provider hedge are correctly
scoped ("do not overclaim what applies to you").

---

## 03-wed — The iteration loop

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 7 | Small-N loop reasoning is sound, but the worked example's climax is contradicted by its own code (Wilson intervals overlap, ship=False — see Unresolved #1). |
| Chip Huyen | 8 | Prompt-change-as-product-experiment with an eval gate is the right AI-specific move. |
| Jerry Liu | 8 | Funnel/cohort/transcript/Wilson quartet is a coherent small-scale toolkit. |
| Hamel Husain | 9 | Transcripts-over-dashboards is his central point, correctly load-bearing. |
| Simon Willison | 8 | A/B-is-theater-at-40-users is honestly argued with Kohavi/peeking sourcing. |
| Seibel | 8 | "Stop measuring, go talk to users" is in the lens and partly conceded. |
| Boris Cherny | 7 | decide.py is a good guard, but a guard whose worked example prints the opposite of the prose undercuts the "executable claim" ideal. |
| Cohort peer | 8 | Hypothesis template with "we're wrong if" is directly usable. |
| Mira Murati | 8 | Local-maxima / painted-door treatment is a real strategic frame. |
| swyx | 8 | Model-swap-as-experiment is 2026-native. |
| Ethan Mollick | 8 | The turn-a-week cadence is good behavior design. |
| Lilian Weng | 7 | The 38%-vs-25% "do not overlap" claim is numerically false at the stated n — a consistency defect. |
| Jeremy Howard | 8 | Anti-statistical-theater lens is his, correctly placed. |

**Weighted average: 7.7**

Notes: the lesson's decision procedure ("ship only if Wilson intervals don't
overlap") is correct; the *demonstration* of it is wrong. See Unresolved #1 —
flagged, not auto-fixed, because the resolution (bigger n vs a "hold, not enough
data" conclusion) is a pedagogical choice for the author.

---

## 04-thu — Auth & security for real users

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | Authn/authz split framed as the mechanism under most breaches. |
| Chip Huyen | 8 | Build-vs-buy decided on real 2026 numbers, not vibes. |
| Jerry Liu | 8 | RLS-as-the-boundary (app filtering is "a countdown") is the correct hierarchy. |
| Hamel Husain | 8 | The AI-boundary section defends, doesn't re-teach, the trifecta. |
| Simon Willison | 9 | His "no reliable general defense, constrain capability" posture is the lens and the load-bearing rule. |
| Seibel | 8 | Cohort-peer "why RLS at four users" is raised and answered (retrofit-catastrophic). |
| Boris Cherny | 9 | "The RLS policy that exists in a migration but was never tested" points straight at Saturday's test. |
| Cohort peer | 8 | Reflection Qs map to real product decisions. |
| Mira Murati | 8 | SOC2-as-sales-enablement is the correct commercial read. |
| swyx | 8 | Better Auth insurgent framing is current and verified. |
| Ethan Mollick | 8 | Decision tree is teachable. |
| Lilian Weng | 8 | Provider numbers consistent with Sunday's card. |
| Jeremy Howard | 8 | b0w02/b3w08/b4w09 homes linked, not re-taught. |

**Weighted average: 8.4**

Notes: Better Auth facts (YC, $5M seed, npm/stars) WebSearch-verified. Clerk Pro
is "~$25/mo" here; clerk.com's current page snippet says "from $20/mo" — within
the lesson's own hedge, minor.

---

## 05-fri — Data & scale

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | "One Postgres, feel a little bored" is the correct default with a real mechanism (one thing to secure/back up). |
| Chip Huyen | 9 | Cost-curve-as-the-one-never-premature concern is her framing; cost_curve.py makes it runnable. |
| Jerry Liu | 8 | pgvector-until-measured-pain keeps retrieval in b3w06. |
| Hamel Husain | 8 | Thresholds table is evidence-gated, not anticipatory. |
| Simon Willison | 8 | Managed-Postgres claims sourced across two domains each. |
| Seibel | 9 | "Use Postgres, model costs, ignore the rest" — the table is the pre-PMF founder's whole need. |
| Boris Cherny | 8 | Expand/contract + backfill-separately is the outage-avoiding discipline. |
| Cohort peer | 8 | "Isn't RLS over-building at four users" answered via the cheap-now/expensive-later quadrant. |
| Mira Murati | 7 | Model-curve cost strategy stays surface. |
| swyx | 8 | Neon-vs-Supabase current; scale-to-zero/branching correct. |
| Ethan Mollick | 8 | Honest-thresholds framing is good judgment training. |
| Lilian Weng | 8 | pooling/tokenizer/cache figures consistent with Monday. |
| Jeremy Howard | 8 | Premature-scaling thread reinforced, not repeated. |

**Weighted average: 8.2**

Notes: cost_curve.py's pass bar ("watch the margin jump" 0.30→0.05) is real but
undersells: defaults yield 88% margin and the sub-70% WARN branch never fires with
the shipped inputs. Cosmetic; not fixed.

---

## 06-sat — BUILD: harden the product

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | Four-layers-one-pass-bar is the right decomposition; PGlite gives real Postgres RLS locally. |
| Chip Huyen | 8 | Observability-humble (one redacted JSON line) before Langfuse is honest. |
| Jerry Liu | 8 | Metric-computed-from-events (not a mutable counter) is the recompute-history discipline. |
| Hamel Husain | 8 | Redact-at-the-boundary is wired, not just asserted. |
| Simon Willison | 9 | The AI runs as `app_user`, no capability the human lacks — his architectural defense, made executable. |
| Seibel | 8 | "Polish the paths users walk, then ship" with a stopping rule. |
| Boris Cherny | 9 | The isolation test that *failed first* is his whole thesis; verified real this session. |
| Cohort peer | 8 | Runnable top-to-bottom; the footgun is taught by the code hitting it. |
| Mira Murati | 7 | AI-feature grafting is described, not built here (deferred, fair). |
| swyx | 8 | PGlite→Neon/Supabase mapping is the correct portability seam. |
| Ethan Mollick | 8 | UI-polish checklist is behaviorally concrete. |
| Lilian Weng | 8 | Superuser-bypass explanation matches Sunday's A10 exactly. |
| Jeremy Howard | 8 | Design-system-literacy deferred to Block 2, not re-taught. |

**Weighted average: 8.4**

Notes: two code-lab defects found and **fixed** this session (README `sed`
id-extraction; `.env` never loaded) — see Surgical Fixes. Superuser-bypass claim
independently reproduced.

---

## 07-sun — Synthesis + quiz + flashcards

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | Quiz rewards reasoning (A10 RLS mechanism, A12 cost levers), not recall. |
| Chip Huyen | 8 | "Measurement is continuous, not a phase" correctly elevated. |
| Jerry Liu | 8 | Synthesis keeps retrieval/vectors subordinate to measured pain. |
| Hamel Husain | 8 | "Watch a human use your product" is the honest closing assignment. |
| Simon Willison | 8 | A9/A10 compress the RLS/trifecta evidence correctly. |
| Seibel | 8 | "The chart tells you where, the human tells you what" is the right last word. |
| Boris Cherny | 8 | A10's two-part fix matches Saturday's code exactly. |
| Cohort peer | 8 | 12 Qs well-calibrated; scoring guidance actionable. |
| Mira Murati | 7 | Forward pointers mostly operational. |
| swyx | 8 | Provider shortlist current. |
| Ethan Mollick | 8 | Converts the week into a scheduled next action. |
| Lilian Weng | 8 | All 30 flashcards trace to weekday lessons; no contradictions found. |
| Jeremy Howard | 8 | No duplicate territory with prior quizzes. |

**Weighted average: 8.1**

Consistency audit (Sunday vs weekdays vs code-lab): tokenizer ~30%; deflection
41/59/70–85; Clerk 50k / Supabase 50k MAU $25 / Better Auth ~28–30k stars, 150k
npm; Neon ~$0.106 CU-hr, $0.35/GB, $19/mo vs Supabase $25/mo; north star = weekly
sharing accounts + regeneration counter — all consistent across the three
surfaces. Quiz (12Q + key) and flashcards (30) trace to weekday content. The one
consistency defect is the Wed worked example (Unresolved #1); Sunday's Wilson
flashcard/A8 state the *rule* correctly, so the rot did not spread.

---

## code-lab/1 (harden-the-product: TS/Hono/PGlite backend + RLS test)

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | Small, readable, deterministic; migrations idempotent; the RLS wall is the architecture. |
| Chip Huyen | 8 | Events carry account_id+user_id+request_id so the two pipes join; metric computed from the log. |
| Jerry Liu | 8 | File roles map 1:1 to the four layers. |
| Hamel Husain | 8 | redact() at the logging boundary; scrypt + timing-safe compare done correctly. |
| Simon Willison | 9 | Session token stored as SHA-256 digest; user-enumeration closed via dummy-hash verify; AI runs as app_user. |
| Seibel | 8 | Runs entirely locally, no cloud account — right for a teaching build. |
| Boris Cherny | 9 | isolation.test.ts is a genuine CI-grade proof (fails when the role switch is removed — verified). |
| Cohort peer | 8 | typecheck/lint/test all clean; walkthrough reproduces after fixes. |
| Mira Murati | 7 | No AI-feature path built (deferred to the reader). |
| swyx | 8 | Hono/PGlite versions pinned; maps to managed Postgres cleanly. |
| Ethan Mollick | 8 | Pass bar is a concrete hostile-stranger script. |
| Lilian Weng | 8 | Typed EVENTS tuple prevents string-drift. |
| Jeremy Howard | 8 | `set_config(...is_local)` + `SET LOCAL ROLE` is the pooler-safe, correct pattern. |

**Weighted average: 8.2**

Notes: two defects (both **fixed**) would each have leaked past a superficial
read because `npm test`/typecheck/lint all pass regardless of them — they only
surface in the documented curl walkthrough.

---

## Overall Week 14: **8.2 / 10**

(File averages: 8.1, 8.3, 8.3, 7.7, 8.4, 8.2, 8.4, 8.1, 8.2.) Strongest:
Thursday and Saturday — the RLS/AI-boundary through-line is the spine of the week
and the isolation test is a genuinely executable security claim (verified by
breaking it). Anti-slop is excellent across the board. The one real blemish is
Wednesday's worked example printing the opposite of its prose.

---

## Surgical fixes applied this session

1. **code-lab/1/package.json** — `dev` and `start` scripts did not load `.env`,
   yet the README instructs `cp .env.example .env` and sets `METRICS_TOKEN`
   there. Result: following the README exactly, `process.env.METRICS_TOKEN` is
   `undefined`, so `/metrics` returns **403 even with the correct bearer token**,
   and the README's own documented output is unreachable. Fixed by adding
   `--env-file-if-exists=.env` to both scripts (verified: `.env` now loads under
   `npm start`; still boots with no `.env` for CI/`npm test`). Reproduced the
   `{"weeklySharingAccounts":1,...}` output after the fix.
2. **code-lab/1/README.md** — the hostile-stranger walkthrough extracted the
   report id with `sed 's/[^0-9a-f-]//g'`, which keeps the `d` from `"id"` and
   yields a malformed UUID (`d7b2198d9-...`), so `POST /reports/$RID/share`
   returned **Internal Server Error**. Changed to
   `sed -E 's/.*"id":"([^"]+)".*/\1/'`. Verified: share now returns
   `{"shared":true}`.
3. **06-sat** — the two Block-5 capstone links to Weeks 12 and 13 were marked
   `(pending)` and pointed at folder roots. Both weeks now exist; upgraded to
   `[[.../week-12-.../06-sat-build-ship-the-product-skeleton|Week 12]]` and
   `[[.../week-13-.../06-sat-build-add-one-magical-feature|Week 13]]` and dropped
   the "pending" marker.

All code-lab checks re-run clean after edits (typecheck, lint, test pass; full
curl walkthrough behaves as documented).

## Unresolved concerns (recommendations, not applied)

1. **03-wed worked example contradicts its own code (highest priority).** The
   prose asserts "Wilson intervals on 38% (n≈120) and 25% (n≈110) do not overlap.
   Decision: keep, and roll to all users," but the lesson's `should_ship(28, 110,
   46, 120)` returns `overlap: True, ship: False` — CIs are (0.182, 0.343) and
   (0.301, 0.473), which overlap. There is therefore **no ship:True demonstration
   anywhere in the lesson**, and the pass bar implies the default case ships. Not
   auto-fixed because two valid resolutions exist: (a) raise the cohort sizes so
   25%↔38% genuinely separates (~n≥200 each) and update the "n≈110/120" prose, or
   (b) rewrite the conclusion to the honest small-N outcome ("promising but the
   intervals still overlap — hold and gather another cohort"), which would sharpen
   the lesson's own thesis. Author's call.
2. **Word counts run ~2,900–3,600/daily** vs the L3 4,500–6,500 soft target (the
   `word_count_target` frontmatter says 5,200–5,400). Density is high and the
   brief says density over length, and the lessons satisfy `quality-standard.md`'s
   older 2,000–4,000 band — but they are meaningfully under the block-5 generator
   floor. Tue and Fri could each absorb ~400 words on the gaps their own lenses
   name (observability across model generations; model-curve pricing).
3. **Currency: Better Auth was acquired by Vercel ~2026-07-09** (WebSearch), days
   before the `last_verified: 2026-07-17` stamp. 04-thu treats it as the
   independent open-source insurgent "recommended by Next.js." No claim is false
   (it remains open-source and Next.js-recommended — arguably more so under
   Vercel), but a one-clause acknowledgment would keep the liveness pass honest.
4. **Clerk Pro price**: 04-thu says "~$25/mo"; clerk.com's current page reads
   "from $20/mo." Within the lesson's hedge, but Phase 4 should confirm against
   the live pricing page.

## Phase 4 citation-verify list (liveness pass — WebFetch was egress-blocked)

1. Thu [^1]/[^2]: Clerk 50k-MRU free tier + Pro price against the live clerk.com
   pricing page.
2. Thu [^4]: Better Auth stars/downloads + note the Vercel acquisition against
   better-auth.com / TechCrunch.
3. Mon [^8]/[^9]: deflection 41/59/70–85 and 90%-deflection-40%-resolution against
   the Digital Applied and Nextiva posts.
4. Tue [^3]/[^7]: PostHog/Amplitude and Langfuse/Braintrust pricing against the
   vendors' live pages.
5. Fri [^3]: Neon $0.106/CU-hr, $0.35/GB, $19/mo against the live Neon pricing.
6. Tue [^9]: EU AI Act 2 Aug 2026 GPAI transparency date against the official
   timeline.

---

_Review + surgical polish produced 2026-07-17. Files edited: 06-sat-harden-the-product.md,
code-lab/1/package.json, code-lab/1/README.md. No git commits made._
