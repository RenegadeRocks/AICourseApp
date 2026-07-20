---
type: lesson
block: block-5-product-building-principles
week: week-14
session_slug: analytics-iteration-what-to-measure
day_of_cycle: 2
day_name: tue
date_due: 2026-08-18
tags:
  - instrumentation
  - event-taxonomy
  - posthog
  - amplitude
  - llm-observability
  - langfuse
  - braintrust
  - session-replay
  - privacy-by-design
  - opentelemetry
sources:
  - posthog-vs-amplitude-2026
  - amplitude-taxonomy-playbook-2024
  - langfuse-braintrust-pricing-2026
  - langfuse-otel-genai-2026
  - posthog-gdpr-compliance-2026
  - justanalytics-session-replay-gdpr-2026
  - otel-genai-semconv-2026
  - eu-ai-act-transparency-2026
  - hamel-husain-evals-faq-2026
  - simonwillison-llm-logging-2025
last_verified: 2026-07-17
word_count_target: 5300
---

# Instrumentation & the analytics stack: two pipes, one taxonomy, no lawsuits

## Why this matters

Monday you decided *what* to measure. Today you wire it, and you make two
decisions you will live with for a year: your event taxonomy (the vocabulary
every future metric is built from) and your stack (product analytics on one
pipe, LLM observability on the other). Get the taxonomy wrong and every
downstream chart is built on sand. Get the privacy design wrong and session
replay turns from an insight tool into a demand letter. Get the observability
wrong and you are debugging a hallucination in month three with no trace of what
the model actually saw.

After this lesson you can design an event taxonomy that survives a year of
feature growth, choose a product-analytics tool and an LLM-observability tool on
evidence rather than hype, wire them so a single user action is traceable across
both, and do it all in a way that will not get you fined when the EU AI Act's
transparency obligations bite on August 2, 2026.

## Prerequisites

- [[block-4-test-validate-package/week-10-build-landing-page-with-cta-recap--create-ai-generated-launch-creatives/05-fri-launch-day-instrumentation|Launch-day instrumentation]]
  is the canonical home for "how to fire your first event." We do not re-teach
  that. Today is the *system*: taxonomy, two pipes, privacy.
- [[01-mon-product-analytics-for-ai-products|Monday's metric hierarchy]]. Every
  event you design today exists to compute one of Monday's numbers. If an event
  maps to no metric, do not build it.
- [[block-3-advanced-topics-voice/week-08-automation-agent-integration-mcps--build-hybrid-agent-scraper-summarizer/05-fri-reliability-engineering-for-unattended-agents|Reliability engineering]]
  (Block 3), for the tracing mindset. LLM observability is that discipline
  pointed at production.

## Part 1 — Event taxonomy: the vocabulary you can't easily change later

An event taxonomy is the naming scheme for everything you log. It feels like
bikeshedding until you have 200 events named by six different past-selves and no
chart is trustworthy. Amplitude's taxonomy playbook makes the case plainly: a
taxonomy is a governance artifact, and the cost of fixing it rises with every
event you add on top of a broken one.[^1]

### The Object-Action convention

The convention that scales is **Object-Action**: name events `Object Action`,
where the object is a noun in your product and the action is a past-tense verb.
`Note Shared`. `Report Generated`. `Subscription Upgraded`. Not `click_share`,
not `user did thing`, not `shareNoteButtonClicked`. The Object-Action grammar
means a new engineer can guess the event name, and your event list sorts into
readable clusters by object.[^1]

Rules that prevent the sand-foundation problem:

- **Events are what happened; properties are the details.** `Report Generated`
  is the event. `{model: "sonnet-5", tokens: 1840, latency_ms: 2200,
  feature: "summary", regenerated: false}` are properties. Do not encode details
  in the event name (`Report Generated With Sonnet` is a trap; you will have
  fifty variants and no way to aggregate).
- **Track state-changes and value-moments, not UI noise.** You do not need
  `Button Hovered`. You need the events that map to Monday's metrics: activation,
  the north-star action, the six AI signals. Start with fifteen good events, not
  a hundred reflexive ones.
- **Identify accounts, not just users.** For any B2B or team product, every
  event carries an `account_id` (the org) alongside `user_id`. Monday's north
  star was per-account; if you only log per-user you cannot compute it later
  without a painful backfill.
- **Version your schema.** Keep the event dictionary in a file in your repo (a
  `tracking-plan.md` or a typed schema), reviewed in PRs. The tool's UI is where
  events *land*, not where they are *defined*. Willison's logging discipline for
  LLM apps is the same instinct: the definition of what you capture lives in
  code you can diff, not in a dashboard someone edited at 2am.[^2]

### The typed-event pattern (kills a whole class of bugs)

Define events once, in a typed module, and emit only through it. No raw string
event names sprinkled across the codebase. This is the single highest-leverage
taxonomy practice, because it makes "we renamed the event and half the app kept
firing the old name" impossible. We use exactly this pattern in Saturday's
code-lab.

## Part 2 — The product-analytics stack in 2026

You need one product-analytics tool. The 2026 decision is essentially
**PostHog vs Amplitude**, with a long tail of alternatives that mostly define
themselves against these two.

**PostHog** is the all-in-one, usage-priced, open-source-core option. Analytics,
session replay, feature flags, and A/B testing are first-class and included; you
pay per event/recording after a generous free tier (on the order of 1M analytics
events and thousands of recordings free, with no monthly-active-user cap).[^3]
For an indie builder or a team under, say, a few hundred thousand events a month,
PostHog is usually free or near-free, and having flags plus experiments plus
replay in one tool means one taxonomy, not four.

**Amplitude** is the depth option. Its behavioral-analysis, cohorting, and
experimentation tooling is more refined; its experiment product (CUPED variance
reduction, holdouts, mutually-exclusive groups, approval workflows) is rated top
of the category, and it suits organizations where non-technical stakeholders
need to self-serve insights.[^3] The cost is that flags and experiments are
priced add-ons, and paid plans climb fast (free to 50k MTUs, then Plus around
$49/mo, then custom with median contracts in the tens of thousands per
year).[^3]

> My take: at the stage of *this* course — one product, real but modest usage —
> start on PostHog. The reason is not price alone; it is that flags,
> experiments, and replay under one taxonomy lets you run Wednesday's iteration
> loop without integrating four tools. Graduate to Amplitude when you have
> analysts who live in the tool and need its depth. Do not run both; two
> taxonomies is worse than a slightly weaker single one.

The long tail is real but off-path for you today: Mixpanel (classic
event-analytics), June/Pocus (B2B-flavored), and warehouse-native stacks
(Snowflake/BigQuery + a modeling layer) for teams that already have a data
engineer. All of them assume you have already solved taxonomy. None of them
change the Object-Action discipline above.

## Part 3 — Session replay, and the ethics you cannot skip

Session replay records a user's interactions and lets you watch them back. It is
the fastest way to see *why* a funnel drops, and it is a privacy hazard with
legal teeth. This is one of the week's live controversies, so let me give you
both the "why it's great" and the "why it can bite," and then the design that
lets you have the first without the second.

The value is genuine: a two-minute replay of a confused user often teaches you
more than a week of aggregate charts. Hamel Husain's whole "look at your data"
argument extends here — watching real sessions is qualitative gold, especially
at low user counts where charts are noisy.[^4]

The hazard: replay can capture everything a user types, including PII, passwords
in mis-typed fields, chat messages, and health or financial data. Under GDPR,
JustAnalytics' field guide is clear: if your replay captures form inputs or any
text a user types, you almost certainly need *explicit opt-in consent* under
Article 6(1)(a); only if you **mask all text inputs by default** and record just
DOM structure, mouse movement, and clicks can you plausibly argue legitimate
interest under Article 6(1)(f).[^5] PostHog's own GDPR docs push you toward the
safe default: mask all inputs and text so data is captured only when explicitly
unmasked, and EU organizations default to IP capture disabled.[^6]

The design that keeps you safe:

1. **Client-side masking, on by default.** The PII must never leave the browser.
   PostHog's docs and every serious guide agree: client-side masking means you
   can truthfully say the personal data was never collected, which is a far
   stronger legal position than "we collected it and deleted it."[^5][^6]
2. **Consent gate for anything beyond structural replay.** If you unmask inputs,
   gate recording behind explicit opt-in, and keep proof of consent.
3. **Don't record sensitive surfaces at all.** Payment pages, anything under
   health/financial regulation: exclude them from replay entirely.
4. **Retention limits.** Replays are not forever. Set a short retention (30–90
   days) and honor deletion requests.

The controversy in one line: session replay is legitimate insight *or*
surveillance depending entirely on masking defaults and consent. The tool does
not decide which; you do, at config time.

## Part 4 — The second pipe: LLM observability

Product analytics tells you *that* a user regenerated three times. It does not
tell you *what the model saw, thought, cost, or returned*. That is the second
pipe: LLM observability, which captures traces (the full call tree of a
request), token counts, cost, latency, and, increasingly, in-production eval
scores. This is where you debug a hallucination, catch quality-drift (Monday's
metric 4), and watch cost-per-active-user (metric 5) at the request level.

The 2026 decision is largely **Langfuse vs Braintrust**, and it splits on
philosophy:

**Langfuse** is open-source (MIT), self-hostable, OpenTelemetry-native. It does
deep hierarchical tracing built for multi-step agent reasoning, agnostic prompt
management (with an MCP server), and flexible LLM-as-judge / remote custom
evaluators. Pricing meters "units" (a trace plus its observations and scores is
several units), free Hobby tier around 50k units, then roughly $8 per 100k
units.[^7] Choose it if you want vendor-neutral, self-hostable, predictable
unit-based pricing and OpenTelemetry standards.

**Braintrust** is proprietary, "batteries-included," and eval-loop-centric. It
bundles a model gateway with caching and failover across 100+ models, and an
integrated environment for iterating on "golden datasets" mined from your logs.
Pricing meters processed data (GB) plus evaluation scores (per 1k): a free
Starter with $10 credits/1GB/10k scores, Pro around $249/mo, overage about
$4/GB and $2.50 per 1k scores.[^7] Choose it if you want the tightest
prompt-iteration and eval loop and are willing to pay for a managed platform.

The unifying standard worth knowing: **OpenTelemetry now has GenAI semantic
conventions** for spans (model, tokens, cost, latency as standard attributes),
and Langfuse leans on them, which means you can instrument once against OTel and
keep your options open.[^8] If you are unsure, instrument with OTel GenAI
conventions and point them at Langfuse; you can re-point later without
re-instrumenting.

> My take: the honest answer for an indie AI product is that you can start with
> almost nothing — structured JSON logs of every model call (prompt hash,
> model, tokens, cost, latency, a truncated output, and an accept/reject
> signal) written to your own Postgres. That *is* observability. Willison has
> logged his LLM calls to SQLite for years and gets 80% of the value.[^2] Reach
> for Langfuse when you have multi-step agents whose traces you cannot read in a
> flat log, or when you want LLM-as-judge scoring wired in. Reach for Braintrust
> when eval iteration is your bottleneck. Do not buy a platform to avoid
> reading fifty logs by hand; that is the observability version of premature
> scaling.

## Part 5 — Wiring the two pipes together

The magic is a shared identifier. Every product-analytics event and every
LLM-observability trace for the same user action carries the same
`request_id` (or `trace_id`). Now when you see a spike in Monday's regeneration
rate on the "summary" feature in PostHog, you can pivot into Langfuse, pull the
traces for those exact requests, and read what the model actually produced. The
product pipe tells you *where* it hurts; the AI pipe tells you *why*.

The pattern:

1. Generate a `request_id` at the edge (per user action).
2. Attach it as an event property on the product-analytics event
   (`Report Generated`, `{request_id, feature, regenerated}`).
3. Attach the same id as a trace attribute on the LLM call
   (OTel `gen_ai` span, `{request_id, model, tokens, cost_usd, latency_ms}`).
4. In your model-call wrapper, also record the accept/reject signal back onto
   both, so feature-trust (Monday, metric 1) is computable on either pipe.

That is the whole integration. It is fifteen lines, and it is the difference
between "users hate the summary feature" (useless) and "the summary feature's
p95 latency tripled after we switched models, regenerations followed, here are
the transcripts" (a fix).

## Part 6 — Privacy-by-design and the regulatory clock

Two dates and one principle. The principle: **collect the minimum, mask at the
edge, and make deletion cheap.** If you never collect a piece of PII, you never
have to secure it, delete it, or explain it to a regulator.

The dates: GDPR is already live and governs everything above. The newer clock is
the **EU AI Act**, whose transparency obligations and enforcement powers for
general-purpose AI providers enter application on **August 2, 2026**.[^9] For
most readers of this course you are a *deployer* of GPAI, not a provider, so the
heaviest provider obligations are not yours — but the transparency rules (users
should know when they are interacting with AI, and AI-generated content carries
implications) are the direction of travel, and building "the user knows this is
AI and can see/delete what we stored" into your product now is cheaper than
retrofitting it under enforcement.[^9] Do not overclaim what applies to you;
do design as if transparency is mandatory, because it increasingly is.

## Worked example: the dual-pipe wrapper

This is the load-bearing 20 lines. One function that emits to both pipes with a
shared id. Stdlib-only so you can run it; swap `print` for your real SDKs.

```python
# dual_pipe.py — one action, two pipes, one id. Run: python dual_pipe.py
import uuid, time, json, hashlib

def emit_product_event(name, request_id, props):
    """Stand-in for posthog.capture(...) — the PRODUCT pipe."""
    print("PRODUCT", json.dumps({"event": name, "request_id": request_id, **props}))

def emit_llm_trace(request_id, span):
    """Stand-in for an OTel gen_ai span / Langfuse trace — the AI pipe."""
    print("LLM    ", json.dumps({"request_id": request_id, **span}))

def run_ai_feature(user_id, account_id, feature, prompt, call_model):
    request_id = str(uuid.uuid4())          # THE shared id
    t0 = time.time()
    result = call_model(prompt)             # your real model call
    latency_ms = int((time.time() - t0) * 1000)

    # AI pipe: what the model saw/did (prompt hashed, never stored raw here)
    emit_llm_trace(request_id, {
        "model": result["model"],
        "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest()[:16],
        "input_tokens": result["input_tokens"],
        "output_tokens": result["output_tokens"],
        "cost_usd": round(result["cost_usd"], 6),
        "latency_ms": latency_ms,
    })
    # Product pipe: the value-moment, joinable by request_id
    emit_product_event("Report Generated", request_id, {
        "user_id": user_id, "account_id": account_id,
        "feature": feature, "regenerated": False,
    })
    return request_id, result["text"]

def record_outcome(request_id, user_id, accepted):
    """Feature-trust signal onto BOTH pipes, joinable later."""
    emit_product_event("Report Outcome", request_id,
                       {"user_id": user_id, "accepted": accepted})
    emit_llm_trace(request_id, {"outcome_accepted": accepted})

if __name__ == "__main__":
    def fake_model(_p):
        return {"model": "sonnet-5", "text": "summary...", "input_tokens": 1200,
                "output_tokens": 300, "cost_usd": 0.0054}
    rid, _ = run_ai_feature("u_1", "acct_1", "summary", "Summarize Q3 board notes", fake_model)
    record_outcome(rid, "u_1", accepted=True)
```

**Pass bar:** running it prints four JSON lines that all share one `request_id`.
Grep that id across both pipes and you can reconstruct: which feature, which
model, what it cost, how long it took, and whether the user accepted it. If you
can do that join, you have wired steady-state analytics for an AI product. If
you cannot, no dashboard will save you later.

## Common mistakes experts see

1. **Encoding properties into event names.** `Report Generated With Sonnet` gives
   you fifty un-aggregatable events. Object-Action name, everything else a
   property.[^1]
2. **Logging users but not accounts.** Monday's per-account north star becomes
   uncomputable without a painful backfill. Always carry `account_id`.
3. **Session replay with default-unmasked inputs.** That is the config that
   turns replay into a GDPR liability. Mask at the client by default; consent for
   anything more.[^5][^6]
4. **One pipe only.** Product analytics without LLM traces means you see the
   symptom and can never read the cause. Two pipes, one shared id.
5. **Buying a platform to avoid reading logs.** Fifty structured logs read by
   hand beat a $249/mo dashboard you configured and never open.[^2][^4]
6. **Defining events in the tool's UI.** The dictionary lives in the repo,
   reviewed in PRs. UIs get edited at 2am and drift silently.

## Reflection questions

1. Write five of your product's events in Object-Action form. Which detail did
   you almost put in the name that belongs in a property?
2. For your product, what exactly would session replay capture that would need
   consent? Which surfaces would you exclude entirely?
3. If you saw a regeneration spike in your product pipe, what is the exact
   sequence of clicks to reach the offending transcripts? If you can't answer,
   your two pipes are not wired.
4. Langfuse or Braintrust or a Postgres JSON log — which fits *your* current
   bottleneck, and what would have to change for the answer to change?
5. What is one piece of PII your product collects that it does not actually
   need? What breaks if you stop collecting it today?

## My take (reviewer lens)

**Hamel Husain** would say the whole tool debate is a distraction from the one
habit that matters: open twenty real traces and read them, with a spreadsheet,
before you buy anything.[^4] He is right that the highest-leverage instrument
early is a human with a spreadsheet, and I have tried to honor that by keeping
the "start with Postgres logs" path first-class. Where I would push back on a
naive reading of Hamel: at multi-step-agent complexity, flat logs genuinely stop
being readable, and *then* Langfuse's hierarchical traces earn their keep. The
skill is knowing which regime you are in.

**Simon Willison** would like the "log everything to your own store" default and
would warn about a specific footgun I glossed: it is dangerously easy to log raw
prompts and outputs that contain user PII into your observability store, which
then becomes the *least* secured copy of your most sensitive data.[^2] Hash or
redact at the logging boundary, not after. I flagged it in the wrapper (prompt
hashed) but he would want it louder.

**Boris Cherny** would point at the taxonomy-in-code discipline and note the real
failure is drift between the typed event module and what the tool actually
receives — nobody notices when a property silently stops being sent. His fix is a
contract test that fails CI if the emitted shape diverges from the schema. That
is exactly the kind of thing Saturday's code-lab should (and does) include.

## Further reading

**Must-read**

- Amplitude, "Data Taxonomy Playbook." The governance case for Object-Action and
  a versioned tracking plan.[^1]
- Langfuse docs on OpenTelemetry GenAI conventions, for instrument-once
  portability.[^8]

**Recommended**

- PostHog GDPR compliance docs, for the masking-by-default posture.[^6]
- JustAnalytics, "GDPR-Safe Session Replay," for the Article 6 legal-basis
  distinction.[^5]

**Optional**

- Braintrust vs Langfuse comparisons (2026), to sanity-check pricing against your
  own volume.[^7]

## Citations

[^1]: Amplitude, "Data Taxonomy Playbook" / event-naming best practices —
Object-Action convention, events-vs-properties, tracking plan as governance.
https://amplitude.com/blog/data-taxonomy-playbook (search-verified 2026-07-17;
corroborated by PostHog's own event-naming guidance,
https://posthog.com/docs/product-analytics/best-practices).
[^2]: Simon Willison on logging LLM calls to a local store (SQLite/`llm` tool)
and redacting sensitive data at the boundary. https://simonwillison.net/tags/llm/
(search-verified 2026-07-17; consistent with his `llm` CLI logging docs at
https://llm.datasette.io/).
[^3]: PostHog vs Amplitude comparison (2026) — PostHog usage-priced all-in-one
(analytics+replay+flags+experiments included, ~1M events free); Amplitude depth
+ add-on-priced experiments, free to 50k MTUs then paid.
https://posthog.com/blog/posthog-vs-amplitude and
https://amplitude.com/compare/posthog (search-verified 2026-07-17; two
independent domains).
[^4]: Hamel Husain, "Your AI Product Needs Evals" / evals FAQ — look at your
data; read real traces before instrumenting heavily.
https://hamel.dev/blog/posts/evals/ (search-verified 2026-07-17.)
[^5]: JustAnalytics, "GDPR-Safe Session Replay: A Field Guide to PII Masking and
Lawful Basis" (2026) — Article 6(1)(a) consent vs 6(1)(f) legitimate interest;
client-side masking. https://justanalytics.app/blog/gdpr-session-replay-pii-masking-guide
(search-verified 2026-07-17; corroborated by PostHog GDPR docs below.)
[^6]: PostHog, "GDPR compliance" and "Controlling data collection" docs —
mask-all-inputs default, EU orgs default IP capture off.
https://posthog.com/docs/privacy/gdpr-compliance (search-verified 2026-07-17.)
[^7]: LLM observability pricing (2026): Langfuse (MIT, self-hostable,
OTel-native, unit-metered, ~50k-unit free tier, ~$8/100k units) vs Braintrust
(proprietary, eval-loop-centric, GB+scores metered, Starter free, Pro ~$249/mo).
https://langfuse.com/pricing and https://www.braintrust.dev/ plus
https://aibizhub.io/articles/llm-observability-pricing-braintrust-vs-phoenix-vs-langfuse-2026/
(search-verified 2026-07-17; multiple domains).
[^8]: Langfuse OpenTelemetry / GenAI semantic-conventions integration.
https://langfuse.com/docs/opentelemetry/get-started (search-verified 2026-07-17;
corroborated by OpenTelemetry GenAI semantic-conventions spec,
https://opentelemetry.io/docs/specs/semconv/gen-ai/).
[^9]: EU AI Act implementation timeline — from 2 Aug 2026 the Commission's
enforcement powers for GPAI providers and transparency/high-risk obligations
enter application. https://artificialintelligenceact.eu/implementation-timeline/
and https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai
(search-verified 2026-07-17; two official/authoritative sources).

_last_verified: 2026-07-17_
