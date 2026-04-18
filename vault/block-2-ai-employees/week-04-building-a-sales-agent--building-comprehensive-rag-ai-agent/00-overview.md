---
type: week-overview
block: block-2-ai-employees
week: week-04
title: 'Week 4 — Sales Agents + Comprehensive RAG'
live_sessions:
  - '2026-06-13 — Building a Sales Agent'
  - '2026-06-14 — Building Comprehensive RAG AI Agent'
study_window: 2026-06-08 to 2026-06-14
last_verified: 2026-04-17
---

# Week 4 — Sales agents and RAG agents, taught as the same shape of system

## The thesis of this week

The two highest-volume AI "workers" being shipped into enterprises in 2026 are the outbound/inbound sales agent and the knowledge-grounded RAG agent. Most cohorts teach these as separate tracks — one for "GTM folks," one for "ML folks." That framing hides the load-bearing insight: they are the **same shape of system** built against two different external worlds. Both decompose into four primitives — *tool-use + LLM reasoning + retrieval + eval* — and differ only in what "the outside" is. For the sales agent it is an email + CRM + calendar stack; for the RAG agent it is a document corpus + vector index + rerank layer. Everything else — the architecture patterns, the failure modes, the evaluation discipline — generalises.

Week 4 teaches both ladders in parallel and joins them at the top with one evaluation discipline. By Sunday you should be able to walk into a room and argue, with named numbers, why most 2026 AI-SDR platforms are inbox-flooding theatre, why long-context has *not* obsoleted RAG, and why the only durable moat on either product is the eval harness you refused to skip.

## Who this week is for

You have shipped something with an LLM in the middle — a chat app, a small automation, a custom agent driven from Claude Code. You have read Anthropic's *Building Effective Agents*, or at least heard it referenced. You can describe chunking, embeddings, and reranking at a cocktail party. You have not yet had to defend those choices against a CFO asking cost-per-correct-answer, a GC asking where the claim citation comes from, or a postmaster asking why 30% of your sends went to spam in week three.

This week replaces cocktail-party fluency with operator-level fluency. Precision here compounds for the rest of Block 2 — every subsequent week assumes you can reason about tool schemas, retrieval quality, and evals without re-deriving them.

## Shape of the week

Two paired builds plus a synthesis day. Each weekday is ~90–120 minutes of reading plus ~45–90 minutes of hands-on work.

| Day | Topic | Shape |
|-----|-------|-------|
| Mon | What a sales agent actually is — the 8-layer pipeline, 2026 vendor teardown (11x, Artisan, Regie, Clay), seat-vs-outcome pricing | Deep-dive + vendor teardown exercise |
| Tue | Agent architectures — Anthropic's five workflow patterns vs autonomous, MCP as the connector layer, tool-calling reliability against BFCL and τ-bench | Deep-dive + tool-schema build |
| Wed | Outbound deliverability and compliance — SPF/DKIM/DMARC, the Google/Yahoo February-2024 enforcement, the five-jurisdiction compliance matrix (CAN-SPAM / CCPA / GDPR / DPDP 2025 / CASL) | Deep-dive + DNS + compliance audit |
| Thu | RAG fundamentals — chunking strategies, 2026 MTEB snapshot, hybrid BM25+dense with RRF, reranking budgets, Anthropic's Contextual Retrieval and its 49% failure-rate reduction | Deep-dive + corpus experiment |
| Fri | Advanced RAG — GraphRAG and LazyGraphRAG, agentic retrieval (Self-RAG, Chain-of-RAG), the long-context debate, claim-level grounding via Citations API, Chroma's Context Rot finding | Deep-dive + cost-per-correct-answer comparison |
| Sat | RAG evaluation — RAGAS, LLM-as-judge calibration, Hamel's eval-driven discipline (Nurture Boss 33%→95%, Honeycomb 70%→90%), build-vs-buy across LangSmith / Braintrust / Phoenix / Helicone | Deep-dive + eval harness build |
| Sun | Synthesis, quiz, flashcards, end-to-end runnable exercise | Review + integration |

## Why these two tracks belong together

Teach sales agents without RAG and you get a personalisation layer that hallucinates customer names. Teach RAG without the sales-agent framing and you get a retriever that retrieves beautifully and answers questions no one in the business is paying to have answered. The two tracks share four structural claims:

- **Both are tool-using LLM loops, not "apps with AI inside."** Tuesday's tool-schema discipline and Thursday's retriever design are the same engineering problem viewed from two sides: *what does the model call, and what does the model read?*
- **Both fail at the integration seam, not in the model.** The sales agent collapses at dispatch + compliance (Wednesday) because the model was never the bottleneck; the RAG agent collapses at chunking + grounding (Thursday + Friday) for the same reason.
- **Both are bounded by the eval harness, not the architecture.** Saturday is the structural load-bearing day of the week. The teams that win on either product are the teams that ran binary LLM-as-judge with human calibration, not the teams that picked the cleverest framework.
- **Both have a 2025–26 controversy you have to take a position on.** *Is 11x's AI-SDR category real pipeline or inbox-flooding theatre?* *Does Gemini 1.5 Pro's 2M window and Claude's 1M GA kill RAG?* Neither is decided. This week arms you to argue either side with named operator numbers.

The sales-ladder (Mon–Wed) and RAG-ladder (Thu–Sat) are deliberately not bridged by a middle lesson; Tuesday's MCP + tool-schema material is what wires them. A reader who wants "what does my sales agent's RAG layer look like?" synthesises it from Tue + Thu. That is the intended structure.

## What "L3 depth" means in this vault

Every deep-dive this week engages five things:

1. **At least one live 2025–26 controversy, with both sides named.** The AI-SDR category legitimacy debate (Farrokh / Cegelski / Orlob vs Clay / Outreach / Artisan disclosures);[^1][^2] the long-context-vs-RAG argument (Chroma's Context Rot finding vs Gemini/Claude 1M-context marketing);[^3][^4] the autonomous-vs-workflow debate (Cognition's "enthusiastic interns" framing vs Sierra's $100M-ARR workflow-first architecture);[^5] the LLM-judge reliability debate (position bias and judge permissiveness vs Hamel's calibrated binary judges).[^6]
2. **At least three citations to research or operator posts published after January 2024.** Frontier, not history. Anthropic's Contextual Retrieval (Sept 2024),[^7] Google/Yahoo bulk-sender enforcement (Feb 2024),[^8] GraphRAG and LazyGraphRAG (2024),[^9] Chroma's Context Rot (2025).[^3]
3. **Runnable experiments that produce numbers.** Reproduce the Contextual Retrieval uplift on your own 1k-doc corpus. Stand up a six-tool sales-agent schema and measure pass^3 reliability. Run cost-per-correct-answer across RAG, GraphRAG, and pure long-context on the same 50-question eval set.
4. **Operator-level specifics with numbers.** 11x's $14M claimed / $3M real ARR and 70–80% churn;[^1] Anthropic's Contextual Retrieval reducing top-20 retrieval failure from 5.7% to 2.9% (49% relative), 67% with a reranker;[^7] Nurture Boss going 33%→95% answer quality over three rubric iterations;[^6] τ-bench pass^8 below 25% even for frontier models.[^10]
5. **A reviewer lens with named disagreements.** Every lesson names specific paragraphs a Karpathy, a Chip Huyen, a Jerry Liu, a Jason Liu, a Simon Willison, a Harrison Chase, a Boris Cherny, a Lilian Weng, a Douwe Kiela, or an Aman Hylak would push back on — and what they'd argue instead.

## How to study this week

In priority order if you're short on time:

1. **Run the experiment.** Saturday's eval harness and Friday's cost-per-correct-answer comparison are where the capability actually builds. If you do nothing else with the week, do those two.
2. **Read the "Must-read" citations on each day.** Usually three to five sources per lesson. Contextual Retrieval, Building Effective Agents, and Hamel's evals post are the three that the rest of Block 2 assumes you have read in full.
3. **Do the problem sets.** Some are hands-on builds; some are "read this paper and write down where you agree and disagree." The variety is deliberate — different kinds of understanding need different kinds of work.
4. **Read the lesson prose.** It is scaffolding for the first three. Reading the prose alone is skimming the week, not learning it.

A note on pacing: Monday and Thursday are the heaviest reads. Wednesday and Friday are the heaviest builds. Tuesday is the lesson to re-read in Block 2 Week 5 when you start wiring agents together — it pays back twice.

## The live sessions

The cohort has live sessions on 2026-06-13 (Building a Sales Agent) and 2026-06-14 (Building Comprehensive RAG AI Agent). They are bonuses. The lessons in this vault are the primary instruction — each is a standalone masterclass. If you miss a live session, nothing in the vault is incomplete.

## Citations

[^1]: TechCrunch (2025-03-24). *11x investigation: exaggerated customer lists, disputed revenue.* — $14M claimed ARR vs ~$3M real, 70–80% cohort churn after the summer-2024 trial window.
[^2]: Sifted (2025). *11x churn and toxic-culture reporting* — ZoomInfo / Airtable named-customer disputes, legal action threats.
[^3]: Chroma (2025). *Context Rot research* — all 18 tested models degrade with longer context; coherent docs hurt; 200K-window model fails at 50K.
[^4]: Anthropic (2026-03-13). *Claude Opus 4.6 / Sonnet 4.6 1M-context GA.* — 1M tokens at standard pricing.
[^5]: Anthropic (2024-12-19). *Building Effective Agents.* Schluntz & Zhang — five workflow patterns + the autonomous edge, with the "simplest solution possible" directive.
[^6]: Hamel Husain (2024–2025). *Your AI Product Needs Evals* and *Field Guide to Rapidly Improving AI Products.* Nurture Boss 33%→95%, Honeycomb 70%→90%, binary LLM-as-judge calibration.
[^7]: Anthropic (2024-09-19). *Introducing Contextual Retrieval.* — top-20 retrieval failure 5.7% → 2.9% (49% relative reduction); 67% reduction with a reranker.
[^8]: Google / Yahoo (2024-02). *Bulk sender requirements.* SPF + DKIM + DMARC + one-click unsubscribe + <0.3% complaint rate enforced.
[^9]: Microsoft Research / Edge et al. (2024). *GraphRAG* and *LazyGraphRAG.* Entity extraction + Leiden community detection for global sensemaking; LazyGraphRAG drops ingestion cost ~700×.
[^10]: Yao et al. (2024). *τ-bench.* Pass^8 below 25% for frontier models on realistic multi-turn tool-use; "think"-tool uplift 0.370 → 0.570.
