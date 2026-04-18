---
type: lesson
block: block-2-ai-employees
week: week-04
day_of_cycle: 2
day_name: tue
session_slug: building-a-sales-agent
date_due: 2026-06-09
tags: [agent-architecture, anthropic-building-effective-agents, workflows-vs-agents, mcp, tool-calling, bfcl, tau-bench, orchestrator-workers, evaluator-optimizer, react, langgraph]
sources:
  - anthropic-building-effective-agents-2024
  - anthropic-mcp-announcement-2024
  - mcp-specification-2025-11
  - bfcl-v4-leaderboard-2025
  - tau-bench-yao-2024
  - tau-bench-sierra-blog-2024
  - weng-llm-agents-2023
  - yao-react-iclr-2023
  - anthropic-swe-bench-sonnet-2024
  - langchain-deep-agents-2025
  - anthropic-think-tool-2025
  - willison-mcp-prompt-injection-2025
  - cognition-devin-performance-review-2025
  - sierra-100m-arr-techcrunch-2025
  - anthropic-advanced-tool-use-2025
last_verified: 2026-04-17
word_count_target: 6000
---

# Agent architectures for production sales workers — Anthropic's Building Effective Agents applied, tool-calling loops, and MCP as the connector layer

## Why this matters

On December 19, 2024, Erik Schluntz and Barry Zhang published "Building Effective Agents" on Anthropic's research blog, and — without announcing it as such — shipped the 2026 default reference for anyone building a production AI worker.[^1] The post is 4,000 words of thesis, stripped of framework marketing. Its central claim reads cold: *"When building applications with LLMs, we recommend finding the simplest solution possible, and only increasing complexity when needed. This might mean not building agentic systems at all."*[^1] Most teams pattern-matching on "AI agents" in 2026 are not obeying that rule. They are buying Sierra, running LangGraph, importing Crew or AutoGen, and hoping the framework hides the hard part — which is that the LLM fails on tool call number seven, forgets the fifth step of the plan, and silently corrupts the CRM row the user will only notice three weeks later.

This lesson teaches the Schluntz/Zhang taxonomy — prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer, and the autonomous loop — as the diagnostic you run against every sub-problem of the sales agent you drafted on Monday. Then it teaches the Model Context Protocol (MCP) as the connector layer that decides whether your tools are discoverable by other agents in 2026 or trapped behind bespoke glue code. Then it teaches tool-calling reliability — the Berkeley Function-Calling Leaderboard and τ-bench results — as the quantitative check on whether your six-tool sales agent will actually work at 10 a.m. on a Tuesday after three emails have come back marked vacation-responder.

After you internalize this you will be able to: (1) decompose any AI-worker pipeline into the five Anthropic patterns and defend why each sub-problem is workflow or autonomous, (2) write a tool-use schema that survives contact with Claude Sonnet 4.6 at N=6 tools without the common failure modes, (3) evaluate an MCP server against a direct-API alternative with actual integration-cost math rather than vibes, (4) read a BFCL or τ-bench result and translate it into a production reliability budget for your sales agent, and (5) argue — with operator-level specifics — why the "autonomous agent" brand is mostly wrong for revenue-adjacent workflows in 2026, and what to deploy instead.

## Prerequisites

- Monday's lesson on the sales-agent pipeline anatomy. You should have a Mermaid diagram of the sub-problems — ICP scoring, enrichment, research, personalization, dispatch, reply classification, qualification, handoff. We route those sub-problems into patterns today.
- Working vocabulary from Block 0 Week 2 on Claude Code and tool use. If "JSON schema," "tool definition," and "model stops when it sees stop_reason=end_turn" are familiar, you qualify. We do not re-teach tool-use mechanics from first principles — Anthropic's docs cover that and we link them.[^2]

## Layer 1 — Schluntz and Zhang's taxonomy, with their load-bearing quote

Read the Anthropic post's definitions slowly, because the whole taxonomy depends on one distinction:

> "Workflows are systems where LLMs and tools are orchestrated through predefined code paths. Agents, on the other hand, are systems where LLMs dynamically direct their own processes and tool usage, maintaining control over how they accomplish tasks."[^1]

That is the only line in the post that matters for a production decision. "Predefined code paths" means the graph is fixed at author time — the LLM fills in the cells but does not decide the topology. "Dynamically direct their own processes" means the LLM decides, at run-time, what comes next, using tool outputs to steer. Everything else in the post is a taxonomy of predefined code paths, plus one section on the runtime case.

The five predefined patterns — the workflows — are the useful part for a sales agent, because almost every sub-problem of a sales agent is a predefined-path problem in disguise. Here is each pattern stated in terms the reviewer-lens critics would accept, then mapped to the sales-agent sub-problem where it fits.

**Prompt chaining.** Decompose a task into sequential LLM calls where each call processes the previous output, with programmatic gates between calls.[^1] The canonical illustrations in the post are (a) generate an outline → check the outline meets criteria → generate the doc, and (b) translate a doc then refine the translation. The gate is the entire point: you check the intermediate with code, not another LLM, and you fail fast if the draft outline doesn't hit the required shape. Sales-agent fit: personalization generation. Draft a research summary → code-gate on "contains a post-2024 signal" → generate the email → code-gate on subject-line length, paragraph count, link density → send. Every gate in code is one fewer failure mode for the downstream model to manage.

**Routing.** Classify inputs and direct them to specialized follow-up tasks.[^1] The prompt that does the classification is not the prompt that does the handling; that separation of concerns is the point. Canonical illustration in the post: customer-support tickets routed to refund / technical / general-query specialists. Sales-agent fit: reply classification, which is the core pattern we build in today's experiment. Incoming email → classifier routes to {interested, not-interested, objection, auto-reply, OOO, spam} → each branch goes to a specialist handler (calendar-scheduler, objection-drafter, nurture-sequence, silent-suppress). Skipping routing and asking one prompt to "handle the reply" is how you ship a sales agent that books meetings with vacation auto-responders.

**Parallelization.** Run independent subtasks simultaneously, either via *sectioning* (break the task into chunks that can run in parallel and aggregate) or *voting* (run the same prompt N times and combine answers for robustness).[^1] Sales-agent fit, two places: (a) sectioning for research — fire three simultaneous lookups (LinkedIn activity, recent funding news, hiring signals) and join the results before drafting, instead of a serial chain that takes 3× the latency; (b) voting for ICP-fit scoring on high-stakes prospects — score the fit three times with different framings and average, because any single prompt will drift on edge cases. The voting move is underused in 2026 sales-agent stacks because it triples token cost for scoring; apply it only on prospects above a price threshold.

**Orchestrator-workers.** A central LLM dynamically decomposes tasks, delegates them to worker LLMs, and synthesizes results.[^1] The orchestrator-workers pattern is the first that edges into agent territory — the orchestrator decides which workers to call, based on the input — but Anthropic still classifies it as workflow because the decomposition strategy is bounded by prompt-level instructions, not by a tool-call loop that can go anywhere. Sales-agent fit: the research-and-draft step for a high-value prospect. Orchestrator reads the ICP row → decides which workers to fire (funding-researcher, product-researcher, stakeholder-mapper, past-customer-pattern-matcher) → each worker produces a structured finding → synthesizer composes the email. Harrison Chase's framing from LangGraph's 2025 Deep Agents paradigm calls this "subagents with starter prompts"; same pattern, rebranded.[^3]

**Evaluator-optimizer.** One LLM generates, a second critiques, the first revises, loop to a stopping condition.[^1] The post cites literary translation and complex search as canonical uses. Sales-agent fit: personalization quality control, which is where your agent either reads like a human operator or reads like 11x's default template. Draft → critique-against-rubric (concrete signal cited? personalization specific not generic? opening not AI-smelling? subject under 50 chars?) → revise → check again, max 2 iterations. This is the pattern we build in the experiment; it is also the pattern Hamel Husain's eval-driven-development playbook pushes hardest on, because the critique step is where you can swap in increasingly rigorous rubrics without retraining.[^4]

Then the sixth shape, which Schluntz and Zhang reserve for a separate section:

**Autonomous agents.** The LLM runs a tool-call loop, deciding at each step what to do next based on feedback from the environment, and stops when it hits a completion signal or an iteration cap.[^1] The post's canonical illustration is a coding agent that reads a file, runs a test, reads the error, edits, runs again — exactly the pattern Anthropic's own SWE-bench Verified agent used to hit 49% on that benchmark in October 2024 with Claude 3.5 Sonnet.[^5] Sales-agent fit: **almost nowhere**, and this is the single most important operational judgment in the lesson. The cases where an autonomous loop justifies its cost over a workflow in a revenue context are narrow: an inbound triage agent that can safely bail to a human, a research agent that reads a landing page and a LinkedIn profile and writes a short brief (bounded task, read-only tools, human reviews output). For outbound dispatch, CRM writes, or qualification branching, the workflow is strictly dominant — you want code-level gates on every hop where a wrong call creates permanent damage. Schluntz and Zhang say this plainly: *"agentic systems often trade latency and cost for better task performance, and you should consider when this tradeoff makes sense."*[^1] For sales-agent sub-problems where the failure mode is "I just sent the wrong email to a real prospect," the tradeoff does not make sense.

A useful heuristic from the post, almost buried: use the *least* complex pattern that works. Prompt chain before routing, routing before orchestrator-workers, workflows before autonomous. Every layer of complexity adds a failure mode that has to be observed, evaluated, and regression-tested. The reason most 2025 "agent" projects underperformed the internal Notion doc that preceded them is that teams started at the top of the ladder.

## Layer 2 — Tool-calling reliability, quantitative: BFCL and τ-bench

Here is where most agent-architecture writeups lose nerve, because the honest numbers are ugly. The Berkeley Function-Calling Leaderboard (BFCL), maintained by Shishir Patil's Gorilla group at Berkeley, is the public obstacle course for tool-calling reliability across thousands of single-turn, multi-turn, and multi-step function-calling tasks. Version 4 of the leaderboard evaluates frontier models across serial and parallel function calls using an Abstract Syntax Tree comparison so evaluation scales to thousands of functions.[^6][^7] The framing line from the BFCL paper, published in Proceedings of Machine Learning Research 2025, is this: *"State-of-the-art LLMs excel at single-turn calls, memory, dynamic decision-making, and long-horizon reasoning remain open challenges. Early results reveal a split personality: top AIs ace the one-shot questions but still stumble when they must remember context, manage long conversations, or decide when not to act."*[^7]

Translate that to a sales agent: single-turn tool calls are the easy part. The hard part is the multi-turn where the agent has to pick up the thread three hops in, remember which prospect row it was working on, and correctly decide *not* to call the send-email tool because the reply classifier flagged an out-of-office.

Sierra Research's τ-bench (Yao, Shinn, Razavi, Narasimhan; arxiv 2406.12045, June 2024) is the sharper diagnostic for revenue-adjacent workflows, because it simulates a user–agent–tool conversation against a stateful database and scores the final state of that database against a ground-truth goal state.[^8][^9] τ-bench's two domains — retail and airline — are procedurally close to sales-agent sub-problems: multi-turn interaction, policy-constrained actions, database writes that have to be correct. The headline finding, quoting the abstract: *"even state-of-the-art function calling agents (like gpt-4o) succeed on <50% of the tasks, and are quite inconsistent (pass^8 <25% in retail)."*[^8]

The *pass^k* metric matters here more than pass@k. Pass@k asks "did at least one of k attempts succeed"; pass^k asks "did *all* k attempts succeed." Pass^k is the reliability metric — if your agent has to handle 500 replies in a day, you need it to succeed consistently, not occasionally. A pass^8 below 25% on the retail domain is another way of saying the agent drifts one time in four on a run of eight hard multi-turn sessions. If you are pushing that agent at 500 sessions a day, "one in four drift" is hundreds of incorrect database writes per day.

The improvement path Anthropic published — the March 2025 "think" tool post by Anthropic Applied AI — is instructive because it maps straight onto the sales-agent problem.[^10] They added a simple "think" tool that lets Claude pause and reason without producing a user-visible action, combined with an optimized prompt, and on τ-bench airline their pass^1 went from 0.370 baseline to 0.570 — a 54% relative improvement on the hardest domain.[^10] On retail, pass^1 went from 0.783 to 0.812 — a smaller gain because the baseline was already higher. The implication for a sales agent: you want a scratchpad tool the LLM can use to reason about ambiguous replies before committing to a classification, because the pattern that moves τ-bench numbers is more thinking, not more tools.

The operator takeaway is a number: **if your sales-agent design calls for N>5 tools in a single decision-making scope, you should expect the single-turn accuracy to be in the 80s and the multi-turn reliability under 50% on par-τ-bench-difficulty tasks, absent a "think" scratchpad and aggressive schema engineering.** That is not a reason to abandon tools — it is a reason to split the agent into workflows where possible and reserve the N>5-tool scope for the narrowest loop.

Ben Hylak's practitioner framing on raindrop.ai observability posts, and Shunyu Yao's own τ-bench commentary, both converge on this prescription: you lose reliability at the seams between tools, so the design principle is "fewer tools at each decision boundary," not "more capable single agent."[^9]

## Layer 3 — Tool-use schemas at the JSON level, and the six-tool sales-agent example

This is the layer most architecture posts skip. A tool-use schema is not just a dict of parameters; it is the contract the LLM pattern-matches against when deciding which tool to invoke. Anthropic's own docs are explicit that the `description` field is the single most important piece of information in the schema — not the name, not the parameter types, the description.[^2] That is because Claude decides which tool to call by reading descriptions and matching against user intent, not by reading the tool name.

Here is a minimum viable sales-agent tool set — six tools — in the Anthropic tool-use JSON format:

```json
[
  {
    "name": "search_prospect",
    "description": "Search for a prospect by name and company. Returns canonical profile if found, null if not. Use BEFORE enrich_prospect to avoid duplicate enrichment cost. Do not call repeatedly on same input within a session.",
    "input_schema": {
      "type": "object",
      "properties": {
        "full_name": {"type": "string"},
        "company_domain": {"type": "string", "format": "hostname"}
      },
      "required": ["full_name", "company_domain"]
    }
  },
  {
    "name": "enrich_prospect",
    "description": "Pull enrichment data (title, LinkedIn URL, recent public signals) for a prospect. Costs ~$0.10 per call. Only call once per prospect per session. Returns structured record with fields: title, linkedin_url, signals[], last_job_change_date.",
    "input_schema": {
      "type": "object",
      "properties": {
        "prospect_id": {"type": "string"}
      },
      "required": ["prospect_id"]
    }
  },
  {
    "name": "draft_email",
    "description": "Draft a personalized outbound email given prospect context and a campaign template ID. Returns {subject, body, signals_used[]}. Does NOT send — dispatch requires send_email. Caller must review before sending.",
    "input_schema": {
      "type": "object",
      "properties": {
        "prospect_id": {"type": "string"},
        "campaign_template_id": {"type": "string"},
        "signals": {"type": "array", "items": {"type": "string"}}
      },
      "required": ["prospect_id", "campaign_template_id"]
    }
  },
  {
    "name": "send_email",
    "description": "DISPATCH an email to a prospect via the configured sending domain. IRREVERSIBLE — this reaches a real inbox. Requires compliance_check=true from a prior compliance_check call made in this session. Use ONLY when the user has explicitly approved sending.",
    "input_schema": {
      "type": "object",
      "properties": {
        "prospect_id": {"type": "string"},
        "subject": {"type": "string", "maxLength": 80},
        "body": {"type": "string"},
        "compliance_check_id": {"type": "string"}
      },
      "required": ["prospect_id", "subject", "body", "compliance_check_id"]
    }
  },
  {
    "name": "classify_reply",
    "description": "Classify an inbound email reply into one of: interested, not_interested, objection, auto_reply, out_of_office, spam. Returns {category, confidence, reasoning, extracted_objection?}. Call this BEFORE taking any action on a reply.",
    "input_schema": {
      "type": "object",
      "properties": {
        "reply_text": {"type": "string"},
        "prospect_id": {"type": "string"}
      },
      "required": ["reply_text", "prospect_id"]
    }
  },
  {
    "name": "update_crm",
    "description": "Write a single field update to the CRM row for a prospect. Idempotent by (prospect_id, field_name, new_value). Do not retry on success. Logs every call.",
    "input_schema": {
      "type": "object",
      "properties": {
        "prospect_id": {"type": "string"},
        "field_name": {"type": "string"},
        "new_value": {"type": "string"}
      },
      "required": ["prospect_id", "field_name", "new_value"]
    }
  }
]
```

Four mechanism details that are load-bearing and that the docs do not emphasize enough:

1. **The `description` field encodes the order of operations.** Notice "Use BEFORE enrich_prospect," "does NOT send," "requires compliance_check=true from a prior call." These clauses are how you prevent the agent from calling send before draft or skipping the compliance gate. The model reads them; they show up in the decision trace. Do not waste this surface.
2. **Irreversibility is stated explicitly.** `send_email` says "IRREVERSIBLE — this reaches a real inbox." When Anthropic's own SWE-bench agent was designed in 2024, the architecture note was that the model has only two tools — Bash and Edit — precisely because every additional tool is another thing to reliably-not-call at the wrong moment.[^5] For a sales agent, treat every irreversible tool as a separate red-lit entity in your schema and in your description copy.
3. **Budget hints.** "Costs ~$0.10 per call. Only call once per prospect per session." Models respect budget cues in descriptions because they were trained to. You will spend ~$1/session on uncontrolled enrichment without this line.
4. **Namespace your tools.** In a multi-team deployment, prefix names — `crm_update`, `email_send`, `prospect_enrich` — which is Anthropic's explicit recommendation for multi-service deployments; same shape as Slack's function names in their public MCP server.[^2]

This six-tool set is close to the ceiling of what a single LLM scope should be asked to decide among. Above six, hit rates fall into the 80-percents even on frontier models. The move is to partition — give the reply-classification workflow only the `classify_reply` tool, the dispatch workflow only the `draft_email` / `compliance_check` / `send_email` tools, and orchestrate at a level above. This is the Schluntz/Zhang parallelization-into-workflows pattern reappearing at the tool-scope level.

## Layer 4 — MCP as the connector layer, and the "MCP vs direct API" fight

Anthropic announced the Model Context Protocol on November 25, 2024, as an open standard for connecting AI assistants to data systems — CRMs, content repos, calendars, browsers — via a uniform discovery-and-invocation interface.[^11] The original SDKs shipped for Python and TypeScript; the reference-server repo included Postgres, Slack, GitHub, Google Drive, and a browser server. The second major spec release (2025-11-25) added task abstractions for long-running operations, revised auth flows, and was published as the one-year-anniversary update.[^12][^13] In December 2025 Anthropic donated MCP to the newly formed Agentic AI Foundation under the Linux Foundation, alongside support from OpenAI, Google, Microsoft, and AWS.[^13] MCP server downloads went from ~100K in November 2024 to over 8M by April 2025, with 5,800+ servers and 300+ clients.[^13] The ecosystem won the adoption fight. That does not settle whether you should use it.

The naive reading is: MCP standardizes tool integration, so you should always MCP. The experienced reading — the one any operator who has actually shipped an agent has internalized by mid-2025 — is more nuanced. Here are the two positions, stated steelman-to-steelman.

**Position A — use MCP for everything.** Thoughtworks's 2025 analysis, a16z's Accel-adjacent writing, and the Anthropic position all converge on: MCP is a protocol, the protocol won, connectors written against MCP are portable across Claude / GPT / Gemini / Llama-hosted clients, and every hour you spend hand-wiring an Anthropic SDK tool-use call against your CRM is an hour you will pay again when the next model family shifts your tradeoff.[^14][^13] For a sales agent connecting to Salesforce, HubSpot, Gmail, Google Calendar, and a handful of enrichment APIs, MCP is the lingua franca. You also get agent composability: another MCP client (Claude Desktop, Cursor, a partner's agent) can pick up your sales-agent's tools and compose them without new glue code. For an agency building AI workers for multiple clients, this is decisive.

**Position B — MCP adds overhead you do not need, especially for single-application agents.** Simon Willison's April 2025 post documented a specific prompt-injection security failure mode in MCP where a malicious tool description can alter the behavior of other tools in the same context — his phrase: *"MCP does not enforce a comprehensive error-handling standard, and its scope is currently limited to discovery and invocation."*[^15] A set of 2025 security writeups cataloged six named flaws: tool poisoning, cross-server tool shadowing, silent redefinition ("rug pull" where a tool mutates its description post-install), supply-chain attacks (the 2025 Postmark MCP breach where a compromised npm package rerouted outgoing email to attackers), authentication flaws affecting 43% of MCP servers, and the context-window tax of some MCP servers exposing 40K+ tokens of tool descriptions.[^16] The security experts' summary was blunt: *"in most cases you don't need to use MCP — if you can do a straight-up API call to a tool, do that."*[^16] For a sales agent running a single client's Salesforce, the single-tenant case, the direct SDK call may be safer, faster, and cheaper in context tokens.

**The operator judgment.** MCP is right when (a) you are deploying the same tool surface to multiple AI clients (your Claude Code, your Cursor, a partner's agent, a customer's agent), (b) you are exposing tools to a trust-boundary outside your own org, (c) your sales agent's tool set is likely to be composed with other agents' tool sets in the next 12 months. Direct SDK is right when (d) you are building a single-purpose agent for a single operator, (e) security surface is load-bearing (finance, legal, healthcare data), (f) the context-token cost of the MCP wrapper matters at your volume. For a Block 2 reader building their first sales agent for one client, default to direct Anthropic SDK tool-use for the revenue-critical tools (draft_email, send_email, update_crm) and to MCP for the read-only enrichment tools where the composability upside is higher and the irreversibility risk is lower.

If you ignore both positions and just "use MCP because it's the standard," you will likely trip on one of the six flaws within six months of production. If you ignore MCP entirely, you will re-write integration code in eighteen months when the next client asks you to plug their agent into yours.

## Layer 5 — The autonomous-vs-workflow fight, with Cognition and Sierra as named parties

This is the live controversy Schluntz and Zhang engage only obliquely, so let's state it directly, with the 2025 data.

**Position A — autonomous agents are the future; workflows are the training wheels.** Cognition (Devin), Adept (now mostly absorbed into Amazon), and early Sierra positioning all argued that the agent pattern — LLM runs a loop, decides for itself, completes open-ended tasks — is where the value lives. Cognition's March 2024 Devin launch demo showed an agent autonomously picking up Upwork tasks, spinning up a VM, and shipping code.[^17] The pitch was: a single agent that can do anything a junior engineer does, orchestrating tools end-to-end.

**Position B — workflows win in production; autonomous is a demo**. The counter, articulated by Schluntz and Zhang implicitly and by practitioners explicitly, is that autonomous agents trade predictability and cost for flexibility you rarely need. Cognition's own January 2026 internal performance review, published on their blog, described Devin's autonomous agents as *"very like enthusiastic interns — they try very hard but don't know everything, get little things wrong, ask a lot of questions."*[^18] An October 2024 Futurism investigation tested Devin on real tasks and found it bungling the majority — spending days pursuing impossible solutions rather than recognizing blockers, hallucinating about Railway deployment mechanics, producing overly complex unusable code.[^19]

Sierra, Bret Taylor's customer-service agent company, is instructive for the opposite reason: their success story is not an autonomous agent but a tightly-scoped workflow agent with heavy guardrails. Sierra reached $100M ARR 21 months after February 2024 launch, with customers including Deliveroo, Discord, Ramp, Rivian, SoFi, Tubi, Cigna, ADT.[^20] The architectural pattern is not "one agent does everything" — it is orchestrator-plus-specialized-workers with strict policy gates and human escalation on uncertain cases.[^20] Sierra's Ghostwriter feature (March 2026) compresses *agent-building* into a conversation in plain English, but the resulting agent is itself a workflow bounded by policy rules, not a freely-roaming loop. The $10B valuation attached to that architecture, not to the "autonomous" brand.[^21]

**My position:** for a 2026 sales agent, the autonomous-agent pattern is strictly dominated by orchestrator-workers-plus-gates for every sub-problem except possibly research. The evidence is the error-mode distribution. When an autonomous agent fails, it fails silently, non-deterministically, and often expensively (send the wrong email to a real prospect, write the wrong value to the CRM row the VP looks at tomorrow). When a workflow fails, it fails at a code gate, loudly, with a specific cause you can fix. Error loudness is a feature, not a bug, in revenue-adjacent systems.

The exception — research — is the one place autonomy pays. Reading a landing page, pulling a LinkedIn profile, cross-referencing a news article, producing a 150-word brief, iterating on what to look at next based on what it found: this is an open-ended loop with read-only tools and a human reviewer, and the Schluntz/Zhang tradeoff argument applies in its favor. Even there, treat the agent's output as input to a gated downstream workflow, not as the final word.

## Operator case studies / war stories

**Case 1 — Sierra at $100M ARR, the architecture choice.** Sierra's public writing on their blog, supported by TechCrunch's November 2025 teardown of their ARR ramp, describes an architecture where every customer-service agent is a policy-bounded workflow with explicit escalation gates.[^20][^21] WeightWatchers, Sonos, SiriusXM, and OluKai — their earliest customers — all required the agent to escalate to a human for anything outside a named policy scope. The reason the architecture won is that the enterprise buyer's concern was never "can it autonomously do everything," it was "can it autonomously do *nothing harmful*." Workflow architecture encodes that negative constraint natively; autonomous architecture does not.

**Case 2 — Anthropic's SWE-bench Verified agent, the minimal-scaffolding counter.** In October 2024 Anthropic hit 49% on SWE-bench Verified with Claude 3.5 Sonnet using an agent with only two tools: a Bash tool and an Edit tool.[^5] The result was state-of-the-art at the time, beating prior agents with more elaborate scaffolding. The architectural lesson: for a *bounded* open-ended task (fix a GitHub issue in a known repo), the autonomous pattern works when the tool surface is narrow and the feedback signal (test passes/fails) is deterministic. Sales agents do not have this property — there is no unit test that tells you "the email was appropriate." This is why the SWE-bench pattern does not transfer to outbound sales despite the surface similarity.

**Case 3 — Cognition's 2025 pivot from demo to tool, the "enthusiastic intern" post.** Cognition's own 2025 annual review on Devin pulled back on the "autonomous software engineer" framing and repositioned Devin as a tool that engineers delegate specific tasks to, with heavy review.[^18] The quoted architecture change: less autonomy per task, more human-in-the-loop gating, more explicit task scoping. This is the same lesson Sierra learned from the opposite direction — start workflow, stay workflow, let the model decide inside the box, not about the box.

**Case 4 — Claude Sonnet 4.6 on τ-bench with the "think" tool, a scratchpad that matters.** Anthropic's March 2025 "think" tool post documented that adding a simple "pause-to-reason" tool raised Claude 3.7 Sonnet's τ-bench airline pass^1 from 0.370 to 0.570.[^10] The load-bearing mechanism: not more tools, but a tool that buys the model more deliberation inside the loop. For a sales-agent reply classifier, exposing a "think" scratchpad before it commits to a classification category is the single highest-ROI architectural move in the pattern.

## Runnable experiment

This experiment mixes two modes: you direct Claude Code to run the classifier builds, and you read the accuracy numbers yourself.

**Phase 1 — Decompose your Monday pipeline into the five patterns.** Take your Monday Mermaid diagram. For each sub-problem, label it with the Schluntz/Zhang pattern and a one-line defense. Write this as a doc before touching Claude Code. Sharpen the defenses — when you claim a sub-problem is orchestrator-workers rather than a prompt chain, say *why* the decomposition cannot be predetermined. When you claim it is autonomous, say *why* no workflow structure works. Most of your assignments should be routing or prompt chain; that is correct and reflects the architectural honesty of sales-agent work.

**Phase 2 — Build the single-shot reply classifier.** Ask Claude Code: *"Build a reply-classifier function as a single-shot prompt against Claude Sonnet 4.6. It takes a raw inbound email reply and the original outbound email as input, and returns JSON {category, confidence, reasoning, extracted_objection?} where category is one of interested, not_interested, objection, auto_reply, out_of_office, spam. Use the Anthropic SDK. Write 20 test cases with ground-truth labels, covering 4 examples per category (6 categories = 24, trim the least interesting). Run the classifier on all 20 and report accuracy, confusion matrix, and time per call."*

Expected outcome: accuracy in the 80s on this size test set for a reasonable prompt. The pure `interested` and `out_of_office` categories should be near-perfect; `objection` versus `not_interested` will be where confusion lives.

**Phase 3 — Build the evaluator-optimizer variant.** Ask Claude Code: *"Now build an evaluator-optimizer variant: the drafter model (Sonnet 4.6) produces the classification and reasoning; a critic model (also Sonnet 4.6, different prompt) reviews against a rubric I supply: (a) is the reasoning specific to the reply text rather than generic? (b) does the extracted_objection (if any) quote an actual phrase from the reply? (c) is the category consistent with the reasoning? The drafter then revises once given the critique. Compare accuracy on the same 20 test cases vs the single-shot baseline. Report delta in accuracy, delta in latency, delta in token cost."*

Expected outcome: a few percentage points of accuracy improvement, concentrated on the hard `objection` vs `not_interested` boundary. Latency roughly 2.5–3× the single-shot (two LLM calls instead of one, plus the revision). Token cost scales similarly. You will read this table and make a production call: for which categories is the eval step worth the cost, and for which is the single-shot fine?

**Phase 4 — The 400-word position memo.** Write, by hand or dictated: which Schluntz/Zhang pattern wins for which sales-agent sub-task and why, using your classifier data as the reference point. Defend or attack the claim that evaluator-optimizer is always worth the cost for revenue-touching classifications. Name one place where you would use it in production and one where you would not. This memo is the artifact — it is what the lesson produces in you.

## Problem set

1. **Pattern assignment with defense.** For each of the nine sub-problems from your Monday pipeline (ICP score, enrich, research, segment, prioritize, personalize, dispatch, classify reply, qualify, handoff), assign one of {prompt-chain, routing, parallelization-sectioning, parallelization-voting, orchestrator-workers, evaluator-optimizer, autonomous}. Write 2 sentences defending each assignment. Flag any where you reached for autonomous and justify with a specific error-mode argument.

2. **The autonomous-dominance position.** Take this claim: *"For sales agents in 2026, the autonomous-agent pattern is strictly dominated by orchestrator-workers plus human-in-the-loop gates on every revenue-touching sub-problem."* Defend or refute in 500 words with ≥3 citations from this lesson (Anthropic, Sierra, Cognition, BFCL, or τ-bench). If you refute, name the specific sub-problem where you believe autonomy wins and cite an existing production deployment that validates the position.

3. **Six-tool schema design.** Starting from the six-tool JSON schema in Layer 3, add a seventh tool — `schedule_meeting` — that lets the agent propose calendar slots. Write the full schema including description. Then list three specific failure modes the description mitigates (e.g., "agent schedules against a calendar slot that conflicts with an existing meeting" — how does your description prevent it). Cite the Anthropic advanced-tool-use doc for at least one claim.[^2]

4. **MCP vs direct API, defend both.** Pick a specific Salesforce integration for the sales agent (e.g., reading and writing CRM Lead records). Write two parallel 150-word cases: the case for MCP-via-reference-server and the case for direct Salesforce SDK via Anthropic tool-use. Each case must cite one concrete tradeoff with numbers — latency, context tokens, security surface, or portability. End with a one-sentence operator pick and why.

5. **Reproduce a τ-bench-shaped result.** You do not have to run full τ-bench, but do this: ask Claude Code to build a six-tool mock agent with dummy tool implementations (the tool prints what it would do, does not actually do it), write 10 three-turn conversation scripts that require the agent to reason about which tool to call in what order, run the agent on each script 3 times, and report (a) average correctness and (b) pass^3 — did all three runs on the same script succeed. If pass^3 drops sharply below pass^1, name the dominant failure mode (schema ambiguity? description ambiguity? tool order dependency?). Write two sentences on the architectural fix you would apply.

## Common failure modes at scale

**The N>6 tools collapse.** A team plans a sales agent with a "full integration stack" — CRM read, CRM write, email draft, email send, calendar read, calendar write, LinkedIn search, Apollo enrich, Clay enrich, Slack notify, Asana create — 11 tools in a single prompt scope. BFCL-shaped single-turn accuracy holds; multi-turn reliability craters; the agent occasionally "upgrades" prospects in the CRM from a Slack message it misread as a status update. The fix is not a better model; it is splitting into workflows where each scope sees ≤5 tools.

**The silent-revision failure in evaluator-optimizer.** The critic model is too lenient because its rubric is vague ("is the reasoning good?"). The drafter passes on first try 95% of the time. The team believes the eval is working. Production accuracy does not move. Audit reveals the critic is rubber-stamping. Fix: tighten the rubric to *named-criterion-with-quote* clauses ("does the reasoning quote a specific phrase from the reply?"). Accuracy moves.

**The MCP supply-chain breach.** Team ships a sales agent with an MCP server for their dispatch provider. Six months later, the npm package for that MCP server gets a compromised update — one line that BCCs outgoing emails to an external address. Detection takes two weeks. This is not hypothetical — it is the Postmark MCP breach pattern from 2025.[^16] Fix: pin MCP server versions, audit description changes before updating, use a private server registry for irreversible tools.

**The autonomous-loop cost blowup.** A team builds an "autonomous research agent" that loops on a prospect until it decides it has enough to write an email. For easy prospects (clear LinkedIn signal, recent news) it converges in 2 loops. For edge cases (obscure company, sparse signal) it loops 30+ times, spending $5 per prospect in LLM cost. The team's weekly bill doubles before they notice. Fix: hard iteration cap, cost-per-prospect budget cap, fall back to a workflow fallback that produces a competent default email without unbounded exploration.

**The description-bleed in MCP.** A team exposes tools through MCP. One tool's description says "USE THIS TOOL FIRST." Another MCP server's tool, from a different vendor, has a description that contradicts it. The agent loops between the two tools, each description pulling it in a different direction. This is the cross-server shadowing case documented in 2025 security writeups.[^16] Fix: curate the tool set exposed to any single agent scope; do not trust third-party descriptions blindly.

## Open questions / what's not settled

**Is MCP the long-term winner, or a transitional protocol?** Thoughtworks and the Linux Foundation adoption trajectory argue yes.[^14] The security writeups, the context-token cost of large server tool lists, and the fact that most production agents still call direct SDK for the irreversible tools argue the protocol will fork or mature significantly in the 2026–2027 window.[^16] Operator position: bet on MCP for read-only and composable cases; keep direct SDK for the send/write-CRM tools through 2026.

**Do orchestrator-workers + evaluator-optimizer actually replicate autonomous gains?** The Schluntz/Zhang claim is effectively yes — that workflows cover most of the value of agents with better control.[^1] Cognition's Devin post-mortem supports this for software engineering.[^18] But Sierra's Ghostwriter and the OpenAI Operator / Anthropic Claude Code agentic coding experiments suggest there are tasks where the autonomous loop is a real capability unlock, not just a control-loss. The unsettled question is the *size* of the autonomous-only region and whether it grows or shrinks as models improve.

**Does τ-bench retail pass^8 at <25% transfer to sales-agent pass^k at typical daily volume?** Not directly — τ-bench is a specific simulated workload. But the *shape* of the finding (multi-turn reliability collapses relative to single-turn) is expected to transfer qualitatively. Open question: what is the actual pass^k curve for a production sales-agent at 100, 500, 2000 sessions per day? No vendor has published honest numbers. Until they do, the operator default is to treat every autonomous agent decision as suspect above a price threshold and route it to human review.

## Reviewer lens — named critics with specific disagreements

- **Erik Schluntz and Barry Zhang (Anthropic, authors of Building Effective Agents).** They would push back on this lesson's framing that "autonomous is almost nowhere" for sales agents. Their own post is careful: *"some tasks need the flexibility of dynamic decision-making, and you shouldn't avoid agentic systems when they are the right fit."*[^1] They would specifically push back on the Layer 1 paragraph that says autonomous fits "almost nowhere" — they would say "at high token-per-task ratios with human review, autonomous fits more sub-problems than this lesson concedes." Fair critique; the lesson errs toward workflow-first for a reader who is building their first production agent.

- **Harrison Chase (LangChain, LangGraph).** He would push back on the MCP-vs-direct-API framing that defaults to direct SDK. His 2025 Deep Agents position argues that outsourcing the agentic runtime (state, checkpointing, observability) is the right move and that LangGraph-style orchestration — which does wrap tool APIs — is underweighted here.[^3] The counter on his view: LangGraph the runtime is different from MCP the protocol; the lesson conflates the two. Valid — we simplified for the operator audience. A reader who is going to run LangGraph should read Harrison's context-engineering post before picking either.

- **Shunyu Yao (τ-bench first author).** He would push back on the Layer 2 reading that pass^k<25% on retail means "don't deploy multi-turn sales agents." His more precise position from the τ-bench paper and follow-up τ²-bench work is that the variance is informative: it tells you *where* to invest evaluation and scaffolding, not that the system is unusable.[^8] Fair — the lesson could be read as too defeatist about multi-turn. The corrective is: pass^k low means evaluate more, not deploy less.

- **Lilian Weng (LLM Powered Autonomous Agents, 2023, updates 2024–2025).** Her framing of agent = LLM + memory + planning + tool use would push back on the lesson's near-absence of the memory layer.[^22] The Anthropic post doesn't emphasize memory either, and the lesson inherited the gap. The reviewer-fair answer is that memory for a sales agent is handled outside the LLM loop (the CRM is the memory, the agent reads and writes), but for the autonomous-research sub-problem, short-term working memory inside the loop is its own design question.

- **Boris Cherny (Claude Code, Anthropic).** He would push back on the tool-schema defaults in Layer 3 — specifically that the lesson underuses Anthropic's 2025 advanced tool-use features: tool_search_tool (for >100-tool surfaces), programmatic tool calling, and tool-use examples.[^2] A sales agent scaling to 20+ tools should probably use tool_search_tool rather than namespace-and-prune; the lesson's "stay at ≤6 tools per scope" is an honest 2024 heuristic and the 2025 advanced features partly relax it.

- **Douwe Kiela (Contextual AI).** He would push back on the sharp separation between "tool-calling" and "retrieval" in this lesson. His Contextual AI position is that retrieval *is* a tool call in the agentic setting, and that the architecture patterns for retrieval agents (agentic RAG, we cover Friday) are the same architecture patterns as sales agents — it is not two disciplines, it is one. Fair; the lesson treats them as adjacent rather than overlapping, and Thursday/Friday integrate them more fully.

## Further reading

**Must (read this week, before Wednesday's lesson):**

1. Schluntz, E., Zhang, B. "Building Effective Agents," Anthropic research blog, December 19, 2024. https://www.anthropic.com/research/building-effective-agents — the whole post, slowly.[^1]
2. Yao et al. "τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains," arxiv 2406.12045, June 2024. Read the abstract, §3 (evaluation protocol), and §5 (results table).[^8]
3. Anthropic Applied AI Team, "The 'think' tool: Enabling Claude to stop and think," Anthropic engineering blog, March 2025.[^10]

**Recommended:**

4. Weng, L. "LLM Powered Autonomous Agents," lilianweng.github.io, June 2023 — the planning/memory/tool-use framework remains load-bearing.[^22]
5. Patil et al. "The Berkeley Function Calling Leaderboard (BFCL): From Tool Use to Agentic Evaluation of Large Language Models," PMLR 2025. https://gorilla.cs.berkeley.edu/leaderboard.html — read the V4 methodology section.[^6][^7]
6. Model Context Protocol specification 2025-11-25. https://modelcontextprotocol.io/specification/2025-11-25 — skim the spec, then read the community blog "One Year of MCP" for context.[^12][^13]
7. Willison, S. "Model Context Protocol has prompt injection security problems," simonwillison.net, April 2025 — read the whole piece before you ship an MCP server in production.[^15]

**Optional (but clarifying):**

8. Yao et al. "ReAct: Synergizing Reasoning and Acting in Language Models," arxiv 2210.03629 (ICLR 2023) — the origin of tool-use loops, still cited because nothing has replaced the idea, only refined it.[^23]
9. Cognition, "Devin's 2025 Performance Review: Learnings From 18 Months of Agents At Work," cognition.ai/blog, 2025 — read as an honest post-mortem on the autonomous-agent pitch.[^18]
10. Chase, H. "Why you should outsource your agentic infrastructure but own your cognitive architecture," LangChain blog, 2025.[^3]

## Citations

[^1]: Schluntz, E. and Zhang, B. "Building Effective Agents." Anthropic research blog, December 19, 2024. https://www.anthropic.com/research/building-effective-agents — source for the workflows-vs-agents definitions and all five workflow patterns quoted in Layer 1 and throughout.

[^2]: Anthropic documentation. "Tool use with Claude" and "Introducing advanced tool use on the Claude Developer platform." Verified April 2026 at https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview and https://www.anthropic.com/engineering/advanced-tool-use — source for schema best practices, description field importance, namespacing, tool_search_tool, programmatic tool calling, tool-use examples (all 2025 advanced features).

[^3]: Chase, H. "Why you should outsource your agentic infrastructure but own your cognitive architecture." LangChain blog, 2025. https://www.langchain.com/blog/why-you-should-outsource-your-agentic-infrastructure-but-own-your-cognitive-architecture — source for the infrastructure-vs-cognitive-architecture distinction referenced in Layer 1. Deep Agents appears as a LangChain product on the same page; the orchestrator-workers-as-subagents pattern is developed further in LangChain's "Running Subagents in the Background" companion post linked from this piece.

[^4]: Husain, H. parlance-labs.com evaluation-driven-development writing, 2024–2025, referenced from Saturday's RAG-evaluation lesson — cited here for the evaluator-optimizer rubric discipline in Layer 1.

[^5]: Anthropic. "Raising the bar on SWE-bench Verified with Claude 3.5 Sonnet." Anthropic news, October 2024. https://www.anthropic.com/news/swe-bench-sonnet — source for the 49% SWE-bench Verified result with a two-tool (Bash + Edit) agent architecture; source for the minimal-scaffolding design philosophy cited in Layer 3 and Operator Case 2.

[^6]: Berkeley Function-Calling Leaderboard V4. https://gorilla.cs.berkeley.edu/leaderboard.html — public leaderboard and dataset cards, verified April 2026.

[^7]: Patil, S. et al. "The Berkeley Function Calling Leaderboard (BFCL): From Tool Use to Agentic Evaluation of Large Language Models," Proceedings of Machine Learning Research 2025 (also ICML 2025 poster). https://proceedings.mlr.press/v267/patil25a.html — source for the split-personality quote in Layer 2 about single-turn vs multi-turn reliability.

[^8]: Yao, S., Shinn, N., Razavi, P., Narasimhan, K. "τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains." arxiv 2406.12045, June 2024. https://arxiv.org/abs/2406.12045 — source for the pass^8 <25% retail finding in Layer 2 and the pass^k metric discussion.

[^9]: Sierra Research blog. "τ-bench: shaping the development and evaluation of agents." 2024. https://sierra.ai/blog/tau-bench-shaping-development-evaluation-agents — source for the Yao et al. commentary cited in Layer 2 on the seams between tools being where reliability is lost.

[^10]: Anthropic Applied AI Team. "The 'think' tool: Enabling Claude to stop and think." Anthropic engineering blog, March 2025. https://www.anthropic.com/engineering/claude-think-tool — source for the τ-bench pass^1 improvement from 0.370 to 0.570 on airline with the think tool, cited in Layer 2 and Operator Case 4.

[^11]: Anthropic. "Introducing the Model Context Protocol." Anthropic news, November 25, 2024. https://www.anthropic.com/news/model-context-protocol — source for MCP launch date, initial SDKs, reference-server list.

[^12]: Model Context Protocol specification, version 2025-11-25. https://modelcontextprotocol.io/specification/2025-11-25 — source for the tasks abstraction and revised auth flows in the spec's second major version.

[^13]: Model Context Protocol blog. "One Year of MCP: November 2025 Spec Release." https://blog.modelcontextprotocol.io/posts/2025-11-25-first-mcp-anniversary/ — source for the MCP Registry reaching "close to two thousand entries" by September 2025 (407% growth from initial onboarding), one-year ecosystem growth narrative, and the testimonial support from representatives at OpenAI, Google, Microsoft, and AWS noting platform integration. Finer-grained counts (8M+ downloads, 5,800+ servers, 300+ clients) are not in this post; treat those as approximate and sourced from aggregated community trackers cross-referenced in the lesson body.

[^14]: Thoughtworks. "The Model Context Protocol's impact on 2025." https://www.thoughtworks.com/en-us/insights/blog/generative-ai/model-context-protocol-mcp-impact-2025 — source for the framing of MCP as a foundational open-source standard that has "played a significant role in driving AI adoption" by enabling richer agentic context. The specific "lingua franca" language is this lesson's characterization of that ecosystem-enabler framing in Position A of Layer 4.

[^15]: Willison, S. "Model Context Protocol has prompt injection security problems." simonwillison.net, April 9, 2025. https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/ — source for the prompt-injection vulnerability analysis and the quote in Layer 4.

[^16]: Scalifi AI Blog. "Six Fatal Flaws of the Model Context Protocol (MCP)." https://www.scalifiai.com/blog/model-context-protocol-flaws-2025 — source for the six-category MCP flaw taxonomy: (1) weak foundations / security not a primary design concern, (2) communication vulnerabilities (session IDs in URLs, no message signing), (3) prompt injection & tool manipulation via malicious tool descriptions, (4) shared-context-space data-handling issues enabling remote poisoning, (5) governance and tool-risk categorization gaps, (6) architectural limitations of stateful text-only communication. Specific quantifications referenced in the lesson body (Postmark breach, 43% OAuth flaw rate, 40K-token context tax) are drawn from linked community incident reports cited in the same piece.

[^17]: Cognition. "Introducing Devin, the first AI software engineer." cognition.ai/blog, March 2024. https://cognition.ai/blog/introducing-devin — source for the original Devin positioning cited in Layer 5 Position A.

[^18]: Cognition. "Devin's 2025 Performance Review: Learnings From 18 Months of Agents At Work." cognition.ai/blog, 2025. https://cognition.ai/blog/devin-annual-performance-review-2025 — source for Cognition's own reframing of Devin's realistic positioning as "junior execution at infinite scale" and "senior intelligence on demand," plus the documented competency gaps around ambiguous requirements, scope changes, and soft skills. The "enthusiastic interns" phrasing in Layer 5 Position B / Operator Case 3 paraphrases this junior-execution-at-scale framing.

[^19]: Futurism. "The 'First AI Software Engineer' Is Bungling the Vast Majority of Tasks It's Asked to Do." October 2024. https://futurism.com/first-ai-software-engineer-devin-bungling-tasks — source for the Devin real-task failure reporting cited in Layer 5 Position B.

[^20]: Sierra. "About Sierra." https://sierra.ai/about — source for named Sierra customers including CLEAR, Casper, and Minted with testimonials supporting the policy-bounded agent-for-support framing cited in Operator Case 1. Additional Sierra customer names referenced in the lesson body (WeightWatchers, Sonos, SiriusXM, Deliveroo, Discord, Ramp, Rivian, SoFi, Tubi, Cigna, ADT, Bissell, Vans) come from Sierra's customers subpage and third-party coverage (including TechCrunch [^21]) rather than the About page specifically.

[^21]: TechCrunch. "Bret Taylor's Sierra reaches $100M ARR in under two years." November 21, 2025. https://techcrunch.com/2025/11/21/bret-taylors-sierra-reaches-100m-arr-in-under-two-years/ — source for the $100M ARR in 21 months from February 2024 launch figure and the $10B valuation from the September 2025 round cited in Layer 5 and Operator Case 1.

[^22]: Weng, L. "LLM Powered Autonomous Agents." lilianweng.github.io, June 23, 2023. https://lilianweng.github.io/posts/2023-06-23-agent/ — source for the Agent = LLM + memory + planning + tool use framework cited in the Reviewer Lens.

[^23]: Yao, S. et al. "ReAct: Synergizing Reasoning and Acting in Language Models." ICLR 2023, arxiv 2210.03629. https://arxiv.org/abs/2210.03629 — source for the tool-use reasoning-action interleaving pattern referenced in the Further Reading list.
