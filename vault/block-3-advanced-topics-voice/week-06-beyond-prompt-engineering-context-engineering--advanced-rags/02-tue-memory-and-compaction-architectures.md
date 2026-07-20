---
type: lesson
block: block-3-advanced-topics-voice
week: week-06
day_of_cycle: 2
day_name: tue
session_slug: beyond-prompt-engineering-context-engineering
date_due: 2026-06-23
tags: [memory, compaction, structured-notes, sub-agents, context-isolation, claude-memory-tool, context-editing, mem0, letta, chatgpt-memory, simon-willison, context-collapse]
sources:
  - anthropic-context-management-2025
  - anthropic-memory-tool-docs
  - anthropic-effective-context-engineering-2025
  - anthropic-multi-agent-research-2025
  - simonwillison-memory-dossier-2025
  - mem0-benchmarks-2026
  - letta-memgpt
  - claude-code-compaction-internals
  - axios-chatgpt-memory-2025
last_verified: 2026-07-17
word_count_target: 5500
---

# Memory and compaction architectures — keeping an agent coherent past its window

## Why this matters

Monday established the budget. Today is about what happens when a real workload exceeds it, which every long-horizon agent does: a multi-hour Claude Code refactor, a support agent on its 40th turn, a research agent that has read 60 pages. You have exactly four families of tools for surviving past the window — **compaction** (summarize and restart), **structured note-taking** (write durable state outside the window), **sub-agent isolation** (spend other windows and keep the distillate), and **memory systems** (persist knowledge across sessions). Every agent framework, every vendor memory feature, and every "our agent has long-term memory" pitch you will ever evaluate is a packaging of these four. Learn the primitives and vendor marketing decompresses into architecture. You will also learn the failure mode the pitches omit: memory that contaminates, injecting stale or cross-context facts into places they don't belong — the reason Simon Willison, one of the field's most credible practitioners, turned the flagship consumer memory feature *off*.[^5]

## Prerequisites

- [[01-mon-context-engineering-the-successor-discipline|Monday's lesson]] — attention budget, context rot, just-in-time context.
- [[03-wed-claude-md-memory-architecture|CLAUDE.md as memory architecture]] from Block 0 Week 0. CLAUDE.md is the file-based memory pattern you already use daily; today generalizes it. One-line recap only: a markdown file auto-loaded into every session, holding durable project knowledge. Not re-taught here.
- [[02-tue-agent-architectures|Agent architectures]] from Block 2 Week 4 — orchestrator/worker vocabulary.

## Layer 1 — Compaction: the art of losing the right information

Compaction is the fallback when a conversation must outlive its window: summarize the history, reinitialize with the summary plus the most recent turns, continue.[^1] It sounds trivial. It is not, because compaction is a *lossy* operation and the loss function is a design decision.

Claude Code's production pipeline is the best-documented example, and its internals (reconstructed by practitioners from the shipped code, so treat the exact thresholds as indicative rather than contractual) show four escalating stages, ordered by a clear philosophy — avoid LLM calls until you must:[^2]

1. **Snip** — drop whole messages that are provably safe to drop.
2. **Microcompact** — replace the *content* of old tool results with a cleared-content marker while keeping the call structure intact; targets recomputable results (file reads, greps, web fetches). Cheap, no LLM call, and it removes exactly the tokens with the worst decay profile: stale tool output.
3. **Context collapse** — LLM-summarize selected segments.
4. **Autocompact** — LLM-summarize the whole history when the token count crosses a threshold that reserves headroom for the summary itself.

The design lessons generalize to any agent you build:

- **Tool results decay fastest.** A file read from 50 turns ago is almost pure noise — the file may have changed, and if the agent needs it again it can re-read it. Anthropic's context-editing feature productizes exactly this insight at the API level: automatically clear stale tool calls/results as you approach limits. Their internal 100-turn web-search evaluation reports an 84% token reduction from context editing, and a 29% task-improvement from context editing alone.[^1]
- **What you keep needs a contract.** A good compaction summary preserves: architectural decisions and their reasons, unresolved bugs, current plan state, and explicit user instructions. It drops: raw outputs, dead ends already marked dead, and pleasantries. Anthropic's advice is to tune compaction prompts on real traces, first maximizing recall of critical information, then improving precision by cutting redundancy.[^1][^3]
- **Compaction compounds.** A summary of summaries loses second-order information. If your agent routinely triple-compacts, your architecture is wrong; you need notes or sub-agents, not better summaries.

The operator failure story you should carry (a composite of the pattern, labeled as such): an agent five compactions deep "remembers" that the deploy failed but not *why*, retries the same broken approach, and burns an afternoon. That is the recall/precision contract violated, and no window size fixes it.

## Layer 2 — Structured note-taking: NOTES.md and the to-do list as memory

The second primitive costs almost nothing and is chronically underused: the agent *writes its own state to durable storage outside the window* — a NOTES.md, a to-do list, a scratchpad file — and re-reads it after compaction or restart.[^3] Claude Code's built-in to-do list, the agent diaries you see in long-horizon demos (Anthropic's essay uses Claude playing Pokémon, tallying progress across thousands of steps), and every "plan file" pattern in agentic coding are this primitive.

Why it beats compaction where it applies: the *agent* decides at write time what is worth remembering, in a structured form it can parse later, instead of a summarizer deciding at compaction time under token pressure. Notes have three properties compaction summaries lack: they are incremental (updated as facts arrive, not reconstructed under duress), inspectable (you can read and correct them), and selective (a to-do list is a few hundred tokens, a summary is thousands).

Anthropic shipped this primitive as an API feature in fall 2025: the **memory tool** (public beta September 29, 2025) gives Claude file operations — create, read, update, delete — against a memory directory that *your application* stores and persists across conversations; it is entirely client-side, so you control storage, and it pairs with context editing so cleared tool results can be recovered from notes if needed. Combined memory-plus-context-editing improved Anthropic's internal agentic-search evals by 39% over baseline.[^1][^4]

Design rules for notes that work:

- **Schema beats prose.** `## Decisions`, `## Open questions`, `## Done`, `## Next` — a predictable structure the agent (and you) can scan. Freeform diaries rot into the same noise you were escaping.
- **Notes are context too.** A 30K-token NOTES.md re-loaded every session is just a slow-motion context bomb. Notes need their own compaction policy (archive completed sections; cap size).
- **Write triggers, not vibes.** Instruct the agent *when* to write: after each completed sub-task, before each risky operation, on each decision. "Take notes as useful" produces either graphomania or silence.

The connection back to Block 0: CLAUDE.md is the *human-curated* end of this spectrum; the memory tool is the *agent-curated* end. Production systems need both, and the failure modes differ — humans under-update, agents over-write.

## Layer 3 — Sub-agent isolation: spend someone else's window

The third primitive: when a sub-task needs deep exploration, spawn a sub-agent with a *clean context window*, let it burn tens of thousands of tokens searching, and return only a distilled summary to the orchestrator.[^3] The parent's budget is charged only for the distillate. This is context isolation as architecture: specialized workers with focused windows, coordinated by a lead that holds the plan.

The canonical public data point is Anthropic's multi-agent research system (June 2025 engineering post): a lead agent (then Opus 4) plans and spawns parallel search sub-agents (then Sonnet 4); the multi-agent system beat a single-agent Opus 4 baseline by 90.2% on their internal research eval. Two numbers from the same post keep the enthusiasm honest: token usage explains most of the performance variance (about 80% in their BrowseComp analysis), and the architecture burns roughly **15× the tokens of a normal chat**.[^6] Sub-agents are not efficiency tools; they are *quality* tools that buy fresh attention budgets with money.

When isolation pays, per the same post: breadth-first tasks decomposable into parallel, independent explorations (research, due diligence, competitive scans) that exceed one window. When it does not: tightly-coupled tasks where every worker needs the full shared state — Anthropic explicitly names coding and debugging as poor fits for parallel multi-agent today, and most agentic workflows fail the independence test.[^6] The sub-agent boundary is also a *communication* cost: everything the worker learned but didn't write into its summary is lost. Bad distillation prompts turn a $5 sub-agent run into a two-line answer that forces the orchestrator to re-do the work.

Rule of thumb: one window per *concern*, not per *step*. If two steps must share fine-grained state, they belong in one window.

## Layer 4 — Memory across sessions: the vendor landscape, mid-2026

Cross-session memory is where the four primitives meet product marketing, so here is the landscape stripped to architecture. All fast-moving facts below were search-verified this week.

**Anthropic (Claude).** The memory tool (Layer 2) is the developer surface: file-based, client-side, no server-side retention by Anthropic; your infrastructure, your retention policy.[^4] For consumers, Claude's project-scoped memory keeps recall bounded by project. The design bet: memory as *legible files* the developer and user can inspect and edit.

**OpenAI (ChatGPT).** Memory rolled out across Free, Plus, and Pro tiers through 2025, combining saved memories with implicit reference to chat history; it is on by default and largely automatic.[^7] The design bet: memory as an *invisible dossier* that makes the product stickier. That bet is exactly what the contamination critique targets (Layer 5).

**Open frameworks.** Two names matter most in mid-2026, both real, maintained, and benchmarked: **Mem0** (extraction-based: an LLM distills salient facts from conversations into a store, retrieved by relevance; reported 92.5% on LoCoMo and 94.4% on LongMemEval in its May 2026 update, at under 7K tokens per retrieval call versus 25K+ for full-context stuffing — vendor-reported, on a benchmark the vendor co-promotes, so discount accordingly) and **Letta** (the productized MemGPT lineage: the LLM-as-operating-system pattern, with main context as RAM and recall/archival stores the model pages in and out via function calls).[^8] Zep and others compete on temporal knowledge graphs. LoCoMo (long multi-session conversation QA) is the most-cited benchmark of the space; it is small (81 QA pairs in its core set) and gameable, so treat leaderboard deltas as directional.[^8]

The architectural takeaway: every one of these is retrieval plus write-policy. "Memory system" = (what gets written, when) × (what gets retrieved, when) × (where it lands in the window). Evaluate them with the same eval discipline as any retriever — which is Friday's lesson.

## Layer 5 — Live controversy: memory as moat vs memory as contamination

**The moat position** is the default in product strategy discourse: memory compounds switching costs; the assistant that knows your preferences, your codebase, your writing voice is the assistant you can't leave. OpenAI's default-on rollout, Anthropic's memory tooling, and the funded memory-startup cohort (Mem0, Letta, Zep) all express it. On this view memory is *the* consumer AI lock-in of the late 2020s.

**The contamination position** got its canonical text on May 21, 2025: Simon Willison, *"I really don't like ChatGPT's new memory dossier."*[^5] His argument is not privacy hand-waving; it is an engineering claim in three parts. First, **loss of context control**: he wants to know exactly what is in the window so he can predict model behavior; an invisible dossier makes every response a function of hidden state. Second, **staleness with no invalidation**: memory mixes outdated facts with current ones and has no mechanism to detect that circumstances changed — his generated self-portrait wore a wedding ring he no longer wears; his dog got a "Half Moon Bay" sign because he'd mentioned the town before. Third, what researchers call **context collapse**: data from separate spheres of life (work, family, clients) bleeds into a single profile, so a work query gets colored by personal history.[^5] For professionals, add a fourth: client A's context leaking into client B's output is not a quirk, it is a confidentiality incident.

**My position.** Both are right about different products, and the variable is *legibility*. Memory implemented as inspectable, editable, scoped artifacts (CLAUDE.md, memory-tool files, per-project stores) captures most of the compounding value while staying debuggable — when output goes weird you can open the file and see why. Memory implemented as an invisible, unscoped, default-on dossier maximizes short-term stickiness and accumulates exactly the failure modes Willison documents, plus a new attack surface (a poisoned memory persists across every future session — recall the injection taxonomy from [[03-wed-mcp-security|Block 0's MCP security week]]). For anything you build for clients: memory must be scoped per client, inspectable on demand, and erasable on request; the EU AI Act's full applicability arriving August 2, 2026 makes the erasable part more than good manners. The moat framing also has a quieter problem: a moat made of hidden state is a moat made of unreproducible behavior, and unreproducible behavior is what kills enterprise deals.

## Worked example / runnable experiment — build and then contaminate a memory

Claude Code orchestration, 60–90 minutes, on your Week-4 RAG project.

**Phase 1 — notes discipline.** Start a session and paste:

> For this session, maintain a file AGENT_NOTES.md with sections: Decisions, Open questions, Done, Next. Update it after every completed sub-task, before any risky operation, and whenever I overrule you. Keep it under 150 lines; archive overflow to AGENT_NOTES_ARCHIVE.md.

Then do 30–45 minutes of real work on the project (add a feature, fix a bug). Watch when it writes, and correct it when it writes prose instead of state.

**Phase 2 — survive a compaction.** When the session has real history, run `/compact`, then immediately ask: "Without re-reading any code, what is our current plan, what have we decided and why, and what's blocked?" Grade the answer against AGENT_NOTES.md. The delta between what compaction kept and what the notes kept is Layer 1 vs Layer 2, on your own data.

**Phase 3 — contaminate.** Plant a stale fact in the notes ("Decision: we use SQLite for the eval store" after you have switched to Postgres in Phase 1, or similar). Start a *fresh* session, let it load the notes, and give it a task that touches the decision. Observe how confidently the stale memory propagates, and how far downstream it gets before anything challenges it. Then write the one-line invalidation rule you'd add to the notes schema to prevent it (e.g., every Decision line carries a date and a "verify against: <file>" pointer). This is Willison's wedding-ring failure, reproduced in your own stack for free.

## Cross-domain examples — memory decisions your clients will actually face

- *Customer-support agent, 200 tickets/day.* The temptation is a per-customer memory ("remembers you!"). The engineering reality: per-customer stores are mostly empty, per-*product* memory (known issues, resolution patterns, vocabulary) is dense and compounds. Start with one shared, curated product memory and per-conversation notes; add per-customer memory only when repeat-contact rates justify it. The metric that decides: fraction of tickets from repeat contacts within memory's retention window.
- *Agency running agents for five clients.* One memory store is a confidentiality incident on a timer; five stores with one schema is the answer, and the schema itself becomes reusable IP. The sales artifact: show a client *their* memory file in a review meeting. Legibility converts to trust, and trust converts to renewals.
- *Solo consultant's research assistant.* The dossier problem in miniature: your assistant remembers a position you have since reversed and keeps arguing it back at you. The fix costs one convention: decisions in notes carry dates, and the standing instruction says prefer recent over stored when they conflict.
- *Voice agent (preview of Week 7).* Compaction budgets meet latency budgets: you cannot pause a phone call to summarize. Voice memory must be *pre-computed between calls*, not managed during them, which is why the primitives today (notes written after runs, memory read before runs) matter more for voice than the in-flight techniques.

## Problem set

1. **The compaction prompt.** Write the actual compaction instruction for your Week-4 agent: what must be preserved verbatim, what summarized, what dropped. Then test it: run a long session, compact with your instruction, and ask five state questions whose answers you know. Score recall. Pass: 4/5 with the instruction, and a documented failure case. Fail: an untested prompt.
2. **The notes schema.** Design AGENT_NOTES.md sections and write-triggers for a *specific* agent you run (not the generic template from the experiment). Include the size cap, the archive rule, and the invalidation convention. Run it for one real work session and attach the resulting file.
3. **Sub-agent contract (design).** For a due-diligence task ("assess this vendor's security posture from these 40 documents"), write the orchestrator's dispatch prompt for one sub-agent: scope, tool grants, token budget, and the exact structure of the summary it must return. Defend the budget number using the 15× economics.[^6]
4. **The contamination red-team.** Extend the Phase-3 experiment: plant three stale facts of increasing subtlety (an obvious one, a plausible one, one entangled with a true fact). Measure how far each propagates before detection. Write the invalidation rule that catches the *worst* one, and note what it costs in write-time discipline.
5. **Build-vs-buy memo, 300 words.** For your own stack: memory tool + files vs Mem0 vs Letta vs nothing-but-CLAUDE.md. Pick one. Defend with (a) your actual repeat-traffic profile, (b) the legibility requirement from the controversy section, (c) switching cost if you are wrong. Vendor benchmark numbers may be cited only with their task distribution named.[^8]

## Common mistakes experts see

- **Memory as a dumping ground.** Writing everything means retrieving noise. A memory without a curation policy is a landfill with an API.
- **No invalidation story.** Facts change. Any memory design that cannot mark, date, or expire an entry will eventually inject a confident lie.
- **Compacting instead of architecting.** Repeated compaction in every run is a smell: the task wants notes or sub-agent decomposition, not a better summarizer.
- **Sub-agents for coupled work.** Parallel workers on a tightly-shared-state problem (a refactor, a debug) spend their savings on coordination failures.[^6]
- **Skipping the distillation contract.** A sub-agent without explicit instructions on what its summary must contain returns either everything or nothing.
- **Cross-scope memory in client work.** One memory store across clients is a confidentiality incident on a timer.
- **Trusting vendor memory benchmarks at face value.** LoCoMo is small and vendors report their own scores.[^8] Run your own traces before you pick a framework.

## Reflection questions

1. Write the loss function of a compaction summary for *your* Week-4 agent: three things it must never drop, three things it should always drop, and the one item you're unsure about.
2. Anthropic's 15× token multiplier for multi-agent research is a price. Describe a client engagement where paying it is obviously right, one where it's obviously wrong, and the metric that separates them.[^6]
3. Willison's three complaints (control, staleness, collapse) — rank them by severity *for an agency running agents for multiple clients*, and defend the ranking.
4. Your agent's NOTES.md has grown to 40K tokens over two months. Design its compaction policy without losing the property that made notes better than summaries in the first place.
5. Mem0-style extraction memory vs Letta-style paging memory: which failure mode does each buy, and which matches a customer-support agent that handles 200 tickets/day?
6. A memory entry is itself a prompt-injection payload with persistence. Sketch the attack, then the two cheapest mitigations.

## My take (reviewer lens)

**Simon Willison** would endorse the contamination layer (it's his argument) but would push the lesson to go further on *injection*: a persistent memory written by model output is untrusted content that gets re-trusted every session, and the lesson gives that one reflection question when it deserves a full threat model; he'd also insist the "moat" framing name the incentive problem — vendors profit from illegible memory, users pay for it in debuggability. **Lilian Weng** would flag that the four-primitive taxonomy is tidy but the research frontier is messier: memory-in-the-loop retrieval as working memory, learned write policies, and reflection-based memory (her own agent-survey lineage) blur the compaction/notes boundary, and a lesson this operational should at least gesture at where the primitives are converging. **A cohort peer** would make the practical complaint: the lesson names five vendor/framework options and picks none. Fair; the pick, for this course's stack, is boring and deliberate — CLAUDE.md plus the memory tool plus per-project files, because legibility beats benchmark deltas at our scale, and Saturday's build acts on exactly that choice.

## Further reading

**Must-read**
- Anthropic, *Managing context on the Claude Developer Platform* (Sep 2025) — context editing + memory tool, with the 39%/84%/29% eval numbers.[^1]
- Simon Willison, *I really don't like ChatGPT's new memory dossier* (May 21, 2025).[^5] The contamination case, from a builder.
- Anthropic Engineering, *How we built our multi-agent research system* (Jun 2025).[^6] The 90.2%/15× tradeoff, stated plainly by the people who paid it.

**Recommended**
- Memory tool docs (platform.claude.com).[^4] Read the tool-operation loop before Saturday.
- Anthropic's context-engineering essay, compaction + note-taking sections.[^3]
- Claude Code compaction internals write-ups.[^2] Reverse-engineered, so hold loosely, but the stage ordering is instructive.

**Optional**
- Mem0's 2026 benchmark posts and the LoCoMo paper — read as vendor claims with methodology attached.[^8]
- Axios on ChatGPT memory's rollout across tiers.[^7]

## Citations

[^1]: Anthropic, *Managing context on the Claude Developer Platform*, claude.com/blog, September 2025. Context editing (auto-clearing stale tool calls/results); memory tool beta; internal evals: +39% agentic search (memory + context editing), +29% (context editing alone), 84% token reduction in 100-turn web-search eval. https://claude.com/blog/context-management (search-verified 2026-07-17 across two queries; corroborated by joshuaberkowitz.us and thomas-wiegold.com summaries; fetch egress-blocked — liveness pass pending)

[^2]: Practitioner reconstructions of Claude Code's compaction pipeline (snip → microcompact → context collapse → autocompact; microcompact clears recomputable tool-result content, e.g. "[Old tool result content cleared]"): https://decodeclaude.com/compaction-deep-dive/ ; https://oldeucryptoboi.com/blog/context-compaction-deep-dive/ ; official surface: https://code.claude.com/docs/en/context-window (search-verified 2026-07-17; internals are reverse-engineered — treat thresholds as indicative; fetch egress-blocked — liveness pass pending)

[^3]: Anthropic Engineering, *Effective context engineering for AI agents*, September 29, 2025 — compaction, structured note-taking (incl. the Pokémon tally example), sub-agent architectures sections. https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^4]: Anthropic, *Memory tool*, Claude Platform Docs. Client-side file-based memory: Claude requests file operations, your application executes and stores; beta since 2025-09-29. https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool (search-verified 2026-07-17; corroborated by leoniemonigatti.com and apito.ai walkthroughs; fetch egress-blocked — liveness pass pending)

[^5]: Simon Willison, *I really don't like ChatGPT's new memory dossier*, simonwillison.net, May 21, 2025. Context control, staleness (wedding-ring and Half Moon Bay examples), context collapse. https://simonwillison.net/2025/May/21/chatgpt-new-memory/ (search-verified 2026-07-17)

[^6]: Anthropic Engineering, *How we built our multi-agent research system*, June 2025. Multi-agent (Opus 4 lead + Sonnet 4 subagents) outperformed single-agent Opus 4 by 90.2% on internal research eval; token usage explains ~80% of BrowseComp variance; ~15× tokens vs chat; breadth-first fit, coding poor fit. https://www.anthropic.com/engineering/multi-agent-research-system (search-verified 2026-07-17; corroborated by bytebytego.com and zenml.io summaries; fetch egress-blocked — liveness pass pending)

[^7]: Axios, *ChatGPT has memory on its free, Pro and Plus versions*, July 11, 2025. https://www.axios.com/2025/07/11/chatgpt-memory-update (search-verified 2026-07-17)

[^8]: Mem0 reported results (May 2026 algorithm update): 92.5% LoCoMo, 94.4% LongMemEval, <7K tokens/retrieval; largest gains temporal (+29.6) and multi-hop (+23.1). https://mem0.ai/blog/ai-memory-benchmarks-in-2026 ; https://mem0.ai/blog/state-of-ai-agent-memory-2026 ; independent comparisons: https://www.innobu.com/en/articles/agent-memory-2026-mem0-letta-zep-hermes-openclaude-comparison.html ; Letta/MemGPT OS-style paging: https://blog.devgenius.io/ai-agent-memory-systems-in-2026-mem0-zep-hindsight-memvid-and-everything-in-between-compared-96e35b818da8 (search-verified 2026-07-17; vendor-reported figures flagged as such; fetch egress-blocked — liveness pass pending)

_last_verified: 2026-07-17_
