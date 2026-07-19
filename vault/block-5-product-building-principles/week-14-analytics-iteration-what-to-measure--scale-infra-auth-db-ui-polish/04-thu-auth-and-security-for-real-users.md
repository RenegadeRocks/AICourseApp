---
type: lesson
block: block-5-product-building-principles
week: week-14
session_slug: scale-infra-auth-db-ui-polish
day_of_cycle: 4
day_name: thu
date_due: 2026-08-20
tags:
  - authentication
  - clerk
  - better-auth
  - supabase-auth
  - workos
  - rbac
  - multi-tenancy
  - row-level-security
  - secrets-management
  - soc2
sources:
  - clerk-pricing-2026
  - clerk-changelog-new-plans-2026
  - supabase-auth-rls-2026
  - workos-nextauth-alternatives-2026
  - betterauth-vs-nextauth-2026
  - buildmvpfast-better-auth-decision-2026
  - owasp-agentic-top10-2026
  - simonwillison-lethal-trifecta-2025
  - twelve-factor-config-2011
  - vanta-soc2-basics-2026
last_verified: 2026-07-17
word_count_target: 5300
---

# Auth & security for real users: the day your product stops being a demo

## Why this matters

Up to now your product had one user: you. The moment a stranger logs in, three
new failure modes appear that a demo never has. They can see *each other's data*
if your multi-tenancy is wrong. They can *become* each other if your sessions are
sloppy. And because your product has an AI that reads user data and calls tools,
a hostile user can try to make the AI leak or act across that boundary. This is
the day you build the walls, and it is the difference between a product you can
sell upmarket and one that produces a breach post-mortem.

After this lesson you can make the build-vs-buy auth decision on real 2026
numbers, implement session and role management without rolling your own crypto,
enforce tenant isolation at the layer that actually holds (the database), manage
secrets like an adult, and understand the AI-specific attack surface well enough
to not build the vulnerable version. You will also know the minimum SOC 2 posture
that lets you sell to a company with a security questionnaire.

## Prerequisites

- [[block-0-basecamp/week-02-basecamp-part-3-mcps-voice-agents--basecamp-part-4-revisiting-n8n-ai-agent-fundamentals/03-wed-mcp-security|MCP security & the lethal trifecta]]
  (Basecamp). That is the canonical home for *how* prompt-injection attacks work.
  We do not re-teach the attack today; we defend the user-data boundary against
  it. If "lethal trifecta" is unfamiliar, read that first.
- [[block-3-advanced-topics-voice/week-08-automation-agent-integration-mcps--build-hybrid-agent-scraper-summarizer/05-fri-reliability-engineering-for-unattended-agents|Reliability engineering for unattended agents]]
  (Block 3), for the trust-boundary mindset when an agent acts without a human.
- [[block-4-test-validate-package/week-09-packaging-selling-your-ai-agents--create-your-first-sellable-agent-package/05-fri-pricing-the-package|Packaging & pricing]]
  (Block 4), because SOC 2 readiness is a sales-enablement decision, not just a
  security one.

## First principles: authentication vs authorization

Two words people blur, and the blur causes breaches.

- **Authentication (authn)**: *who are you?* Login, sessions, MFA. Answered once
  per session.
- **Authorization (authz)**: *what are you allowed to touch?* Roles, permissions,
  tenant isolation. Answered on *every* request.

The number-one real-world failure is not weak passwords; it is **broken
authorization** — a logged-in user (correctly authenticated) reaching data they
should not (incorrectly authorized). This is OWASP's #1 web risk for years
running, and it is entirely on you: no auth provider fixes it, because it lives
in your data-access layer. Keep the two words separate in your head and you will
avoid the most common way products leak.

## Part 1 — Build vs buy: the 2026 auth decision

Rolling your own auth from scratch is almost always a mistake; you will get
password hashing, session fixation, or token rotation subtly wrong. The real
decision is *which* not-from-scratch option, and it is one of this week's live
controversies. Four contenders, with current numbers.

**Clerk** is the drop-in, best-DX, buy-it option. As of a February 2026 pricing
change, the free tier covers **50,000 monthly active/retained users** (up from
10,000), with Pro from about $25/mo plus roughly $0.02 per user beyond the
included allotment, and unlimited applications on every plan.[^1] A subtlety that
matters for your cost math: Clerk bills on **Monthly Retained Users (MRU)**, a
user who returns at least 24 hours after signup, not raw MAU, so a naive MAU
estimate *overstates* your Clerk bill.[^2] You get hosted UI components, MFA,
social login, and organizations out of the box. Cost climbs at scale.

**Supabase Auth** is the batteries-included-with-your-database option. If you are
already on Supabase Postgres, auth is included: real user tables, row-level
security for authorization, social providers, magic links, MFA. Free to 50,000
MAU, Pro at $25/mo with additional MAU around $0.00325 each, which at 100k MAU is
roughly $187/mo versus Clerk's much higher figure at the same scale.[^3] The pull
is that authz lives *in the same database* as your data, so tenant isolation and
auth share one enforcement point (Part 3).

**Better Auth** is the 2026 open-source insurgent and the reason "Auth.js
(NextAuth)" is no longer the default recommendation. It is a TypeScript library
that runs *inside your app* with no external service, storing users in your own
database. Created September 2024 by Bereket Engida, it went through Y Combinator's
S25 batch, raised a $5M seed, and by mid-2026 has ~28–30k GitHub stars and 150k+
weekly npm downloads; it is now the auth library recommended by Next.js, Nuxt,
and Astro.[^4] Zero marginal cost per user (you host it), full control, at the
price of operating it yourself. Auth.js still works for existing projects, but
the 2026 consensus is: do not start a new one on it.[^5]

**WorkOS** is the sell-to-enterprise option: SSO, SCIM directory sync, audit
logs, the things a Fortune-500 security questionnaire demands. Free for SSO and
Directory Sync up to a large user count, then enterprise pricing.[^6] You reach
for WorkOS when a specific enterprise deal requires SAML SSO, not before.

The decision tree that most 2026 guides converge on:

- Shipping fast, want it to just work, under ~50k users → **Clerk**.
- Already committed to Supabase Postgres, want auth+data in one place → **Supabase Auth**.
- Want zero per-user cost and full control, comfortable operating it → **Better Auth**.
- A specific enterprise deal needs SAML SSO now → add **WorkOS**.

> My take: the common 2026 pattern is real — start on Clerk for speed, and if you
> cross the free tier and cost becomes a line item, migrate to Supabase Auth or
> Better Auth.[^7] Plan for that migration by keeping your user-id references
> clean and provider-agnostic from day one, so the swap is a weekend, not a
> rewrite. For this course's Saturday build we use a provider you can run
> entirely locally so nobody needs a paid account, and I will name the migration
> path explicitly.

## Part 2 — Sessions and roles without rolling your own crypto

Whatever provider you pick, understand what it is doing so you can debug it.

**Sessions.** After login, the server needs to remember who you are across
requests. Two dominant patterns: a **session cookie** pointing at server-side
state (easy to revoke, needs a store) or a **stateless JWT** the client carries
(scales without a store, harder to revoke before expiry). For most products a
short-lived access token plus a rotating refresh token, in **httpOnly, Secure,
SameSite cookies**, is the right default. The non-negotiables: httpOnly (so
JavaScript, and any XSS, cannot read the token), Secure (HTTPS only), SameSite to
blunt CSRF, and short access-token lifetimes with rotation. Your provider does
this; your job is to not undo it (never put a session token in `localStorage`,
where any injected script can read it).

**Roles (RBAC).** Role-Based Access Control assigns permissions to roles and
roles to users. Start with the fewest roles that model reality (often just
`owner`, `member`, and maybe `admin`), and store the *permission check*, not the
role name, at the point of use: check `can("delete", report)`, not
`if user.role == "admin"`. That indirection means adding a role later does not
require hunting every `if role ==` in your codebase. Do not over-engineer to
attribute-based access control (ABAC) until a real requirement forces it; that is
authz premature scaling.

## Part 3 — Multi-tenancy: the wall that must not leak

This is the highest-stakes section. In a multi-tenant product, every row of data
belongs to a tenant (an account/org), and the cardinal sin is one tenant reading
another's rows. There are three isolation models:

1. **Row-level (shared tables, `tenant_id` column).** One database, every table
   carries `tenant_id`, every query filters on it. Cheapest, most common,
   most dangerous if you enforce it only in application code, because one
   forgotten `WHERE tenant_id = ?` leaks everything.
2. **Schema-per-tenant.** Each tenant gets its own Postgres schema. Stronger
   isolation, heavier operations, painful past a few hundred tenants.
3. **Database-per-tenant.** Total isolation, maximum operational cost. For
   regulated or high-value enterprise tenants only.

For nearly everyone the answer is **row-level, enforced in the database, not the
app**. The mechanism is **Postgres Row-Level Security (RLS)**: you write policies
on the table itself so the database *refuses* to return rows outside the current
tenant, regardless of what the application query says. Supabase builds its entire
auth-to-data story on RLS for exactly this reason: the enforcement lives one layer
below your application code, so an application bug cannot leak across
tenants.[^3][^8]

The rule to tattoo on your wrist: **application-layer tenant filtering is a
performance optimization, not a security boundary.** The security boundary is
RLS (or an equivalent DB-enforced policy). If your isolation depends on every
developer remembering a `WHERE` clause forever, you do not have isolation; you
have a countdown.

## Part 4 — The AI-specific attack surface

Now the part that is new since your product grew an AI. A traditional web app's
attack surface is requests. Your product's attack surface *also* includes the
text the model reads, because that text can contain instructions. This is the
lethal trifecta from [[block-0-basecamp/week-02-basecamp-part-3-mcps-voice-agents--basecamp-part-4-revisiting-n8n-ai-agent-fundamentals/03-wed-mcp-security|Basecamp]]:
Simon Willison's formulation that danger arises when a system combines
**(1) access to private data, (2) exposure to untrusted content, and (3) the
ability to exfiltrate** (send data out).[^9] We do not re-explain the mechanism;
we defend the boundary.

The concrete risk for *your* multi-tenant AI product: a malicious user (or a
document they upload) plants an instruction that makes the AI read or act on
*another tenant's* data, or exfiltrate the current tenant's data to an attacker.
The defenses, layered:

- **The AI runs inside the same authz walls as the user, never above them.** The
  model's tool calls and data reads must execute *as the current tenant*, subject
  to the same RLS policies. If the AI queries the database with a service-role key
  that bypasses RLS, one prompt injection reads every tenant. Never give the model
  a credential more powerful than the user it acts for.
- **Treat all retrieved/user content as untrusted data, not instructions.**
  Separate the system prompt (trusted) from retrieved documents and user input
  (untrusted) structurally, and never let untrusted content escalate privileges.
- **Constrain exfiltration.** Limit the tools that can send data outward; be
  especially careful with any tool that fetches arbitrary URLs (a classic
  data-exfil channel) or renders model-controlled links/images.

The field now has a named, quantified threat model for this: the **OWASP Agentic
AI Top 10** (2026) catalogs agent-specific risks including agent authorization
compromise and tool misuse, and there are real incidents behind it (a Postgres-MCP
SQL-injection finding, a supply-chain compromise of an MCP server, and
CVE-2025-6514 among them).[^10] You do not need to memorize the list; you need to
internalize the one rule it keeps repeating: **the agent must never be able to do
something the human on whose behalf it acts could not do.** Authz is the same
boundary for the human and the AI.

## Part 5 — Secrets and SOC 2 readiness

**Secrets.** API keys, database passwords, signing secrets. The baseline, from
the 12-Factor App's config principle: **strict separation of config from code**,
secrets in the environment, never in the repo.[^11] Practically: `.env` files
gitignored for local dev, your host's secret manager (or a dedicated one) in
production, and never a key in client-side code where the browser can read it.
Rotate on any suspected exposure. This is unglamorous and it is the single most
common way indie products get owned: a key committed to a public repo, scraped
within minutes.

**SOC 2 readiness.** The moment you sell to a company of any size, a security
questionnaire arrives, and eventually the question "are you SOC 2?" SOC 2 Type II
is an audited attestation that you have and *follow* security controls (access
control, encryption, monitoring, incident response) over a period. You do not
need the full audit to start selling, but the *readiness posture* is a sales
asset: MFA everywhere, least-privilege access, encryption in transit and at rest,
audit logging, and a written incident-response plan.[^12] Automation platforms
(Vanta, Drata) will get an indie team audit-ready far faster than doing it by
hand, and the decision to pursue it is a packaging/pricing decision tied to
moving upmarket ([[block-4-test-validate-package/week-09-packaging-selling-your-ai-agents--create-your-first-sellable-agent-package/05-fri-pricing-the-package|Block 4]]).
Do not pursue SOC 2 before a customer asks; do build the product so pursuing it
later is checkbox work, not a rewrite.

## Worked example

The full auth + RLS + AI-boundary wiring is Saturday's code-lab. Today, the one
policy that carries the most weight: the RLS pattern that makes the AI safe by
construction.

```sql
-- rls_tenant_isolation.sql — the wall the AI cannot walk around.
-- Every tenant-owned table carries tenant_id and enforces it in the DB.
alter table reports enable row level security;

-- The policy: a session may only see rows for its own tenant.
-- current_setting('app.tenant_id') is set per-request from the authenticated session.
create policy tenant_isolation on reports
  using (tenant_id = current_setting('app.tenant_id')::uuid);

-- The AI acts AS the user: same connection, same tenant setting, same policy.
-- It CANNOT use a service-role key that bypasses RLS. That is the whole defense.
```

**Pass bar:** with this policy live, a query for `select * from reports` returns
only the current tenant's rows even if the application forgot its `WHERE` clause,
and even if a prompt injection convinces the AI to try to read everything. If you
can demonstrate that a second tenant's rows are invisible from the first tenant's
session, you have built the wall that actually holds. If your isolation still
depends on the application remembering to filter, you have not.

## Common mistakes experts see

1. **Confusing authn and authz.** Building strong login and leaving broken
   object-level authorization is the #1 real breach. Every request re-checks
   *what*, not just *who*.
2. **Tenant isolation in app code only.** One forgotten `WHERE tenant_id` leaks
   everything. Enforce in the database (RLS).
3. **Giving the AI a god-mode credential.** A service-role key that bypasses RLS
   turns one prompt injection into a full-tenant breach. The AI acts *as* the
   user, never above.[^9][^10]
4. **Session tokens in localStorage.** Any XSS reads them. httpOnly, Secure,
   SameSite cookies, short lifetimes, rotation.
5. **Secrets in the repo.** Committed keys are scraped in minutes. Config in the
   environment, always.[^11]
6. **Rolling your own crypto/sessions.** You will get rotation or fixation subtly
   wrong. Use a maintained provider.
7. **Pursuing SOC 2 before a customer asks — or building so it needs a rewrite
   later.** Both are wrong. Build ready, certify on demand.

## Reflection questions

1. In your product, where exactly is tenant isolation enforced — the app or the
   database? If the app, write down the query that leaks everything when someone
   forgets a clause.
2. Does your AI feature query data with the user's permissions or with a
   service-role key? If the latter, what stops a prompt injection from reading
   every tenant?
3. Which auth provider fits your next 12 months, and what is your concrete
   migration path if its cost becomes a line item?
4. Name every place a secret currently lives in your project. Is any of them a
   git-tracked file or client-side code?
5. If a customer sent you a security questionnaire tomorrow, which three controls
   would you fail on, and which is a one-day fix versus a one-month one?

## My take (reviewer lens)

**Simon Willison** would sharpen the AI-boundary section: he argues there is
still *no reliable, general defense* against prompt injection, so the only robust
posture is architectural — assume injection will succeed and ensure the trifecta
is never fully present.[^9] I framed the defenses as layers, which is right, but
he would insist the load-bearing one is not "detect the injection" (unreliable)
but "make sure the AI has no capability the current user lacks and no unconstrained
exfil path." Detection is a nice-to-have; capability-constraint is the wall.

**Boris Cherny** would point at the operational failure mode: the RLS policy that
exists in a migration but was never *tested* against a hostile second tenant. His
instinct is to make the isolation claim executable — a test that spins up two
tenants and asserts cross-tenant reads return zero rows, run in CI on every
change. Saturday's code-lab includes exactly that test, because an untested wall
is a wall you are trusting on faith.

**A cohort peer** shipping their first paid product would push back on the whole
lesson as premature: "I have four users, why am I doing RLS and SOC 2?" Fair for
SOC 2, which is genuinely on-demand. Not fair for tenant isolation, because the
first cross-tenant data leak is not a bug you fix, it is a trust event you may not
survive, and retrofitting RLS after you have data is far harder than starting with
it. Auth and isolation are the two things worth doing *right* before you have
users, precisely because fixing them after is so costly.

## Further reading

**Must-read**

- Simon Willison's writing on the lethal trifecta and prompt injection, for the
  architectural-defense posture.[^9]
- OWASP Agentic AI Top 10 (2026), for the named threat model.[^10]

**Recommended**

- Supabase Row-Level Security docs, for the DB-enforced isolation pattern.[^8]
- The 2026 auth-provider comparisons (Clerk / Supabase / Better Auth / WorkOS),
  for current pricing before you commit.[^1][^4][^7]

**Optional**

- The 12-Factor App, "Config," for secrets discipline.[^11]
- A SOC 2 readiness primer (Vanta/Drata), for the sell-upmarket checklist.[^12]

## Citations

[^1]: Clerk pricing (2026) — free tier raised to 50,000 users Feb 5 2026, Pro
from ~$25/mo + ~$0.02/user beyond included, unlimited apps.
https://clerk.com/pricing and https://clerk.com/changelog/2026-02-05-new-plans-more-value
(search-verified 2026-07-17; two Clerk sources plus third-party
https://saasprices.net/blog/clerk-free-plan-changes).
[^2]: Clerk bills on Monthly Retained Users (returns ≥24h after signup), not raw
MAU. https://clerk.com/articles/clerk-pricing-explained (search-verified
2026-07-17; corroborated by https://www.promptstoproduct.com/clerk-pricing-explained).
[^3]: Supabase Auth included with Postgres; free to 50k MAU, Pro $25/mo,
additional MAU ~$0.00325; ~$187/mo at 100k MAU vs Clerk far higher.
https://supabase.com/pricing (search-verified 2026-07-17; corroborated by
https://gautamkhorana.com/blog/authentication-services-2026-clerk-auth0-supabase-workos/).
[^4]: Better Auth — TypeScript, in-app, users in your DB; created Sep 2024 by
Bereket Engida, YC S25, $5M seed, ~28–30k GitHub stars, 150k+ weekly npm
downloads, recommended by Next.js/Nuxt/Astro. https://www.better-auth.com/ and
https://betterstack.com/community/guides/scaling-nodejs/better-auth-vs-nextauth-authjs-vs-autho/
(search-verified 2026-07-17; two independent domains).
[^5]: Auth.js (NextAuth) fine for existing projects, not recommended for new ones
in 2026. https://workos.com/blog/top-nextauth-alternatives-secure-authentication-2026
(search-verified 2026-07-17; corroborated by
https://blog.logrocket.com/best-auth-library-nextjs-2026/).
[^6]: WorkOS — enterprise SSO/SCIM/audit logs, free for SSO+Directory Sync to a
large user count then enterprise pricing. https://workos.com/pricing
(search-verified 2026-07-17.)
[^7]: 2026 pattern: start on Clerk for speed, migrate to Supabase Auth / Better
Auth when cost becomes a line item.
https://www.buildmvpfast.com/blog/best-auth-providers-2026-clerk-supabase-comparison
(search-verified 2026-07-17; corroborated by makerkit.dev auth comparison).
[^8]: Supabase Row-Level Security docs — DB-enforced tenant isolation via
policies. https://supabase.com/docs/guides/database/postgres/row-level-security
(search-verified 2026-07-17; corroborated by PostgreSQL RLS docs,
https://www.postgresql.org/docs/current/ddl-rowsecurity.html).
[^9]: Simon Willison, "The lethal trifecta for AI agents" (2025) — private data +
untrusted content + exfiltration; no reliable general defense, defend
architecturally. https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/
(search-verified 2026-07-17; canonical home b0w02).
[^10]: OWASP Agentic AI Top 10 (2026) — agent authorization compromise, tool
misuse; real incidents (Postgres-MCP SQLi, MCP supply-chain compromise,
CVE-2025-6514). https://genai.owasp.org/ (search-verified 2026-07-17; two-source
verification recorded in `_refresh-2026-07-master-report.md` theme 3).
[^11]: The Twelve-Factor App, "Config" — strict separation of config from code,
secrets in the environment. https://12factor.net/config (search-verified
2026-07-17.)
[^12]: SOC 2 Type II readiness basics (access control, encryption, monitoring,
incident response); automation via Vanta/Drata.
https://www.vanta.com/resources/soc-2-compliance (search-verified 2026-07-17;
corroborated by https://drata.com/grc-central/soc-2).

_last_verified: 2026-07-17_
