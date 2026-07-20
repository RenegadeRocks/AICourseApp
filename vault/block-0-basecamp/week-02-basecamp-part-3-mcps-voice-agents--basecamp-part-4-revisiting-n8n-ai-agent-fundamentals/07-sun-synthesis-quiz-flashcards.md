---
type: synthesis
block: block-0-basecamp
week: week-02
day_of_cycle: 7
day_name: sun
title: 'Week 2 Synthesis — Agent engineering as runtime selection'
study_date: 2026-05-10
date_due: 2026-05-10
tags: [synthesis, quiz, flashcards, mcp, voice-agents, n8n, agent-fundamentals, lethal-trifecta, react, tau-bench, runtime-selection]
last_verified: 2026-07-17
word_count_target: 3800
---

# Week 2 Synthesis — Agent engineering as runtime selection

## The one-sentence thesis of this week

The six topics you covered this week — MCP as a protocol, building an MCP server, MCP security, voice-agent architecture, n8n as a workflow engine with agent islands, and the deeper pass on agent fundamentals (ReAct, planning, memory, evals) — are not a grab-bag of emerging tools. They are the six decisions that answer one question: *given a task, which runtime do you put the LLM inside, and which runtime do you explicitly refuse?* Week 2 is about developing the taste to refuse as often as to accept.

---

## The unifying frame: agent engineering is runtime selection, not model selection

Week 0 installed the substrate (how models work, how your tooling works, how context economics work, how to recover from an agent that broke something). Week 1 installed the primitives (prompting, retrieval, agentic loops with tool use). Week 2 moves one floor down: *the protocols and runtimes that compose those primitives into shippable products*.

The silent thread across Mon–Sat is that almost every operator-level decision you will be asked to make in 2026 reduces to a *runtime* decision, not a model decision:

- **Mon — MCP as a protocol.** The decision is not "which tool-calling API" but "do I commit to a client-agnostic protocol, accept its limits, and spend the protocol's negotiation surface (`initialize`, `protocolVersion`, capabilities) as my integration contract, or write vendor-specific glue?"
- **Tue — Building an MCP server.** The decision is not "which SDK" but "how fat are my tools, how will my schema descriptions read to the model on every turn, and how much of my REST surface do I deliberately refuse to expose?"
- **Wed — MCP security.** The decision is not "which guardrail" but "do I own the trust boundary at the protocol, the client, the OS, or the sandbox — and do I enforce it with mechanisms or with vibes?"
- **Thu — Voice agents.** The decision is not "which TTS" but "pipelined with seams I control or end-to-end with naturalness I cannot reconstruct, on what network, under what latency budget, against what codec?"
- **Fri — n8n for agent workflows.** The decision is not "n8n vs LangGraph" but "workflow-with-agent-islands vs agent-end-to-end, and which of these can a non-author maintain at 3 a.m. six months from now?"
- **Sat — Agent fundamentals deeper.** The decision is not "which agent framework" but "plan-first or interleaved, which of the four memory types earns its complexity, and which of your current automations should not be agents at all?"

Frame it that way and the week snaps into focus. Agent engineering is the discipline of picking the *right runtime* for a problem — and of knowing when the right runtime is "not an agent."

---

## Where each day's content goes forward

| This week's lesson | Underwrites in later weeks |
|---|---|
| Mon — MCP as a protocol | Every lesson that involves a tool call going forward; Block 1 browser-agents; Block 2 client integration work |
| Tue — Building an MCP server | Week 5+ skills and custom tools; any client project shipping a custom tool surface |
| Wed — MCP security | Every production deployment; Week 18+ enterprise posture; incident response playbooks |
| Thu — Voice agents | Block 2 voice-first products; Week 20+ latency-sensitive deployments; any telephony product decision |
| Fri — n8n for agent workflows | Block 1 automation projects; client work where ops must maintain the system; Block 4 hand-off to non-engineer teams |
| Sat — Agent fundamentals deeper | Every agent decision after today; Week 7–9 evals; Week 13 reasoning agents; Week 18 parallel orchestration |

Week 2 is not a survey. It is the layer of mechanical decisions that Week 5, Week 13, and Week 20 will silently assume you have internalized. When Week 18 asks you to parallel-orchestrate agents, you will re-open Saturday's planning vs interleaved table. When Block 2 asks you to ship a voice product, you will re-open Thursday's latency budget. When a client-engagement CISO in Block 4 asks "what's our MCP story," you will re-open Wednesday's mitigation stack.

---

## The week's key moves — the mental-move table

Thirteen highest-leverage operational moves drawn from the six lessons. Each row: the move, the mechanism that explains why, when to apply it, when not to.

| # | Move | Mechanism | Apply when | Do NOT apply when |
|---|------|-----------|------------|-------------------|
| 1 | Treat MCP as a JSON-RPC 2.0 protocol with four primitives (tools, resources, prompts, sampling), three transports, and two auth revisions — not as "the USB-C of AI" | Every field in the `initialize` handshake is load-bearing; `protocolVersion` negotiation is your compatibility reflex | Any server/client you ship or evaluate | Marketing conversations where "USB-C of AI" is the level of detail requested |
| 2 | Speak 2025-11-25 on the client (the current stable revision), negotiate down to 2024-11-05 | The spec defines a handshake specifically for this; unilateral upgrades break deployed servers. The 2026-07-28 stateless-core RC is upcoming, not shipped | Shipping a new MCP client in 2026 | Prototyping against a single known server |
| 3 | Match tool granularity to LLM-useful operations, not to REST routes — one to three tool calls for the 80% use case | Tool descriptions eat context tokens on every turn; too-thin tools burn compose cycles; too-fat tools hide failure modes | Designing any MCP server from scratch | Wrapping an API for one-off personal use |
| 4 | Write the tool description as if it were a system-prompt instruction: triggers, anti-triggers, return shape, every parameter described | The description IS a prompt fragment the model reads on every turn it's in context; enums eliminate invented values | Any tool exposed to an agent | Internal debug tools not consumed by a model |
| 5 | Apply Willison's lethal trifecta check: private data + untrusted content + exfiltration channel = no reliable defense | The transformer has no architectural way to distinguish instruction sources; this is mechanism, not policy | Threat-modeling any multi-server MCP deployment | Purely local, single-tenant, no-egress scripts |
| 6 | Enforce trust at the client with OS primitives (sandbox-runtime, bubblewrap, Seatbelt), not with vibes | Permission prompts fatigue; the spec cannot sanitize tool output; only kernel-level boundaries hold under real attack distributions | Any production deployment with credentialed MCP servers | Throwaway local experiments on non-sensitive data |
| 7 | Draw the voice pipeline as seven components (capture/transport, VAD, endpointing, STT, LLM, TTS, playback/AEC) before picking a vendor | You cannot argue about latency budgets until you know where each millisecond goes; vendor demos hide the transport and AEC costs | Any voice-product scoping conversation | Purely text-mode products |
| 8 | Decide pipelined vs end-to-end by use case: regulated/telephony/multilingual → pipelined; consumer-companion/prosody-critical → end-to-end | Pipelined preserves control points and 10× cost advantage; end-to-end preserves acoustic nuance a text bottleneck destroys | Committing to a voice architecture | Before you have drawn the pipeline in Move 7 |
| 9 | Budget 800 ms end-of-user to start-of-agent on web, 900–1400 ms on telephony, and locate the bottleneck in the endpointing + LLM-TTFT + TTS-TTFA chain | Production voice data shows >1000 ms spikes abandonment; endpointing timeout + LLM TTFT dominate; sub-500 ms on PSTN is a vanity metric | Any voice SLA conversation | Prototypes where perceived responsiveness isn't yet the product |
| 10 | Use Anthropic's distinction: workflow = predefined code paths with LLM functions; agent = LLM chooses control flow at runtime. 80% of real problems are workflow-with-agent-islands | Workflows are predictable, debuggable, cheaper; unconstrained agents loop, burn tokens, produce confident garbage under novel input | Scoping any "AI agent" request from a stakeholder | Dynamic research/planning tasks where replan is the whole point |
| 11 | Reach for n8n when integration dominates (70% glue, 30% reasoning); reach for LangGraph when stateful branching dominates; reach for Temporal when durable-execution SLA demands it (< 5% of cases) | Each shelf trades different failure modes — observability vs expressiveness vs durability; misreaching costs three months of wrong abstraction | Framework decisions in client engagements | Personal weekend builds where the cost is your afternoon |
| 12 | Pick planning-first for long, irreversible, multi-file tasks; interleaved ReAct for short, read-mostly, cheap-to-retry tasks; fixed-DAG workflow for structured repetitive steps (not an agent at all) | Plans made before observation are frequently wrong; interleaved reasoning adapts but accumulates context errors past ~20 steps (Cognition SWE-bench report) | Picking an agent shape for a task with known horizon | Before measuring tool-call count and wall time on your actual task |
| 13 | Use benchmarks for triage, then build a 50-example domain-specific eval set with LLM-as-judge validated against expert critique shadowing | Headline pass^1 scores hide the pass^k collapse (TAU-bench airline: ~60% pass^1 → <40% pass^8 on frontier models); your production distribution isn't the benchmark's distribution | Before committing to a base model for a product | Ruling models in for further testing — headline is a fine first filter |

---

## 20 quiz questions

*Span: Mon–Sat. Mix: 8 recall, 8 apply, 4 controversy-defense. Answers at end.*

---

**Q1 (Recall)** — What are the four primitives of the Model Context Protocol, and which actor controls each (model / application / user / server)?

**Q2 (Recall)** — Which two RFCs were formalized by the 2025-06-18 MCP authorization revision, and what class of attack do they collectively defuse?

**Q3 (Recall)** — Define Willison's *lethal trifecta*, naming all three ingredients.

**Q4 (Recall)** — Name the seven pipeline components of a pipelined voice agent, in order from microphone to speaker.

**Q5 (Recall)** — What is the numeric production target (in milliseconds) for end-of-user-speech to start-of-agent-speech on (a) a wired web call and (b) a PSTN telephony call?

**Q6 (Recall)** — State Anthropic's five workflow patterns from *Building Effective Agents* (Dec 2024).

**Q7 (Recall)** — Name the four types in the agent-memory taxonomy and which Claude Code mechanism primarily carries each (if any).

**Q8 (Recall)** — What does BFCL v3 add that v1 and v2 lacked, and why does that matter for agent selection?

**Q9 (Apply)** — Your team wants to expose "everything in our Notion" to an agent. Design the tool surface: how many tools, what names, and what's explicitly refused. Justify using Tuesday's schema-as-prompt discipline.

**Q10 (Apply)** — You are attaching three MCP servers to Claude Code: Filesystem, Gmail, and a company-wide GitHub server. Enumerate the lethal-trifecta paths. Then list the concrete mitigations in mechanism-not-vibes order.

**Q11 (Apply)** — You're scoping a voice agent for outbound appointment reminders to elderly patients on residential landlines. Walk through the architecture decision (pipelined vs end-to-end), the vendor stack, and three specific calibration choices the Thursday "operator war story" forces you to make upfront.

**Q12 (Apply)** — A marketing-ops lead asks you to ship "an AI agent that watches our support inbox and files Jira tickets with smart categorization." Pick the primitive (n8n / LangGraph / Zapier Agents / custom Python) and defend in one paragraph using Friday's shelf-A/B/C/D map.

**Q13 (Apply)** — You have a nightly data-reconciliation job running ReAct that aborts ~8% of nights due to a loop-detection trip. Using Saturday's planning-vs-interleaved framework, what is your first intervention, what are you measuring, and what is the cost envelope you accept?

**Q14 (Apply)** — Your team claims their support-agent has "memory" because they've wired a Pinecone vector store over past tickets. Apply Layer 4's *complexity test* (write / read / cost-of-stale / system-prompt-equivalent). What do you change?

**Q15 (Apply)** — A junior engineer proposes logging every `Thought:` field from your production ReAct agent to satisfy a compliance audit trail. Write the two-sentence pushback grounded in Saturday's research callouts.

**Q16 (Apply)** — You need to build an MCP server for an internal CRM with ~200 REST endpoints. Applying Tuesday's "match granularity to LLM-useful operations" rule, outline how many tools you ship, which REST routes collapse into one tool, and which get explicitly refused.

**Q17 (Controversy-defense)** — Position: "In 2026, end-to-end speech-to-speech models (gpt-realtime, Gemini Live) obsolete pipelined voice stacks for all new greenfield consumer deployments." Take a side and defend with at least two specific data points from Thursday's lesson.

**Q18 (Controversy-defense)** — Position: "The 2025-06-18 MCP spec adequately addresses MCP's security problems; further protocol-level work on tool-output sanitization is unnecessary." Take a side. Cite Willison, Parecki, the Anthropic sandboxing stance, or a disclosed CVE.

**Q19 (Controversy-defense)** — Position: "Orchestrator-workers is the dominant pattern for long-horizon agent work; interleaved ReAct is a legacy pattern kept alive by tutorial inertia." Take a side. Defend with at least one benchmark point (SWE-bench Pro, TAU-bench, BFCL) and one operator war story.

**Q20 (Controversy-defense)** — Position: "n8n is a toy for non-engineers; any serious AI-agent production work should be built in LangGraph or a Temporal-backed custom service." Take a side. Defend with reference to shelves A–D, maintenance horizon, and at least one production case study named in Friday's lesson.

---

## Answers

**Q1** — **Tools** (model-controlled): the model decides when to invoke. **Resources** (application-controlled): URI-addressable read-only data the app chooses to inject. **Prompts** (user-controlled): named templates the user invokes, typically via slash command. **Sampling** (server-initiated): the *server* asks the client's model to complete text. Adjacent primitives worth knowing: roots (filesystem advertisement) and elicitation (structured user prompt mid-call, 2025-06-18).

**Q2** — **RFC 9728 Protected Resource Metadata** (`/.well-known/oauth-protected-resource` discovery; MCP servers are OAuth 2.0 Resource Servers only, not their own authorization servers) and **RFC 8707 Resource Indicators** (clients must name the specific MCP server a token is for, so the AS issues audience-scoped tokens). Together they defuse the *confused-deputy* attack class where a compromised server laundered tokens across audiences. Dynamic Client Registration (RFC 7591) is the complementary bit for client onboarding.

**Q3** — (1) Access to private data + (2) exposure to untrusted content + (3) an exfiltration channel. With all three present, there is no reliable architectural defense — the transformer cannot distinguish user instructions from tool-output instructions. Willison coined the framing in June 2025 and demonstrated it in the Supabase MCP disclosure (July 2025) and the GitHub MCP exploit (May 2025).

**Q4** — (1) Capture and transport (mic → codec → WebRTC/SIP/WebSocket); (2) VAD; (3) endpointing / turn detection; (4) streaming STT; (5) LLM inference (optimizing for TTFT); (6) streaming TTS (optimizing for TTFA); (7) playback and echo cancellation.

**Q5** — (a) 800 ms on wired web / good network — the threshold derived from conversation-analysis work (Stivers et al.) showing average human inter-speaker gap around 200 ms; (b) 900–1400 ms on PSTN telephony, because PSTN adds ~100–200 ms one-way each direction for the media bridge plus 20–50 ms for codec transcoding. Beyond ~1000 ms, production voice data shows abandonment spikes 40%+.

**Q6** — (1) Prompt chaining; (2) routing; (3) parallelization (voting or sectioning); (4) orchestrator-workers; (5) evaluator-optimizer. All five are *workflows* in Anthropic's taxonomy — control flow fixed in code. A true *agent* has the LLM deciding its own control flow at runtime.

**Q7** — **Working** (context window — every chat model), **episodic** (past conversations — vector store or Postgres+embeddings), **semantic** (facts about the world — user profiles, account records), **procedural** (skills/routines — Claude Code's skills files or system prompt). In Claude Code specifically: working = session context; episodic = auto-memory/memory directory; semantic = CLAUDE.md + user profile memory; procedural = skills + hooks.

**Q8** — BFCL **v3 (September 2024)** added multi-turn and multi-step function calling — v1 and v2 tested only single-shot correctness via AST match. v4 (2025) added holistic agentic evaluation with periodically-refreshed real-world data. This matters because production agents fail on turn N of N, not on turn 1; a v1 score tells you nothing about whether the model maintains schema adherence across a long conversation.

**Q9** — A defensible answer: **~12–18 tools**, not a REST mirror. Ship `search_pages`, `read_page`, `search_and_read` (the 80% call pattern collapsed), `create_page`, `update_page`, `append_block`, `query_data_source`, `retrieve_data_source_schema`, `list_databases_for_user`, `get_recent_edits`, `create_comment`, `resolve_mention`. **Refuse**: raw block-level CRUD (too thin; agent composes badly), workspace-admin operations (wrong trust surface for most users), destructive bulk operations (behind explicit confirm tool). Every parameter has a `describe()` with trigger conditions; every enum is constrained; names read as intent (`search_pages` not `list_pages_query_v2`). Refer to Notion's actual hosted server (18 tools / 6 categories) as the precedent.

**Q10** — **Paths:** (a) Gmail email body (untrusted) → Filesystem write (exfiltration); (b) Filesystem read of `~/.ssh` or `.env` (private data) → Gmail send (exfiltration); (c) GitHub public-issue body (untrusted) → any of the above (exfiltration via PR/issue comment). **Mitigations, mechanism-first:** (1) Run each server under `sandbox-runtime` or in a Docker container with scoped network egress; (2) configure deny-by-default permissions (`"deny": ["WebFetch", "Bash(curl *)"]`) and narrow allowlists; (3) enforce per-tool OAuth scopes (Gmail read vs send as different tokens; GitHub `repo:read` only where possible); (4) turn on GitHub MCP's lockdown mode if public repos are in scope; (5) keep permission prompts enabled for anything that crosses tool families; (6) store tokens in OS keychain, not plaintext dotfiles. Do NOT rely on prompt-level "ignore suspicious instructions" as a primary control.

**Q11** — **Architecture**: pipelined. Regulated domain, telephony transport, older demographic, multilingual possibility, transcript-as-record-of-care all point pipelined. **Stack**: Twilio (PSTN) + Pipecat + Deepgram Nova-3 (with `keyterm` boosting medication names) + GPT-4o-mini (cheap, low TTFT) + Cartesia Sonic Turbo or ElevenLabs Turbo v2.5. **Calibration forced by the war story**: (1) widen endpointing silence timeout well beyond demo default — elderly patients pause mid-sentence; use a transformer-based turn detector rather than pure VAD where possible; (2) verify echo cancellation end-to-end on speakerphone through the actual carrier bridge, not in-browser; (3) watch for 8 kHz µ-law upsampling degrading WER on accented speakers and test against actual pilot-population audio, not in-house voices. Measure drop-off rate at first agent response from day one.

**Q12** — **n8n**, for this specific ask. Shelf B fits because: (a) it's 70% integration work (inbox, Jira, probably Slack notifications, probably a Notion log), which is what n8n does natively via its ~500-node directory; (b) an ops lead is the probable owner going forward — visual workflow is maintainable by someone who isn't the author; (c) AI Agent node handles the "smart categorization" as an agent-island inside an otherwise predefined workflow, which is the correct Anthropic-taxonomy shape. LangGraph is overkill (you'd write Slack/Jira/inbox glue in Python for no gain). Zapier Agents is plausible if non-engineers own maintenance and self-host isn't required. Temporal is flat wrong — no durable-execution SLA here.

**Q13** — **First intervention**: move from interleaved ReAct to plan-first (Plan mode / orchestrator-worker). **Measuring**: tool-call count per run, wall time, abort rate, token cost per run, and on-call burden (alerts/week). **Accepted envelope**: ~2.4× token cost, ~40% longer wall time, in exchange for <1% abort rate. Cite Saturday's war story — replacing ReAct with plan-first on a nightly reconciliation cut tool calls from 23 → 11 and aborts from 8% → <1%, at the cited 2.4× token and 40% wall-time cost, and was worth it because on-call cost dominated.

**Q14** — **Run the complexity test**: What writes (auto-ingestion of closed tickets? unvalidated?). What reads (median retrievals per session? if zero, the memory does nothing). Cost of stale (a stale ticket summary misleads an agent response — how bad?). Could the system prompt + current ticket do the job (often yes for Tier-1 support)? **Recommended change**: instrument retrievals-per-session for a week. If median is zero, delete the vector store and reclaim the latency. If retrievals do fire, validate writes (human-curated or reviewer-approved, no unvalidated model-written facts — LangMem-style poisoning risk). Replace "we have memory" with "we have a 50-example eval set for tickets-with-episodic-memory vs without."

**Q15** — The Lanham 2023 / Turpin 2023 / Chen-Benton 2025 research shows reasoning traces disclose the actual influencing cue <20% of the time — `Thought:` is post-hoc rationalization, not causal trace. For audit, log inputs → tool calls → outputs; those have deposition-grade integrity. `Thought:` does not.

**Q16** — Ship ~20–30 tools, not 200. Collapse CRUD verbs into intent-named bundles: `POST /accounts` + `GET /accounts/{id}` + `PATCH /accounts/{id}` become `create_account_with_primary_contact` and `update_account_details` (separate, because the 80% call patterns differ). Collapse paginated list endpoints into `search_<entity>` with explicit filter parameters. **Refuse** bulk-delete, schema-migration, workspace-admin routes entirely — put them behind human-in-loop or don't expose at all. Every tool has a description with triggers/anti-triggers; every parameter has a `describe()`; every enum is constrained. Version the tool surface; add tools, don't reshape.

**Q17** — Defensible either side. **"Agree" defense**: Sesame CSM listening tests show participants rate generated speech as equivalent to real recordings without context; OpenAI's Realtime line now ships GPT-Realtime-2 (May 2026) with GPT-5-class reasoning *inside* the voice model, closing the old "e2e can't think" objection, plus a July-2026 latency cut; prosody preservation (`[whispers]`, `[laughs]`, pitch, pace) is architecturally impossible in pipelined where the text bottleneck destroys the signal. **"Disagree" defense (stronger)**: the cost gap persists — a token-metered model like GPT-Realtime-2 runs ~$0.30–0.50/min vs raw components ~$0.02–0.06/min (and managed platforms like Retell/VAPI ~$0.13–0.36/min all-in); pipelined enables per-language best-of-breed STT/TTS (Deepgram Flux, Cartesia Sonic 3.5, ElevenLabs v3) for multilingual products; compliance and observability (separate text transcript as record) are still better on pipelined; hybrid stacks (end-to-end for conversation + pipelined transcript for logging) are the common production compromise. Strong answer splits by use case rather than pretending one wins everywhere.

**Q18** — Defensible either side but "disagree" is stronger, and mid-2026 events tilted it further that way. **"Disagree" defense**: the 2025-06-18 revision fixed audience-binding (RFC 8707) and discovery (RFC 9728), and 2025-11-25 layered on more OAuth (OIDC discovery, M2M client-credentials) — but none of it addressed tool-output sanitization, tool-description poisoning (Invariant Labs PoC, April 2025), or cross-server shadowing. The 2026 evidence is damning: OX Security's "Mother of All AI Supply Chains" showed a systemic command-execution flaw baked into every official MCP SDK (150M+ downloads, up to ~200K vulnerable instances) that Anthropic confirmed as *intentional*; 30+ CVEs landed in a single 60-day window (~43% command-injection); Windsurf shipped a zero-click RCE (CVE-2026-30615); and the Unicode TAG-block concealment class (arXiv 2607.05744) defeats the human approval view entirely. Auth fixes were necessary, never sufficient. **"Agree" defense (Position B from Wednesday)**: MCP correctly offloads sanitization and sandboxing to the client layer where context exists (who the user is, what surface renders the output, is a human approving). Protocol-level sanitization would produce an LCD spec serving neither personal installs nor multi-tenant SaaS. Anthropic's sandboxing posture — and its refusal to change the SDK behavior OX flagged — is the practical vote for this view. The OWASP Top 10 for Agentic Applications (2026) is the framework to structure either argument.

**Q19** — Defensible either side. **"Agree" defense**: SWE-bench Verified (Opus 4.5 at 80.9%, Opus 4.6 exceeding it) and SWE-bench Pro both reward long-horizon planning; plan-heavy agents dominate both leaderboards. Cognition's technical report argues interleaved ReAct accumulates context errors past ~20 steps. The nightly-reconciliation war story (Saturday §Layer 3) showed plan-first cut aborts from 8% to <1% on a real client workload. **"Disagree" defense (stronger)**: Yao's original 2022 result on HotpotQA and ALFWorld showed interleaved beat planning-heavy baselines precisely because it adapted to observations the plan couldn't anticipate. TAU-bench airline (policy-heavy conversational domain) rewards local adaptation; plan-first loses on short user interactions because the plan is longer than the execution. The real axis is task horizon and reversibility — Saturday's table — not a binary. GPT-5's 45% fewer tool calls on TAU-bench telecom suggests model-level efficiency progress matters at least as much as scaffold choice.

**Q20** — "Disagree" is stronger, but a mature answer acknowledges both sides. **"Disagree" defense**: n8n sits on Shelf B (developer-facing workflow engine, self-hostable). For problems that are 70% integration and 30% reasoning — which is most real stakeholder asks — LangGraph costs you weeks of Python glue code for Slack/Jira/GCal work n8n solves natively. Delivery Hero reports 200+ engineer-hours saved per month on a single n8n workflow. Regulated industries (healthtech, fintech, EU data residency) run n8n inside their VPC where Zapier is a non-starter. Maintenance by non-authors is strictly better than reading Python. **The correct production pattern is often hybrid**: n8n as the outer workflow, a LangGraph service called out to for the agent-heavy inner loop. **"Agree" defense (narrower)**: for stateful, multi-agent, complex-branching applications with typed state and checkpointable graphs, LangGraph wins unambiguously (Friday's head-to-head table). For exactly-once semantics on multi-day workflows, Temporal wins unambiguously. The mistake is assuming those characteristics describe most real problems — they describe <5% of them.

---

## 30 flashcards

*Format: front (question/prompt) ↔ back (answer). Anki-importable.*

1. Q: The four MCP primitives and who controls each? → A: Tools (model), resources (application), prompts (user), sampling (server).
2. Q: The three MCP transports? → A: stdio (local subprocess), HTTP+SSE (2024-11-05, deprecated), Streamable HTTP (2025-03-26, current).
3. Q: What RFC does MCP 2025-06-18 require clients to use for token requests? → A: RFC 8707 Resource Indicators — scoping tokens to the specific MCP server.
4. Q: What discovery document does a 2025-06-18 MCP server publish? → A: `/.well-known/oauth-protected-resource` (RFC 9728 Protected Resource Metadata).
4b. Q: MCP spec revisions and governance as of mid-2026? → A: Revisions 2024-11-05 → 2025-03-26 → 2025-06-18 → **2025-11-25** (current stable: async Tasks, OIDC/M2M OAuth, JSON Schema 2020-12); the **2026-07-28 stateless-core RC** is upcoming. MCP is governed by the Linux Foundation's **Agentic AI Foundation** (Dec 9 2025), co-hosted with A2A, goose, and AGENTS.md — the "A2A faded" story is inverted.
5. Q: The lethal trifecta? → A: Private data + untrusted content + exfiltration channel = no reliable defense.
6. Q: Willison's one-line on MCP and the trifecta? → A: MCP encourages users to mix and match tools from different sources — many access private data, many pull in untrusted content, and exfiltration paths are almost limitless.
7. Q: CVE-2025-59536? → A: Claude Code hooks in `.claude/settings.json` executing on session events before user approval — triggered by `cd`-ing into a malicious repo.
8. Q: CVE-2025-6514? → A: `mcp-remote` npm proxy (437k downloads) — malicious server could return a `file:` URI as `authorization_endpoint` triggering arbitrary OS command execution during OAuth handshake. CVSS 9.6. Fixed in 0.1.16.
9. Q: The postmark-mcp supply-chain incident? → A: Sept 2025 — counterfeit npm package BCC'd every outgoing email to attacker-controlled address; 1,643 downloads before removal.
10. Q: Anthropic's `sandbox-runtime` primitives? → A: macOS `sandbox-exec` + Seatbelt profiles; Linux `bubblewrap` + network namespaces. Declare allowed paths and hosts; everything else fails closed.
10b. Q: The 2026 MCP security escalation (four facts)? → A: (1) OX Security "Mother of All AI Supply Chains" — systemic command-exec flaw in every official MCP SDK, ~200K vulnerable instances, Anthropic calls it intentional; (2) 30+ CVEs in 60 days (~43% command-injection); (3) Windsurf zero-click RCE CVE-2026-30615; (4) Unicode TAG-block concealment (arXiv 2607.05744) defeats the human approval view. Framework: OWASP Top 10 for Agentic Applications 2026.
11. Q: The seven components of a pipelined voice agent? → A: Capture/transport, VAD, endpointing, streaming STT, LLM inference (TTFT), streaming TTS (TTFA), playback + echo cancellation.
12. Q: End-to-end voice-agent latency target on wired web? → A: ≤800 ms end-of-user-speech to start-of-agent-speech; >1000 ms spikes abandonment ~40%.
13. Q: PSTN telephony voice-agent latency reality? → A: 900–1400 ms because of ~100–200 ms each direction on the PSTN-to-cloud bridge plus codec transcoding.
14. Q: Why does endpointing matter more than any other single knob? → A: Pure VAD silence-timeout (500–800 ms) is the biggest single source of perceived rudeness; transformer turn detectors cut it to 150–300 ms and use partial-transcript semantics.
15. Q: LiveKit's 2025 turn detector numbers? → A: 85% true-positive rate holding during mid-sentence pauses; 97% true-negative firing on real ends-of-turn. 135M-param model fine-tuned from SmolLM v2.
16. Q: Cartesia Sonic 3.5 TTFA? → A: ~75–90 ms first audio over WebSocket from US-East (GA 2026, out of preview); State-Space-Model architecture.
17. Q: ElevenLabs v2.5 Flash vs v3 positioning (2026)? → A: Flash v2.5 (~75 ms) for real-time calls; v3 — now GA — at ~500–800 ms for expressive produced audio with inline tags like `[whispers]`, `[laughs]`.
18. Q: Deepgram's 2026 STT shift and its enterprise killer feature? → A: **Flux** folds turn detection into the transcription model itself (turn-complete transcripts, no separate VAD/endpointing stitching); Nova-3's `keyterm` prompting still boosts named entities at inference without retraining. Deepgram also ships Aura-2 TTS.
19. Q: OpenAI Realtime pricing (2026)? → A: `gpt-realtime` (GA Aug 2025) was superseded by **GPT-Realtime-2** (May 7 2026): $32/1M audio input ($0.40 cached), $64/1M audio output (~$0.30–0.50/min typical); companion Realtime-Translate $0.034/min and Realtime-Whisper $0.017/min are per-minute. Legacy Beta removed May 12 2026.
20. Q: Anthropic's five workflow patterns? → A: Prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer.
21. Q: The one Anthropic sentence every agent practitioner should memorize? → A: *When building applications with LLMs, we recommend finding the simplest solution possible, and only increasing complexity when needed. This might mean not building agentic systems at all.*
22. Q: Four types of agent memory? → A: Working (context window), episodic (past conversations), semantic (facts about the world), procedural (skills/routines).
23. Q: The complexity test for each memory type? → A: What writes (validated?), what reads (median retrievals?), cost of stale vs cost of missing, could system prompt + current context do the job?
24. Q: TAU-bench pass^1 vs pass^8 on airline? → A: Frontier-class ~60%+ pass^1 collapses to <40% on pass^8 — reliability, not capability, is where production agents fail.
25. Q: BFCL v3 addition? → A: Multi-turn and multi-step function calling; v4 (2025) adds holistic agentic evaluation with refreshed real-world data.
26. Q: The four "shelves" of workflow-engine tooling? → A: A (business-ops SaaS-stitching: Zapier, Make), B (developer-facing self-hostable: n8n, Windmill), C (data/ML orchestration and durable execution: Airflow, Dagster, Temporal), D (agent-framework libraries: LangGraph, CrewAI, Agents SDKs).
27. Q: n8n's AI Agent node sub-nodes? → A: Chat Model, Memory (optional), Tools (0+), Output Parser (optional). Built on LangChain's agent executor.
28. Q: n8n's two MCP nodes? → A: MCP Client Tool (agent calls out to MCP servers) and MCP Server Trigger (n8n workflow exposed as MCP server to external clients).
29. Q: When does Temporal actually beat n8n? → A: Multi-day workflows requiring exactly-once semantics under pod/region failover with saga-pattern compensation — fewer than 5% of real workflow problems.
30. Q: The one-line rule for whether "agent engineering" is installed in a practitioner? → A: They pick workflows when workflows fit, plan-first when the horizon demands it, interleaved when adaptation dominates, *and* they refuse to build an agent at all when a fixed DAG is the right answer.

---

## Further reading

**Must-read (from the six lessons):**
- Anthropic, *Building Effective Agents* (2024-12-20) — https://www.anthropic.com/research/building-effective-agents. The single most operationally useful agent doc. Read before every new agent project. (see Fri/Sat)
- Willison, S., *The Lethal Trifecta for AI Agents* (2025-06) and *MCP has prompt injection security problems* (2025-04) — https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/ and https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/ (see Wed)
- MCP Specification (current stable 2025-11-25; 2026-07-28 stateless-core RC upcoming) — https://modelcontextprotocol.io/specification/2025-11-25/changelog (see Mon/Tue/Wed)
- Yao et al., *ReAct: Synergizing Reasoning and Acting in Language Models* (2022, arXiv 2210.03629) (see Sat)
- OpenAI, *Introducing gpt-realtime* (2025-08-28) and the GPT-Realtime-2 release (2026-05-07) — https://openai.com/index/introducing-gpt-realtime/ (see Thu)
- Anthropic, *Writing Tools for Agents* (2025) engineering post (see Tue)

**Recommended:**
- Parecki, A., *Let's Fix OAuth in MCP* (2025-04) — https://aaronparecki.com/2025/04/03/15/oauth-for-model-context-protocol (see Wed)
- Invariant Labs tool-poisoning and GitHub-MCP exploit posts (2025-04 / 2025-05) (see Mon/Wed)
- Check Point Research disclosure of CVE-2025-59536 and CVE-2026-21852 (see Wed)
- Anthropic, *Code Execution with MCP* (2025) and `sandbox-runtime` repo (see Wed)
- Yao et al., *τ-bench* (arXiv 2406.12045, 2024) and Sierra Research *τ²-bench* (arXiv 2506.07982, 2025) (see Sat)
- SWE-bench Pro (arXiv 2509.16941, 2025) (see Sat)
- Husain, H., *Using LLM-as-a-Judge For Evaluation* (2024-10) — https://hamel.dev/blog/posts/llm-judge/ (see Sat)
- LiveKit Agents + transformer turn detector announcements (2024–2025) (see Thu)
- n8n docs on the AI Agent node, MCP Client Tool, MCP Server Trigger (see Fri)
- Honda, S., *Benchmarking AI Agents: Stop Trusting Headline Scores* (Alan eng blog, 2025) (see Sat)

**Optional / supplementary:**
- Sesame CSM-1B release notes (2025-03-13) (see Thu)
- Cartesia Sonic 3.5, Deepgram Flux/Nova-3, ElevenLabs v3 (GA) model cards (see Thu)
- LangGraph 1.0 release post (October 2025) (see Fri)
- ZenML and OrangeLoops n8n-vs-LangGraph comparisons (2025) (see Fri)
- Delivery Hero and SanctifAI n8n case studies (see Fri)
- AgentSeal scan of 1,808 public MCP servers (Nov 2025) (see Wed)

The six lessons' own citation blocks carry the full URL trails; this section points at the must-reads a reviewer would ask you to have already internalized. For the mid-2026 refresh specifically, add: the Linux Foundation AAIF announcement (MCP + A2A co-governance, Dec 2025), the MCP 2025-11-25 changelog and 2026-07-28 RC, OX Security's "Mother of All AI Supply Chains," and the OpenAI GPT-Realtime-2 release — all cited in Mon/Wed/Thu.

---

## Where you'd still lose points (reviewer lens)

A Willison, a Karpathy, a Huyen, a Liu, or an Anthropic security researcher re-reads this synthesis and pushes back. Here is where they would, and where your own read is probably still thin:

1. **The "runtime selection" framing is a didactic simplification.** Karpathy would point out that in practice MCP-vs-bespoke, pipelined-vs-end-to-end, and workflow-vs-agent are continuous spectra with hybrid options at every level (hybrid voice stacks with parallel text transcription; n8n-outer + LangGraph-inner production pattern; MCP-over-code-execution-sandbox per Anthropic's late-2025 pattern). If your answer to any runtime question is a clean binary, you probably haven't shipped enough of them. Use the dichotomies in this synthesis as starting heuristics, not taxonomies.

2. **You probably have not actually read the spec.** Willison would call this out. Everyone nods at RFC 8707 and RFC 9728 (2025-06-18) and the 2025-11-25 M2M/OIDC additions — few have traced the audience-binding rejection path end-to-end through a real client. If asked "show me the exact place in the handshake where a mis-audienced token is rejected, and which client SDK enforces it," you should be able to produce a file path. If not, spend 30 minutes with the current (2025-11-25) spec this week.

3. **The lethal-trifecta defense stack you wrote above is only as strong as the weakest link — and the weakest link is usually the human.** Huyen would note: permission-prompt fatigue is the single biggest real-world defeater of Layer 4.1; Anthropic's 84%-prompt-reduction target (from the sandboxing launch) is an *admission* of this. If your production deployment relies on the user reading every prompt carefully, you have not deployed a defense.

4. **You did not measure the voice pipeline yourself.** A voice-infra engineer would point out that Thursday's latency tables are industry-typical numbers from vendor pages and a handful of 2025 measurement posts. Until you run your own stack — on a real phone, through a real carrier, with a real accented speaker, with a toddler in the background — you are working off averages. Do the Thursday experiment. The numbers you produce will embarrass the ones you memorized.

5. **You cited benchmarks after claiming not to trust them.** Hamel Husain and the Alan engineering blog author would hold you to the bit: if pass^k collapse is real and prompt-optimization creates 10+ point divergences, then the reason to cite SWE-bench Verified or TAU-bench telecom is *model-selection triage*, not production commitment. Your own 50-example domain eval with LLM-as-judge validated against expert critique shadowing is the only number that justifies a production decision. Build it.

6. **You waved past tool-description integrity.** Invariant Labs' tool-poisoning research shows that tool *descriptions* are part of the model's instruction stream. The week's content mentions it; your mental model probably does not treat descriptions from third-party servers as *adversarially-authored system prompts*. They are. Any mitigation stack that doesn't include "review every tool description on every server I install, and pin server versions" is incomplete.

7. **You did not specify `initialize` behavior under version mismatch.** An MCP contributor would ask what your client does when a server responds with an older `protocolVersion` than requested — speak the older version? disconnect? warn? The spec defines the happy path; client implementations diverge on the edges. If you ship a client, this is your second-day bug.

8. **"Pick by use case" is true and also a cop-out.** A senior product engineer would ask: write down, right now, the three specific signals in a stakeholder ask that swing you from pipelined to end-to-end, or from n8n to LangGraph. If you can't name them in two minutes, "pick by use case" is a rhetorical escape hatch. The mental-move table above is a start; your operator notebook should have your own version with your own engagements in it by the end of this block.

If any of the above felt uncomfortable, it should. That discomfort is the calibrated judgment you are building in this program. Return to the source lessons when you want to close the specific gap.

---

_last_verified: 2026-07-17_
