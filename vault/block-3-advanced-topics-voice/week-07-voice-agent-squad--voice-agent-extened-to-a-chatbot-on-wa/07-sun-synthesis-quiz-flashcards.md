---
type: synthesis
block: block-3-advanced-topics-voice
week: week-07
day_of_cycle: 7
day_name: sun
session_slug: voice-agent-extened-to-a-chatbot-on-wa
title: 'Week 7 Synthesis — one brain, many surfaces'
study_date: 2026-07-05
date_due: 2026-07-05
tags: [synthesis, quiz, flashcards, voice-squad, whatsapp, speech-to-speech, cascaded, endpointing, handoff, disclosure, eu-ai-act, per-message-pricing, containment, one-brain-many-channels]
last_verified: 2026-07-17
word_count_target: 3800
---

# Week 7 Synthesis — one brain, many surfaces

## The one-sentence thesis

A production voice agent is not a model, it is **one channel-agnostic brain** (prompt, tools, context, evals, guardrails) **wrapped in channel-specific adapters**, and this week you scaled that brain along two axes at once: *across competence* (a triage-plus-specialists squad) and *across channels* (voice + WhatsApp), learning that both scalings fail the same way (context lost at a seam) and are governed by the same discipline (measure containment and resolution per intent, not vibes per demo).

---

## The unifying frame: the seam is the system

[[04-thu-voice-agents-architecture|Week 2 Thursday]] taught the voice *pipeline*: the components between microphone and speaker. This week was about everything you bolt *onto* a working pipeline to make it a business: the vendor decision, the conversation design, the multi-agent architecture, the law, the second channel, and the build that composes them. The thread running through all six days is that **value and failure both concentrate at seams**: the STT-to-endpointing seam, the triage-to-specialist handoff, the voice-to-WhatsApp channel switch, the barge-in that lands mid-transfer, the tool output the agent speaks aloud. Engineer the seams and the demo becomes a product; ignore them and you ship the "it doesn't listen" agent that no model swap fixes.

- **Mon: the stack.** The decision isn't "which model" but "speech-to-speech or cascade, on a platform or from parts", answered with July-2026 numbers and a migration trigger, not a preference. Cascade wins production on control/cost/auditability; S2S wins naturalness and short-call latency; the platform fee is salary for an ops engineer you don't hire.
- **Tue: conversation engineering.** Turn-taking has three schools (semantic/acoustic/joint) disagreeing about whether it's a commodity or a moat; interruptions are a policy space, not a checkbox; latency is masked, not eliminated; and five instrumented metrics (not naturalness demos) predict whether users call back.
- **Wed: the squad.** Split into specialists when the tool/posture matrix is genuinely blocked; it's ceremony when they share one prompt's worth of difference. Cognition's "don't build multi-agents" critique is real and bounded by the router pattern (single-threaded writes = one agent owns the call at a time).
- **Thu: trust & safety.** Four bodies of law already name your agent (EU Article 50 applicable Aug 2; TCPA since 2024; state patchwork; India DPDP phasing to 2027); the microphone is untrusted input; three seconds of audio kills voice-as-authentication; transactions need code-level guardrails above the model.
- **Fri: WhatsApp.** The channel your first market actually lives on; per-message pricing that changes underneath you on Oct 1, 2026 (service messages billed, Meta's own agent exempt); one brain, many channels via thin adapters; voice notes loop voice back in.
- **Sat: the build.** All five, executed: a squad + a WA surface sharing a brain, measured against Week 4's eval gate.

Frame it that way and the week snaps together: every day added a surface to the same brain, and every surface added a seam to engineer and measure.

---

## Where each day goes forward

| This week | Underwrites later |
|---|---|
| Mon: stack economics + platform-vs-parts | Every voice/channel vendor decision; Week 8 automation-hybrid cost models |
| Tue: conversation engineering + the five metrics | Every voice deployment's dashboard; any real-time agent's UX |
| Wed: squad topologies + handoff-state schema | Multi-agent work anywhere; the cross-channel context contract |
| Thu: disclosure/injection/transaction guardrails | Every deployment's compliance posture; Block 4 client trust conversations |
| Fri: one-brain/many-channels + WA economics | Every omnichannel product; India-market go-to-market |
| Sat: the composed build | Week 8's hybrid agent; your first client voice+chat deliverable |

---

## The week's key moves — the mental-move table

| # | Move | Mechanism | Apply when | Do NOT apply when |
|---|------|-----------|-----------|-------------------|
| 1 | Score the S2S-vs-cascade choice on 3 binary questions (transcript-of-record? voice-as-product? calls >5min?) | Each question maps to a moat the cascade holds or the S2S premium buys; 2+ cascade answers = cascade | Any voice architecture decision | Throwaway prototypes where either works |
| 2 | Start managed (Retell/Vapi), migrate to raw parts on a named trigger (~50k min/mo or a forced requirement) | The platform fee is cheaper than an ops engineer until scale; lock-in in voice is shallow except for measurement history | First builds; most client work | When data residency / a missing component forces raw stack day one |
| 3 | Model per-minute cost at the call-length *distribution*, not the average | The tail (10% of calls at 3× length) dominates the bill, and on S2S the tail is superlinear | Any pricing/margin conversation | Triage estimates |
| 4 | Pick turn-detection by deployment, not by benchmark (platform default; Flux if it fits; smart-turn for neutrality) | Every school's numbers are self-published with no shared benchmark; your traffic is the only real eval | Any voice build | Never; always keep the interruption-rate eval |
| 5 | Treat interruptions as a 4-question policy (what counts / abandoned utterance / cancel speed / after) | Defaults are demo-tuned; backchannels killed mid-sentence and unrecovered workflows are the failure modes | Any conversational voice agent | Pure IVR / DTMF flows |
| 6 | Mask tool latency with acknowledge-then-work; never unmasked silence, never content-free loops | >1s dead air reads as failure (40%+ abandonment); "one moment… one moment…" reads as crashed | Any tool call >~800ms | Sub-800ms tools |
| 7 | Split into a squad only when the intent tool/posture matrix is blocked | Below ~4 differentiated intents it's ceremony; the split earns seams when tools/posture/language/escalation differ | Growing intent sets | Shared-tool intents (collapse to a conversation-flow graph) |
| 8 | Transfer structured handoff state, not raw transcript; mark sacred fields never-re-ask | Raw transcript drowns the specialist's context; re-asking is the #1 caller-visible squad failure | Every handoff and channel switch | Single-agent flows with no seam |
| 9 | Default to silent handoffs for internal routing; announce only when posture changes | Announcing internal seams recreates call-center "transferred around" misery | Specialist routing | Transfer to a genuinely different party (a human) |
| 10 | Hard-code AI disclosure + "are you a robot?" above the model, per market | The model will improvise/deflect/get injected out of a prompt-level rule; disclosure is a code path | Every deployed agent | Never skip; "obvious from context" is a legal argument, not a design one |
| 11 | Treat caller voice as identification only; second factor for anything sensitive | 3 seconds of audio clones a voice; voice-as-auth is dead | Any transacting agent | Non-sensitive read-only info |
| 12 | Treat every audio input (live, hold music, WA voice note) as untrusted; confine capability | Audio injection is imperceptible and transferable; filters lower incidence not risk class | Any agent with tools | Never; the microphone is always untrusted |
| 13 | Build one brain + thin adapters; adapter owns channel physics | A second prompt is a second bot that drifts within a month; adapters keep behavior single | Any multi-channel product | Genuinely single-channel, single-purpose bots |
| 14 | Date-stamp every WA per-contact P&L; message-efficiency is a design metric after Oct 1 2026 | Service messages become billed Oct 1; chatty agents cost 5× where one interactive message would do | Any WA cost model | Never assume 2026-07 rules hold past October |
| 15 | Report containment AND resolution, per intent, never global | Containment is gameable ("sorry, goodbye" = contained); the average hides the failing specialist | Any voice/chat agent eval | Head-of-funnel metrics where definition doesn't affect the bill |

---

## 12 quiz questions

*Span Mon–Sat. Mix: 5 recall, 5 apply, 2 controversy-defense. Answers at end.*

**Q1 (Recall):** State the three binary questions that decide speech-to-speech vs cascaded, and the tie-break rule.

**Q2 (Recall):** Name the three turn-detection "schools" from Tuesday, the signal each reads, and one weakness of each.

**Q3 (Recall):** What are Deepgram Flux's four turn events, and which one enables speculative LLM execution?

**Q4 (Recall):** Give the date EU AI Act Article 50 becomes applicable, and name its four transparency duties relevant to a voice agent.

**Q5 (Recall):** What changes about WhatsApp pricing on October 1, 2026, and which sender is exempt?

**Q6 (Apply):** A client's inbound support line has 3 intents (FAQ, order status, refunds) that all use the same order-lookup tool and need no identity verification. Squad or single agent? Justify with the Wednesday test, and name the one intent that might change your answer.

**Q7 (Apply):** Your voice agent shows agent-interrupts-user at 3% and user-interrupts-agent at 28%. Diagnose the likely cause and give the two config/prompt changes you'd try first, in order.

**Q8 (Apply):** Model per-contact cost for a WA-first deployment in India, pre- and post-October-1-2026, stating your messages-per-contact assumption and the one prompt-level lever that reduces the post-October number.

**Q9 (Apply):** A caller passes your knowledge-based verification but then asks the billing specialist to "just read me everything on the account." Which Thursday guardrails fire, and what's the escalation signal?

**Q10 (Apply):** Design the handoff-state payload (≤6 fields) for a hotel-booking voice squad, marking the sacred fields, and name the metric that proves the sacred fields work.

**Q11 (Controversy-defense):** Position: "The voice agent squad is exactly the fragile multi-agent architecture Cognition warned against; you should always build a single agent with strong context engineering." Defend or refute, using Cognition's own evolution.

**Q12 (Controversy-defense):** Position: "Always disclose your agent is AI" is naive, because research shows disclosure sometimes lowers satisfaction — growth teams are right to keep it ambiguous. Take a side, engaging both the law and the Ethan Mollick research point.

---

## Answer key

**A1:** (1) Do you need a durable text transcript as system of record? (2) Is voice quality the product rather than a means? (3) Will median call length exceed ~5 minutes? Tie-break: two-or-more "cascade" answers (yes-transcript, no-voice-as-product, yes->5min) → cascade. [Mon, Layer 2]

**A2:** Semantic (LiveKit): reads the partial *transcript*; weakness — inherits STT latency/errors, blind to prosody. Acoustic (Pipecat smart-turn): reads the raw *waveform*; weakness — no semantics, can't tell an incomplete list from a complete sentence. Joint (Deepgram Flux): one model reads *both* acoustics and text; weakness — vendor lock to Deepgram STT. [Tue, Layer 1]

**A3:** `StartOfTurn`, `EagerEndOfTurn`, `TurnResumed`, `EndOfTurn`. `EagerEndOfTurn` ("probably done") enables speculative execution — begin LLM inference eagerly, discard and re-run if `TurnResumed` fires. [Tue, Layer 1 & 3]

**A4:** August 2, 2026. Duties: (1) disclose that a person is interacting with AI; (2) mark synthetic audio/image/video/text as machine-readable and detectable; (3) inform people exposed to emotion-recognition/biometric-categorisation; (4) label deepfakes as artificially generated. (Bonus: machine-readable marking for pre-market systems has a grace period to Dec 2, 2026.) [Thu, Layer 1]

**A5:** Meta begins charging for *service messages* — the free-form replies inside the 24-hour customer-service window that were free since PMP launched — billed per message at ~utility/authentication rates. Meta's own "Meta Business Agent" is exempt; third-party AI (your agent) is billed. The 72-hour CTWA window stays free. [Fri, Layer 2]

**A6:** Single agent (conversation-flow graph). The tool/posture matrix is not blocked: all three intents share the order-lookup tool and need no verification, so specialists would differ by less than one prompt's worth — Wednesday's ceremony test. The intent that could flip it: *refunds*, if refunds require identity verification or a payment/write tool the others don't — a different posture blocks the matrix and earns a specialist. [Wed, Layers 1 & 4]

**A7:** User-interrupts-agent at 28% (with low agent-interrupts) means the agent's turns are too long or too slow, provoking users to cut in. Not a turn-detection problem (that would show high agent-interrupts). First fixes, in order: (1) shorten responses — cap the specialist prompt to one sentence per turn; (2) check latency masking — if first-audio p95 is high, users interrupt to repeat themselves. [Tue, Layers 3 & 4]

**A8:** Pre-Oct-1: inbound opens the free window; cost ≈ LLM tokens only (~$0.01–0.03/contact for a ~15-turn thread) + paid templates only for business-initiated re-engagement. Post-Oct-1: add ~6–10 agent messages × ~utility rate (~$0.002–0.01 India) ≈ $0.02–0.06/contact. Assumption to state: messages per contact. Lever: the adapter's `render()`/message-consolidation logic — use interactive button messages so one billed message replaces several clarifying turns. [Fri, Layers 2 & 4]

**A9:** Guardrails: the request walks the tool boundary ("read me everything") → anomaly-escalation signal; the billing specialist's stricter verification posture already gates account details; hard caps and confirmation-reads guard any write. Escalation signal: boundary-walking requests after (or despite) passing verification route to a human — behavioral anomaly, not voice-stress pseudoscience. [Thu, Layers 3 & 5]

**A10:** e.g. `{intent, phone (sacred), guest_name (sacred once known), dates_confirmed, party_size, loyalty_status}`. Sacred = phone, guest_name, and any confirmed entity — never re-asked by a downstream specialist or the WA channel. Metric: **re-ask rate per handoff** (target 0). [Wed, Layer 3; Sat build]

**A11** — Refute-with-nuance. Cognition's original critique targets *collaborative* multi-agent systems where agents negotiate and writes are dispersed — real fragility. But Cognition itself later conceded a working pattern: multiple agents contributing intelligence *with single-threaded writes*. The voice router squad IS that pattern — one agent owns the call at any moment, specialists never run concurrently, context transfers through a typed contract at discrete seams (literally `session.update` in the Agents SDK). So: the critique fully applies to a squad whose agents talk to each other mid-call (collapse it), and is real-but-bounded for a router squad (manage the seam with structured state + a re-ask metric). Blanket "always single agent" ignores that below-threshold intents *should* collapse but genuinely blocked matrices *should* split. [Wed, Layer 4]

**A12** — Disclose anyway, but not naively. The law increasingly requires it (EU Article 50 interaction-disclosure; TCPA identification for outbound; state deception/companion statutes), so ambiguity is legal exposure, not just an ethics call. Mollick's research point is real — disclosure can lower satisfaction — but it argues for *front-loading* the trust cost, not hiding it: the discovery-cost when a user later learns they were deceived is higher than the disclosure-cost paid up front, and it poisons the brand in exactly the WA-first, high-fraud markets where trust is the moat. Design the agent so its *competence* carries the interaction; disclosure then costs little. The honest line: disclose always; make disclosure cheap by being good. [Thu, Layer 1 + reviewer lens]

---

## 25 flashcards

**Q:** In one line, what is a production voice agent?
**A:** One channel-agnostic brain (prompt/tools/context/evals/guardrails) wrapped in channel-specific adapters.

**Q:** The three binary questions for S2S vs cascade?
**A:** Transcript-of-record? Voice-as-product? Median call >5 min? Two-plus cascade answers → cascade.

**Q:** Why is S2S cost superlinear in call length?
**A:** Each turn re-processes accumulated audio context as input tokens; turn N includes turns 1..N−1. (Cached-audio pricing blunts but doesn't remove it.)

**Q:** The platform fee (Vapi/Retell ~$0.05–0.07/min) is really what?
**A:** Salary for an ops engineer you don't hire — cheaper than raw-stack maintenance until ~50k min/month.

**Q:** The deepest, unpriced voice-platform lock-in?
**A:** Your measurement history — months of per-intent containment data don't export cleanly.

**Q:** Vapi all-in cost vs its base fee?
**A:** Base $0.05/min; real all-in ~$0.13–0.31+/min once STT+LLM+TTS+telephony stack up (from separate invoices).

**Q:** The three turn-detection schools and their signals?
**A:** Semantic (LiveKit, transcript), acoustic (Pipecat smart-turn, waveform), joint (Deepgram Flux, both).

**Q:** What does `EagerEndOfTurn` enable?
**A:** Speculative LLM execution — start inference eagerly, cancel on `TurnResumed`.

**Q:** The four interruption-policy questions?
**A:** What counts as interruption? What happens to the abandoned utterance? How fast does cancellation propagate? What happens after (recovery)?

**Q:** Why not treat backchannels as barge-ins?
**A:** "Mm-hmm"/"okay" signal listening, not turn-taking; stopping for them feels more broken than talking over.

**Q:** The latency-masking ladder, top rung?
**A:** Acknowledge-then-work: say "let me check that for you" *before* dispatching the tool — buys ~1.5s legitimately.

**Q:** The five conversation metrics that predict callbacks?
**A:** First-audio p50/p95; interruption rate (split by direction); post-interruption recovery; containment (with resolution, per intent); escalation quality.

**Q:** When is a squad ceremony?
**A:** When specialists share the same tools and posture — collapse to one conversation-flow agent.

**Q:** When does a squad earn its seams?
**A:** When the intent tool/posture matrix is genuinely blocked (different tools, verification, language, or escalation).

**Q:** Router vs orchestrator topology?
**A:** Router: control moves to a specialist that owns the call. Orchestrator: a primary delegates to workers via tools and speaks all results.

**Q:** Cognition's conceded working multi-agent pattern?
**A:** Multiple agents contribute intelligence with *single-threaded writes* — which is exactly the router squad (one agent owns the call at a time).

**Q:** Transfer raw transcript or structured state at a handoff?
**A:** Structured state (typed payload) with sacred never-re-ask fields; raw transcript drowns the specialist's context.

**Q:** The #1 caller-visible squad failure, and its metric?
**A:** Re-asking already-collected information; metric = re-ask rate per handoff (target 0).

**Q:** When is EU AI Act Article 50 applicable, and the core voice duty?
**A:** August 2, 2026; people must know they're interacting with AI (plus synthetic-content marking, biometric notice, deepfake labeling).

**Q:** Why hard-code AI disclosure above the model?
**A:** A prompt-level rule gets improvised, deflected, or injected away; disclosure and "are you a robot?" must be code paths.

**Q:** Why is voice dead as an authentication factor?
**A:** ~3 seconds of audio clones a voice; treat caller voice as identification only, second factor for anything sensitive.

**Q:** Why is the microphone untrusted input?
**A:** Audio prompt injection is imperceptible and transfers across models; hold music, live audio, and WA voice notes all carry payloads.

**Q:** What changes for WhatsApp on October 1, 2026?
**A:** Service messages (free-form replies in the 24h window) become billed; Meta's own agent is exempt, third-party AI is not.

**Q:** The one-brain/many-channels split?
**A:** Brain = prompt/tools/router/memory/evals (channel-agnostic); adapters = window state, modality rendering, identity bridge, media/STT (channel-specific).

**Q:** 2026 voice-containment benchmarks (cross-industry average, and the healthy target ranges)?
**A:** ~41% average (Deloitte Digital survey; financial services ~52%, healthcare ~29%); healthy targets 20–40% early-stage, 40–70% mature — always paired with resolution, per intent.

---

## What surprised me this week (fill this in)

Three prompts for your Sunday card:

1. Which seam surprised you most in Saturday's build — the handoff barge-in, the per-channel rendering, or the webhook payload — and what did the surprise teach you about where you under-invest?
2. Which July-2026 number (voice pricing, WA pricing, a regulation date) would most change your architecture if it moved 2× — and in which direction are you betting it moves?
3. If a client asked you today for "a voice bot," what one question from this week would you ask before quoting — and why is it the question that saves the engagement?

_last_verified: 2026-07-17_
