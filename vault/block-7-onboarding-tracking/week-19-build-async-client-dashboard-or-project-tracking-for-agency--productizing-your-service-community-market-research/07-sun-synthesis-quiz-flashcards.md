---
type: lesson
block: block-7-onboarding-tracking
week: week-19
session_slug: synthesis-quiz-flashcards
day_of_cycle: 7
day_name: sun
date_due: 2026-09-27
tags:
  - synthesis
  - quiz
  - flashcards
  - review
sources:
  - supabase-rls-docs
  - manyrequests-productized-guide
  - jonathanstark-value-pricing-productized
  - reddit-responsible-builder-policy
  - vendasta-ai-workforce-margins
last_verified: 2026-07-17
word_count_target: 3200
---

# Synthesis, quiz, and flashcards

## The week as one model

Week 19 was one idea in three faces: **turn a business that depends on you being
in the room into a system that runs.** Each face removes you from a loop that was
taxing your attention.

- **The async client dashboard** removes you from the *status loop*. Transparency
  substitutes for meetings: when the state of the work is always visible, the
  standing status call becomes redundant, and the "where are we?" tax (often
  tens of thousands of dollars a year of your capacity) disappears. The build-vs-
  buy call is real; for a few clients, buy and retire the meeting.

- **The productized service** removes you from the *delivery loop*. Fixed scope,
  fixed price, standardized delivery, and AI on the low-judgment steps let the work
  happen without you touching every deliverable. But efficiency is not
  scalability: you still hit a capacity ceiling, and the honest capacity model
  (verification hours included) tells you where it is and which lever moves it.

- **Community-driven market research** removes you from the *what-to-build-next
  loop*. An audience treated as a standing research instrument hands you real
  problems in real buyer language, continuously, for the price of genuine
  participation. It aims; formal validation fires.

The through-line under all three is the same primitive you have now built by hand:
**structured data plus a thin, grounded AI layer plus a human quality gate.** The
dashboard is client-scoped data plus a grounded summary plus your approval. The
productized service is an SOP plus AI on the mechanical steps plus your judgment
gate. The community research is systematic capture plus AI clustering plus your
disconfirming questions. In every case, AI does the low-judgment volume and you
own the gate. That pattern is the whole block.

## How the four debates resolve

1. **Build vs buy the client portal.** Buy for a handful of clients (Seibel's
   default); the build in this week is a learning vehicle and an option you own.
   The decision axis that most often forces the call is data permissions: a shared
   Notion cannot isolate clients, so multiple clients rule it out.

2. **Productized vs custom vs product.** Not a universal winner. Productize when
   the outcome is standardizable and buyers are numerous and similar; value-price
   (Jonathan Stark's case) when outcome value varies enormously by buyer; build
   product only after the service taught you what to build. A mature business runs
   more than one.

3. **AI-augmented margins: real or hype.** The efficiency gain is real; the margin
   is not free. Verification cost is the term the hype omits, and the flagship
   solo productized business (DesignJoy) *declined* in revenue at its capacity
   ceiling. Build the boring eval-and-gate layer and you get a real, defensible
   margin improvement, just not the 60–80% fantasy.

4. **Community-as-research vs formal research.** Complementary instruments with
   opposite biases. Community listening is cheap, broad, hypothesis-generating;
   formal interviews and smoke tests are rigorous, hypothesis-testing. Use the
   community to aim, formal validation to fire. Either alone is a failure mode.

## What connects to the rest of the program

This week sits on the Block 4–6 spine and hands forward to the rest of Block 7.
Packaging and scope came from
[[block-4-test-validate-package/week-09-packaging-selling-your-ai-agents--create-your-first-sellable-agent-package/02-tue-package-design-scope-tiers-guarantees|Week 9]];
the multi-tenant auth and data patterns from
[[block-5-product-building-principles/week-14-analytics-iteration-what-to-measure--scale-infra-auth-db-ui-polish/04-thu-auth-and-security-for-real-users|Week 14]];
the grounded-AI-feature discipline from
[[block-5-product-building-principles/week-13-making-your-product-feel-magic-with-ai--how-to-add-smart-features-that-wow-users/04-thu-reliability-of-magic|Week 13]];
the validation half of the research funnel from
[[block-4-test-validate-package/week-11-define-your-product-idea-validate-idea-using-ai--market-user-validation-interview-or-poll-potential-users/03-wed-interviews-that-dont-lie-to-you|Week 11]];
the eval discipline behind the quality gate from
[[block-2-ai-employees/week-04-building-a-sales-agent--building-comprehensive-rag-ai-agent/06-sat-rag-evaluation|Week 4]];
and the consent line for community data from
[[block-3-advanced-topics-voice/week-08-automation-agent-integration-mcps--build-hybrid-agent-scraper-summarizer/03-wed-the-scraping-stack-legally-and-technically|Week 8]].
The SOP library you started Thursday is the input to the rest of Block 7's
onboarding-and-tracking systems.

---

## Quiz (13 questions)

Take it cold, without re-opening the lessons. Aim for 80%+.

**Q1.** Why does a client chase status, according to Monday, and what does the
dashboard actually substitute for?

**Q2.** Name the four sections every client dashboard must show, and say which one
is described as the highest-leverage and least-built.

**Q3.** A solo operator wants to run a client portal for six clients on one shared
Notion workspace. What is the specific technical reason this is a bad idea?

**Q4.** In the multi-tenant access model, why must data isolation live in the
database layer rather than the application layer? Name one concrete mechanism.

**Q5.** The AI status summary should "assemble facts deterministically and let the
model only phrase them." What failure does this design prevent, and why is it
especially bad on a client dashboard?

**Q6.** Multiple choice. Which is the correct posture for an AI-generated,
client-facing status summary in v1?
(a) Auto-send it to the client on a schedule.
(b) Generate it as a draft the operator approves before the client sees it.
(c) Let the client trigger it themselves and trust the model.
(d) Skip the AI and always hand-write it.

**Q7.** Define a productized service in one sentence, and give the specific
contrast with how a traditional agency handles scope and price.

**Q8.** Jonathan Stark argues productized services and value pricing are "not
combinable on the same offering." What is his reason, and when is he right that you
should value-price instead of productize?

**Q9.** The lesson says "efficiency is not scalability." Explain the difference,
and use the DesignJoy revenue trajectory as the example.

**Q10.** In the capacity model, what is the term the "one person does the work of
five" margin stories omit, and where does that cost come from?

**Q11.** Multiple choice. Your capacity model shows verification hours are 60% of
your delivery hours per client and you are over capacity. Which lever does the
model recommend first?
(a) Raise price only.
(b) Push the quality gate onto AI to cut verification.
(c) Add a subcontractor to run the SOP while you own the quality gate.
(d) Do nothing; you are fine.

**Q12.** Why are community research and formal interviews described as
"complementary instruments with opposite biases"? Give the bias of each.

**Q13.** Under Reddit's Responsible Builder Policy, which of these is clearly
allowed and which needs approval: (a) a human reading public subreddits and taking
notes for their own market research, (b) automated scraping of Reddit content to
build a commercial data product?

---

## Answer key

**A1.** A client chases status because silence reads as risk: absent information
gets filled with the worst story (forgotten, underwater, deprioritized). The
dashboard substitutes *visibility* for the status meeting; trust-through-visibility
replaces trust-through-contact, and the latter does not scale.

**A2.** Progress, Deliverables, Metrics, Next steps. The highest-leverage,
least-built is the "blocked on you" part of Next steps, because client-side delay
is the top hidden cause of blown timelines and a dated visible record ends the
"you never told me" argument.

**A3.** Notion does not support row-level permissions: sharing a database means
every invited guest sees every record, so you cannot show Client A only their
projects while hiding Client B's. Fine for one client, a data-leak risk at scale.

**A4.** Application-layer filtering (remembering `WHERE client_id = ?` on every
query) fails the moment one query forgets, leaking data. Database-layer isolation
fails closed. Mechanism: PostgreSQL Row-Level Security with a policy matching the
row's `client_id` against a JWT `client_id` claim.

**A5.** It prevents the model from inventing progress that did not happen
(hallucination). On a client dashboard this is especially bad because the surface's
entire job is trust, and a summary that claims false progress is a trust-destroying
lie to a paying client.

**A6.** (b). Client-facing AI content starts human-in-the-loop; you are the eval
layer until the feature earns trust.

**A7.** A productized service is a service sold like a product: fixed scope, fixed
price, standardized workflow, usually a published price. Contrast: a traditional
agency creates a custom scope and custom price for every client, requiring
discovery, a proposal, and a negotiation on every sale.

**A8.** A productized service requires a *published* price; value pricing requires
a *conversation* to discover a specific buyer's willingness to pay, so you cannot do
both on one offer. He is right to value-price when outcome value varies enormously
across buyers (a published price on a $500K-value outcome leaves money on the
table); productize when outcomes and value are similar across many buyers.

**A9.** Efficiency is margin per unit of delivery (productization + AI improve it);
scalability is whether revenue grows without your labor growing. A productized
service you still deliver is efficient but not scalable, still capped by your
capacity. DesignJoy was highly efficient (solo, ~$3.1M ARR in 2024) yet revenue
*declined* to ~$1.7M in 2025 at its one-person capacity ceiling.

**A10.** Verification cost: the human time to check AI-generated output, which has
a real defect rate (~45% vulnerability rate cited for AI-generated code). The cost
moves from production to verification rather than disappearing, and verification is
often the larger term.

**A11.** (c). When verification dominates hours, you cannot safely automate the
quality gate, so you add capacity via a subcontractor running the SOP while you own
the gate. (Below ~40% verification share, the model instead recommends price or
more AI.)

**A12.** Community research is unprompted, high-volume, and in real buyer language,
but biased toward loud/extreme voices and self-selected members (over-represents
the engaged, silent on willingness-to-pay). Formal interviews are rigorous and can
test willingness-to-pay, but are slow, small-sample, and biased by who agrees to
talk and by your framing. Opposite biases, so use both.

**A13.** (a) is clearly allowed: manual human reading for your own research is the
researcher use case the policy supports. (b) needs approval and a paid data
agreement: the policy prohibits commercializing Reddit data (and training ML on it)
without written approval.

**Scoring:** 12–13 correct, you are fluent. 10–11, re-read the weakest lesson. Below
10, redo the week's reflection questions before the live session.

---

## Flashcards

Q: What does an async client dashboard substitute for, and why does that work?
A: Visibility substitutes for status meetings. When work state is always legible,
the standing status call becomes redundant (the GitLab/Doist async principle).

Q: The four sections of a client dashboard?
A: Progress, Deliverables, Metrics, Next steps.

Q: The highest-leverage, least-built dashboard element?
A: The "blocked on you" list, surfacing client-side delay as a dated visible
record.

Q: Why does silence from a service provider read as risk to a client?
A: Absent information gets filled with the worst story; the "where are we?" email
is the client buying down that anxiety at the cost of your time.

Q: Trust-through-contact vs trust-through-visibility?
A: Contact (weekly calls) costs a meeting per client and does not scale; visibility
(a dashboard) is a one-time build that scales to every client.

Q: Why can't a shared Notion be a multi-client portal?
A: No row-level permissions; every guest on a shared database sees every record.

Q: The default build-vs-buy call for a handful of clients?
A: Buy (Assembly / ManyRequests / SPP), retire the status meeting, build later if
you outgrow it. Building is a learning vehicle at this scale.

Q: Why enforce tenant isolation in the database, not the app?
A: App-layer filters fail the moment one query forgets `WHERE client_id`; database
isolation (RLS) fails closed.

Q: The six-step Supabase RLS pattern?
A: Enable RLS on every exposed table; put tenant in the JWT; policy matches
`client_id` to the JWT claim; index the RLS column; test from the client SDK; never
ship the service_role key to the frontend.

Q: Why test RLS policies from the client SDK, not the SQL editor?
A: The SQL editor runs privileged and bypasses RLS; a policy that looks right there
can be wide open in production.

Q: The grounding rule for an AI status summary?
A: Assemble facts deterministically in code; let the model only phrase them, so it
cannot invent progress.

Q: Correct v1 posture for AI-generated client-facing content?
A: Draft that the operator approves before the client sees it; you are the eval
layer.

Q: Right model tier for a bounded status-summary task?
A: A cheap, fast tier (e.g., Haiku 4.5 / Sonnet 5), not a frontier reasoning model.

Q: Define a productized service.
A: A service sold like a product: fixed scope, fixed price, standardized workflow,
usually a published price.

Q: The three productized models by operational intensity?
A: Fixed-scope project → retainer → unlimited subscription.

Q: 2026 pricing bands for productized services?
A: Retainers ~$1.5K–$10K/mo; unlimited subscriptions ~$3K–$15K/mo; solo design
subs ~$2.5K–$7.5K/mo.

Q: The three stages of removing the founder from delivery?
A: Templatize → systematize with AI → delegate the process (not the outcome).

Q: The vacation test for a productized business?
A: Could you take a two-week vacation without delivery stopping? If not, you have a
productized job, not a productized business.

Q: Efficiency vs scalability?
A: Efficiency is margin per unit of delivery; scalability is revenue growth without
labor growth. Productization improves efficiency, not necessarily scalability.

Q: What does DesignJoy's 2024→2025 revenue decline illustrate?
A: Even the flagship solo productized service hit the capacity ceiling its
one-person structure guarantees; efficiency is not scalability.

Q: Jonathan Stark's objection to productizing?
A: Productized (published price) and value pricing (price after a conversation) are
different and not combinable; publish a fixed price and you leave money on
high-value, high-variance outcomes.

Q: The five parts of a delivery SOP?
A: Trigger, Inputs, Steps, Quality gate, Output/handoff (each step annotated
code | llm | human).

Q: The term the AI-margin hype omits?
A: Verification cost, the human time to check AI output at its real defect rate.

Q: The AI-generated-code defect signal cited this week?
A: ~45% vulnerability rate, the basis for the "agentic engineering with a review
gate" reframe.

Q: The honest AI-agency margin verdict?
A: The efficiency gain is real but the margin is not free; 60–80% headline figures
are vendor-adjacent and omit verification and churn.

Q: The capacity-model inputs people get wrong?
A: They under-count delivery hours (forget verification) and over-count available
hours (ignore sales/admin/support).

Q: When does the capacity model recommend a subcontractor over price/AI?
A: When verification dominates delivery hours (you can't safely automate the
quality gate), add a subcontractor to run the SOP while you own the gate.

Q: Community research vs formal interviews — the role of each?
A: Community aims (cheap, broad, hypothesis-generating, real buyer language);
formal validation fires (rigorous, tests willingness-to-pay).

Q: The bias of community research?
A: Over-represents loud/extreme, self-selected engaged members; silent on
willingness-to-pay.

Q: "Give before take" in community research?
A: Contribute genuine value for weeks before extracting; it protects signal quality
(members stay candid) and is also your cheapest customer acquisition.

Q: The single best defense against research theater?
A: Write listening questions in advance, including at least one that could
disconfirm your offer.

Q: What does Reddit's Responsible Builder Policy allow vs restrict?
A: Manual human reading for your own research is allowed; commercializing Reddit
data or training ML on it needs written approval and a paid agreement; inferring
sensitive traits or de-anonymizing users is prohibited.

Q: The 2026 creator-community platform landscape?
A: Skool (Hormozi 2024 investment, Skool Games) and Circle (~$200M valuation,
powers Adobe communities) are the two dominant platforms.

Q: The one primitive underlying all three artifacts this week?
A: Structured data + a thin grounded AI layer + a human quality gate.

_last_verified: 2026-07-17_
