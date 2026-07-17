---
type: synthesis
block: block-2-ai-employees
week: week-04
day_of_cycle: 7
day_name: sun
session_slug: week-04-synthesis
title: 'Week 4 Synthesis — Sales agents + RAG as production AI workers'
study_date: 2026-06-14
date_due: 2026-06-14
tags: [synthesis, quiz, flashcards, sales-agent, rag, contextual-retrieval, deliverability, mcp, agent-architectures, graphrag, ragas, eval-driven-development]
sources:
  - anthropic-contextual-retrieval-2024
  - anthropic-building-effective-agents-2024
  - anthropic-mcp-spec-2024
  - google-bulk-sender-2024
  - yahoo-postmaster-2024
  - microsoft-graphrag-2024
  - liu-lost-in-middle-2023
  - kamradt-needle-in-haystack
  - bfcl-berkeley-2024
  - taubench-yao-2024
  - ragas-es-2023
  - mt-bench-zheng-2023
  - husain-evals-driven-development
  - jxnl-rag-eval
  - eugeneyan-llm-patterns
  - farrokh-cegelski-30mpc
  - clay-apollo-outbound-benchmarks
  - jina-late-chunking-2024
  - cohere-rerank-v3-2024
  - voyage-rerank-2-2024
last_verified: 2026-07-17
word_count_target: 3800
---

# Week 4 Synthesis — Sales agents + RAG as production AI workers

## The one-sentence thesis of this week

The two highest-volume AI workers shipped into enterprises in 2026 — the outbound/inbound sales agent and the knowledge-grounded RAG agent — are the same shape of system built against two different external worlds. Both decompose into the same four primitives — **tool-use + LLM reasoning + retrieval + eval** — and differ only in what the "external system" is: an email + CRM + calendar stack for the sales agent, a document corpus + vector index + rerank layer for the RAG agent. Block 0 taught what AI can do and what prompting looks like; Block 1 taught how to sell an engagement; Block 2 Week 4 is where you actually build the deliverable, and it is the first week in which your artifact either works against a real inbox or a real corpus — or collapses on contact.

---

## The unifying frame: two parallel production-build ladders

Read the week as two three-rung ladders climbed in parallel, joined at the top by a single evaluation discipline.

**Sales-agent ladder (Mon → Tue → Wed):** Monday defined the end-to-end pipeline anatomy — ICP → enrichment → research → personalization → dispatch → reply-handling → CRM handoff — and teardown of the 2025–26 vendor landscape (11x under new CEO Prabhav Jain with the Julian voice rep; Artisan, now self-serve at $250/mo via Ava 2.0; Regie's $30M Series B; Clay; Instantly; Smartlead) with disclosed pipeline numbers where they exist and loud silences where they don't.[^1][^2] Tuesday reframed that pipeline through [Anthropic's December 2024 "Building Effective Agents" post](https://www.anthropic.com/research/building-effective-agents),[^3] which distinguishes five workflow patterns (prompt-chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer) from the autonomous agent, and argues that most production sales work is a workflow composition with a narrow autonomous edge — wired to the outside world through MCP (the November-2024 Model Context Protocol, with the **2026-07-28 stateless-core + OAuth-hardening spec landing days after this week's session**) and, in 2026, a harness chosen first (Claude Agent SDK / OpenAI Agents SDK / LangChain Deep Agents).[^4] Wednesday was the reality check: the February-2024 Google + Yahoo bulk-sender enforcement — hardened in **November 2025 to outright 5xx rejection**, not just spam-foldering[^5][^6] — made SPF + DKIM + DMARC + one-click unsubscribe + a <0.3% complaint rate non-negotiable, and every sales agent that ignores it ships to 0% inbox.

**RAG ladder (Thu → Fri → Sat):** Thursday taught the fundamentals at production depth — chunking (fixed vs recursive vs semantic vs contextual vs late), embedding-model choice against a **live MTEB board now topped by open-weight models (QZhou-Embedding, KaLM-Embedding-Gemma3, Qwen3-Embedding)**, hybrid retrieval (BM25 + dense via RRF), reranking with the current instruction-following generation (Voyage rerank-2.5, Cohere Rerank 4, ColBERTv2),[^7][^8][^9][^10] and Anthropic's Contextual Retrieval — the full 49% / 67% number ladder is taught canonically in [[03-wed-rag-as-a-system]] (b0w1), and Thursday adds the deployment cost math on top of it.[^11] Friday climbed to the frontier: [Microsoft's GraphRAG](https://arxiv.org/abs/2404.16130) (entity extraction + Leiden community detection for global sensemaking),[^12] agentic retrieval (Self-RAG, Chain-of-RAG, multi-hop loops),[^13][^14] long-context vs RAG cost-per-correct-answer math in the era of 1M-token windows everywhere (Gemini 3, Claude Fable 5 / Opus 4.8 / Sonnet 5) plus Fable 5's 2× pricing and the ~30% new-tokenizer inflation,[^15][^16] Lost-in-the-Middle degradation ([Liu et al. 2023](https://arxiv.org/abs/2307.03172)) and the RULER benchmark,[^17][^18] and claim-level citation grounding (Anthropic Citations 2025, Instructor for structured output).[^19][^20] Saturday closed with eval: RAGAS metric decomposition (pin the version — v0.3/v0.4, org moved to vibrantlabsai),[^21] LLM-as-judge reliability ([Zheng et al. MT-Bench 2023](https://arxiv.org/abs/2306.05685)),[^22] Hamel Husain's eval-driven development methodology and the **≥90% canonical judge-agreement bar** at [parlance-labs.com](https://parlance-labs.com/),[^23] and production observability (LangSmith, Braintrust, Arize Phoenix, Helicone).[^24][^25][^26][^27]

**The joint at the top:** Saturday's eval discipline applies identically to both ladders. The sales-agent evaluation harness measures reply-classification accuracy, personalization faithfulness, deliverability score, and per-meeting unit cost; the RAG-agent harness measures retrieval hit-rate@k, faithfulness, context precision/recall, and answer correctness. In both cases, an agent shipping without regression-gated evals is an artifact you cannot defend to a CFO.

---

## Where each day's content goes forward

| This week's lesson | Underwrites in later weeks |
|---|---|
| Mon — Sales-agent pipeline + vendor teardown | Every "should we build or buy?" conversation with a client; Block 3/4 GTM projects; any AI-SDR evaluation brief |
| Tue — Agent architectures (Anthropic playbook + MCP) | Every agent you build in Block 2 Weeks 5–8 (document, report, voice, creative agents); every tool-schema design; every MCP-vs-API integration call |
| Wed — Deliverability + compliance | Every outbound campaign you run or advise on; every multi-jurisdiction (GDPR / DPDP / CAN-SPAM) compliance review; any "our emails stopped landing" incident |
| Thu — RAG fundamentals | Every knowledge-base project; every embedding-choice and chunk-strategy defense; Block 2 document-agent week; any client corpus that outgrows "paste it in the context window" |
| Fri — Advanced RAG | Every enterprise "summarize across 10-K" query; every long-context-vs-RAG routing decision; any multi-hop research agent |
| Sat — Eval (RAGAS + LLM-judge + Hamel) | Every production AI system in Blocks 3–5; every regression gate; every CI-integrated deploy; every "why is quality drifting" incident |

Week 4 is the pivot from "could build" to "has shipped and measured." Weeks 5–8 of Block 2 (document agents, report generators, voice agents, creative workers) silently assume the Week-4 primitives: that you know how to specify a tool schema, when to prefer a workflow over an autonomous agent, how to gate a domain, how to evaluate a generation. Every future agent in this vault is a variation on Week 4's two ladders.

---

## The week's key moves — the mental-move table

Thirteen highest-leverage moves from the six lessons. Each row: the move, the mechanism, when to apply, when not to.

| # | Move | Mechanism | Apply when | Do NOT apply when |
|---|------|-----------|------------|-------------------|
| 1 | Map every sales-agent sub-task to one of Anthropic's five workflow patterns before writing code | [Anthropic's Dec 2024 post](https://www.anthropic.com/research/building-effective-agents) argues most "agent" work is a workflow composition. Reply classification = routing; research-and-draft = orchestrator-workers; personalization QA = evaluator-optimizer. Only the highest-agency edge case is truly autonomous | Designing any new agent with ≥3 distinct steps | A 1-shot transform where a single well-specified prompt does the job |
| 2 | Default to workflows over autonomous agents; earn the autonomy | Anthropic explicit: "When building applications with LLMs, we recommend finding the simplest solution possible, and only increasing complexity when needed." Cost, latency, and failure modes all compound with autonomy. Sierra + Cognition demos don't change the math for your deployment | Any production agent | A research / exploratory agent where the value is the unconstrained exploration |
| 3 | Write tool schemas with ≤6 tools per agent scope; decompose when you exceed it | Multi-turn tool-use reliability degrades as N tools grows (BFCL-V4 multi-turn scores are far below single-turn; the board is led by Qwen3.7 Max at 0.750 and churns quarterly). The "~6–8 tools" number is an *operator heuristic*, not a published BFCL result — Anthropic's tool_search_tool / programmatic tool calling relax it further. Decompose into sub-agents with narrow tool sets | Agent spec with 7+ tools in one decision scope | Genuinely tight coupling where splitting creates worse cross-agent coordination failures, or a >100-tool surface where tool_search_tool is the better fix |
| 4 | Treat MCP as the default connector when you'll reuse a tool across agents or sessions | [MCP](https://modelcontextprotocol.io/) solves the MxN integration problem (canonical intro: [[01-mon-mcp-as-a-protocol]]). When you'll wire CRM / email / calendar / docs to N different agents, MCP amortizes; note the 2026-07-28 stateless-core spec revision lands days after this week. For a single-agent bespoke integration, direct API is often cheaper | Multi-agent or long-lived platform | One-off agent, single tool, throwaway prototype |
| 5 | Configure SPF + DKIM + DMARC + one-click unsubscribe before sending a single cold email | Post-Feb-2024 Google + Yahoo rules: 5000+/day senders must authenticate, must offer one-click unsubscribe, must keep complaint rate <0.3%. Missing any single one = bulk rejection. Postmaster Tools is the feedback loop | Any new outbound domain | A warm-intro or referral channel where you're sending to <10/day from a reputed-domain account |
| 6 | Warm a new sending domain 0 → 500/day over 4–6 weeks; cap ramp at 2× prior-week volume | Deliverability research (GlockApps, MailGenius, Smartlead 2024/25) shows domain reputation is built on volume gradient, not absolute volume. Spike from 0 → 500 in week one = spam folder for 90 days | Any fresh-domain outbound launch | Pooled-reputation send via Instantly/Smartlead where you inherit the pool's reputation |
| 7 | Use a separate subdomain (mail.example.com) for outbound; never burn the primary | If your primary domain's reputation tanks, your transactional email (invoices, password resets, customer support) dies with it. Subdomain isolation is a one-line DNS cost for a seven-figure blast-radius reduction | Any serious outbound operation | Pure relational / 1:1 sending where volume never crosses 50/day |
| 8 | Choose chunk size by evaluating on YOUR corpus + query distribution, not by defaulting to 500 tokens | Fixed 500-token chunks are a LangChain convention, not a universally-optimal size. Recursive-by-sentence + overlap dominates on prose; structured tables need custom chunking; code needs AST-aware splits. Evaluate hit-rate@5 on ≥30 queries before committing | Any new RAG deployment | A proof-of-concept where speed matters more than final quality |
| 9 | Add BM25+dense hybrid (RRF) for corpora with acronyms, named entities, or rare tokens | Dense embeddings normalize toward semantic similarity and miss exact-match queries; BM25 catches them. Reciprocal Rank Fusion with k≈60 is the default combiner. Hybrid gains are largest on technical/legal/medical corpora | Any corpus with domain jargon or named entities | Conversational/narrative corpora where semantic similarity dominates the query pattern |
| 10 | Apply Anthropic Contextual Retrieval for corpora where chunks lose meaning out-of-context | [Anthropic 2024](https://www.anthropic.com/news/contextual-retrieval): 49% top-20 failure-rate reduction (5.7% → 2.9%) from prepending Claude-Haiku-generated 50–100 token context to each chunk before embedding and BM25 indexing. 67% with rerank. Tested on codebases, fiction, ArXiv, science papers — transfer to legal/financial corpora unproven | Technical docs, codebases, multi-document reports where "which company / which period / which section" is ambiguous | Narrative corpora where each chunk is self-contained; ultra-high-volume low-margin deployments where preprocessing cost exceeds retrieval-quality value |
| 11 | Add a reranker (Voyage rerank-2.5, Cohere Rerank 4 — the current instruction-following generation) when retrieval is your bottleneck AND latency budget has headroom | Rerankers rescore top-N candidates with a cross-encoder — higher quality, ~100–600ms added latency; the 2.5/4 generation also takes natural-language relevance instructions. [Jason Liu's position](https://jxnl.co/writing/2024/08/20/rag-flywheel/): add reranker by default. [Ben Hylak counter](https://raindrop.ai/): in agent loops, latency dominates user-perceived quality | Batch / single-shot RAG with >200ms budget | Sub-200ms user-facing loops; high-QPS deployments where rerank cost dominates unit economics |
| 12 | Route global/synthesis queries to GraphRAG or long-context; route local/factoid to vanilla RAG | [Microsoft GraphRAG](https://microsoft.github.io/graphrag/) wins on global sensemaking ("what are the 5 themes across these 100 earnings calls?") at 10–100× ingestion cost. Long-context (Claude / Gemini 1M tokens) is $10–100× more expensive per query than RAG. Vanilla RAG still wins for local-answer queries at cost-per-correct-answer | Heterogeneous query distribution with both local and global needs | Homogeneous local-QA workload — GraphRAG overhead is dead weight |
| 13 | Ship no RAG to production without a rubric-grounded LLM-judge validated against ≥20 human labels to **≥90% agreement** (the week's canonical bar), gated on a **significance test over a ≥100-query set**, not a raw point-drop on 30 | Hamel Husain's core thesis at [parlance-labs.com](https://parlance-labs.com/): start with 20 real-user queries, hand-label, scale via a judge calibrated to ≥90% (Hamel's published Honeycomb number), and gate deploys on a bootstrapped-CI significance test — a 2pp move on N=30 is inside the ±9pp noise band. Without this, "it looks good" is your quality bar | Any production RAG deployment | A throwaway internal tool with one user (you) |

---

## 20 quiz questions

*Span: Mon–Sat. Mix: multiple-choice + short-written + ≥3 number-specific + ≥1 prompt/schema completion per sub-topic. Answers at end.*

---

**Q1 (Multiple choice, Mon)** — Which of these is NOT a documented failure mode of 2024/25 AI SDR platforms (11x, Artisan, Regie)?
(a) Sender-reputation collapse from volume-at-launch
(b) Hallucinated personalization ("congrats on your recent promotion to Director" when no such promotion occurred)
(c) Reply-classification misfires that auto-book calendar holds on spam responses
(d) Token-cost blow-ups from per-email Claude Opus research calls

**Q2 (Short-written, Mon)** — Name the 7 stages of a sales-agent pipeline end-to-end, in order.

**Q3 (Number-specific, Mon)** — State a 2024/25 publicly-disclosed pipeline-generation number (or explicitly-noted missing disclosure) from one of: 11x, Artisan, Regie, Clay, Outreach, Gong.

**Q4 (Multiple choice, Tue)** — [Anthropic's "Building Effective Agents"](https://www.anthropic.com/research/building-effective-agents) distinguishes workflows from autonomous agents. Which pattern best matches "given an inbound email reply, classify into {interested, not-interested, objection, auto-reply, out-of-office, spam}"?
(a) Prompt chaining
(b) Routing
(c) Orchestrator-workers
(d) Evaluator-optimizer
(e) Autonomous agent

**Q5 (Schema completion, Tue)** — Write the Anthropic tool-use JSON schema for a `update_crm_contact` function that takes `contact_id` (string, required), `stage` (enum: "new" | "working" | "qualified" | "closed_won" | "closed_lost", required), and `notes` (string, optional). Include a description field on each parameter.

**Q6 (Number-specific, Tue)** — Berkeley Function-Calling Leaderboard: state the rough tool-count threshold beyond which frontier-model function-call accuracy degrades measurably, and the magnitude of degradation you'd expect.

**Q7 (Short-written, Tue)** — In one sentence each, describe the 5 workflow patterns from Anthropic's post: prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer.

**Q8 (Number-specific, Wed)** — State the post-Feb-2024 Google bulk-sender threshold for triggering the authentication requirement, and the spam-complaint-rate ceiling above which Gmail begins filtering to spam.

**Q9 (Schema completion, Wed)** — Write the DNS TXT records you'd publish for `mail.acme.com` to enable SPF (authorizing `_spf.google.com` include), DKIM (selector `google`, placeholder for public key), and a DMARC policy of `p=quarantine; rua=mailto:dmarc-reports@acme.com; pct=25`.

**Q10 (Short-written, Wed)** — Name the 4 legal regimes a US-based sales agent targeting US + EU + India + Canada recipients must comply with, and for each name the one clause that differs most sharply from the US default.

**Q11 (Multiple choice, Thu — this week's own MTEB material)** — As of July 2026, which statement about the top of the MTEB embedding leaderboard is correct?
(a) Google Gemini Embedding is the clear English #1
(b) OpenAI text-embedding-3-large holds the top spot
(c) Open-weight models (QZhou-Embedding, KaLM-Embedding-Gemma3, Qwen3-Embedding) now lead both the English and multilingual boards
(d) Cohere embed-v4 leads on the multilingual board

**Q12 (Number-specific, Thu — this week's cost-math trap)** — Anthropic quotes Contextual Retrieval preprocessing at "$1.02 per million document tokens." On which model was that figure computed, and what happens to the number if you run the preprocessing on Claude Haiku 4.5 instead? (This is the silent-model-swap the Thursday cost math warns about.)

**Q13 (Short-written, Thu)** — Define reciprocal rank fusion (RRF) in one sentence and state the k-value default most implementations use.

**Q14 (Short-written, Thu — this week's reranker generation)** — Name the current-generation reranker capability (shipped Aug 2025 on Voyage rerank-2.5, and on Cohere Rerank 4) that a 2024-era "Cohere Rerank 3.5" pipeline lacks, and give one sales-agent-relevant use for it.

**Q15 (Multiple choice, Fri)** — [Microsoft GraphRAG](https://arxiv.org/abs/2404.16130) is strictly better than vanilla RAG on which query class?
(a) Factoid lookup ("what was Q3 revenue?")
(b) Global sensemaking ("what are the 5 themes across this corpus?")
(c) Multi-hop factual reasoning ("who funded the company whose CEO went to Stanford?")
(d) Latency-sensitive single-shot QA

**Q16 (Number-specific, Fri)** — State the approximate cost multiplier per query for pure long-context (Claude Opus 4.8 / Fable 5 / Gemini, 1M-token window) vs a well-tuned RAG pipeline over a ~500K-token corpus, and name the two July-2026 pricing/tokenizer changes that widen the gap. Also state the accuracy evidence for Lost-in-the-Middle degradation.

**Q17 (Short-written, Fri)** — Define agentic retrieval in one sentence. Name one paper from 2023–24 that formalizes a variant.

**Q18 (Multiple choice, Sat)** — RAGAS's `faithfulness` metric measures:
(a) Whether the retrieved context contains the answer
(b) Whether the generated answer is grounded in the retrieved context
(c) Whether the retrieval ranks the relevant chunk in top-k
(d) Whether the answer is factually correct against ground truth

**Q19 (Number-specific, Sat)** — State [Zheng et al.'s MT-Bench 2023](https://arxiv.org/abs/2306.05685) reported agreement rate between LLM-as-judge (GPT-4) and human raters on pairwise tasks, and the canonical narrow-rubric-grounded judge-agreement bar this week adopts (Hamel Husain's published Honeycomb figure). Bonus: why is a 30-query regression set the wrong thing to gate a deploy on?

**Q20 (Controversy-defense)** — Take a position: "In 2026 at enterprise scale (>10M tokens of docs, multi-tenant, regulated industry), long-context obsoletes RAG." Defend or refute with ≥4 citations including ≥1 benchmark number per side.

---

## Answers

**Q1** — (d). Token-cost blow-ups are a concern but not a documented platform-level failure of the named vendors in 2024/25 disclosures; a/b/c are all documented in the [30 Minutes to President's Club](https://www.30mpc.com/podcast) takedowns,[^28] Jason Bay's Blissful Prospecting teardowns, and Reddit r/sales threads on 11x/Artisan deployments.[^1]

**Q2** — (1) ICP definition → (2) data-source enrichment (Apollo, ZoomInfo, Ocean, Clay) → (3) segmentation + prioritization → (4) research (public signals: news, hiring, funding, LinkedIn activity) → (5) personalization at the paragraph level → (6) dispatch infrastructure (SendGrid / Postmark / Resend + warmed subdomain) → (7) reply detection + classification → calendar handoff + CRM write. (Accept 6–8 stages depending on whether enrichment and segmentation are split.)

**Q3** — Defensible answer requires citing a specific disclosure. Example: Artisan's case studies claimed specific meetings-booked figures for named customers (and its May-2026 Ava 2.0 launch discloses pricing — $250/mo self-serve — but still no cohort pipeline data); 11x's pre-scandal materials disclosed ARR but not pipeline-conversion; Clay customer case studies disclose enrichment volume (thousands of contacts/hour) but rarely end-pipeline conversion. An answer noting that most AI-SDR vendors disclose vanity metrics (emails sent, meetings booked) but not controlled-cohort incremental pipeline vs manual baseline is fully defensible and arguably the correct read of the disclosure landscape as of mid-2026.

**Q4** — (b) Routing. An inbound email is classified into one of N disjoint categories and forwarded to the appropriate downstream handler — the textbook routing workflow. (A-B evaluator-optimizer composition works too but is strictly more expensive; Anthropic's "simplest solution" principle favors routing.)

**Q5** —
```json
{
  "name": "update_crm_contact",
  "description": "Update a contact record in the CRM with new stage and optional notes.",
  "input_schema": {
    "type": "object",
    "properties": {
      "contact_id": {
        "type": "string",
        "description": "The unique identifier of the contact to update."
      },
      "stage": {
        "type": "string",
        "enum": ["new", "working", "qualified", "closed_won", "closed_lost"],
        "description": "The new pipeline stage for this contact."
      },
      "notes": {
        "type": "string",
        "description": "Optional free-form notes to append to the contact record."
      }
    },
    "required": ["contact_id", "stage"]
  }
}
```

**Q6** — Honest answer distinguishes benchmark from folklore. [BFCL-V4](https://gorilla.cs.berkeley.edu/leaderboard.html)[^29][^30] measures that multi-turn tool-use reliability is far below single-turn (the board is led by Qwen3.7 Max at 0.750 as of July 2026 and churns quarterly), but the specific "degradation beyond ~6–8 tools, dropping 5–15 pp" figure is an **operator heuristic, not a published BFCL result** — BFCL does not report a tool-count-threshold curve. So the defensible answer: cap tool count per decision scope (≤6 is the working rule) because multi-turn reliability degrades as N grows, and note that this is a heuristic that Anthropic's tool_search_tool and programmatic tool calling relax for large surfaces. Naming it as a hard benchmark number is the trap.

**Q7** — (1) *Prompt chaining* — decompose a task into sequential LLM calls where each output feeds the next. (2) *Routing* — classify input into one of N categories and dispatch to a specialized prompt/tool. (3) *Parallelization* — run multiple LLM calls in parallel either on different slices (sectioning) or the same input for majority-vote (voting). (4) *Orchestrator-workers* — a central LLM decomposes and delegates subtasks to worker LLMs, then synthesizes. (5) *Evaluator-optimizer* — one LLM drafts, a second critiques against a rubric, the first revises until a quality gate is met.

**Q8** — Threshold: 5000+ messages/day to Gmail addresses triggers the bulk-sender authentication + one-click-unsubscribe + spam-rate requirements per [Google's sender guidelines](https://support.google.com/a/answer/81126).[^5] Spam-complaint-rate ceiling: <0.3% reported in Postmaster Tools, with a stricter aspirational target of <0.1%. Crossing the ceiling triggers filtering to spam; sustained crossing triggers rejection.

**Q9** —
```
; SPF
mail.acme.com.        IN  TXT  "v=spf1 include:_spf.google.com ~all"

; DKIM (selector "google")
google._domainkey.mail.acme.com.  IN  TXT  "v=DKIM1; k=rsa; p=<BASE64_PUBLIC_KEY>"

; DMARC (published at _dmarc of the sending subdomain)
_dmarc.mail.acme.com.  IN  TXT  "v=DMARC1; p=quarantine; pct=25; rua=mailto:dmarc-reports@acme.com; adkim=r; aspf=r"
```
Defensible variants: `~all` vs `-all` on SPF (soft-fail vs hard-fail); `pct=25` as a phased rollout before moving to `pct=100`; separate aggregate (`rua`) and forensic (`ruf`) reporting addresses.

**Q10** — (a) **US — CAN-SPAM**: opt-out regime, commercial messages require physical address + unsubscribe, no explicit consent needed for B2B.[^31] (b) **EU — GDPR** (Article 6 + recital 47): lawful-basis required; "legitimate interest" for B2B is defensible but fragile, explicit opt-in strongly preferred.[^32][^33] (c) **India — DPDP Act 2023** (in force 2025): explicit consent required, data-fiduciary registration, right-to-erasure.[^34] (d) **Canada — CASL**: explicit opt-in regime, one of the strictest globally; implied consent only in narrow circumstances (existing business relationship within 2 years).[^35] The sharpest break is **consent model**: US opt-out → EU / Canada opt-in → India explicit-consent. A single-template blast to all four jurisdictions without consent segmentation is legally exposed.

**Q11** — (c). As of July 2026 the MTEB top is open-weight: **QZhou-Embedding** (Kingsoft, on Qwen2.5-7B) leads English MTEB at ~75.97, **KaLM-Embedding-Gemma3-12B** (Tencent) is #1 on the multilingual MMTEB board at 72.32, and Alibaba's **Qwen3-Embedding** line outranks Google's Gemini Embedding.[^mteb] Google's Gemini Embedding held the English #1 (~68 band) only as recently as early 2026 — the board churns quarterly, which is the operator lesson: benchmark on your own corpus, never screenshot a leaderboard as durable.

**Q12** — The $1.02/M-doc-token figure is computed on **Claude 3 Haiku ($0.25/M input)** with prompt caching at 10% of input.[^11][^37] Run the same preprocessing on **Claude Haiku 4.5 ($1/M input)** and the per-token ingestion cost is **~4× higher** before any token-count changes — quoting Anthropic's $1.02 while running Haiku 4.5 is the silent-model-swap that makes a cost table lie. The fix: either quote the Claude-3-Haiku basis explicitly, or recompute for Haiku 4.5 on your own chunk/document sizes.

**Q13** — **Reciprocal Rank Fusion** combines multiple ranked lists by assigning each document a score of Σ 1/(k + rank_i) across lists, where rank_i is the document's rank in list i (or ∞ if absent). Default **k = 60** (the Cormack et al. 2009 convention, used by Elasticsearch, Weaviate, Qdrant, pgvector implementations).[^36] The k-value is surprisingly flat across the 10–100 range.

**Q14** — **Instruction-following**: the current reranker generation (Voyage rerank-2.5 / 2.5-lite, Aug 2025; Cohere Rerank 4, Dec 2025) lets you steer relevance scores in natural language — a 2024-era Cohere Rerank 3.5 pipeline can only re-score, not take a relevance instruction.[^voyagererank] Sales-agent use: push retrieval intent the pipeline would otherwise pre-filter for — e.g., "rank the prospect's most recent funding/hiring signals above older news," or "prefer primary sources over aggregators" — directly into the reranker instead of building a separate filter stage. (Bonus: 2.5/4 also carry a 32K context window, 8× Cohere v3.5, so long documents chunk less.)

**Q15** — (b) Global sensemaking. GraphRAG's entity-extraction + Leiden-community-report preprocessing produces summaries at multiple granularities, which enables queries that require synthesis across many chunks.[^12] Factoid lookup is equal-or-worse than vanilla RAG; multi-hop is better served by agentic retrieval; latency-sensitive QA is strictly worse given GraphRAG's multi-call synthesis.

**Q16** — Cost: a ~500K-token corpus is ~650K tokens on the current tokenizer, so pure long-context runs **~$3.28/query on Opus 4.8 ($5/$25)** and **~$6.57/query on Fable 5 ($10/$50)**, vs **~$0.10–0.20/query** for a well-tuned RAG over the same corpus — a **~30–50× multiplier per query** (at 10K queries/day that is ~$1K/day RAG vs ~$32.8K/day long-context on Opus 4.8, an ~$11M/year swing).[^15] The two July-2026 changes that widen the gap: **Fable 5's 2× pricing** ($10/$50 vs Opus's $5/$25) and the **new tokenizer** (Opus 4.7+/Sonnet 5/Fable 5) that tokenizes the same text to ~30% more tokens, inflating the long-context input bill. Lost-in-the-Middle: [Liu et al. 2023](https://arxiv.org/abs/2307.03172) documented a U-shaped accuracy curve — models recover information best from the beginning and end of their input, with ~20–30 accuracy-point drops in the middle on multi-document QA at 20+ document inputs.[^17] 2024 follow-ups (RULER, Needle-in-a-Haystack, Chroma's Context Rot) show modest improvement in frontier models but degradation persists well before the claimed window limit.[^18][^38]

**Q17** — **Agentic retrieval** is a multi-step pattern where the model issues a query, inspects the results, decides whether the answer is sufficient, and if not reformulates or issues sub-queries — treating retrieval as a tool the agent calls in a loop rather than a single pre-generation step. Named papers: [Self-RAG (Asai et al. 2023, arxiv 2310.11511)](https://arxiv.org/abs/2310.11511);[^13] Chain-of-RAG (2024);[^14] [RAFT (Zhang et al. 2024, arxiv 2403.10131)](https://arxiv.org/abs/2403.10131).[^39]

**Q18** — (b). RAGAS `faithfulness` measures whether every factual claim in the generated answer is supported by the retrieved context — in other words, it catches the generator making stuff up *given* what it was given.[^21][^40] (a) is `context_recall`/`context_precision`, (c) is `context_precision` at rank, (d) is `answer_correctness` (requires ground truth).

**Q19** — [Zheng et al. 2023](https://arxiv.org/abs/2306.05685): GPT-4-as-judge agrees with human raters at roughly **80%+ on pairwise comparisons** on MT-Bench, comparable to human-human agreement.[^22] The canonical bar this week adopts is **≥90%** — Hamel Husain's *published* Honeycomb figure ([parlance-labs.com](https://parlance-labs.com/)): a narrow, rubric-grounded judge validated against N≥20 hand-labeled examples reaches ≥90% agreement, the point at which teams trust it to gate deploys.[^23][^41] (This week fixes ≥90% as the single number — not the 85% or 95% variants that circulate; at 20-label calibration sizes the 90-vs-95 distinction is inside the sampling noise.) Bonus: a 30-query regression set is the wrong gate because a binary metric on N=30 carries ~±9pp at 95% CI, so a 2pp deploy-gate move is noise — gate on a significance test over a ≥100-query set instead.

**Q20** — Defensible both sides. **Pro-long-context:** Gemini 3 / 2.5 Pro and Claude Fable 5 / Opus 4.8 / Sonnet 5 with 1M-token context + prompt caching make single-shot retrieval viable for mid-sized corpora; citation grounding is simpler when the full corpus is in-context; operational complexity drops (no vector DB, no index refresh, no chunking strategy). Cite: Anthropic prompt-caching pricing (cached reads at ~10% of input),[^37] frontier needle-in-haystack results.[^16][^38] **Pro-RAG:** (1) Cost: ~30–50× per-query multiplier, *widened* in July 2026 by Fable 5's 2× pricing and the new tokenizer's ~30% token inflation, unsustainable at enterprise scale ([Hamel Husain](https://parlance-labs.com/));[^15][^23] (2) Lost-in-the-Middle / Context Rot degradation persists well before the claimed window limit (Liu 2023 + RULER 2024 + Chroma 2025);[^17][^18] (3) Access control / multi-tenancy is trivial in a vector DB, brutal in a shared-context approach; (4) Freshness — a 1M-token context window doesn't index; RAG does. Synthesis (defensible): **Hybrid routes by query**. Local/factoid → RAG. Global synthesis on <200K-token sub-corpora → long-context. Global synthesis on large corpora → GraphRAG. Long-context does not obsolete RAG at 2026 enterprise scale; it moves the boundary rather than erasing it.

---

## 40 flashcards

*Format: front ↔ back. Anki-importable.*

1. Q: 4 primitives shared by sales agent + RAG agent? → A: Tool-use + LLM reasoning + retrieval + eval.
2. Q: 7 stages of sales-agent pipeline? → A: ICP → enrichment → segmentation → research → personalization → dispatch → reply/CRM.
3. Q: Date of Anthropic "Building Effective Agents" post? → A: December 2024.
4. Q: 5 workflow patterns from Anthropic's post? → A: Prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer.
5. Q: Anthropic's rule-of-thumb on workflows vs autonomous agents? → A: Prefer the simplest solution; only add autonomy when the value justifies the added complexity, cost, and latency.
6. Q: MCP stands for? Announced when by whom? → A: Model Context Protocol, announced November 2024 by Anthropic.
7. Q: MCP's architectural problem? → A: The MxN problem — M LLMs × N tools exploding integration combinatorics.
8. Q: MCP's 3 server primitives? → A: Prompts, Resources, Tools. (Clients support Roots and Sampling.)
9. Q: BFCL stands for? → A: Berkeley Function-Calling Leaderboard.
10. Q: Tool-count rule per agent scope, and its status? → A: Cap at ~≤6 tools per decision scope — an operator heuristic (NOT a published BFCL result); relaxed by tool_search_tool / programmatic tool calling for large surfaces.
11. Q: Date of Google/Yahoo bulk-sender enforcement? → A: February 1, 2024.
12. Q: Bulk-sender volume threshold for authentication requirement? → A: 5000+ emails/day to Gmail.
13. Q: 3 required authentication mechanisms post-Feb 2024? → A: SPF + DKIM + DMARC (with at least one aligned).
14. Q: Spam-complaint-rate ceiling in Postmaster Tools? → A: <0.3% (aspirational <0.1%).
15. Q: Why separate outbound subdomain vs root domain? → A: Isolates reputation — if outbound tanks, transactional email (invoices, resets) survives.
16. Q: Rough domain warmup cadence week 1 → week 6? → A: 20–50/day → 100 → 200 → 350 → 500+, capped at ~2× prior-week volume.
17. Q: 4 legal regimes for global outbound? → A: US CAN-SPAM (opt-out), EU GDPR (opt-in preferred), Canada CASL (opt-in), India DPDP 2023 (explicit consent).
18. Q: MTEB English leader, July 2026? → A: QZhou-Embedding (Kingsoft, on Qwen2.5-7B), ~75.97 — open-weight; open models now top the board (also KaLM-Embedding-Gemma3-12B #1 multilingual at 72.32, Qwen3-Embedding above Gemini). (Contextual Retrieval's 49%/67% ladder → see b0w1 [[03-wed-rag-as-a-system]].)
19. Q: Contextual Retrieval cost-basis trap? → A: Anthropic's "$1.02/M doc tokens" is Claude 3 Haiku ($0.25/M input); running it on Haiku 4.5 ($1/M) is ~4× more — don't quote $1.02 while running Haiku 4.5.
20. Q: Current-generation reranker capability a 2024 Cohere Rerank 3.5 lacks? → A: Instruction-following — steer relevance in natural language (Voyage rerank-2.5, Aug 2025; Cohere Rerank 4, Dec 2025; both 32K context).
21. Q: Voyage's 2026 brand? → A: "Voyage AI by MongoDB" (MongoDB acquired Voyage, Feb 2025).
22. Q: Long-context vs RAG cost multiplier, and the two July-2026 changes that widen it? → A: ~30–50× per query; widened by Fable 5's 2× pricing ($10/$50) and the new tokenizer (~30% more tokens).
23. Q: RRF default k value? → A: k = 60.
24. Q: When BM25+dense hybrid strictly wins over dense alone? → A: Corpora with acronyms, named entities, rare tokens (technical/legal/medical).
25. Q: 5 chunking strategies named Thursday? → A: Fixed-size, recursive, semantic, contextual (Anthropic), late-chunking (Jina).
26. Q: MTEB benchmark, and the operator caveat? → A: Massive Text Embedding Benchmark — standard cross-task embedding comparison; the board churns quarterly, so benchmark on your own corpus rather than screenshotting a leaderboard.
27. Q: GraphRAG's paper authors + year? → A: Edge et al., Microsoft Research, 2024 (arxiv 2404.16130).
28. Q: GraphRAG preprocessing algorithm for community detection? → A: Leiden algorithm on an extracted entity-relationship graph.
29. Q: Query class where GraphRAG strictly wins? → A: Global sensemaking / multi-doc synthesis.
30. Q: GraphRAG ingestion cost vs vanilla RAG? → A: Roughly 10–100× per-document ingestion cost.
31. Q: Lost-in-the-Middle authors + year? → A: Liu et al. 2023 (arxiv 2307.03172).
32. Q: Lost-in-the-Middle headline finding? → A: U-shaped accuracy curve across input position; 20–30 point mid-position drop on multi-doc QA at 20+ docs.
33. Q: RULER benchmark authors + year? → A: Hsieh et al. NVIDIA, 2024.
34. Q: Needle-in-a-Haystack eval originator? → A: Greg Kamradt, 2023.
35. Q: Self-RAG paper? → A: Asai et al. 2023, arxiv 2310.11511.
36. Q: RAFT paper? → A: Zhang et al. 2024, arxiv 2403.10131.
37. Q: RAGAS `faithfulness` measures? → A: Whether every factual claim in the generated answer is supported by the retrieved context.
38. Q: RAGAS `context_precision` vs `context_recall`? → A: Precision = % of retrieved chunks that are relevant; Recall = % of relevant chunks that were retrieved.
39. Q: Zheng et al. MT-Bench LLM-judge agreement rate? → A: ~80%+ pairwise agreement with humans (GPT-4 judge).
40. Q: Canonical rubric-grounded LLM-judge agreement bar (this week)? → A: ≥90% judge–human agreement on ≥20 hand-labeled examples (Hamel's published Honeycomb figure) — and gate deploys on a significance test over ≥100 queries, since 2pp on N=30 is inside ±9pp noise.

---

## Open questions — what's not settled this week

1. **Does Anthropic's Contextual Retrieval transfer?** The 49% reduction is measured on codebases, fiction, ArXiv, science papers.[^11] Legal, medical, high-volume customer-support, and heavily tabular corpora are absent. [Douwe Kiela's Contextual AI](https://contextual.ai/) has its own numbers on similar preprocessing;[^42] neither side has published a head-to-head on the 2026 enterprise worst-case corpus. Transfer is a genuine open question, not marketing nuance.

2. **Is the MCP ecosystem a durable standard or vendor lock-in?** [Anthropic announced MCP in Nov 2024](https://www.anthropic.com/news/model-context-protocol);[^4] by Dec 2025 it was donated to the Agentic AI Foundation under the Linux Foundation (co-founded with Block and OpenAI).[^43] The question is whether broad adoption across model vendors holds or whether competing specs fracture the space in 2026–27. Build on MCP today with an abstraction layer you can swap.

3. **Autonomous sales agents at scale — real or theater?** Sierra (now $150M+ ARR at a $15.8B valuation, but on a workflow-first architecture), Cognition, and the AI-SDR platforms market autonomy.[^44] [30 Minutes to President's Club](https://www.30mpc.com/podcast) and Jason Bay argue the public pipeline numbers are inbox-flooding dressed up.[^28] The ground truth requires disclosed A/B data vs a well-run manual team — which no major AI SDR vendor has published under controlled conditions as of July 2026, even as Artisan's $250/mo self-serve tier widens the top of the funnel.

4. **Long-context pricing trajectory.** Prompt caching and the 1M-token windows now standard everywhere (Gemini 3 and Gemini 2.5 Pro at 1M — the 2M figure was a Gemini-1.5-Pro-era spec; Claude Fable 5 / Opus 4.8 / Sonnet 5 at 1M) push long-context economics downward — but July 2026 also cut the other way, with Fable 5 pricing the capability frontier at 2× Opus and the new tokenizer inflating token counts ~30%.[^15][^16][^37] If 2027 brings a genuine 10× price deflation, the RAG-vs-long-context decision boundary shifts enterprise-wide; it has not yet.

5. **LLM-as-judge failure modes at the tail.** [Zheng et al.](https://arxiv.org/abs/2306.05685) documented position bias, length bias, verbosity bias.[^22] 2024–26 literature (Panickssery et al., Hamel Husain posts, Jason Liu on [jxnl.co](https://jxnl.co/)) catalogued mitigations but no generalized fix.[^45][^23][^46] At the tail of hard cases (adversarial inputs, ambiguous queries, jailbreaks), human eval still wins — the open question is which cases fall at that tail for *your* deployment.

---

## Reviewer lens — where you'd still lose points

1. **The "two parallel ladders" frame is clean but elides the production-glue layer.** A [Hamel Husain](https://parlance-labs.com/) critique:[^23] the week teaches Mon–Wed for sales and Thu–Sat for RAG, but real sales agents retrieve (ICP research, company dossiers, news enrichment) and real RAG deployments dispatch (Slack bots, email digests, JIRA tickets). The separation is pedagogical — production systems blur the layers by design.

2. **Contextual Retrieval numbers are cited without a reproduction attempt.** A [Jason Liu](https://jxnl.co/) pushback:[^46] the [Anthropic cookbook notebook](https://github.com/anthropics/anthropic-cookbook/tree/main/skills/contextual-embeddings) is runnable;[^11] anyone treating 49% as gospel without running the notebook on their own corpus is taking Anthropic's marketing copy at face value. The reviewer-lens correction: reproduce on your corpus or don't cite the headline number as your own quality bar.

3. **The workflow-vs-autonomous frame assumes the Anthropic taxonomy generalizes.** A [Lilian Weng](https://lilianweng.github.io/) pushback: her 2023 LLM-Powered Autonomous Agents post decomposes differently (memory + tool use + planning + reflection),[^47] and the field has not converged. Anthropic's five patterns are a *useful* taxonomy, not the only one — the operator move is to internalize the patterns but not reify them as "the" architecture.

4. **The deliverability section is US-biased.** A European-operator critique: Microsoft 365 filtering, O365 SmartScreen, and European ISP behavior differ meaningfully from Gmail + Yahoo.[^48] The week teaches the Feb-2024 G/Y enforcement as the canonical event; the EU-facing operator needs to add the O365 tenant-level filtering layer that has no public disclosure equivalent.

5. **The eval section names RAGAS, LLM-judge, and Hamel — but the regression-gate design is under-specified.** A [Barry McCardel (Hex)](https://hex.tech/blog/) pushback:[^49] "regression gate that blocks deploy if metric drops >5%" is shape, not content. The real work is the statistical significance test (are you sure the 5% drop isn't within run-to-run variance?), the multi-metric composition (what if precision rises 10% while recall drops 8%?), and the human-override workflow. The week points at eval-driven development; it doesn't teach the gate-design sub-problem at full depth.

---

## End-to-end runnable exercise — one spec, one deploy commitment

Pick **ONE concrete AI worker** you will build and ship in the next 30 days. Options:

- **Option A — Sales agent** targeting your Block 1 Week 2 ICP niche. Goal: 50 qualified outbound touches/week with deliverability + compliance guaranteed, reply-classification accuracy >90%, CRM write-back automated.
- **Option B — RAG agent** over a real corpus you have access to (client docs, your own operator notes, a publicly-scraped vertical corpus). Goal: answer 85%+ of a ≥100-query eval set with faithfulness >0.9 and average latency <5s. (A 30-query set is fine for the 4-hour thin slice, but remember Saturday's math: binary metrics on N=30 carry ~±9pp, so the 40-hour production gate needs the bigger set.)

Then in a single afternoon, produce the following 1-page spec:

**1. Scope (50 words).** One-sentence problem statement, the single ICP or corpus slice, the single measurable outcome metric. No second scope.

**2. Architecture (100 words + diagram).** Map to Tuesday's 5 patterns: what's prompt-chain, what's routing, what's orchestrator-workers, what's evaluator-optimizer, what (if anything) is autonomous. Draw it as a Mermaid diagram. For the sales agent: include dispatch + deliverability layer. For RAG: include chunking + embedding + retrieval + rerank choices.

**3. Infrastructure (75 words).** Named stack: for sales — SendGrid/Postmark/Resend + warmed subdomain (draft the DNS); for RAG — embedding model (Voyage / OpenAI / open-weight Qwen3-Embedding), vector DB (pgvector / Weaviate / Qdrant), rerank (Voyage rerank-2.5 / Cohere Rerank 4 / none), contextual-retrieval preprocessing (yes / no — cost it on Haiku 4.5's real price), generation model (Claude Sonnet 5 default / Opus 4.8 where reasoning demands it).

**4. Eval harness (125 words + metric table).** Minimum 5 metrics with targets and regression gates:
- Sales: reply-classification accuracy, personalization faithfulness, deliverability score (mail-tester/GlockApps), per-meeting unit cost, complaint rate.
- RAG: retrieval hit-rate@5, context precision, faithfulness, answer correctness (LLM-judge + N human labels), latency P50/P95.
Specify the LLM-judge rubric (judge: Opus 4.8, version-pinned), the ≥20-example human-label validation set calibrated to the week's canonical ≥90% judge-agreement bar, the regression-gate rule (default: deploy blocked only when the drop is statistically distinguishable from noise — bootstrapped 95% CI excluding zero on a ≥100-example set; a raw point-drop on a 30-query set is a flag, not a gate), and the re-eval cadence.

**5. Milestones.**
- **4-hour milestone** (ship within 14 days): end-to-end thin slice running on 5 test inputs with all 5 metrics measured once. Not production. Not fast. Works end-to-end.
- **40-hour milestone** (ship within 45 days): production deployment against the full ICP / corpus with regression gate wired into CI.
- **Sunset criteria** (named in advance): if N weeks after 40-hour milestone the primary outcome metric has not moved the underlying business metric (meetings booked / questions answered correctly in production) by X%, shut down and document why.

**6. Commit.** Put the 4-hour milestone date in your calendar. Share the 1-page spec with one peer who will ask you about it on that date.

---

## Citations

*URLs reused from prior-day (Mon–Sat) Citations sections in this week, re-verified in the 2026-07-17 refresh pass; the July-2026 additions (MTEB state, reranker generation, model pricing/tokenizer, Sierra Series E, Artisan Ava 2.0, MCP 2026-07-28 RC) trace to the updated weekday citations.*

[^1]: Marina Temkin, "a16z- and Benchmark-backed 11x has been claiming customers it doesn't have," TechCrunch, March 24 2025. URL: https://techcrunch.com/2025/03/24/a16z-and-benchmark-backed-11x-has-been-claiming-customers-it-doesnt-have/. Claim supported: 2025–26 AI SDR vendor scandals / failure modes (11x fake-logo, reply-classification and personalization misfires) referenced in Mon recap and Q1. Byline corrected from "Julie Bort" and re-verified 2026-07-17.

[^2]: Marina Temkin / Julie Bort, "Artisan, the 'stop hiring humans' AI agent startup, raises $25M — and is still hiring humans," TechCrunch, April 9 2025. URL: https://techcrunch.com/2025/04/09/artisan-the-stop-hiring-humans-ai-agent-startup-raises-25m-and-is-still-hiring-humans/. Retrieved 2026-04-17. Claim supported: Artisan vendor profile and 250-customer/$5M-ARR disclosure level referenced in Mon vendor teardown.

[^3]: Erik Schluntz and Barry Zhang, "Building Effective Agents," Anthropic research blog, December 19 2024. URL: https://www.anthropic.com/research/building-effective-agents. Retrieved 2026-04-17. Claim supported: five workflow patterns (prompt-chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer) vs autonomous agent; "simplest solution" principle; Tue architecture frame.

[^4]: Anthropic, "Introducing the Model Context Protocol," Anthropic news, November 25 2024. URL: https://www.anthropic.com/news/model-context-protocol. Retrieved 2026-04-17. Claim supported: MCP launch date, Nov-2024 attribution, MxN framing.

[^5]: Neil Kumaran, "More secure, less spam: Making email safer for you," Google Blog, October 3 2023. URL: https://blog.google/products/gmail/gmail-security-authentication-spam-protection/. Retrieved 2026-04-17. Claim supported: Feb-2024 Google bulk-sender enforcement, 5000+/day authentication threshold, <0.3% complaint-rate ceiling, one-click-unsubscribe mandate.

[^6]: Marcel Becker, "More Secure, Less Spam," Yahoo Postmaster Blog, October 2023. URL: https://blog.postmaster.yahooinc.com/post/730172167494483968/more-secure-less-spam. Retrieved 2026-04-17. Claim supported: Yahoo parallel enforcement of SPF/DKIM/DMARC + unsubscribe + complaint-rate rules in Feb 2024.

[^7]: OpenSearch, "Introducing reciprocal rank fusion for hybrid search." URL: https://opensearch.org/blog/introducing-reciprocal-rank-fusion-hybrid-search/. Retrieved 2026-04-17. Claim supported: BM25 + dense hybrid retrieval via RRF as production pattern.

[^8]: Voyage AI, "rerank-2 and rerank-2-lite: the next generation of Voyage multilingual rerankers," September 30 2024. URL: https://blog.voyageai.com/2024/09/30/rerank-2/. Retrieved 2026-04-17. Claim supported: Voyage rerank-2 as named reranker in Thu recap.

[^9]: Cohere reranker line: Rerank 3.5, December 2024 (https://cohere.com/blog/rerank-3pt5), superseded by Cohere Rerank 4 (rerank-4-pro / -fast, 32K context, December 2025) — the current Cohere flagship named in the Thu recap and mental move 11. Verified 2026-07-17.

[^10]: Santhanam et al., "ColBERTv2: Effective and Efficient Retrieval via Lightweight Late Interaction," arxiv 2112.01488, NAACL 2022. URL: https://arxiv.org/abs/2112.01488. Retrieved 2026-04-17. Claim supported: ColBERTv2 as named late-interaction reranker.

[^11]: Anthropic, "Introducing Contextual Retrieval," September 19 2024. URL: https://www.anthropic.com/news/contextual-retrieval. Claim supported: the number ladder (49% top-20 failure-rate reduction, 67% with rerank), tested domains, Claude 3 Haiku context generation, and the $1.02/M-doc-token (Claude-3-Haiku-basis) cost math. The ladder's canonical teaching home in this vault is b0w1 [[03-wed-rag-as-a-system]]; this week quizzes only the cost-basis and transfer questions, not the ladder itself. Verified 2026-07-17.

[^12]: Edge et al. (Microsoft Research), "From Local to Global: A Graph RAG Approach to Query-Focused Summarization," arxiv 2404.16130, 2024. URL: https://arxiv.org/abs/2404.16130. Retrieved 2026-04-17. Claim supported: GraphRAG entity-extraction + Leiden community detection for global sensemaking; ingestion-cost framing.

[^13]: Asai et al., "Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection," arxiv 2310.11511, October 17 2023. URL: https://arxiv.org/abs/2310.11511. Retrieved 2026-04-17. Claim supported: Self-RAG as a formalized agentic-retrieval variant.

[^14]: Wang et al., "Chain-of-Retrieval Augmented Generation," arxiv 2501.14342, January 24 2025. URL: https://arxiv.org/abs/2501.14342. Retrieved 2026-04-17. Claim supported: Chain-of-RAG as a 2024–25 agentic-retrieval variant with multi-hop gains.

[^15]: Anthropic model docs and pricing, July 2026. URL: https://platform.claude.com/docs/en/about-claude/models/overview (lineage: https://claude.com/blog/1m-context-ga). Claim supported: 1M context standard on Claude Fable 5 ($10/$50 per Mtok), Opus 4.8 ($5/$25), Sonnet 5 ($2/$10 intro through Aug 31 2026, then $3/$15); new tokenizer on Opus 4.7+/Sonnet 5/Fable 5 (~+30% tokens on the same text) — the basis for Q16's and Q20's cost math. Verified 2026-07-17.

[^mteb]: MTEB leaderboard state, July 2026: QZhou-Embedding #1 English MTEB ~75.97 (arxiv 2508.21632, https://huggingface.co/Kingsoft-LLM/QZhou-Embedding); KaLM-Embedding-Gemma3-12B #1 multilingual MMTEB 72.32; Qwen3-Embedding above Gemini Embedding. Live board: https://huggingface.co/spaces/mteb/leaderboard. See Thursday's citations for the full sourcing. Verified 2026-07-17.

[^voyagererank]: Voyage AI by MongoDB, "rerank-2.5 and rerank-2.5-lite: instruction-following rerankers," August 11 2025. URL: https://www.mongodb.com/company/blog/product-release-announcements/rerank-2-5-and-rerank-2-5-lite-instruction-following-rerankers. First instruction-following rerankers; 32K context; +7.94%/+7.16% over Cohere Rerank v3.5. Cohere Rerank 4 (Dec 2025) is the Cohere counterpart. Verified 2026-07-17.

[^16]: Gemini Team, Google DeepMind, "Gemini 1.5: Unlocking multimodal understanding across millions of tokens of context," arxiv 2403.05530, 2024. URL: https://arxiv.org/abs/2403.05530. Retrieved 2026-04-17. Claim supported: Gemini 1.5–2.5 long-context era and needle-in-haystack recall at 1M tokens.

[^17]: Liu et al., "Lost in the Middle: How Language Models Use Long Contexts," TACL 2024 (arxiv 2307.03172). URL: https://aclanthology.org/2024.tacl-1.9/. Retrieved 2026-04-17. Claim supported: U-shaped accuracy curve; ~20–30 point mid-position drop on multi-document QA.

[^18]: Hsieh et al. (NVIDIA), "RULER: What's the Real Context Size of Your Long-Context Language Models?," arxiv 2404.06654, April 2024. URL: https://arxiv.org/abs/2404.06654. Retrieved 2026-04-17. Claim supported: RULER benchmark; most 32K-claimed models fail to maintain performance at claimed length; U-shape persistence beyond ~200K.

[^19]: Anthropic, "Introducing Citations on the Anthropic API," January 23 2025. URL: https://www.anthropic.com/news/introducing-citations-api. Retrieved 2026-04-17. Claim supported: Anthropic Citations API 2025 for claim-level grounding.

[^20]: Jason Liu, Instructor documentation and writing, jxnl.co. URL: https://jxnl.co/systematically-improve-your-rag/. Retrieved 2026-04-17. Claim supported: Instructor library for schema-enforced structured output in RAG pipelines.

[^21]: Shahul Es et al., "Ragas: Automated Evaluation of Retrieval Augmented Generation," arxiv 2309.15217, September 26 2023 (EACL 2024). URL: https://arxiv.org/abs/2309.15217. Retrieved 2026-04-17. Claim supported: RAGAS framework metric decomposition (faithfulness, context-precision, context-recall, answer-correctness).

[^22]: Zheng et al., "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena," arxiv 2306.05685, 2023. URL: https://arxiv.org/abs/2306.05685. Retrieved 2026-04-17. Claim supported: ~80%+ GPT-4-judge / human agreement on pairwise MT-Bench; position / length / verbosity biases.

[^23]: Hamel Husain, "Your AI Product Needs Evals," hamel.dev, March 29 2024. URL: https://hamel.dev/blog/posts/evals/. Claim supported: eval-driven development methodology and the 20-hand-label rubric-grounded judge discipline. The canonical agreement bar is **≥90%** (the published Honeycomb figure in the Field Guide, https://hamel.dev/blog/posts/field-guide/) — an earlier draft of this vault quoted ">95%," which the source does not support. Corrected and re-verified 2026-07-17.

[^24]: LangSmith Evaluation documentation, docs.langchain.com/langsmith/evaluation. URL: https://docs.langchain.com/langsmith/evaluation. Retrieved 2026-04-17. Claim supported: LangSmith as named production eval/observability tool.

[^25]: a16z, "Investing in Braintrust," October 8 2024. URL: https://a16z.com/announcement/investing-in-braintrust/. Retrieved 2026-04-17. Claim supported: Braintrust as named LLM eval/observability platform.

[^26]: Arize Phoenix GitHub repository. URL: https://github.com/Arize-ai/phoenix. Retrieved 2026-04-17. Claim supported: Arize Phoenix as named open-source OTel-based LLM observability tool.

[^27]: Helicone AI features documentation. URL: https://www.helicone.ai/. Retrieved 2026-04-17. Claim supported: Helicone as named proxy-based LLM observability tool.

[^28]: 30 Minutes to President's Club podcast (Armand Farrokh + Nick Cegelski). URL: https://open.spotify.com/show/28wBBJzGItlklSjZTIwqds. Retrieved 2026-04-17. Claim supported: operator critique of AI-SDR vendor measurement regime; inbox-flooding-vs-pipeline framing.

[^29]: Berkeley Function Calling Leaderboard V4. URL: https://gorilla.cs.berkeley.edu/leaderboard.html. Retrieved 2026-04-17. Claim supported: tool-count degradation threshold and frontier-model function-call accuracy figures.

[^30]: Patil et al., "The Berkeley Function Calling Leaderboard (BFCL): From Tool Use to Agentic Evaluation of Large Language Models," PMLR 2025. URL: https://proceedings.mlr.press/v267/patil25a.html. Retrieved 2026-04-17. Claim supported: BFCL single-turn vs multi-turn tool-use reliability characterization.

[^31]: FTC, "CAN-SPAM Act: A Compliance Guide for Business." URL: https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business. Retrieved 2026-04-17. Claim supported: US CAN-SPAM opt-out regime, physical-address and 10-day opt-out clauses.

[^32]: Morgan Lewis, "GDPR Legitimate Interests — EDPB October 2024 Guidelines." URL: https://www.morganlewis.com/blogs/sourcingatmorganlewis/2024/10/gdpr-when-can-data-controllers-rely-on-legitimate-interests-for-data-processing-new-guidelines-from-the-edpb. Retrieved 2026-04-17. Claim supported: GDPR Article 6 + Recital 47 legitimate-interest three-part test for B2B direct marketing.

[^33]: GDPR Recital 47, "Overriding Legitimate Interest." URL: https://gdpr-info.eu/recitals/no-47/. Retrieved 2026-04-17. Claim supported: direct-marketing reasonable-expectations test under GDPR.

[^34]: MeitY (India), "Digital Personal Data Protection Rules, 2025," PIB release, November 14 2025. URL: https://www.pib.gov.in/PressReleasePage.aspx?PRID=2190655. Retrieved 2026-04-17. Claim supported: India DPDP Act 2023 in-force status, explicit-consent regime, consent-manager framework.

[^35]: CRTC, "CASL Guidance on Implied Consent." URL: https://crtc.gc.ca/eng/com500/guide.htm. Retrieved 2026-04-17. Claim supported: Canada CASL express-opt-in regime; narrow implied-consent windows (existing business relationship).

[^36]: Cormack, Clarke, Büttcher, "Reciprocal Rank Fusion outperforms Condorcet and individual Rank Learning Methods," SIGIR 2009. Referenced via OpenSearch RRF writeup: https://opensearch.org/blog/introducing-reciprocal-rank-fusion-hybrid-search/. Retrieved 2026-04-17. Claim supported: RRF scoring formula and k=60 default convention.

[^37]: Anthropic, "Prompt caching with Claude," August 2024. URL: https://www.anthropic.com/news/prompt-caching. Retrieved 2026-04-17. Claim supported: cache-hit pricing at 10% of standard input (backs the ~$1.02/M doc-tokens Contextual Retrieval cost math and the cached-read pricing frame in Q20).

[^38]: Greg Kamradt, "LLMTest_NeedleInAHaystack," GitHub. URL: https://github.com/gkamradt/LLMTest_NeedleInAHaystack. Retrieved 2026-04-17. Claim supported: Needle-in-a-Haystack as the founding long-context recall eval referenced for Gemini / frontier results.

[^39]: Zhang et al., "RAFT: Adapting Language Model to Domain Specific RAG," arxiv 2403.10131, March 2024. URL: https://arxiv.org/abs/2403.10131. Retrieved 2026-04-17. Claim supported: RAFT as named distractor-aware domain-RAG fine-tuning paper.

[^40]: RAGAS documentation, "Faithfulness metric." URL: https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/faithfulness/. Retrieved 2026-04-17. Claim supported: RAGAS faithfulness = whether each claim in the answer is grounded in retrieved context.

[^41]: Hamel Husain, "A Field Guide to Rapidly Improving AI Products," hamel.dev, March 24 2025. URL: https://hamel.dev/blog/posts/field-guide/. Retrieved 2026-04-17. Claim supported: Honeycomb three-iteration >90% judge-human alignment; rubric-grounded judge reaching high agreement on narrow production tasks.

[^42]: Contextual AI, "Introducing RAG 2.0," March 2024. URL: https://contextual.ai/introducing-rag2/. Retrieved 2026-04-17. Claim supported: Douwe Kiela / Contextual AI's own preprocessing-RAG numbers referenced in the Contextual-Retrieval-transfer open question.

[^43]: Model Context Protocol blog, "One Year of MCP: November 2025 Spec Release." URL: https://blog.modelcontextprotocol.io/posts/2025-11-25-first-mcp-anniversary/. Retrieved 2026-04-17. Claim supported: MCP governance / ecosystem growth trajectory underlying the durable-standard-vs-lock-in open question.

[^44]: Sierra scale figures. TechCrunch, "Bret Taylor's Sierra reaches $100M ARR in under two years," November 21 2025 (https://techcrunch.com/2025/11/21/bret-taylors-sierra-reaches-100m-arr-in-under-two-years/); updated May 4 2026: $950M Series E at $15.8B post-money, $150M+ ARR in eight quarters (https://techcrunch.com/2026/05/04/sierra-raises-950m-as-the-race-to-own-enterprise-ai-gets-serious/). Claim supported: Sierra as named agent vendor at scale — on a workflow-first architecture. Verified 2026-07-17.

[^45]: "A Survey on LLM-as-a-Judge," arxiv 2411.15594, November 2024. URL: https://arxiv.org/abs/2411.15594. Retrieved 2026-04-17. Claim supported: comprehensive catalogue of LLM-judge biases and mitigation strategies referenced in Open Question 5.

[^46]: Jason Liu, "Systematically Improving Your RAG," jxnl.co, May 22 2024. URL: https://jxnl.co/writing/2024/05/22/systematically-improving-your-rag/. Retrieved 2026-04-17. Claim supported: measurement-driven RAG methodology underlying the Reviewer-Lens reproduction critique and Open-Question-5 mitigation catalogue.

[^47]: Lilian Weng, "LLM Powered Autonomous Agents," lilianweng.github.io, June 23 2023. URL: https://lilianweng.github.io/posts/2023-06-23-agent/. Retrieved 2026-04-17. Claim supported: Weng's Agent = LLM + memory + planning + tool-use decomposition referenced in Reviewer Lens point 3.

[^48]: Microsoft Defender for Office 365 team, "Strengthening Email Ecosystem: Outlook's New Requirements for High-Volume Senders," April 2 2025. URL: https://techcommunity.microsoft.com/blog/microsoftdefenderforoffice365blog/strengthening-email-ecosystem-outlook%E2%80%99s-new-requirements-for-high%E2%80%90volume-senders/4399730. Retrieved 2026-04-17. Claim supported: O365 / Microsoft tenant-level filtering requirements distinct from Gmail + Yahoo, referenced in Reviewer Lens point 4.

[^49]: Barry McCardel, "I'm sorry, but those are vanity evals," LinkedIn post, April 2025. URL: https://www.linkedin.com/posts/barrymccardel_im-sorry-but-those-are-vanity-evals-hex-activity-7317617617370763264-I_qo. Retrieved 2026-04-17. Claim supported: McCardel / Hex critique of vanity dashboards vs real regression-gated evals referenced in Reviewer Lens point 5.

_last_verified: 2026-07-17_
