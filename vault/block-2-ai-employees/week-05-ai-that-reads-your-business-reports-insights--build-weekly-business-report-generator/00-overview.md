---
type: week-overview
block: block-2-ai-employees
week: week-05
title: 'Week 5 — AI that reads your business: reports and insights + build a weekly business report generator'
live_sessions:
  - '2026-06-20 — AI That Reads Your Business: Reports & Insights'
  - '2026-06-21 — Build: Weekly Business Report Generator'
study_window: 2026-06-15 to 2026-06-21
last_verified: 2026-07-17
---

# Week 5 — The AI analyst worker, built as a six-stage pipeline

## The thesis of this week

Every "AI reads your business and writes the report" product — Ramp Intelligence, Brex Agents, Hex Magic, Vic.ai, Puzzle, the internal weekly-recap bot somebody on your team is quietly building — is the same six-stage pipeline underneath: **categorise the job → parse the documents → connect the data → verify the numbers → generate the narrative → ship it with evals and governance**. Every stage has a well-understood failure mode, a disclosed-number benchmark, and a decision that separates a shippable system from a confidently-wrong one.

The industry is currently in an over-correction cycle. Half the commentary says long-context models and native multimodal have killed the document-understanding stack; the other half says numerical hallucination makes the whole category unshippable. Both are wrong in operator-specific ways. This week rebuilds the analyst-worker stack from the parse stage up, with the failure taxonomy that lets you predict where *your* implementation will break before you ship it.

The Saturday build is where every earlier lesson is paid back as a stage contract.

## Who this week is for

You have already shipped a RAG system or a sales agent (Weeks 3 and 4 of this block, or equivalent work elsewhere). You know that retrieval ≠ understanding, that evals matter more than prompts, and that governance is not an afterthought. You are now looking at the back-office category — finance close, CPM, competitive intel, operational reporting — and asking whether to build an internal tool, buy a vertical vendor, or ship a client service on top of one. This week gives you the mechanical model to answer that question and the pipeline to defend the answer.

You direct Claude Code. You can read a JSON schema. You've argued about MCP (a full week of it in [[01-mon-mcp-as-a-protocol|Block 0 Week 2]]). You've hit the point where "just give Claude the PDF" stops being a sufficient architecture.

## Shape of the week

Seven lessons tracing one pipeline from commercial framing to shipped generator. Each day is roughly 90–150 minutes of reading plus 30–90 minutes of hands-on work. Saturday is a full build.

| Day | Topic | Shape |
|-----|-------|-------|
| Mon | The analyst-replacement thesis — four categories, disclosed-number anchors, where the clean commercial lane actually is | Deep-dive + vendor-benchmark exercise + positioning problem set |
| Tue | The document-understanding stack — five archetypes (specialised OSS, hosted gen-AI, native multimodal, cloud doc-AI, academic) with win/lose conditions per archetype | Deep-dive + parser bake-off experiment |
| Wed | Data connectivity, MCP, and the governance ladder — source-class × team-size decision matrix, the deprecated-reference-server object lesson, read-only tokens, PII masking, audit logs | Deep-dive + connector build + threat-model problem set |
| Thu | Analytical reasoning and the code-execution offload — numerical failure taxonomy, PAL, FinanceBench, evaluator-critic loop, typed units | Deep-dive + reasoning-vs-code-offload experiment |
| Fri | Report generation patterns — slot-fill vs narrative-synthesis vs chart-generating, the insight-vs-description gap, voice transfer, Vega-Lite grounding | Deep-dive + rubric-driven rewrite + chart reliability drill |
| Sat | Build the weekly report generator — Claude Code vs LangGraph vs Pydantic AI vs CrewAI, eight-stage pipeline with per-stage contracts, eval harness, observability | Full build + 500-word CEO-lens review |
| Sun | Synthesis, quiz, 40-card flashcard set, 30-day capstone | Review + ship-ready capstone plan |

## Why these topics belong together

The analyst-worker is the canonical back-office AI employee. It is also the category where the six stages are most *visibly* separable: you can watch a bad parse corrupt a good narrative, or a good parse get ruined by a hallucinated ratio. That visibility is what makes it the right week to teach the pipeline as a whole.

- **Monday** sets the commercial frame — not every "AI analyst" category is shippable; one of the four is cleaner than the other three, and the disclosed numbers from Brex, Ramp, Vic.ai, and Puzzle tell you which.
- **Tuesday** is the parse stage. Native multimodal didn't kill the parser stack; it changed the archetype you pick.
- **Wednesday** is the connect stage. MCP made this *easier to wire* and *harder to secure*. The lethal trifecta is where most shipped systems are quietly exposed right now.
- **Thursday** is the verify stage — the hardest and most under-taught. Language models cannot reliably add, divide, or carry units. Code execution can. The architecture question is what you offload and how you check it came back right.
- **Friday** is the generate stage. The reason AI reports sound the same as competitors' AI reports is not a prompt-engineering problem; it's an RLHF neutrality problem with a specific set of fixes.
- **Saturday** is ship. Every earlier lesson becomes a stage contract in the build.
- **Sunday** compresses the pipeline into a 15-move operator table, a quiz that tests the seams, and a 30-day capstone you can run solo or as a client engagement.

The pipeline is load-bearing because the failures chain. A unit confusion in stage 4 produces a confidently-wrong sentence in stage 5 that survives casual review in stage 6 and fails audit in stage 7. The only defence is knowing the failure mode of every stage before you assemble them.

## What "L3 depth" means in this vault

Every lesson this week engages five things:

1. **At least one live controversy in the field.** The long-context-killed-parsers claim (refuted by SCORE-Bench ranking inversion); the self-correction-works-without-external-grounding debate (Huang 2024 vs the reasoning-model crowd); the MCP-as-security-boundary argument (Willison's lethal trifecta, coined June 2025); the "AI without analysts" frame from Hex's McCardel; the buy-vs-build reversal now that Anthropic itself ships finance-agent templates.
2. **At least three citations to research and disclosures published after January 2024.** Frontier, not history. FinanceBench, PAL, Huang 2024, S²R (ACL 2025), SCORE-Bench, Anthropic Contextual Retrieval, Ramp's 2026 procurement-agent disclosures, Brex Agents 2025, Claude for Financial Services (May 2026).
3. **Runnable experiments that demonstrate a mechanism.** A parser bake-off with cost-per-page numbers. A reasoning-vs-code-offload A/B on a FinanceBench-style question. A rubric-driven narrative rewrite with an adversarial senior-editor critic. A full pipeline build on Saturday.
4. **Operator-level specifics with numbers.** Brex 70% of expenses fully automated at 3x-faster close; Ramp 16% average annual vendor-spend savings and 46 hours/month of purchasing work eliminated by its procurement agents; Vic.ai 97% invoice accuracy; FinanceBench 81% parsing ceiling; Contextual Retrieval 5.7% → 2.9% failure; SCORE-Bench ranking inversions across parsers.
5. **A reviewer lens with named technical disagreements.** Each lesson names what a McCardel, a Husain, a Jerry Liu, a Jason Liu, a Simon Willison, a Boris Cherny, a Harrison Chase, a Kiela, or a Karpathy would push back on and what they'd specifically argue instead. Disagreements are orthogonal across critics, not five restatements of the same point.

## How to study this week

Each day, in priority order if you're short on time:

1. **Run the experiment.** Parse the same PDF through three stacks. Run the same FinanceBench-style question with and without code offload. Rewrite the same paragraph with and without a rubric critic. The capability builds in the hands.
2. **Read the "Must-read" citations.** Usually three to five sources. FinanceBench and Contextual Retrieval recur across the week — read them once, well.
3. **Do the problem set.** Some are hands-on, some are positioning writeups, some are adversarial threat models. The variety is deliberate.
4. **Read the lesson prose.** It's scaffolding for the first three. Prose-only is a skim.

Saturday is not optional. If you study only one day this week, study Saturday — but Saturday only works because Monday through Friday gave you the stage contracts it depends on.

## The Saturday and Sunday live sessions

The cohort has live sessions on 2026-06-20 and 2026-06-21. They are bonuses. The lessons in this vault are the primary instruction — each one is a standalone masterclass. If you miss the live sessions, nothing in the vault is incomplete. The Sunday capstone is a 30-day solo or client-facing ship plan that continues past the live-session window.

## Prerequisites from earlier weeks

This week assumes Block 2 Week 3 (landing pages and micro-prototypes) and Week 4 ([[01-mon-what-a-sales-agent-is|sales agent]] with [[04-thu-rag-fundamentals|RAG]]). Specifically: you can reason about structured output, you've wired at least one retrieval system, you know what an evaluator-critic loop is, and you have an opinion on LangGraph vs Claude Code for orchestration. If any of those is shaky, the Thursday and Saturday lessons will hurt more than they should — go back and ship the Week 4 capstone first.
