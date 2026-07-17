---
type: lesson
block: block-0-basecamp
week: week-02
day_of_cycle: 6
day_name: sat
session_slug: basecamp-part-4-revisiting-n8n-ai-agent-fundamentals
date_due: 2026-05-09
tags: [agents, react, planning, memory, tool-use, evals, tau-bench, bfcl, swe-bench, orchestrator-workers, plan-mode]
sources:
  - yao-2022-react
  - anthropic-2024-building-effective-agents
  - yao-2024-tau-bench
  - sierra-2025-tau2-bench
  - patil-2024-bfcl
  - anthropic-opus-4-5
  - anthropic-opus-4-6
  - openai-gpt-5
  - deepmind-gemini-3-1-pro
  - cognition-swe-bench-technical-report
  - claude-code-plan-mode
  - langchain-memory-for-agents
  - hamel-husain-llm-judge
  - alan-benchmark-tradeoffs
  - swe-bench-pro-2025
  - anthropic-claude-fable-5-mythos-5-2026
  - anthropic-claude-sonnet-5-2026
last_verified: 2026-07-17
word_count_target: 6000
---

# Agent fundamentals deeper — ReAct, planning vs execution, memory, tool-use architecture, and what the evals actually tell you

## Why this matters

Most "AI agents" shipping to production in 2026 are a ReAct loop wearing different hats. You already use them daily — Claude Code is one, your n8n flows wrap them, the voice agent you set up on Thursday is another. The question you now need to answer, as the person accountable for the system, is not *"how do I build an agent?"* It is:

- When should the agent plan first versus interleave reasoning with actions?
- Which memory strategies earn the complexity they add, and which are cargo cult?
- What does TAU-bench 86% actually tell you about whether this agent will survive contact with your customers?
- Why do all five Anthropic "agent patterns" collapse to the same two architectures at 3 a.m. when something breaks?

By the end of this lesson you will have run the same bug-fix task through Claude Code twice — once in Plan mode, once in interleaved mode — and you will have numbers on tool-call count, wall time, and diff quality. You will have a working model of why frontier models still plateau around 70% on τ²-bench airline even as SWE-bench climbs past 80%. And you will know which of your current automations should *not* be agents at all.

## Prerequisites

- [[01-mon-prompting-first-principles]] — the distribution-shifting mental model. Everything an agent does is still next-token prediction; tools are just tokens that cause side effects.
- [[01-mon-mcp-as-a-protocol]] — MCP as the standard way to expose tools. We assume you've wired at least one. (The [[03-wed-mcp-security]] lethal-trifecta frame is the security counterpart.)
- Claude Code installed and working on a real repo. Not a toy. You need a codebase with at least one open bug or TODO for the experiment.
- Read the first five pages of Anthropic's *Building Effective Agents* (Dec 2024)[^1] before the experiment. 15 minutes.

## Layer 1 — ReAct, revisited with four years of hindsight

Shunyu Yao's *ReAct* paper dropped on arXiv in October 2022[^2] and quietly became the load-bearing abstraction of the entire agent stack. Read the paper today and three things jump out.

**First, the core claim is structural, not magical.** ReAct proposed that interleaving *reasoning traces* with *actions* — `Thought: ... / Action: ... / Observation: ...` in a loop — outperforms either reasoning alone (Chain-of-Thought) or acting alone (WebGPT-style tool use). On HotpotQA and Fever, reasoning-only hallucinated; action-only propagated errors; the interleaved version did neither. On ALFWorld (household task simulator) and WebShop, ReAct beat imitation learning and RL baselines by 34% and 10% absolute with one or two in-context examples.[^2]

**Second, the "agent loop" you think you're running is almost exactly ReAct with better scaffolding.** Claude Code, OpenAI's Assistants API, LangGraph, AutoGPT's corpse, n8n's AI Agent node — all of them run some variant of:

```
while not done:
    thought = LLM(history)
    action = parse_tool_call(thought)
    observation = execute(action)
    history.append(thought, action, observation)
```

The post-2024 additions are mostly cosmetic-looking but load-bearing in practice: structured tool-call JSON instead of free-text parsing, parallel tool calls in a single turn, validated inputs via JSON Schema, and model-native training on these patterns so you don't need the few-shot examples Yao needed.

**Third — and this is the part most tutorials miss — ReAct's original framing assumes the reasoning is *generative*, not *post-hoc*.** We already covered this ghost in [[01-mon-prompting-first-principles]]: Lanham 2023 and Turpin 2023 showed that chain-of-thought traces are frequently post-hoc rationalizations, not causal drivers of the answer. For an agent, this has a specific and dangerous consequence: **the `Thought:` text that justifies a tool call may not be what actually drove the call.** If the model is going to call `delete_customer_record` because something in the context pattern-matched to a stereotype of "irate user deserves escalation," the `Thought:` field will give you a plausible-sounding business justification for the deletion. It will not mention the pattern match. Logging `Thought:` as an audit trail is a compliance story you cannot back up with research.

Operationally: treat `Thought:` as useful for debugging token-level behavior, not as ground truth about why the agent acted. For audit, log inputs, tool calls, and outputs. Not reasoning.

### What 2025-era ReAct loops add

- **Structured tool calls.** Every major provider now trains the model to emit tool calls as JSON matching a declared schema, not as free text the framework regexes out. This alone eliminates a class of parsing failures that plagued LangChain 0.0.x.
- **Parallel tool calls in one turn.** Every current frontier model emits arrays of tool calls per step. For read-heavy investigation (e.g., "check these 8 files"), this collapses 8 round-trips into 1.
- **Result truncation and summarization.** Tool outputs that blow context (a 50MB log file, a full DB dump) are truncated or summarized by a smaller model before being fed back. Cognition's SWE-bench technical report and Anthropic's agent engineering posts both cite context explosion as the #1 cause of multi-turn agent failures.[^3]
- **Explicit stop conditions.** The naive ReAct loop runs until the model says "done." Production loops add max-steps, max-tool-calls-per-type, budget caps, and loop-detection (is the model calling the same tool with the same args three times in a row?).

> My take: the thing ReAct got right, which is easy to miss, is that the *observation* step is where learning happens in-context. The biggest quality lift you can give a legacy ReAct agent today is not a better model — it's a better `observation` formatter. If your tool returns a 500-line JSON blob, the model has to spend attention parsing it before it can reason. Return pre-digested summaries with the actual signal on top.

## Layer 2 — Anthropic's five patterns and why they collapse to two

In December 2024 Anthropic published *Building Effective Agents*[^1], which is the single most operationally useful document on agents written to date. It does three things: names five workflow patterns, distinguishes workflows from agents, and argues that most teams should not be building agents at all.

The five patterns:

1. **Prompt chaining.** `LLM → LLM → LLM`. Each call consumes the previous output. Used when the task decomposes cleanly into a fixed sequence: *draft → critique → revise*, or *extract → validate → format*. No dynamic routing. Deterministic control flow.
2. **Routing.** A classifier LLM picks one of N downstream specialists. Used when you have distinct handling paths that benefit from specialized prompts (support tier-1 vs. tier-2, code question vs. policy question).
3. **Parallelization.** Run N LLM calls concurrently, either on chunks of one task (sectioning) or on different perspectives of the same task (voting). Fan-in aggregator combines.
4. **Orchestrator-workers.** A central LLM dynamically decomposes a task at runtime and dispatches to worker LLMs. Distinguishes from prompt chaining by having *dynamic* rather than hard-coded sub-tasks.
5. **Evaluator-optimizer.** One LLM produces; another critiques; loop until the critic passes. Used when quality criteria are well-specified and iterating helps.

All five are workflows in Anthropic's taxonomy — the control flow is fixed by code. A true *agent* has the LLM deciding its own control flow at runtime, usually by choosing tools. Claude Code is an agent. An n8n flow with three sequential LLM nodes is a prompt chain.

**The collapse:** once you've built a dozen of these, you realize there are two underlying architectures and the five patterns are just styling:

- **Fixed-DAG workflows.** The graph of LLM calls is defined in your code. Prompt chaining, routing, parallelization, and most evaluator-optimizer setups live here. These are *programs with LLMs as functions*. Predictable, debuggable, cheaper.
- **Loop-driven agents.** The LLM chooses the next action at each step. Orchestrator-workers at the extreme, full ReAct agents in the middle. These are *programs where the LLM is the scheduler*. Powerful, unpredictable, expensive.

The Anthropic guide's most important single sentence is: *"When building applications with LLMs, we recommend finding the simplest solution possible, and only increasing complexity when needed. This might mean not building agentic systems at all."*[^1] Re-read that after your next production agent incident. It is the most-ignored line in the agent literature.

**Domain examples of each pattern actually earning its complexity:**

- *Prompt chaining (legal):* extract clauses → classify risk → draft red-line memo. Hard-coded sequence; you know the shape in advance.
- *Routing (e-commerce support):* classify intent → route to refund-handler vs. shipping-tracker vs. human-escalation. Specialized prompts per lane reduce hallucination.
- *Parallelization (security):* run the same PR through five critic prompts — auth, injection, secrets, deps, perf — in parallel; aggregator summarizes. Votes catch what single-pass misses.
- *Orchestrator-workers (research):* break "analyze this market" into sub-queries, dispatch each to a sub-agent with web search, synthesize. Sub-tasks not known at author time.
- *Evaluator-optimizer (localization):* translator produces; native-speaker-simulating critic rejects on register/idiom; loop. Works because quality is well-defined even when diverse.

### Reviewer lens on the guide

*Three specific disagreements I'd push on Anthropic's write-up:*

1. **The orchestrator-workers pattern quietly assumes the orchestrator can reliably decompose.** In practice, decomposition is the hardest part. A weak orchestrator with strong workers performs worse than a medium model running plain ReAct. The guide doesn't emphasize this enough — anyone who's debugged a multi-agent system knows the bottleneck is always the planner.
2. **The evaluator-optimizer pattern has a quiet assumption that the evaluator is better than the generator.** If they're the same model, you get a model-vs-itself loop where the critic's blindspots match the generator's. Hamel Husain has written repeatedly that aligned LLM judges require domain-expert critique shadowing before they become reliable.[^4] The guide notes this but doesn't emphasize how often teams skip it.
3. **"Agents" as defined in the guide map almost 1:1 to ReAct** — the guide gestures at this but never names the equivalence. Calling your product "agentic" in 2026 and meaning "it loops ReAct-style with tools" is marketing, not architecture.

## Layer 3 — Planning vs execution: the live controversy

Here is the argument you will be asked to have, probably in the next three months, by a skeptical engineering lead: *should our agent plan first, or interleave reasoning with action?*

### Position A — Explicit-plan-first

Claude Code's **Plan mode** is the canonical implementation.[^5] Activate it (Shift+Tab twice, or `/plan`) and Claude enters a read-only research phase: it can read files, grep, ask clarifying questions — but cannot write, execute shell, or edit. It produces a plan. You approve. Then it executes.

Arguments for:
- Plans are inspectable before anything side-effects. Massive for high-stakes changes.
- Decomposition upfront catches ambiguity earlier than decomposition mid-execution.
- Anthropic's orchestrator-worker pattern formalizes this: separate *planner LLM* decomposes; *worker LLMs* execute each step.[^1]
- Cognition's SWE-bench technical report describes Devin using a plan-decompose-execute architecture for multi-hour coding tasks; they argue interleaved ReAct loops accumulate context errors past ~20 steps.[^3]

### Position B — Interleaved / ReAct-style

Most ReAct-descended agents (the original Yao 2022 loop, OpenAI Swarm, many LangGraph default patterns) interleave reasoning with acting at every step. No separate plan phase.

Arguments for:
- Plans made before observing the environment are frequently wrong. Real codebases, real APIs, real data surprise you. Dynamic reasoning adapts.
- For short tasks (< 10 tool calls) the overhead of planning exceeds the gain. Measured on TAU-bench airline, plan-first variants often lose on short user interactions because the plan is longer than the execution.
- Yao's original result stands: on HotpotQA and ALFWorld, interleaved reasoning + action beat planning-heavy baselines *because* the model could adapt to observations the plan couldn't anticipate.[^2]

### What the 2025-2026 data actually says

> **A note on model names before the numbers.** The benchmark figures below are attached to the models that *set* them at the time — Opus 4.5/4.6, GPT-5, Gemini 3.1 Pro. Read them as historical high-water marks, not the current frontier. As of mid-2026 the lineup has moved several generations: Anthropic ships **Claude Fable 5 / Mythos 5** (Jun 2026, a new Mythos-class tier above Opus, $10/$50 per Mtok, 1M context), **Opus 4.8** (May 2026), and **Sonnet 5** (Jun 2026, the new default agent tier); OpenAI ships **GPT-5.6** (Sol/Terra/Luna, GA Jul 2026); the open-weight frontier essentially closed with **Kimi K3** (Jul 2026). The *shape* of the findings — plan-heavy agents topping SWE-bench, pass^k collapse on TAU-bench — is what generalizes; the leaderboard numbers churn monthly, so check a live source (e.g. metr.org/time-horizons, Artificial Analysis) before quoting one.

- **SWE-bench Verified and SWE-bench Pro** reward long-horizon planning. Claude Opus 4.5 hit 80.9% on Verified; Opus 4.6 pushed higher, and the current Fable-5/Sonnet-5 generation higher still; on SWE-bench Pro (real enterprise repos, harder tasks) all frontier models drop 20+ points.[^6][^7] Plan-heavy agents dominate the top of these leaderboards.
- **TAU-bench / τ²-bench** (airline, retail, telecom) reward *local adaptation to a simulated user*. Claude Opus 4.6 hit 99.3% on telecom and 91.9% on retail — but airline, which has more edge-case policy rules, stays harder.[^8] GPT-5 reached 96.7% on telecom with 45% fewer tool calls than prior models.[^9] Crucially, these scores are pass^1. Pass^8 on the airline domain stays below 40% for everyone, generation after generation — *reliability* under repeated trials is where everyone fails.[^10]
- **Tool-specialized endpoints are now a pattern, not a one-off.** Gemini 3.1 Pro shipped a separate `gemini-3.1-pro-preview-customtools` endpoint tuned for autonomous agent behavior and briefly took the Artificial Analysis Intelligence Index crown in late 2025.[^11] The generalizable data point survives the model churn: at the frontier, planning and tool-use benefit from different training signals, which is why vendors keep shipping agent-tuned variants alongside the base reasoning model.

### My operational take

The question is mis-framed. The real axis is task horizon and reversibility:

| Task shape                                                  | Use                         |
|-------------------------------------------------------------|-----------------------------|
| Long, touches many files, irreversible (DB migration, prod deploy, multi-file refactor) | Plan-first (Plan mode, or orchestrator-worker) |
| Short, read-mostly, cheap to retry (investigation, debugging, search) | Interleaved ReAct |
| Long but repetitive structured steps (ETL, batch transforms) | Fixed-DAG workflow, not an agent at all |
| Customer-facing, single user turn, conversational (τ²-bench shape) | Interleaved with hard policy guardrails |

War story: on an actual client engagement (Q1 2026) we replaced a ReAct agent with a plan-first pattern for a nightly data-reconciliation job. The ReAct version averaged 23 tool calls per run and hit a loop-detection abort ~8% of nights. Plan-first averaged 11 tool calls, aborted < 1%, but cost 2.4× more per run (reasoning tokens) and took 40% longer wall-clock. We kept plan-first — the on-call burden of 8% nightly failures was worth the extra $34/day. Your tradeoff will be different, and the numbers only exist because we measured both.

## Layer 4 — Memory strategies: four types, and when each earns its complexity

The agent-memory literature has converged on a four-type taxonomy borrowed from cognitive science. LangChain's memory docs, Oracle's developer blog, and OpenAI's Assistants architecture all reference roughly the same four.[^12]

1. **Working memory — the context window.** Everything in the current conversation. Cheapest, most reliable, capped by context length. *Earns complexity when:* tasks fit in one session.
2. **Episodic memory — past conversations.** Stored verbatim or summarized, retrieved by recency or relevance. Usually a vector store over chat logs, or a Postgres table with embeddings. *Earns complexity when:* the agent interacts with the same user across sessions AND past interactions meaningfully change current behavior (support, personal assistant, long-running research project). *Does NOT earn complexity when:* each session is functionally independent (utility tools, stateless lookups).
3. **Semantic memory — facts about the world.** Profiles, preferences, domain knowledge. Can be explicit (a user-profile record) or implicit (vector store of learned facts). *Earns complexity when:* facts accumulate faster than the user can specify them in a system prompt, AND stale facts have low cost to be wrong. *Red flag:* if your semantic memory writes are unvalidated, you will eventually poison it with the model's own hallucinations. LangChain's LangMem docs explicitly warn about this.[^12]
4. **Procedural memory — skills and routines.** *How* to do things. In Claude Code this is skills; in a custom agent it's the system prompt plus reusable sub-routines. Usually stored in files/code, not a vector DB. *Earns complexity when:* the same multi-step pattern recurs enough that inlining it costs more tokens than loading it on demand.

**The complexity test** — ask for each memory type:

- What writes to it? How are those writes validated?
- What reads from it? Under what conditions?
- What is the cost of a stale or wrong memory vs. the cost of not having it at all?
- Can a system prompt and the current context window do the same job?

If the last question is "yes," skip the memory system. The number of production agents with a vector-store "memory" that does nothing the system prompt couldn't do is staggering. Cross-domain examples:

- *Medical triage agent:* episodic memory earns its keep (same patient, multiple contacts). Semantic memory is dangerous — hallucinated facts about a patient's medication history can kill someone. Use episodic-only, curated by humans.
- *Sales outreach agent:* semantic memory on accounts is gold (decision makers, last contact reason). Episodic on every LinkedIn check-in is noise.
- *Developer coding agent:* procedural memory (skills, CLAUDE.md) dominates. Episodic memory of past PRs is rarely worth retrieving — the current diff contains almost everything that matters.
- *Customer support agent:* all four — working (current ticket), episodic (past tickets from this customer), semantic (product facts), procedural (escalation policies). But you should build them in that order and stop when quality stops improving.

## Layer 5 — Tool-use architecture details that bite you

Three specifics most agent tutorials skip, because you only learn them at scale.

### Parallel tool calls

Every frontier model in 2026 emits multiple tool calls per turn. Your framework decides whether to execute them in parallel or serially. **Always parallel unless ordering matters.** Read-only calls (grep, file read, DB select, web search) can all fan out. Write calls usually cannot. The naive "execute each tool_call sequentially" loop that ships with many frameworks leaves 5-10× latency on the table.

But — parallel tool calls also amplify failure modes. If the model fans out 10 searches and one fails, how does your framework report back? If it silently drops the failed one, the model reasons on incomplete evidence and confidently concludes nonsense. Instrument every tool-call leg. Surface failures in the observation, not just success.

### Validated tool inputs

JSON Schema validation on tool inputs is mandatory, not optional. The model will, at non-trivial rates, hallucinate:

- Wrong types (string where int expected)
- Missing required fields (the current frontier tier has largely fixed this; smaller/cheaper models haven't)
- Extra fields that you silently ignore but shouldn't
- Enum values outside the allowed set
- Schema-valid but semantically nonsense combinations (start_date > end_date)

The Berkeley Function Calling Leaderboard (BFCL) v3 specifically tests *multi-turn* function calling with schema adherence; v4 added *holistic agentic evaluation* with real-world data.[^13] Read the BFCL leaderboard methodology once, then design your tool schemas to match — you'll save weeks of debugging.

### Tool result truncation

Tools return data of unpredictable size. A `read_file` on a 2MB YAML? A `grep` that matches 4000 lines? A DB query returning 100k rows? If you feed these raw into the next LLM turn you will:

1. Blow the context window (hard failure).
2. Blow your budget (soft failure, often goes unnoticed until the invoice).
3. Drown the signal in noise (silent quality drop — the bit the model needed is at token 47,000 of 80,000 and attention doesn't reach it).

Production pattern: every tool that can return > 2k tokens gets a wrapper that summarizes or paginates. The wrapper often calls a smaller/cheaper model to compress before returning. Your agent's "intelligence" is largely a function of how well you design these compressors.

## Layer 6 — Evals: what TAU-bench, BFCL, and SWE-bench actually measure

Before the experiment, a field guide to the three benchmarks you will see cited in every agent release note.

### TAU-bench / τ²-bench (Yao et al. 2024, arXiv 2406.12045)

Two domains in the original — airline customer service, retail — later extended to telecom in τ²-bench.[^14][^8] The agent is given tools (APIs) and policy guidelines. A *simulated user* (another LLM) drives the conversation. The agent must resolve the user's issue while following policy. Evaluation compares final database state to a gold state.

What it measures well:
- Tool-use fluency in a multi-turn conversation.
- Policy adherence (the airline domain has gnarly rules about basic-economy flights).
- Ability to refuse or redirect bad user requests.

What it measures badly:
- **Reliability under repeated trials.** The paper introduced pass^k precisely because pass^1 is misleading — even frontier models that average 60%+ pass^1 drop below 25% on pass^8 in the original paper.[^14] If your production use case requires the same agent to handle the same edge case consistently 8 times in a row, headline TAU-bench scores are a trap.
- **Arithmetic and state tracking.** A recurring failure mode: agents narrate their plan confidently while underlying numbers drift.[^10]
- **Adversarial users.** The simulated user is cooperative. Real users aren't.

### BFCL (Berkeley Function Calling Leaderboard)

BFCL v1 introduced AST-based evaluation of function-call correctness. v2 added enterprise and community-contributed functions. **v3 (Sept 2024) added multi-turn and multi-step function calling.** v4 added holistic agentic evaluation with periodically-refreshed real-world data.[^13]

Use BFCL to answer: does model X emit syntactically valid, semantically appropriate function calls? It does not answer: will the agent built around model X succeed on your workflow? Those are different questions, and the gap between them is where every production agent lives.

### SWE-bench Verified and SWE-bench Pro

Real GitHub issues from popular Python repos; agent must produce a patch that passes the hidden test suite. Verified = 500 human-validated tasks. Pro = 2025's harder, enterprise-repo variant.[^7]

Claude Opus 4.5 hit 80.9% on Verified and Opus 4.6 exceeded it (GPT-5 sat around 74.9%); the current Fable-5/Sonnet-5/GPT-5.6 generation is higher still, yet all frontier models continue to drop 20+ points on Pro.[^6][^9][^7] The plateau is informative and durable across generations: either the remaining gap needs a capability qualitatively different from scaling, or the benchmark has hit a ceiling imposed by test-suite brittleness. Probably both.

### The live controversy — are these good proxies for production?

*Position A (industry default):* yes, with caveats. Track TAU-bench telecom + SWE-bench Verified + BFCL v4 together; any model that moves up on all three is a better agent base model.

*Position B (Hamel Husain, Alan engineering blog, Sierra's own papers):*[^4][^10][^14] no. Headline benchmark scores are pass^1 averages that hide the pass^k collapse. Prompt optimization creates 10+ percentage point divergences in reproduction attempts. Agents that "reason well" on a benchmark can fail on the exact same task under mild user pressure. Your eval for *your* production agent — domain-specific, adversarial, pass^k — is the only eval that matters. Benchmarks are for model-selection first-pass, not deployment gates.

My position is Position B with a concrete addition: **use benchmarks for triage, then build a 50-example domain-specific eval set with LLM-as-judge validated against expert critique shadowing (Hamel's protocol).**[^4] If you don't have that, you don't have eval; you have vibes plus a leaderboard.

## Runnable experiment — plan-first vs interleaved, on a real bug

You will run this on a real codebase with a real bug. Not a toy. Pick a repo you know, find an open issue or a TODO that's been bugging you, and use that.

**Setup.** Open Claude Code in the repo. Pick one task — something that touches 2-5 files and takes ~20-40 minutes by hand. If nothing qualifies, pick a nontrivial refactor: "split this 800-line file into three modules along these boundaries."

**Step 1 — interleaved run.** Fresh Claude Code session. No Plan mode. Paste the task verbatim. Let Claude run end-to-end. Record:
- Tool calls made (count from the transcript — Claude Code shows each one).
- Wall time from first message to final "done."
- Final diff — save as `interleaved.patch`.
- Number of times Claude asked a clarifying question.
- Any loops/retries/backtracks.

**Step 2 — plan-first run.** Fresh session on the same commit (git stash or branch cleanup). Activate Plan mode (Shift+Tab twice). Paste the identical task. Let Claude produce a plan. Read it carefully. Approve or request one round of revisions, then exit Plan mode and execute. Record the same five metrics. Save as `planfirst.patch`.

**Step 3 — grade the diffs.** Two checks:

- *Correctness.* Run the tests. Does each patch pass? (If you don't have tests, write two quick ones before starting. This is the biggest single lift you can give the experiment.)
- *Quality.* Diff the two patches against each other. Which is closer to what you would have written? Which adds unneeded changes? Which misses something?

**Step 4 — direct Claude Code to summarize.** Paste this:

> I just ran the same task two ways. Read `interleaved.patch` and `planfirst.patch`. For each:
> - Describe the architectural choice.
> - Flag any bugs or code smells.
> - Rate on correctness, minimality, and style on 1-5.
> Then produce a recommendation: which approach would you ship, and what changes would you make before merging?

**What you should see.** Most experienced users report: interleaved is faster and has lower tool-call count on tasks under ~8 steps; plan-first wins on tasks over ~15 steps and on anything touching more than three files. If your numbers strongly diverge from that pattern, the task itself is probably at an awkward length, or Plan mode needed more context (CLAUDE.md, pointers to relevant files) that you didn't provide.

**Deliverable.** A five-line writeup in your notebook: task, tool calls (interleaved / plan-first), wall time, diff quality, which you'd ship. You now have a micro-dataset of one on a question most people only have opinions about. Do this three more times this month on different task shapes and you will have calibrated judgment nobody around you has.

## Common mistakes experts see

1. **Wrapping a fixed-DAG workflow in the word "agent" because it sounds better in the pitch deck.** If the control flow is hard-coded, it's a workflow. Call it one. You'll debug it faster.
2. **Logging `Thought:` as an audit trail.** Post-hoc rationalization, not causal trace. Log inputs → tool calls → outputs. Nothing else has deposition-grade integrity.
3. **Vector-store memory that nothing reads.** Check your own system: count the retrievals per session. If median is zero, delete the memory system and reclaim the latency.
4. **Parallel tool calls with silent failures.** One leg of a fan-out fails; framework drops it; model reasons on incomplete evidence. Instrument every leg.
5. **Choosing a base model by TAU-bench pass^1.** The 60% → 25% pass^8 collapse in the original paper is still the rule, not the exception. If your production SLO needs 99% task completion, headline scores are marketing.
6. **No tool-result truncation.** A 50MB log eats your context budget and drowns the signal. Compress at the tool-wrapper layer, not the prompt layer.
7. **Orchestrator-worker with a weak orchestrator.** The planner is the bottleneck. Put your strongest model there; don't balance the cost across layers.
8. **Evaluator-optimizer where evaluator == generator.** Blindspots match. Use a different model or a different prompt style for the critic, or use a human critique set (Hamel's critique shadowing).

## Reflection questions

1. For each production agent you run or have reviewed this year: is it a workflow or an agent in Anthropic's taxonomy? Could it be demoted to a workflow with no capability loss and cleaner debugging?
2. Pick one of your current agents. What does its episodic memory actually *change* about behavior? If you ablated it tomorrow, which user-visible outcomes would move, and by how much?
3. If TAU-bench pass^1 and pass^8 diverge by 2× on frontier models, what pass^k target would *your* production use case require? How would you measure it on your own workload?
4. Claude Code's Plan mode is a product decision to separate research from execution. What is the analogous separation in your domain's workflow, and have you built it?
5. You have 30 minutes to improve an existing ReAct agent that's underperforming. Before touching the model, what three things do you instrument and log?

## My take (reviewer lens — three disagreements with this lesson itself)

Where this lesson cuts corners, in case you're reading critically:

1. **I've treated the ReAct/plan-first distinction as a clean binary.** It isn't. Modern agent frameworks mix them — plan high-level, ReAct the sub-steps, re-plan on failure. The table above is a starting heuristic, not a taxonomy. Karpathy would roll his eyes at the oversimplification; he'd be right; the table is still useful on Monday morning.
2. **The memory-taxonomy claim that "the field has converged" is stronger than the evidence.** LangChain and OpenAI use the four-type split; plenty of systems in production use simpler two-tier (context + vector) or richer graph-based memory (Mem0, Letta). Michael Seibel would say: don't adopt a four-layer memory system because a blog post told you to; ship the ugly two-tier version first and see what fails.
3. **I gave benchmarks a hard critical read but still told you to use them.** That tension is real. Boris Cherny would note: the tooling bias in BFCL (AST-based eval favors models whose training data matches the benchmark's function-shape distribution) means a high BFCL score partly measures "how much BFCL-shaped data was in the training set." Benchmarks are imperfect but the alternative — no measurement — is worse. Use them. Distrust them. Build your own.

## Further reading

**Must-read**
- Anthropic, *Building Effective Agents* (Dec 2024)[^1]
- Yao et al., *ReAct: Synergizing Reasoning and Acting in Language Models* (2022)[^2]
- Yao et al., *τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains* (arXiv 2406.12045)[^14]

**Recommended**
- Husain, *Using LLM-as-a-Judge for Evaluation: A Complete Guide* (Oct 2024)[^4]
- BFCL leaderboard and methodology[^13]
- Cognition, *SWE-bench Technical Report*[^3]
- LangChain, *Memory for agents*[^12]

**Optional**
- Sierra, τ²-bench repository for reproduction[^8]
- SWE-bench Pro paper (arXiv 2509.16941)[^7]
- Gemini 3.1 Pro model card[^11]
- Current model lineup (mid-2026): Anthropic Fable 5 / Mythos 5 and Sonnet 5[^15]; and METR's living time-horizon chart (metr.org/time-horizons) as the source that survives model churn

## Citations

[^1]: Anthropic, "Building Effective Agents," research post, December 20, 2024. https://www.anthropic.com/research/building-effective-agents

[^2]: Yao, S. et al., "ReAct: Synergizing Reasoning and Acting in Language Models," arXiv:2210.03629, October 2022, ICLR 2023. https://arxiv.org/abs/2210.03629

[^3]: Cognition Labs, "SWE-bench technical report," 2024. https://cognition.ai/blog/swe-bench-technical-report

[^4]: Husain, H., "Using LLM-as-a-Judge For Evaluation: A Complete Guide," October 29, 2024. https://hamel.dev/blog/posts/llm-judge/

[^5]: Ronacher, A., "What Actually Is Claude Code's Plan Mode?", December 17, 2025. https://lucumr.pocoo.org/2025/12/17/what-is-plan-mode/ — and Anthropic Claude Code docs, "Plan mode," https://claudelog.com/mechanics/plan-mode/

[^6]: Anthropic, "Introducing Claude Opus 4.5," November 2025. https://www.anthropic.com/news/claude-opus-4-5

[^7]: Chen et al., "SWE-Bench Pro: Can AI Agents Solve Long-Horizon Software Engineering Tasks?", arXiv:2509.16941, updated November 2025. https://arxiv.org/pdf/2509.16941

[^8]: Sierra Research, "τ²-Bench: Evaluating Conversational Agents in a Dual-Control Environment," arXiv:2506.07982, 2025. https://github.com/sierra-research/tau2-bench — and Claude Opus 4.6 benchmarks, Vellum AI. https://www.vellum.ai/blog/claude-opus-4-6-benchmarks

[^9]: OpenAI, "Introducing GPT-5," August 2025. https://openai.com/index/introducing-gpt-5/

[^10]: Honda, S., "Benchmarking AI Agents: Stop Trusting Headline Scores, Start Measuring Trade-offs," Alan engineering blog, 2025. https://medium.com/alan/benchmarking-ai-agents-stop-trusting-headline-scores-start-measuring-trade-offs-0fdae3a418cf

[^11]: Google DeepMind, "Gemini 3.1 Pro Model Card," November 2025. https://deepmind.google/models/model-cards/gemini-3-1-pro/

[^12]: LangChain, "Memory for agents," blog, 2024-2025. https://blog.langchain.com/memory-for-agents/ — and LangChain memory overview, https://docs.langchain.com/oss/python/concepts/memory

[^13]: Patil, S. et al., "The Berkeley Function Calling Leaderboard (BFCL): From Tool Use to Agentic Evaluation of Large Language Models," OpenReview, 2025. https://openreview.net/forum?id=2GmDdhBdDk — leaderboard at https://gorilla.cs.berkeley.edu/leaderboard.html

[^14]: Yao, S. et al., "τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains," arXiv:2406.12045, June 2024. https://arxiv.org/abs/2406.12045

[^15]: Anthropic (Jun 2026). *Introducing Claude Fable 5 and Mythos 5.* https://www.anthropic.com/news/claude-fable-5-mythos-5 — new Mythos-class tier above Opus, $10/$50 per Mtok, 1M-token default context. *Introducing Claude Sonnet 5* (Jun 30 2026), https://www.anthropic.com/news/claude-sonnet-5 — new default agent tier, intro pricing $2/$10 through 2026-08-31 then $3/$15. Cited to mark the current lineup against which the Opus-4.5/4.6/GPT-5/Gemini-3.1 benchmark numbers in this lesson are historical.

_last_verified: 2026-07-17_
