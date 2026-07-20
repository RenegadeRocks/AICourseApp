---
type: lesson
block: block-3-advanced-topics-voice
week: week-06
day_of_cycle: 4
day_name: thu
session_slug: advanced-rags
date_due: 2026-06-25
tags: [agentic-rag, agentic-search, query-planning, iterative-retrieval, self-correction, deep-research, grounding, citations, boris-cherny, grep-vs-embeddings, cost-latency-math]
sources:
  - cherny-latent-space-2025
  - amazon-agentic-search-aaai-2026
  - anthropic-multi-agent-research-2025
  - marsdevs-agentic-rag-2026
  - rag-vs-long-context-2026
  - anthropic-effective-context-engineering-2025
  - lighton-rag-agents
  - anthropic-sonnet-5-pricing-2026
last_verified: 2026-07-17
word_count_target: 5500
---

# Agentic retrieval — when the model runs the search, and when that's a waste of money

## Why this matters

Everything through Wednesday assumed a fixed pipeline: query comes in, retrieval fires once, generation consumes what came back. Agentic retrieval deletes that assumption and hands the loop to the model: it plans queries, runs them, reads results, notices gaps, reformulates, searches again, and stops when it judges the evidence sufficient. This is the architecture behind every "deep research" product you have used, behind Claude Code's famous no-vector-database design, and behind the mid-2026 resolution of the "RAG is dead" argument: naive RAG died; retrieval moved inside the agent.[^4][^7] It is also the most over-prescribed pattern of the year: an agentic loop on a FAQ bot multiplies cost by 3–10× and latency by 2–5× to answer questions a single retrieval already answered.[^5] Today you learn the loop, the evidence for it, the grounding discipline that keeps it honest, and, the part that wins client meetings, the arithmetic for when to refuse it.

## Prerequisites

- [[03-wed-retrieval-beyond-naive-rag|Wednesday]] — the five retrieval families the agent will orchestrate.
- [[02-tue-memory-and-compaction-architectures|Tuesday]] — sub-agent isolation and the 15× token multiplier; agentic retrieval inherits both.
- [[05-fri-advanced-rag|Block 2's advanced-RAG survey]] — Self-RAG and the latency-cost-quality trilemma at intro level.
- Tool-use fundamentals from [[01-mon-mcp-as-a-protocol|Block 0 Week 2]] (one line: tools are typed contracts the model invokes; MCP standardizes the wiring; not re-taught).

## Layer 1 — The loop, mechanically

Single-shot RAG is a function: `answer = generate(query, retrieve(query))`. Agentic retrieval is a loop with a policy:

```
state = {question, evidence: [], notes}
while not sufficient(evidence) and budget_remains:
    plan     = decide_next_search(state)      # which tool, which query
    results  = execute(plan)                  # BM25 / dense / SQL / grep / web
    evidence += appraise(results)             # keep, discard, follow up
answer = generate_with_citations(question, evidence)
```

Each capability in that loop is a distinct engineering surface:

**Query planning.** The agent decomposes the question ("compare our Q3 churn to the industry benchmark" → internal SQL query + external web search + definition lookup) and *chooses tools per sub-question*, using Wednesday's families as its menu. This is where routing stops being a rules engine and becomes model judgment.

**Iterative reformulation.** First searches fail productively: the agent reads near-misses, extracts better vocabulary (the corpus says "logo churn," not "customer churn"), and re-queries. This single behavior is why agentic loops rescue queries that no static pipeline tuning can: the reformulation is *conditioned on this corpus's actual language*, discovered at runtime.

**Sufficiency judgment and self-correction.** The stop condition is a model judgment ("do I have enough to answer, from sources that agree?"), and its failure modes are the loop's failure modes: stopping early (missed evidence) or never stopping (budget burn). Production systems bound it with hard caps (max tool calls, max tokens, max wall-clock) because "the model will know when it's done" is not an SLA. Recall Tuesday: Anthropic's research system found token spend was the dominant predictor of quality,[^3] which cuts both ways. Budget *is* the quality dial, and an unbounded dial is a pager incident.

**Grounded generation.** Every claim in the final answer maps to specific retrieved evidence, with citations. In an agentic system this is harder than in single-shot RAG because evidence arrived across many steps; the discipline is to make the evidence list a first-class artifact (Tuesday's notes pattern) rather than trusting whatever survived in the window. A separate citation pass (one model call whose only job is to attach evidence IDs to claims and delete unsupported sentences) is the cheap, effective version, and it is exactly how Anthropic's research system ends its runs.[^3]

## Layer 2 — The existence proof: Claude Code fired its vector database

The strongest evidence that agentic retrieval is not hype is that the most successful agent product of the era removed its RAG stack. Early Claude Code used embeddings and a local vector index over your repository. In 2025 Anthropic deleted it (the embedding pipeline, the index, the chunking heuristics) and replaced it with agentic search over plain tools: `grep`, `glob`, `ls`, targeted reads, in a plan–act–observe loop. Boris Cherny, on the Latent Space podcast (May 2025): agentic search "outperformed everything. By a lot. And this was surprising," with the side benefits of no index staleness, no chunking decisions, and no second copy of sensitive code sitting in an embedding store.[^1]

Why it works for code: the corpus is *structured for lexical search* (identifiers are exact, conventions are greppable), the agent can afford multiple probes, and live filesystem state beats any snapshot. And the pattern now has measured generality beyond code: an Amazon Science paper accepted at AAAI 2026 reports agentic keyword search reaching ~94.5% of RAG-level faithfulness with no vector store at all, and RL-trained search policies (Search-R1 lineage) *beating* standard RAG by ~24% relative.[^2]

Now the discipline of not over-reading it. Grep-based agentic search wins when queries and corpus share vocabulary and probes are cheap. It loses on paraphrase-heavy natural-language corpora (support tickets, contracts, research papers) where the whole point of dense retrieval is that the user's words don't match the document's. The mid-2026 practitioner synthesis is a spectrum, not a coup: **agentic loop as the backbone; lexical tools where vocabulary is exact; a semantic index where paraphrase dominates; hybrid where you can't tell.**[^1][^7] Wednesday's families didn't get fired; they got demoted from "the architecture" to "tools on the agent's belt."

## Layer 3 — Deep-research patterns: the loop at maximum

Scale the loop up (multi-step, multi-source, minutes-long, report-shaped output) and you get the deep-research pattern that OpenAI, Anthropic, and Google all productized. Tuesday covered its multi-agent skeleton and its economics (orchestrator + parallel search sub-agents; 90.2% over single-agent on Anthropic's internal eval; ~15× chat tokens[^3]); today's angle is what the pattern teaches about *retrieval design*:

- **Breadth then depth.** Effective research agents start with short, broad queries to map the territory, then narrow. Anthropic explicitly prompts this, because sub-agents left alone default to verbose, over-specific first queries that return nothing.[^3]
- **Source appraisal is a retrieval step.** The loop must rank *sources*, not just passages: recency, authority, independence of corroboration. (You are watching this lesson practice its own doctrine: every fast-moving claim here carries two independent corroborations because single-snippet truth is not truth.)
- **Effort scaling.** The lead agent sizes the budget to the question: one sub-agent for a lookup, several for a comparison, many only for genuine breadth-first surveys. Hard-coding one budget for all queries is the amateur tell, in both directions.[^3]

When you build a "mini deep research" for a client (and Saturday's stretch goal is exactly that), these three transfer directly; the multi-agent scaffolding often does not, because most business questions are two searches wide, not twenty.

## Layer 4 — The refusal arithmetic: when agentic retrieval is overkill

The controversy of the day is really an invoice. Practitioner consensus numbers for agentic RAG versus one-pass RAG: roughly **3–10× tokens and 2–5× latency**, earning that price on multi-hop, ambiguous, or high-stakes queries and wasting it on single-fact lookups.[^5] Put current prices on it (Sonnet 5: $2/$10 per Mtok intro through 2026-08-31, then $3/$15[^6]) for a support assistant at 10,000 queries/day:

| | Single-shot RAG | Agentic (avg 5 loops) |
|---|---|---|
| Input tokens/query (typ.) | ~4K | ~25K |
| Output tokens/query (typ.) | ~400 | ~2.5K |
| Cost/query @ $3/$15 | ~$0.018 | ~$0.11 |
| Cost/day @ 10K queries | ~$180 | ~$1,125 |
| p50 latency | ~1–2s | ~8–30s |

(Illustrative token profiles; your traces will differ, and that is Friday's point. The long-context comparison is even harsher: stuffing 500K tokens per query instead of retrieving runs 8–25s to first token and orders of magnitude more per query than a tuned retrieval pipeline.[^7])

A ~$950/day delta buys real quality on the queries that need it and nothing on the queries that don't. So the shippable architecture is almost always **tiered**: single-shot RAG answers everything by default; an escalation trigger — low retrieval confidence, explicit multi-hop shape, judge-flagged insufficiency, or the user asking for depth — promotes the query to the agentic loop; the loop runs with hard budget caps. You quote the client two numbers (fast-lane cost, deep-lane cost) and the mix ratio becomes a tunable business lever rather than a surprise. This is the same shape as Wednesday's graph triage and Tuesday's sub-agent rule: the expensive pattern is a *mode*, never the default.

The strategic version of the controversy — "1M-token contexts kill retrieval entirely" — you already have the tools to dismiss precisely: context rot makes the stuffed window *less accurate* (Monday), and the price sheet makes it absurd at volume; the mid-2026 consensus is hybrid — retrieve tens of thousands of relevant tokens, then let a long-window model reason over them,[^7] an architecture Jerry Liu was already sketching in 2024 as "towards long context RAG."[^8] The frontier position that *did* move: the retrieval step itself is increasingly agentic rather than pipeline-fixed. That is the honest July-2026 statement of where the debate landed.

## Worked example / runnable experiment — single-shot vs agentic, on your corpus

Claude Code orchestration, ~60 minutes, no new code (the instrumented version arrives in Saturday's `code-lab/6/`).

**Phase 1 — build a two-lane test set.** From your Week-4 regression set plus logs, pick 10 single-fact queries and 10 genuinely hard ones (multi-hop, ambiguous, vocabulary-mismatched). If you can't find 10 hard ones, note that; it is a finding about whether you need today's lesson in production at all.

**Phase 2 — run both lanes.** Paste into Claude Code:

> For each of these 20 queries: (a) answer with my Week-4 single-shot pipeline; (b) answer agentically: you may search my corpus up to 6 times, reformulating as needed; keep an evidence log with source IDs per search; cap total work at 6 tool calls per query. Record per query: answer, tool calls used, approximate tokens, wall-clock, and the evidence log.

**Phase 3 — score and decide.** Grade both lanes against gold answers (use your Week-4 judge; it met the [[06-sat-rag-evaluation|≥90% agreement bar]] before you trusted it — if it didn't, that's your Friday homework). Produce the 2×2: easy/hard × single-shot/agentic. The canonical result — agentic ≈ single-shot on easy queries at several times the cost, agentic materially better on hard ones — is the empirical license for the tiered architecture. If your result differs, believe your result, and bring it to Friday's ablation methodology.

**Phase 4 — write the escalation trigger.** From your Phase-2 traces, define the concrete signal that should promote a query to the agentic lane. Test it: would it have caught your hard queries? What fraction of easy ones does it false-promote, and what does each false promotion cost?

## Operator case studies — where the loop earned it, and where it didn't

**Where it earned it: compliance research over policy documents.** A team serving EU-regulated clients (the AI Act's full applicability on 2026-08-02 is generating exactly this traffic) fields questions like "does our biometric-adjacent feature trigger high-risk obligations under the current transition rules?" No single chunk answers that; the loop plans sub-questions (feature classification, annex categories, transition timelines), retrieves per sub-question, and reconciles conflicts between documents of different dates. Single-shot RAG scored so badly on this traffic that the team had been doing it by hand. The agentic lane, capped at 8 tool calls, made it reviewable rather than automatic: the evidence log *is* the deliverable, because counsel wants the trail more than the conclusion. That reframe (the loop as evidence-assembler, the human as judge) is frequently the honest product for high-stakes domains.

**Where it didn't: the internal help-desk bot.** A mid-size company shipped agentic-by-default because the demo impressed. Three weeks of traces showed 84% of queries were single-fact ("how do I reset MFA?"), the loop averaged 4.2 searches to conclude what search #1 had already found, and p50 latency went from 1.8s to 14s. Users started emailing IT again, which is the metric that matters. The rollback to tiered kept the loop for the 16% and cut cost per query by two-thirds. Nobody was fired for the demo, but the lesson stuck: novelty is not a routing policy.

**The middle case: sales-engineering answer desk.** Questions arrive vocabulary-mismatched (prospect language vs product docs), which looks like a job for reformulation. The team found something cheaper first: mining two weeks of agentic traces for the *learned* vocabulary mappings, then injecting those mappings into single-shot query rewriting. Half the loop's lift, at single-shot prices. The agentic lane stayed, but as the *teacher* of the fast lane rather than the workhorse. Saturday's memory lane implements exactly this pattern.

(Composites of documented patterns, labeled as such; latency and share numbers are illustrative of the ranges in the cited production guides.[^5])

## Problem set

1. **Trace autopsy.** Run five hard queries through the Phase-2 agentic lane and read every trace end to end. For each: mark the step where the decisive evidence arrived, the steps that added nothing, and whether the stop decision was right. Deliverable: a table plus one paragraph on what a better `decide_next_search` prompt would change.
2. **Trigger engineering.** Implement your Phase-4 escalation trigger as an actual rule (or 10-line classifier prompt) and evaluate it on the 20-query set: promotion precision, promotion recall on the hard slice, and the monthly dollar cost of its errors at 5K queries/day. Iterate once. Deliverable: both confusion matrices.
3. **The caps memo.** For a client with a p95 SLA of 8 seconds and a $0.05/query margin, derive the agentic lane's caps (tool calls, tokens, wall-clock) from the constraints rather than from defaults. Show the arithmetic linking each cap to the SLA or the margin.
4. **Deep-research scoping.** A client asks for "an agent that researches competitors weekly." Scope it with today's frames: breadth-first or not, single or multi-agent, budget per run at current prices,[^6] evidence-log requirements, and the one metric that decides after four weeks whether it survives. One page.
5. **Position defense, 250 words.** "By 2027, agentic search makes standalone vector databases a niche product." Argue either side using at least the Cherny account,[^1] the Amazon result,[^2] and one vocabulary-structure argument of your own. Committing to a side is required; hedging scores zero.

## Common mistakes experts see

- **Agentic-by-default.** The loop as the front door for every query. Your CFO meets the token bill before your users meet the quality.
- **No hard caps.** "The model stops when it has enough" is a prayer. Cap tool calls, tokens, and wall-clock; alert on cap-hits.
- **Reformulation without memory.** The agent re-runs semantically identical queries because nothing tracks what was already tried. The evidence log (Tuesday's notes pattern) is load-bearing here.
- **Citations bolted on after.** If evidence IDs aren't carried through the loop, the final "citations" are decorative. Grounding is an architecture, not a formatting pass.
- **Over-reading the grep result.** "Claude Code doesn't use RAG" → "we deleted our vector index" → recall collapses on a paraphrase-heavy corpus. Match the tool to the vocabulary structure.[^1]
- **Escalation triggers nobody measured.** A confidence threshold picked by vibes promotes 40% of traffic. The trigger is a classifier; evaluate it like one.
- **Ignoring the sufficiency-judgment failure in evals.** Teams eval answer quality but never eval *stopping behavior*. Early stops look like hallucinations downstream and get misdiagnosed for weeks.

## Reflection questions

1. Take your worst Week-4 retrieval failure. Trace, step by step, how the agentic loop would have rescued it, or argue honestly that it wouldn't have, and what would.
2. The Amazon result says keyword agentic search hits ~94.5% of RAG faithfulness without a vector store.[^2] What property of *their* evaluation corpora would you check before betting your client's support bot on the same conclusion?
3. Your escalation trigger promotes 12% of queries; the client asks you to cut deep-lane cost by half without hurting satisfaction. Name three levers, in the order you'd pull them.
4. Design the sufficiency check for a *legal* research agent, where stopping early is catastrophic and stopping late is billable. What asymmetry do you build in, and where does it live (prompt, judge, cap)?
5. Anthropic prompts sub-agents to search broad-then-narrow.[^3] Why does the same heuristic help a *single*-agent loop over a private corpus? What corpus property would invert it?
6. Reconstruct the "does 1M context kill RAG" answer from first principles you learned this week (rot, price, latency, and the agentic reframe) in five sentences, without citing anyone.

## My take (reviewer lens)

**Boris Cherny** would sign off on the agentic backbone (it's his result) but would push back on the tiered architecture's complexity for small teams: the fleet-scale pattern he now runs treats *simplicity of the loop* as the feature — plain tools, filesystem state, no router — and he'd argue many teams building confidence-threshold escalation machinery should instead ship the agentic lane for everything and cap it hard, because a tuned router is itself an eval liability. Reasonable at Claude Code's economics; at a client's 10K-queries/day margin, the arithmetic above says otherwise, and the disagreement is genuinely about traffic shape. **swyx** would note the lesson under-plays how fast "deep research" is commoditizing — every lab shipped one, open-source clones abound, and the durable value for this cohort is not the loop (a weekend build now) but proprietary corpora, domain evals, and distribution; agentic retrieval is becoming infrastructure, and infrastructure margins go to zero. **Karpathy** would poke at the loop pseudocode: `sufficient(evidence)` hides the entire unsolved problem — calibrated self-assessment — inside a function name, and he'd want the lesson to say plainly that current models are unreliable judges of their own evidence coverage, which is why every production system bounds the loop with dumb caps. He's right, and that admission is the strongest argument for Friday: if the model can't referee itself, your evals have to.

## Further reading

**Must-read**
- Anthropic Engineering, *How we built our multi-agent research system*.[^3] Re-read with today's retrieval lens; the prompting appendix is the practical gold.
- The Cherny/Latent Space agentic-search account plus one careful secondary analysis.[^1]
- MarsDevs, *Agentic RAG: The 2026 Production Guide* — the cost/latency multipliers with worked scenarios.[^5]

**Recommended**
- Amazon Science AAAI 2026 agentic-search paper coverage.[^2]
- LightOn, *RAG is dead, long live RAG: retrieval in the age of agents* — the best short statement of the reframe.[^4]
- A 2026 RAG-vs-long-context decision framework (open-techstack or byteiota).[^7]

**Optional**
- Search-R1 lineage (RL-trained search policies) — where the loop's `decide_next_search` stops being a prompt and becomes a trained policy.[^2]

## Citations

[^1]: Boris Cherny on Latent Space (May 2025), via detailed secondary accounts: Claude Code dropped embeddings/vector search for agentic search ("outperformed everything. By a lot. And this was surprising"); grep/glob/ls in a plan–act–observe loop; security/staleness/simplicity rationale. https://zerofilter.medium.com/why-claude-code-is-special-for-not-doing-rag-vector-search-agent-search-tool-calling-versus-41b9a6c0f4d9 ; https://smartscope.blog/en/ai-development/practices/rag-debate-agentic-search-code-exploration/ ; https://vadim.blog/claude-code-no-indexing/ (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^2]: Amazon Science paper at AAAI 2026: agentic keyword search ≈94.5% of RAG faithfulness with no vector store; Search-R1-style RL policies beating RAG ~24% relative. Coverage: https://www.startuphub.ai/ai-news/ai-research/2026/claude-code-benchmarking-semantic-search-vs-grep ; https://buzzgrewal.medium.com/ai-agents-dont-need-vector-search-anymore-inside-the-agentic-search-stack-replacing-rag-in-2026-58efcabe4f6f (search-verified 2026-07-17; secondary coverage of the paper — numbers flagged as reported; fetch egress-blocked — liveness pass pending)

[^3]: Anthropic Engineering, *How we built our multi-agent research system*, June 2025. Orchestrator-worker; 90.2% over single-agent internal eval; token use ~80% of BrowseComp variance; ~15× chat tokens; broad-then-narrow query prompting; effort-scaling rules; end-of-run citation pass. https://www.anthropic.com/engineering/multi-agent-research-system (search-verified 2026-07-17 across two queries; fetch egress-blocked — liveness pass pending)

[^4]: LightOn, *RAG is dead, long live RAG: retrieval in the age of agents*; also the vault's July-2026 landscape delta §7 (URL-cited) for the "naive RAG died; retrieval lives inside agents" consensus. https://lighton.ai/lighton-blogs/rag-is-dead-long-live-rag-retrieval-in-the-age-of-agents (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^5]: MarsDevs, *Agentic RAG: The 2026 Production Guide* — agentic RAG ≈3–10× tokens, 2–5× latency vs one-pass; earns it on multi-hop/ambiguous/high-stakes, not FAQ or single-fact. https://www.marsdevs.com/guides/agentic-rag-2026-guide (search-verified 2026-07-17, consistent with [^3]'s 15× research-grade figure; fetch egress-blocked — liveness pass pending)

[^6]: Claude Sonnet 5 pricing: $2/$10 per Mtok intro through 2026-08-31, then $3/$15; 1M window. https://www.anthropic.com/news/claude-sonnet-5 (vault landscape delta, URL-verified 2026-07-17) ; https://pricepertoken.com/pricing-page/model/anthropic-claude-sonnet-5 (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^7]: RAG vs long-context economics and the 2026 hybrid consensus: https://open-techstack.com/blog/rag-vs-long-context-2026/ ; https://byteiota.com/rag-vs-long-context-2026-retrieval-debate/ ; https://www.keepmyprompts.com/en/blog/1m-context-windows-trap-rag-decision-framework (TTFT 8–25s on ~500K-token prompts vs 50–150ms hot retrieval; "retrieve 50–200K then reason" default). (search-verified 2026-07-17; individual cost multipliers vary by author — direction consistent across all three; fetch egress-blocked — liveness pass pending)

[^8]: Jerry Liu (LlamaIndex), *Towards Long Context RAG*, llamaindex.ai blog, 2024 — small-to-big retrieval and hybrid long-context + retrieval architectures. https://www.llamaindex.ai/blog/towards-long-context-rag (URL-verified in vault refresh 2026-07-17)

_last_verified: 2026-07-17_
