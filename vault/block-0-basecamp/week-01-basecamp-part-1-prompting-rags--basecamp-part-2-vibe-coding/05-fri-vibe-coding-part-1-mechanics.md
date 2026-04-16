---
type: lesson
block: block-0-basecamp
week: week-01
day_of_cycle: 5
day_name: fri
session_slug: basecamp-part-2-vibe-coding
date_due: 2026-05-01
tags: [vibe-coding, agentic-loop, claude-code, tool-use, ReAct, subagents, SWE-bench, CLAUDE.md, operator-framing]
sources:
  - karpathy-2025-vibe-coding-tweet
  - anthropic-claude-code-how-it-works
  - anthropic-tool-use-how-it-works
  - anthropic-building-effective-agents
  - anthropic-claude-opus-4-5-release
  - anthropic-claude-sonnet-4-5-release
  - yao-2022-react-paper
  - simon-willison-vibe-engineering
  - piebald-claude-code-system-prompts
  - alexop-claude-code-full-stack
last_verified: 2026-04-15
word_count_target: 6500
---

# Vibe coding, the agentic loop, and what Claude Code is actually doing under the hood

## Why this matters

The phrase "vibe coding" went viral. It has since been used to describe everything from a weekend prototype to a VC-funded startup's entire engineering strategy. Almost every use is wrong — wrong about what Karpathy actually said, wrong about the constraint, wrong about which part is dangerous and which part is genuinely new.

This lesson gives you the mechanical model that separates the signal from the noise. Not because you need to defend a position at a dinner party, but because you are probably already vibe coding — directing Claude Code to scaffold a tool, build an internal workflow, prototype a client app — and your ability to design more ambitious systems depends on understanding what is happening at each step of the loop.

By the end of today:

1. You will know exactly what Karpathy said and what he was hedging — and be able to apply his hedge as a design test for any system you are about to build.
2. You will have a mechanical model of the agentic loop at the level Claude Code runs it: observe → plan → act → observe result → iterate, with the context window as the scratchpad.
3. You will understand what Claude Code's tool definitions actually do, how the model decides when to invoke them, and how results flow back into the conversation.
4. You will know when to use subagent parallelism, when it breaks, and what the Task tool costs you in terms of context isolation.
5. You will have a tested mental model of CLAUDE.md, hooks, slash commands, and MCP as control surfaces — not features to toggle, but leverage points in the loop.
6. You will have read and formed a position on the live controversy: when is vibe coding a legitimate building strategy, and when is it irresponsible?

## Prerequisites

- Claude Code installed (any recent version — v2.x or later). Active Claude Max subscription.
- You have run at least one multi-step Claude Code task before. You know what the tool output stream looks like.
- Optional but useful: Monday's lesson on prompting first principles. The mechanics of the agentic loop extend directly from the context-window-as-computation model you built there.

---

## 1. What Karpathy actually said — and what the hedge means

On February 2, 2025, Andrej Karpathy posted this to X:[^1]

> "There's a new kind of coding I call 'vibe coding', where you fully give in to the vibes, embrace exponentials, and forget that the code even exists. It's possible because the LLMs (e.g. Cursor Composer w Sonnet) are getting too good. Also I just talk to Composer with SuperWhisper so I barely even touch the keyboard. I ask for the dumbest things like 'decrease the padding on the sidebar by half' because I'm too lazy to find it. I 'Accept All' always, I don't read the diffs anymore. When I get error messages I just copy paste them in with no comment, usually that fixes it. The code grows beyond my usual comprehension, I'd have to really read through it for a while. Sometimes the LLMs can't fix a bug so I just work around it or ask for random changes until it goes away. It's not too bad for throwaway weekend projects, but still quite amusing. I'm building a project or webapp, but it's not really coding - I just see stuff, say stuff, run stuff, and copy paste stuff, and it mostly works."

The post received over 4.5 million views. The phrase "vibe coding" became a movement. Most people who adopted the term missed the seven-word hedge buried near the end: *"not too bad for throwaway weekend projects."*

Read that hedge as a precise technical specification, not a caveat. Karpathy was describing a workflow that is appropriate for a specific context: throwaway, weekend, projects. All three words matter.

**Throwaway** means no users. No one's data is at risk. No one's workflow breaks if the app fails. The cost of a mistake is losing a few hours, not a data breach or a broken internal tool that a finance team depends on.

**Weekend** means narrow scope and bounded time. A weekend project is a prototype of one feature, not a production system. It will be rewritten or discarded. The maintenance burden is zero by design.

**Projects** — plural — suggests variety. He was describing rapid exploration: try many things, keep what works, throw out the rest. This is exploration mode, not exploitation mode.

The viral meme reframed this as "the future of software development." That is not what Karpathy wrote. He described a specific mode of building that is genuinely powerful within its domain. He also told you the domain boundary.

A second, less-quoted Karpathy post from a few days later reinforced this. When asked about applying vibe coding to production systems, he declined to endorse it. The original tweet was a personal experiment report, not a manifesto.[^1b]

The question this lesson is actually answering: given that Karpathy's framing is correct, what are the conditions under which you can responsibly extend vibe-coding-adjacent workflows to things that aren't throwaway weekend projects? That requires understanding the mechanism.

---

## 2. The agentic loop, mechanically

Before Claude Code, before Cursor, before any specific product: the conceptual machinery.

In October 2022, Shunyu Yao and colleagues at Princeton and Google published *ReAct: Synergizing Reasoning and Acting in Language Models.*[^2] The core idea was simple and has since powered every major agentic system you have used: interleave language model reasoning traces with tool actions in a single loop.

The ReAct loop, abstractly:

```
Thought: [model reasons about what to do next]
Action: [model invokes a tool]
Observation: [tool result is returned]
Thought: [model reasons about the result]
Action: [model invokes next tool, or decides it's done]
...
```

On HotpotQA (multi-hop question answering) and Fever (fact verification), ReAct agents substantially outperformed pure chain-of-thought reasoning by catching and correcting their own errors mid-loop — the tool call gave them ground truth to reason against, rather than hallucinating forward. On ALFWorld and WebShop (interactive decision making), ReAct outperformed imitation and reinforcement learning baselines by 34% and 10% respectively, using only one or two in-context examples.[^2]

That 2022 paper is the conceptual ancestor of every agent harness running today. Claude Code, Cursor, Codex Agents, OpenHands, SWE-agent — all of them are industrialized ReAct loops with better tooling, more reliable execution, and a lot of engineering to handle the edge cases Yao's paper left as exercises.

### The context window as scratchpad

Here is the mechanical fact that everything else follows from: *the context window is the agent's entire working memory.*

There is no persistent state between individual model calls. Each call to the Claude API takes a sequence of messages (the conversation history, including all previous tool calls and their results) and returns the next response. The "loop" exists in your harness — in Claude Code's orchestration layer — not inside the model. The model sees a snapshot. Your harness manages the append.

This has concrete consequences for how you use Claude Code:

- **Every tool result grows the context.** Each Bash execution, each file read, each Grep result is appended as a message. On a long session working across a large codebase, context fills fast.
- **The model's "plan" is just text in the context.** When Claude Code says "I'll first read the schema, then generate the validation logic, then write the tests," that plan exists as tokens in the running context. It can be abandoned, revised, or forgotten if context pressure causes auto-compaction to drop it.
- **CLAUDE.md is how you anchor persistent state.** Because each new session starts fresh, anything the model needs to remember across sessions — your project conventions, preferred libraries, known constraints — lives in CLAUDE.md. It loads at the start of every session.[^3]

The Anthropic Claude Code docs describe this as: "Your conversation history, file contents, command outputs, CLAUDE.md, auto memory, loaded skills, and system instructions" all live in the context window. When context fills up, Claude Code clears older tool outputs first, then summarizes. Instructions from early in the conversation are the first things at risk.[^3]

Practical design implication: if you start a long Claude Code session with an important constraint ("don't modify the production database schema"), say it in CLAUDE.md, not just in your first message. The first message will compress away. CLAUDE.md persists.

### The three phases Claude Code describes

The official documentation names three phases: gather context, take action, verify results.[^3] These aren't sequential stages that each happen once — they interleave continuously. A concrete trace for a data-pipeline task:

1. **Gather:** Read the existing ETL script. Grep for the schema definition. Read the upstream data source spec.
2. **Act:** Write a new validation function.
3. **Verify:** Run the test suite.
4. **Gather:** Read the test failure output.
5. **Act:** Fix the validation logic.
6. **Verify:** Run the suite again.
7. Act, verify, repeat until tests pass or until Claude Code hits an impasse and surfaces the question to you.

The loop is driven by a `while (stop_reason == "tool_use")` condition in the harness. The model emits a tool call; the harness executes it; the result comes back as a new message; the model sees the updated context and decides what to do next. The loop exits when the model emits a final response without a tool call — `stop_reason: "end_turn"` — or when you interrupt it.[^4]

---

## 3. Tool use under the hood — what actually happens when Claude Code calls Bash

Claude Code's built-in tools fall into five categories:[^3]

| Category | Tools | What they do |
|---|---|---|
| File operations | Read, Write, Edit, MultiEdit | Read files, create files, apply targeted diffs |
| Search | Glob, Grep | Find files by pattern, search content by regex |
| Execution | Bash | Run any shell command with your permissions |
| Web | WebSearch, WebFetch | Search the web, fetch a URL |
| Orchestration | Task, AskUser | Spawn subagents, ask you a question |

The mechanism by which Claude Code decides when to call `Bash` vs `Read` vs `Grep` is not a rule engine or a decision tree. It is the language model reading the tool descriptions in its context and predicting, given the current conversation state, which tool call token sequence maximizes the quality of the next action. This is important to internalize: the model is not following a program. It is pattern-completing, guided by the tool schemas and by the system prompt.

### JSON schema tool definitions

Every tool Claude Code can call is defined as a JSON schema in the system prompt. The schema specifies:

- The tool's name (what the model must emit to invoke it)
- A natural-language description (what the tool does, when to use it)
- An `input_schema` (the parameters the model must provide, with types and descriptions)
- Which parameters are required

When Anthropic constructs Claude Code's system prompt, it includes approximately 24 built-in tool schemas that together consume 14–17K tokens of context.[^5] Those tokens are not wasted: they are the interface contract the model reads in order to know how to act.

When Claude Code decides to read a file, the model emits something like:

```json
{
  "type": "tool_use",
  "id": "toolu_01XyzAbc",
  "name": "Read",
  "input": {
    "file_path": "/path/to/your/file.py",
    "offset": 0,
    "limit": 200
  }
}
```

The harness extracts this, executes the file read, and returns the result as a `tool_result` message:

```json
{
  "type": "tool_result",
  "tool_use_id": "toolu_01XyzAbc",
  "content": "<file contents here>"
}
```

That tool result is appended to the conversation history and the model sees it on the next call. This is how tool results get injected back into context: they become new messages in the running conversation, indistinguishable in format from any other message, and the model reasons about them accordingly.[^4]

The Anthropic docs describe the contract precisely: "Tool use is a contract between your application and the model. You specify what operations are available and what shape their inputs and outputs take; Claude decides when and how to call them. The model never executes anything on its own."[^4] The model emits a structured request. Your harness (or Anthropic's server, for server-executed tools) runs the operation. The result flows back as a message.

### Why the model calls tools reliably — and why it sometimes doesn't

The Anthropic-schema tools (Bash, the text editor tools used internally, computer control) are *trained-in*. Claude has been optimized on thousands of successful trajectories that use these exact tool signatures. This is why Claude Code calls `Bash` with the right flag combinations and handles errors gracefully — the model has seen and learned from millions of tool-call cycles using these specific schemas.[^4]

When you add a custom MCP tool with a poorly written description, the model is working without that trained-in advantage. It knows the schema format but hasn't seen thousands of successful invocations of your specific tool. This is the main reason MCP tool description quality matters so much: your description is doing load-bearing work in place of the trained-in pattern.

---

## 4. Claude Code's specific anatomy — what you are actually working with

### The system prompt

Claude Code's system prompt at session start is approximately 2.5K tokens of instructions plus 14–17K tokens of tool definitions.[^5] The Piebald-AI GitHub project has reverse-engineered and published all parts of Claude Code's system prompt for every version, including sub-agent prompts (Plan, Explore, Task) and utility prompts.[^5]

The system prompt instructs the model to:
- Work autonomously and use tools to gather context before acting
- Prefer targeted edits over full-file rewrites
- Ask you questions rather than guess when ambiguous
- Be explicit about risks before taking destructive actions (dropping tables, deleting files)
- Use CLAUDE.md as the authoritative source of project-specific constraints

You cannot read the full system prompt during a session, but you can effectively extend it in two ways: CLAUDE.md (which gets loaded at session start and becomes part of the context before the first user message) and hooks (which inject tool-call behavior at specific lifecycle events).

### CLAUDE.md — the project memory layer

CLAUDE.md is a markdown file at your project root. Claude Code reads it at the start of every session and loads it into context before your first message. It functions as persistent working memory across sessions.[^3]

Three tiers of CLAUDE.md exist:

1. **Project-level** (`<project-root>/CLAUDE.md`) — applies to this repository or folder
2. **User-level** (`~/.claude/CLAUDE.md`) — applies to all your Claude Code sessions
3. **Directory-level** (inside a subdirectory) — applies only when Claude Code is working in that subtree

What belongs in CLAUDE.md: conventions the model would otherwise have to re-learn each session (your preferred data validation library, which database not to touch, the correct naming convention for your API routes), known constraints (this service is behind a VPN, do not modify the production config file), and architectural facts (the auth flow lives in `/src/auth/`, the legacy ETL is in `/pipelines/legacy/`).

What does not belong: one-off task descriptions, things you only need for this session, or long background stories about the project. CLAUDE.md competes for context. Be aggressive about keeping it focused.

Auto-memory (available from v2.1.59) means Claude Code can write to a MEMORY.md file automatically when it learns something useful about your project during a session. The first 200 lines or 25KB of MEMORY.md load at session start.[^3]

### Hooks

Hooks let you inject code at specific lifecycle events in the Claude Code loop:

- **Pre-tool-call hooks** — run before a tool is invoked (can be used to log, audit, or block specific commands)
- **Post-tool-call hooks** — run after a tool result is returned (can be used to process results, send notifications)
- **Session hooks** — run at session start or end

If you are building a workflow where Claude Code touches production infrastructure, pre-tool-call hooks are your audit trail. Log every Bash command to a file. Alert if a command matches a destructive pattern. This is how you get the benefits of agentic automation without losing the ability to reconstruct what happened.

### Slash commands and skills

Slash commands (files in `.claude/commands/`) and skills (files in `.claude/skills/`) give Claude Code reusable capabilities. A skill is a markdown file describing a workflow — the equivalent of a stored procedure for agent behavior. When you invoke `/validate-schema`, Claude Code reads the skill definition, follows its steps, and reports back.

The skills system as of Claude Code 2.5 unifies slash commands into the skills interface: every skill gets a slash-command entry point, and frontmatter controls whether Claude can auto-invoke the skill, whether it appears in the `/` menu, and whether it runs in a subagent context.[^6]

This is the correct pattern for workflows you run repeatedly: write a skill once, invoke it by name. Marketing directors who run a weekly competitive-intelligence pipeline, finance analysts who pull and validate a monthly data extract, operations leads who audit a vendor list — all of these are skill candidates.

### MCP extensions

Model Context Protocol lets you connect Claude Code to external systems: databases, internal APIs, SaaS tools, file systems outside your project directory. MCP tools appear to Claude Code exactly like built-in tools — as JSON schemas in the tool list.

A key change in recent Claude Code versions: MCP tool schemas are no longer loaded at session start. Only tool names are loaded. The full schema is fetched on demand via ToolSearch when Claude Code actually decides to use the tool.[^6] This cuts context overhead dramatically for setups with many MCP connections — instead of loading 50 full MCP tool schemas upfront, Claude Code loads names and fetches schemas as needed.

---

## 5. Subagent parallelism — the Task tool, what it buys, what it costs

When Claude Code encounters a task that can be decomposed into independent subtasks, it can spawn subagents via the Task tool. Each subagent is a separate Claude instance with its own fresh context window, working independently and returning a summary when finished.[^7]

A subagent cannot see the main agent's conversation history. The main agent cannot see the subagent's tool calls as they happen — it only sees the final summary. This isolation is both the feature and the constraint.

**When subagent parallelism genuinely helps:**

- The task decomposes cleanly into independent chunks with no shared state. Example: "Validate the data quality in these 8 separate CSV files and give me a summary report on each." Each file is independent. Eight subagents can process them in parallel, and the main agent synthesizes the summaries.
- You want the subtask to run without polluting the main agent's context. A subagent that reads 20 large files, processes them, and summarizes the output uses its own context, not yours.
- The subtask is well-specified enough to run unattended. Subagents cannot interrupt you to ask questions mid-task.

**When subagent parallelism breaks or confuses things:**

- Tasks touch shared files. If two subagents are editing the same file, one will clobber the other. The official documentation is explicit: "Parallel only works when agents touch different files."[^7]
- The task requires iterative clarification. Because subagents return only a summary, any ambiguity that would normally trigger a clarifying question goes unasked, and the subagent makes its best guess.
- The main agent's plan depends on subagent results before proceeding. Subagents run in batches; the main agent waits for each batch to complete before proceeding.[^7] If you are depending on strict ordering, sequential execution is safer.
- Context overhead on the main agent. Each subagent summary that comes back gets appended to the main context. A dozen subagents each returning a 500-token summary adds 6,000 tokens before the main agent makes its next decision.

Practical configuration note: Claude Code parallelism is capped at 10 subagents per batch. If you specify more, they run in batches of 10.[^7] You can set `CLAUDE_CODE_SUBAGENT_MODEL` to run subagents on a lighter model (Sonnet rather than Opus) to save tokens on tasks where the subtask is mechanical.

The correct mental model for subagents: a specialist team you brief and then wait for. You don't watch them work. You get a report. That's the abstraction. Design tasks that produce useful reports, and you will get value. Design tasks where you need to supervise mid-execution, and you will be frustrated.

---

## 6. Benchmark numbers with appropriate context

Claude Opus 4.5, released November 24, 2025, scores 80.9% on SWE-bench Verified — the first AI model to break the 80% barrier on that benchmark.[^8] Claude Sonnet 4.5, released September 29, 2025, scores 77.2% on the standard configuration (10 trials, 200K thinking budget) and 82.0% with parallel test-time compute.[^9]

SWE-bench Verified is a set of 500 real GitHub issues from popular Python repositories. A model (or agent) must read the repo, understand the bug, write a fix, and pass the existing test suite. It is a meaningful benchmark for software engineering capability, closer to real work than HumanEval or similar coding benchmarks that test isolated function completion.

Three things worth understanding about these numbers before you cite them:

**The harness matters.** The SWE-bench score is not the model score alone. The eval infrastructure — how the agent is prompted, what tools it has, how many attempts it gets, how results are aggregated — contributes substantially to the number. Anthropic's Sonnet 4.5 benchmark notes specify the methodology: "64K thinking budget, interleaved scratchpads, 200K context window" with parallel compute for the high score.[^9] A different harness on the same model weights would produce a different number. When you read SWE-bench leaderboard comparisons, always ask: were the harnesses controlled?

**Performance improvements between models are partly harness improvements.** The Opus 4.5 announcement notes that improved hosting environments reduced infrastructure failures, which "benefited comparative benchmarks."[^8] Model capability and system reliability are compounding — you cannot easily separate how much of a score improvement is a smarter model vs. a more reliable executor.

**SWE-bench Verified is Python-repository bugs.** It does not measure: data pipeline robustness, MCP integration quality, cross-application agent coordination, business-logic correctness in domains with few training examples (legal, medical, specialized finance). Your use case may be dramatically easier or dramatically harder than the benchmark suggests.

The practical takeaway: Opus 4.5 and Sonnet 4.5 are genuinely capable at complex, autonomous software tasks. The numbers support using them for serious agentic work. The numbers do not support believing the model will reliably complete any arbitrary multi-step task you describe without well-designed tooling, clear CLAUDE.md context, and a review pass on the output.

---

## 7. The live controversy — vibe coding as a building strategy

The field is not settled on this. Here are the two serious positions, with named proponents.

### Position A: Vibe coding extends the legitimate surface area of who can build

The optimist case, stated carefully: LLMs have lowered the floor for software construction far enough that competent domain experts can now build working tools for their own workflows without a software engineer in the loop. A marketing operations analyst who can describe precisely what a customer segmentation pipeline should do — including edge cases, error handling, what "good output" looks like — can direct Claude Code to build it, review the output, and ship it. The constraint was never whether they understood the domain. The constraint was that they needed someone else to translate the domain knowledge into code. That constraint is materially weaker now.

This position has empirical support: Anthropic's internal report on how teams use Claude Code shows teams across functions — not just engineering — building and maintaining tools previously out of their reach.[^10] The SWE-bench scores are one data point. The other data point is the number of non-engineers shipping working internal tools.

The tech-optimist version of this position overstates it. "Anyone can build anything" is not what the evidence supports. What the evidence supports is: "domain experts with precise mental models of the problem can direct capable AI tools to build solutions within that domain, if they can read and evaluate the output."

### Position B: Vibe coding is irresponsible on systems with users, money, or security surface

Simon Willison, who has written more carefully about this than almost anyone, put it directly: "Vibe coding is irresponsibly building software through dice rolls, not caring what code is produced."[^11] He has also noted: "I'm sure we will see all sorts of horrifying data breaches from irresponsible vibe coding in the future."[^11]

Willison is not arguing that AI-assisted development is wrong. He proposed a complementary term — *vibe engineering* — for "where seasoned professionals accelerate their work with LLMs while staying proudly and confidently accountable for the software they produce."[^11] The distinction is accountability and comprehension, not the tools used.

The security failure mode is concrete. An AI agent building a web app will by default trust user input, will not implement rate limiting unless asked, will not audit authentication edge cases systematically, and will not catch logic errors in payment flows that only manifest under specific conditions. Karpathy's description of his own vibe coding workflow included: "The code grows beyond my usual comprehension, I'd have to really read through it for a while." On a throwaway weekend project, that is amusing. On a tool handling someone else's data, it is an incident waiting to happen.

### The nuanced position this lesson endorses

Vibe coding is a legitimate building strategy under three conditions, all of which must hold simultaneously:

1. **You can evaluate the output at the level that matters.** If the system processes financial data, you can run the output against known-correct test cases, audit the validation logic, and confirm the edge cases are handled. If you cannot do this evaluation, you are trusting output you cannot verify.

2. **The blast radius of failure is bounded and accepted.** Throwaway tools for your own use: low blast radius. Tools used by a team: medium blast radius, requires monitoring. Tools used by customers with their data: high blast radius, requires formal review even if the code was AI-generated.

3. **You have a recovery path.** If the tool breaks, fails, or produces wrong output, you can detect it and recover. Agentic systems that touch external databases, send emails, or make financial transactions need reversibility or explicit limits on what they can do autonomously.

If all three conditions hold, the speed advantage of directed AI construction is real and the risk is manageable. If any one fails, you are in Willison's "dice rolls" territory regardless of how good the model is.

---

## 8. Runnable experiment — trace the loop on a real task

This experiment has one goal: watch the agentic loop execute, step by step, on a non-trivial task. Reading the trace will give you the mechanical understanding no amount of description can replace.

### What to build

Give Claude Code the following task in a fresh project folder:

> "Build a small CLI tool that does the following: reads a CSV file, validates each row against a schema I will describe, and writes a validation report. The schema: each row must have a 'date' field in YYYY-MM-DD format, an 'amount' field that is a positive number, and a 'category' field that is one of: 'revenue', 'expense', 'transfer'. Rows that fail validation should be logged to a separate error file with the row number and the specific validation error. Give me a help message when I run it with --help. Use whatever language and libraries make sense."

This task is not trivial. It requires the model to make architecture decisions (which CSV parsing approach to use, how to structure validation logic, how to output errors), write code, and produce something runnable. A capable model on this task will make 15–25 tool calls before delivering a result.

### How to observe

Give Claude Code one additional instruction before it starts:

> "Before you begin, tell me your plan step by step. As you work, narrate each major decision you are making and why. When you have finished, summarize which tools you used, in what order, and what each one returned."

This narration instruction does two things: it surfaces the planning phase (making the model's internal decomposition visible), and it produces a readable trace of the tool-use loop after the fact.

### What to look for in the trace

Read the output carefully and note:

1. **How the model decomposed the task.** Did it plan to write the schema validator first, or the CLI wrapper first? Did it anticipate the error output file, or add it after realizing it was needed?
2. **How many Bash calls it made and what each returned.** Did it run the tool after writing it to verify it worked? Did it catch and fix any errors from the initial run?
3. **Whether the context compacted mid-task.** On a task this size you may not hit compaction, but watch for it on larger tasks.
4. **What the model did when it had to make an ambiguous decision** (e.g., whether "positive number" means strictly positive or allows zero). Did it guess, ask you, or document the assumption?

### What to do next

After the tool runs, try breaking it: feed it a CSV with malformed rows, a CSV with an extra column not in the schema, a CSV that is empty. Note whether the error handling holds. If it doesn't, tell Claude Code exactly what broke and what the correct behavior should be.

This is the complete workflow: design the task, observe the loop, evaluate the output, specify the correction. You are the domain expert who can evaluate correctness. The loop is the mechanism that implements your specification. The quality of the outcome depends on the precision of both.

---

## 9. Common failure modes at scale

### Context collapse on long sessions

A Claude Code session working across a large monorepo or a complex multi-service architecture will accumulate tool results fast. File reads, grep results, bash outputs — each appends to the context. When Claude Code auto-compacts, it summarizes the conversation. The summary preserves the key decisions but loses the detailed reasoning and the specific tool outputs.

The failure pattern: you start a session with a complex constraint ("the payment service must not be modified until after the security audit on May 15th"). The model acknowledges it. Two hours later, after context compaction, the constraint is gone from active context. The model edits a file in the payment service. You do not notice until the audit.

The mitigation: anything that must survive compaction goes in CLAUDE.md, not in the first message. Run `/context` regularly to see what is consuming space. Use `/compact focus on [specific constraint]` rather than letting auto-compaction choose what to preserve.

### Subagent summary loss

A subagent processing a large data pipeline returns a 400-token summary of what it did. The main agent uses that summary to proceed. The summary omits a critical edge case the subagent encountered and worked around silently.

This is the information-loss failure of the subagent pattern. The fix: be explicit in your Task tool invocation about what the summary must include. "Return a summary that includes: (1) what validations passed, (2) what validations failed and why, (3) any ambiguous cases where you made a judgment call, and (4) any files you modified." The model will construct the summary to match your specification.

### Tool call cascades

A Claude Code session trying to debug a broken deployment environment makes a Bash call that times out. The model retries. The retry also times out. The model tries a different approach. Several tool calls and 10 minutes later, the model has made 40 tool calls and the context is mostly timeout error messages.

Claude Code is not good at recognizing when to stop and surface the underlying infrastructure problem. It will try alternatives. You need to interrupt it. The lesson: watch the output stream during complex tasks. If you see repeated failures on the same class of operation, interrupt and diagnose the environment before letting the loop continue.

### Vibe-coded security debt

A marketing team builds an internal lead-scoring tool using Claude Code over a few sessions. It works. It processes a CSV export from the CRM and writes scores back. Six months later, a team member adds a feature: the tool now accepts a URL as input and fetches the lead data directly. Claude Code builds the URL-fetching feature. No one audits the input validation on the URL parameter. The tool is now a server-side request forgery vector sitting inside the corporate network.

This failure is not Claude Code's fault. It is a design failure: no audit gate between "feature added" and "feature deployed." The mitigation is procedural: any Claude Code session that touches a tool with network access or external data sources requires a human review of the diff, not just a test run.

---

## 10. Open questions — what is not settled

### How much of the SWE-bench improvement is model vs. harness?

The field does not have a rigorous decomposition of how much of the improvement from GPT-4-era baselines to Opus 4.5's 80.9% is attributable to base model capability vs. better agentic scaffolding, vs. better test-time compute strategies, vs. better training data for tool use. This matters for how you design your own agent harnesses: if most of the gain is in the scaffolding, your harness design decisions matter more than your model choice.

### Does the ReAct loop scale to tasks with unclear termination conditions?

The canonical ReAct loop exits when the model emits `end_turn`. On well-defined tasks (fix this bug, write this function, validate these rows), termination is clear. On open-ended tasks (improve this codebase, audit this system for security issues, refactor this module), the model's notion of "done" may not match yours. There is active work on evaluator-optimizer loops (Anthropic's *Building Effective Agents* describes this as a workflow pattern) where a second model judges task completion, but this is not yet standard in Claude Code's out-of-the-box behavior.[^12]

### Is "vibe engineering" stable as a category, or will better tools dissolve the distinction?

Willison's distinction between vibe coding (irresponsible, no comprehension) and vibe engineering (responsible, accountable) depends on the human reviewing and understanding the output. If models improve to the point where their self-review is more reliable than human review for specific task classes (which the SWE-bench numbers suggest is approaching for certain software engineering tasks), the category boundaries will shift. The question of when to trust AI self-review vs. require human review is not settled.

---

## Reviewer lens — specific technical pushback

**1. On the ReAct framing as "the" ancestor of agentic loops.**
The ReAct paper is influential but not the only relevant lineage. Concurrent work on tool-augmented LMs (Toolformer, Schick et al. 2023) and the broader neurosymbolic AI tradition had agent-tool loops before ReAct. Framing ReAct as the single origin story flattens the intellectual history. A complete account would note ReAct's specific contribution — the interleaving of reasoning traces with actions, and the empirical demonstration that this outperforms pure chain-of-thought — without implying the field started there.

**2. On the SWE-bench numbers as evidence of general capability.**
Chip Huyen, in her work on LLM evaluation methodology, argues persistently that benchmark performance on curated datasets does not predict performance on the messy, heterogeneous tasks of real production systems. SWE-bench Verified is a well-constructed benchmark, but it is Python repositories with existing test suites. There is no equivalent benchmark for: agentic workflows that span multiple services, tasks with ambiguous specifications, tasks where the correct answer requires domain knowledge not present in the training data. Citing 80.9% without noting the benchmark's domain limitations is a form of overfitting to the available measurement.

**3. On CLAUDE.md as the solution to context collapse.**
The lesson recommends CLAUDE.md for anything that must survive compaction. This is correct but incomplete. CLAUDE.md itself consumes context on every session start. A CLAUDE.md that has grown to 5,000 tokens because every project convention was added uncritically is now eating 5% of a 100K context window before the first message. The correct recommendation is CLAUDE.md for critical constraints, and periodic audits of CLAUDE.md to remove constraints that no longer apply. Context is not free, and the file that protects you from context collapse can itself become a context problem.

**4. On the vibe-coding hedge as a design test.**
The lesson uses Karpathy's "throwaway weekend project" hedge as a three-condition test (evaluate output, bounded blast radius, recovery path). This is useful but arguably under-specifies the security surface. "You can evaluate the output" is necessary but not sufficient for systems with external network access or user-supplied input. Simon Willison's lethal trifecta — private data + untrusted content + exfiltration channel — is the more precise frame for evaluating whether a system is safe to deploy. A lesson on vibe coding that doesn't explicitly cite the lethal trifecta has left the security analysis incomplete.

---

## Further reading

**Must read (fewer than 5):**
- [Anthropic, *How Claude Code Works*](https://code.claude.com/docs/en/how-claude-code-works) — primary source on the agentic loop, tools, and context management. Read the full page.
- [Yao et al., *ReAct: Synergizing Reasoning and Acting in Language Models* (arXiv 2210.03629)](https://arxiv.org/abs/2210.03629) — read Section 2 (method) and Section 4 (results on HotpotQA). Skip the ALFWorld details unless you want the RL comparison.
- [Simon Willison, *Vibe engineering* (Oct 2025)](https://simonwillison.net/2025/Oct/7/vibe-engineering/) — the clearest articulation of the responsible/irresponsible distinction from someone who has been thinking about this longer than almost anyone.

**Recommended:**
- [Anthropic, *Building effective agents* (Dec 2024)](https://www.anthropic.com/research/building-effective-agents) — the taxonomy of workflow patterns (prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer). Read it once for the vocabulary, return to it when designing multi-step workflows.
- [Piebald-AI, *Claude Code System Prompts* (GitHub)](https://github.com/Piebald-AI/claude-code-system-prompts) — reverse-engineered system prompts for every Claude Code version. Useful for understanding what the model is actually being told at session start.
- [Armin Ronacher, *What Is Claude Code's Plan Mode?* (Dec 2025)](https://lucumr.pocoo.org/2025/12/17/what-is-plan-mode/) — a detailed technical post on how plan mode works differently from auto mode, with specific implications for tool sequencing.

**Optional / going deeper:**
- [Anthropic, *Tool use: how it works*](https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works) — the precise mechanics of the client-side agentic loop, the tool-use contract, and when to use server-executed vs. client-executed tools.
- [alexop.dev, *Understanding Claude Code's Full Stack*](https://alexop.dev/posts/understanding-claude-code-full-stack/) — MCP, skills, subagents, and hooks explained with the composition view.

---

## Problem set

**Problem 1 — Classify your own workflows.**
List three things you have built or are actively building with Claude Code (or Codex, or Cursor). For each one, apply the three-condition test from Section 7: (a) Can you evaluate the output at the level that matters? (b) Is the blast radius bounded and accepted? (c) Do you have a recovery path? Which of your three workflows would Willison classify as vibe coding, and which as vibe engineering? If any is borderline, what would you need to add to move it into the "engineering" category?

**Problem 2 — Design a CLAUDE.md.**
Pick a real project you are working on. Write a CLAUDE.md for it that is under 300 words. The constraint forces you to prioritize. What are the three to five facts about this project that the model would otherwise have to re-learn every session or might get wrong? What are the one or two hard constraints that must survive compaction? Share it with one other person in the cohort and ask them: "If you started a Claude Code session on this project with this CLAUDE.md, what would you know, and what would still be missing?"

**Problem 3 — Read and stress-test a claim.**
The Anthropic *Building Effective Agents* post recommends: "find the simplest solution possible, and only increase complexity when needed, which might mean not building agentic systems at all." Read the full post (link in Further Reading). Then find one example from your own work or your organization where you used an agentic loop when a simpler workflow would have worked. What was the actual cost of the additional complexity (debugging time, context overhead, unpredictable behavior)? What would the simpler version have looked like?

**Problem 4 — Harness dissection.**
Run the experiment in Section 8. After Claude Code finishes, ask it: "Show me a count of every tool you called during this task and how many times you called each one." Then ask: "Which of those tool calls could have been eliminated with better upfront context from me?" This is how you build the habit of trace analysis. Report what you found.

**Problem 5 — Position defense.**
Read Simon Willison's *Vibe engineering* post (Oct 2025) and the Karpathy tweet thread. Write a 200-word position: where exactly do you disagree with Willison's framing, if anywhere, and why? If you agree with it entirely, name one specific context from your own work where the distinction between vibe coding and vibe engineering would have changed a decision you made.

---

## Citations

[^1]: Andrej Karpathy, tweet, February 2, 2025. https://x.com/karpathy/status/1886192184808149383 — Primary source coining "vibe coding." Full text quoted in Section 1. Verified live 2026-04-15. The hedge "not too bad for throwaway weekend projects" appears in the body of the tweet, not in a reply.

[^1b]: Andrej Karpathy, retrospective tweet on vibe-coding engagement, February 2025. https://x.com/karpathy/status/2019137879310836075 — Karpathy's commentary on how the original tweet was received. Verified URL in memory file, referenced for context on hedging intent.

[^2]: Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, Yuan Cao. "ReAct: Synergizing Reasoning and Acting in Language Models." arXiv:2210.03629, October 6, 2022. https://arxiv.org/abs/2210.03629 — Section 2 describes the Thought/Action/Observation loop. Section 4 reports 34% and 10% improvements on ALFWorld and WebShop. Verified 2026-04-15.

[^3]: Anthropic. "How Claude Code works." Claude Code Documentation. https://code.claude.com/docs/en/how-claude-code-works — Primary source on the agentic loop phases, built-in tools, context window management, CLAUDE.md, and auto-memory. Verified 2026-04-15.

[^4]: Anthropic. "Tool use: how it works." Claude API Documentation. https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works — Describes the tool-use contract, the client-side `while (stop_reason == "tool_use")` loop, the three tool execution categories (user-defined, Anthropic-schema, server-executed), and the JSON `tool_use` / `tool_result` message structure. Verified 2026-04-15.

[^5]: Piebald-AI. "Claude Code System Prompts." GitHub repository. https://github.com/Piebald-AI/claude-code-system-prompts — Reverse-engineered and published system prompt contents for each Claude Code version. 24 built-in tool descriptions, sub-agent prompts, CLAUDE.md loading. System prompt: ~2.5K tokens; tool definitions: ~14-17K tokens. Verified 2026-04-15.

[^6]: alexop.dev. "Understanding Claude Code's Full Stack: MCP, Skills, Subagents, and Hooks Explained." https://alexop.dev/posts/understanding-claude-code-full-stack/ — Published 2025-2026. Details on hooks, skills system unification as of Claude Code 2.5, MCP tool-name-only loading with on-demand schema fetch via ToolSearch. Verified 2026-04-15.

[^7]: claudefa.st. "Claude Code Sub-Agents: Parallel vs Sequential Patterns." https://claudefa.st/blog/guide/agents/sub-agent-best-practices — Details on Task tool parallelism cap (10 agents per batch), file-collision constraint, summary-only return, subagent model configuration via CLAUDE_CODE_SUBAGENT_MODEL. Verified 2026-04-15. Cross-referenced with official Claude Code subagents docs at https://code.claude.com/docs/en/sub-agents.

[^8]: Anthropic. "Introducing Claude Opus 4.5." Anthropic News. November 24, 2025. https://www.anthropic.com/news/claude-opus-4-5 — 80.9% on SWE-bench Verified; 10.6% improvement over Sonnet 4.5 on Aider Polyglot; 76% fewer output tokens at medium effort vs. Sonnet 4.5 best. Eval methodology: 64K thinking budget, interleaved scratchpads, 200K context window, parallel compute aggregation. Verified 2026-04-15.

[^9]: Anthropic. "Introducing Claude Sonnet 4.5." Anthropic News. September 29, 2025. https://www.anthropic.com/news/claude-sonnet-4-5 — 77.2% on SWE-bench Verified (10 trials, 200K thinking budget, no test-time compute); 82.0% with parallel attempts. OSWorld: 61.4% (up from 42.2%). Sustained focus on tasks exceeding 30 hours. Verified 2026-04-15.

[^10]: Anthropic. "How Anthropic teams use Claude Code." Internal case study PDF. https://www-cdn.anthropic.com/58284b19e702b49db9302d5b6f135ad8871e7658.pdf — Reports on cross-functional (non-engineering) teams building and maintaining tools using Claude Code. Verified URL in search results 2026-04-15.

[^11]: Simon Willison. "Vibe engineering." Simon Willison's Newsletter / Substack. October 7, 2025. https://simonwillison.net/2025/Oct/7/vibe-engineering/ — Defines vibe coding as "irresponsibly building software through dice rolls, not caring what code is produced." Proposes "vibe engineering" as the responsible alternative. Quote on data breaches from https://fedi.simonwillison.net/@simon/114920467223772328. Verified 2026-04-15.

[^12]: Anthropic. "Building effective agents." Anthropic Research. December 20, 2024. https://www.anthropic.com/research/building-effective-agents — Describes the evaluator-optimizer workflow pattern and the broader taxonomy of agentic workflows. Recommendation to start simple and add agentic complexity only when needed. Verified 2026-04-15.
