---
type: lesson
block: block-5-product-building-principles
week: week-13
session_slug: how-to-add-smart-features-that-wow-users
day_of_cycle: 3
day_name: wed
date_due: 2026-08-12
tags:
  - generative-features
  - personalization
  - editable-output
  - structured-outputs
  - generative-ui
  - model-routing
  - cost-latency-tradeoffs
sources:
  - structured-outputs-reliability-2026
  - google-a2ui-v09-2026
  - mcp-apps-2026
  - ag-ui-protocol-2026
  - anthropic-building-effective-agents-2024
  - master-report-model-lineup-2026
  - granola-recipes-2026
  - chartmogul-ai-churn-wave-2026
last_verified: 2026-07-17
word_count_target: 5600
---

# Generative and personalization features: in-product creation without losing the driver's seat

## Why this matters

The two most common magical features you will ship are *generation* (the product
makes something for the user: a draft, a transform, a summary) and
*personalization* (the product tailors itself to this user). Both are easy to
demo and easy to get wrong. Generation fails when the output is generic slop the
user rewrites; personalization fails when it contaminates your context, leaks
across users, or reads as creepy. This lesson is the craft of building both so
the human stays in the driver's seat, the output is structured enough to drive
real UI, and the cost/latency is controlled at the granularity of each feature.
On Saturday, if your feature generates or personalizes anything, this is the
lesson you will reach back for.

## Prerequisites

- [[01-mon-what-magic-actually-is|Monday]] (effort-collapse vs displacement) and
  [[02-tue-the-proactive-ambient-pattern|Tuesday]] (rungs, trust). Generation is
  usually rung 1–3.
- Memory and personalization-from-user-data are canonical in
  [[02-tue-memory-and-compaction-architectures|Block 3 Week 6]]. We use memory
  as a component here; we do not re-teach compaction or retrieval.
- Structured outputs driving downstream systems are canonical in
  [[05-fri-report-generation-patterns|Block 2 Week 5]]. Here we point them at UI
  instead of reports.

## Part 1 — In-product generation, and the editable-output pattern

### The core move: generate a starting point, not an answer

The single most important design decision in any generative feature is whether
the output is a *starting point the user edits* or a *final answer the user
accepts*. For almost every feature you will build, the answer is starting point,
and building it that way is what separates magic from slop.

Why: the jagged frontier from [[01-mon-what-magic-actually-is|Monday]] guarantees
that some fraction of generations will be wrong, generic, or off-target. If the
output is framed as a final answer, every one of those failures is a visible
product failure that the user has to catch and fix, and catching-and-fixing is
often more work than doing it themselves — the effort-displacement trap. If the
output is framed as an editable starting point, the same failures are just "a
draft I improved," which is how humans already work with first drafts. The
framing converts the model's inevitable imperfection from a bug into a feature.

This is the **editable-output pattern**, and it has a specific shape:

1. **Generate into an editable surface**, not a read-only display. The draft
   appears in the same text field, canvas, or form the user would have filled
   themselves. There is no "accept/reject" gate between the generation and the
   editing; the user just starts editing.
2. **Make the generated content visually distinct until touched.** Like
   ghost-text's grey, signal "this is a draft" so the user knows what to trust,
   then let their edits promote it to "mine."
3. **Preserve a one-action regenerate and a one-action revert.** Cheap to try
   again, cheap to undo, so experimentation costs nothing.
4. **Never destroy user work to insert a generation.** If the field has content,
   generation augments or offers alongside; it does not overwrite. Overwriting
   user work is the fastest way to make a generative feature feel hostile.

Granola's Recipes are a clean instance: a Recipe generates structured notes into
your document, and you edit from there; the AI produced the scaffold, you own the
result.[^1] The magic is that the blank-page cost vanished while your authorship
did not.

### Keeping the human in the driver's seat

"Human in the driver's seat" is not a slogan; it is a set of concrete
constraints that you either build or do not:

- **The human initiates or can trivially decline.** Generation is rung 1–3
  (offered), not rung 4 (done and shipped). A drafted reply is not a sent reply.
- **The human sees the inputs.** If the generation used the contact's history,
  the last three messages, or a knowledge-base article, that provenance is
  visible. This is Tuesday's legible-context rule applied to generation.
- **The human's edit is the source of truth.** The moment the user touches the
  output, their version wins and the model does not silently re-run and clobber
  it.
- **The human can always do it manually.** The generative feature sits *beside*
  the manual path, never replacing it. A user who distrusts the draft can ignore
  the button entirely and lose nothing.

These constraints cost engineering effort and they are the difference between a
feature users keep and one they disable. The retention data punishes generative
features that take the wheel and produce work the user did not sanction.[^2]

## Part 2 — Personalization without contamination

Personalization means the product behaves differently for this user based on
what it knows about them. Done well, it is deep magic: the product feels like it
was built for you. Done badly, it produces three specific failures, and avoiding
those three is most of the craft.

### Failure 1 — Context contamination

You stuff a user's history, preferences, and past outputs into the prompt, and
the accumulated context starts to *degrade* generation rather than improve it:
stale preferences override current intent, one strong past example dominates,
irrelevant history dilutes the signal. This is a context-engineering problem, and
the discipline lives in
[[01-mon-context-engineering-the-successor-discipline|Block 3 Week 6]]. The
product-feature-level rule: **personalize with the smallest sufficient context,
retrieved for relevance to the current task, not the largest available.** More
user data in the prompt is not more personalization; past a point it is noise
that makes the feature worse and more expensive.

### Failure 2 — Cross-user leakage

The catastrophic failure: user A's data appears in user B's generation. This
happens through shared caches, mis-scoped retrieval indexes, prompt templates
that accidentally share state, or a memory store keyed wrong. It is a security
and privacy incident, not a quality bug, and it will end a product's
credibility. The rule: **every retrieval, cache, and memory lookup is scoped to
a user (or org) identity that is verified server-side, never trusted from the
client.** Test this explicitly with an adversarial eval (Thursday): can you
construct an input as user B that surfaces user A's data? If you have not tried,
assume you are vulnerable.

### Failure 3 — Creepy personalization

Covered Tuesday, applied here: personalization built on *inferred* traits
(mood, intent, sensitive attributes) or on *cross-context* data the user did not
know you had reads as surveillance. NNG and Nielsen both flag over-personalization
as a 2026 trust hazard; the CDT taxonomy names "data and memory exploitation" as
a dark-pattern category.[^3] The rule: **personalize on what the user explicitly
gave you for this purpose, surface the basis, and prefer chosen preferences over
inferred ones.** A "you seem stressed" nudge is creepy; a "you set your tone
preference to concise" default is not.

### Memory is the substrate, and it is canonical elsewhere

Personalization that persists across sessions needs memory, and memory
architecture (what to store, when to compact, how to retrieve) is fully covered
in [[02-tue-memory-and-compaction-architectures|Block 3 Week 6]]. The product
decision on top of that machinery is *what is worth remembering at all*. Default
to remembering explicit, durable preferences (tone, format, recurring entities)
and forgetting transient context. A memory that stores everything is a
context-contamination and creepy-personalization machine; a memory that stores
the few stable preferences a user would happily state out loud is a magic
machine. The product taste is in the curation, not the storage.

## Part 3 — Structured outputs that drive UI

A generation that produces a wall of text can only ever be a text feature. A
generation that produces *structured* output can drive real interface: fill a
form, render a card, populate a table, configure a chart, propose a set of
actions the user clicks. Structured outputs are how generation escapes the chat
box and becomes a native feature. The machinery is canonical in
[[05-fri-report-generation-patterns|Block 2 Week 5]]; here is what is specific to
driving UI.

### Reliability in 2026 is good, with a real caveat

As of 2026, structured output is close to a solved reliability problem for teams
using the right tools. OpenAI's Structured Outputs (constrained decoding against
a JSON schema) reports failure rates under 0.1%; Anthropic's tool-use approach
is a close second at under 0.2%, relying on very strong instruction-following
rather than hard-constrained decoding.[^4] The caveat that matters for UI:
Anthropic returns its structured result in a single block at the end of the
stream, so you cannot parse fields progressively; if your feature wants to render
UI *as* fields arrive (a form filling in live), OpenAI or Gemini's streaming
structured output is the better fit, and you should know this before you pick a
model for a specific feature.[^4] Whatever the provider, validate the output
against your schema on your side (Zod in TypeScript, Pydantic in Python) and have
a fallback for the sub-1% that fails validation — never render un-validated model
output directly into UI.

### The two ways to drive UI from a model

**Static generative UI (recommended default).** You pre-build the UI components,
and the model's structured output decides *which* component appears and *what
data* it gets. The model returns `{type: "conflict_card", deal_id, reason,
suggested_action}`; your React app renders your own trusted `ConflictCard`. The
model never emits markup or code. This is safe, testable, on-brand, and covers
the overwhelming majority of product features. Start here and usually stay here.

**Declarative generative UI (the 2026 frontier, use deliberately).** The model
returns a declarative *description* of an interface, and a renderer turns it into
your native components. Google open-sourced A2UI as a public project in early
2026 and shipped v0.9 in July 2026: agents send declarative component
descriptions ("a form with a name field, an email field, a submit button") that
clients render with their own design-system widgets, with the client holding a
*catalog of trusted, pre-approved components* so the agent can only request
what you have vetted.[^5] In parallel, the MCP ecosystem shipped MCP Apps
(building on MCP-UI and OpenAI's Apps SDK) to bring UI capabilities into MCP
clients like ChatGPT, Claude, and VS Code, and AG-UI emerged as the runtime
streaming layer that carries these UI events between agent and app.[^6][^7] These
matter when your product is *inside* an agent surface, or when the space of
possible UIs is too large to pre-build. For a standalone Week-12 web app,
declarative generative UI is usually more than you need in v1; know it exists,
reach for it when static components genuinely cannot express the range.

> My take: the "the agent builds the whole interface on the fly" pitch is the
> most over-hyped idea in this space. For 95% of product features, static
> generative UI (model picks a component, you render it) delivers all the magic
> with none of the injection surface, the brand drift, or the un-testability of
> model-emitted markup. Declarative gen-UI is real and improving fast, but treat
> it as a capability for a specific class of problem, not the future of all
> frontends.

## Part 4 — Cost and latency at feature granularity

Every generative and personalization feature has a per-invocation cost and
latency, and the discipline that separates a sustainable product from a
money-losing one is making those choices *per feature*, not globally. The
current model landscape gives you a wide ladder to route across.[^8]

The 2026 lineup you are routing among (verified current):[^8]

- **Claude Haiku 4.5** — cheapest, fastest; the workhorse for high-frequency,
  low-stakes features (autocomplete, classification, smart defaults).
- **Claude Sonnet 5** — the new default (intro $2/$10 per Mtok), the sensible
  middle for most generation.
- **Claude Opus 4.8** ($5/$25 per Mtok) — for the hard, low-frequency generations
  where quality is the product.
- **Claude Fable 5 / Mythos 5** ($10/$50 per Mtok, 1M context) — the top tier,
  reserved for the rare feature that genuinely needs it.
- Note the tokenizer change on Opus 4.7+/Sonnet 5/Fable: roughly +30% tokens for
  the same text, so re-baseline any cost math you carried over from earlier
  models.[^8]

The routing principles:

1. **Match model to feature stakes and frequency.** A ghost-text suggestion fires
   thousands of times a day and tolerates being occasionally mediocre; route it
   to Haiku. A once-a-week board summary fires rarely and must be excellent;
   route it to Opus or Fable. Using Opus for autocomplete is how you turn a
   loved feature into a line item that eats your margin.
2. **Cache what repeats.** Prompt caching on stable prefixes (system prompt,
   retrieved context that does not change per request) cuts cost and latency
   substantially for features that re-use context. Personalization contexts and
   RAG prefixes are prime candidates.
3. **Do the cheap deterministic thing first.** If a smart default can be computed
   without a model call (the most common category, last month's value, a rule),
   do that and reserve the model for the cases the rule cannot handle. The
   cheapest generation is the one you did not make.
4. **Budget latency per rung.** A rung-0 default must be instant (so precompute or
   use a rule). A rung-3 "we did this for you" digest can take seconds because
   the user did not initiate it. Spend latency where the user is not waiting.
5. **Measure cost per successful task, not per call.** A cheaper model that fails
   and forces a retry or a human fix is more expensive than a pricier model that
   succeeds. This is Friday's frontier, previewed: the right metric is
   fully-loaded cost per magical outcome.

## The context budget: a worked accounting

"Smallest sufficient context" and "route by stakes and frequency" are principles;
here is the arithmetic that turns them into decisions, because the difference
between a sustainable feature and a money-loser is usually a few thousand tokens
you did not need to send.

Take the draft-follow-up feature at a realistic scale: a freelancer with 200
active deals, of which 30 go quiet in a given week. Consider two designs for the
context you send per draft.

**The lazy design** stuffs everything: the full message history of the deal (say
2,000 tokens), the user's entire profile and all past drafts (3,000 tokens), a
large system prompt with ten few-shot examples (2,500 tokens), plus the deal
metadata (500 tokens). That is roughly 8,000 input tokens per draft. It feels
"more personalized." It is mostly noise: past drafts for *other* deals dilute the
signal, and ten few-shot examples past the third add little. The generation is
both worse (context contamination) and more expensive.

**The disciplined design** sends the last three messages of *this* deal (600
tokens), the user's one saved tone preference (50 tokens), a tight system prompt
with two few-shot examples (900 tokens), and the deal metadata (200 tokens).
Roughly 1,750 input tokens, a bit over a fifth of the lazy design, and the
generation is *better* because the signal is not buried.

Now apply the two levers from the routing section. First, **prompt-cache the
stable prefix**: the system prompt, the few-shot examples, and the tone spec do
not change between the 30 drafts in a batch, so caching them means you pay full
price for that prefix once and a fraction on each subsequent call. Second, **do
the cheap deterministic thing first**: the detection (which deals are quiet) is a
database query, not a model call, so you only pay for generation on the 30 deals
that qualify, not all 200.

The numbers move the feature from "an expensive novelty I might disable" to "a
line item I barely notice." The exact costs will shift with the tokenizer change
(re-baseline for the ~+30% tokens on current models) and with your model
choice.[^8] The point is not the arithmetic itself but the habit: **every feature
has a per-invocation context budget, and you set it deliberately by asking what is
the smallest context that makes the generation good, not the largest context you
happen to have.** Teams that never do this accounting ship features whose unit
economics quietly go negative at scale, which is the Wednesday version of the
Friday churn story.

## Worked example — spec a generation feature end to end

Extend the CRM "draft follow-up" feature into a full generation spec you could
hand to Saturday's build.

**Surface:** the draft appears inline in the follow-up field (editable-output
pattern), visually marked as a draft until the user edits.

**Inputs (legible):** the contact's last three messages, the deal stage, and the
user's saved tone preference. Shown as "drafted from your last 3 messages · tone:
concise," with the messages one click away.

**Structured output (drives UI):** the model returns
`{subject, body, confidence, used_context_ids[]}`, validated with Zod. `subject`
and `body` populate the fields; `used_context_ids` renders the provenance chips;
`confidence` drives the gate.

**Personalization without contamination:** only the tone preference and *this
deal's* recent messages enter the prompt — smallest sufficient context, scoped
to this user and this deal server-side. No global history, no cross-deal
bleed.

**Model routing:** Sonnet 5 by default (quality matters, frequency is moderate);
prompt-cache the system prompt and tone spec; fall back to a template if the
model call fails validation or times out (Thursday's fallback path).

**Cost/latency:** a few hundred output tokens per draft, drafted on demand when
the user opens the deal (or precomputed for the weekly digest). Streamed into the
field so it feels instant.

**Confidence gating (built Thursday, specced now):** if the deal has fewer than,
say, two prior messages (thin context, jagged edge), suppress the draft and show
only the nudge. The feature degrades from generation to detection rather than
generating from nothing.

**Pass bar for the exercise:** you have named the editable surface, the legible
inputs, the validated structured output, the personalization scope, the model
choice with a reason, and the low-confidence degradation. If your feature
overwrites user content, generates from empty context, or renders unvalidated
model output into the UI, it does not pass — fix those before Saturday.

## Common mistakes experts see

1. **Framing generation as a final answer.** The editable-output pattern converts
   the model's inevitable misses from product failures into "a draft I improved."
2. **Overwriting user work to insert a generation.** Augment or offer alongside;
   never clobber. Clobbering makes the feature feel hostile.
3. **Personalizing with the largest available context instead of the smallest
   sufficient one.** More user data past a point is noise, cost, and
   contamination.[^3]
4. **Client-trusted scoping on retrieval or memory.** Cross-user leakage is a
   privacy incident; scope every lookup to a server-verified identity and test it
   adversarially.
5. **Rendering unvalidated model output into UI.** Validate against your schema
   (Zod/Pydantic) and handle the sub-1% failure; never trust raw model JSON in
   the DOM.[^4]
6. **Using a frontier model for a high-frequency low-stakes feature.** Route by
   stakes and frequency; Haiku for autocomplete, Opus/Fable for the rare hard
   generation.[^8]
7. **Reaching for declarative generative UI when static components would do.**
   The model picking among your trusted components is safer and covers almost
   everything.[^5]

## Reflection questions

1. For your Saturday feature, is the output a starting point or a final answer?
   If final, what breaks when the model is wrong, and can you reframe it as
   editable?
2. What is the smallest sufficient context to personalize your feature well?
   What are you tempted to add that is actually noise?
3. How is every retrieval and memory lookup in your feature scoped to a user?
   Could an adversarial user B surface user A's data?
4. What structured shape does your feature's output need to drive UI rather than
   just display text?
5. Which model tier does your feature deserve, given its stakes and frequency,
   and what is the cheaper deterministic thing you could do first?

## My take (reviewer lens)

**Jerry Liu (LlamaIndex)** would push on the "smallest sufficient context" rule
as under-specified. His work argues the hard part is not *choosing to* keep
context small but *building the retrieval* that reliably surfaces the *right*
small context per task, which for personalization means real retrieval over the
user's history, not a hand-picked three messages. The steelman: for a v1 feature,
a deterministic "last three messages" rule beats an unreliable retrieval layer,
but Jerry is right that as the feature matures, the personalization quality
ceiling is set by retrieval quality, and the lesson under-invests in that.

**Chip Huyen** would push back on the cost section as too tidy. Her lens: routing
by stakes and frequency is correct in principle, but in practice the cost that
kills AI features is not per-call inference, it is the *hidden* cost of the eval,
monitoring, and fallback infrastructure that reliable generation requires, plus
the retries and human-in-the-loop time when the model is wrong. "Cost per
successful task" is the right metric and also the one almost no one actually
instruments. The lesson names it and then hand-waves the measurement, which is
where the real work is.

**swyx** would challenge the "declarative gen-UI is over-hyped" take as too
conservative for where 2026 is heading. His counter: with A2UI, MCP Apps, and
AG-UI all shipping real specs and real client support this year, the products
that win the next cycle may be the ones that bet early on agent-generated
interfaces, and "static components cover 95%" is exactly what people said about
every platform shift before it flipped. The honest response: he may be right
about the trajectory and I am still right that a solo builder shipping a Week-12
app in August 2026 should not bet their one feature on a v0.9 spec — early-adopt
in a side experiment, not in the feature you are graded on Saturday.

## Further reading

**Must-read:**
- The 2026 structured-output reliability comparison (OpenAI Structured Outputs
  <0.1%, Anthropic tool-use <0.2%, streaming caveats).[^4]
- Anthropic, *Building Effective Agents* — the evaluator-optimizer and structured
  patterns underneath generation.[^9]

**Recommended:**
- Google Developers Blog, *A2UI v0.9* and the a2ui.org spec — the declarative
  generative-UI frontier.[^5]
- MCP Apps announcement and AG-UI generative-UI concepts — UI inside agent
  surfaces.[^6][^7]

**Optional:**
- The current Anthropic model/pricing lineup for routing decisions.[^8]

## Citations

[^1]: Granola Recipes (structured notes generated into an editable document),
2026 reviews: BlueDotHQ, https://www.bluedothq.com/blog/granola-review, and
Efficient App, https://efficient.app/apps/granola. (search-verified 2026-07-17;
fetch egress-blocked — liveness pass pending)

[^2]: ChartMogul, *The AI churn wave*, 2026,
https://chartmogul.com/reports/saas-retention-the-ai-churn-wave/ — generative
features that displace rather than collapse effort correlate with early churn.
Corroborated by Userpilot, https://userpilot.com/blog/customer-churn/.
(search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^3]: Over-personalization as a 2026 trust hazard: Nielsen Norman Group, *State
of UX 2026*, https://www.nngroup.com/articles/state-of-ux-2026/, and CDT, *Dark
Patterns in AI Chatbots* ("data and memory exploitation" category), May 2026,
https://cdt.org/insights/dark-patterns-in-ai-chatbots-a-taxonomy-to-inform-better-design/.
(search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^4]: Structured-output reliability, 2026: TokenMix, *Structured Output and JSON
Mode Guide 2026*, https://tokenmix.ai/blog/structured-output-json-guide (OpenAI
Structured Outputs <0.1% failure; Anthropic tool-use <0.2%; Anthropic returns a
single end-of-stream block — no progressive field parsing). Corroborated by
Crazyrouter, *AI Structured Output Guide 2026*,
https://crazyrouter.com/en/blog/ai-structured-output-json-mode-guide-2026, and
DigitalApplied, https://www.digitalapplied.com/blog/openai-structured-outputs-complete-guide.
(search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^5]: Google, *A2UI v0.9* — declarative, framework-agnostic generative UI with a
client-held catalog of trusted components: Google Developers Blog,
https://developers.googleblog.com/a2ui-v0-9-generative-ui/, and spec at
https://a2ui.org/. Corroborated by InfoQ, *Google Releases A2UI v0.9*,
https://www.infoq.com/news/2026/07/google-a2ui-genui/. (search-verified 2026-07-17;
fetch egress-blocked — liveness pass pending)

[^6]: MCP Apps (UI capabilities for MCP clients, building on MCP-UI and OpenAI
Apps SDK; ChatGPT/Claude/Goose/VS Code support): Model Context Protocol Blog,
*MCP Apps*, Jan 26 2026, https://blog.modelcontextprotocol.io/posts/2026-01-26-mcp-apps/.
Corroborated by CopilotKit, https://www.copilotkit.ai/blog/the-state-of-agentic-ui-comparing-ag-ui-mcp-ui-and-a2ui-protocols.
(search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^7]: AG-UI as the runtime/streaming layer carrying UI events between agent and
app: AG-UI docs, https://docs.ag-ui.com/concepts/generative-ui-specs, and
CopilotKit generative-UI examples, https://github.com/CopilotKit/generative-ui.
(search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^8]: Current Anthropic model lineup and pricing (Claude Fable 5 / Mythos 5
$10/$50, 1M ctx; Opus 4.8 $5/$25; Sonnet 5 new default, intro $2/$10; Haiku 4.5;
+~30% tokenizer change on Opus 4.7+/Sonnet 5/Fable), per the course refresh:
`vault/00-program/_refresh-2026-07-master-report.md` (two-source web-verified).
(verified 2026-07-17 in master report)

[^9]: Anthropic, *Building Effective Agents*, Dec 19 2024,
https://www.anthropic.com/research/building-effective-agents. Evaluator-optimizer
and structured-output patterns. (evergreen; primary source)

_last_verified: 2026-07-17_
