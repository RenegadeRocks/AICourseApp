---
type: lesson
block: block-3-advanced-topics-voice
week: week-07
day_of_cycle: 3
day_name: wed
session_slug: voice-agent-squad
date_due: 2026-07-01
tags: [voice-agent-squad, multi-agent, triage, handoff, router, orchestrator, vapi-squads, retell-conversation-flow, openai-agents-sdk, context-transfer, cognition, dont-build-multi-agents, tool-calling, latency-masking]
sources:
  - vapi-squads-docs-2026
  - vapi-handoff-docs-2026
  - retell-conversation-flow-2026
  - openai-agents-sdk-voice-2026
  - cognition-dont-build-multi-agents-2025
  - cognition-multi-agents-working-2026
  - langchain-multi-agent-2025
  - anthropic-building-effective-agents-2024
  - openai-realtime-2-1-2026
last_verified: 2026-07-17
word_count_target: 5500
---

# The voice agent squad — triage, handoff, shared context, and the honest case that your squad is ceremony

## Why this matters

Your single voice agent worked at demo scale. Then the client added intents: appointment booking grew a billing question, billing grew an insurance-verification flow, insurance grew a Spanish-language path, and now your one prompt is 3,000 words of competing instructions with 22 tools attached, and reliability is sliding in a way no prompt edit fixes. The industry's 2026 answer is the **squad**: a triage agent that greets and classifies, handing off to narrow specialists that each hold a short prompt and few tools. Vapi ships it as a first-class primitive ("Squads"), Retell ships the same shape as conversation-flow trees and agent transfers, and OpenAI's Agents SDK ships `RealtimeAgent` handoffs for speech-to-speech.[^1][^3][^4]

But there is a serious, named counter-position, Cognition's "Don't Build Multi-Agents," arguing that splitting agents is how you *manufacture* fragility, because context dies at the seams.[^5] Both sides are right about something, and the difference between a squad that raises containment and a squad that drops calls at every handoff is a set of specific engineering decisions this lesson makes explicit: what transfers at a handoff, what the caller hears during one, what happens when they barge into one, and, before any of that, whether your intent map justifies a squad at all. Saturday you build a triage-plus-two-specialists squad; today you design it so it deserves to exist.

## Prerequisites

- [[02-tue-conversation-engineering|Yesterday]]: interruption policy, latency masking, the five metrics. Handoffs inherit all of it.
- [[01-mon-the-2026-voice-stack|Monday]]: platform choices; today references Vapi/Retell mechanics without re-introducing the platforms.
- [[02-tue-agent-architectures|Week 4 Tue — agent architectures]]: the general routing/orchestration patterns; today is those patterns under a 700 ms clock.

## Layer 1 — Why split at all: the reliability mechanics

The argument for splitting is not organizational tidiness; it is three measurable failure curves.

**Prompt interference.** A single prompt serving N intents carries instructions that conflict at the margins ("always verify identity before account details" vs "never delay an emergency booking"). As N grows, the model's per-intent instruction-following degrades: the same context-competition problem context engineering addresses ([[01-mon-context-engineering-the-successor-discipline|Week 6 Mon]]), except on a voice call you also pay the reliability tax in real time, with no retry button the user can see.

**Tool-selection dilution.** An agent choosing among 22 tools mis-selects more than an agent choosing among 5. Anthropic's *Building Effective Agents* names routing as the canonical fix: classify the input, then hand to a downstream configuration with a focused toolset, "separation of concerns" for prompts.[^7] A squad is that routing pattern with audio attached.

**The latency compound.** Voice adds the constraint text agents don't have: every extra reasoning step or tool retry happens inside Tuesday's latency budget. A specialist with a short prompt and five tools produces faster first tokens than a generalist wading through 3,000 words of instructions. Prompt length isn't just a quality variable, it's a TTFT variable. Small specialists are a *latency* optimization before they are a quality one.

The honest threshold: below ~4 distinct intents with mostly-shared tools, a squad buys you ceremony. The split earns its seams when intents need *different* tools, *different* verification postures (billing wants identity checks; FAQ wants none), *different* languages or voices, or *different* escalation rules. Count your intents and their tool/posture matrix before you draw squad diagrams; that matrix is the design input, not the org chart of the client's call center.

## Layer 2 — Topologies: router vs orchestrator, and what the platforms actually give you

**Topology 1: Router (triage → specialist, flat).** One triage agent greets, classifies, optionally collects identity, then hands off. Control *moves*: the specialist owns the call until it ends or re-routes. This is Vapi's Squads model: a squad is a set of assistants plus handoff tools declaring which destinations each assistant may transfer to and when; handoffs can be **silent** (the caller never hears a seam: same voice, no announcement) or announced; destinations can be resolved **dynamically** at runtime via a webhook that returns the target assistant based on your own logic (CRM lookup, business hours, caller history); and squads can even hand off to *other squads*.[^1][^2] Retell reaches the same shape either as **agent transfer** between separate agents or, often better, as a **conversation flow**: one agent whose call-script is an explicit node graph, each node with its own focused prompt, its own knowledge base ("Node KB"), and even its own LLM choice per node.[^3]

**Topology 2: Orchestrator (hub-and-spoke).** A primary agent owns the whole conversation and *delegates* to workers via tool calls, speaking all results itself. In voice, this is the OpenAI Agents SDK's second pattern: a `RealtimeAgent` can hand off (which swaps instructions/tools on the same live session) or can **delegate through tools** to a backend agent (including a heavyweight reasoning model) while the voice agent narrates.[^4] The SDK's constraints are instructive about what a voice handoff *is*: a realtime handoff is a `session.update` (new instructions, new tools, same session, history carried), and you *cannot change the voice mid-session once an agent has spoken*.[^4] The "handoff" is a costume change, not a new actor.

**Choosing.** Router when intents are separable and a call mostly lives in one lane (support lines, booking desks; Saturday's build). Orchestrator when the call *interleaves* competences ("compare my plan against the new one and book the upgrade"), because a router would ping-pong handoffs, which callers experience as being transferred around, the signature failure of human call centers that your client bought AI to escape. The hybrid that shows up in mature deployments: router at the top for lane selection, each lane internally an orchestrator with tool-delegation for its heavy lifting. And note the mapping to a text-agent idea you already know: the router is [[06-sat-build-the-weekly-report-generator|Week 5's]] workflow-vs-agent distinction at conversation scale: predefined control flow where you can get away with it, dynamic delegation only where you can't.

## Layer 3 — The seams: context transfer, the audible handoff, and barge-in across it

The squad's failure modes all live at the seams. Three engineering surfaces:

**1. What transfers.** The worst squad re-asks your name after triage collected it. Every platform gives you a context-transfer control: Vapi's `contextEngineeringPlan` on each destination governs how much conversation history the receiving assistant sees; the Agents SDK carries session history through handoffs by default.[^1][^4] But raw-transcript transfer is often *worse* than nothing at scale: the specialist inherits triage's entire meander, burning its context budget on chit-chat. The robust pattern is **structured handoff state**: a typed payload, `{intent, entities_confirmed, identity_status, sentiment_flag, attempted_steps}`, built by triage and injected into the specialist's context alongside (or instead of) trimmed history. This is Tuesday's conversation-state schema promoted to an interface contract between agents; write it down as a schema, because Saturday's build and Friday's WhatsApp extension both consume it. Silent rule: *anything the caller already said is sacred* — collected once, never re-asked. Measure it: "re-ask rate" per handoff is a squad-specific metric to add to Tuesday's five.

**2. What the caller hears.** Three options, in descending order of seamlessness: **silent handoff** (same voice, no announcement; Vapi supports this natively; the caller experiences one agent with shifting competence)[^2]; **announced continuity** ("let me pull in our billing specialist": same voice or new voice, framed as help arriving, masking the handoff latency with Tuesday's acknowledge-then-work rung); **audible transfer** (new voice, explicit transfer; only when the destination genuinely is different, like a human). Default to silent for specialist routing: callers don't care about your architecture, and announcing internal seams manufactures the "being transferred around" feeling. Exception: when verification posture *changes* ("for billing I need to verify your identity"), announcing the *reason* builds trust even as the handoff stays invisible.

**3. Barge-in across the handoff.** Tuesday's hardest recovery case: the caller interrupts *during* the transfer: "wait, actually it's about a refund, not billing." If the handoff is mid-flight, who handles the correction? Concretely: the handoff must be **atomic and abortable**: either it hasn't committed (triage still owns the call and re-routes) or it has (the specialist receives the correction as its first turn, and its structured-state contract must let it bounce the call back without re-asking anything). What breaks in practice is the half-committed state where the barge-in audio lands on a session whose instructions are mid-swap; test exactly this on Saturday (it's in the build's test script), because it's the seam-failure users describe as "it just ignored me."

**Tool-calling mid-call, squad edition.** Specialists do the heavy tool work (bookings, lookups, payments), which is where Tuesday's masking ladder gets used for real. The squad adds one twist worth designing: triage can *pre-fetch*. If triage knows the caller's number, it can fire the CRM lookup *during its own greeting*, passing results in the handoff payload, so the specialist opens with "I can see your last order…" and the tool latency was hidden inside a seam that was happening anyway. Pre-fetch-on-triage is the single cheapest latency win in the squad pattern.

## Layer 4 — The controversy: when a squad is ceremony

**The skeptic's position, at full strength.** Cognition's June 2025 essay "Don't Build Multi-Agents" (Walden Yan) argues multi-agent architectures are "a tempting idea… quite bad in practice": splitting a task across agents plays telephone with context, decision-making disperses, and reliability collapses at the seams; the durable path is a *single* agent with serious context engineering.[^5] The voice translation of the argument is uncomfortably strong: every handoff is a context bottleneck you built on purpose; the caller's meaning is one continuous thing, and you sliced it. When your billing specialist doesn't know what the caller told triage about their emergency, that's not a bug in your handoff payload — it's the architecture doing what the architecture does.

**The rebuttal, and Cognition's own evolution.** LangChain's response essay ("How and when to build multi-agent systems") makes the pragmatic case: context isolation is a *feature* when subtasks are separable (it is how you keep any one agent's context clean), and the failure Cognition describes is real but belongs to *collaborative writes*, not routed reads.[^6] And by late 2025 Cognition itself published "Multi-Agents: What's Actually Working," conceding a narrower class of viable patterns: multiple agents may contribute intelligence *as long as writes stay single-threaded*: one agent owns the decision stream.[^8]

**Resolution for voice, specifically.** Notice that the working pattern Cognition concedes is *exactly the router squad*: at any moment, one agent owns the conversation (single-threaded writes; the call itself is the write stream), specialists never collaborate simultaneously, and context transfers through a typed contract at discrete seams. The voice squad is not the multi-agent architecture Cognition attacked (parallel agents cooperating on shared output); it is closer to *one agent with hot-swappable configuration*, which is literally the Agents SDK implementation (`session.update`, same session).[^4] So both are right: if your "squad" has agents negotiating with each other mid-call, Cognition's critique applies with full force and you should collapse it; if your squad is a router with structured handoff state, the critique's mechanism (context death at seams) is real but bounded, and you manage it with the Layer-3 contract plus a re-ask-rate metric. The ceremony diagnosis, then, is checkable: **a squad is ceremony when the specialists share the same tools and posture** (then it's one agent wearing hats; collapse it into a conversation-flow graph), and **it's architecture when the tool/posture matrix is genuinely blocked** (then seams pay for themselves).

## Worked example — design your Saturday squad

Produce the **squad spec** (one page + one diagram) for the use case you costed Monday and conversation-spec'd Tuesday:

1. **Intent → tool/posture matrix.** Rows: intents. Columns: tools needed, verification posture, language/voice, escalation rule. If the rows are near-identical: write "single agent, conversation-flow graph" and be done; that's a legitimate output of this exercise.
2. **Topology + platform mapping.** Router or orchestrator, and the concrete mechanism (Vapi squad w/ handoff tools; Retell conversation flow w/ agent transfer; Agents SDK handoffs).
3. **Handoff state schema.** The typed payload, ≤8 fields, with the "sacred, never re-ask" fields marked.
4. **Seam policies.** Silent vs announced per edge; barge-in-during-handoff behavior; pre-fetch-on-triage opportunities.
5. **Squad metrics.** Tuesday's five, plus: re-ask rate per handoff, handoff latency (caller-audible gap), misroute rate (calls a specialist bounces back), and per-specialist containment. Set targets; Saturday measures them.

## Common mistakes experts see

1. **Squad-as-org-chart.** One agent per department because the client has departments. The design input is the tool/posture matrix, not the phone tree you're replacing.
2. **Raw transcript as handoff context.** The specialist drowns in triage's meander. Structured state first, trimmed history second.[^1]
3. **Re-asking collected information.** The single most caller-visible squad failure. Instrument re-ask rate; treat any nonzero value as a bug.
4. **Announcing internal seams.** "Transferring you to our booking assistant" recreates the call-center misery you were hired to end. Silent handoffs for internal routing.[^2]
5. **Ping-pong routing.** Caller bounces triage→billing→triage→bookings because intents interleave. That's the orchestrator's use case; a router forced onto it generates transfers instead of answers.
6. **Untested barge-in-during-handoff.** The half-committed seam is where "it ignored me" lives. Test the interruption at the worst moment, deliberately.
7. **A squad of specialists sharing one prompt's worth of difference.** If you can diff the specialists' prompts in one paragraph, collapse the squad. (This is the Cognition test applied honestly.)[^5]

## Reflection questions

1. Take a real phone menu you've suffered ("press 2 for billing"). Which of its nodes deserve to be squad specialists, which collapse into one conversation-flow agent, and which should remain deterministic IVR? Defend the partition with the tool/posture matrix.
2. The Agents SDK can't change voice mid-session after speech.[^4] What product decisions does that constraint quietly make for you, and when would it force you off the orchestrator topology?
3. Pre-fetch-on-triage hides tool latency inside the handoff seam. What's the failure mode when the pre-fetched data is stale or wrong by the time the specialist uses it, and which of Tuesday's metrics would catch it?
4. Cognition's "single-threaded writes" concession maps to "one agent owns the call at a time." Construct the voice scenario where you'd be tempted to violate it (two agents active simultaneously), and then argue whether the temptation survives the barge-in analysis.
5. Your squad's per-specialist containment is 70/65/20 across three specialists. Walk the diagnosis tree: what are the three structurally different explanations for the 20, and what one-week experiment distinguishes them?

## My take (reviewer lens)

**Lilian Weng** would sharpen Layer 4's resolution: the lesson claims the router squad escapes Cognition's critique because writes are single-threaded, but the *handoff state schema is itself a lossy compression* of the conversation: deciding what goes in the payload is deciding, in advance, what the specialist is allowed to know, and misroutes will trace back to fields you didn't include. She'd push for the schema to be versioned and error-analyzed like any memory system: log every handoff payload, and when a specialist flounders, diff what it knew against what triage knew. That's the right upgrade, and Saturday's logging schema includes the payload for exactly this reason.

**Boris Cherny** would note the tooling pitfall the lesson under-weights: squads multiply *configuration surface*: three assistants × prompts × tools × seam policies on a platform, usually edited in a web console with no diffs, no review, no rollback. His fleet-management instinct: config-as-code from day one (keep squad JSON in the repo, push via API, never hand-edit the console), or your Wednesday-night hotfix to the triage prompt will silently regress the handoff contract. Saturday's build creates the squad via API partly to install this habit.

**Seibel** would ask the revenue question: "Your client's line has 200 calls a day and two intents. You've spent a day on topology theory for a problem a single Retell agent with a good prompt solves this afternoon." Correct, and Layer 1's threshold says so. The steelman for spending today anyway: the reader is one client-growth event away from the 8-intent version, and the expensive mistake isn't building the small thing first; it's building the small thing with no handoff-state schema, so the squad migration later means re-architecting mid-production instead of adding rows to a matrix.

## Further reading

**Must-read**
- Cognition, "Don't Build Multi-Agents": read it *before* you defend your squad spec; if your design can't answer it, simplify.[^5]
- Vapi Squads + handoff docs: the concrete mechanics Saturday uses (handoff tools, silent handoffs, dynamic destinations, `contextEngineeringPlan`).[^1][^2]
- Anthropic, *Building Effective Agents*: the routing pattern; ten minutes to re-read the workflow taxonomy with voice in mind.[^7]

**Recommended**
- Cognition, "Multi-Agents: What's Actually Working" + LangChain, "How and when to build multi-agent systems" — the debate's second round; together they triangulate the resolution used here.[^6][^8]
- OpenAI Agents SDK voice-agents guide — the handoff-as-session.update mental model, and the delegation-through-tools pattern for heavyweight reasoning.[^4]

**Optional**
- Retell conversation-flow blog + docs — the strongest argument that your "squad" might really want to be one agent with a node graph.[^3]

## Citations

[^1]: Vapi, "Introduction to Squads (Multi-Assistant Conversations)," https://docs.vapi.ai/squads — squads as specialized assistants with handoff tools; `contextEngineeringPlan` for controlling transferred history; dynamic handoff destinations via `handoff-destination-request` webhook; squad-to-squad transfers; corroborated by the Vapi docs repo, https://github.com/VapiAI/docs/blob/main/fern/squads.mdx (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^2]: Vapi, "Handoff tool" and "Silent Handoffs," https://docs.vapi.ai/squads/handoff and https://docs.vapi.ai/squads/silent-handoffs — handoff destinations per assistant, assistant overrides, seamless no-announcement transfers (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^3]: Retell, "Single/Multi Prompt Agent Overview," https://docs.retellai.com/build/single-multi-prompt/prompt-overview and "Retell AI's Advanced Conversation Flow," https://www.retellai.com/blog/unlocking-complex-interactions-with-retell-ais-conversation-flow — multi-prompt state trees, conversation-flow node graphs with per-node LLM and Node KB, agent transfers; corroborated by Retell community course materials, https://community.retellai.com/t/lesson-6-agent-types-single-prompt-vs-multi-prompt-vs-conversation-flow/2924 (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^4]: OpenAI Agents SDK, "Voice Agents / Building Voice Agents," https://openai.github.io/openai-agents-js/guides/voice-agents/build/ and RealtimeAgent reference, https://openai.github.io/openai-agents-js/openai/agents-realtime/classes/realtimeagent/ — handoff = `session.update` with new instructions/tools on the same session; history carried; voice cannot change mid-session after an agent has spoken; delegation through tools for reasoning-model backends; corroborated by https://github.com/openai/openai-realtime-agents (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^5]: Walden Yan / Cognition, "Don't Build Multi-Agents" (June 2025), https://cognition.com/blog/dont-build-multi-agents — context fragmentation and dispersed decision-making as the core multi-agent failure; single agent + context engineering as the recommended default; discussed by Jason Liu, https://jxnl.co/writing/2025/09/11/why-cognition-does-not-use-multi-agent-systems/ (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^6]: LangChain, "How and when to build multi-agent systems," https://www.langchain.com/blog/how-and-when-to-build-multi-agent-systems — the pragmatic counter: context isolation as a feature for separable subtasks (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^7]: Anthropic, *Building Effective AI Agents* (December 2024), https://www.anthropic.com/research/building-effective-agents — the routing workflow pattern; canonical treatment per [[06-sat-build-the-weekly-report-generator|Week 5 Sat]] (Tier-1, stable).

[^8]: Cognition, "Multi-Agents: What's Actually Working," https://cognition.com/blog/multi-agents-working — the narrowed position: multi-agent patterns viable when writes stay single-threaded (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

_last_verified: 2026-07-17_
