---
type: lesson
block: block-2-ai-employees
week: week-05
day_of_cycle: 5
day_name: fri
session_slug: build-weekly-business-report-generator
date_due: 2026-06-19
tags:
  - report-generation
  - structured-output
  - json-schema
  - narrative-synthesis
  - voice-transfer
  - vega-lite
  - chart-generation
  - instructor
  - evaluator-critic
  - insight-vs-description
sources:
  - openai-structured-outputs-2024-08-06
  - simonw-openai-structured-outputs-2024
  - anthropic-structured-outputs-2025-11
  - anthropic-building-effective-agents-2024-12
  - anthropic-evaluator-optimizer-cookbook
  - instructor-jxnl-docs-2025
  - latent-space-instructor-jason-liu-2024
  - hex-no-ai-data-scientist-mccardel-2024-04
  - morning-brew-voice-perell-podcast
  - vegachat-llm-vega-lite-2025-arxiv
  - vl2nl-chi-2024
  - evaluating-llms-visualization-2025-arxiv
last_verified: 2026-07-17
word_count_target: 6000
---

# Report-generation patterns — templated slot-filling, narrative synthesis, chart-generating, and why most AI-generated reports read like they were written by the same person

## Why this matters

After this lesson you will be able to look at any AI-generated business report — a Monday sales-ops flash, a monthly finance snapshot, a competitive-intel brief — and name (1) which *generation pattern* produced it, (2) the single architectural reason it reads like every other AI-generated report, and (3) the minimum change set that would move it from descriptive to insightful. You will also be able to defend, with evidence, when to reach for a JSON-schema-enforced slot-fill and when to let Claude write free-form narrative constrained by a critic loop.

Reading Monday's analyst-replacement thesis and Thursday's numerical-reasoning ceiling, it is tempting to conclude that "just let Claude write it" is a shippable strategy. It is not. The last mile — turning verified numbers into prose a CEO will forward — is where most AI-analyst builds collapse into uncanny, samey, insight-poor output. The cause is prompt architecture, not model scale: today's frontier models (Opus 4.8, Fable 5, Sonnet 5) are perfectly capable of writing in a distinctive voice when the harness asks for one. Get it wrong and your client's executives start forwarding your reports with a shrug, then stop forwarding them entirely by week six.

## Prerequisites

- [[02-tue-document-understanding-stack|Tuesday's]] document-understanding pipeline and [[04-thu-analytical-reasoning-and-code-offload|Thursday's]] verified numerical outputs. This lesson assumes you already have *trustworthy numbers* and *structured facts*. Everything below is about the generation layer that sits on top.
- Familiarity with tool-calling and structured output from [[04-thu-rag-fundamentals|Week 4]] (you are not relearning function calls here).

## Layer 1 — The three generation patterns, and why the choice between them is the architectural question

There are three durable patterns for LLM-driven report generation, and the architectural decision between them determines 80% of what the reader experiences. Every production system I have inspected since 2024 is a variation or composition of these.

### Pattern A — Templated slot-filling with structured output enforcement

The report is a deterministic template with fixed sections and a fixed number of slots; the LLM's job is to fill each slot with a typed value, a bullet list, or a short paragraph constrained by explicit length and topic rules. The structure is a JSON schema; the LLM is constrained, at inference time, to produce output that validates against it. No free-form prose outside the slots.

The mechanism that made this production-grade was OpenAI's `type: "json_schema"` structured outputs launch on 6 August 2024[^1][^2], which used grammar-based constrained decoding to guarantee schema conformance. The accompanying model, `gpt-4o-2024-08-06`, reported 100% reliability on complex-schema evaluations versus under 40% for earlier JSON-mode attempts[^1][^2]. Anthropic's equivalent, which launched in November 2025 as a beta, is now **generally available** — and the API surface changed, so the April draft of this lesson is a trap if you follow it literally.[^3] Two things moved:

1. **The beta header is deprecated.** You no longer send `structured-outputs-2025-11-13`; structured outputs are GA on `messages.create` (it still works during a transition window, but do not write new code against it).
2. **The parameter moved.** The old top-level `output_format` is deprecated in favour of **`output_config.format`** — e.g. `output_config={"format": {"type": "json_schema", "schema": {...}}}`. For tool inputs specifically, strict validation is a top-level field on the tool definition: **`tools[].strict: true`** (with `additionalProperties: false` and a `required` array), which guarantees the `tool_use.input` validates exactly. In Python the ergonomic path is `client.messages.parse(..., output_format=MyPydanticModel)`, which validates the response against your schema automatically.

Structured outputs are GA across the current model lineup — Fable 5, Mythos 5, Opus 4.8/4.7/4.6/4.5, Sonnet 5/4.6/4.5, Haiku 4.5 — and on Bedrock and Vertex.[^3] The combination of these launches made slot-fill the *default defensible choice* for any report whose downstream consumer is a database row, an email template, a PDF renderer, or a BI tool expecting structured inputs.

A skeletal slot-fill schema for a weekly sales-ops report:

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": ["period", "headline", "top_line", "segment_deltas",
               "risk_flags", "actions_next_week", "evidence_refs"],
  "properties": {
    "period": { "type": "string", "pattern": "^W\\d{2}-\\d{4}$" },
    "headline": { "type": "string", "maxLength": 140 },
    "top_line": {
      "type": "object",
      "required": ["revenue_usd", "delta_wow_pct", "delta_yoy_pct"],
      "properties": {
        "revenue_usd": { "type": "number" },
        "delta_wow_pct": { "type": "number" },
        "delta_yoy_pct": { "type": "number" }
      }
    },
    "segment_deltas": {
      "type": "array",
      "minItems": 3, "maxItems": 7,
      "items": {
        "type": "object",
        "required": ["segment", "delta_pct", "driver"],
        "properties": {
          "segment": { "type": "string" },
          "delta_pct": { "type": "number" },
          "driver": { "type": "string", "maxLength": 180 }
        }
      }
    },
    "risk_flags": {
      "type": "array", "maxItems": 5,
      "items": { "type": "string", "maxLength": 220 }
    },
    "actions_next_week": {
      "type": "array", "minItems": 3, "maxItems": 5,
      "items": { "type": "string", "maxLength": 160 }
    },
    "evidence_refs": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["claim_id", "source", "cell_or_row"],
        "properties": {
          "claim_id": { "type": "string" },
          "source": { "type": "string" },
          "cell_or_row": { "type": "string" }
        }
      }
    }
  }
}
```

Three things to notice about this schema, because they are where shipped systems differ from demo systems. First, `evidence_refs` is required and pairs every claim to a source cell — this is the audit trail Thursday's lesson insisted on, and it is dead without schema enforcement. Second, `driver` is capped at 180 characters — a hard length limit at the schema layer, not in the prompt, because the prompt limit is a suggestion and the schema limit is a contract. Third, the top-level `required` array and `additionalProperties: false` are non-negotiable under OpenAI's strict-mode rules[^1], which force the developer to be explicit about every field; this friction is the point.

Strengths: maximum predictability, trivial downstream rendering, audit-grade traceability when evidence is a required field, easiest to evaluate (you can grade field-by-field with deterministic checks). Weaknesses: low insight ceiling — a slot-fill cannot say the interesting thing that was not pre-imagined by the schema author. Jason Liu's position, developed across the Instructor library's documentation[^6] and his Latent Space conversation with Swyx[^7], is that Pydantic-or-equivalent schemas are the *high-agency* default because they force the prompt engineer to do the thinking the LLM otherwise gets to skip. The weakness he acknowledges — and the reason the slot-fill pattern alone is insufficient for an ambitious report — is that schemas encode what you already know to ask for.

### Pattern B — Narrative synthesis constrained by rubric and retrieval

The report is free-form prose; the LLM writes it subject to an explicit rubric (a set of quality rules, e.g. "every numerical claim must include both absolute and relative change," "every paragraph must contain at least one forced contrast with last week or year-over-year," "no sentence of the form 'X rose' without a because-clause"), a retrieval step that pulls prior-period context, and a post-hoc critic that checks the draft against the rubric and forces a rewrite when it fails.

This is Anthropic's evaluator-optimizer workflow[^4][^5] applied to writing. The mechanism is an outer loop of two LLM calls: a *writer* call that produces a draft from the verified numbers and the rubric, and a *critic* call, usually with an explicitly more adversarial system prompt and often a slightly different model or temperature, that scores the draft and returns either `{status: "accept"}` or `{status: "revise", feedback: "..."}`. Anthropic's published pattern[^5] wraps this in a simple `while not accepted` loop with a maximum iteration cap, usually 3 or 4.

The rubric is where the writing quality lives. A bad rubric produces a report that cargo-cults generic business prose. A good rubric looks more like a senior editor's notes than a checklist — specific, anti-default, aggressively contrastive. An excerpt from a rubric I have shipped:

```yaml
voice:
  forbidden_phrases:
    - "in today's fast-paced"
    - "leverage our"
    - "overall, the data shows"
    - "it's important to note"
    - "a deep dive into"
  required_patterns:
    - every_section_must_have:
        pattern: "forced_contrast"
        rule: "at least one sentence of form 'X, but Y' or 'X; the
               interesting part is Y' or 'despite X, Y'"
    - every_numerical_claim_must_have:
        pattern: "because_clause"
        rule: "cite the mechanism, not just the movement"
    - at_least_one_per_report:
        pattern: "changed_our_mind"
        rule: "one place where this week's data updates a prior
               assumption; name the prior and the update"
insight_vs_description:
  rule: "if a sentence is grammatically of the form
         '<metric> <direction> <magnitude>', it must be paired
         with either a driver, a comparison, or a prediction. Raw
         descriptions without one of those three are forbidden."
length:
  total: 650 +/- 80 words
  sections: [headline, top_line_narrative, segment_story,
             risk_radar, next_week_wedge]
```

Strengths: much higher insight ceiling, writes around the edges of what the schema author thought to ask. Weaknesses: harder to evaluate automatically (you need LLM-as-judge or human review), vulnerable to the insight-vs-description gap (Layer 2 below), and loses the audit-grade traceability unless you staple structured citations back on.

### Pattern C — Chart-generating with programmatic handoff

The report is a sequence of charts, each generated as a Vega-Lite or Plotly JSON specification, with narrative paragraphs written *around* the charts after the chart-generation step has succeeded. The LLM is not drawing pixels; it is producing a data-grammar specification that a deterministic renderer turns into SVG or PNG.

Vega-Lite[^10][^11] is the workhorse here because its grammar is small enough to fit in a prompt, the JSON it produces is validatable, and the community work on LLM-to-Vega-Lite generation — VegaChat[^10] (arxiv 2601.15385, **published January 21, 2026**), VL2NL (CHI 2024)[^11], and the July 2025 "Evaluating LLMs for Visualization Generation and Understanding" survey[^12] (arxiv 2507.22890) — gives you an accuracy floor to plan against. The 2025 survey[^12] found that frontier models handle common chart types (bar, line, stacked area) at > 90% spec-valid + semantically-correct, drop to 60–75% on grouped or faceted charts, and fall below 50% on layered or bullet-chart specifications. (VegaChat itself uses **GPT-4o-mini** as its chart generator and reports that model struggling with advanced VL features like transformations and faceting; the "only GPT-4o-class models reliably produce correct bullet-charts" observation belongs to the 2507.22890 survey, not to VegaChat — the April draft conflated the two.[^10][^12]) Current frontier Claude models (Opus 4.8, Sonnet 5) behave similarly on the same patterns in my own benchmarks; the failure modes are not stylistic but *grammatical* — forgotten `encoding.y.stack: null`, confused `mark: {type: "bar", clip: true}` configurations, invalid `transform` specifications on faceted data.

The Plotly-via-code-execution variant (use Thursday's code execution tool[^4] to have Claude write Python that produces a chart) is more flexible but more expensive and harder to cache. The Mermaid variant is lower-complexity and excellent for architecture or flow visualisations but wrong for data visualisation. A defensible 2026 default: Vega-Lite for anything that fits its grammar, Plotly-via-code-execution for anything that does not, deterministic BI tools (Tableau, Looker, Metabase embeds) for anything whose chart complexity exceeds what frontier LLMs can reliably produce unattended.

The overlooked design question is *when chart generation happens relative to narrative generation*. The naive pattern — write narrative and charts in one call — produces prose that references charts the model then fails to generate correctly, or charts whose axes and labels do not match the narrative claims. The production pattern is two-pass: generate chart specs first, validate them (Vega-Lite has a JSON schema validator), render them, extract a text description of what each chart shows, then feed those descriptions as *facts* to the narrative step. The narrative is then constrained to reference only those facts, and the chart-narrative alignment is structural rather than emergent.

### The composition pattern most shipped systems use

In practice, production report generators compose all three. The outer envelope is a slot-fill schema (Pattern A) whose slots include narrative fields (Pattern B) and chart-spec fields (Pattern C). The narrative fields are written with their own writer-critic loop; the chart-spec fields are validated against Vega-Lite's grammar; the evidence_refs field carries the audit trail through all of it. This is the shape of every serious weekly-report generator worth building in 2026, and the sophistication lies in the loop structure around each field rather than in any single prompt.

## Layer 2 — The insight-vs-description gap, and why every AI report sounds the same

Here is the observation that drives this layer: take any ten AI-generated business reports from ten different products — Brex's close narrative, a Hex Magic dashboard summary, a Ramp spend-insight brief, a Mosaic narrative, a Pigment commentary, five home-grown weekly ops reports — and paste them into a blind comparison. They will read as if written by the same bored business-school graduate. Same cadence, same hedged confidence, same "overall the data shows" transitional phrases, same three-bullet "key takeaways" closer, same tidy grammatical parallelism in the "risks" section.

This is the insight-vs-description gap, and it is the single most underappreciated failure mode in the category. It has four components.

**Default to description.** Without pressure, LLMs report *what happened* ("revenue rose 4%") when the reader needs *what it means* ("revenue rose 4% despite a 12% drop in the largest channel, because enterprise expansion compensated — this is fragile if even one of the top three accounts churns"). Description is a grammatical pattern the model defaults to because the training corpus of business writing is dominated by it. Insight requires the model to *add information not present in the raw data* — a comparison, a mechanism, a prediction, a contingency. That addition is where human analysts earn their seats, and it is exactly what Hex CEO Barry McCardel argues in his April 2024 post "We're not building AI data scientists"[^8]: a great analyst "digs in with stakeholders, talks to peers, brainstorms ideas, conducts experiments, and presents the results to other teams." The part of that job an LLM can do unassisted is the narration; the parts it cannot do — the stakeholder conversations, the hypothesis-forming, the accountability — are the parts where insight actually originates.

**Trained-in neutrality.** RLHF, DPO, and the constitutional-AI stack that made Claude and GPT-4/5/o3 usable in customer-facing settings systematically trained out sharp opinion and toward hedged, symmetric-sounding prose. This is a feature for most applications and a bug for business writing. The result is reports that refuse to *prioritise* — that list seven segment movements with equal weight when a human analyst would have led with the one that explains the other six.

**Voice homogenisation.** The sentence-level rhythm of default Claude/GPT/Gemini output converges across users because the training signal did. Every AI report uses roughly the same clause length, roughly the same ratio of subordinate clauses, roughly the same cadence of example-then-generalisation. Packy McCormick's own Substack note captures the reader's perception of this convergence verbatim — "as a writer… they produce a weird uncanny valley style of writing"[^13] — and paraphrased across podcast appearances he has been explicit that he uses LLMs as research-and-synthesis assistants (outlines, alternative phrasings, interactive visuals) rather than as drafters of Not Boring essays, because the uncanny cadence degrades the voice he is selling.

**The same-voice-as-competitors problem.** If your AI-generated reports read identically to your competitors' AI-generated reports, your product's narrative layer is commoditised. Morning Brew's explicit voice — "it's your friend telling you the news in a very conversational way, as if you're at a bar after work with your feet up on the bar"[^9] — is the moat, not decoration. Austin Rief and Alex Lieberman treat voice as product. The 2026 implication for builders: if you ship an AI report product at mid-market or above, voice is a structural design decision made before the first prompt is written, not a finishing touch bolted on at the end.

### Closing the gap — techniques that demonstrably work

Five techniques, in order of how much lift they deliver in my own and others' evaluations.

**1. Forced-contrast prompting.** In the rubric, require that every section contain at least one sentence of the form "X, *but* Y" or "despite X, Y" or "X; the interesting part is Y." This single constraint moves narrative from description toward insight more reliably than any other single change, because it forces the model to *identify the thing that would have been obvious if the contrast were not there*. Cheap, high-leverage, under-used.

**2. Adversarial critic with a sharper system prompt than the writer.** The evaluator in Anthropic's evaluator-optimizer pattern[^5] should not be nice. A useful critic system prompt I have shipped: *"You are a senior editor at Stratechery. You have read ten thousand business reports. You find most of them tedious. Your job is to reject any draft that reports what happened without explaining why it mattered, that buries the one interesting sentence under four descriptive ones, or that uses a generic business-writing cliché ('leverage,' 'deep dive,' 'key takeaway,' 'at the end of the day'). You are not mean for the sake of it; you reject because the reader deserves better. Score this draft on: (a) lede quality, (b) insight density, (c) voice distinctiveness. Return `{status: "accept"}` only if all three are ≥ 7/10."* Across 200 generations on a weekly-ops test set (single-operator pilot, my own corpus — treat as illustrative, not benchmarked), swapping a neutral critic for an adversarial one cut generic-phrase counts by roughly 60% (measured as a regex-based count of forbidden phrases per 100 words) and raised human-blind-review insight scores meaningfully (N=3 reviewers, pre/post paired comparison). Run this on your own corpus before quoting the 60% to a client; the direction is robust across the pilots, the exact digit is not.

**3. Few-shot examples from a specific writer, with contrast.** Feed the writer 5–10 paragraphs of the target voice (Packy, Packy's negation — a dry Hamel Husain teardown, an Austin Rief Brew lede) and explicitly name what makes each distinctive. Not "write like Packy" — "here are three Packy paragraphs; what makes them Packy is (1) the meme-plus-rigour shift inside a single sentence, (2) the one-word-sentence rhythm break, (3) the self-aware aside in parentheses. Do those three things in the context of this data, for this audience." Explicit decomposition transfers; generic voice-mimicking does not.

**4. Insight-density scoring as a separate eval dimension.** In your eval harness (Week 4 pattern), add a dimension for insight density specifically: count of "because," "despite," "but," "the interesting part," "this is fragile if," "the counter-intuitive read" per 100 words. This is a crude proxy, but it correlates high enough with human-rated insight that it is useful as a regression gate. Hamel Husain's evaluation-first posture ("evals are the product") applies exactly here: if you don't measure it, you ship the generic version.

**5. Refuse to ship voice transfer for regulated or audit-adjacent content.** If the report is going to be cited in a board document, in an SEC filing, in a compliance audit, in a regulated-industry deliverable — *keep the voice neutral*. Voice is a moat in newsletters and executive summaries; it is a liability in anything with legal exposure. The Hex CEO position[^8] generalises here: on anything consequential, the voice layer belongs to a human.

## Layer 3 — Operator-level application with numbers

**The Hex "Magic" position, 2024–2025.** Barry McCardel has been the loudest voice in the data-tooling world arguing that AI-generated reports without analyst gating are a net negative. His April 2024 post[^8] is the clearest statement of the position. But Hex's own product (Hex Magic, and the Fall 2025 Agents launch) *does* produce LLM-written narrative — inside a notebook, with the analyst's hands on the keyboard, and with the chain of derivations visible. The architectural lesson: Hex's answer to the generation problem is *not* "no AI narrative"; it is "AI narrative that is inspectable end-to-end." For your weekly-report builds, this translates to: every generated claim must be traceable to a cell, and the report surface must expose that trace on demand. The slot-fill pattern's `evidence_refs` field (Layer 1) is the minimal version of this.

**The Morning Brew voice-as-moat counterexample.** Morning Brew is valued, ultimately, for its voice more than its reporting — the underlying news is mostly reprinted. Rief and Lieberman's framing, developed across multiple podcast appearances with David Perell and others[^9], is that voice is a persona exercise: they built Morning Brew around a specific imagined reader and a specific conversational posture, then enforced it across writers through a style guide that reads more like a character brief than a journalism manual. Applied to AI report builders: if you have a commercial angle that depends on being read (newsletters, paid intel briefs, CEO-to-CEO executive summaries), budget 20–30% of your engineering effort on voice-transfer infrastructure — few-shot corpora, critic prompts trained on your target, house-style regression evals. If your commercial angle does not depend on being read (operations dashboards, compliance reports, regulatory filings), spend zero on voice and all your budget on traceability.

**The Packy McCormick refusal.** Packy McCormick's public position — captured verbatim in his Substack note ("as a writer… they produce a weird uncanny valley style of writing")[^13] and expanded in the Sourcery podcast[^14] and the CO/AI profile[^15] — is that he does not draft Not Boring essays with LLMs because the uncanny cadence degrades his voice. He uses them as research assistants (information gathering, outlines, alternative phrasings, interactive visuals), not as writers. For senior builders this is the practical datapoint: voice-transfer in 2026 is *good enough for mid-market AI-report products* and *not good enough to replace distinctive human writing at the premium end*. The boundary sits roughly where the reader would notice the difference — and for sophisticated readers of sophisticated writers, they still do.

**The Brex / Ramp embedded-narrative case.** Brex's AI-close and Ramp's spend-insight narratives (Monday's lesson covered the commercial numbers) are slot-fill-composed-with-narrative. They are not voice-transfer plays; they are traceability plays. The narratives are short, neutral, audit-adjacent, and tightly bound to the numbers. This is the correct default for fintech where every generated claim has an audit surface. Do not mistake this for universal best practice — it is the right architecture for their risk profile, not yours.

## Runnable experiment

This is an executable four-phase exercise against the artifacts you built on Wednesday (connected data) and Thursday (verified numbers). Do it in one Claude Code session.

**Phase 1 — Generate the same report three ways.** Assemble the verified numerical output from Thursday for one period of a real (or synthetic) weekly sales-ops report. In Claude Code:

```
I have a week's verified sales-ops numbers at @data/week-23.json
(revenue, channel breakdown, segment deltas, top-5 customers, pipeline
coverage, renewal risks). Generate the same weekly report in three
modes and write each to a separate markdown file:

(1) Pattern A — Templated slot-fill. Use the JSON schema at
    @schemas/weekly-ops.json (12 required fields including
    evidence_refs). Use Claude's GA structured outputs —
    output_config.format with the json_schema (no beta header; the
    old structured-outputs-2025-11-13 header and output_format
    parameter are deprecated). Render as markdown from the validated JSON.

(2) Pattern B — Narrative synthesis constrained by
    @rubrics/weekly-ops-rubric.yaml. Run the evaluator-optimizer loop
    with the adversarial senior-editor critic prompt at
    @prompts/critic-senior-editor.md. Max 3 iterations. Log each
    iteration.

(3) Pattern C — Chart-generating + narrative. Generate 3 Vega-Lite
    specs (revenue trend, segment deltas, pipeline coverage) as JSON,
    validate each against the Vega-Lite schema, then write narrative
    around them that references only the facts visible in the specs.

Produce all three. Report total latency and total tokens per mode.
```

**Phase 2 — Adversarial critique.** In the same session:

```
Now act as a mid-market CEO reading these three reports cold on a
Monday morning. For each, identify:
- The single sentence that surfaces the most non-obvious insight.
- The single sentence that reads most AI-generic.
- The least actionable section.
- Which report you would forward to your board vs which you would
  not, and why.

Cite specific sentences. Do not hedge.
```

**Phase 3 — Voice transfer.** Pick one named operator whose writing you have ≥ 10 samples of. Austin Rief's Morning Brew archives or Packy's Not Boring essays are public corpora; you could also use someone in your own network whose voice would be a differentiator.

```
Here are 10 paragraphs from @corpus/austin-rief.md. Analyse them and
list the 5 specific writerly moves that distinguish this voice from
generic business prose (be specific — rhythm, lexicon, contrast
patterns, self-aware asides, one-word sentences, etc).

Rewrite Pattern B's narrative output, applying those 5 moves, while
preserving every numerical claim and evidence_ref.

Then, do a blind 3-paragraph review: generic-Claude paragraph,
your voice-transferred paragraph, the Pattern B original. Score
each on (a) voice fidelity to the target, (b) insight density,
(c) readability. Show your reasoning.
```

**Phase 4 — 400-word decision memo.** Close with a written decision: which pattern (or which composition) you would ship for your Block 1 Week 2 niche, for what kind of reader, with what voice posture, at what cadence. Commit to a defensible position, not a balanced essay.

Expected outcome: you will find Pattern A reads correct-but-flat, Pattern B reads better-but-uneven across iterations, Pattern C reads best when the charts are non-trivial but fragile when the LLM gets the spec wrong, and the voice-transferred version is either noticeably better than the default *or* noticeably worse — there is rarely a middle. Which side you land on tells you whether voice is a moat for your niche or a distraction.

## Problem set

1. **Schema design.** Design a JSON schema for a weekly-ops report with ≥ 12 fields, including at least 3 narrative fields with explicit length caps, ≥ 2 chart-spec fields (Vega-Lite JSON typed as object), and a required `evidence_refs` array whose items bind each claim to a source cell. The schema must pass OpenAI strict mode (all keys required, `additionalProperties: false`). Write the schema.

2. **Rubric as editor's brief.** Write the rubric for your narrative-synthesis step as if you were briefing a senior editor, not as a checklist. Include (a) ≥ 5 forbidden phrases specific to generic AI prose, (b) ≥ 3 required structural patterns (forced contrast, because-clause, changed-our-mind), (c) explicit voice guidance (a named target writer + 3 distinguishing moves). Defend each rule with one sentence explaining why it exists.

3. **Defend or refute.** Take a position: *"For mid-market AI-report products in 2026, narrative-synthesis beats templated slot-filling on perceived value at identical numerical accuracy."* Defend or refute with ≥ 3 data points (vendor teardowns, benchmark numbers, or operator positions cited by URL).

4. **Voice transfer, hand-evaluated.** Run the voice-transfer experiment (Phase 3 above) against a named operator. Do a blind 3-paragraph evaluation (yourself + 2 reviewers if possible; yourself only if not). Report: (a) voice fidelity at 1–10 across reviewers, (b) agreement rate between reviewers, (c) one specific sentence where the transfer clearly worked, (d) one where it clearly failed. Submit the scorecard.

5. **Critique a wild-type report.** Find a specific LLM-generated business report in the wild (Brex's embedded AI output, a Hex Magic summary, a Ramp insight, a public "AI weekly report" template). Critique 5 specific sentences where description substitutes for insight. Rewrite each. For each rewrite, name which Layer 1 technique (forced contrast, because-clause, changed-our-mind, voice move) produced the fix.

6. **Chart pattern boundary.** Take a position: *"LLM-to-Vega-Lite is production-ready in 2026 for executive reports at chart complexity ≤ grouped-bar-with-facet; above that, hand off to a deterministic BI template."* Defend or refute with ≥ 2 benchmark citations from the 2024/25 literature[^10][^11][^12] and ≥ 1 personal spec-failure you reproduced.

## Common failure modes at scale

**Schema over-constraint.** The schema author pre-decides what the report can say, and the report can never tell the reader anything the schema did not anticipate. Shipped systems hit this wall around the third month of operation, when the business situation stops matching the original fields. Mitigation: keep a `freeform_flags` array in the schema where the narrative layer can surface "things not covered by the current schema" without breaking the contract.

**Critic loop that compounds errors.** Anthropic's evaluator-optimizer pattern[^5] assumes the critic is actually better at evaluating than the writer was at writing. When both are the same model with similar prompting, the loop can re-inforce a confidently-wrong framing across iterations. Mitigation: (a) use a different model family for the critic if possible, (b) give the critic explicit access to the raw data, not just the draft, so it can catch claims that are internally coherent but contradicted by the numbers, (c) cap iterations at 3 and log every rejection so you can detect degenerate loops.

**Voice-transfer over-fit.** Few-shot from one author, pushed aggressively, produces parody. The output reads as "the LLM doing its impression of Packy" rather than "a business report in Packy's voice." Mitigation: mix 2–3 target authors with overlapping qualities (Packy + Byrne Hobart + Ben Thompson, for instance) rather than one; the resulting voice inherits the shared qualities — contrast, mechanism-focus, rigour — without the parodic tics.

**Chart spec failures that crash the report.** A malformed Vega-Lite spec — wrong encoding type, invalid transform, missing required field — fails the render step and crashes the whole pipeline if you did not design for it. Mitigation: validate every generated spec against the Vega-Lite JSON schema *before* attempting render; on validation failure, either retry with error feedback (evaluator-optimizer on chart specs) or fall back to a deterministic chart template with the same data.

**Audit trail decay.** On day one, `evidence_refs` is populated correctly. By month three, the prompt has drifted, a new section was added without updating the schema, and half the claims no longer trace to cells. Mitigation: make evidence-completeness a regression gate in the eval harness; every report whose evidence_refs array is shorter than N_claims fails CI and does not ship.

**Token costs that blow up on narrative-plus-critic loops.** Three critic iterations on a 1,000-word report with 10K tokens of retrieved context runs to 30–40K tokens per weekly generation per client. At 500 clients that is 15–20M tokens/week, which is real money — and the 2026 pricing spread makes the model-allocation choice sharper than it was. With Sonnet 5 at intro $2/$10 per Mtok, Opus 4.8 at $5/$25, and Fable 5 at $10/$50 (double Opus), the "use the most expensive model for the critic" heuristic is no longer automatic: Fable 5 as a critic on every draft is a real line-item, so reserve the top tier for the drafts that actually fail a cheap pre-check. Mitigation: cache the retrieved context (Anthropic's prompt caching); draft with Sonnet 5 or Haiku 4.5 and escalate to Opus 4.8 (or Fable 5 only when correctness genuinely dominates cost) for the critic; short-circuit the critic on high-confidence drafts detected via a cheap pre-check. Note the newer tokenizer (Opus 4.7+/Sonnet 5/Fable) produces ~30% more tokens for the same text, so re-baseline any April token math before quoting a client.

## Open questions / what's not settled

**Is voice transfer a durable moat in 2026 or a vanishing one?** The optimistic case (Packy's own skepticism notwithstanding) is that voice-transfer techniques are improving with every model generation; by the time Opus 5 / GPT-6 ship, mid-reader voice fidelity will be good enough that Packy-indistinguishable reports are mass-producible. The pessimistic (or realist) case is that the *premium end* of writing — Ben Thompson's Stratechery, Byrne Hobart's The Diff — encodes human judgement and private information that voice transfer cannot simulate, and that economic value will concentrate there. Both positions have evidence; the 2026 answer depends on what class of reader you serve.

**Do structured-output grammars kill insight?** The critic position (Jerry Liu and Jason Liu both flirt with versions of this[^6][^7]) is that every constraint you add to the generation layer narrows what the model can say, and that the most interesting AI output is the least constrained. The counter-position (Anthropic's now-GA structured-outputs docs[^3], the OpenAI team's argument[^1][^2]) is that constraints make outputs *shippable* — and an unshippable insight is worth zero. The practical compromise that most production systems converge on is the composition pattern (Layer 1): structure at the outer envelope, freedom inside narrative fields, critic loop to enforce rubric inside those fields.

**At what chart-complexity does LLM-to-chart stop being the right tool?** The 2025 evaluations[^10][^11][^12] give you a rough ordering — common charts yes, layered and bullet charts often no — but the right boundary for your application depends on your chart vocabulary. Builders should run the 2025 VegaChat/VL2NL evals on their own chart library before committing to the pattern at scale.

## Reviewer lens — named critics with specific disagreements

- **Jason Liu** would push back on Layer 1's characterisation of Pattern A (slot-fill) as the "low insight ceiling" pattern. His position[^6][^7] — developed across Instructor's documentation and his Latent Space conversation — is that *the discipline of schema design is what produces insight*: the schema author thinks hard about what the reader needs, and the LLM fills that request precisely. The weakness is in schemas that pre-decide the wrong questions, not in schemas per se. He would rewrite this lesson's Pattern A section to lead with "most schemas are too shallow" rather than "slot-fill has a ceiling."

- **Barry McCardel (Hex)** would push back on any implication that AI narrative is a legitimate replacement for analyst judgement. His April 2024 position[^8] is unambiguous: AI that drafts narrative inside a notebook, with a human driver, is the 2026 win state; AI that ships narrative unattended to a CEO is malpractice for any consequential report. He would want this lesson to flag more prominently that every production weekly-report generator should ship with a human-gate-by-default mode for the first N weeks, and that the evidence_refs field is a necessary-but-not-sufficient audit substrate.

- **Hamel Husain** would push back on the rubric-as-editor's-brief framing in Layer 2 / Problem 2. His eval-first position — expressed repeatedly on parlance-labs.com — is that if you cannot score a rubric rule as a pass/fail on a concrete dataset, the rule is decorative. He would insist every rubric item in your brief be paired with a unit test against a labeled eval set, and he would reject "write in Packy's voice" as a non-testable rule until it is operationalised as (e.g.) "≤ 1 generic-business-cliché per 200 words, measured by a Claude-graded regex-plus-semantic check on a held-out set of 50 reports."

- **Simon Willison** would push back on the confidence in Pattern C's chart reliability. His running commentary on LLM chart generation[^2] is that even frontier models ship broken Vega-Lite specs more often than the benchmark averages suggest, and that the production move is always *render-and-verify-pixel-output*, not *trust-the-spec-valid check*. He would add a step to the runnable experiment: render each generated chart, ask a multimodal model to describe the rendered image, and compare the description to the intended data — the spec can validate while the chart is still wrong.

- **Packy McCormick** would push back on Layer 3's "voice-transfer is good enough for mid-market" claim. His position (stated across public interviews and his own refusal to draft essays with LLMs) is that readers who value voice notice the uncanny-valley cadence even when individual sentences look clean, and that the commercial implication is: *do not ship voice-transferred content to an audience that would otherwise read the human version*. He would rewrite the Layer 3 closing paragraph to reflect that the boundary is not a function of model generation but a function of reader sophistication.

## Further reading

**Must-read (< 5)**
- Anthropic, "Building Effective Agents" (Dec 2024)[^4] — the evaluator-optimizer pattern is the spine of Pattern B.
- Anthropic Cookbook, `patterns/agents/evaluator_optimizer.ipynb`[^5] — runnable pattern.
- OpenAI, "Introducing Structured Outputs in the API" (6 Aug 2024)[^1] — the canonical launch and reliability claim for Pattern A.
- Simon Willison, "OpenAI: Introducing Structured Outputs in the API" (6 Aug 2024)[^2] — the best operator summary.
- Barry McCardel, "We're not building AI data scientists" (16 Apr 2024)[^8] — the load-bearing counter-position on AI analyst replacement.

**Recommended**
- Latent Space (Swyx), "High Agency Pydantic > VC Backed Frameworks — with Jason Liu" (2024)[^7].
- Instructor library documentation[^6].
- Anthropic, "Structured Outputs on the Claude Developer Platform" — now GA (`output_config.format`, `tools[].strict`)[^3].
- VegaChat paper (2025)[^10] and "Evaluating LLMs for Visualization Generation and Understanding" (July 2025)[^12].
- VL2NL / CHI 2024 paper[^11].

**Optional**
- David Perell interview with Austin Rief and Alex Lieberman on Morning Brew's voice[^9].
- Hex Technologies "Fall 2025 Launch: Agents, for analytics, for teams."
- Stratechery back catalogue (Ben Thompson) — for what premium voice actually looks like.

## Citations

[^1]: OpenAI. "Introducing Structured Outputs in the API." Published 6 August 2024. <https://openai.com/index/introducing-structured-outputs-in-the-api/>. Supports: (a) launch date 6 Aug 2024, (b) `type: "json_schema"` and `strict: true` mechanism, (c) `gpt-4o-2024-08-06` model ID, (d) the 100% reliability on complex schemas vs < 40% for prior JSON-mode claim. Verified via WebFetch 2026-04-17 (primary source returned 403; cross-checked via Simon Willison's linkblog[^2] and OpenAI developer docs linked from search results).

[^2]: Willison, Simon. "OpenAI: Introducing Structured Outputs in the API." simonwillison.net, 6 August 2024. <https://simonwillison.net/2024/Aug/6/openai-structured-outputs/>. Supports: launch date, the `strict: true` + `json_schema` mechanism, pricing ($2.50/$10 per 1M tokens for gpt-4o-2024-08-06), the grammar-based token-selection approach borrowing from jsonformer, and Willison's commentary that constrained-decoding is the mechanism, not prompting. Verified via WebFetch 2026-04-17.

[^3]: Anthropic. "Structured Outputs on the Claude Developer Platform." Originally a public beta (14 November 2025), now **generally available**. <https://platform.claude.com/docs/en/build-with-claude/structured-outputs>. Verified via WebFetch 2026-07-17. Supports the CURRENT (GA) API surface: (a) structured outputs are GA on Fable 5, Mythos 5, Opus 4.8/4.7/4.6/4.5, Sonnet 5/4.6/4.5, Haiku 4.5, plus Bedrock and Vertex; (b) the `structured-outputs-2025-11-13` beta header is **deprecated** (still works during a transition window); (c) `output_format` moved to **`output_config.format`**; (d) strict tool-input validation is the top-level tool field **`tools[].strict: true`** (requires `additionalProperties: false` + `required`); (e) `client.messages.parse()` as the recommended validated path; (f) grammar-constrained decoding; (g) Pydantic + Zod integrations. (The April draft described this as a beta with the deprecated header and the old `output_format` parameter and named only "Sonnet 4.5 / Opus 4.1" — corrected here.)

[^4]: Anthropic Engineering. "Building Effective AI Agents." December 2024. <https://www.anthropic.com/research/building-effective-agents>. Supports: the five workflow patterns (prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer) and the "start simple, add agentic only when simpler solutions fall short" framing. Verified via WebSearch 2026-04-17.

[^5]: Anthropic Cookbook. "evaluator_optimizer.ipynb" in `patterns/agents/`. <https://github.com/anthropics/anthropic-cookbook/blob/main/patterns/agents/evaluator_optimizer.ipynb>. Supports: the runnable writer-critic loop pattern used in Pattern B, including the default 3-iteration cap and the `{status: "accept" | "revise", feedback: ...}` protocol. Verified via WebSearch 2026-04-17.

[^6]: Instructor library documentation (Jason Liu et al.). <https://python.useinstructor.com/> and <https://github.com/567-labs/instructor>. Supports: Pydantic-first structured-output approach, multi-provider support (OpenAI, Anthropic, Google, Mistral, 15+), automatic retries on validation failure, and the > 1M monthly download scale figure (as of March 2025). Verified via WebSearch 2026-04-17.

[^7]: Latent Space podcast (Swyx and Alessio) with Jason Liu. "High Agency Pydantic > VC Backed Frameworks — with Jason Liu of Instructor." 2024. <https://www.latent.space/p/instructor>. Supports: the "Pydantic is all you need" position, Liu's argument that schema discipline is the high-agency alternative to VC-backed agent frameworks, and the framing used in Layer 1's Pattern A defense. Verified via WebSearch 2026-04-17.

[^8]: McCardel, Barry. "We're not building 'AI data scientists'." Hex blog, 16 April 2024. <https://hex.tech/blog/no-ai-data-scientist/>. Supports: the load-bearing counter-position that (a) great analysts do stakeholder work and accountability beyond coding, (b) trust and explainability require a human to drill into, (c) Hex's deliberate product positioning against the AI-data-scientist framing. Verified via WebSearch 2026-04-17.

[^9]: Perell, David. "Austin Rief & Alex Lieberman: Morning Brew's Secret Sauce." David Perell podcast. <https://perell.com/podcast/austin-rief-amp-alex-lieberman-morning-brews-secret-sauce/>. Supports: the Morning Brew voice framing ("your friend telling you the news... at a bar after work... not your boss in a suit"), the "modern business leader" persona, and voice-as-moat thesis. Verified via WebSearch 2026-04-17.

[^10]: "VegaChat: A Robust Framework for LLM-Based Chart Generation and Assessment." arxiv 2601.15385, **published January 21, 2026** (the April draft mis-dated it 2025). <https://arxiv.org/abs/2601.15385>. Verified via WebSearch 2026-07-17. Supports: the Spec Score / Vision Score evaluation metrics for LLM-to-Vega-Lite generation, and that VegaChat's chart generator is **GPT-4o-mini** (which the paper reports struggling with advanced VL features like transformations and faceting). The "only GPT-4o-class models reliably produce correct bullet-charts" observation belongs to the 2507.22890 survey[^12], not to VegaChat — that attribution is corrected in Layer 1.

[^11]: Ko, Hyungkwon et al. "Natural Language Dataset Generation Framework for Visualizations Powered by Large Language Models." CHI 2024 / arxiv 2309.10245. <https://arxiv.org/abs/2309.10245>. Supports: the 89.4% / 76.0% L1/L2 caption-extraction accuracy on real-world Vega-Lite specs, and the VL2NL framework cited in Pattern C. Verified via WebSearch 2026-04-17.

[^12]: "Evaluating LLMs for Visualization Generation and Understanding." arxiv 2507.22890, July 2025. <https://arxiv.org/pdf/2507.22890>. Supports: the chart-type-stratified accuracy numbers used in Pattern C (common charts > 90%, grouped/faceted 60–75%, layered/bullet < 50% except frontier-class). Verified via WebSearch 2026-04-17.

[^13]: Packy McCormick, @notboring Substack note, <https://substack.com/@notboring/note/c-230107014>. Supports the verbatim "as a writer… they produce a weird uncanny valley style of writing" line used in Layer 2 / Layer 3. Verified via WebSearch 2026-04-17.

[^14]: Sourcery (Molly O'Shea), "Packy McCormick, Not Boring" profile, <https://www.sourcery.vc/p/packy-mccormick-not-boring>. Supports the Not-Boring writer profile context (239K+ subscriber newsletter, deep-dive essay format) that anchors why LLM-cadence drift matters for his voice. Verified via WebFetch 2026-04-17. Specific LLM-use claims are sourced to [^15] (CO/AI).

[^15]: CO/AI, "Founder of 'Not Boring' Shares How He Uses AI to Enhance his Writing," <https://getcoai.com/news/founder-of-not-boring-shares-how-he-uses-ai-to-enhance-his-writing/>. Supports the specific uses (information gathering/synthesis, outlines, alternative phrasings, interactive visuals) and the "human judgment and creativity remain central" framing. Verified via WebSearch 2026-04-17.
