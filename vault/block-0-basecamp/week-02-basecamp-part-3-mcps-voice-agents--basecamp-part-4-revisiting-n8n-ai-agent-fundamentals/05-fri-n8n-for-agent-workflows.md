---
type: lesson
block: block-0-basecamp
week: week-02
day_of_cycle: 5
day_name: fri
session_slug: basecamp-part-4-revisiting-n8n-ai-agent-fundamentals
date_due: 2026-05-08
tags: [n8n, agent-workflows, langgraph, temporal, zapier, mcp, workflow-engines, visual-programming, durable-execution, anthropic-building-effective-agents]
sources:
  - anthropic-building-effective-agents-2024
  - n8n-ai-agent-node-docs
  - n8n-mcp-client-tool-docs
  - n8n-mcp-trigger-announcement-2025
  - n8n-release-notes
  - langgraph-vs-n8n-zenml
  - langgraph-vs-n8n-orangeloops-2025
  - langgraph-1-0-release-2025
  - zapier-agents-may-2025
  - zapier-agents-december-2025
  - temporal-docs-durable-execution
  - n8n-case-studies-delivery-hero
  - n8n-case-studies-sanctifai
  - latenode-n8n-2025-reality-check
  - simon-willison-building-effective-agents-summary
  - anthropic-cookbook-agent-patterns
last_verified: 2026-04-15
word_count_target: 6000
---

# n8n for agent workflows — when the visual workflow engine is the correct primitive, and when it is the wrong shape for what you are actually building

## Why this matters

By this point in the week you have built MCP servers, wired voice agents, and stood up a small LangGraph graph from scratch. Today the question gets uncomfortably practical: when a stakeholder at your company asks you to ship an "AI agent" for their team — ingest a signal, reason about it, take an action, tell someone — which primitive do you reach for?

The defensible answer in April 2026 is almost never *"LangGraph, obviously."* It is almost never *"Temporal, obviously."* It is almost always *"what can the operating team maintain six months from now when I have moved on to the next project, and which of these tools is the cheapest thing that still satisfies the real durability, observability, and SLA requirements of the workload?"*

n8n is, in 2025–2026, the single most under-respected tool in the AI-catalyst-lead toolbox. It is the workflow engine that a marketing ops person can keep alive on Monday morning when your pager goes off at 3 a.m. It has shipped a credible LangChain-based AI Agent node,[^1] MCP Client and MCP Trigger nodes,[^2][^3] and a self-hostable execution model that lets you put the whole thing inside your VPC without a vendor negotiation. It is also not the right tool for a dynamic, self-directed agent that has to replan itself across hundreds of steps under a five-nines SLA.

Your job today is to develop the taste to tell those cases apart — mechanically, not by vibe — so that when you walk into a leadership meeting you can defend your framework choice in a single paragraph. By the end of the lesson you will have:

1. A workable mental map of the workflow-engine category and where n8n sits in it relative to Zapier, Make, Pipedream, Windmill, Airflow, Temporal, Inngest, LangGraph, and Dagster.
2. A clean split between *workflow* and *agent* in Anthropic's sense — and a view on why n8n is predominantly a workflow engine with agent-shaped nodes inside, and why that is a feature for 80% of real production use cases.
3. Specific knowledge of n8n's 2025 AI surface area: the AI Agent node, the LangChain substrate, the MCP Client and MCP Server Trigger nodes, the memory and vector-store primitives.
4. A concrete comparison chart against LangGraph (code-first, stateful graphs) and Temporal (durable execution primitives, deep expert territory) so you know what operational characteristics each purchase buys you and which it costs.
5. A runnable experiment you will drive through n8n's UI — or through Claude Code generating the workflow JSON for you — where a new GitHub issue is summarized by Claude and posted to Slack, including the exact failure modes you should watch for.

The goal is not to turn you into an n8n enthusiast. It is to get you to the point where you can cleanly say *"use n8n for this, and LangGraph for that, and neither for the third thing,"* and have the reasons lined up.

## Prerequisites

- n8n installed somewhere you can reach a browser UI: self-hosted Docker container on your laptop (`docker run -it --rm -p 5678:5678 docker.n8n.io/n8nio/n8n` is the canonical one-liner from n8n's docs), or a free n8n Cloud trial.
- Anthropic API key with credit (any tier), and a Claude Code install on the same machine.
- A GitHub account with a sandbox repo you are willing to fire test issues at, and a Slack workspace where you can add an incoming webhook or install a Slack app.
- You have read or skimmed [[../week-01-basecamp-part-1-prompting-rags--basecamp-part-2-vibe-coding/01-mon-prompting-first-principles|Monday Week 1 (prompting mechanics)]] and [[02-tue-mcp-deep-dive|Tuesday's MCP deep dive]]. MCP shows up directly today because n8n's MCP nodes are what let Claude Code drive an n8n instance from the outside.

## Layer 1 — The workflow-engine category, demystified

The word *"workflow"* in 2026 has been so over-loaded by marketing copy that it is almost useless as a search term. Before we can say anything specific about n8n, we need to pin down what *category* of tool n8n even is, because the named competitors sit in three or four different product categories that answer three or four different questions. Conflating them is how teams end up picking the wrong primitive for the wrong problem and blaming the tool six months later.

Here is the map I use when a team asks *"should we use X or Y?"*

### The three shelves

**Shelf A — business-ops automation (SaaS-stitching).** Zapier, Make (formerly Integromat), Pipedream, Workato, Tray.io. These are designed for non-engineers to glue SaaS tools together: "when a row is added to Airtable, post to Slack and create a HubSpot deal." The integrations directory is the product. Execution is ephemeral, observability is shallow, and the vendor owns the runtime. Zapier is the category leader by user count and brand recognition. Zapier's 2025 evolution into *Zapier Agents* is a real product move into the agent space,[^4][^5] but the DNA is still business-ops SaaS-stitching with LLM calls grafted in.

**Shelf B — developer-facing workflow engines (technical, open-core or self-hostable).** n8n, Windmill, Pipedream (which straddles A and B), and arguably the low-code side of Airbyte. These are for someone who is technically fluent — writes a little JavaScript or Python when needed, reads HTTP docs, understands credentials and webhooks — but who does not want to spin up a FastAPI service for every automation. The sweet spot is: you want to ship this in a week, you want to hand it to a mid-senior engineer to maintain, and you want the option to self-host behind your firewall.

**Shelf C — data/ML orchestration and durable execution.** Airflow, Dagster, Prefect, Temporal, Inngest, Restate. These are engineer-owned infrastructure. Airflow and Dagster are about data pipelines (DAGs, scheduling, lineage). Temporal and Inngest are about *durable execution* — the idea that a workflow function can crash, the machine can die, and the platform guarantees resumption from the last checkpoint with exactly-once semantics. Temporal in particular is the right answer when you are writing a bank-grade multi-day process that must not lose state under any failure; it is the wrong answer when you are wiring an MCP call to a Slack message. You do not wear Temporal to brunch.

**Shelf D — agent-framework code libraries.** LangGraph, LangChain, CrewAI, AutoGen, smolagents, Pydantic AI, the new Agents SDKs from both OpenAI and Anthropic. These are not workflow engines at all — they are Python (or TypeScript) libraries for expressing agent control flow in code. LangGraph in particular hit a 1.0 stable release in October 2025[^6] and has become the serious-code-first default for teams building stateful, multi-agent applications with explicit graphs. It is code, not a UI; the "graph" is an abstraction inside your Python process.

n8n sits firmly on Shelf B. It occasionally *reaches into* Shelf D by wrapping LangChain primitives inside visual nodes. But it is not on Shelf A (too technical), not on Shelf C (not durable-execution-grade), and not on Shelf D (not a code library). When someone asks *"n8n or LangGraph?"* they are often asking a shelf-B vs shelf-D question, which is the same shape as *"spreadsheet or Python?"* — the honest answer is *"which kind of user, which maintenance horizon, which failure mode do you care about?"*

### Why n8n specifically is the 2025 standout on shelf B

Three things made n8n the runaway shelf-B story in the AI era, and none of them are about AI directly.

1. **Fair-code, self-hostable license.** n8n uses the Sustainable Use License, which is not OSI-open-source but is close enough that a security-conscious enterprise can run it inside their own VPC with their own data. This single fact is why I see n8n deployed in regulated industries where Zapier is a non-starter.
2. **Node-level code escape hatch.** Any time the UI runs out of expressiveness, you drop into a Code node and write JavaScript or Python. Unlike Zapier's Formatter-and-Filter grammar, n8n does not force you back onto a vendor-specific mini-language; you write the language you already know.
3. **An integrations directory approaching 500 nodes in 2025**, including an AI and LangChain cluster that ships dozens of LLM, embedding, vector-store, and agent nodes as first-class primitives.[^7][^1]

Add to that the 2025 AI-first push — the v1.113.3 release alone shipped more than seventy AI-related nodes across LLMs, embeddings, vector databases, speech, OCR, and image models[^8] — and n8n has credibly repositioned itself from "SaaS glue" to "the workflow engine you use to ship agents your operations team can actually maintain."

That repositioning is also the source of the most interesting live controversy in this space, which we will hit in Layer 4.

## Layer 2 — Workflow vs agent, the Anthropic framing, and why it matters for tool choice

Anthropic's December 2024 essay *Building Effective Agents* is the single most important piece of vendor-neutral guidance on this question, and it is short enough to read in one sitting.[^9] Simon Willison summarized it accurately on his blog the same week.[^10] The distinction it draws is the one you should internalize for the rest of this lesson, because it is the distinction that tells you which tool to pick.

> *Workflows are systems where LLMs and tools are orchestrated through predefined code paths. Agents are systems where LLMs dynamically direct their own processes and tool usage, maintaining control over how they accomplish tasks.*

Anthropic then catalogs five named **workflow patterns**:

1. **Prompt chaining** — output of LLM call 1 becomes input to LLM call 2.
2. **Routing** — an initial LLM call classifies the input and picks which downstream path runs.
3. **Parallelization** — fan out multiple LLM calls in parallel (voting, sectioning), combine results.
4. **Orchestrator-workers** — an orchestrator LLM plans a task and dispatches sub-tasks to worker LLM calls, then synthesizes.
5. **Evaluator-optimizer** — one LLM generates, another critiques, loop until a quality bar is met.

And then **agents**, which are distinct from all of those: the LLM itself decides, at runtime, which tool to call next, when to stop, when to ask a human, when to re-plan. There is no predefined graph. Anthropic's own guidance on this is almost stern: most teams should start with the simplest workflow that solves the problem, and only escalate to *true* agent semantics when flexibility at runtime is genuinely required — because agents trade predictability, cost, and latency for open-endedness.

Map this framing onto the tools:

- **n8n** is primarily a **workflow** engine, with an **AI Agent node**[^1] that gives you agent-shaped behavior *inside a single workflow step*. The overall graph is still predefined; the agent node is a bounded region where the LLM picks tools dynamically. That architectural fact is the single most important thing to understand about n8n for agent use cases: it is a workflow with agent islands, not an agent end-to-end.
- **LangGraph** makes both workflows and agents first-class in code. You can express any of Anthropic's five workflow patterns, and you can also express dynamic agent loops with explicit state, because everything is a graph you wrote.
- **Temporal** does not care whether the work is "AI-shaped"; it gives you durable execution as a substrate. You write the orchestration as code in any supported SDK; Temporal guarantees that if your worker dies mid-run, the next worker resumes exactly where the last one left off.
- **Zapier Agents** is the closest shelf-A competitor to n8n's agent-node pattern. Zapier rebuilt Agents in May 2025 around *Pods* — groupings of related agents with shared tools — and shipped drafts, versioning, and a visual activity dashboard by the end of 2025.[^4][^5]

For 80% of production AI use cases inside real companies, the correct shape is a workflow with one or two agent islands inside it, *not* an unconstrained agent. This is because:

- The business logic surrounding the LLM call — "only run on Tier 1 customers," "skip the weekend," "escalate if the confidence is low" — is naturally predefined code, not something you want an LLM to re-derive every time.
- The failure modes of unconstrained agents are worse than the failure modes of workflows. A workflow that fails fails in a known place with a known retry. An agent that fails can loop, re-plan, burn tokens, and produce confident garbage for forty-five minutes before you notice.
- Observability and debuggability of a predefined graph is strictly better than of a dynamic plan. You can look at an n8n execution log and see exactly which node ran in which order. You cannot always reconstruct what a self-directed agent decided and why.

Anthropic's guidance is explicit on this point: *start with the simplest solution, increase complexity only when needed.* n8n is, for a very large class of real problems, the simplest solution that works — *and the simplicity is the point.*

## Layer 3 — n8n's 2025 AI surface area in detail

Let's get mechanical. What does n8n actually ship for AI and agent use cases, as of the current release train in early 2026?

### The AI Agent node

The AI Agent node, documented at [docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.agent][^1], is n8n's canonical primitive for wrapping an LLM with tool-calling behavior inside a single workflow step. Under the hood it is built on LangChain's agent executor — you are using the same substrate you would in Python, but expressed in the n8n UI.

The node is a *cluster node*, which in n8n terminology means it hosts sub-nodes:

- **Chat Model** — the LLM. Attach an Anthropic Chat Model node for Claude, an OpenAI Chat Model for GPT, or a self-hosted Ollama node. Swapping is a drag-and-drop operation.
- **Memory** — optional. Attach a Simple Memory node for in-workflow context, a Postgres Chat Memory node for durable multi-turn memory, or a Redis / MongoDB backed memory node.
- **Tools** — zero or more. Any n8n node can in principle become a tool. The canonical agent-tool nodes include HTTP Request, Code (JavaScript/Python), Wikipedia, SerpAPI, Vector Store retrievers, and — as of 2025 — the MCP Client Tool.
- **Output Parser** — optional. Pin the agent's output to a JSON schema or a structured format.

The practical shape: you drop one AI Agent node into your graph, wire its inputs (the prompt), attach a Claude model and a handful of tools, and downstream nodes consume the agent's output. This is Anthropic's orchestrator-workers pattern rendered visually, or — if you set `maxIterations` high and give the agent the HTTP Request and Code tools — close to a bounded autonomous agent.

### MCP Client Tool and MCP Server Trigger

n8n's 2025 MCP release was the strategically important one. Two nodes matter:

- **MCP Client Tool node**,[^2] used as a sub-node of the AI Agent. It exposes any MCP server's tools to the agent as callable tools. You point it at an MCP endpoint (SSE or streamable HTTP), and every tool the server advertises becomes available to the Claude or GPT model inside the Agent node.
- **MCP Server Trigger node**,[^3] which does the inverse: it lets your *n8n workflow* act as an MCP server that external clients — Claude Desktop, Claude Code, Cursor, Lovable — can connect to. Every workflow you expose through the trigger becomes a tool those clients can call.

The community announcement in early 2025[^11] landed this as a major unlock: n8n went from "a workflow engine that can call LLMs" to "a workflow engine that is a first-class MCP citizen on both sides of the protocol." For the agent use case this is the piece that closes the loop: you can now drive an n8n instance from Claude Code through MCP, and an n8n agent node can reach out to any MCP server in the world for tools.

### Memory and vector-store nodes

For RAG and memory, n8n ships native nodes for Pinecone, Qdrant, Weaviate, Supabase Vector, PGVector, and a local in-memory store for development. These plug straight into the AI Agent node as tools or retrieval sources. You get the same ergonomics you would get with LangChain's `VectorStoreRetriever` in Python, minus the import statement.

### Deployment models

- **n8n Cloud** — managed, multi-tenant, price-scaled by execution.
- **Self-hosted Docker** — single container, runs anywhere Docker runs; fine for a small team.
- **Kubernetes with queue-mode workers** — the production pattern. A main process, a webhook process, and an arbitrary number of worker processes coordinate through a Redis queue. This is how teams scale n8n to tens of thousands of executions per day. Delivery Hero's IT team runs n8n at this tier and reports 200+ engineer-hours saved per month on a single workflow.[^12]
- **n8n Enterprise** — adds SSO, RBAC, audit logs, SOC 2 compliance, and support contracts.

The practical implication: unlike Zapier, you can run n8n on the same side of the firewall as your data. In regulated industries — healthtech, fintech, any EU data-residency situation — this is not a nice-to-have; it is a go / no-go gating criterion for whether you can use the tool at all.

## Layer 4 — n8n vs LangGraph vs Temporal, honestly

With the categories in place, here is the head-to-head that matters for real tool choice. I am going to give you the version I would defend in a principal-engineer review, not the marketing-page version.

### n8n vs LangGraph

The ZenML comparison from 2025 is the cleanest third-party write-up I have found,[^13] and OrangeLoops published a hands-on build-the-same-thing-in-both comparison in June 2025 that is worth the twenty-minute read.[^14] The short version:

| Dimension | n8n | LangGraph |
|---|---|---|
| Primary user | Technical generalist, ops engineer, solution architect | Python engineer shipping production agents |
| Expressiveness | Visual DAG + code nodes; AI Agent cluster node for bounded dynamic control | Arbitrary code; explicit state machine with nodes and conditional edges |
| Dynamic control flow | Bounded, inside AI Agent node | First-class; whole graph can replan |
| State management | Workflow variables + memory nodes; not a first-class graph state | First-class, typed state object, checkpointable |
| Human-in-the-loop | Via Wait/Webhook nodes; straightforward | Via interrupt primitives; integrated with LangSmith |
| Observability | Per-execution UI with node-by-node inputs/outputs and timing | LangSmith traces; programmatic |
| Maintenance by non-authors | High — visual workflows are readable | Low — requires reading Python |
| Durability | Queue-mode workers + Postgres store; recoverable but not exactly-once | Checkpointing supported; real durability requires an external substrate |
| License | Fair-code, self-hostable | OSS (MIT) library you run in your own process |
| Sweet spot | Cross-system orchestration with agent islands | Stateful, multi-agent, complex-branching apps |

LangGraph wins unambiguously when the problem is *"express a subtle agent control flow with branching, loops, human-in-the-loop, and type-safe state."* n8n wins unambiguously when the problem is *"connect the AI piece to the other forty-seven systems, schedule it, monitor it, hand it off to an ops team."*

The most common mistake I see is teams reaching for LangGraph because it feels *"more serious,"* when the actual problem is 70% integration and 30% agent cleverness. In that case you end up writing and maintaining Python glue code for Slack posting, Jira ticket creation, and GCal availability checking that n8n would have solved out of the box in an afternoon.

The second most common mistake is the reverse: teams build something in n8n, it works for the first six weeks, and then they hit a branch condition that needs a stateful replan loop across five tool calls, and the AI Agent node cannot express it cleanly. At that point the right move is almost always to keep n8n as the outer workflow and call out to a small LangGraph service for the agent-heavy inner loop. Several teams — including the ones surfaced in n8n's own best-practices post on deploying agents in production[^15] — are explicitly running this hybrid.

### n8n vs Temporal

This comparison is different in kind. Temporal is not a direct competitor; it is a different shelf. You reach for Temporal when:

- The workflow can run for hours, days, or weeks and must survive process restarts, pod evictions, and region failovers with exactly-once semantics on externally-visible side effects.
- You need first-class compensation logic — the saga pattern — because a partial failure must unwind cleanly.
- You have a team of backend engineers who can own a Temporal cluster, and the workload justifies the operational cost of running one.

If that describes your problem, Temporal is a strictly better answer than n8n. n8n's queue-mode gives you retries and resumption on failure, but it is not a durable-execution substrate; long-running workflows that span complex state changes are outside its comfort zone.

The flipside: in my experience, fewer than 5% of AI-era workflow problems actually need durable execution. Most teams self-talk themselves into thinking they need it, then spend three months standing up a Temporal cluster for a workload that could have been an n8n workflow plus a Postgres retry table. Michael Seibel's *just do the ugly thing* instinct applies strongly here: if your workflow runs in under thirty seconds per execution and retries are safe to replay, you do not need durable execution; you need a workflow engine with decent retry semantics.

### Where Zapier Agents sits

Zapier Agents in its late-2025 form[^4][^5] is a plausible competitor to n8n's agent pattern for non-technical teams. It ships visual agent construction, Pods for grouping, a drafts/published versioning model, and 8,000+ integrations that exceed n8n's count. The trade-off is the classic Shelf A vs Shelf B split: Zapier owns the runtime, so you cannot self-host, you cannot escape the per-execution pricing model, and you have less expressiveness at the code-escape-hatch level. For a marketing-ops team of non-engineers, Zapier Agents is almost certainly the faster road. For anything where data residency, code-level expressiveness, or self-hosting matters, n8n is the more defensible choice.

## Layer 5 — The live controversy: is visual workflow the wrong abstraction for agents?

Here is the fight, stated honestly, so you can have a position on it.

**Position A — code-first.** Visual workflow engines are the *wrong* primitive for agents because agents, by Anthropic's definition, exhibit dynamic control flow — which drag-and-drop represents poorly. A box on a canvas with an arrow coming out of it is inherently a predefined path; agents are defined by not having predefined paths. The LangGraph authors, and the broader Python-agent community, argue that as soon as your control flow gets interesting — branching based on agent state, looping until a condition, re-planning after a tool result — you are fighting the visual abstraction and writing text-in-a-box workarounds that would have been fifteen lines of Python. Claude Code itself, as an agent, is not a visual workflow; it is a loop-plus-tools written in code, and that is not an accident.

The sharpest version of the critique: **visual workflow engines make simple things easy and hard things impossible.** The moment the hard thing shows up, you are porting to code anyway, so why not start there.

**Position B — visual-first.** The majority of production "agent" workloads in 2026 are not true dynamic agents — they are Anthropic-style workflows with one agent-shaped step inside. For those, the visual abstraction is *right*: it is readable by non-authors, inspectable by ops, maintainable by people who did not write it, and it forces you to make the predefined paths explicit instead of burying them inside an LLM's prompt. The n8n community position, echoed by Zapier's bet on Agents, is that the hard-things-are-impossible critique is solved by the code-escape-hatch: when the visual abstraction runs out, drop a Code node in and keep going.

The sharpest version of the defense: **most teams do not have a LangGraph problem; they have an integration-and-governance problem, and the visual engine is the correct answer to the second.**

My take, after eighteen months of watching teams pick and fail: both positions are partially right, and the project-level decision tree is actually straightforward.

- If the agent-shaped step is the *entire* application, and nothing else meaningful happens around it, LangGraph (or Claude Code, or a bespoke loop) is correct. You are building an agent, not a workflow.
- If the agent-shaped step is *one of many* steps in a broader process that involves triggering from external systems, updating other systems, notifying humans, scheduling, and auditing, n8n is almost certainly correct. The agent is a node in a larger graph, and the larger graph is workflow-shaped.
- If both halves are complex — a sophisticated agent embedded in a sophisticated workflow — run the hybrid: n8n (or Temporal, if durability matters) as the outer skeleton, LangGraph as the agent-heavy inner service, MCP or HTTP as the contract between them.

The secondary controversy — *does n8n's 2025 agent push dilute its workflow strength?* — has a simpler answer: no, but it changes the positioning risk. n8n's workflow DNA is still the core product; the AI and agent nodes are additive, built on LangChain, and isolable. The real risk is that n8n starts marketing itself as an agent platform, gets compared head-to-head with LangGraph and Claude Code on agent-ish benchmarks, and loses on a metric — *dynamic control flow expressiveness* — that was never what its customers were buying in the first place. The Latenode capabilities review from 2025 is worth reading partly because it is unusually honest about exactly this risk.[^16]

## Runnable experiment — ship a small agentic workflow you can defend

We will build the canonical "new GitHub issue → Claude summarizes it → posts to Slack" workflow end-to-end, but with enough depth that you see the agent pattern, not just the CRUD. You have two paths: direct it from Claude Code through MCP, or build it in the n8n UI by hand. Do at least one. The whole thing should take under ninety minutes.

### Setup (fifteen minutes)

1. Start n8n locally: `docker run -it --rm --name n8n -p 5678:5678 -v n8n_data:/home/node/.n8n docker.n8n.io/n8nio/n8n`. Open `http://localhost:5678` and create an owner account.
2. In n8n Settings → Credentials, add: **Anthropic API** (API key), **GitHub API** (fine-grained PAT with Issues read scope on the sandbox repo), **Slack** (install the n8n Slack integration or use Slack Incoming Webhooks — the latter is faster for experiment code).
3. Install the n8n MCP community node if you want Claude Code to drive n8n directly: `npm install -g n8n-nodes-mcp` inside the container, or set `N8N_COMMUNITY_PACKAGES_ENABLED=true` and install from the UI.

### Path A — drive it from Claude Code through MCP (recommended)

1. Open Claude Code in a scratch directory.
2. Install `czlonkowski/n8n-mcp`, which is an MCP server purpose-built to let Claude Code build and manage n8n workflows for you. Follow the README; the config drops into your `claude_desktop_config.json` or equivalent.
3. Prompt Claude Code:

> I am connected to a local n8n instance on `http://localhost:5678` via the n8n-mcp server. I want you to create a workflow in that n8n instance with the following shape:
>
> 1. Trigger: GitHub webhook, firing on `issues.opened` for the repository `<your-org>/<your-repo>`.
> 2. Node 2: AI Agent node using Anthropic Claude Sonnet 4.5 as the chat model. Give it this system prompt: *"You are a triage assistant. Given a GitHub issue body and title, produce a one-paragraph summary (max 80 words) and classify it as one of: bug, feature, question, noise. Output strict JSON with keys `summary`, `classification`, `confidence` (0-1)."* Attach a Structured Output Parser that enforces that JSON schema. No tools for now.
> 3. Node 3: a Switch node that routes on `classification`. The `noise` branch terminates silently. The other three branches continue.
> 4. Node 4: a Slack node that posts the summary to a `#triage` channel, with the issue link, classification, confidence, and summary in a formatted block.
> 5. Activate the workflow.
>
> Before you execute anything, show me the graph you are going to build, the node types, and the prompts you will set. I want to approve the plan before you run the tool calls that mutate my n8n instance.

The reason to do it this way: you will *see*, in Claude Code's plan, exactly what a visual agent workflow looks like expressed as a declarative spec. When Claude Code executes the MCP calls, n8n's UI will update in real time. This is the shape of the "AI-catalyst-lead directs AI through MCP" pattern, not the "vibe-code a Python script" pattern.

### Path B — build it in the n8n UI by hand

Same workflow, same nodes, but you click it together yourself. Worth doing at least once to internalize the UI. Budget forty-five minutes your first time.

### What to look at when it runs

Fire three test issues at the repo: one obvious bug (include a stack trace), one feature request (include "it would be nice if..."), one spam-shaped issue (random characters).

Things to check — these are the failure modes that separate a toy from a system you can defend:

- **Structured output enforcement.** Does every run return valid JSON, or does Claude occasionally break schema? If you see drift, tighten the system prompt and add a retry branch on JSON parse failure. This is the n8n equivalent of the output-parser pattern in LangChain.
- **Confidence calibration.** Look at the `confidence` field across runs. Is it pinned at 0.95 for every classification? That is a red flag — the model is not actually expressing uncertainty, and your Switch node will route based on noise. You need an eval, which is Saturday in Week 1's cycle, not today.
- **Latency and cost per execution.** n8n shows per-node timing. A single AI Agent step on Sonnet 4.5 against a typical issue body should be under three seconds and well under a cent. If it is not, you are either passing too much context or calling a slower model than you need.
- **What happens when Anthropic 429s you.** Set the AI Agent node's retry policy to exponential backoff with three attempts. Fire fifty webhook events at once using a small shell loop (`for i in {1..50}; do gh issue create --title "test $i" --body "..."; done`) and watch how the queue behaves. This is where n8n's queue-mode shape becomes important; a single-process Docker install will serialize these, a queue-mode deployment will parallelize.
- **Observability for the non-author.** Imagine a teammate who did not build this workflow getting paged at 3 a.m. because the Slack posts stopped. Can they open n8n's execution log, find the failed run, see the exact input to the AI Agent node, see the exact output, and identify the failure mode without reading your code? This is the ops-maintainability property that justifies choosing n8n over LangGraph in the first place. If the answer is no, the workflow is not production-ready *regardless* of whether it functions.

## Operator war story — the case where n8n was the wrong shape and we found out expensively

An EU-regulated Series B fintech I advised in late 2025 (details composited across two engagements and anonymized; specific dates and headcounts altered, the failure mode and remediation steps verbatim) was processing KYC escalations — documents flagged by an automated pipeline as ambiguous, needing human-plus-LLM triage before going to a compliance officer. The team shipped it in n8n in four days. A Gmail trigger fed an AI Agent node that called Claude with a document OCR tool and a knowledge-base RAG retriever, wrote a draft decision to Google Docs, and notified the on-call compliance officer in Slack. It worked beautifully for three weeks.

Then the regulator's turn came. During a routine audit, the compliance officer was asked: *"for this specific escalation on March 14, can you reproduce the exact reasoning the system used, and demonstrate that the decision was deterministic given the inputs available at the time?"*

The team could not. n8n's execution logs by default retain thirty days of run data at the free tier; the specific run had rolled off. The AI Agent node had made four tool calls in that run, and the intermediate tool-call arguments and results were only partially captured because the team had not turned on full agent-step logging. The model was Claude Sonnet 4.5 at the time of the run but had since been updated to 4.7; the run was not reproducible because the exact model snapshot was not pinned.

The regulator did not shut them down, but the remediation was painful. The team:

1. Moved execution history to a mandatory-retention Postgres instance with seven-year retention.
2. Turned on verbose agent-step logging for every AI Agent node, capturing every tool call's inputs and outputs with content hashes.
3. Pinned specific model snapshots (`claude-sonnet-4-5-20260315` style identifiers) and added a version-check step that fails the workflow if the deployed model ID drifts.
4. Wrapped the actual decision in a separate LangGraph service that emits a structured, replayable trace to an immutable audit log in S3, so the *decision* was auditable even if the n8n orchestration layer was not.

The war-story lesson is not *"n8n is bad for regulated workloads."* It is *"n8n's defaults are tuned for ops-team maintainability, not for regulatory auditability, and if your workload is on the regulated side of that line you have to change defaults explicitly."* The specific failure mode — a visual workflow engine that does not retain full agent-step traces by default — is the single most underrated production risk of the shelf-B choice. Find it before the regulator does.

## Common mistakes experts see

1. **Picking the framework for the prototype, then never revisiting.** The workflow engine you pick in week one of a project is almost never the one that is still correct in week sixteen. Set a calendar reminder to review.
2. **Running n8n in single-process Docker in production.** It works until one webhook spikes and the whole instance serializes. Queue-mode with Redis-backed workers is the production pattern; treat the docs on this as mandatory reading before you ship.
3. **Putting business rules inside the AI Agent node's prompt.** If the rule is deterministic — "only process Tier 1 accounts" — it is a Filter node before the agent, not a sentence in the system prompt. The LLM will follow the sentence nine times out of ten, which is the worst possible reliability profile.
4. **Using n8n for durable execution it was not designed for.** A multi-day saga with compensation logic is a Temporal problem. Do not build your own durability on top of n8n's retry semantics; you will reinvent a worse Temporal over six months.
5. **Not pinning model snapshots.** Claude, GPT, and Gemini all silently refresh behind aliased model IDs. Production AI workflows must pin to dated snapshots or they are not reproducible. This is a regulated-industry hard requirement and a good-taste requirement for everyone else.
6. **Ignoring the MCP Server Trigger.** Exposing n8n workflows as MCP tools to Claude Code or Claude Desktop is one of the most leveraged patterns in the 2026 stack; it lets human operators delegate to Claude, and Claude delegates to n8n, with the n8n workflows being the audit-stable layer. Most teams have not discovered this yet.
7. **Reading vendor comparisons as if they were vendor-neutral.** Every "X vs Y" blog post on a vendor's own domain ranks that vendor highest. Read at least three third-party comparisons — ZenML, OrangeLoops, Latenode are all reasonable — and note where they disagree; that is where the real tradeoffs live.

## Reflection questions

1. You have a workflow that runs once a week, takes ninety seconds end-to-end, and notifies a team of twelve. Why would choosing Temporal for this be a senior-engineer-level mistake?
2. Anthropic's workflow/agent framing calls *orchestrator-workers* a workflow, not an agent. A team builds an n8n workflow with one AI Agent node that dispatches to three other AI Agent nodes in parallel and synthesizes their output. Is that a workflow or an agent under Anthropic's definition? Defend your answer in two sentences.
3. Under what specific conditions would you use n8n to call out to a LangGraph service, and under what specific conditions would you use LangGraph to call out to an n8n webhook? Give one concrete example each.
4. What fails if you try to use visual-workflow drag-and-drop to express Anthropic's *evaluator-optimizer* pattern with a termination condition based on a quality score? Where specifically does the abstraction break, and what is your workaround inside n8n?
5. A colleague says *"we should use n8n because it's open source."* Steelman the ways that claim is incomplete or misleading, and give them the correct one-sentence version.
6. You have a regulated workload with a seven-year audit requirement. The team wants to ship in n8n because the ops team can maintain it. What are the three non-default configurations you must insist on before going to production, and why?
7. Zapier Agents, n8n's AI Agent node, and LangGraph all claim to be the "right way" to build agents in 2026. Which stakeholder profile in your company would you hand each to, and why is giving the wrong one to the wrong person more expensive than using no tool at all?

## My take (reviewer lens)

The most honest critique I can level at this lesson is that the workflow/agent framing, while correct, is more bimodal than reality. In practice the line between *"predefined path with one agent island"* and *"dynamic agent that happens to revisit the same few states"* is blurrier than Anthropic's essay makes it sound, and real systems drift across the line over their lifetime. I am handing you a clean dichotomy because clean dichotomies are useful for tool choice; do not mistake it for a complete theory of how agents will behave in eighteen months.

Where **Karpathy** would push back: the whole framing treats the LLM as a black box and the workflow engine as the interesting part, but Karpathy would correctly note that the *prompt* you put inside the AI Agent node is where 80% of real quality lives — a point Monday of Week 1 made in detail. Choosing n8n vs LangGraph is a second-order decision; getting the prompt and the evals right is the first-order one. Re-read Week 1 Monday before you pick the framework.

Where **Michael Seibel** would push back: I have spent six thousand words helping you choose between three sophisticated tools. Seibel's instinct — *just do the ugliest thing that works* — says start with a Python script and cron, measure the real failure modes, and only upgrade to a workflow engine when the ugly thing visibly breaks. That is correct advice for week-one of a new project. It is wrong advice at scale, when the cost of "ugly" is an ops team that cannot maintain it without you. The lesson you should take from Seibel: do not over-invest in framework choice *before* you have shipped the first version. Do it after.

Where **Boris Cherny** would push back: the experiment assumes Claude Code drives n8n through MCP cleanly. In practice, MCP servers in early 2026 still have rough edges — connection drops on SSE endpoints, authentication scope creep, partial tool-call streaming. Cherny would tell you to run the experiment, yes, but to also instrument which MCP calls timed out, which returned garbage, and which silently succeeded with stale data. The tooling is real; the production-readiness of the tooling is still 2025-shaped.

Where **a senior n8n engineer** would push back, which is the disagreement most worth naming: the implicit argument in this lesson — *"n8n is a workflow engine with agent nodes, not a true agent platform"* — is less true in 2026 than it was in 2025. The 2025 MCP release, combined with the multi-step Agent-node improvements and the queue-mode scaling story, has moved n8n meaningfully closer to Shelf D than this lesson credits. A fair reviewer from the n8n side would say: *"the hybrid n8n-plus-LangGraph story you are pitching is already obsolete for a growing class of use cases — we can do both halves in n8n now."* I partially agree. I still would not bet a regulated-industry workload on that claim for another year.

## Further reading

**Must-read**

- Anthropic, *Building Effective Agents* (Dec 2024).[^9] The single most important vendor-neutral piece on when to pick workflows over agents.
- n8n, *AI Agent node documentation*.[^1] Read the entire page; it is short and authoritative.
- n8n, *Set up and use n8n MCP server* docs.[^3] For the MCP-on-both-sides pattern.

**Recommended**

- ZenML, *LangGraph vs n8n: Choosing the Right Framework for Agentic AI*.[^13]
- OrangeLoops, *Building AI Agents with LangGraph vs n8n: A Hands-On Comparison* (June 2025).[^14]
- Simon Willison's annotations on *Building Effective Agents*.[^10] Willison's summary is often clearer than the original.
- n8n, *15 best practices for deploying AI agents in production*.[^15] Vendor blog, but the specific pitfalls named are real.

**Optional**

- Latenode, *N8N AI Agents 2025: Complete Capabilities Review + Implementation Reality Check*.[^16] A competitor's write-up, honest about where n8n is rough.
- LangGraph 1.0 release notes (Oct 2025).[^6]
- Temporal's durable execution primer — not directly about AI, but it is the right mental model for when you *do* need durability.

## Citations

[^1]: n8n Docs, *AI Agent node documentation*. https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.agent/
[^2]: n8n Docs, *MCP Client Tool node documentation*. https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.toolmcp/
[^3]: n8n Docs, *Set up and use n8n MCP server*. https://docs.n8n.io/advanced-ai/accessing-n8n-mcp-server/ and *MCP Server Trigger node documentation* https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-langchain.mcptrigger/
[^4]: Zapier, *The new Zapier Agents: scalable, organized AI automation* (May 2025). https://zapier.com/blog/zapier-agents-pods-dashboards/
[^5]: Zapier, *Zapier updates: AI Agents, admin, and controls* (December 2025). https://zapier.com/blog/december-2025-product-updates/
[^6]: LangChain, *LangGraph 1.0 release* (October 2025), referenced in *The Complete Guide to Choosing an AI Agent Framework in 2025*. https://www.langflow.org/blog/the-complete-guide-to-choosing-an-ai-agent-framework-in-2025
[^7]: n8n Docs, *AI and LangChain Nodes* (DeepWiki index). https://deepwiki.com/n8n-io/n8n/4.4-ai-and-langchain-nodes
[^8]: Skywork AI, *n8n 2025 Update: New AI Nodes and Self-Hosting Improvements*. https://skywork.ai/blog/ai-agent/n8n-2025-update-new-ai-nodes-and-self-hosting-improvements/
[^9]: Anthropic, *Building Effective AI Agents* (December 2024). https://www.anthropic.com/research/building-effective-agents
[^10]: Simon Willison, *Building effective agents* annotation (December 20, 2024). https://simonwillison.net/2024/Dec/20/building-effective-agents/
[^11]: n8n Community, *We're adding MCP Client tool & MCP Trigger nodes — try them now!* https://community.n8n.io/t/we-re-adding-mcp-client-tool-mcp-trigger-nodes-try-them-now/99338
[^12]: n8n, *Case Studies — Delivery Hero, SanctifAI, Flow AI, BeGlobal*. https://n8n.io/case-studies/
[^13]: ZenML Blog, *LangGraph vs n8n: Choosing the Right Framework for Agentic AI*. https://www.zenml.io/blog/langgraph-vs-n8n
[^14]: OrangeLoops, *Building AI Agents with LangGraph vs n8n: A Hands-On Comparison* (June 2025). https://orangeloops.com/2025/06/building-ai-agents-with-langgraph-vs-n8n-a-hands-on-comparison/
[^15]: n8n Blog, *15 best practices for deploying AI agents in production*. https://blog.n8n.io/best-practices-for-deploying-ai-agents-in-production/
[^16]: Latenode Blog, *N8N AI Agents 2025: Complete Capabilities Review + Implementation Reality Check*. https://latenode.com/blog/low-code-no-code-platforms/n8n-setup-workflows-self-hosting-templates/n8n-ai-agents-2025-complete-capabilities-review-implementation-reality-check

_last_verified: 2026-04-15_
