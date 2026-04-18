---
type: lesson
block: block-2-ai-employees
week: week-05
day_of_cycle: 6
day_name: sat
session_slug: build-weekly-business-report-generator
date_due: 2026-06-20
tags:
  - orchestration
  - claude-code
  - langgraph
  - evaluator-critic
  - eval-harness
  - observability
  - deployment
  - report-generator
  - build-day
  - production-llm
sources:
  - anthropic-building-effective-agents-2024
  - langgraph-1-0-ga-2025
  - anthropic-claude-code-subagents-2025
  - hamel-husain-evals-faq-2026
  - boris-cherny-workflow-2025
  - braintrust-observability-2025
  - langsmith-pricing-2025
  - arize-phoenix-docs-2025
  - prefect-airflow-dagster-2025
  - modal-cron-docs-2025
  - pydantic-ai-v1-2025
  - simonwillison-building-effective-agents-2024
last_verified: 2026-04-17
word_count_target: 6000
---

# Build the weekly business report generator — end-to-end, in a single Claude Code session, with eval + deploy + monitoring

## Why this matters

After this lesson you will have shipped — not described — a working AI analyst worker: a pipeline that on a schedule pulls data from a real source, parses whatever documents need parsing, verifies its own numbers through a deterministic runtime, drafts a narrative in a voice you chose, passes the draft through an evaluator-critic, renders the final report, and delivers it with a regression eval gate and an observability trace you can open and read. The sharp generalist will tell you "you can build that with Claude Code in a weekend." They are correct, but the sharp generalist will also ship a system that silently rots in week three because they skipped the eval harness, the single-point-of-failure fallback, and the cost model. The delta you will own after this day is the thing that survives that week three.

This is the synthesis day for Week 5. Every earlier lesson was a component: Monday framed the category, Tuesday parsed the documents, Wednesday wired the connectors, Thursday hardened the numbers, Friday shaped the generation. Today you compose. The value is not in any single component — most of them are fifty lines of orchestration code at this point — but in how you join them, where you insert the gates, and which of the three or four available architectures you commit to. You will finish with a running system and, more importantly, with a defensible position on the two live arguments of 2026: *do you orchestrate on Claude Code or on a framework?* and *do you pay the observability tax on day one?* The rest of Block 2 takes for granted that you have shipped something like this at least once.

## Prerequisites

- The Week 4 eval harness pattern (retrieval regression set, LLM-as-judge scoring, hit-rate@k). You are reusing it.
- One real connector from Wednesday: Postgres MCP, Stripe MCP, a Sheets/Airtable tab, or a dropped-CSV pattern. Anything that returns rows.
- Thursday's code-execution sandbox enabled in your Claude Code environment *or* an e2b/Modal/Riza endpoint you can call.
- A 2–4 hour uninterrupted block. The build is not long, but the feedback loop with Claude Code benefits from continuity.

## Layer 1 — The architecture decision: Claude Code vs LangGraph vs Pydantic AI vs CrewAI, for this specific shape of worker

The first decision is not a technology decision, it is a *shape* decision. A weekly report generator is a **scheduled, mostly-deterministic pipeline with a small number of LLM-gated decisions and one or two loops (the critic, and occasionally a retrieval re-query)**. It is not an autonomous agent. It is not a chat system. It is not a multi-agent swarm. Anthropic's December 2024 *Building Effective Agents*[^1] explicitly separates "workflows" (LLM-augmented pipelines with predefined control flow) from "agents" (LLMs that dynamically direct their own processes). A weekly report generator lives firmly in the workflow column and, inside that column, it is an **orchestrator-workers-plus-evaluator-optimizer hybrid**: an orchestrator stage plans the week's report against last week's schema diff, workers (each a narrowly-scoped tool call) fetch and verify, and an evaluator-optimizer loop tightens the narrative before render[^1].

Once you have named the shape, the framework question answers itself in most cases. The four options that matter in April 2026:

**Claude Code as orchestrator.** You write a top-level `report.md` plan, let Claude Code run it, and each "step" is either a Bash/tool invocation or a subagent call[^3]. Boris Cherny — the head of Claude Code — runs his own production work as five parallel Claude Code sessions with system-notification gating, not as a managed-framework graph[^5]. The advantage is brutal: the "framework" is your filesystem and a well-written CLAUDE.md. You get Claude Code's subagent isolation (each subagent in its own context window with its own tool grants[^3]) for free. The cost is that state across runs lives in whatever you persist to disk or DB; there is no built-in durable-execution guarantee.

**LangGraph 1.0** (released October 22 2025, the first stable major release in this space)[^2]. You model the pipeline as a state graph — fetch node, parse node, verify node, draft node, critic node, render node — with durable execution, built-in persistence, and native human-in-the-loop pause points[^2]. For a weekly report that actually matters (e.g. a board-pack page, a regulatory filing summary), LangGraph's durability guarantees are genuinely load-bearing: if Modal restarts your container mid-run, the graph resumes. Uber, LinkedIn, and Klarna run production agents on it[^2]. The cost is the learning curve and the framework-specific idioms; for a solo operator shipping the first version, it is overbuilt.

**Pydantic AI 1.0** (September 2025, type-safe, API-stability committed)[^11]. The right choice if your consumers are other systems — i.e. the report is not just a rendered markdown page for a human but a structured JSON payload feeding a downstream pipeline. Pydantic AI enforces schema at every boundary; in the Nextbuild 90-day benchmark cited by ZenML it scored 8/10 on developer experience, highest of five frameworks tested[^11]. For a solo-operator report generator the type-safety surface is underutilised; for a team shipping a report-generator *platform* with ten variants, it is the correct spine.

**CrewAI.** Role-based multi-agent collaboration, the largest GitHub community of the four (44.6k stars as of early 2026)[^11]. Wrong shape for this problem. CrewAI shines when the task is actually collaborative — research agent + writer agent + editor agent debating — and mis-shaped when the workflow is a mostly-linear pipeline with one critic loop. You will spend more time working around the Crew abstraction than benefiting from it.

**My recommendation, and the one this lesson builds on:** if you are a solo operator or a two-person team shipping your first weekly report generator, **orchestrate on Claude Code**, write subagents for the three or four irreducibly-LLM-gated steps (parse-unknown-document, draft-narrative, critic), and leave the scheduling to whatever your deployment target already gives you (Modal cron, Railway cron, a Mac mini with `launchd`). When you cross 50 reports/week, or any single report failure would be a six-figure business event, migrate the pipeline spine to LangGraph for durability — the migration is small if the subagent contracts are clean. This matches the Anthropic *Building Effective Agents* guidance almost word-for-word: *start with LLM APIs directly; add framework only when the added complexity is justified*[^1][^12].

Simon Willison's December 2024 read on the Anthropic piece put it more bluntly: the single best piece of advice in the paper is *"Don't use a framework"* until you have hit the wall that framework solves[^12]. For 90% of the readers of this lesson, the Claude-Code-as-orchestrator path is correct for version one, and the version-two migration is a known, bounded refactor.

## Layer 2 — The pipeline spine, end to end, with the gates in the right places

Here is the six-stage pipeline, written as an architecture not a listing. Each stage is a tool the orchestrator calls; each has a contract (what it takes in, what it returns, what it logs); each has a failure mode you will watch in production.

```
fetch  →  parse  →  verify  →  retrieve-context  →  draft  →  critic  →  render  →  deliver
  (W3)    (W2)      (Th)        (W4 RAG)          (F)      (Th+F)     (F)
```

**Stage 1 — fetch.** Uses Wednesday's connector choice. Contract: `fetch(period_start, period_end) → rows[]`. The orchestrator never touches raw credentials; the fetch tool is the only layer that holds the read-only service-account token. Log the row count, the distinct source tables touched, and the SHA-256 of the serialised result. The log is your cheap provenance layer: when someone asks in four weeks why the Week 12 revenue number disagrees with the ledger, you have a hash to compare against a replay.

**Stage 2 — parse.** Runs only for rows that contain document pointers (PDF URLs, S3 keys, attachment blobs). Uses Tuesday's pipeline choice. Contract: `parse(doc_ref) → structured_json`. Most weekly reports for most SMB verticals will skip this stage entirely — the inputs are already structured. Do not add parse for parse's sake. If your first version has no PDFs or scanned inputs, delete the stage from the orchestrator entirely; reintroduce when the first real document appears.

**Stage 3 — verify.** This is Thursday's code-execution offload, and it is where most pilot builds get lazy and pay for it. Contract: `verify(claim_set) → {claim_id: (value, provenance)}`. Every numerical claim in the final report must originate here. The orchestrator writes a set of claims as *questions the report intends to answer* (total revenue Q-over-Q; gross margin delta; top-3 churning accounts) and the verify tool computes each in Python against the fetched rows, returning both the computed value and the exact row references that produced it. The LLM is never allowed to produce a number in the draft stage that does not have a matching `claim_id`. If it tries, the critic catches it; if the critic misses, the render template refuses to substitute and the build fails loud. The cost of this architecture is real — Patronus FinanceBench documented that frontier models with retrieval still refused or incorrectly answered 81% of questions on real 10-K filings at the original 2023 evaluation, and while the gap has closed on simple aggregations, the structural failure modes have not — but the cost of skipping it is a Monday email with the wrong revenue number to your CEO.

**Stage 4 — retrieve-context.** Uses Week 4's RAG pattern to pull prior-period reports, definitions, any glossary the narrative needs. Contract: `retrieve(query, k=5) → chunks[]`. The retrieval set is *not* the full data warehouse; it is the report archive plus a small domain glossary. Keep it small. A solo operator's retrieval index at version one is 20–40 prior reports and one FAQ document. This is the stage where people reach for GraphRAG, contextual retrieval, agentic reranking, and other Week 4 sophistication; resist. The embedding-over-40-docs pattern is adequate for the first three months; revisit if retrieval is measurably the failure mode in your eval.

**Stage 5 — draft.** Friday's narrative pattern, constrained by the schema, fed the verified claims and the retrieved context. Contract: `draft(schema, claims, context, voice_spec) → draft_report`. The draft tool is a subagent in Claude Code (or a typed agent in Pydantic AI, or a node in LangGraph); it is *not* the orchestrator. Separation matters because the draft stage wants a long context and a specific system prompt; the orchestrator wants a short context and a decision-making prompt. Mixing them wastes tokens and fragments voice.

**Stage 6 — critic.** An evaluator-optimizer loop per Anthropic's pattern[^1]. Contract: `critic(draft) → {verdict: pass|revise, issues: [...]}`. The critic has three jobs in order of importance: (1) *every number in the draft maps to a claim_id*; (2) *no sentence asserts causality that is not in the claim set* ("revenue rose *because* churn dropped" requires a claim linking the two; absent that, rewrite as correlation); (3) *voice and rubric compliance*. If verdict is revise, feed `issues` back to the draft tool with an explicit "keep everything else, change only these" instruction. Cap the loop at N=2; if it still fails, hand to human. Andrej Karpathy's skeptical read of self-correction — that the same model grading its own work can compound rather than correct errors — is correctly raised here, and it is why the first critic job (the numerical-provenance check) is fully deterministic and the second (causality) uses few-shot examples rather than free judgement[^1].

**Stage 7 — render.** Friday's chart + markdown pattern. Deterministic, template-driven. If you are rendering to a PDF or a Notion page, this is where the adapter lives. Contract: `render(approved_draft) → delivery_artifact`.

**Stage 8 — deliver.** Posts to Slack, emails, writes to Notion, pushes to a storage bucket, whatever the consumer wants. The only thing worth saying about this stage: *log the delivery*. A weekly report that "shipped" but was not in fact received is the modal failure of Q1 of most deployments, and it is always a plumbing problem not an AI problem.

Two decisions at this seam are load-bearing and most tutorials hide them:

**Where do you insert the human gate?** For the first 4–8 weeks of production, place a human gate between stage 6 (critic) and stage 7 (render). Not a sign-off form — a Slack message with the draft and a thumbs-up. The gate is the training data for your eval: every time the human edits, that edit is a labelled failure mode you add to the regression set. LangGraph makes this gate a first-class concept with native pause-for-input APIs[^2]; in Claude Code you implement it as a subagent that writes to Slack and blocks on a reply. After 4–8 weeks of near-zero edits, retire the gate. Hamel Husain's repeated field observation is that teams who skip this phase ship less-evaluated systems and carry more latent risk, not more velocity[^4].

**Where do you fail loud, and where do you fallback?** Fail loud on any verify failure — if the numerical provenance does not check, the build dies and a human gets paged. Fallback silently on any retrieve-context failure — if prior-period retrieval returns empty, the draft stage degrades gracefully to a new-period-only narrative. This calibration is the cheapest insurance policy you will write.

## Layer 3 — The eval harness that justifies unattended operation

A weekly report generator is not an eval-optional deployment. The claim that distinguishes a toy from a product is *"over the last N weeks, this generator has maintained M% numerical-accuracy and P% narrative-quality against a gold regression set"*. Everything in this layer is about making that claim defensible.

**The regression set.** 5–20 prior periods of gold-standard reports. Gold means: a human wrote the report, a second human reviewed it, you know the exact input row set, and you know the exact output text. If you do not have historical reports, run the generator manually for 5 weeks with heavy human editing, capturing the edits; those five become the regression set (and the edits become the first revision of your critic prompt).

**The three metrics.** Borrow from Thursday but adapted:

1. **Numerical accuracy.** For every numerical claim in a generated report, was it equal to the gold report's claim within a documented tolerance (usually 0.5% for margin metrics, exact for counts)? Report as a percentage. Regression threshold: 99.5%. Anything below is a block-ship.
2. **Narrative quality — LLM-as-judge against rubric.** Claude Opus 4.7 grading each generated report against a 5-point rubric (insight density, voice fidelity, structure, no-hallucination, non-triviality) with the gold report as the calibration example. Use binary scoring per rubric dimension, not 1–5 scores — Arize's 2024/25 experiments and Hamel's pedagogy both converge on binary being more reliable[^4][^6]. Regression threshold: 80%+ pass rate on each dimension.
3. **Coverage.** Did the generator address all scheduled sections? Binary per section, averaged. Regression threshold: 100% — a missing section is a build failure, not a quality degradation.

**The LLM-as-judge bias caveat, explicitly acknowledged.** Zheng et al.'s 2023 and Hamel's 2024 posts both document that LLM-as-judge exhibits position bias, verbosity bias, and self-preference bias (models prefer text that looks like their own outputs)[^4]. Mitigations you will use: randomise ordering across runs; grade on rubric dimensions separately rather than overall preference; use a different-family model for the judge if budget allows (Claude generates, GPT-5 judges, or vice versa) for the narrative-quality metric only — numerical accuracy is deterministic and does not need this.

**The eval schedule.** Run the regression set on every prompt change, every model swap, and every scheduled Saturday morning against the current week's production run. The last one is non-negotiable: production drift shows up here before it shows up in the delivered report. This is the discipline Hamel's course drills into its 3,000+ graduates, and it is the single highest-leverage investment in the entire build[^4].

## Operator case studies — three specific weekly-report deployments and what broke

**Case 1 — Clippd (sports analytics, golf), July 2025.** Public write-up via the Dagster-vs-Prefect-vs-Airflow comparison literature: Clippd rebuilt their weekly data pipeline on Dagster and cut "over eight hours of manual data work each week," shifting from opaque pipelines to an org-wide data platform serving over 200 college golf programs[^9]. The interesting detail is not the hours saved, it is the architecture: Dagster's asset-centric model meant the "weekly insight page" was defined as a downstream asset of the underlying data tables, and the regeneration trigger was freshness of the upstream assets rather than a dumb cron. For report generators the lesson is: if the upstream data is bursty (e.g. the warehouse load finishes at variable times), scheduling on *upstream freshness* beats scheduling on *wall-clock time* — the report runs when the data is ready, not at a fixed hour.

**Case 2 — Brex, Ramp, and the financial-close category, 2024–2025.** The public claims — Brex's embedded AI close with specific cycle-time reductions, Ramp's Intelligence product posts on spend anomaly detection — are load-bearing evidence that *narrow* analyst-replacement workflows (expense categorisation, invoice coding, anomaly flagging) are shippable today. They are not evidence that open-ended "summarise our business" reports are shippable. The delta is the input distribution: Brex's model sees thousands of categorisation decisions with a clear feedback signal from the AP team; a weekly narrative report sees one composition decision per period with no clear feedback signal until a human reads it and frowns. Architect for your actual distribution. If your "report" is really a hundred small categorisation decisions stitched together, lean into the Brex/Ramp pattern; if it is a single narrative page, lean into the human-gate-then-eval-set pattern above.

**Case 3 — the Fédération Wallonie-Bruxelles pipeline migration (Dagster, 2025).** Belgium's public administration serving 4.5M citizens doubled pipeline delivery speed by moving from reactive maintenance to proactive data development[^9]. The part of that case relevant to solo operators is the smallest detail: the win was *pipeline authoring speed*, not pipeline runtime speed. A mature orchestrator (Dagster, LangGraph, or even well-organised Claude Code) halves the time to add a new report variant. For a freelance operator shipping the fifth weekly report for the fifth client, that authoring speed compounds into real margin. Plan your repo structure accordingly: one shared `tools/` library across all reports, one small `reports/<client>/` directory per deployment.

## Runnable experiment — build the generator, timed, with explicit milestones

This is the build log you will keep. Treat it as a shipping diary, not an architecture essay.

**Phase 0 (pre-work, 30 min).** Pick the three anchors: (a) one real data source — Postgres, Stripe, a Sheet, a CSV dump; a synthetic ledger with 500 rows if needed; (b) one report format from Friday — templated slot-filled is the fastest first version, move to narrative once the pipeline is stable; (c) one deployment target — Modal's free cron tier[^10] is the lowest-friction for a solo operator on any OS; Railway's Hobby plan at $5/month if you prefer their UX; Mac mini with `launchd` if you want to avoid any cloud bill. Set a hard total budget: $0–$5/month for version one.

**Phase 1 (hour 0–2, scaffold).** In a fresh Claude Code session, prompt:

> "Scaffold a weekly report generator project at `~/reports/<slug>/`. Structure: `orchestrator.py` entrypoint, `tools/` directory with one file per stage (fetch, parse, verify, retrieve, draft, critic, render, deliver), `config/` with `.env.example`, `schema.json`, `voice_spec.md`, `rubric.md`, and `evals/` with `gold/` (5 prior-period reports, empty for now), `regression.py` (the harness), `tests/`. Write the orchestrator as an explicit sequential pipeline per Anthropic's Building Effective Agents guidance — not an autonomous agent. Each stage is a function call with a typed input and typed output; the orchestrator logs timestamps, token counts, and cost. Use `.env` for the single API key; do not embed secrets. Generate a minimal CI script that runs regression.py against a fixture. Create a README that states the architecture, the per-stage contracts, and the decision points."

Read what Claude Code produces. Accept the parts that match the architecture in Layer 2; push back on any part where it invents an autonomous-agent or a multi-agent-crew pattern. This pushback is where the session becomes yours rather than a generic scaffold.

**Phase 2 (hour 2–4, tool implementation).** One at a time, each stage. Fetch first — wire to your actual data source, run once, eyeball the rows. Verify second — write the `claim_set` for your five most important numbers this week, implement each as a Python function against the fetched rows, compare against your own hand calculation. Draft third — write the system prompt and voice spec (200–400 words of real text, not a placeholder), run the draft subagent against the verified claims, read the output critically. Do not move to critic until the draft is good enough to be embarrassing-but-plausibly-human. Critic fourth — the three-job prompt from Layer 2, with the numerical-provenance check implemented deterministically in Python *before* the LLM critic runs. Render fifth — Markdown template, Vega-Lite JSON for the one chart, one-button export to your delivery format.

**Phase 3 (hour 4–5, eval harness).** Port Week 4 Saturday's harness. Add the three metrics from Layer 3. Run the harness against your gold set (or against 1–2 runs of the pipeline where you hand-graded the output). Record the baseline numbers. These are what you beat going forward; they are also the numbers you show a client to justify an unattended deployment.

**Phase 4 (hour 5–6, deploy + observability).** Modal or Railway cron pointing at `orchestrator.py`, scheduled for your real cadence. Wire observability: LangSmith free tier (5,000 traces/month)[^7] for trace collection, or Braintrust free tier (1M trace spans, 10K eval runs)[^6] if you want eval and tracing in one UI, or Arize Phoenix self-hosted if you want full open-source control[^8]. For version one, pick one and commit; stop re-evaluating vendors. The free tier of any of the three is enough for the first 3 months of a solo deployment.

**Phase 5 (hour 6–8, first real run + writeup).** Run end-to-end for one real period. Open the trace. Find the single step that took the most tokens and the single step that took the most wall-clock; write down why. Read the generated report as if you were the CEO who will receive it; list the three things that would embarrass you. Fix the worst one. Write 500 words on what broke, what surprised, what you would change in v2. This writeup is the artifact you show a prospect in Block 2's commercial-conversion conversation.

## Problem set

1. **Define the minimum viable eval for your generator.** Specify three metrics with thresholds tight enough that a failing run blocks ship. Include the tolerance for numerical accuracy and the LLM-as-judge rubric as binary dimensions. Estimate (with traces from your build) the cost per eval run at your current scale.
2. **Defend or refute:** "Claude Code as orchestrator beats LangGraph for a solo-operator weekly report generator in 2026, and the correct migration trigger is 50 reports/week or any single report failure being a six-figure event." Use your build experience and at least two cited sources.
3. **Write the 30-day rollout plan.** Name the human gate position, the exit criteria (when do you retire the gate?), the kill criteria (when do you roll back to the prior template-only process?), and the sunset trigger (under what condition does the generator get shut down as unworkable?). Two paragraphs max.
4. **Identify the single-point-of-failure in your pipeline and design the minimum fallback.** Must cover: detection (how do you know it failed?), degradation (what does the worst-acceptable output look like?), alert (who gets paged?). Write the fallback as a deterministic template that runs if the main pipeline fails.
5. **Cost the full system at three scales.** 1 run/week, 5 runs/week, 50 runs/week. Separate LLM inference cost, deployment cost, and observability cost. Identify the scale at which LLM cost dominates and the two optimizations (prompt caching, model routing, batch inference, retrieval narrowing) you would apply first. Your reasoning is the grading surface, not the exact numbers.

## Common failure modes at scale

**Silent drift after model swap.** You upgrade from `claude-sonnet-4-6` to `claude-opus-4-7` for quality, and the report's tone shifts noticeably without any prompt change. Caught by running the eval set immediately on model swap and comparing binary rubric pass rates. Fix: re-anchor voice with a style example in the system prompt, or pin the model version in config and gate upgrades behind eval-passing runs.

**Verify-stage silent success.** The verify tool returns a value for every claim, but one claim's function has a subtle bug — it sums the wrong column. Report ships with a confidently-stated wrong number. Caught by having the critic's numerical-provenance check re-compute claims from a *different* code path (e.g. the verify tool uses Pandas, the critic's check uses a DuckDB query over the same data). If the two paths disagree, fail loud. This is cheap and catches more errors than any prompt engineering.

**Token cost blow-up from retrieval.** Retrieve-context pulls too many chunks; draft stage context expands; a report that cost $0.14 last week costs $2.30 this week. Caught by logging token counts per stage and alerting on any stage exceeding its baseline by 3x. Fix: cap retrieve-context at a fixed token budget, prioritise chunks by recency and relevance.

**Delivery path rot.** Slack webhook URL rotated; Notion API key expired; email bounced. The pipeline "succeeded" but no one received the report. Caught by logging the deliver stage with a return code and surfacing failures to PagerDuty or a fallback email. Fix: health-check the delivery target before the run starts, not after.

**Evaluator self-preference on voice.** The critic grades voice fidelity by comparing to prior reports generated by the same model family, which biases toward its own idioms over time. Symptom: reports drift toward a generic-Claude voice over months. Fix: include the original hand-written exemplars in the critic prompt every time, and run a monthly manual voice review against the exemplars.

## Open questions — what is not settled

**Durable-execution vs keep-it-simple for solo operators.** LangGraph 1.0's durable execution is genuinely new and genuinely useful[^2]. The open question is whether a solo operator should adopt it preemptively or wait until a specific incident forces it. The Anthropic "start simple, add framework only when needed" position[^1][^12] argues the latter; the LangGraph team's "production agents need this" argues the former. Honest answer in April 2026: if your report is a $500/month deliverable to one client, stay simple; if it is a $10K/month deliverable to a regulated business, the durability is cheap insurance.

**LLM-as-judge for narrative quality, in production, unattended.** Hamel Husain's body of work shows LLM-as-judge *works* when it is calibrated against human labels and when the rubric is binary and narrow[^4]. The open question is whether that calibration decays over weeks without human spot-checks. There is no clean longitudinal study yet. Conservative position: re-calibrate the judge with 5 fresh human labels every 4 weeks. Cost is 20 minutes; insurance is real.

**Claude Code vs managed-agent platforms for the commercial play.** If you are shipping this to a client, do you package it as Claude Code plus a well-documented repo, or as a managed platform with a vendor's agent runtime? The managed-platform pitch is easier to sell ("we handle the infra"); the open-source-ish pitch is easier to sustain ("your code, your data, no lock-in"). In 2026 both are viable and the choice should be dictated by your client's procurement posture, not your technical preference.

## Reviewer lens — named critics with specific disagreements

- **Boris Cherny (Head of Claude Code, Anthropic)** would push back on Layer 1's suggestion that LangGraph becomes the right choice at 50 reports/week. His publicly documented workflow is *five parallel Claude Code sessions with system-notification gating*, not a framework[^5]. His counter-position: the scale threshold for migration is higher than most people think, and the "parallelism" problem is better solved at the session level than the graph level. Citation: the Boris-Uses-Claude-Code workflow write-up[^5]. The steelmanned response in this lesson is the explicit caveat that for most readers, Claude Code is the correct endpoint, not just the correct start.

- **Hamel Husain (parlance-labs.com)** would push back on the phrasing in Layer 3 that calls the eval harness "the discipline." Hamel's *Q: Should I practice eval-driven development?* post is explicit: writing evaluators *before* you have error data is an anti-pattern, because you cannot anticipate what will break[^4]. He advocates error-analysis-first, evals-after. Specific disagreement: where Layer 3 says "regression set of 5–20 prior periods," Hamel would say "fine, but do not write the rubric until you have seen two or three real failures; the rubric you pre-commit to is usually wrong." Citation: hamel.dev/blog/posts/evals-faq/should-i-practice-eval-driven-development.html[^4].

- **Harrison Chase (LangChain / LangGraph)** would push back on Layer 1's solo-operator recommendation of Claude Code. His case for LangGraph is that durable execution, checkpointer-based persistence, and the human-in-the-loop pause API are not "framework overhead" but "features you will need to rebuild by hand in Claude Code and will rebuild badly"[^2]. Specific disagreement: the claim that migration from Claude Code to LangGraph is a "small, bounded refactor" is optimistic; in practice, state contracts written under a stateless orchestrator rot when ported to a stateful graph. The honest response is that he is correct for teams shipping stateful long-running agents; for weekly reports where each run is independent, the state contract is trivial and the refactor *is* bounded.

- **Jerry Liu (LlamaIndex)** would push back on Layer 2's dismissal of retrieval sophistication at version one. His LlamaIndex Workflows and Contextual Retrieval work argues that even for small archives (20–40 prior reports), contextual chunking and reranking measurably improve retrieval hit-rate — and therefore narrative quality. Specific disagreement: the lesson's "keep it small, embed-over-40-docs is enough for three months" line probably is leaving 5–10% narrative-quality on the table that a lightweight contextual-retrieval layer would capture cheaply. The steelmanned response: the marginal value of retrieval sophistication at version-one scale is genuinely small, but the marginal *cost* in 2026 is also small (Claude's contextual-retrieval pattern is effectively a prompt change), so the honest split is "implement only if your version-one eval reveals retrieval as the binding constraint."

- **Simon Willison (simonwillison.net)** would endorse the overall Claude-Code-first stance but push back on the eval layer complexity. His documented position, drawing on Anthropic's paper, is that most builders over-engineer the evaluation layer before they have shipped enough to know what actually matters[^12]. Specific pushback: "three metrics with binary rubrics" is plausibly over-specified for a first version; a single "would I send this to the CEO?" human gate for the first month, plus a retroactive eval set built from the edits, captures 90% of the value at 10% of the investment. The response is that this lesson is aimed at the builder who *has* decided to go unattended, for whom the eval layer is load-bearing; for the builder who is happy to keep the human gate indefinitely, Simon's lighter approach is correct.

## Further reading

**Must-read (under 5):**
- Anthropic, *Building Effective Agents* (Dec 2024) — the architectural north star for this lesson[^1].
- Simon Willison's annotation of the same piece (Dec 2024) — the sharpest one-page summary[^12].
- Hamel Husain, *LLM Evals: Everything You Need to Know* FAQ (updated 2026) — the eval discipline[^4].
- LangGraph 1.0 release post (Oct 2025) — if you suspect you will migrate[^2].
- Boris Cherny / How Boris Uses Claude Code write-up (2025) — for the Claude-Code-native pattern[^5].

**Recommended:**
- Anthropic's *Create custom subagents* docs[^3] — the subagent pattern in practice.
- Arize vs Braintrust vs LangSmith vs Phoenix comparison pieces[^6][^7][^8] — for the observability choice.
- Prefect/Dagster/Airflow comparisons[^9] — only if you end up needing a real data orchestrator.

**Optional:**
- Pydantic AI v1 announcement[^11] — for when the report is a payload, not a page.
- LangChain v1 + LangGraph v1 joint post — for the overall framework family trajectory.

## Citations

[^1]: Anthropic, *Building Effective AI Agents*, published December 19 2024. https://www.anthropic.com/research/building-effective-agents. Supports: the five workflow patterns (prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer); the workflows-vs-agents distinction; the "start simple, add framework only when needed" guidance. Verified 2026-04-17.

[^2]: LangChain, *LangGraph 1.0 is now generally available*, changelog entry, October 22 2025. https://changelog.langchain.com/announcements/langgraph-1-0-is-now-generally-available (supporting): the first stable major release in the durable-agent-framework space; production deployments at Uber, LinkedIn, Klarna; durable execution, built-in persistence, human-in-the-loop, memory management as the four stabilised runtime features. Verified 2026-04-17.

[^3]: Anthropic, *Create custom subagents*, Claude Code documentation. https://code.claude.com/docs/en/sub-agents. Supports: subagents as specialized AI assistants with their own context window, system prompt, tool grants, and permissions. Verified 2026-04-17.

[^4]: Hamel Husain, *LLM Evals: Everything You Need to Know* (FAQ), hamel.dev, updated January 2026. https://hamel.dev/blog/posts/evals-faq/ and the specific sub-post *Q: Should I practice eval-driven development?* https://hamel.dev/blog/posts/evals-faq/should-i-practice-eval-driven-development.html. Supports: error-analysis-first over eval-driven-development; binary rubrics over scored rubrics; LLM-as-judge bias mitigations (ordering randomisation, per-dimension scoring). Hamel's October 2024 X post https://x.com/HamelHusain/status/1843040529115938923 supports: the EDD framing relative to pre-generative-AI ML practice. Verified 2026-04-17.

[^5]: *How Boris Uses Claude Code* community write-up, 2025. https://howborisusesclaudecode.com and https://paddo.dev/blog/how-boris-uses-claude-code/. Supports: Boris Cherny's five-parallel-sessions pattern, plan-first-execute-second discipline, CLAUDE.md as living documentation, verification-loop philosophy. Verified 2026-04-17.

[^6]: Braintrust, *Best LLM evaluation platforms 2025* and *Best AI observability platforms 2025*, braintrust.dev articles, 2025. https://www.braintrust.dev/articles/best-llm-evaluation-platforms-2025 and https://www.braintrust.dev/articles/best-ai-observability-platforms-2025. Supports: free tier specifics (1M trace spans, 10K eval runs), binary-vs-score eval guidance. Verified 2026-04-17.

[^7]: LangSmith pricing, LangChain documentation, 2025. Surveyed via Braintrust comparison and independent platform docs. Supports: free tier of 5,000 traces/month; Plus at $39/user/month with 10,000 traces; enterprise self-host on Kubernetes. Verified 2026-04-17 via the comparison piece at https://www.braintrust.dev/articles/best-ai-observability-platforms-2025.

[^8]: Arize Phoenix documentation and FAQ, 2025. https://arize.com/docs/phoenix/resources/frequently-asked-questions/braintrust-open-source-alternative-llm-evaluation-platform-comparison. Supports: free self-hosting, managed cloud starting at $50/month, the AX-vs-Phoenix split between managed-enterprise and open-source-control. Verified 2026-04-17.

[^9]: ZenML, *Orchestration Showdown: Dagster vs Prefect vs Airflow*, 2025. https://www.zenml.io/blog/orchestration-showdown-dagster-vs-prefect-vs-airflow. Supports: Clippd's July 2025 eight-hours-saved pipeline rebuild on Dagster; Fédération Wallonie-Bruxelles doubling pipeline delivery speed; the asset-centric-vs-task-centric distinction; Airflow 3.0 DAG-versioning and event-driven scheduling additions. Verified 2026-04-17.

[^10]: Modal, *Scheduling remote cron jobs*, docs. https://modal.com/docs/guide/cron. Supports: Python function scheduling via `@app.function(schedule=...)`, cron option robust to redeploys. Verified 2026-04-17.

[^11]: ZenML / LangWatch / Speakeasy comparison pieces on Pydantic AI, LangGraph, CrewAI, 2025. https://langwatch.ai/blog/best-ai-agent-frameworks-in-2025-comparing-langgraph-dspy-crewai-agno-and-more and https://www.zenml.io/blog/pydantic-ai-vs-langgraph. Supports: Pydantic AI v1.0 release September 2025 with API stability commitment; CrewAI's 44.6k GitHub stars; the code-size comparison (Pydantic AI ~160 lines, LangChain ~170, LangGraph ~280, CrewAI ~420 for the same chat functionality); Nextbuild 90-day benchmark result of 8/10 for Pydantic AI developer experience. Verified 2026-04-17.

[^12]: Simon Willison, *Building effective agents*, simonwillison.net, December 20 2024. https://simonwillison.net/2024/Dec/20/building-effective-agents/. Supports: the "don't use a framework" annotation; the start-with-direct-API-calls principle; the workflow-vs-agent distinction as the most useful contribution of the Anthropic paper. Verified 2026-04-17.
