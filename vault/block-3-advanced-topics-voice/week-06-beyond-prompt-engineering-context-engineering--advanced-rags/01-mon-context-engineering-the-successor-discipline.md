---
type: lesson
block: block-3-advanced-topics-voice
week: week-06
day_of_cycle: 1
day_name: mon
session_slug: beyond-prompt-engineering-context-engineering
date_due: 2026-06-22
tags: [context-engineering, context-rot, attention-budget, system-prompt-altitude, tool-design, just-in-time-context, long-context, nolima, ruler, karpathy, anthropic]
sources:
  - karpathy-context-engineering-tweet-2025
  - anthropic-effective-context-engineering-2025
  - chroma-context-rot-2025
  - nolima-arxiv-2502-05167
  - ruler-arxiv-2404-06654
  - hamel-p6-context-rot
  - anthropic-sonnet-5-pricing-2026
  - claude-code-context-window-docs-2026
  - philschmid-context-engineering-2025
last_verified: 2026-07-17
word_count_target: 5500
---

# Context engineering — the discipline that replaced prompt golf

## Why this matters

For two years the industry's model of skill was the clever prompt: the magic phrase, the "act as a world-class copywriter," the chain-of-thought incantation. That game — call it prompt golf — is over as the differentiating skill, and the people who ended it are not bloggers but the builders of the most-used agent products in the world. What replaced it is a budgeting discipline. Every production agent you ship from this week forward — the Week-4 RAG agent, the Week-5 report generator, the voice agents coming in Week 7 — lives or dies on a single recurring decision: *of everything you could put in front of the model right now, what earns its place?* Get this right and the same model, at the same price, behaves like a better model. Get it wrong and your agent degrades in exactly the ways clients notice: forgets instructions mid-task, latches onto stale tool output, burns $40 of tokens doing $2 of work.

By the end of today you will be able to (1) define context engineering precisely and defend the distinction from prompt engineering against a skeptic, (2) explain context rot mechanistically and cite the three benchmark families that measure it, (3) audit a real agent's context window and price each component, (4) choose between just-in-time and pre-loaded context for a given workload, and (5) hold a defensible position on the live controversy: is this a genuine discipline or a rebrand?

## Prerequisites

- [[05-fri-context-window-economics|Context-window economics]] from Block 0 Week 0 — the token cost math, including the ~30% token inflation from Anthropic's current tokenizer, is assumed, not re-taught here.[^8]
- [[01-mon-mental-model-of-llms|The LLM mental model]] — attention as the mechanism, tokens as the unit.
- [[04-thu-rag-failure-modes-and-long-context-debate|The RAG-vs-long-context debate]] from Block 0 Week 1 — today extends that debate with the mid-2026 benchmark record.
- A Claude Code session you can open and a real agent or project of yours to audit.

## Layer 1 — The definitional move: from prompt to context

The term has a precise birthdate. On June 19, 2025, Shopify CEO Tobi Lütke wrote that he preferred "context engineering" to "prompt engineering," defining it as "the art of providing all the context for the task to be plausibly solvable by the LLM." Six days later Andrej Karpathy amplified it: "+1 for 'context engineering' over 'prompt engineering'. People associate prompts with short task descriptions you'd give an LLM in your day-to-day use. When in every industrial-strength LLM app, context engineering is the delicate art and science of filling the context window with just the right information for the next step."[^1]

Anthropic's engineering team formalized the discipline in "Effective context engineering for AI agents" (September 29, 2025), and their definition is the one worth memorizing because it names the actual work: prompt engineering is writing and organizing instructions; context engineering is **the set of strategies for curating and maintaining the optimal set of tokens during inference** — everything that lands in the window, most of which is not the prompt.[^2] The essay's framing question is the one you should tape above your desk: *what configuration of context is most likely to generate the model's desired behavior?*

Look at what actually fills a production agent's window and the distinction stops being semantic:

| Component | Typical share of a mid-task agent window | Who wrote it |
|---|---|---|
| System prompt | 2–10% | You, once |
| Tool definitions | 5–25% (MCP-heavy agents can go higher) | You + every server you connect |
| Retrieved documents / files | 10–40% | Your retrieval stack |
| Message history + prior tool results | 30–70% | The run itself |
| The user's actual request | often <1% | The user |

(Shares are operator estimates from auditing our own builds, not a published benchmark — your `/context` audit in the experiment below will give you your real numbers.)

Prompt engineering optimizes one row. Context engineering owns the table. That is the whole argument for the new name, and it is also — as we will see in Layer 5 — the whole argument against it.

## Layer 2 — The finite budget: context rot, and why 1M tokens does not repeal it

The naive mid-2026 objection: "Sonnet 5, Fable 5, GPT-5.5, Gemini 3.5 Flash, and Kimi K3 all ship 1M-token windows.[^8] Why budget at all?" Because the window is advertised capacity, not effective capacity, and the gap between the two is measured, replicated, and large.

**The mechanism.** Transformer attention computes pairwise relationships between tokens. As the window grows, every token's relevance signal competes with more neighbors; the model was also trained on far more short sequences than long ones. Anthropic's essay names the consequence an "attention budget": models have a finite budget of usable attention, and every token you add depletes it.[^2] The observable symptom is what Chroma's July 2025 technical report named **context rot**.

**The evidence, in three benchmark families:**

1. **Chroma's context-rot report** (Kelly Hong, Anton Troynikov, Jeff Huber, July 2025) evaluated 18 frontier models — GPT-4.1, Claude 4, Gemini 2.5, Qwen3 among them — and found every one degrades as input length grows, *including on tasks that should be trivially easy*. Performance depends non-uniformly on needle–question similarity, distractor presence, and haystack structure; a coherent haystack can hurt more than shuffled text.[^3] Hamel Husain's operator note on the report adds the practical kicker: different model families rot differently, so you cannot even assume a uniform degradation curve when you swap models.[^4]
2. **NoLiMa** (Adobe Research, arXiv 2502.05167, ICML 2025) removed the crutch that made classic needle-in-a-haystack tests look reassuring: lexical overlap between question and needle. With overlap minimized, models must infer latent associations, and the results are brutal — at 32K tokens, 11 of the tested models drop below 50% of their own short-context baseline; GPT-4o falls from a 99.3% baseline to 69.7%. NoLiMa defines *effective length* as the longest context where a model keeps ≥85% of its short-context score, and for every model tested that lands far below the advertised window.[^5]
3. **RULER** (NVIDIA, arXiv 2404.06654) generates synthetic tasks across 13 task types in four categories — retrieval, multi-hop tracing, aggregation, QA — at configurable lengths, and computes an effective context length against an 85%-class threshold. Its enduring contribution is showing that models which pass simple retrieval at a given length still fail aggregation and multi-hop tracing at that same length.[^6]

The 2026 state of play: the frontier moved, the shape of the curve did not. Community leaderboards tracking RULER/MRCR/NoLiMa-class evals through 2026 continue to show a substantial divergence between advertised and effective windows for multi-fact retrieval past ~200K tokens (one mid-2026 analysis puts the gap at 30–60 points depending on model and task; treat the exact number as indicative, the direction as settled).[^7] The operational rule this licenses:

> **Rule of thumb: treat your effective budget as a fraction of the advertised window, and treat everything past it as a paid liability.** You are paying $2–$10 per million input tokens (Sonnet 5 intro pricing, through 2026-08-31)[^8] for tokens that may actively make answers worse. Long context is a capability you invoke deliberately, not a default you fill.

Note what this does *not* say. It does not say long windows are useless — loading a 300K-token codebase for a one-shot architectural review is a legitimate, deliberate spend. It says the window is not free real estate, in either dollars or accuracy.

## Layer 3 — Anatomy of a well-engineered context

Anthropic's essay plus eighteen months of community practice give us a component-by-component discipline.[^2][^9]

**System prompt: fly at the right altitude.** The failure modes are symmetric. Too low: hardcoded if-else prompt logic ("if the user asks about refunds, say X; if about shipping, say Y") that is brittle, bloats the prompt, and fights the model's own judgment. Too high: vague exhortations ("be helpful and accurate") that assume shared context the model does not have. The Goldilocks altitude is *specific enough to guide behavior, flexible enough to leave judgment to the model*: heuristics, not case tables. Structure helps — distinct sections (`<background>`, `<instructions>`, tool guidance, output format) beat a wall of prose. Start minimal, add rules only in response to observed failures. Your system prompt should read like an onboarding memo to a competent new hire, not like a legal contract or a pep talk.

**Tool definitions: the tax nobody audits.** Every tool schema you register is resident context on every single call. Connect three MCP servers with 15 tools each, each with verbose descriptions and JSON schemas, and you can spend tens of thousands of tokens before the conversation starts — this is precisely why Claude Code's recent releases push MCP tool loading toward on-demand patterns and why Anthropic's essay insists tools be "token-efficient" and non-overlapping.[^2][^9] The audit questions: Would a human engineer, given this toolbox, know unambiguously which tool to use? Do any two tools overlap? Does any tool return unbounded output? A tool that can return 50K tokens of JSON is a context bomb with a friendly name.

**Examples: curate, don't enumerate.** Few-shot examples remain powerful; the discipline is choosing a small set of diverse, canonical examples over stuffing every edge case. Anthropic's phrasing: examples are the "pictures worth a thousand words" — but a slideshow of thirty pictures is noise.[^2]

**History and tool results: the silent majority.** In any long-running agent, accumulated turns and tool outputs dominate the window. This is tomorrow's entire lesson (compaction, structured notes, sub-agent isolation). Today's takeaway is just: the majority of your context budget is spent by the run itself, not by anything you wrote, so any context strategy that only addresses the prompt is managing the minority share.

**The unifying principle**, straight from the essay and worth quoting as doctrine: find *the smallest possible set of high-signal tokens that maximize the likelihood of the desired outcome*.[^2]

## Layer 4 — Just-in-time vs pre-loaded context

The pre-2025 default was pre-loading: embed everything, retrieve everything relevant, stuff the window before inference. The agentic alternative that now dominates production practice is **just-in-time context**: keep lightweight identifiers in the window (file paths, queries, links, database schemas) and give the agent tools to load content at the moment of need.[^2]

The canonical existence proof is Claude Code itself. It does not maintain a vector index of your repository. It navigates with `grep`, `glob`, `ls`, and targeted file reads, in a plan–act–observe loop against live filesystem state — and it writes analysis of multi-gigabyte data by inspecting heads and tails rather than ingesting files.[^2][^10] Thursday's lesson covers the full agentic-search-vs-embeddings debate; what matters today is the context-budget consequence: just-in-time loading means the window holds only what this step needs, and metadata (file names, folder structure, timestamps) does double duty as a signal layer the agent reasons over.

The honest tradeoff table:

| | Pre-loaded | Just-in-time |
|---|---|---|
| Latency per step | Low (already in window) | Higher (tool round-trips) |
| Token efficiency | Poor at scale | Good |
| Works when data is unindexed / live | No | Yes |
| Failure mode | Context rot, stale snapshots | Agent explores badly, misses what it never looks at |
| Best for | Small stable corpora; single-shot Q&A | Large/dynamic corpora; long-horizon agents |

Mature systems are hybrids: CLAUDE.md-style files dropped into context up front (cheap, always relevant), retrieval for precision, just-in-time exploration for everything else. The decision is per-workload, and Friday gives you the eval machinery to make it empirically rather than aesthetically.

## Layer 5 — Live controversy: discipline or rebrand?

**The skeptics' case.** A visible contingent of practitioners — you will find them in every comment thread under every context-engineering post, and in longer form in pieces like IntuitionLabs' comparison and the OpenAI developer-forum thread arguing the whole ladder is transitional — hold that context engineering is "rebranded prompt engineering, or worse, pseudoscientific buzzword creation": serious builders were assembling retrieval, memory, and tool output into windows years before the term existed, and giving it a title inflates a job function out of a technique.[^11] The sharpest version of the critique: renaming is what this industry does instead of maturing, and in two years another term will replace it (the same forum thread proposes "automated workflow architecture" as the successor — proving the treadmill it complains about).

**The proponents' case.** Karpathy's point was never that the work is new; it is that the *word* "prompt" miscommunicates the work, anchoring people to short task descriptions when the real object is a runtime-assembled window of instructions, retrieval, history, memory, and tool state.[^1] Philipp Schmid's widely-circulated July 2025 essay and Addy Osmani's "bringing engineering discipline to prompts" both land the same way: the rename is a correction, acknowledging that prompt-writing was always a subset of a larger systems problem, and the subset stopped being the interesting part.[^9][^11] By late 2025 the term had institutional weight — Anthropic's essay, dedicated framework support, Gartner briefings — which is either evidence that it names something real or evidence that hype cycles capture institutions too, depending on your priors.

**My position.** The rename earns its keep on one test: does it change what practitioners *measure*? Prompt golf optimized wording and eyeballed outputs. Context engineering, as actually practiced by teams who use the term seriously, budgets tokens per component, tracks effective-context benchmarks, and ablates additions. That is a different engineering loop, not a different word for the same loop. But the skeptics deserve one concession: nothing in this lesson required the term. If you practiced "prompt engineering" the way Anthropic practices "context engineering," you were doing context engineering. Fight about the discipline, not the noun. (And the discipline's own vocabulary is a moving target: as agentic patterns keep hardening, expect "harness engineering" and friends to contest the same ground.[^11])

## Worked example / runnable experiment — audit a real context window

No paste-and-run Python today; this is a Claude Code orchestration exercise on your own project. Time: 45–60 minutes.

**Phase 1 — measure.** Open a Claude Code session in the repo of your Week-4 RAG agent (or any real project). Run `/context`. Record the breakdown: system prompt, system tools, MCP tools, memory files, messages.[^10] This is your baseline ledger.

**Phase 2 — price it.** Paste into Claude Code:

> Read the output of /context I'm about to paste. Build me a table: component, tokens, % of window, cost per call at Sonnet 5 pricing ($3/$15 per Mtok — use the post-August standard rate so the numbers stay honest), and cost per 1,000 calls. Then flag the three components with the worst signal-per-token and explain your reasoning.

**Phase 3 — ablate one component.** Pick the worst offender it flags — typically an MCP server whose tools you rarely use, or a bloated CLAUDE.md section. Disable or trim it. Re-run `/context`, then re-run three representative tasks from your project and judge whether quality moved. You have just run your first context ablation; Friday formalizes the methodology and Saturday industrializes it.

**Phase 4 — the rot demo (optional, 15 min).** Take a question your RAG agent answers correctly with 5 retrieved chunks. Re-ask it with the same 5 chunks buried in 50 plausible-but-irrelevant chunks from the same corpus. Run each variant three times. Most readers see their first hands-on context-rot failure inside ten minutes, and it reliably converts "1M tokens means retrieval is dead" believers faster than any benchmark citation.

## Cross-domain examples — the budget outside engineering

The discipline is not a developer-only concern, and you will sell it to people who never open a terminal.

- *Sales team running an outreach agent.* The window fills with CRM history for every prospect "for personalization." Result: the model anchors on stale interactions and re-references a two-year-old objection in a fresh thread. The context-engineering fix is a curation rule (last 3 touches plus account facts, nothing older), and it is explainable to a sales manager in one sentence: the agent reads less and remembers better.
- *Legal review assistant.* Fifty exhibits pre-loaded "so it has everything." Multi-fact questions silently degrade in the middle of the pile, which is precisely the NoLiMa profile: low lexical overlap between the question and the governing clause. The fix is retrieval plus a clause-level citation requirement, and the pitch to the partner is accuracy, not cost.
- *Executive brief generator.* Board pack quality dropped after someone "helpfully" added the full prior-quarter transcript to the standing prompt. The deletion row wins here. Removing context is a legitimate deliverable, and clients find it more credible than additions because it cuts their bill.

The pattern to reuse in client conversations: name the budget, show the audit, propose one deletion and one addition, and put a measurement on both. That sequence works on stakeholders who would glaze over at the word "transformer."

## Problem set

1. **The audit memo.** Run the Phase 1–2 experiment on a real project and write a one-page memo: current window composition, cost per 1,000 calls, the two worst signal-per-token components, and one deletion proposal with an expected saving in dollars. Pass: every number traceable to the audit. Fail: any adjective ("bloated," "heavy") without a number attached.
2. **The rot probe design.** Without running it, design the Phase-4 rot demo for a corpus you actually work with: what is the "needle" task, what filler is realistic, at what sizes will you probe, and what result would falsify your current architecture? Pass: the probe uses your documents and your task shape, and names a decision that flips on the outcome.
3. **The altitude rewrite.** Take a system prompt you own that contains at least five if-then rules. Rewrite it at Goldilocks altitude: heuristics plus structure, half the tokens. Run five representative tasks on both versions and record which failures appear and disappear. Pass: a before/after table. Fail: a rewrite you never ran.
4. **The skeptic's brief (position defense).** In 300 words, argue *for* the position that context engineering is a rebrand, citing the strongest evidence from this lesson honestly. Then one paragraph: the single measurable practice that survives even if the term dies, and why. This is Sunday-quiz preparation; the exam rewards people who can argue both sides.
5. **The tokenizer trap (calc).** Your April cost model assumed 1M tokens of monthly context spend at $3/Mtok input. The current tokenizer emits ~30% more tokens for the same text.[^8] Recompute the monthly spend, then compute what percentage of context you must *delete* to hold the old budget constant. Show the arithmetic.

## Common mistakes experts see

- **Filling the window because it's there.** The advertised window is a ceiling, not a target. Every token past sufficiency is paid noise.
- **Auditing prompts but not tools.** Teams iterate the system prompt for weeks while three MCP servers silently occupy five figures of tokens per call.
- **Case-table system prompts.** If-else logic in prose. Brittle, long, and it fights the model. Heuristics over enumerations.
- **Assuming rot is linear or uniform.** Chroma showed degradation varies by task, distractor profile, and model family.[^3][^4] Test your workload; don't extrapolate from a needle test.
- **Treating "it fits" as "it works."** Fitting 400K tokens into a 1M window says nothing about whether token 380,001 influences the answer. NoLiMa's effective-length concept exists precisely because fit and function diverge.[^5]
- **Refusing long context on principle.** The inverse error. A deliberate 300K-token single-shot analysis can beat an elaborate retrieval pipeline. The sin is defaulting, in either direction, without measuring.
- **Optimizing wording before composition.** Rewriting sentences in a window whose composition is wrong is polishing deck chairs. Composition first, wording second.

## Reflection questions

1. Your agent's window is 70% accumulated tool results. A colleague proposes a bigger context window as the fix. Using the attention-budget frame and one benchmark result from this lesson, argue why that may make behavior *worse*, and name the condition under which they'd be right.
2. Take Karpathy's definition apart: which words distinguish it from a good definition of prompt engineering, and would a skeptic accept the distinction as more than scope creep?
3. Your `/context` audit found MCP tool definitions at 22% of the window. Name three different remediations with different cost/risk profiles, and what you'd measure to choose.
4. NoLiMa minimizes lexical overlap between question and needle. Why does that single design choice change the ranking of models relative to classic needle-in-a-haystack, and what does it imply about which *production* workloads rot fastest?
5. Construct the strongest case that the context-engineering rename will look silly by 2028. Then name the one measurable practice from this lesson you'd keep even if the term dies.
6. Where in your current stack are you pre-loading context that should be just-in-time? What identifier (path, query, key) would you leave in the window instead?

## My take (reviewer lens)

**Karpathy** would sharpen, not soften, the definitional section: his tweet is being used as a slogan, but his actual claim included that context engineering is one slice of a thicker software layer — state management, control flow, model routing — and a lesson that stops at "curate tokens" undersells the systems problem. He'd also warn against over-indexing on benchmark numbers from specific models: the models will churn; the attention-budget reasoning is what transfers. **Hamel Husain** would push on the missing error-analysis loop: the lesson says "measure," but a `/context` audit is not an eval, and teams will trim the component that *looks* wasteful rather than the one their failure traces implicate; his P6 note exists because context rot shows up in traces first.[^4] Fair — Friday's lesson is the answer, and the Phase-3 ablation here is deliberately a toy. **Jeremy Howard** would push back on the vocabulary itself: fast.ai has spent a decade watching renamed disciplines inflate course catalogs, and he'd note this lesson spends a full layer adjudicating a naming dispute that a practitioner could ignore entirely with no loss of capability. Guilty, with intent: you will be selling this skill, and the buyer will use the new word.

## Further reading

**Must-read**
- Anthropic Engineering, *Effective context engineering for AI agents* (Sep 29, 2025).[^2] The canonical text for this whole week.
- Chroma Research, *Context Rot* (Jul 2025).[^3] Read the haystack-structure findings; they are the least intuitive.
- NoLiMa paper, §4–5 (results and effective-length table).[^5]

**Recommended**
- Karpathy's original thread.[^1] Two minutes, endlessly cited; read the primary source.
- Philipp Schmid, *The New Skill in AI is Not Prompting, It's Context Engineering* (Jul 2025).[^9] The best short practitioner statement.
- Hamel Husain, *P6: Context Rot*.[^4] Operator commentary, model-family differences.

**Optional**
- RULER paper for the task-category taxonomy.[^6]
- The skeptics' thread on the OpenAI developer forum[^11] — read it to steelman the other side before Sunday's quiz asks you to.

## Citations

[^1]: Andrej Karpathy, X post, June 25, 2025: "+1 for 'context engineering' over 'prompt engineering'… the delicate art and science of filling the context window with just the right information for the next step." https://x.com/karpathy/status/1937902205765607626 — Tobi Lütke's June 19, 2025 post defined it as "the art of providing all the context for the task to be plausibly solvable by the LLM." (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^2]: Anthropic Engineering, *Effective context engineering for AI agents*, September 29, 2025. Definitions of context engineering vs prompt engineering; attention budget; system-prompt altitude; token-efficient tools; just-in-time context; "smallest possible set of high-signal tokens." https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents (search-verified 2026-07-17 via multiple secondary corroborations incl. marktechpost.com and howaiworks.ai; fetch egress-blocked — liveness pass pending)

[^3]: Kelly Hong, Anton Troynikov, Jeff Huber (Chroma Research), *Context Rot: How Increasing Input Tokens Impacts LLM Performance*, July 2025. 18 models evaluated; non-uniform degradation; distractor and haystack-structure effects. https://www.trychroma.com/research/context-rot ; replication toolkit: https://github.com/chroma-core/context-rot (search-verified 2026-07-17; also cited with URL in [[05-fri-advanced-rag]])

[^4]: Hamel Husain, *P6: Context Rot*, hamel.dev. Operator commentary; differential rot across model families. https://hamel.dev/notes/llm/rag/p6-context_rot.html

[^5]: Ali Modarressi et al. (Adobe Research / LMU), *NoLiMa: Long-Context Evaluation Beyond Literal Matching*, arXiv 2502.05167, ICML 2025, §4–5. Effective length = longest context retaining ≥85% of base score; at 32K, 11 models below 50% of baseline; GPT-4o 99.3% → 69.7%. https://arxiv.org/abs/2502.05167 (search-verified 2026-07-17)

[^6]: Cheng-Ping Hsieh et al. (NVIDIA), *RULER: What's the Real Context Size of Your Long-Context Language Models?*, arXiv 2404.06654. 13 tasks, 4 categories; effective-length threshold calibrated at 85.6% (Llama-2-7B at 4K). https://arxiv.org/abs/2404.06654 ; https://github.com/NVIDIA/RULER (search-verified 2026-07-17)

[^7]: Community long-context leaderboards and analyses tracking RULER/MRCR/NoLiMa-class results into 2026, e.g. https://awesomeagents.ai/leaderboards/long-context-benchmarks-leaderboard/ and the mid-2026 accuracy-past-200K analysis at https://ofox.ai/blog/long-context-llm-benchmarks-200k-tokens-2026/ (30–60-point advertised-vs-effective divergence claim; single-analysis figure — treat as indicative). (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^8]: Claude Sonnet 5: released 2026-06-30, 1M-token window, intro pricing $2/$10 per Mtok through 2026-08-31, then $3/$15; current-generation tokenizer produces ~30% more tokens for the same text. Corroborated via https://www.anthropic.com/news/claude-sonnet-5 (per vault landscape delta, URL-verified 2026-07-17), https://pricepertoken.com/pricing-page/model/anthropic-claude-sonnet-5 and https://www.aimadetools.com/blog/claude-sonnet-5-pricing-explained/ (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending). 1M-window ubiquity across vendors: see [[05-fri-context-window-economics]].

[^9]: Philipp Schmid, *The New Skill in AI is Not Prompting, It's Context Engineering*, philschmid.de, July 2025. Component taxonomy of production context. https://www.philschmid.de/context-engineering (search-verified 2026-07-17)

[^10]: Claude Code docs, *Explore the context window* — `/context` command and window breakdown; compaction pipeline details in tomorrow's lesson. https://code.claude.com/docs/en/context-window (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^11]: Skeptic and steelman sources: IntuitionLabs, *Context Engineering vs. Prompt Engineering* ("many experienced developers see context engineering as rebranded prompt engineering," https://intuitionlabs.ai/articles/context-engineering-vs-prompt-engineering-ai); OpenAI Developer Community thread, *Prompt Engineering Is Dead, and Context Engineering Is Already Obsolete* (https://community.openai.com/t/prompt-engineering-is-dead-and-context-engineering-is-already-obsolete-why-the-future-is-automated-workflow-architecture-with-llms/1314011); Addy Osmani, *Context Engineering: Bringing Engineering Discipline to Prompts* (https://addyo.substack.com/p/context-engineering-bringing-engineering). (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

_last_verified: 2026-07-17_
