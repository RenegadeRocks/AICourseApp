---
type: synthesis
block: block-2-ai-employees
week: week-05
day_of_cycle: 7
day_name: sun
session_slug: week-05-synthesis
title: 'Week 5 Synthesis — The AI analyst worker stack'
study_date: 2026-06-21
date_due: 2026-06-21
tags: [synthesis, quiz, flashcards, ai-analyst-worker, document-understanding, mcp, code-execution, financebench, report-generation, evaluator-critic, weekly-report-generator]
sources:
  - ramp-announcing-ramp-intelligence-2025
  - brex-intelligent-finance-platform-2025
  - hex-no-ai-data-scientist-2024
  - llamaparse-launch-liu-2024
  - unstructured-score-bench-2025
  - docling-ibm-launch-2024
  - anthropic-pdf-support-docs
  - financebench-islam-2023-arxiv-2311-11944
  - finqa-chen-2021-arxiv-2109-00122
  - pal-gao-2022-arxiv-2211-10435
  - huang-iclr-2024-self-correct-2310-01798
  - anthropic-code-execution-tool-2025
  - anthropic-mcp-announcement-2024-11-25
  - simonwillison-mcp-prompt-injection-2025-04
  - anthropic-building-effective-agents-2024
  - hamel-husain-llm-judge-2024
  - edpb-opinion-28-2024-ai-models
last_verified: 2026-07-17
word_count_target: 3800
---

# Week 5 Synthesis — The AI analyst worker stack

## The one-sentence thesis of this week

The six deep-dives this week — category landscape (Mon), document-understanding (Tue), data connectivity and governance (Wed), numerical reasoning and code-execution offload (Thu), report-generation patterns (Fri), and the end-to-end build (Sat) — decompose into a single operator pipeline: **category pick → parse → connect → verify → generate → ship**. Block 2 Week 3 built the surface that wins prospects. Week 4 built the retrieval and agent layer. Week 5 is the back-office worker that reads the business and writes the Monday brief, and it is the cleanest ROI story in the three-worker portfolio because the labor arbitrage — two analyst hours compressed into fifteen minutes — is explicit and measurable.

---

## The unifying frame: the six-stage pipeline, each stage a failure surface

Every AI analyst worker that ships and survives the first quarter of use passes through six pipeline stages. Each stage has a dominant failure mode that kills production deployments, and each has an architectural mitigation the week taught explicitly.

- **Stage 1 — Category pick ([[01-mon-analyst-replacement-thesis|Mon]]).** Failure: category confusion. Selling a category-4 weekly-report build while the client thinks they are getting Brex's category-1 close-cycle outcome. Brex's Fall 2025 release discloses "nearly 70% of all expenses on Brex are handled entirely by automation" and close-cycle compression of 3x;[^1] Ramp's April 2026 procurement-agent fleet discloses 16% average annual vendor-spend savings and 46 hours/month of purchasing work eliminated.[^2] Those numbers are category-1 (financial close/procurement). Category-4 (operational weekly reporting) still has no *category-native* incumbent, but the "no incumbent" claim is now qualified: Anthropic itself shipped Claude for Financial Services agent templates (month-end closer, GL reconciler, and eight more) on May 5, 2026, and Menlo's 2025 survey found 76% of AI use cases are bought rather than built.[^19] The cleanest commercial lane is now "the cross-functional, source-specific, client-voiced report the horizontal templates can't reach" — and you still have to name the category in the SOW or the client benchmarks your build against the wrong disclosed number.

- **Stage 2 — Parse ([[02-tue-document-understanding-stack|Tue]]).** Failure: silent table flattening and hallucinated citations. Patronus AI's FinanceBench found that GPT-4-Turbo with retrieval refused or incorrectly answered 81% of 150 manually-reviewed 10-K questions, and the dominant root cause under inspection was parsing, not modeling.[^3] Unstructured's own SCORE-Bench documents that parser rankings invert across TEDS, NED, and GriTS on the same corpus — which means a single leaderboard number is noise until anchored to a document class.[^4] The architectural fix: document-class-first spec, then bakeoff across ≥3 archetypes (specialised OSS, hosted gen-AI-first, native multimodal), with a hand-labelled eval of N≥20.

- **Stage 3 — Connect ([[03-wed-data-connectivity|Wed]]).** Failure: over-scoped service accounts, the deprecated-server trap, and the Willison "lethal trifecta" (private data + untrusted content + external communication; coined June 16, 2025).[^5] MCP is now multi-vendor infrastructure under the Linux Foundation's Agentic AI Foundation (Dec 2025), with an official Registry and a 2026-07-28 stateless-core release candidate in flight;[^6] the object lesson of the week is that *server provenance is a security property* — the archived `@modelcontextprotocol/server-postgres` reference server carries a documented Datadog SQL-injection bypass of its read-only mode, so build on a maintained alternative (`crystaldba/postgres-mcp` in `--access-mode=restricted`).[^20] The governance primitives — narrow views, PostgreSQL RLS with `SET LOCAL` tenant context, Presidio-style PII masking at the connector layer, append-only audit logs — are not optional for any production build. The EDPB's Opinion 28/2024 on AI models makes the Article 5 data-minimisation principle binding on LLM pipelines that process EU personal data.[^7]

- **Stage 4 — Verify ([[04-thu-analytical-reasoning-and-code-offload|Thu]]).** Failure: unit confusion, sign errors, aggregation off-by-one, rounding compounding, hallucinated column values. Chen et al.'s FinQA (EMNLP 2021) formalised the failure taxonomy at 8,281 expert-annotated pairs;[^8] Gao et al.'s Program-Aided Language Models (ICML 2023) showed that delegating arithmetic to a Python runtime beat chain-of-thought by +6.4 points on GSM8K.[^9] In 2026 Anthropic's code execution tool[^10] is the frictionless PAL substrate — $0.05/container-hour after a free monthly allowance (~1,550 container-hours/month per org), and free when bundled with the current `web_search_20260209`/`web_fetch_20260209` tool versions. Pair it with an evaluator-critic that meets the Huang 2024 external-signal condition[^11] and numerical-accuracy moves from ~68% (single-shot) to ~94% (generator + code-execution + critic with forced tool-use) on a typical 30-question weekly-ops eval — indicative single-operator pilot figures, not a public benchmark.

- **Stage 5 — Generate ([[05-fri-report-generation-patterns|Fri]]).** Failure: description-as-insight, voice-averaging across clients, and LLM-to-chart breakdowns on executive-grade visuals. The failure mode is economic: when the same generator writes the Monday report for ten clients in ten industries, all ten start sounding like the same person, the reports become commodity, and price compresses. The mitigation is pattern selection per reader (templated slot-fill for regulatory, narrative-synthesis for mid-market CEO, chart-generating with deterministic Vega-Lite for board decks), plus voice transfer enforced at the prompt layer with hand-graded paragraph-level fidelity as the success metric.

- **Stage 6 — Ship ([[06-sat-build-the-weekly-report-generator|Sat]]).** Failure: the pipeline works on Tuesday, breaks on Monday at 9am, and no one notices because observability wasn't wired. Anthropic's *Building Effective Agents* (Dec 2024) provides the orchestrator-workers and prompt-chain patterns that beat autonomous-agent frameworks for predictable scheduled workflows.[^12] The shipping discipline is explicit-pipeline over autonomous-agent, Cron + Modal/Railway/Vercel for solo scale, LangSmith/Braintrust/Helicone free tier for observability from day 1, and a 30-day rollout with a human spot-check gate on the first N reports.

The pipeline is also the frame for why the Week 5 build is the cleanest commercial pitch in Block 2. On a Week 3 landing-page build you compete with every prototype shop. On a Week 4 sales-agent build you compete with 11x, Artisan, Regie. On a Week 5 weekly-report build you have no named incumbent in category 4 and a labor-arbitrage number anyone can verify: two hours of analyst time × weekly cadence × 52 weeks × blended rate, minus your fee, equals first-year ROI.

---

## Where each day's content goes forward

| This week's lesson | Underwrites in later weeks |
|---|---|
| Mon — Category landscape + replacement vs augmentation | Every commercial framing for back-office AI work; Block 3 voice-agent category-mapping; any "build vs buy" conversation against Brex/Ramp/Mosaic/Pigment |
| Tue — Document-understanding stack | Every pipeline that ingests real business PDFs; Week 4 RAG parsing layer revisited; Block 3 multimodal voice-agent document handoff |
| Wed — Data connectivity + MCP + governance | Every production AI worker that reads customer data; Block 3 enterprise deployments with SOC 2 in scope; any "why did our AI leak PII" postmortem |
| Thu — Numerical reasoning + code-execution offload | Every claim-in-writing that will be cited to an executive; Block 3 voice-agent numerical answering; any financial-reporting engagement |
| Fri — Report-generation patterns + voice transfer | Every LLM-generated artifact whose value is narrative, not dashboard; Block 3 voice-persona work; any "our AI reports all sound the same" retrospective |
| Sat — End-to-end build + eval + deploy + monitor | Every weekly/monthly/quarterly scheduled AI job; Block 3 voice-agent deployment patterns; any "v1 shipped but we can't measure drift" retrospective |

Together, Weeks 3–5 give you three deployable AI workers: a conversion surface, two operational agents, and a back-office analyst. Block 3 layers advanced patterns and voice agents onto this stack.

---

## The week's key moves — the mental-move table

Fifteen highest-leverage moves drawn from the six lessons. Each row: the move, the mechanism, when to apply, when not to.

| # | Move | Mechanism | Apply when | Do NOT apply when |
|---|------|-----------|------------|-------------------|
| 1 | Name the report category (1/2/3/4) in the SOW before pricing | Category-1 pitches compete with Brex/Ramp disclosed numbers; category-4 has no incumbent. The category sets the benchmark the client compares you against | First engagement, any commercial framing | Internal tools where no client comparison exists |
| 2 | Spec the document class before picking a parser | Parser rankings invert across corpora (Unstructured SCORE-Bench); the spec collapses tool selection from "which is best" to "which is best for this" | Any build that ingests PDFs/docs | Pure-database builds with no document layer |
| 3 | Hand-label N≥20 eval docs BEFORE running a pipeline bakeoff | Every hour labeling saves ~20 hours debugging an unscorable pipeline (Husain)[^13] | Any document-parsing pipeline that will ship | Throwaway one-shot extractions |
| 4 | Cache parsed markdown by SHA-256 of raw bytes | First parse expensive; every re-chunk free. Frequently moves pipeline cost 10x | Any corpus re-processed across runs | Single-run archival extraction |
| 5 | Route pages, don't one-parser-fits-all | Clean text → cheap extractor, tables → Docling/LlamaParse, charts → Claude Vision with chart prompt | Heterogeneous corpora with >1 page class | Uniform document classes |
| 6 | Default MCP for new connector work; SDK for battle-tested production; LangChain loaders for batch RAG ingest | MCP wins on governance separability; SDK wins on control; loaders win on one-shot index ingest | New build, solo or small team | When adversarial content exposure is high — then SDK-in-sandbox (Willison lethal trifecta)[^5] |
| 7 | Narrow service-account scope to views that project only necessary columns | Over-broad `SELECT public.*` is the single most common SOC 2 finding pattern | Any read-path against customer-data tables | Internal demo data only |
| 8 | Force RLS + `SET LOCAL tenant_id` for multi-tenant analyst workers | Prevents prompt-injected cross-tenant leaks; Postgres has had RLS since 9.5 | Multi-tenant deployments | Single-tenant per-deployment |
| 9 | Offload any claim that will be cited in writing to the code execution sandbox | PAL +6.4 over CoT on GSM8K; production numerical accuracy moves ~68%→~86%→~94% with code + critic | Any claim in a board document, regulatory filing, or executive brief | Trivial single-op aggregations where offload latency > value |
| 10 | Declare `units` in the tool-call schema | Catches unit-confusion (bps vs pct vs points) at the tool layer, not the narration layer | Any numerical tool-use definition | Pure-text tool definitions |
| 11 | Build the evaluator-critic with external signal + named failure taxonomy + flag-don't-overwrite | Huang 2024: intrinsic self-correction fails; external-feedback self-correction works[^11] | Any production generation with audit-critical numerical claims | Narrative-only generation with no numbers |
| 12 | Pick the generation pattern by reader, not by default | Templated slot-fill for regulatory, narrative-synthesis for mid-market CEO, chart-generating for board decks — voice-transferred per client | Any client-facing report | Internal ops dashboards |
| 13 | Ship the explicit orchestrator-workers pipeline, not an autonomous agent | Anthropic *Building Effective Agents* (Dec 2024) — prompt-chain and orchestrator-workers beat autonomous for predictable scheduled jobs[^12] | Weekly/monthly scheduled AI work | Research/exploration work where the plan is unknown |
| 14 | Wire observability (LangSmith/Braintrust/Helicone free tier) from day 1 | Cannot fix what you cannot see; a weekly cron that silently fails ships an empty report | Any production scheduled pipeline | Local dev / one-shot scripts |
| 15 | 30-day rollout with human spot-check gate on first N reports | Hex's "AI drafts, human publishes" framing avoids confidently-wrong output at audit-surface[^14] | Any first production deployment for a new reader | Internal pilots the reader has explicitly accepted as draft-quality |

---

## 20 quiz questions

*Span: Mon–Sat. Mix: 8 recall, 8 apply, 4 controversy-defense. Answers at end.*

---

**Q1 (Recall)** — Name the six pipeline stages of an AI analyst worker and the dominant failure mode at each stage.

**Q2 (Recall)** — State the four categories of "AI that reads your business" and the disclosed automation number associated with one named incumbent in each.

**Q3 (Recall)** — Give the FinanceBench headline number (November 2023, Islam et al., arxiv 2311.11944) on GPT-4-Turbo with retrieval, and state what the root-cause diagnosis was.

**Q4 (Recall)** — Name the five document-parsing archetypes and one named vendor or project in each.

**Q5 (Recall)** — Define the Willison "lethal trifecta" for MCP-equipped agents.

**Q6 (Recall)** — Give the six failure modes in the numerical-reasoning taxonomy (Thursday).

**Q7 (Recall)** — State the PAL (Program-Aided Language Models) headline gain over chain-of-thought on GSM8K and cite the paper.

**Q8 (Recall)** — Name the three conditions an evaluator-critic must meet (per Huang 2024 + S²R 2025) to produce real accuracy gain rather than intrinsic self-correction theatre.

**Q9 (Apply)** — For a mid-market SaaS weekly sales-ops report pulling from Postgres + Stripe + HubSpot + Google Sheets + S3, produce a 5-source connector matrix with MCP / SDK / LangChain-loader / iPaaS picks, defended one line each. Pick one source where you flip the choice between solo-operator and 15-person-team scenarios.

**Q10 (Apply)** — Write the Pydantic schema for a weekly ops report output enforcing ≥12 fields. Must include at least: `period_start`, `period_end`, `top_line_revenue` (with `units` field), `wow_delta_pct`, `top_three_insights: list[Insight]`, and `chart_specs: list[VegaLiteJSON]`. Defend one non-obvious choice.

**Q11 (Apply)** — Write the evaluator-critic prompt for a weekly-ops generator. It must (a) use external signal via code execution, (b) name the failure taxonomy from Thursday, (c) flag-don't-overwrite. ≤ 180 words.

**Q12 (Apply)** — Design the 20-question eval set for one report type in your Block 1 Week 2 niche. Specify the distribution (single-aggregation / multi-step / sign-and-direction / edge-ambiguous), the labeling rubric for numerical fields, and the gold-answer hand-check protocol.

**Q13 (Apply)** — Sketch the day-1 governance checklist for an AI analyst worker against customer-data tables at a 20-person SaaS selling to regulated buyers. Categorise each item must-have / should-have / nice-to-have. Include at minimum: least-privilege, view-layer PII masking, audit logging, SOC 2 sub-processor intake.

**Q14 (Apply)** — Write the Claude tool definition JSON for `run_python` in a report-generator context. Must include the `units` enum, the `expected_type` enum, and a description that names the pre-loaded dataframes. Explain why the `units` field catches a failure class no prompt can.

**Q15 (Apply)** — Cost your weekly-report generator at 1 run/week, 5 runs/week, and 50 runs/week. State the scale at which LLM cost dominates and name the single optimisation that unlocks 10x cost reduction at that tier.

**Q16 (Apply)** — Design the 30-day rollout plan for the first shipped weekly report. Must include: reader identity, human spot-check gate, sunset criteria for the gate, metric the gate is measured on, and what you do on week 5 when the gate comes off.

**Q17 (Controversy-defense)** — Position: *"In 2026, shipping any LLM-generated claim into a board document without a deterministic runtime verification is malpractice."* Defend or refute in ≤ 300 words citing ≥ 3 benchmark numbers.

**Q18 (Controversy-defense)** — Position: *"By 2027, stand-alone weekly-report-generator products are absorbed as features by BI platforms (Tableau, Looker, Metabase, Mode); the category disappears."* Take a side with ≥ 3 data points.

**Q19 (Controversy-defense)** — Position: *"Claude Code as orchestrator beats LangGraph + Pydantic AI for a solo-operator weekly report generator in 2026."* Take a side with a build-experience argument.

**Q20 (Controversy-defense)** — Position: *"Native-multimodal (Claude Vision) makes specialised pipelines (Unstructured + Table Transformer) architecturally redundant by end of 2027."* Defend or refute, citing Jerry Liu's and Brandon Smock's public positions.

---

## Answers

**Q1** — (1) Category pick / category confusion in the pitch. (2) Parse / silent table flattening + hallucinated citations. (3) Connect / over-scoped service accounts + Willison lethal trifecta. (4) Verify / unit confusion, sign errors, aggregation off-by-one, rounding compounding, hallucinated column values. (5) Generate / description-as-insight + voice-averaging + LLM-chart breakdowns. (6) Ship / observability-absent scheduled job that silently fails.

**Q2** — Category 1 (financial-close automation) — Brex, ~70% of expenses handled entirely by automation, books close 3x faster (Fall 2025 release);[^1] Ramp's April 2026 procurement agents disclose 16% avg vendor savings / 46 hrs/month eliminated.[^2] Anthropic now competes here too via Claude for Financial Services agent templates (May 2026).[^19] Category 2 (management reporting / CPM) — Pigment, "Analyst Agent" that generates complete narrative reports with charts, KPIs, recommendations (2025 product page). Category 3 (competitive/market intelligence) — Consensus, Klue, CompeteIQ, Crayon, Gong Revenue-AI layer. Category 4 (operational reporting) — no *category-native* incumbent (Saturday's build targets this), though horizontal frontier-lab templates now edge in.

**Q3** — GPT-4-Turbo with retrieval refused or incorrectly answered 81% of 150 manually-reviewed questions on the FinanceBench open subset (Islam et al., arxiv 2311.11944, Nov 2023).[^3] Root-cause diagnosis on inspection: parser splitting tables across retrieval chunks, so the answer required cells that had ended up in different retrievals. The diagnosis is "your parser is your retrieval is your accuracy."

**Q4** — (1) Specialised-pipeline OSS — Unstructured, Docling (IBM, July 2024)[^15], Marker, LiteParse (LlamaIndex, 2026 — local Rust core). (2) Hosted gen-AI-first — LlamaParse (Jerry Liu, Feb 2024)[^16], Reducto, Chunkr (schema extraction now split into the separate LlamaExtract product). (3) Native-multimodal — Claude Vision, GPT-5.x Vision, Gemini 3.1 Pro, Qwen-VL.[^17] (4) Cloud document-AI services — AWS Textract, Google Document AI, Azure Form Recognizer. (5) Academic-paper specialists — Nougat (Meta FAIR), GROBID.

**Q5** — Willison's "lethal trifecta" (coined June 16, 2025 — not the earlier April 2025 MCP prompt-injection post): an MCP-equipped agent is exploitable when it simultaneously has (a) access to private data, (b) exposure to untrusted content (email bodies, web pages, tickets that an adversary can plant tokens in), and (c) ability to communicate externally. Any one of the three alone is safe-ish; all three together is confused-deputy territory.[^5]

**Q6** — (1) Aggregation off-by-one. (2) Unit and scale confusion. (3) Sign errors on deltas. (4) Hallucinated column values. (5) Confidently-wrong rounding (compounding across multi-step chains). (6) Out-of-scope hallucination in "just narrate" prompts after verification.

**Q7** — PAL (Gao et al., arxiv 2211.10435, ICML 2023) beat chain-of-thought by +6.4 points on GSM8K with a smaller model — PAL-Codex 72.0% vs CoT 65.6%.[^9] Mechanism: decompose question with LLM, emit Python program, execute deterministically, use result in narration.

**Q8** — The critic must (1) have access to a signal the generator did not — code execution result, retrieval hit, rule check; (2) be prompted with the *specific failure taxonomy* for this domain, not a generic "check for errors"; (3) flag and reroute, not overwrite — emit a structured verdict the orchestrator acts on. Without all three, the critic collapses to Huang 2024's intrinsic self-correction and does not improve accuracy over self-consistency at matched sampling budget.[^11]

**Q9** — Example matrix. Postgres: MCP Postgres reference server (solo) / SDK + connection pool + query tagging (15-person). Flip: solo prefers MCP for speed; 15-person wants EXPLAIN visibility and DBA-traceable queries. Stripe: vendor SDK both scenarios (Stripe's API changes often; SDK pins the contract). HubSpot: community MCP server if audited (solo) / SDK wrapped as internal tool (15-person). Google Sheets: Sheets MCP with pinned named ranges + schema validation — iPaaS tempting but hides schema drift. S3: MCP filesystem server (solo) / Boto3 with IAM role assumption (15-person).

**Q10** — ```python
from pydantic import BaseModel, Field
from typing import Literal

class Insight(BaseModel):
    claim: str
    evidence_tool_call_id: str
    failure_gate_passed: bool

class WeeklyOpsReport(BaseModel):
    period_start: str
    period_end: str
    top_line_revenue: float
    top_line_units: Literal["USD","INR","EUR"]
    wow_delta_pct: float
    wow_delta_units: Literal["pct","bps","points"]
    top_three_insights: list[Insight] = Field(min_length=3, max_length=3)
    chart_specs: list[dict]   # Vega-Lite JSON
    audit_trail: list[str]     # tool-call ids with source locators
    generator_voice_profile: str
    verified_at: str
```
Non-obvious choice: `wow_delta_units` is a typed enum rather than free-text `"percent"`. Forcing the model to pick between `pct`, `bps`, `points` at schema-validation time catches the single most common audit-killing failure — unit confusion — before any renderer sees the value.

**Q11** — "You are the weekly-ops report critic. The DRAFT below contains N numerical claims and K narrative insights. For each numerical claim, verify by running the relevant query against the sandbox-loaded dataframes (`orders_df`, `stripe_df`, `hubspot_df`, `prior_period_df`) using the `run_python` tool. Return a JSON list where each entry has `{claim_text, claim_type, tool_call_id, verified_value, verified_units, drafted_value, drafted_units, match, failure_mode}`. `failure_mode` must be one of: `none | aggregation_off_by_one | unit_confusion | sign_error | hallucinated_source | rounding_chain | out_of_scope`. You may NOT rewrite the draft. If any claim's `match` is false, the orchestrator will re-dispatch generation with verified values. Reject the draft if the number of claims without a tool_call_id exceeds zero."

**Q12** — Example for a mid-market SaaS weekly sales-ops report. Distribution: 5 single-aggregation ("total revenue last week by region"), 5 multi-step ("week-over-week pipeline coverage ratio adjusted for seasonality"), 5 sign-and-direction ("did net-new MRR expand or contract"), 5 edge-ambiguous ("what drove the change in CAC — definitional question on channel attribution"). Labeling rubric: numerical match = exact for counts, within rounding tolerance specified per field for ratios, date match = any valid ISO-8601 for dates. Hand-check: 100% of gold answers re-derived in a separate Claude Code session using code execution, with the source-cell reference captured. Flag any gold answer where two independent derivations disagree and treat as ambiguous (removed from eval, kept in a "needs-adjudication" bucket).

**Q13** — Day-1 must-have: least-privilege read-only service account; PII column masking at the view layer; audit logging of every tool call; SOC 2 sub-processor intake on any observability vendor that sees traces (Cacioppo/Vanta position — this is day-1 not day-30). Day-30 should-have: PostgreSQL RLS with `SET LOCAL` tenant context; Presidio-style text-layer PII masking; BAA with LLM vendor if any chance of PHI. Day-90 nice-to-have: MCP gateway with policy enforcement; signed tool manifests with diff-on-change alerts; tiered redaction by report consumer.

**Q14** — See the schema in Thursday's Layer 3 (reproduced):
```json
{
  "name": "run_python",
  "description": "Execute Python in a sandboxed runtime with pandas/numpy and pre-loaded dataframes: orders_df (schema: [...]), stripe_df (schema: [...]), hubspot_df, prior_period_df. Use for ALL numerical aggregations, deltas, ratios, multi-step calculations.",
  "input_schema": {
    "type": "object",
    "properties": {
      "code": {"type": "string"},
      "expected_type": {"type": "string", "enum": ["scalar","series","dataframe","text"]},
      "units": {"type": "string", "enum": ["USD","bps","pct","points","ratio","count"]}
    },
    "required": ["code","expected_type","units"]
  }
}
```
The `units` field catches the failure class "margin expansion of 4 points" where ground truth is 40 bps. A prompt cannot reliably enforce unit discipline; a schema can. The orchestrator rejects any call whose declared `units` is inconsistent with the drafted narrative's rendered units.

**Q15** — Rough costing for a frontier Claude model + code execution + critic loop at typical report sizes (*use current list pricing and re-check before quoting a client; as of mid-2026 the relevant tiers are Sonnet 5 at intro $2/$10 per Mtok, Opus 4.8 at $5/$25, and Fable 5 at $10/$50 — double Opus — and the newer tokenizer produces ~30% more tokens for the same text, so April cost math is stale*): 1 run/week ≈ $8–$15/run, so ~$35–$65/mo — engineering time dominates. 5 runs/week ≈ $175–$325/mo — still engineering-dominated. 50 runs/week (service bureau) ≈ $1,750–$3,250/mo — now LLM cost is material. The 10x optimisation at 50-run scale: aggressive prompt caching of the common-prompt prefix (schema, tool definitions, critic rubric — often 80% of input tokens), routing simple pages/sections to Haiku 4.5 or Sonnet 5, reserving the top tier (Opus 4.8/Fable 5) only for drafts that fail a cheap pre-check, and caching the parsed-markdown of any re-used source document by SHA-256. These together typically drop cost 8–15x.

**Q16** — Reader: named stakeholder (e.g., "Head of Revenue Ops, reads Monday 9am"). Human spot-check gate: named reviewer (probably you or a designated analyst) reads every report for weeks 1–4 before send. Sunset criteria: gate comes off when (a) zero material numerical errors across 4 consecutive weeks, (b) narrative voice fidelity score ≥ 4/5 on hand-graded sample, (c) reader NPS ≥ 8. Metric: `material_numerical_error_count` + `voice_fidelity_manual_score` weekly. Week 5 when gate lifts: move from spot-check-every-report to sample-check 1-in-4; maintain drift-detection on a rolling 20-question regression eval; keep a kill-switch that re-enables spot-check if any metric drops.

**Q17** — Defend, narrowly scoped. Benchmark evidence: FinanceBench 81% refuse-or-wrong for GPT-4-Turbo with retrieval at launch;[^3] FinQA 48.56% numerical-reasoning baseline for GPT-3 vs ~89% human;[^8] GSM8K is saturated but harder variants (GSM8K-Hard, MATH-Hard, Scheherazade) retain material model gaps. The failure modes protected against are unit confusion, sign error, aggregation off-by-one, and rounding compounding — all of which produce confident-wrong narrative at audit-surface failure. Concession: for questions where the arithmetic is trivially the question (`df.q4.sum()`), offload adds latency without adding safety; a production pipeline offloads for any claim with >1 arithmetic operation OR any claim that will be cited in writing, whichever is stricter. The position holds at the "will be cited in writing" threshold; it is overstrict if applied to every single draft sentence.

**Q18** — Refute, but with a *narrower* moat than the April draft claimed and a real new threat. The category-death pressure is no longer just BI incumbents; as of May 2026 Anthropic itself ships Claude for Financial Services agent templates (month-end closer, GL reconciler, and eight more) into categories 1–2, and Menlo's 2025 survey shows 76% of AI use cases are now bought rather than built.[^19] Data points for refutation: (a) no BI incumbent nor horizontal template yet matches the mid-market insight-density bar on *cross-functional* weekly reporting — Looker AI, Tableau Pulse, Metabase AI stay descriptive, and the finance-agent templates are scoped to finance workflows, not the CEO's cross-functional Monday brief; (b) the AI-native entrants (Hex, Mosaic, Pigment) have velocity but not horizontal distribution and are moving upmarket into category 2; (c) category-4 value lives in the voice-transferred, source-specific narrative layer — the layer both BI vendors and horizontal templates have the weakest muscle around. Hedge: if a frontier lab ships a horizontal, voice-configurable, cross-source weekly-report agent, category 4 compresses fast. The defensible lane is now "the report a horizontal template can't govern or voice for this specific client," and it is 18–36 months, not open-ended.

**Q19** — Defend for solo-operator specifically. Mechanism: Claude Code is the orchestrator you are already running; LangGraph/Pydantic AI add a dependency layer for capabilities (stateful graph, typed deps) that a weekly-scheduled deterministic pipeline doesn't need. Anthropic's *Building Effective Agents* (Dec 2024) is explicit that prompt-chain and orchestrator-workers workflows — both trivially expressible as Claude-Code-driven Python — beat agent frameworks for predictable workflows.[^12] The build-experience argument: in a Saturday 6–8 hour sprint, adding LangGraph means ~90 minutes of framework scaffolding before first working run; Claude Code hits first working run at ~45 minutes. Concession: at 5+ concurrent report-types with shared state and human-in-the-loop approval steps, LangGraph's stateful primitives earn their weight. Below that, YAGNI.

**Q20** — Refute for audit-critical financial tables through 2027; concede for general business documents. Jerry Liu's position (LlamaIndex blog, 2024/25): specialised pipelines with structure-aware chunking produce more *auditable* failures than VLMs because parse errors are explicit rather than hallucinated-value-that-looks-plausible.[^16] Brandon Smock's PubTables-1M / Table Transformer work (CVPR 2022): task-specific table models beat general VLMs on hierarchical and merged-cell tables by material margins, and the gap has not closed in 2025.[^18] Concession: for layout-heavy documents without audit surface (board decks, infographics, internal reports), native VLMs are already sufficient and will dominate. The specialised-pipeline moat is verticals where audit + table pathology + regulatory scrutiny coexist — which remains a 24–36 month defensible position.

---

## 40 flashcards

*Format: front ↔ back. Anki-importable.*

1. Q: Six-stage AI analyst worker pipeline? → A: Category pick → parse → connect → verify → generate → ship.
2. Q: Stage-1 failure mode? → A: Category confusion in the pitch (client benchmarks against wrong incumbent's disclosed number).
3. Q: Four categories of "AI reads your business"? → A: (1) Financial-close automation, (2) Management reporting / CPM, (3) Competitive/market intelligence, (4) Operational reporting.
4. Q: Brex Fall 2025 disclosed number? → A: ~70% of expenses handled entirely by automation; books close 3x faster; expenses reviewed 6x faster.
5. Q: Ramp procurement-agent disclosed numbers (April 2026)? → A: 16% average annual savings on vendor spend; 46 hours/month of manual purchasing work eliminated per customer. ($44B valuation, June 2026.) (The April draft's "$163M / 208,000 hours" pair was unverifiable and mis-attributed to the 2023 Ramp Intelligence launch — replaced.)
6. Q: Hex (Barry McCardel) counter-thesis (April 2024)?[^14] → A: Paraphrase — AI without analysts ships confidently-wrong reports that pass casual review but fail audit (McCardel's own framing is closer to "imagine you worked with a Data Scientist who, while knowledgable and sharp, was well-known for hallucinating, making up facts"). Three load-bearing claims from the post: (1) data work transcends coding — analysts do stakeholder engagement, experiment design, and decision influence; (2) demand for insights is effectively unlimited, so AI efficiency raises headcount rather than cutting it; (3) humans provide the accountability dimension AI cannot.
7. Q: FinanceBench headline (Islam et al., arxiv 2311.11944)? → A: GPT-4-Turbo with retrieval refused or incorrectly answered 81% of 150 manually-reviewed 10-K questions. Root cause: parser splitting tables across chunks.
8. Q: Five document-parsing archetypes? → A: (1) Specialised OSS (Unstructured, Docling, Marker, LiteParse), (2) Hosted gen-AI-first (LlamaParse; LlamaExtract now a separate product; Reducto, Chunkr), (3) Native-multimodal (Claude Vision, GPT-5.x Vision, Gemini 3.1 Pro), (4) Cloud document-AI (Textract, Doc AI, Form Recognizer), (5) Academic specialists (Nougat, GROBID).
9. Q: Unstructured SCORE-Bench lesson? → A: Parser rankings invert across TEDS, NED, GriTS on the same corpus. A single leaderboard number is noise until anchored to a document class.
10. Q: Docling launch facts? → A: IBM Research Zurich, July 2024 open-source, TableFormer table model, layout model on 81,000 DocLayNet pages, ~5pp of human classification, 30x speedup avoiding OCR on digital-native PDFs.
11. Q: LlamaParse launch facts? → A: Jerry Liu, Feb 2024, "first parser built with genAI," ~10x cheaper than frontier-VLM-only at comparable robustness on mixed corpora. Schema-guided extraction has since split out into the separate LlamaExtract product.
12. Q: Procycons 2025 LlamaParse vs Gemini 3 Pro benchmark? → A: LlamaParse ChrF++ 81, Gemini 3 Pro edit-similarity 88; LlamaParse leads on robustness metrics, Gemini leads on raw similarity.
13. Q: Anthropic native PDF limits (2026)? → A: 32 MB max request; 600 pages per request on 1M-context models, 100 pages when the request's context window is under 1M tokens. (The old flat "100-page envelope" was the 200k-context number.)
14. Q: MCP governance status (2026)? → A: Launched Nov 25 2024 (reference servers: Google Drive, Slack, GitHub, Git, Postgres, Puppeteer); now under the Linux Foundation's Agentic AI Foundation (donated Dec 9 2025, co-founded with Block + OpenAI), with an official Registry (Sept 2025), the 2025-11-25 spec release, and a 2026-07-28 stateless-core RC in flight. No longer "Anthropic's protocol." The Postgres reference server is archived + SQLi-vulnerable — use a maintained one.
15. Q: Willison lethal trifecta (when coined)? → A: Coined June 16, 2025 (not the earlier April MCP prompt-injection post). Private data access + untrusted content exposure + external communication ability. Any one is safe; all three is exploitable confused-deputy.
16. Q: Willison "rug pull" attack class? → A: MCP server silently mutates tool definitions after user approval. Mitigation: no auto-approve in prod; diff-on-change alerts.
17. Q: PostgreSQL RLS multi-tenant pattern? → A: Every tenant-scoped table has `tenant_id` column; policies `USING (tenant_id = current_setting('app.tenant_id')::int)`; MCP server sets `app.tenant_id` via `SET LOCAL` per session.
18. Q: Presidio? → A: Microsoft open-source PII detection; Analyzer (NER+regex) + Anonymizer (redact/hash/replace); LiteLLM first-class integration.
19. Q: EDPB Opinion 28/2024? → A: Dec 2024 authoritative EU guidance that Article 5 GDPR principles (data minimisation, purpose limitation) apply throughout AI model development and deployment.
20. Q: HIPAA HTI-1 final rule effective date? → A: Jan 1, 2025. Introduced Decision Support Intervention transparency requirements for certified health IT.
21. Q: PCI DSS 4.0 / 4.0.1 dates? → A: v4.0 mandatory March 31, 2024; v4.0.1 active end of 2024; future-dated requirements enforceable March 31, 2025.
22. Q: Numerical-reasoning failure taxonomy? → A: (1) Aggregation off-by-one, (2) unit/scale confusion, (3) sign error, (4) hallucinated column, (5) rounding compounding, (6) out-of-sandbox hallucination in narration.
23. Q: FinQA scale and gap? → A: 8,281 expert-annotated financial QA pairs (Chen et al. EMNLP 2021, arxiv 2109.00122); original GPT-3 baseline 48.56% numerical reasoning vs ~89% human.
24. Q: PAL (Program-Aided LMs) headline? → A: +6.4 over CoT on GSM8K with smaller model (PAL-Codex 72.0% vs CoT 65.6%). Arxiv 2211.10435, Gao et al., ICML 2023.
25. Q: Anthropic code-execution tool pricing (2026)? → A: $0.05/container-hour after a free monthly allowance (~1,550 container-hours/month per org); free when bundled with the current `web_search_20260209` / `web_fetch_20260209` tool versions. Current tool-type versions are `code_execution_20260521` / `code_execution_20260120` (bash + multi-language + file manipulation).
26. Q: Self-consistency headline? → A: Wang et al., arxiv 2203.11171, +17.9% on GSM8K over chain-of-thought via majority vote on N sampled reasoning paths.
27. Q: Huang 2024 (arxiv 2310.01798) headline? → A: Large Language Models Cannot Self-Correct Reasoning Yet. Intrinsic self-correction fails on GSM8K, CommonSenseQA, HotpotQA; works only with valid external feedback (code execution, retrieval, rule check).
28. Q: Evaluator-critic three conditions? → A: (1) External signal the generator lacks, (2) domain-specific failure taxonomy in the prompt, (3) flag-and-reroute, not overwrite.
29. Q: Typical numerical-accuracy stack gain? → A: Single-shot CoT ~68% → generator + code execution ~86% → generator + code execution + critic with forced tool-use ~94% on a 30-question weekly-ops eval. Indicative single-operator pilot figures — the ordering is robust, the exact digits are not; run the three-arm eval on your own corpus.
30. Q: Four report-generation patterns (Friday)? → A: (1) Templated slot-fill, (2) narrative synthesis (rubric-constrained), (3) chart-generating (Vega-Lite / Plotly / Mermaid), (4) voice-transferred narrative.
31. Q: Insight-vs-description gap? → A: Description: "revenue rose 4%." Insight: "revenue rose 4% despite 12% drop in largest channel because X compensated — fragile if Y reverts." LLMs default to description; few-shot + forced-contrast + adversarial critic closes the gap.
32. Q: Named-operator voices to transfer-test? → A: Austin Rief (Morning Brew), Packy McCormick (Not Boring), Ben Thompson (Stratechery), Lenny Rachitsky.
33. Q: Anthropic *Building Effective Agents* (Dec 2024) key patterns? → A: Prompt-chain, orchestrator-workers, evaluator-optimiser, parallelisation, routing. Prefer explicit pipeline over autonomous agent for predictable workflows.
34. Q: Claude Code vs LangGraph for solo-operator weekly generator? → A: Claude Code wins for first working run speed and YAGNI; LangGraph earns its weight at 5+ concurrent report-types with shared state + human-in-the-loop approval.
35. Q: Observability free tier options? → A: LangSmith free tier, Braintrust free tier, Helicone free tier, Arize Phoenix (OSS self-host). Wire from day 1.
36. Q: Hamel Husain eval-driven-development core claim? → A: Single strongest predictor of production AI product working is whether team built eval harness before first generation run. Hand-check 100% of evals ≤20 docs; sample-check larger sets.
37. Q: LLM-as-judge calibration requirement? → A: 100+ labeled examples for reliability; judge model-and-prompt must be different from generator; judge must cite its tool output for every verdict (Hamel Husain).
38. Q: Cache strategy for parsed markdown? → A: SHA-256 of raw bytes as key; store in Postgres/S3/KV; survive across sessions (Anthropic gateway only caches 15 min intra-session).
39. Q: Single-point-of-failure fallback pattern? → A: Last-known-good template + email alert + weekly run skipped with explicit "data pipeline unavailable, no report this week" notification. Fail loud, never fail silent with stale data.
40. Q: One-line rule for whether Week 5 is installed? → A: You can (a) name the report's category and the incumbent whose disclosed number the client will compare it to, (b) sketch the parser + connector + verifier + generator + shipper stack, (c) write the schema with typed units, (d) cite FinanceBench-PAL-Huang-MCP-Willison from memory, and (e) commit to a 30-day rollout with a named human spot-check gate.

---

## Open questions — what's not settled this week

1. **Does the Pigment/Mosaic "Analyst Agent" pattern surface genuine insight or fluent description?** No published head-to-head eval vs human analyst output at paragraph-level insight density as of April 2026. Pigment's position: yes. Hex's position: no, by construction. An eval harness built from Thursday's discipline can fill the gap; the resolution matters for category-2 build-vs-buy.

2. **Does the Contextual Retrieval 49% retrieval-miss reduction transfer to financial-document QA?** Anthropic's five test domains did not include financial filings. No published FinanceBench-with-Contextual-Retrieval head-to-head. If you run one, publish it.

3. **How long does the category-4 weekly-report lane stay open?** Now threatened from two sides: BI incumbents (Tableau Pulse, Looker AI, Metabase AI) shipping mid-market narrative generation, *and* horizontal frontier-lab agent templates (Claude for Financial Services, May 2026) plus the buy-over-build tide (Menlo 2025: 76% bought). The defensible lane narrowed to cross-functional, source-specific, client-voiced reporting the templates can't reach — call it 18–36 months, not open-ended.

4. **Does MCP win the connector-layer war, or get absorbed?** Partially *resolved* since April: MCP became multi-vendor infrastructure under the Linux Foundation's Agentic AI Foundation (Dec 2025), with an official Registry and a 2026-07-28 stateless-core RC. Residual open questions are narrower — the security model is still maturing (measured incidents now exist: CVE-2025-6514, postmark-mcp), and the real integration work (auth refresh, rate limiting) still lives in each server, which is why server provenance is a governance property. Possible 2027: MCP stays the discovery/metadata layer; heavy tool implementations migrate to opinionated frameworks.

5. **Is read-only posture durable or transient?** Read-only is the right default today. Ramp CEO's three-year autonomous-finance horizon implies writes eventually. Likely 2027 shape: "AI drafts proposed write → deterministic validator → structured approval queue" — workflow Brex and Ramp already implement.

6. **Does AI flatten the analyst headcount curve, or bend it upward (demand unlock)?** No longer data-free: the Stanford×ADP "Canaries" series (Brynjolfsson/Chandar/Chen) shows ~16% *relative* employment decline for 22–25-year-olds in the most AI-exposed occupations through late 2025, cutting against demand-unlock for junior roles specifically. Open at the senior/insight tier. Monday's "no public longitudinal data yet" claim is now false — the live dashboard is the data.

---

## Reviewer lens — where you'd still lose points

1. **Category-to-build-pitch mapping is US-defaulted.** A Morgan Lewis-style AI contracting critic would note that EU deployments against category-1 workflows pull in DORA (financial services operational resilience, 2025), DPDP Act (India), and NYDFS Part 500 (financial services cybersecurity). Your SOW template from Block 1 Week 1 needs regional adaptation for category-1 specifically.

2. **Your FinanceBench numbers are the starting line, not the finish.** A Hamel Husain-style critic[^13] would push that FinanceBench is a reference benchmark, not your production eval. Every client engagement needs a domain-specific 20-question eval that looks like the client's actual documents and reader. Running FinanceBench proves architecture; running your domain eval proves fit.

3. **Your "MCP replaces LangChain loaders" defensive framing is premature.** A Harrison Chase-style critic would hold that loaders and MCP solve different problems (batch ingestion into RAG index vs runtime tool invocation) and production systems have both. Any synthesis that treats them as substitutes misses the adapter layer (`langchain-mcp-adapters`) that Harrison's team shipped specifically to eliminate the false choice.

4. **"Voice transfer is a moat" is an insight-density claim, not a moat claim.** A Packy McCormick-style critic would note that voice is the moat *for Packy*, not for the AI that imitates Packy. Voice-transfer-fidelity lift plateaus above ~4/5 hand-graded scores and the remaining delta is cultural context the model cannot access. Sell it as differentiated fidelity, not as an imitate-any-writer promise.

5. **Your eval-harness discipline bankrupts if the client's corpus shifts.** A Chip Huyen-style critic would note that any eval captured once and frozen decays within a quarter as the underlying business shifts (new product line, new channel, new geography). Build the eval with a refresh cadence (monthly sample-refresh, quarterly full regeneration) or the "94% accuracy" number you cited on week 1 is 78% by week 12 and you don't notice.

6. **"Ship in 6–8 hours" is a build-time, not a production-time claim.** Anyone who has shipped an AI worker for real will push back: the 6–8 hours is the scaffold; the next 40 hours are the eval harness, the observability wiring, the failure-mode drilldowns, the voice calibration, and the 30-day rollout babysitting. Price accordingly; the Saturday sprint is the proof of concept, not the deliverable.

---

## Further reading

**Must-read (≤5):**
- Anthropic, *Building Effective AI Agents* (Dec 2024) — orchestrator-workers, prompt-chain, evaluator-optimiser patterns underpinning Saturday's build.[^12]
- Islam et al., *FinanceBench* — arxiv.org/abs/2311.11944, the benchmark that reframed "RAG accuracy" as "parser accuracy" and anchored Thursday.[^3]
- Huang et al., *Large Language Models Cannot Self-Correct Reasoning Yet* — ICLR 2024, arxiv.org/abs/2310.01798, the paper every evaluator-critic loop must answer to.[^11]
- Anthropic, *Introducing the Model Context Protocol* (Nov 25, 2024) + Simon Willison's *Model Context Protocol has prompt injection security problems* (April 9, 2025) — read as a pair.[^6][^5]
- Hex / Barry McCardel, *We're not building 'AI data scientists'* (April 16, 2024) — the counter-thesis every replacement-framing pitch must engage.[^14]

**Recommended:**
- Jerry Liu, *Introducing LlamaCloud and LlamaParse* (Feb 2024).[^16]
- Gao et al., *PAL: Program-Aided Language Models* (arxiv 2211.10435, ICML 2023).[^9]
- Hamel Husain, *Using LLM-as-a-Judge For Evaluation* (hamel.dev/blog/posts/llm-judge/).[^13]
- Unstructured, *SCORE-Bench* (2025).[^4]
- IBM Research, *Docling open-source launch* (Nov 2024).[^15]
- EDPB, *Opinion 28/2024 on AI models* (Dec 2024).[^7]

**Optional:**
- Patronus AI FinanceBench GitHub + Hugging Face dataset — the 150-question open subset.
- Anthropic *Advanced Tool Use* engineering post (Oct 2025).[^10]
- Kamoi et al., *When Can LLMs Actually Correct Their Own Mistakes?* (TACL 2024).
- PCI DSS v4.0.1 (PCI SSC, end 2024).
- Brex *Intelligent Finance* platform page + Fall 2025 release.[^1]

---

## Capstone — one end-to-end AI analyst worker, shipped in 30 days

Pick **one real client (or yourself)** for whom you will ship an AI analyst worker in the next 30 days. Write the one-page spec, then commit to the schedule.

**The spec (1 page):**

1. **Scope.** Report type + cadence + reader. Name the reader. Name the exact before-state labor the report replaces (hours/week, blended rate, 52-week annualised cost).
2. **Input sources.** The 3–5 connectors you will use, each with MCP/SDK/loader/iPaaS pick and rationale (Wednesday).
3. **Doc-parsing pipeline (if applicable).** Archetype + tool + cache strategy + eval set size (Tuesday).
4. **Numerical-reasoning mitigation.** The code-execution sandbox, the `units`-enforced tool schema, the evaluator-critic prompt, the 20-question eval set with gold hand-verification (Thursday).
5. **Generation pattern + voice.** Templated / narrative / chart-generating / voice-transferred, with named operator voice if transferring; structured-output schema with Pydantic validation (Friday).
6. **Deployment + observability + fallback.** Target (Cron / Modal / Railway / Airflow / n8n), observability vendor (Braintrust/LangSmith/Helicone free tier), single-point-of-failure fallback, kill-switch (Saturday).
7. **30-day rollout + kill criteria.** Human spot-check gate on first N reports, sunset criteria, metric the gate is measured on, kill criteria if the report is wrong at audit-surface in any of the first 4 weeks.

**The commitment:**

- **Week 1 (by Saturday Day 7 of your own build):** scaffold + first end-to-end dry run on real data. At least one numerical claim verified via code execution. Observability wired.
- **Week 2:** ship first real report to the real reader, human spot-check in the loop. Log every correction the reader requests.
- **Week 3:** iterate on voice fidelity + insight density based on week-2 corrections. Build the 20-question regression eval against 3 prior weeks of manually-produced reports.
- **Week 4:** run the regression eval + decide on gate-lift. If accuracy ≥ pre-committed threshold and voice fidelity ≥ 4/5 *on the Friday Layer-2 rubric* (named-operator-voice fidelity + insight-density + distinctiveness, hand-graded by the same reviewer who calibrated the eval), gate comes off to sample-check (1-in-4). If not, stay on spot-check, iterate on the failure mode, regenerate the eval at week 8.

The spec is the artifact. The commitment is the Week 5 test. Come back in 30 days with the report shipped and a written postmortem on where the pipeline broke — that postmortem is the grounding for every client pitch of an AI analyst worker you make in Block 3 and beyond.

---

## Citations

[^1]: Brex, "Agents on Brex: Welcome to intelligent finance." https://www.brex.com/platform/intelligent-finance. Verified 2026-04-17. Supports the 70% expenses-automated, 3x faster close, 6x faster expense review figures.

[^2]: Ramp, "Ramp Launches Fleet of AI Agents Across Its Procurement Platform," April 29, 2026. https://www.prnewswire.com/news-releases/ramp-launches-fleet-of-ai-agents-across-its-procurement-platform-302756657.html; plus "Ramp Raises Series F at $44 Billion Valuation," June 4, 2026, https://www.prnewswire.com/news-releases/ramp-raises-series-f-at-44-billion-valuation-302791103.html. Verified 2026-07-17. Supports: 16% average annual vendor-spend savings, 46 hours/month of purchasing work eliminated, $44B valuation. (Replaces the April draft's unverifiable "$163M / 208,000 hours" pair.)

[^3]: Islam, P., Kannappan, A., Kiela, D., Qian, R., Scherrer, N., Vidgen, B. (2023). *FinanceBench: A New Benchmark for Financial Question Answering.* arXiv:2311.11944. https://arxiv.org/abs/2311.11944. Verified 2026-04-17. Supports the 10,231-question scope, 150-question open subset, and the GPT-4-Turbo-with-retrieval 81% refuse-or-wrong headline.

[^4]: Unstructured.io, "Introducing SCORE-Bench: An Open Benchmark for Document Parsing" (2025). https://unstructured.io/blog/introducing-score-bench-an-open-benchmark-for-document-parsing. Verified 2026-04-17. Supports TEDS/NED/GriTS ranking instability across corpora.

[^5]: Simon Willison, "The lethal trifecta for AI agents," June 16, 2025, https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/ (where the term is coined — not the earlier April 9, 2025 MCP prompt-injection post, https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/). Verified 2026-07-17. Supports the prompt-injection-via-tool-response class, rug-pull silent-redefinition, and the lethal-trifecta framing (coined June 16, 2025).

[^6]: Anthropic, "Introducing the Model Context Protocol," Nov 25, 2024, https://www.anthropic.com/news/model-context-protocol; plus "Donating the Model Context Protocol and establishing the Agentic AI Foundation," Dec 9, 2025, https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation; and the 2026-07-28 release candidate, https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/. Verified 2026-07-17. Supports launch date and reference servers, plus the official Registry (Sept 2025), 2025-11-25 spec release, Dec 9 2025 AAIF donation, and 2026-07-28 stateless-core RC.

[^7]: European Data Protection Board, "Opinion 28/2024 on certain data protection aspects related to the processing of personal data in the context of AI models," Dec 2024. https://www.edpb.europa.eu/system/files/2024-12/edpb_opinion_202428_ai-models_en.pdf. Verified 2026-04-17. Supports Article 5 GDPR principles applied to AI model deployment.

[^8]: Chen, Z. et al. (2021). *FinQA: A Dataset of Numerical Reasoning over Financial Data.* EMNLP 2021, arXiv:2109.00122. Verified 2026-04-17. Supports the 8,281-pair scope, gold-program annotation, and 48.56% GPT-3 numerical-reasoning baseline vs ~89% human.

[^9]: Gao, L. et al. (2023). *PAL: Program-Aided Language Models.* arXiv:2211.10435, ICML 2023. https://arxiv.org/abs/2211.10435. Verified 2026-04-17. Supports the PAL-Codex 72.0% vs CoT 65.6% GSM8K comparison.

[^10]: Anthropic, *Code Execution Tool* docs, https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool, and pricing, https://platform.claude.com/docs/en/about-claude/pricing. Verified 2026-07-17. Supports the Python/bash/multi-language sandbox (current tool types `code_execution_20260521` / `code_execution_20260120`), $0.05/container-hour after a free monthly allowance (~1,550 container-hours/month per org), and bundled-free with the current `web_search_20260209` / `web_fetch_20260209` tool versions.

[^11]: Huang, J. et al. (2024). *Large Language Models Cannot Self-Correct Reasoning Yet.* arXiv:2310.01798, ICLR 2024. Verified 2026-04-17. Supports intrinsic-self-correction-fails claim and external-feedback-works caveat.

[^12]: Anthropic, *Building Effective AI Agents*, Dec 2024. https://www.anthropic.com/research/building-effective-agents. Verified 2026-04-17. Supports the orchestrator-workers, prompt-chain, evaluator-optimiser, routing, parallelisation patterns.

[^13]: Hamel Husain, *LLM Evals: Everything You Need to Know* (Evals FAQ), hamel.dev, updated Jan 2026. https://hamel.dev/blog/posts/evals-faq/. Plus *Using LLM-as-a-Judge For Evaluation*, Oct 2024. https://hamel.dev/blog/posts/llm-judge/. Verified 2026-04-17. Supports the "100+ labeled examples, ongoing weekly maintenance" line for LLM-as-judge and the critique-shadowing calibration discipline.

[^14]: Hex / Barry McCardel, *We're not building 'AI data scientists,'* April 16, 2024. https://hex.tech/blog/no-ai-data-scientist/. Verified 2026-04-17. Supports the three-part counter-thesis and the "AI drafts, human publishes" framing.

[^15]: IBM Research, "IBM is open-sourcing a new toolkit for document conversion," Nov 12, 2024. https://research.ibm.com/blog/docling-generative-AI. Verified 2026-04-17. Supports Docling open-source launch, TableFormer, 81,000 DocLayNet pages, ~5pp of human classification, 30x OCR-avoidance speedup.

[^16]: Jerry Liu, "Introducing LlamaCloud and LlamaParse," LlamaIndex Blog, Feb 2024. https://blog.llamaindex.ai/introducing-llamacloud-and-llamaparse-af8cedf9006b. Verified 2026-04-17. Supports LlamaParse launch date and "first parser built with genAI" framing.

[^17]: DocVQA leaderboard at https://llm-stats.com/benchmarks/docvqa and the AndesVL technical report arxiv 2510.11496. Verified 2026-07-17. Supports 2025 SOTA DocVQA/ChartQA scores and frontier-VLM positioning. (Current native-multimodal roster: Claude Vision, GPT-5.x Vision, Gemini 3.1 Pro, Qwen-VL — the April draft's "GPT-4o/5, Gemini 2.5 Pro" names are two generations stale.)

[^18]: Smock, B., Pesala, R., Abraham, R. (2022). *PubTables-1M: Towards comprehensive table extraction from unstructured documents.* CVPR 2022, arXiv:2110.00061. https://arxiv.org/abs/2110.00061. Verified 2026-07-17. Supports task-specific vs general-VLM table extraction gap on hierarchical/merged-cell tables.

[^19]: Anthropic, "Agents for financial services," May 5, 2026, https://www.anthropic.com/news/finance-agents (plus "Use Claude for Excel," https://support.claude.com/en/articles/12650343-use-claude-for-excel); Menlo Ventures, "2025: The State of Generative AI in the Enterprise," Dec 9, 2025, https://menlovc.com/perspective/2025-the-state-of-generative-ai-in-the-enterprise/. Verified 2026-07-17. Supports: Anthropic's ten finance agent templates (month-end closer, GL reconciler, etc.) + GA Excel add-in entering categories 1–2, and Menlo's finding that 76% of AI use cases are bought rather than built (up from 53%). Model-lineup detail (Fable 5 / Mythos 5 above Opus, Opus 4.8, Sonnet 5): https://www.anthropic.com/news/claude-fable-5-mythos-5.

[^20]: Datadog Security Labs, "MCP vulnerability case study: SQL injection in the PostgreSQL MCP server," 2025, https://securitylabs.datadoghq.com/articles/mcp-vulnerability-case-study-SQL-injection-in-the-postgresql-mcp-server/; `modelcontextprotocol/servers-archived`, https://github.com/modelcontextprotocol/servers-archived; maintained alternative `crystaldba/postgres-mcp`, https://github.com/crystaldba/postgres-mcp. Verified 2026-07-17. Supports: the archived `@modelcontextprotocol/server-postgres` reference server (archived May 29, 2025, "NO SECURITY GUARANTEES"), the documented stacked-query bypass of its read-only mode, and the maintained `crystaldba/postgres-mcp` `--access-mode=restricted` alternative.

---

_last_verified: 2026-04-17_
