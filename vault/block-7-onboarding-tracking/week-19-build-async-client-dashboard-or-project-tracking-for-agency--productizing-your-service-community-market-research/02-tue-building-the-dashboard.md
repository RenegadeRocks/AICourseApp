---
type: lesson
block: block-7-onboarding-tracking
week: week-19
session_slug: building-the-dashboard
day_of_cycle: 2
day_name: tue
date_due: 2026-09-22
tags:
  - client-dashboard
  - multi-tenant
  - row-level-security
  - ai-status-summary
  - white-label
  - supabase
  - code-lab
sources:
  - supabase-rls-docs
  - makerkit-supabase-rls
  - designrevision-supabase-rls-2026
  - supaexplorer-rls-basics
  - anthropic-claude-models
  - manyrequests-white-label-portal
  - assembly-client-portal
last_verified: 2026-07-17
word_count_target: 3300
---

# Building the dashboard (AI-assisted)

## Why this matters

Today you design the thing you decided to build yesterday: the data model, the
client-scoped access pattern that keeps Client A from ever seeing Client B's data,
the AI-generated status summary that writes your weekly update for you, and the
read-only client view. This is the technical spine of Saturday's `code-lab`. Get
the access model right and you have a portal you can trust with real client data.
Get it wrong and you have a data breach one API call away. The AI summary is the
piece that makes the whole thing sustainable, because a dashboard nobody keeps
current is worse than no dashboard at all.

## Prerequisites

- [[block-5-product-building-principles/week-14-analytics-iteration-what-to-measure--scale-infra-auth-db-ui-polish/04-thu-auth-and-security-for-real-users|Week 14 — auth and security]]. We do **not** re-teach auth here. You already know how to stand up authentication, sessions, and password/OAuth flows. Today is about the layer above auth: multi-tenant *authorization*.
- [[block-5-product-building-principles/week-13-making-your-product-feel-magic-with-ai--how-to-add-smart-features-that-wow-users/06-sat-build-add-one-magical-feature|Week 13 — the magic feature]]. The AI status summary is a direct application of the "one magical feature" pattern: a small, reliable, delightful LLM touch, not an agent.
- [[block-5-product-building-principles/week-12-frontend-basic-uiux-design-principles--build-mvp-backend-connect-with-ai-workflows/04-thu-mvp-backend-architecture|Week 12 — backend architecture]]. The data-model thinking builds on this.

## The data model: four objects and a tenant key

A client dashboard is a small, well-shaped schema. Resist the urge to model your
entire agency. You need four objects and one idea that ties them together.

**The four objects**, mapping directly to Monday's four dashboard sections:

- **Client** — the tenant. Name, brand (logo, color for white-labeling), and the
  users who belong to it.
- **Project** — an engagement for a client. Status (On track / At risk /
  Blocked), current phase, a percent or milestone, and a one-line status reason.
- **Deliverable** — a shipped or in-flight output. Name, date, status (Draft / In
  review / Approved), a link, and a `blocked_on` flag (us vs client) that powers
  the "waiting on you" list.
- **Metric** — an outcome number for the project. Label, value, unit, and a
  timestamp, so you can show "hours saved: 42" or "spend: $8,400 → 31 leads."

**The one idea: the tenant key.** Every row that belongs to a client carries a
`client_id` (the tenant identifier). This single column is what makes the whole
multi-tenant model enforceable. It is not a convenience field. It is the thing the
database uses to decide who can see what. Skip it or make it optional and you have
no isolation.

That is the entire model for v1. A `client` has many `projects`; a `project` has
many `deliverables` and `metrics`; every one of those rows carries the `client_id`
of its owner. You can add invoices, messages, and files later. For a dashboard
that passes Saturday's bar, four objects and a tenant key are enough.

## Multi-tenant access: the part you cannot get wrong

Here is the single most important technical idea this week, and the one that
separates a real client portal from a toy. **You must enforce data isolation at
the database layer, not the application layer.** Application-layer filtering
(remembering to add `WHERE client_id = ?` to every query) works right up until the
one query where a developer or an AI coding assistant forgets, and then Client A
sees Client B's data. The correct pattern moves the guarantee into the database
itself, so a forgotten filter fails closed.

In 2026 the standard, well-documented way to do this on a backend-as-a-service is
**PostgreSQL Row-Level Security (RLS)**, which is what Supabase exposes and
documents as the foundation of safe direct client access.[^1] The mechanics,
verified against Supabase's current docs and multiple 2026 production guides:[^1][^2][^3]

1. **Enable RLS on every table exposed through the API.** With RLS off, any client
   holding your anon key can read or write any row. With it on, the database
   rejects any access that no policy explicitly permits. RLS is not a feature you
   add later; it is the default posture, and every exposed table needs it or you
   are, in the words of the Supabase-ecosystem guides, "one API call away from a
   data breach."[^1][^2]

2. **Put the tenant identity in the JWT.** On login, set a custom claim (the
   user's `client_id` / tenant) in the auth token via an auth hook, so the
   database can read the tenant from the token without an extra lookup on every
   query.[^2][^3]

3. **Write policies that match the row's tenant against the token's tenant.** The
   canonical policy is: allow a row when `client_id = auth.jwt() ->> 'client_id'`.
   Now every query is automatically scoped to the caller's tenant, enforced by
   Postgres, with no application code required and no way to forget.[^2]

4. **Index every column an RLS policy references.** A missing index on `client_id`
   is the top performance killer for RLS-heavy apps, because the policy runs on
   every row access.[^2][^4]

5. **Test policies from the client SDK, not the SQL editor.** The SQL editor runs
   as a privileged role and *bypasses RLS*, so a policy that looks correct there
   can still be wide open in production. Test as a real logged-in client.[^2]

6. **Never expose the `service_role` key in client code.** That key bypasses RLS
   entirely. It lives only on your server. Leaking it into a frontend bundle
   nullifies every policy you wrote.[^2]

The defense-in-depth framing that these guides converge on is worth internalizing:
**RLS handles data and tenant isolation** (users see only their own rows, orgs see
only their own data), while **the application layer handles feature gating, rate
limits, and workflow logic**.[^2][^4] Do not try to make RLS do everything, and do
not try to do isolation in the application. Each layer does its job.

> My take: this is the one place in the week where "move fast and fix later" is
> the wrong instinct, and Boris Cherny would say the same (reviewer lens). A
> forgotten `WHERE` clause in a marketing dashboard is a bug. A forgotten one in a
> client portal holding multiple clients' business data is a breach you have to
> disclose. Build the isolation correctly the first time. It is not more work; it
> is a policy you write once.

The Saturday `code-lab` implements this pattern in a self-contained way so you can
run and test it without a live Supabase project, then maps it to the real Supabase
RLS setup in its README. The concept transfers directly to a production build.

## Read-only client views vs your internal view

The same data, two surfaces. Your team sees everything: internal notes, draft
deliverables, the messy middle. The client sees the curated four sections from
Monday. The read-only client view is not a permissions afterthought; it is a
first-class design decision.

Two ways to implement the split, in increasing robustness:

- **Field/row visibility flags.** Deliverables carry an `is_client_visible`
  boolean; internal notes live in a separate table the client's RLS policy never
  touches. Simple, and enough for v1.
- **A dedicated client-facing read model.** A separate view or set of endpoints
  that exposes only client-safe fields, so the client app *cannot* request an
  internal field even if it tried. More work, more robust, the right end state.

For v1, the client's RLS policy restricting them to their own `client_id`, plus an
`is_client_visible` flag on deliverables, is enough. The client is read-only by
design: their token grants `SELECT` on their rows and nothing more. No update, no
insert. The one exception you may allow later is a client *approval* action
(approve a deliverable), which is a narrow, audited write. Start read-only.

## The AI angle: auto-generated status summaries

This is the feature that makes the dashboard sustainable and the one that applies
Week 13's magic pattern directly. The problem: even a great dashboard decays if
someone has to hand-write the weekly narrative update. The fix: generate it.

The pattern is deliberately small. **Given the structured state of a project (its
status, recent deliverables, open blockers, and metric deltas), an LLM writes a
concise, client-appropriate status summary.** It is a summarization task over
data you already hold, not an agent, not a chatbot. That is what makes it
reliable.

Design decisions that matter:

- **Ground it in real data, not vibes.** The prompt is filled from the database:
  "Here are the deliverables shipped since the last summary, the current status
  and reason, the open client-blockers, and the metric changes. Write a
  three-sentence client update." The model summarizes facts you supply; it does
  not invent progress. This is the single most important reliability decision,
  and it is the same grounding discipline you would apply to any retrieval-backed
  feature. An ungrounded "write a nice update" prompt will hallucinate progress
  and eventually lie to a client, which is a trust-destroying failure in exactly
  the surface whose entire job is trust.

- **Draft, then human-approve, for now.** The summary is generated as a *draft*
  the operator approves before it goes to the client. You are the eval layer. Over
  time, as you trust it, you can auto-publish low-stakes summaries, but a
  client-facing artifact starts human-in-the-loop. This is the reliability-of-
  magic lesson from Week 13 applied: the magical feature must be *reliable* to be
  magical, and reliability here means a human gate on anything a client reads.

- **Use a cheap, fast model and keep the prompt tight.** This is a short
  summarization over small structured input. It does not need a frontier model.
  On the current Anthropic lineup, Haiku 4.5 or Sonnet 5 is the right tier for a
  bounded summarization task like this; Sonnet 5 is the new default and priced for
  exactly this kind of high-volume, low-complexity call.[^5] Reserve the expensive
  tiers for reasoning you cannot do with a template.

- **Make it deterministic where you can.** The metric deltas, the deliverable
  list, the blocker list: compute those in code, deterministically, and let the
  LLM only do the natural-language wrapping. The less you ask the model to reason
  about, the less it can get wrong. The `code-lab` follows this split: code
  assembles the facts, the model writes the prose.

The `code-lab` AI-summary endpoint takes a `client_id`, pulls that client's
project state (already tenant-scoped), assembles the facts deterministically, and
returns a generated summary. In offline mode it uses a deterministic template so
the whole thing runs and tests without an API key; wired to a real key it calls
the model. That offline/online split is itself a good pattern for any AI feature:
the deterministic path is your test harness and your fallback.

## Deliverable QA with AI

A second, optional AI touch worth designing now. Before a deliverable is marked
client-visible, an LLM can run a lightweight QA pass against a checklist: does the
deliverable meet the stated scope, are there obvious errors, does it match the
brief. This is not a replacement for human review. It is a pre-flight check that
catches the embarrassing miss before the client sees it, and it is a preview of
Thursday's theme, quality control at speed. Treat its output as a flag for human
attention, never as an approval. The eval discipline that governs this is the
subject of
[[block-2-ai-employees/week-04-building-a-sales-agent--building-comprehensive-rag-ai-agent/06-sat-rag-evaluation|Week 4's evaluation lesson]];
the short version is that an AI QA pass you have not measured is a false sense of
security, so if you build it, measure its catch rate against a labeled set before
you trust it.

## White-labeling

For a premium-positioned service, the dashboard living at your brand (or the
client's) is part of the product. White-labeling has three levels, in increasing
cost:

1. **Brand skin.** The client's logo and your color on their view. Trivial: two
   fields on the `client` object, read into the view. Do this in v1.
2. **Custom domain.** The portal served at `clients.youragency.com` or a
   per-client subdomain. A DNS and hosting task, not a code task; worth it once
   you have a few clients.
3. **Full white-label / reseller.** Your branding removed entirely, the tool
   appearing as the client's own. This is where bought tools charge a premium
   (Assembly gates it at the $399/mo tier; ManyRequests at Pro),[^6] and where a
   custom build gives it to you for free because it was always your brand.

The white-label question also feeds back into yesterday's build-vs-buy call: if
full white-label is essential to your positioning and your bought-tool tier
charges heavily for it, the custom build's economics improve.

## Worked example: the build spec

Today's artifact is a one-page build spec you will implement Saturday. For a
concrete case, take a solo AI-automation consultant with four clients who decided
(against Seibel's advice, for learning) to build.

**Data model.**
```
client(id, name, logo_url, brand_color)
project(id, client_id, name, status, phase, percent, status_reason, updated_at)
deliverable(id, client_id, project_id, name, status, link, is_client_visible,
            blocked_on, created_at)     -- blocked_on ∈ {none, us, client}
metric(id, client_id, project_id, label, value, unit, recorded_at)
```

**Access model.** RLS on every table. Policy: a row is visible when its
`client_id` matches the `client_id` claim in the caller's JWT. Client tokens grant
`SELECT` only. `client_id` indexed on every table. Service key server-side only.

**Client view.** Four sections: Progress (project status + reason), Deliverables
(client-visible only, with the "blocked on you" list surfaced from
`blocked_on = 'client'`), Metrics (latest per label), Next steps (generated).

**AI summary.** Endpoint `GET /clients/:id/summary`: pull tenant-scoped project
state, assemble facts in code, generate a three-sentence draft summary with a
cheap model, return as `draft` pending operator approval. Offline template
fallback for testing.

**White-label.** v1: logo + brand color from the `client` row rendered into the
view. Custom domain deferred.

**Pass bar for today:** a build spec another developer (or an AI coding assistant)
could implement without asking you a question, with the RLS policy written out
explicitly and the AI-summary grounding described. If your spec says "add auth"
without specifying the tenant-claim-to-RLS-policy chain, it is not done.

## Common mistakes experts see

1. **Filtering by tenant in application code instead of RLS.** Works until one
   forgotten `WHERE` clause leaks a client's data. Enforce isolation in the
   database so it fails closed.[^1][^2]

2. **Testing RLS policies in the SQL editor.** The editor bypasses RLS. A policy
   that looks correct there can be wide open in production. Test as a logged-in
   client via the SDK.[^2]

3. **Shipping the `service_role` key to the frontend.** It bypasses every policy.
   It lives only on your server. This single mistake nullifies all your isolation
   work.[^2]

4. **Ungrounded AI summaries.** "Write a nice status update" hallucinates
   progress and will eventually lie to a client. Fill the prompt with real
   deliverables, blockers, and metric deltas; let the model only phrase them.

5. **Auto-publishing AI summaries to clients on day one.** A client-facing
   artifact starts human-in-the-loop. You are the eval layer until the feature has
   earned trust. Draft, approve, then send.

6. **Over-modeling the schema.** You do not need invoices, messages, files, and a
   CRM in v1. Four objects and a tenant key ship a working dashboard. Add the
   rest when a client asks.

## Reflection questions

1. Write out your RLS policy in one sentence. What claim is in the token, and what
   column does it match? If you cannot, you do not yet have a multi-tenant model.
2. What is the one metric per project your dashboard will show, and where does its
   value come from, entered by hand, computed, or pulled from an integration?
3. What facts will you feed the AI summary prompt, and which of those will you
   compute deterministically in code rather than let the model reason about?
4. What is your human-approval gate on AI-generated client content, and when (if
   ever) would you remove it?
5. Does full white-label matter enough to your positioning to change your
   build-vs-buy decision from Monday?

## My take (reviewer lens)

**Boris Cherny** would zero in on the RLS discipline and the AI-coding-assistant
angle. His current work is fleet-scale agent management, and the relevant warning
is precise: an AI coding assistant will happily write the query that forgets the
tenant filter, because it is optimizing for "make the feature work," not "fail
closed on a permission boundary."[^7] RLS is exactly the kind of guarantee you
want in the database *because* your codegen tools cannot be trusted to remember it
on every query. Let the database be the backstop your assistant will occasionally
need.

**Jerry Liu** would push on the AI-summary grounding. His whole body of work on
retrieval-augmented systems says the same thing this lesson does: the quality of
an LLM output is the quality of the context you feed it, and an ungrounded summary
is a hallucination generator.[^8] He would want the fact-assembly step treated as
a small retrieval problem, structured, deterministic, complete, and would be
skeptical of any summary the model wrote from anything less than the full,
current project state.

**A cohort peer** shipping their first client portal would ask the practical
question the lesson should answer plainly: is this overkill for four clients? Yes,
somewhat, and Monday admitted it. The RLS rigor is non-negotiable *if* you build,
because a leaky client portal is worse than none. But the peer is right that for
four clients a bought portal skips all of this, and the only reason to build is to
own the primitives and the option. Build to learn, then decide.

## Further reading

**Must-read**

- Supabase Docs, "Row Level Security" — the canonical reference for the access
  model this entire dashboard depends on. Read it before you write a line.[^1]

**Recommended**

- MakerKit, "Supabase RLS Best Practices: Production Patterns for Secure
  Multi-Tenant Apps" — the JWT-claim-to-policy pattern and the common breakages,
  in production terms.[^2]

**Optional**

- The Week 13 magic lesson (linked above) — re-read the reliability-of-magic
  section before wiring the AI summary; it is the same discipline.

## Citations

[^1]: Supabase Docs, "Row Level Security."
https://supabase.com/docs/guides/database/postgres/row-level-security — RLS as the
foundation of safe direct client access; every exposed table needs it. (search-
verified 2026-07-17; fetch egress-blocked — liveness pass pending; corroborated by
MakerKit and SupaExplorer guides below.)
[^2]: MakerKit, "Supabase RLS Best Practices: Production Patterns for Secure
Multi-Tenant Apps." https://makerkit.dev/blog/tutorials/supabase-rls-best-practices
— tenant_id + JWT claim policy; index RLS columns; test from client SDK not SQL
editor; never expose service_role; defense-in-depth split. (search-verified
2026-07-17; corroborated by Supabase docs and DesignRevision 2026 guide.)
[^3]: DesignRevision, "Supabase RLS Guide 2026: Policies That Actually Work."
https://designrevision.com/blog/supabase-row-level-security — JWT custom claims
for tenant identity; enabling-RLS-then-writing-policies workflow. (search-verified
2026-07-17; corroborated by MakerKit.)
[^4]: SupaExplorer, "Enable Row Level Security for Multi-Tenant Data."
https://supaexplorer.com/best-practices/supabase-postgres/security-rls-basics/ —
RLS for data + tenant isolation, application for feature gating; index RLS
columns. (search-verified 2026-07-17; corroborated by MakerKit.)
[^5]: Anthropic model lineup (current): Sonnet 5 (new default, priced for
high-volume low-complexity calls), Haiku 4.5, Opus 4.8. Per the July 2026 course
landscape reference; use a cheap fast tier for bounded summarization.
https://www.anthropic.com/pricing — (search-verified 2026-07-17; corroborated by
the course master refresh model lineup.)
[^6]: Assembly / ManyRequests white-label tiers.
https://assembly.com/client-portal and https://manyrequests.com/blog/white-label-client-portal-software
— full white-label gated at Assembly's top tier (~$399/mo) and ManyRequests Pro.
(search-verified 2026-07-17; corroborated by Capterra and GetZendo.)
[^7]: Boris Cherny — current public record on fleet-scale agent management
(Fortune, Jun 2026); AI coding assistants optimize for working code, not for
failing closed on permission boundaries. (attribution per course roster note;
reviewer-lens framing, not a fast-moving stat.)
[^8]: Jerry Liu (LlamaIndex) — retrieval-quality-determines-output-quality
principle applied to grounded generation. https://www.llamaindex.ai/blog —
(evergreen RAG principle; general attribution to Liu's body of work.)

_last_verified: 2026-07-17_
