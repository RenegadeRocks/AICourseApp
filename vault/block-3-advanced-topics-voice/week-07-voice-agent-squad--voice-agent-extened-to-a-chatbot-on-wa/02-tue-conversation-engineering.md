---
type: lesson
block: block-3-advanced-topics-voice
week: week-07
day_of_cycle: 2
day_name: tue
session_slug: voice-agent-squad
date_due: 2026-06-30
tags: [conversation-engineering, turn-taking, endpointing, deepgram-flux, smart-turn, livekit, barge-in, backchanneling, latency-masking, telephony, twilio, containment-rate, resolution-rate, voice-metrics]
sources:
  - deepgram-flux-events-2026
  - pipecat-smart-turn-v3-2025
  - livekit-turn-detector-2025
  - twilio-conversationrelay-flux-2026
  - ihbench-2026
  - cresta-latency-2025
  - twilio-core-latency-2025
  - deloitte-containment-2026
  - famulor-voice-kpis-2026
  - teneo-containment-2026
last_verified: 2026-07-17
word_count_target: 5500
---

# Conversation engineering — turn-taking, interruptions, and the failure modes that make users say "it doesn't listen"

## Why this matters

Every complaint about a production voice agent collapses into one of two sentences: *"it's dumb"* or *"it doesn't listen."* The first is a model problem and it is rare. The second is a conversation-engineering problem and it is the default. Week 2's teardown of a patient-check-in pilot showed the pattern: the model never changed, the pipeline changed four times, and "doesn't listen" tickets dropped 85%. Today you learn the discipline behind that fix as a *design practice*, not a war story — because this week you are shipping a squad, and every seam you add (agent-to-agent handoff, tool call mid-conversation, channel switch to WhatsApp) is a new place for the conversation itself to break.

Conversation engineering is the layer between "the pipeline works" and "the conversation feels human": when to decide the user is done talking, what to do when they interrupt, what the agent does during a 1.8-second tool call, how a phone call differs from a browser session, and — the part almost everyone skips — how to *measure* perceived conversation quality instead of guessing at it. By the end of today you can: (1) design an endpointing strategy using 2026's turn-event models rather than silence timeouts, (2) specify interruption behavior precisely enough that a platform config can implement it, (3) mask tool-call latency without lying to the user, (4) state the telephony-vs-web deltas from memory, and (5) instrument the five metrics that predict whether users will call back.

## Prerequisites

- [[04-thu-voice-agents-architecture|Week 2 Thu]] — the VAD / endpointing / turn-detection distinction and the latency budget table. Assumed cold. One-line recap: VAD asks "is this frame speech?", endpointing asks "did they stop?", turn detection asks "is it my turn?" — and they are different problems with different tools.
- [[01-mon-the-2026-voice-stack|Yesterday]] — the vendor map; today we use Flux, smart-turn, and the platforms without re-introducing them.

## Layer 1 — Turn-taking in 2026: three schools, one API surface

Week 2 established that classical endpointing (VAD + 500–800 ms silence timeout) is the single largest source of perceived rudeness. The 2026 landscape has three genuinely different answers, and — this is the part worth having an opinion on — they disagree about *what signal contains the turn*.

**School 1 — semantic/text-based: LiveKit's transformer turn detector.** A 135M-parameter model reads the *partial transcript* and predicts whether the utterance is complete: "are you going to…" predicts continuation; "…that's all, thanks" predicts completion. LiveKit reports 85% true-positive hold-during-pause and 97% true-negative fire-at-end.[^1] Strength: grammar and pragmatics are strong completion signals. Weakness: the signal arrives only after STT produces text — you inherit STT latency and STT errors, and prosody (the rising pitch of an unfinished list) is invisible.

**School 2 — acoustic/audio-native: Pipecat's smart-turn.** An open model (BSD-2, latest v3 shipped December 2025; v2 covers 14 languages including Hindi) that analyzes the *raw waveform* — intonation, pace, breath — to decide whether the speaker is done, without waiting for a transcript.[^2] The Daily/Pipecat team's argument: humans do turn-taking from tone and rhythm before they've fully parsed the words, so the audio carries the signal earlier than the text does. Strength: no STT dependency, catches prosodic cues. Weakness: no access to semantics — "I need to change my flight from Boston" *sounds* complete and isn't, if the caller was about to say "…to Denver."

**School 3 — joint modeling: Deepgram Flux.** Fold turn detection *into* the STT model, so one network sees both the acoustics and the emerging text and emits turn events directly: `StartOfTurn`, `EagerEndOfTurn`, `TurnResumed`, `EndOfTurn`.[^3] Deepgram's published claims: end-of-turn within ~1.5 s at p95, ~30% fewer interruptions, and 200–600 ms latency reduction versus stitched ASR+VAD+endpointing pipelines.[^3] The event vocabulary is the interesting design contribution — especially `EagerEndOfTurn`: a "probably done, start thinking" signal you can use to begin LLM inference *speculatively*, paired with `TurnResumed` as the "abort, they kept talking" cancellation. That is Week 2's "send partials optimistically" strategy, productized with an explicit state machine instead of your own confidence-threshold hacks. And because Twilio's ConversationRelay now supports Flux natively, this event vocabulary is becoming the default surface on the biggest telephony rail.[^4]

**The live disagreement, named.** Deepgram's position (joint modeling wins because turn-taking needs both signals and a single model kills the stitching latency) versus Daily/Pipecat's position (an open, model-agnostic audio-native detector wins because it composes with *any* STT and keeps you vendor-neutral) versus LiveKit's position (transcript-based detection wins because semantics dominate and the model is tiny enough to run on CPU beside your agent).[^1][^2][^3] Note what the disagreement is really about: **whether turn-taking is a commodity component or a vendor moat.** Deepgram is bundling it to sell STT; Pipecat is unbundling it to commoditize STT. Your decision rule: on a platform (Retell/Vapi/ConversationRelay), take the default — you're buying their tuning. Assembling parts: Flux if Deepgram fits your languages and budget; smart-turn + your STT of choice if you need vendor neutrality or a language Flux lacks. And whichever you pick, keep the eval: turn-detection quality is measurable (interruption rate, false-hold rate), and all three schools' published numbers are self-reported — a caution [[04-thu-voice-agents-architecture|Week 2's reviewer lens]] already flagged for LiveKit's and which applies equally to Deepgram's ~30%.

## Layer 2 — Interruptions: barge-in is a policy, not a feature

Platforms advertise "barge-in support" as a checkbox. In production, barge-in is a *policy space* with four questions you must answer explicitly, because the defaults answer them for you and the defaults are tuned for demos.

**Q1 — What counts as an interruption?** A cough? "Mm-hmm"? "Wait—"? A dog barking? The naive policy — any VAD-positive frame during agent speech cancels playback — makes backchannels ("uh-huh", "okay", "right") kill the agent mid-sentence. Humans backchannel *to signal listening*, not to take the turn; an agent that stops every time the user says "mm-hmm" feels broken in the opposite direction from one that talks over them. The 2026 fix is classification, not thresholds: LiveKit's adaptive interruption handling and Flux's turn events both attempt to distinguish turn-taking speech from backchannel speech.[^1][^3] On platforms you get knobs (minimum interruption duration, interruption-word thresholds); set them per use case — a collections line (users interrupt to object; honor it instantly) tunes opposite to a guided-meditation app (users vocalize constantly; ignore almost everything).

**Q2 — What happens to the abandoned utterance?** When the user cuts off "Your appointment is Tuesday at— ", did they *hear* Tuesday? Your conversation state must record what was actually delivered, not what was generated. The robust pattern: track TTS playback position at cancellation and mark undelivered content as unsaid, so the agent can self-repair ("Sorry — Tuesday the 14th at 3pm") instead of assuming the user has information they never received. Most platform transcripts log *generated* text, not *delivered* audio; this divergence is a real eval blind spot — check what yours logs.

**Q3 — How fast must cancellation propagate?** Week 2 gave the number: within ~100–200 ms across three systems (client playback stop, TTS request cancel, LLM generation cancel). On a cascade the cancellation fans out to three vendors; the failure smell is "the agent finished its sentence over me." Measure it: interruption-to-silence latency belongs in your instrumentation next to first-audio latency.

**Q4 — What happens *after* the interruption?** The most neglected question, and now a benchmarked one: IHBench (2026) evaluates *post-interruption recovery* in voice agents running structured workflows — after a barge-in, does the agent resume the workflow correctly, re-ask what it needs, or lose the thread?[^5] Its existence tells you where the field's pain actually is: not detecting interruptions but *recovering* from them, especially mid-workflow (mid-form-fill, mid-verification). Design rule: every multi-step workflow needs an explicit "where was I, what's still unconfirmed" state that survives an arbitrary interruption at any point. Tomorrow this compounds: a barge-in *during a squad handoff* is the hardest recovery case in the whole architecture.

## Layer 3 — Latency budgets, deepened: masking, speculation, and the tool-call problem

Week 2 decomposed the 800 ms budget stage by stage; take that table as read. Production adds two techniques the napkin doesn't show.

**Speculative execution on `EagerEndOfTurn`.** Begin LLM inference when the turn is *probably* over; if `TurnResumed` fires, discard and re-run with the full utterance.[^3] You pay double inference on resumed turns (typically a small minority) to shave 200–500 ms off every clean turn. On a small-fast LLM the economics are trivially favorable; on an expensive model, meter it. This is the same buy-latency-with-compute trade as speculative decoding, applied at conversation scale — and it's why the Flux event design matters more than its WER.

**Latency masking for tool calls.** A booking lookup takes 900 ms; a CRM write takes 2 s; a payment API takes 4 s. Silence beyond ~1 s reads as failure — Week 2 cited the 40%+ abandonment spike past a second of dead air.[^6] The masking ladder, in order of preference: (1) **acknowledge-then-work**: emit "Let me check that for you" *before* dispatching the tool — the utterance itself buys ~1.5 s of legitimate time; (2) **filler with content**: "Pulling up your account — you said the 14th, right?" masks latency *and* confirms an entity; (3) **progress narration** for known-slow operations: "The payment system usually takes a few seconds…"; (4) **explicit deferral** for anything past ~8 s: "That'll take me a minute — want me to text you?" The anti-pattern is unmasked silence, and the *worse* anti-pattern is looping filler ("one moment… one moment…") which reads as a crashed IVR. Wednesday extends this: in a squad, the handoff itself is a maskable latency event, and the same ladder applies.

**The budget, re-run for each surface.** Web/WebRTC: Week 2's table stands (~500–900 ms achievable end-to-end). Telephony: add 100–200 ms PSTN media legs each way plus codec transcoding; sub-1000 ms is the honest target.[^6][^7] WhatsApp voice notes (Friday's surface): *the budget disappears* — voice notes are asynchronous, so "latency" becomes "response time," the natural threshold moves from 800 ms to tens of seconds, and the entire real-time discipline of this lesson relaxes into something closer to email SLAs. This is the single biggest reason Friday's channel is easier than today's — and why sharing a brain across both channels requires channel-aware behavior, not one config.

## Layer 4 — Measurement: the five numbers that predict whether users call back

Vendors sell demos on naturalness; operators live and die on five instrumented metrics. Wire all five on Saturday.

1. **First-audio latency (p50/p95), per turn.** End-of-user-speech → first agent audio. The p95 matters more than the p50: a conversation with nine 600 ms turns and one 4 s turn is remembered as slow.
2. **Interruption rate, split by direction.** Agent-interrupts-user (endpointing fired early — false end-of-turn) vs user-interrupts-agent (your responses are too long, or your latency provoked a repeat). The *ratio* diagnoses: high agent-interrupts means tune turn detection; high user-interrupts means shorten responses and check masking.
3. **Post-interruption recovery success.** After a barge-in mid-workflow, did the workflow complete without re-asking already-confirmed fields? (The IHBench framing, applied to your own transcripts.)[^5]
4. **Containment rate — with the definitional trap defused.** Containment = calls fully handled without human transfer. The 2026 cross-industry average is ~41% (Deloitte Digital survey), with financial services ~52% and healthcare ~29%; healthy targets are 20–40% early, 40–70% mature.[^8][^9] But containment is gameable — a bot that says "sorry, goodbye" *contained* the call. Pair it always with **resolution rate** (was the issue actually resolved?) and break both down *by intent*: 95% containment on balance checks with 15% on complaints is a healthy system; a flat 60% everywhere is a suspicious one.[^9][^10] This is the same deflection-metric skepticism [[05-fri-case-study-customer-support-agent|Week 3]] drilled for support vendors, now applied to your own agent.
5. **Escalation quality.** When the agent hands to a human, does the human get context (transcript, collected entities, attempted steps) or does the caller start over? "Transfers that restart the conversation" is the top complaint about *partially* automated lines — worse than no automation, because the caller paid the bot toll and then paid the human toll too.

Instrument per-turn events (turn start/end, first-audio, interruptions, tool spans) to your own store — not only the platform dashboard — because per-intent breakdowns and cross-platform migrations both need raw events you own. Saturday's code-lab includes the logging schema.

## Worked example — the conversation spec

Before Saturday's build, write the one-page **conversation spec** for your Monday use case. This is the artifact most teams never write, which is why their barge-in policy is "whatever the platform default was." Sections:

1. **Turn detection**: school (semantic / acoustic / joint / platform default), eagerness setting, and the two user populations that will stress it (e.g., elderly callers with long mid-sentence pauses; non-native speakers).
2. **Interruption policy**: the four Layer-2 questions answered in one line each, including the backchannel list you will *not* treat as barge-in ("okay", "mm-hmm", "right", plus your language/market equivalents).
3. **Latency masking table**: every tool the agent calls, its expected p95, and which rung of the masking ladder covers it.
4. **Surface deltas**: what changes on telephony vs web vs (Friday) WhatsApp.
5. **The five metrics** with your target numbers — defensible ones: early-stage containment targets of 20–40% by intent, not "80% deflection" fantasy.[^8]

If you have 30 spare minutes, run Week 2's latency experiment once more on your current stack, but add two measurements the original omitted: interruption-to-silence latency (interrupt the agent, time the silence) and a deliberate mid-workflow barge-in ("actually wait, change the date") — then read the transcript and grade the recovery yourself. That grade is your first IHBench-style eval row.

## Common mistakes experts see

1. **Tuning endpointing on yourself.** You articulate crisply and pause predictably; your users don't. Week 2's rule, still the #1 field failure: tune on the target population's audio or use model-based detection.
2. **Treating backchannels as barge-ins.** The agent that stops for every "mm-hmm" feels more broken than one that occasionally talks over. Classify, don't threshold.
3. **Logging generated text as if it were delivered audio.** Post-interruption, they diverge — and your agent will reference information the caller never heard.
4. **Masking latency with content-free loops.** "One moment… one moment…" is a crashed IVR. Every masking utterance should carry information or a confirmation.
5. **Reporting containment without resolution, or either without per-intent breakdown.** You will fool yourself first and your client second.[^9][^10]
6. **Designing the escalation path last.** The handoff-to-human experience is part of the conversation, and it is the part your angriest users see.
7. **Assuming turn-taking quality transfers across languages.** Pause patterns, backchannel vocabulary, and prosody are language- and culture-specific; a detector tuned on English will mis-time Hindi or Tamil turns. Check model language coverage (smart-turn v2: 14 languages; Flux Multilingual: 10) before you promise a market.[^2][^3]

## Reflection questions

1. Your agent's metrics show agent-interrupts-user at 2% but user-interrupts-agent at 31%. What are the three most likely causes, in order, and what one-line config change tests each?
2. Speculative execution on `EagerEndOfTurn` doubles LLM cost on resumed turns. Derive the break-even: at what resumed-turn fraction does speculation stop paying, as a function of (latency saved per clean turn) × (value per ms) vs (inference cost per resumed turn)?
3. A caller barges in during the agent's disclosure sentence ("I'm an AI assistant—"). Thursday will make that sentence legally load-bearing in some jurisdictions. What should the interruption policy do, and what does that imply about *where* in the call disclosure belongs?
4. Design the escalation payload: the exact five fields a human agent should see on their screen at transfer time. Which of the five does your current platform actually provide?
5. Why might a *higher* containment rate be worse news than a lower one, for the same intent mix? Give two mechanisms.

## My take (reviewer lens)

**Karpathy** would zero in on the three turn-detection schools' evidence: every accuracy number in Layer 1 is self-published by the vendor whose architecture it flatters, and there is no shared benchmark — no "turn-taking ImageNet" — that would let you compare LiveKit's 85/97 against Flux's "~30% fewer interruptions" against smart-turn at all. He'd say: until someone publishes a cross-vendor eval on identical audio, the school debate is marketing with a citations section, and your only defensible move is the lesson's own hedge — measure interruption rates on *your* traffic. Correct, and it's why the metrics layer is longer than the schools layer.

**Lilian Weng** would push on Layer 2's state framing: the lesson treats interruption recovery as a transcript-bookkeeping problem, but it is really an *agent memory* problem — the conversation state (confirmed entities, delivered information, workflow position) is a working-memory structure that must survive arbitrary preemption, which is the same problem agent architectures face with any interrupt, voice or not. She'd want the conversation spec to define that state schema explicitly rather than gesture at "track playback position." Fair — Saturday's build makes the state schema concrete, and Wednesday's shared-context-across-handoffs section is the same idea one level up.

**A cohort peer** would say the honest thing: "I'm on Retell; I don't control any of this — the platform picked my turn detector and my barge-in policy." True, and the reframe matters: on a platform you don't *implement* conversation engineering, you *evaluate* it — the spec you wrote is your acceptance test, the five metrics are your dashboard, and the knobs the platform does expose (eagerness, interruption sensitivity, masking phrases) are where the spec meets reality. The team that shows up with a conversation spec ships a better agent on the same platform as the team that didn't.

## Further reading

**Must-read**
- Deepgram, Flux docs (turn events, eager end-of-turn thresholds) — the event vocabulary Saturday's build consumes.[^3]
- IHBench (arXiv, 2026) — post-interruption recovery as a first-class eval; skim the task design even if you never run it.[^5]
- Teneo / Famulor containment benchmarking — the containment-vs-resolution trap, with 2026 numbers.[^9][^10]

**Recommended**
- Pipecat smart-turn repo + Daily's v2 write-up — the open, audio-native school; readable model card.[^2]
- LiveKit turn-detection blog — the semantic school's argument, plus honest numbers-with-caveats.[^1]
- Twilio ConversationRelay + Flux changelog — how the event vocabulary lands on telephony.[^4]

**Optional**
- Cresta latency engineering and Twilio core-latency guide — Week 2's must-reads, worth a second pass now that you're specifying rather than learning.[^6][^7]

## Citations

[^1]: LiveKit, "Turn Detection for Voice Agents: VAD, Endpointing, and Model-Based Detection" and "Adaptive Interruption Handling" (2025), https://livekit.com/blog/turn-detection-voice-agents-vad-endpointing-model-based-detection and https://livekit.com/blog/adaptive-interruption-handling — 135M-param transcript-based detector, self-reported 85% TP / 97% TN; adaptive barge-in disambiguation. Canonical technical treatment per [[04-thu-voice-agents-architecture|Week 2 Thu]] (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^2]: Pipecat smart-turn — https://github.com/pipecat-ai/smart-turn and https://huggingface.co/pipecat-ai/smart-turn-v3 (v3, December 2025; BSD-2) ; Daily, "Smart Turn v2: faster inference and 13 new languages," https://www.daily.co/blog/smart-turn-v2-faster-inference-and-13-new-languages-for-voice-ai/ (14 languages incl. Hindi); also served on Cloudflare Workers AI, https://developers.cloudflare.com/workers-ai/models/smart-turn-v2/ and fal, https://fal.ai/models/fal-ai/smart-turn (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^3]: Deepgram Flux — turn events (`StartOfTurn`, `EagerEndOfTurn`, `TurnResumed`, `EndOfTurn`), EOT within ~1.5 s p95, ~30% fewer interruptions, 200–600 ms latency reduction vs stitched pipelines: https://developers.deepgram.com/docs/flux/quickstart and https://deepgram.com/learn/introducing-flux-conversational-speech-recognition ; corroborated by LLMReference, https://www.llmreference.com/model/flux-asr/deepgram and Bolna, https://blog.bolna.ai/deepgram-flux/ ; Flux Multilingual GA April 29, 2026, https://deepgram.com/learn/deepgram-launches-flux-multilingual-press-release (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^4]: Twilio changelog, "Conversation Relay now supports Deepgram Flux + new features," https://www.twilio.com/en-us/changelog/conversation-relay-now-supports-deepgram-flux---new-features — Flux support, improved language detection, SSML controls; HIPAA-eligible/PCI status per https://www.twilio.com/en-us/products/conversational-ai/conversationrelay (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^5]: IHBench: "Evaluating Post-Interruption Recovery in Voice Agents with Structured Workflows" (2026), https://arxiv.org/pdf/2606.19595 — benchmark for whether agents resume structured workflows correctly after barge-in (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^6]: Cresta, "Engineering for Real-Time Voice Agent Latency" (2025), https://cresta.com/blog/engineering-for-real-time-voice-agent-latency ; Retell "Latency Face-Off" and Hamming latency analysis per [[04-thu-voice-agents-architecture|Week 2 Thu]] — 40%+ abandonment spike beyond ~1 s of dead air (search-verified via Week 2 refresh 2026-07-17).

[^7]: Twilio, "Core Latency in AI Voice Agents" (2025), https://www.twilio.com/en-us/blog/developers/best-practices/guide-core-latency-ai-voice-agents — PSTN media-leg and transcoding overhead; sub-1000 ms as the honest telephony target (search-verified via Week 2 refresh 2026-07-17).

[^8]: Pathors, "AI Contact Center KPIs That Actually Matter in 2026," https://pathors.com/en/blog/ai-customer-service-kpi-guide — 2026 Deloitte Digital survey: ~41% average AI voice containment; financial services ~52%, healthcare ~29% (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^9]: Teneo, "Containment Rate Call Centre: Benchmarks & How to Improve It (2026)," https://www.teneo.ai/blog/containment-rate-call-centre-benchmarks-improve-it-2026 — healthy ranges 20–40% early / 40–70% mature; per-intent breakdown guidance (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^10]: Famulor, "AI Voice Agent KPIs: 12 Metrics That Matter in 2026," https://www.famulor.io/blog/ai-voice-agent-kpis-12-metrics-that-matter-in-2026 and Bluejay, "Metrics Every Voice AI Team Should Track," https://getbluejay.ai/resources/metrics-every-voice-ai-team-should-track — resolution-vs-containment misreporting; per-turn instrumentation practice (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

_last_verified: 2026-07-17_
