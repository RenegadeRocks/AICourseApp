---
type: lesson
block: block-5-product-building-principles
week: week-14
session_slug: analytics-iteration-what-to-measure
day_of_cycle: 7
day_name: sun
date_due: 2026-08-23
tags:
  - synthesis
  - quiz
  - flashcards
  - capstone
  - block-5-recap
sources:
  - reforge-north-star-metrics-2024
  - chip-huyen-ai-engineering-2025
  - kohavi-trustworthy-experiments-2020
  - simonwillison-lethal-trifecta-2025
  - startup-genome-premature-scaling-2011
  - clerk-pricing-2026
  - neon-supabase-pricing-2026
last_verified: 2026-07-17
word_count_target: 3600
---

# Synthesis, quiz & flashcards: what to measure, and how to survive real users

## The week in one arc

Two jobs, one week. **Measure honestly, then harden.** The first half taught you
to count the things that predict whether you have a business (retention, the six
AI-specific metrics, a north star with a counter-metric) and to turn those counts
into product changes through a loop that works at forty users, not forty thousand.
The second half taught you to make the product survive strangers: auth you
understand, a versioned schema, tenant isolation enforced in the database, and
observability you can read, capped by a UI-polish pass and a live metric you can
watch.

If you internalize one sentence from each day:

- **[[01-mon-product-analytics-for-ai-products|Mon]]:** A metric you will not act
  on is a distraction; retention's plateau, not its intercept, is the truth, and
  AI products need six extra numbers because a model can run perfectly and still
  lose trust.
- **[[02-tue-instrumentation-and-the-analytics-stack|Tue]]:** Two pipes joined by
  one `request_id` (product analytics + LLM traces), an Object-Action event
  taxonomy defined in code, and session replay masked at the client by default.
- **[[03-wed-the-iteration-loop|Wed]]:** Below a few thousand users, A/B testing
  is theater; run funnel + cohort + transcripts + Wilson-guarded comparisons, and
  treat prompt changes as product experiments gated by an eval set.
- **[[04-thu-auth-and-security-for-real-users|Thu]]:** Authentication is *who*,
  authorization is *what*, the second one leaks; isolate tenants in the database
  (RLS), and the AI must never hold a capability the user lacks.
- **[[05-fri-data-and-scale|Fri]]:** One Postgres until it hurts; the concerns
  worth doing early (pooling, cost modeling, migrations, isolation) are the ones
  expensive to retrofit; everything else is premature scaling.
- **[[06-sat-harden-the-product|Sat]]:** The wall you can't see is off. Access
  data as a non-superuser role, *test* the isolation, and your AI feature becomes
  safe by construction.

## Block 5, closed

Three weeks, one machine: **skeleton (W12) → magic (W13) → hardened product
(W14)**. You can now build elite agents (Blocks 2–3), package and validate them
(Block 4), and assemble them into software people log into and pay for (Block 5).
The remaining blocks build on the assumption that you have shipped a real product
at least once. You have.

## The through-lines to carry forward

- **Premature scaling is the recurring villain.** It killed 70% of the failed
  startups Startup Genome studied,[^5] and it wears many costumes this week: a
  ninety-tile dashboard, an A/B test at forty users, Kubernetes on day one, a
  vector database you do not need. The antidote is the same each time: do the
  cheap-now-expensive-later things (isolation, pooling, cost, migrations), defer
  the rest until a measured pain forces it.
- **The AI layer changes the economics and the threat model.** Cost-per-active-
  user is not near zero,[^2] and your attack surface includes the text the model
  reads.[^4] Both are load-bearing differences from ordinary SaaS.
- **Test your invariants.** The isolation test failing first is the model for
  everything: a security or quality claim a machine does not check is one you will
  eventually break by accident.

---

## Quiz (12 questions)

Take it cold, without re-reading. Answer key follows.

**Q1 (MCQ).** Which of these is a *vanity* metric?
a) Weekly accounts that shared a report
b) Cumulative total signups
c) Regeneration rate
d) 7-day rolling retention

**Q2 (short answer).** A product is used by most customers about once a month. Why
is grading it on day-7 retention "malpractice with a chart," and which retention
flavor fits better?

**Q3 (MCQ).** Your support bot ends 90% of sessions without escalating to a human,
but users report it rarely solves their problem. Which pair of metrics best
exposes this?
a) Deflection rate and total sessions
b) Containment/deflection paired with a resolution or CSAT signal
c) Activation rate and signups
d) Regeneration rate and latency

**Q4 (short answer).** Name the six AI-specific metrics from Monday and, for each,
the one-line reason it predicts churn that a standard SaaS metric would miss.

**Q5 (MCQ).** In an Object-Action event taxonomy, which event name is correct?
a) `clicked_share_button`
b) `Report Generated With Sonnet`
c) `Report Shared`
d) `userSharedReport_v2`

**Q6 (short answer).** Session replay can capture what users type. Under GDPR,
what single configuration choice most changes your legal basis, and why does
client-side masking give you a stronger position than "collect then delete"?

**Q7 (MCQ).** You have 40 active users and want to test a new onboarding flow.
What is the *worst* choice?
a) Read ten session replays of drop-offs
b) Run a two-variant A/B test and stop it when it looks significant
c) Compare pre/post cohorts with Wilson intervals
d) Map the funnel and find the leakiest step

**Q8 (short answer).** Why is comparing two raw conversion percentages (e.g. 25%
vs 38%) at small sample sizes unsafe, and what is the ship rule using Wilson
intervals?

**Q9 (MCQ).** Your AI feature queries the database. Which credential choice makes
a prompt injection catastrophic across all tenants?
a) The current user's tenant-scoped, non-superuser access
b) A service-role/superuser connection that bypasses RLS
c) A read-only replica scoped to the tenant
d) The same `app_user` role the human uses

**Q10 (short answer).** You wrote an RLS policy and it "still leaks." A superuser
connection is the usual cause. Explain the mechanism and the two-part fix.

**Q11 (MCQ).** For a product with the low millions of vectors, the right default
vector store is:
a) A dedicated vector database, always
b) `pgvector` in the Postgres you already run
c) A self-hosted search cluster
d) In-memory only

**Q12 (short answer).** Your AI product charges $20/user/month. Cost-per-active-
user is climbing. Name three levers that reduce it, and say which Monday metric
tells you when a cheaper model is safe.

---

## Answer key

**A1.** (b) Cumulative total signups. It can only go up, so it can never warn you.
A healthy metric can decrement.

**A2.** A monthly-cadence product's users are not *supposed* to return on day 7,
so day-7 retention manufactures a crisis that is not real. Use unbounded/bracket
or rolling retention matched to the monthly frequency, and read the curve's
plateau, not any single point.[^1]

**A3.** (b). Deflection/containment alone can hit 90% while true resolution sits
near 40%; pairing with a resolution or CSAT signal exposes the gap. Deflection
without satisfaction is abandonment relabeled.

**A4.** Feature-trust rate (accept-and-act vs dismiss/edit — a model can run
perfectly and still be distrusted); regeneration rate (users gambling for a
better roll signals quality failure *and* multiplies cost); fallback/containment
rate (whether the AI resolved without a human, which standard error metrics miss
because the AI "succeeded" while being wrong); quality-drift (the provider or the
world changes under you, so a launch-passing eval fails in month three);[^2]
cost-per-active-user (marginal cost is not near zero, so margin can invert);
time-to-trust (users who never stop verifying churn because the AI adds work).

**A5.** (c) `Report Shared`. Object-Action, past tense, details go in properties,
not the name.

**A6.** Whether you mask text inputs by default. Masked-structural-only replay can
argue legitimate interest (GDPR Art. 6(1)(f)); capturing typed text needs
explicit opt-in consent (Art. 6(1)(a)). Client-side masking means the PII never
leaves the browser, so you can truthfully say it was never collected — a stronger
position than collecting and later deleting it.

**A7.** (b). At 40 users an A/B test is badly underpowered, and stopping when it
"looks significant" (peeking) inflates the false-positive rate past 30%. The other
three are the correct small-N instruments.[^3]

**A8.** Small samples make raw percentages noisy; 25% and 38% may be two
overlapping confidence intervals, i.e. indistinguishable. Put a Wilson interval on
each and only ship when the variant is both better *and* its interval does not
overlap the control's.

**A9.** (b). A service-role/superuser connection bypasses RLS, so one injection
reads every tenant. The AI must act as the tenant-scoped, non-superuser role the
human uses.

**A10.** Superusers (and BYPASSRLS roles) ignore RLS entirely, even with FORCE, so
if the app connects as the DB owner the policy never applies. Fix: (1) create a
non-superuser role and grant it only the needed table privileges; (2) switch to
that role per request (`SET LOCAL ROLE`) before scoping the tenant. Then test it.

**A11.** (b) `pgvector`. Keeping vectors in the same Postgres means one system to
secure and back up, and you can filter by `tenant_id` and vector-search in one
query. Graduate to a dedicated store on measured pain, not anticipation.

**A12.** Levers: cut regeneration rate (Wednesday's prompt-iteration loop);
route cheaper models per feature; cache stable prompt prefixes (provider prompt
caching) and cache deterministic outputs/embeddings; cap output length. The
metrics that say a cheaper model is safe: feature-trust rate and regeneration rate
holding steady (plus the eval-set score).

**Scoring:** 10+/12 you are fluent; walk into the live session ready to argue.
Below 8, re-read the day covering your weakest question before Monday.

---

## Flashcards (30)

Q: What makes a metric "vanity"?
A: It can only increase (cumulative), so it can never warn you. Healthy metrics can decrement.

Q: Retention: intercept or plateau?
A: The plateau. A curve that flattens (even at 15%) has product/market fit; one that decays to zero does not, whatever day-1 was.

Q: The three retention flavors?
A: N-day (exactly day N), unbounded/bracket (returned in a window), rolling (day N or later). Match to the product's natural frequency.

Q: Reforge's three-step activation model?
A: Setup → Aha (first value) → Habit (behavior that predicts retention).

Q: Why does a north star need a counter-metric?
A: Without one you eventually optimize against yourself (e.g. "messages sent" rewards a confusing UI). The counter-metric catches the cheat.

Q: Feature-trust rate?
A: Share of AI outputs the user accepts and acts on vs dismisses/edits/ignores. A perfect-running feature can still be distrusted.

Q: Regeneration rate, and why it hurts twice?
A: Frequency of "try again" on one request. High = quality/trust problem AND multiplied token cost.

Q: Containment vs deflection?
A: Containment = ticket did not escalate (subset). Deflection = ended without a human (superset, includes give-ups). Pair either with resolution/CSAT.

Q: Quality-drift, and why it's the "fires while you sleep" metric?
A: Model output degrades as the world and the provider's model change. Continuous in-prod eval catches it before a churn spike does.

Q: Why is cost-per-active-user different for AI products?
A: Marginal cost is not near zero; tokens scale with usage. It sets your pricing floor.

Q: The 2026 tokenizer gotcha?
A: The current-generation Anthropic tokenizer emits ~30% more tokens for the same text, so old cost estimates understate the bill by ~a third.

Q: Object-Action event naming?
A: `Object Action`, past tense (`Report Shared`). Details go in properties, never the event name.

Q: The two analytics pipes and what joins them?
A: Product analytics (what happened) + LLM observability (what the model saw/cost). Joined by one shared `request_id`.

Q: Session replay: the one config that changes your GDPR basis?
A: Masking text inputs by default. Masked → legitimate interest; capturing typed text → explicit consent required.

Q: Langfuse vs Braintrust in one line each?
A: Langfuse = open-source, self-hostable, OTel-native, unit-priced. Braintrust = proprietary, eval-loop-centric, GB+scores priced.

Q: When is A/B testing the wrong tool?
A: Below a few thousand active users. It's underpowered; use funnel + cohort + transcripts + Wilson-guarded comparisons.

Q: The peeking problem?
A: Repeatedly checking a test and stopping when significant inflates false positives past 30%. Pre-commit a window or use sequential methods.

Q: Ship rule with Wilson intervals?
A: Ship only if the variant is better AND its interval does not overlap the control's. Overlap = you learned nothing.

Q: Why is a prompt change a product experiment?
A: It has the blast radius of a UI redesign and can silently break unseen cases. Gate it with a golden eval set.

Q: Local maximum, and two defenses?
A: All-incremental tweaks trap you on a small hill. Defend with painted-door tests for big swings and a reserved budget for non-incremental bets.

Q: Authentication vs authorization?
A: Authn = who are you (once). Authz = what may you touch (every request). Broken authz is the #1 real breach.

Q: The three tenant-isolation models?
A: Row-level (`tenant_id` column, cheapest), schema-per-tenant, database-per-tenant. Default to row-level enforced in the DB.

Q: App-layer tenant filtering is a ___, not a ___.
A: A performance optimization, not a security boundary. The boundary is RLS (DB-enforced).

Q: Why did the code-lab's RLS "leak" at first?
A: The default connection was a superuser, which bypasses RLS even with FORCE. Fix: access data as a non-superuser role and test it.

Q: Why store the session token's hash, not the token?
A: So a database dump is not a pile of live logins — same reasoning as hashing passwords.

Q: The lethal trifecta, and the AI-safety rule it implies?
A: Private data + untrusted content + exfiltration. Rule: the AI must never hold a capability the user it acts for lacks (same authz wall).

Q: The 2026 auth build-vs-buy shortlist?
A: Clerk (fast, best DX, free to 50k users), Supabase Auth (with your Postgres), Better Auth (open-source, zero per-user cost), WorkOS (enterprise SSO).

Q: The default database for 95% of products at this stage?
A: One Postgres. It does relational, JSON, full-text, vectors, and queues. Add a second datastore only on measured pain.

Q: The one scale concern that bites early?
A: Connection pooling on serverless — "too many connections" arrives at hundreds of users. Use transaction-mode pooling / a serverless driver.

Q: Expand/contract migration, in one line?
A: To change a column without downtime: add new + write both (expand), backfill separately, then drop old (contract), across deploys.

---

## My take (reviewer lens)

**Chip Huyen** would want the synthesis to stress that measurement is continuous,
not a phase: the six AI metrics and quality-drift are systems you run forever, not
a checklist you complete.[^2] Right. **Michael Seibel** would want it shorter and
would remind you that all of this serves one question — do people keep using the
thing — and that at your scale the answer comes faster from watching users than
from any dashboard. Also right; the small-N loop is built around exactly that.
Hold both: instrument the few things that matter, then go watch a human use your
product. The chart tells you where to look; the human tells you what is wrong.

## Further reading

Re-read the week's must-reads for whichever quiz question you missed. The single
highest-leverage follow-up, whatever your score: pick one real user, watch them
use your product end to end, and see how many of this week's metrics you could
actually compute for them right now. The gaps are your next week's work.

## Citations

[^1]: Reforge, "How to Choose & Measure North Star Metrics" — activation model,
retention plateau. https://www.reforge.com/blog/north-star-metrics (search-verified
2026-07-17.)
[^2]: Chip Huyen, *AI Engineering* (O'Reilly, 2025) — continuous in-prod
evaluation, inference cost as a first-class concern.
https://www.oreilly.com/library/view/ai-engineering/9781098166298/ (search-verified
2026-07-17.)
[^3]: Ron Kohavi et al., *Trustworthy Online Controlled Experiments* (2020) —
power/sample-size, peeking. https://experimentguide.com/ (search-verified
2026-07-17.)
[^4]: Simon Willison, "The lethal trifecta for AI agents" (2025).
https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/ (search-verified
2026-07-17; canonical home b0w02.)
[^5]: Startup Genome, "Premature Scaling" (2011).
https://s3.amazonaws.com/startupcompass-public/StartupGenomeReport2_Why_Startups_Fail_v2.pdf
(search-verified 2026-07-17.)
[^6]: Clerk pricing (free to 50k users, Feb 2026). https://clerk.com/pricing
(search-verified 2026-07-17.)
[^7]: Neon vs Supabase managed-Postgres pricing (2026).
https://vela.simplyblock.io/articles/neon-serverless-postgres-pricing-2026/
(search-verified 2026-07-17.)

_last_verified: 2026-07-17_
