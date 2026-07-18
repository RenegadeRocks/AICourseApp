---
type: lesson
block: block-3-advanced-topics-voice
week: week-08
day_of_cycle: 4
day_name: thu
session_slug: build-hybrid-agent-scraper-summarizer
date_due: 2026-07-09
tags: [hybrid-agent, pipeline, checkpointing, retries, transient-permanent, structured-outputs, output-contracts, cost-budget, drift-detection, dedup, synthesis, deterministic-spine]
sources:
  - anthropic-building-effective-agents-2024-12
  - anthropic-structured-outputs-docs
  - anthropic-opus-4-8-dynamic-workflows-2026-05
  - llamaindex-workflows-1-0-2026-06
  - opentelemetry-genai-2026
  - refresh-2026-07-landscape-delta
  - firecrawl-v25-2026
  - anthropic-sonnet-5-2026-06
  - redis-agents-vs-workflows-2026
last_verified: 2026-07-17
word_count_target: 5300
---

# Hybrid agent design — deterministic spine, judgment islands, and the plumbing that lets you walk away

## Why this matters

Monday you decided the scraper→summarizer is a hybrid: a deterministic pipeline with two islands of LLM judgment. Today you design the thing in full — not the happy path (that's a demo), but the *unattended* version, where the machinery between the stages is the actual product. The demo is `fetch → summarize → send`. The product is `fetch → checkpoint → extract → checkpoint → dedup → judge-relevance → checkpoint → synthesize → validate-contract → deliver → record → alert-on-anything-wrong`, and every arrow is a place a 3 a.m. run can fail, retry, duplicate, drift, or lie.

This is the lesson that converts "I built an agent that worked when I watched it" into "I built an agent I trust to run while I sleep." By the end you'll have the full architecture on paper: stage boundaries, checkpoint schema, retry semantics, output contracts, a per-run cost budget, and a drift detector — everything Saturday's code-lab implements.

## Prerequisites

- [[01-mon-the-automation-spectrum-in-2026]] — the determinism-per-step test; today we build the pipeline it implies.
- [[02-tue-mcp-integration-patterns-for-unattended-agents]] — idempotency and the TRANSIENT/PERMANENT convention, which we now make load-bearing.
- [[02-tue-building-an-mcp-server]] — where the TRANSIENT/PERMANENT error convention was first taught. One-line recap: transient on 5xx/timeout/429 (retry with backoff), permanent on 4xx/contract-violation (stop, alert, don't retry the same input).
- [[06-sat-build-the-weekly-report-generator]] — the Block 2 build with the same spine-plus-gates shape; this is its unattended, web-fed sibling.

## Layer 1 — The spine-and-islands architecture

Draw the pipeline as a chain of **stages**, each with a typed input and a typed output, connected by **checkpoints**. Classify every stage as deterministic (code) or judgment (LLM). The design invariant, straight from Anthropic's "Building Effective Agents": deterministic wherever the correct behavior is writable in advance; model only where genuine judgment is required, wrapped in the tightest contract you can express.[^1]

The canonical scraper→summarizer, staged:

| # | Stage | Type | In → Out |
|---|---|---|---|
| 1 | **Fetch** | Deterministic | schedule → raw responses per source |
| 2 | **Extract** | Deterministic (schema) / Judgment (prose) | raw → `Item[]` conforming to one schema |
| 3 | **Dedup** | Deterministic + narrow judgment | `Item[]` → deduped `Item[]` |
| 4 | **Relevance judge** | Judgment | `Item[]` → `Item[]` with `keep`, `score`, `reason` |
| 5 | **Synthesize** | Judgment | kept items → cited brief |
| 6 | **Validate contract** | Deterministic | brief → brief-or-reject |
| 7 | **Deliver** | Deterministic | brief → email/file/WA |
| 8 | **Record + alert** | Deterministic | outcome → run log, heartbeat, alerts |

Two judgment islands (4 and 5), a whisker of judgment in 3, everything else boring code. This is not an aesthetic preference; it's the arithmetic from Monday made concrete, and it's what the industry's post-mortems keep re-deriving: hybrid — deterministic control with judgment at the ambiguous steps — is the architecture that reaches production.[^9]

**Why stage boundaries matter beyond tidiness:** each boundary is a place you can checkpoint, retry, cost-cap, cache, and test *independently*. A monolithic `do_everything(sources)` agent has one failure mode — "it broke" — and no recovery point. A staged pipeline has eight failure modes, each nameable, recoverable, and separately eval-able. Nameable failure is fixable failure.

## Layer 2 — Checkpointing: never redo expensive work, never lose it

A checkpoint is durable state written between stages so a re-run resumes instead of restarting. For an unattended pipeline this is not optional, for three reasons: runs fail partway and must resume without re-paying; **LLM stages are non-idempotent** (Tuesday), so re-running stage 5 gives a *different* brief unless you reuse the checkpointed result; and checkpoints are your audit trail when Friday's postmortem asks "what did the model actually see and decide?"

Design the checkpoint store as append-only, keyed by run and stage:

```
runs/2026-07-11/
  01-fetch.json         # raw responses + fetch metadata (status, etag, timing)
  02-items.json         # extracted Item[] (schema-conformant)
  03-deduped.json       # after dedup, with dropped-duplicate provenance
  04-judged.json        # items + keep/score/reason from the relevance judge
  05-brief.md + .json   # synthesized brief + structured metadata
  run.log               # stage timings, token counts, costs, outcomes
```

Rules that separate a checkpoint store from a pile of temp files:

- **Content-hash your items** (`sha256(url + normalized_title)`), so dedup and idempotent writes share one identity and a re-run recognizes what it already processed.
- **Checkpoint judgment *outputs*, and on resume reuse them** rather than re-asking the model. This is correctness (stable output) *and* cost (Layer 4) at once.
- **Make each stage resumable**: on start, load the latest valid upstream checkpoint; skip stages whose output already exists and validates. Saturday's harness implements exactly this.
- **Keep raw fetch bytes long enough to debug.** When the brief is wrong, you need to replay from stage 1's checkpoint to see whether the fault was fetch, extract, judge, or synthesize. Retention is cheap; blind debugging is not.

LlamaIndex Workflows 1.0 (latest release June 30, 2026) is worth studying here even if you build bespoke: it makes typed workflow state and event-driven steps the recommended architecture for exactly this pattern, and its checkpoint/observability story is what you'd otherwise rebuild.[^4] For Saturday we build it by hand once — because owning the mechanism once teaches what the framework is doing for you — then you graduate to the framework when the state machine outgrows a page.

## Layer 3 — Retries with TRANSIENT/PERMANENT semantics

The convention from [[02-tue-building-an-mcp-server]] is the backbone of unattended reliability. Every stage that can fail classifies its failure:

- **TRANSIENT** — 5xx, timeouts, 429, connection resets, model overload. *Retry with exponential backoff + jitter*, capped (3–5 attempts). Jitter is not optional: even Anthropic's own scheduler jitters fires to avoid synchronized retry storms.[^5]
- **PERMANENT** — 4xx (except 429), auth failures, schema-validation failures, a source's ToS block, a contract rejection. *Do not retry the same input.* Log, alert, and degrade — skip the item/source and continue, or fail the run loudly, depending on blast radius.

The failure modes worth calling out because they're where naive pipelines die:

- **The successful-but-timed-out write.** Delivery succeeds; the ack is lost; the retry sends a duplicate. This is why Tuesday's idempotency (delivery keyed by date/brief-ID) and this section are the same defense from two sides.
- **The poison item.** One malformed source crashes stage 2 and takes the whole run with it. Fix: stage-level try/except that quarantines the bad item as PERMANENT and lets the other four sources through. A digest of 4 sources beats a crash over 1.
- **The retry-amplified ban.** Retrying a 403 as if transient hammers a source into rate-limiting or blocking you (Wednesday). Auth/authorization failures are PERMANENT — page a human, don't retry.
- **The infinite-cost retry.** A transient error inside a paid LLM stage, retried without a cap, bills unboundedly. Every retry loop needs a hard attempt cap *and* a per-run cost ceiling (Layer 4).

The one-sentence policy: **retry what a second attempt could plausibly fix; alert on everything else; never let a retry loop run uncapped in tokens or attempts.**

## Layer 4 — Output contracts and cost budgets

### Output contracts

An unattended pipeline's stages communicate through **contracts** — schemas that the producer guarantees and the consumer can assume. The most important contract is the boundary between the judgment islands and the deterministic delivery: the model produces, code validates, and *only validated output ships*.

Anthropic's structured outputs are the enforcement mechanism, GA on the Claude API: supply a JSON Schema via `output_format` and generation is grammar-constrained to conform, eliminating the almost-JSON-at-3-a.m. failure class.[^2] Use it at the extract stage (item schema) and the relevance-judge stage (keep/score/reason schema). The synthesize stage is subtler: you want a structured envelope (title, sections, sources[]) *and* inline citations — but strict JSON-schema output conflicts with Claude's interleaved citation blocks (a documented 400).[^2] The clean resolution: synthesize prose-with-citations in one call, then a deterministic validator (or a cheap second structured call) checks the contract — every claim traces to a source in the kept set, no source is fabricated, length and section requirements met. **Validation is deterministic code, not vibes**; a brief that fails the contract is a PERMANENT failure that alerts rather than ships.

The contract that matters most for a summarizer nobody reviews: **every factual claim in the brief must cite a source URL that exists in the kept-items set, and the validator rejects any claim that doesn't.** This is your primary hallucination containment (Friday goes deeper) and it's enforceable in deterministic code because the kept set is a known, finite list.

### Cost budgets

Give every run a **token and dollar ceiling**, enforced, not estimated. The budget is a first-class input, checked between stages:

- **Per-stage caps.** Extraction over 40 items shouldn't exceed N tokens; if a source returns a 500KB page, truncate or chunk deterministically before the model sees it. Runaway input is the usual cause of a run that costs 10x its neighbors.
- **Model tiering.** Relevance judging (stage 4) is a cheap classification — run it on the cheapest capable tier (Haiku-class or Sonnet 5 at $2/$10 intro). Synthesis (stage 5) is where quality shows — spend the better model there. Don't pay flagship rates to decide "is this on-topic."[^6][^7]
- **Cache the schema and the stable prompts.** Structured-output schemas cache ~24h;[^2] prompt-cache the invariant instruction blocks. On a daily run the marginal cost is the day's content, not the boilerplate.
- **Hard ceiling → controlled stop.** If a run approaches its dollar ceiling, it should *stop cleanly and alert* — ship a partial brief with a "truncated: budget" note or skip synthesis and alert — never silently blow the budget. A cost ceiling that only warns is a cost ceiling that gets exceeded.

Remember the tokenizer: current Anthropic models run ~30% heavier per token than the 2025 generation, so budgets ported from older intuition undercount.[^8] Measure real token counts from stage checkpoints; don't estimate from word counts.

## Layer 5 — Drift detection: when the world changes under a sleeping agent

The uniquely nasty failure of unattended pipelines is **silent drift**: nothing errors, but the output quietly degrades because the world changed. Three kinds, three detectors.

**1. Source-layout drift.** A site redesigns; your selectors now return empty; extraction "succeeds" with zero items and nobody notices for a week. Detectors: (a) **volume guardrails** — a source that reliably yields 5–15 items yielding 0 is an alert, not a valid empty result; (b) **schema-fill-rate** — if `published_at` was populated 95% of the time and drops to 10%, the layout moved; (c) **canary fields** — assert that a known-stable element exists on each fetch. Firecrawl's change-tracking helps here by git-diffing pages against their last scrape, so "the page structure changed" becomes an observable signal rather than a mystery.[^10]

**2. Content drift.** The source's content itself shifts (a niche blog pivots topics), and your relevance judge starts keeping things it shouldn't or dropping things it should. Detector: track keep-rate and score distribution per source over time; a sudden shift is worth a human glance. This shades into eval territory (Friday).

**3. Model drift.** You upgrade the model (or Anthropic ships a new default), and the same prompt now judges or writes differently. This is why Friday's golden-set regression exists: **any prompt or model change re-runs the golden set before shipping.** Model drift is the most dangerous because it's invisible in the output and global in effect — every source, every run, silently different.

The instrumentation that makes drift observable is standardizing: **OpenTelemetry's GenAI semantic conventions** now define agent/LLM/tool spans (`gen_ai.request.model`, `gen_ai.usage.input_tokens`/`output_tokens`, `gen_ai.response.finish_reasons`) and MCP tool-call attributes, supported by Datadog, Honeycomb, New Relic and emitted natively by LangChain/CrewAI.[^3] For Saturday you don't need a full OTel stack — a structured `run.log` with per-stage timings, token counts, item volumes, and keep-rates is enough to *see* drift — but know that the vendor-neutral standard exists and that graduating to it is the path when you have more than one automation to watch.

## Experiment — design the whole pipeline before you build it

This is a design lesson; the experiment is a design artifact you'll implement Saturday. Direct Claude Code (45–60 min):

1. **Draw the stage table for your niche.** *"For a daily scraper→summarizer over [my 4–5 sources], produce the stage table: each stage typed DETERMINISTIC or JUDGMENT, with its input schema and output schema. Then for each stage, name its most likely failure and classify it TRANSIENT or PERMANENT."* Grade against Layer 1 and Layer 3.
2. **Specify the checkpoint store.** *"Design the checkpoint directory and file schemas for this pipeline, keyed by run and stage, content-hashing items on sha256(url+normalized_title). Show how a re-run at 09:05 after a 09:00 crash in stage 4 resumes without re-fetching or re-extracting."* This is the resume logic Saturday implements.
3. **Write the two contracts that matter.** *"Write the JSON Schema for the extract stage's Item and the relevance-judge's output (keep/score/reason). Then write, in deterministic pseudocode, the brief validator: every claim cites a URL in the kept set; no fabricated sources; sections and length within bounds. A failing brief is PERMANENT — show what it alerts."*
4. **Set the budget.** *"Given Sonnet 5 at $2/$10 (intro) for synthesis and a Haiku-class tier for relevance judging, set per-stage token caps and a per-run dollar ceiling for a 40-item run. Show what happens when a source returns a 500KB page (input runaway) and when the run approaches its ceiling mid-synthesis."*
5. **Design the drift detectors.** *"Add volume guardrails, schema-fill-rate checks, and per-source keep-rate tracking to the run log. Simulate source 2's layout breaking (extraction returns 0 items) and show exactly which detector fires and what it alerts — distinguishing 'legitimately quiet day' from 'silently broken.'"* If your design can't tell those two apart, it's not done.

Keep every artifact. Saturday's code-lab is the implementation of this exact design; walking in with the design done is the difference between a 3-hour build and a 6-hour one.

## Common mistakes experts see

- **Monolithic agent, no stage boundaries.** One failure mode ("it broke"), no recovery point, no independent eval. Stage it.
- **Re-running LLM stages on resume.** Non-idempotent: you get a different brief and pay twice. Checkpoint judgment outputs and reuse them.
- **Retrying PERMANENT failures.** Hammering a 403 gets you blocked; retrying a schema violation burns tokens on an input that will never conform.
- **No cost ceiling.** One runaway input or uncapped retry loop turns a $0.45 run into a surprise invoice. Cap per-stage and per-run, enforce, alert.
- **Shipping model output unvalidated.** The whole point of unattended operation is nobody checks — so code must. Validate the contract before delivery, always.
- **Treating an empty result as success.** Zero items from a source that always yields ten is drift, not a quiet day. Volume guardrails distinguish them.
- **Changing the model without re-running the golden set.** Model drift is silent and global; the regression gate (Friday) is the only thing that catches it before your readers do.
- **Estimating cost from word counts.** The current tokenizer runs ~30% heavier; measure real tokens from checkpoints.[^8]

## Reflection questions

1. Your relevance judge (stage 4) checkpoints its keep/score/reason. A re-run reuses that checkpoint. Under what circumstance is reusing it *wrong* — when should a resume actually re-judge — and how would the pipeline know?
2. The brief validator rejects any claim citing a URL not in the kept set. This catches fabricated sources. What class of hallucination does it *not* catch, and what second check would you add (preview of Friday)?
3. You tier models: Haiku-class judges relevance, Sonnet 5 synthesizes. Describe the failure where the cheap judge's mistake is *invisible* until it corrupts the expensive synthesis — and where you'd put a guard.
4. Source-layout drift and a legitimately quiet news day both produce few items. Your volume guardrail must not cry wolf on quiet days. What signal distinguishes them, and what's the cost of getting it wrong in each direction?
5. Anthropic ships a new default model mid-quarter and your pipeline silently upgrades. Nothing errors. Walk the exact sequence by which your readers would notice before you do — then design the gate that makes you notice first.
6. A per-run dollar ceiling forces a choice when hit mid-synthesis: ship a partial brief, skip synthesis and alert, or fail the run. Pick one for *your* niche and justify it in terms of what a bad brief costs your reader versus what no brief costs them.

## My take (reviewer lens)

**Michael Seibel** would call most of this premature. His line: you're designing eight stages, a checkpoint schema, and three drift detectors for a digest you haven't shipped once. Build the four-line happy path, email it to yourself for a week, and let *real* failures tell you which of these eight stages actually need armor — you'll find it's two, not eight, and you'll have wasted a day gold-plating the other six. He's right that the failures teach the priorities, and the lesson should concede it: **implement the spine and the contract-validation first; add checkpointing, tiering, and drift detection when a real run makes you want them.** The architecture is the destination, not Saturday's minimum.

**Lilian Weng** would push from the opposite side on the judgment islands. Her agent-architecture lens: treating relevance-judge and synthesize as isolated single-shot calls leaves capability on the table — a reflective loop (judge, critique its own keeps, revise) or a planner that decides *how much* synthesis a given day's items warrant would raise quality, and the rigid stage table forecloses it. Fair tension: the course's answer is that unattended reliability *buys* its trustworthiness precisely by foreclosing open-ended agentic loops nobody's watching, and that reflection is a controlled extra stage (judge→critique→revise, each checkpointed) rather than a free-roaming loop. Add it as stages 4a/4b when the golden set says quality needs it — not as ambient autonomy.

**Chip Huyen** would want the cost-budget section to admit its own hardest case: the budget is easy to enforce per run and nearly impossible to enforce across the *retry-and-drift tail*, where a flaky source triggers retries across many runs and a slow layout drift inflates token use week over week without any single run breaching its ceiling. Per-run ceilings don't see cumulative creep. The honest addition is a *rolling* cost monitor — weekly spend trend, alert on anomaly — alongside the per-run cap. The lesson has the per-run guard; it should say plainly that the per-run guard is necessary and not sufficient.

## Further reading

**Must-read**

- Anthropic — "Building Effective Agents" (workflow vs agent; simplest-composable-patterns).[^1]
- Anthropic — Structured outputs docs (`output_format`, `strict`, the citation-conflict caveat).[^2]

**Recommended**

- LlamaIndex — "Announcing Workflows 1.0" (typed state, event-driven steps, checkpoint/observability).[^4]
- OpenTelemetry — GenAI semantic conventions blog (agent/LLM/tool spans).[^3]
- Redis — "AI Agents vs Workflows" (the hybrid-as-default consensus, restated cleanly).[^9]

**Optional**

- Firecrawl change-tracking docs (drift-as-observable-signal).[^10]
- Anthropic — Opus 4.8 dynamic workflows (where model-written orchestration is heading).[^11]

## Citations

[^1]: Anthropic. "Building Effective Agents." https://www.anthropic.com/engineering/building-effective-agents — December 19, 2024. Deterministic-where-possible, model-where-judgment-required; simple composable patterns over frameworks.

[^2]: Anthropic. Structured outputs — Claude Platform docs. https://platform.claude.com/docs/en/build-with-claude/structured-outputs — GA on the Claude API; `output_format` grammar-constrained JSON (schema cached ~24h); `strict: true` for tool arguments; citation blocks conflict with strict schema (400). Corroborated by Thomas Wiegold "Claude API Structured Output" https://thomas-wiegold.com/blog/claude-api-structured-output/ and AWS "Structured outputs now available in Amazon Bedrock" https://aws.amazon.com/about-aws/whats-new/2026/02/structured-outputs-available-amazon-bedrock/ (search-verified 2026-07-17; direct fetch egress-blocked — liveness pass pending).

[^3]: OpenTelemetry. "Inside the LLM Call: GenAI Observability with OpenTelemetry." https://opentelemetry.io/blog/2026/genai-observability/ — GenAI semantic conventions: `gen_ai.request.model`, `gen_ai.usage.input_tokens`/`output_tokens`, `gen_ai.response.finish_reasons`, agent/tool spans, MCP tool-call attributes; vendor support (Datadog/Honeycomb/New Relic). Corroborated by Greptime "How OpenTelemetry Traces LLM Calls, Agent Reasoning, and MCP Tools" https://greptime.com/blogs/2026-05-09-opentelemetry-genai-semantic-conventions (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^4]: LlamaIndex. "Announcing Workflows 1.0." https://www.llamaindex.ai/blog/announcing-workflows-1-0-a-lightweight-framework-for-agentic-systems — typed workflow state (Py+TS), event-driven steps as recommended architecture; latest release 2026-06-30 per https://pypi.org/project/llama-index-workflows/ (verified in landscape delta §4, URL-verified 2026-07-17).

[^5]: Claude Code docs. "Run prompts on a schedule." https://code.claude.com/docs/en/scheduled-tasks — scheduler jitter to avoid synchronized API hits (fetched live 2026-07-17).

[^6]: Anthropic. "Claude Sonnet 5." https://www.anthropic.com/news/claude-sonnet-5 — June 30, 2026; intro $2/$10 per Mtok through 2026-08-31 then $3/$15. Verified in master refresh (two-source) and landscape delta §1.

[^7]: Model tiering rationale draws on the Sonnet 5 vs Haiku-class price gap and Anthropic's structured-outputs model coverage;[^2][^6] cheap classification vs expensive synthesis is a cost-architecture choice, not a vendor claim.

[^8]: Course master refresh report, `vault/00-program/_refresh-2026-07-master-report.md` (2026-07-17), cross-cutting theme 1: ~+30% tokens on the current Anthropic tokenizer versus the prior generation.

[^9]: Redis blog. "AI Agents vs Workflows: When to Use Each." https://redis.io/blog/agents-vs-workflows/ — hybrid (deterministic control + judgment at ambiguous steps) as the production-reaching architecture. Failure-rate context (88% of pilots, eval gaps as top blocker) per Digital Applied "AI Agent Adoption 2026" https://www.digitalapplied.com/blog/ai-agent-adoption-2026-enterprise-data-points (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^10]: Firecrawl. Change Tracking docs. https://docs.firecrawl.dev/features/change-tracking — git-diff of a page against its last scrape as a change signal, no extra cost (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^11]: Anthropic. "Introducing Claude Opus 4.8." https://www.anthropic.com/news/claude-opus-4-8 — May 28, 2026; dynamic workflows (model writes a JS orchestration script, runtime executes it). Verified in landscape delta §1.

_last_verified: 2026-07-17_
