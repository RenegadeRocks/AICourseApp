---
type: lesson
block: block-3-advanced-topics-voice
week: week-07
day_of_cycle: 1
day_name: mon
session_slug: voice-agent-squad
date_due: 2026-06-29
tags: [voice-agents, speech-to-speech, cascaded-pipeline, openai-realtime, deepgram-flux, cartesia, elevenlabs, vapi, retell, per-minute-economics, vendor-selection, platform-vs-parts]
sources:
  - openai-gpt-realtime-2-1-2026
  - deepgram-flux-multilingual-2026
  - deepgram-aura-2-2025
  - cartesia-sonic-3-5-2026
  - elevenlabs-agents-pricing-2026
  - retell-pricing-2026
  - vapi-pricing-2026
  - gradium-cascade-vs-s2s-2026
  - modulate-black-box-2026
  - twilio-conversationrelay-2026
last_verified: 2026-07-17
word_count_target: 5500
---

# The 2026 voice stack, vendor by vendor — where speech-to-speech actually wins now, and what a minute really costs

## Why this matters

This week you will ship a voice agent squad and then extend it to WhatsApp. Every decision downstream of today — which platform hosts the squad, which STT hears the caller, which TTS answers, whether there is a text layer in the middle at all — is a decision you will make **today**, with money attached. A voice agent at modest scale (10,000 minutes/month — one mid-size clinic's appointment line, one small lender's collections queue) costs between **$65/month and $5,000/month depending entirely on stack choices that produce nearly identical demos.** The demo does not reveal the bill, the compliance posture, or the migration cost. This lesson does.

You already know the pipeline. [[04-thu-voice-agents-architecture|Week 2 Thursday]] taught the components — VAD, endpointing, STT, LLM, TTS, transport — the 800 ms budget decomposition, and the two architectures (cascaded vs end-to-end speech-to-speech). We are not re-teaching any of that. What changed between that lesson's substrate view and today's production view is the *market*: OpenAI shipped two more Realtime generations, Deepgram folded turn-taking into STT and took it multilingual, per-minute platform economics stabilized enough to model, and the speech-to-speech-vs-cascaded argument moved from "wait and see" to positions you can name and bet against. By the end of today you will: (1) hold the current vendor map with July-2026 numbers, (2) run the per-minute economics for three stack configurations against your own use case, (3) defend a build-on-platform vs assemble-from-parts decision to a technical skeptic, and (4) know which numbers in this lesson to re-verify before quoting them to a client — because in this market, three months is a generation.

## Prerequisites

- [[04-thu-voice-agents-architecture|Week 2 Thu — Voice agents architecture]]. Required. This lesson assumes the pipeline diagram, the latency table, and the VAD/endpointing/turn-detection distinction are in your head.
- [[06-sat-rag-evaluation|Week 4 Sat — eval discipline]]. The vendor decision framework below ends in eval gates, not vibes.
- A spreadsheet or a scratch file. The worked example is an economics model you fill in.

## Layer 1 — What moved since the Week 2 napkin

Four shifts, each verified this cycle, each changing a decision you'd have made differently in April.

**1. OpenAI Realtime got a reasoning tier and a cheap tier — in the same week.** On July 6, 2026, OpenAI released **gpt-realtime-2.1** and **gpt-realtime-2.1-mini**: speech-to-speech models with reasoning and tool use, with the mini priced at roughly a third of the flagship on audio ($10/1M audio input tokens vs $32; $20/1M audio output vs $64; cached audio input $0.30/1M on mini vs $0.40 on the flagship), alongside a ≥25% p95 latency reduction across Realtime models via improved caching — median first-token latency now reported sub-300 ms in US/EU regions.[^1][^2] The strategic read: OpenAI is attacking the cascaded pipeline's two remaining moats — cost and tool-calling reliability — simultaneously. The mini tier exists to make "just use Realtime" defensible for business calls, not only consumer companions.

**2. Deepgram Flux collapsed a pipeline stage and went multilingual.** Flux — the conversational STT model that folds end-of-turn detection into transcription itself (introduced October 2025) — hit **Flux Multilingual GA on April 29, 2026**: ten languages, dynamic language switching mid-conversation, $0.0078/min (English-only Flux is $0.0065/min).[^3] Week 2 flagged Flux as "the biggest change to the pipelined stack"; the multilingual GA is what makes it the *default* STT for any deployment touching India, LATAM, or continental Europe — the languages your WhatsApp market speaks. Tuesday's lesson goes deep on its turn events; today, price it.

**3. TTS prices converged; latency stratified.** Deepgram's Aura-2 at $0.030/1k characters, Cartesia Sonic at ~$0.038/1k, ElevenLabs Flash at ~$0.050/1k — the per-character spread is now under 2x.[^4] What still stratifies is latency and expressiveness: Cartesia's Sonic 3.5 claims sub-90 ms first-audio with 42 languages (Sonic Turbo pushes toward ~40 ms), Aura-2 claims sub-200 ms at enterprise concurrency, ElevenLabs holds the expressiveness crown with v3 while Flash v2.5 stays the real-time pick.[^4][^5] Caveat you should carry: the Aura-2 "sub-200 ms" figure is Deepgram's own claim; the independent Gradium benchmark Week 2 cited measured ~313 ms P50 TTFA. Vendor-published and third-party-measured latency routinely differ by 50–100%. Both numbers are honest; they measure different things (model-internal vs network-inclusive). Quote the pessimistic one to clients.

**4. Platform economics stabilized enough to model.** Retell holds at $0.07/min base with ~600 ms out-of-the-box latency and HIPAA included; Vapi holds at a $0.05/min platform fee over bring-your-own components, landing at real all-in costs of $0.13–0.31+/min once STT/LLM/TTS/telephony invoices arrive — and HIPAA is a $1,000/month add-on on Vapi's pay-as-you-go tier.[^6][^7] ElevenLabs Agents runs plan-bundled minutes with $0.08/min overage ($0.16/min burst above your concurrency cap), LLM and telephony billed separately.[^8] These are the same numbers, within noise, that the July 2026 landscape refresh verified — which itself is informative: after two years of chaos, voice platform pricing has found its floor around $0.05–0.08/min for orchestration.

## Layer 2 — The controversy: speech-to-speech vs cascaded, where the positions actually are in mid-2026

Week 2 sketched this argument in its 2025 form. The 2026 form is sharper, and both sides moved.

**Position A — "The cascade won production, and it's not close."** The strongest public statement of this position is Gradium's 2026 architecture analysis: cascaded pipelines dominate production deployments because they solve what enterprises actually buy — control, debuggability, compliance, and predictable cost. Their numbers: cascaded stacks run a predictable $0.0095–$0.17/min at the component level, while speech-to-speech costs span a 182x range and *grow with conversation length*, because every turn re-processes the accumulated audio context as input tokens.[^9] Modulate's enterprise-facing piece — titled, without subtlety, "Beat the Black Box: Why Cascade Beats Speech-to-Speech for Enterprise Voice Agents" — adds the auditability argument: when a voice agent misspeaks, a cascade gives you the exact text at every stage; an S2S model gives you an audio file and a shrug.[^10] The token-accumulation point deserves emphasis because it is the least intuitive: a 10-minute S2S call is not 10× the cost of a 1-minute call — it is materially more, because turn N's input includes turns 1 through N−1. Cached-audio pricing ($0.30–0.40/1M) exists precisely to blunt this, and it helps, but the cost *shape* remains superlinear in call length while a cascade's is linear.

**Position B — "The gap is closing on every axis Position A names."** OpenAI's July release is a point-by-point rebuttal in product form: reasoning and tool use in the voice model (attacking "S2S can't do reliable tools"), a mini tier at roughly a third of flagship audio pricing (attacking cost), sub-300 ms median first-token (extending the latency lead), and caching improvements (attacking the token-accumulation shape).[^1][^2] The naturalness argument hasn't weakened either — prosody, laughter, hesitation still don't survive a text bottleneck. If you extrapolate the 2024→2026 price trajectory, the "S2S is 5–10× more expensive" claim decays fast.

**Where I'd have you land, and why it's more specific than "it depends."** Score your use case on three binary questions. *One:* do you need a durable text transcript as the system of record (healthcare, finance, legal, anything with a regulator)? If yes → cascade; the parallel-transcription workaround for S2S adds cost and still isn't the system of record your auditor wants. *Two:* is voice quality the product (companion, coaching, language learning) rather than a means (booking, support, collections)? If yes → S2S; users pay the premium in retention. *Three:* will median call length exceed ~5 minutes? If yes → cascade or budget for superlinear S2S cost. Two-or-more cascade answers means cascade. This week's build (Saturday) is a cascade on a platform — deliberately, because the squad pattern and the WhatsApp extension both want the text layer. But note the honest wrinkle in Position A's strongest source: Gradium's claim that "no speech-to-speech model is widely available as a production API" is simply too strong — the Realtime API has been GA since August 2025 and runs production consumer workloads today. When a source overclaims in your preferred direction, discount it; I cite Gradium for its cost data, which is corroborated, not its availability claim, which is not.

## Layer 3 — The vendor map, July 2026, with the numbers you'll actually use

All prices search-verified this cycle from at least two independent sources; the tag in each citation marks the verification mode. Treat everything here as having a 90-day half-life.

### Speech-to-speech (end-to-end)

| Vendor / model | Pricing | Latency | The one-line positioning |
|---|---|---|---|
| OpenAI gpt-realtime-2.1 | $32/1M audio in ($0.40 cached), $64/1M audio out | sub-300 ms median first-token (US/EU) | The reference S2S; reasoning + tools in-model[^1][^2] |
| OpenAI gpt-realtime-2.1-mini | $10/1M audio in ($0.30 cached), $20/1M audio out | same family, ≥25% p95 cut | The "make S2S affordable for business calls" play[^1] |
| OpenAI Realtime-Translate / -Whisper | $0.034/min / $0.017/min | streaming | Per-minute companions for translation and STT[^2] |
| Google Gemini Live | per Vertex pricing | competitive | The EU/APAC data-residency alternative (Week 2 covered it; unchanged in role) |

### Cascaded components

| Component | Vendor / model | Pricing | Latency claim | Note |
|---|---|---|---|---|
| STT + turn-taking | Deepgram Flux (EN) | $0.0065/min | end-of-turn median <300 ms, p95 ~1.5 s | Turn detection inside the model[^3] |
| STT + turn-taking | Flux Multilingual | $0.0078/min | same class | 10 languages, mid-call switching; GA Apr 29 2026[^3] |
| TTS | Deepgram Aura-2 | $0.030/1k chars | vendor: sub-200 ms; independent: ~313 ms P50 | Cheapest of the three majors[^4] |
| TTS | Cartesia Sonic 3.5 | ~$0.038/1k chars (≈$0.03/min typical) | sub-90 ms claimed; Turbo ~40 ms | Latency leader, 42 languages[^5] |
| TTS | ElevenLabs Flash v2.5 | ~$0.050/1k chars | ~75 ms model-internal | Quality-per-millisecond leader; v3 for produced audio only |
| LLM | small-fast tier (Haiku 4.5 / Luna / Flash class) | per-token | 200–500 ms TTFT | Week 2's rule stands: big models via tool call, never inline |

### Platforms (orchestration)

| Platform | Base | Real all-in | Latency | Compliance | Pick when |
|---|---|---|---|---|---|
| Retell | $0.07/min | ~$0.13–0.31/min | ~600 ms out of box | HIPAA included | You want managed defaults and a fast path to production[^6] |
| Vapi | $0.05/min platform fee | ~$0.13–0.31+/min | ~500–700 ms tuned | HIPAA = $1,000/mo add-on (PAYG) | You want component control and can absorb five invoices[^7] |
| ElevenLabs Agents | plan minutes + $0.08/min over | ~$0.10–0.50/min by tier | good | — | Voice quality is the product[^8] |
| Twilio ConversationRelay | Twilio pricing + components | varies | optimized | HIPAA-eligible, PCI-compliant | You're already on Twilio telephony; now supports Flux natively[^11] |

Three map-reading notes. *First*, the platform fee is never the bill: Vapi's $0.05/min becomes $0.13–0.31+ once transcription (~$0.01/min), LLM (~$0.02–0.20/min), TTS (~$0.04/min), and telephony (~$0.01/min) stack up — and the invoices arrive separately, from separate vendors, which is itself an operational cost.[^7] *Second*, compliance placement is a pricing mechanism: Retell bundles HIPAA at $0.07/min while Vapi monetizes it at $1,000/month, which means a healthcare workload's breakeven between the two platforms is not where the per-minute comparison suggests. *Third*, Twilio's ConversationRelay adopting Flux matters beyond Twilio: when the largest telephony provider natively integrates a specific STT's turn-taking events, that STT's event vocabulary (Tuesday's topic) becomes a de facto standard.[^11]

## Layer 4 — Platform vs parts: the decision framework with real money

The question every operator asks in week one — "should I build on Vapi/Retell or assemble Pipecat + Flux + Sonic + Twilio myself?" — is a unit-economics question wearing an architecture costume. Model it.

**The worked example.** An appointment-booking line for a dental group: 4,000 calls/month, 3.5-minute average, so 14,000 minutes/month. Three configurations:

**Config A — managed platform (Retell-style).** ~$0.20/min realistic all-in (base + LLM + voice + telephony at defaults).[^6] Monthly: **$2,800**. Engineering: ~2 days to production. You inherit ~600 ms latency, HIPAA, transcripts, a dashboard, and the platform's opinions.

**Config B — orchestrator platform, tuned components (Vapi-style).** Flux ($0.0065) + small-fast LLM (~$0.03 at this call shape) + Sonic 3.5 (~$0.03) + telephony ($0.01) + platform fee ($0.05) ≈ **$0.127/min → $1,780/month**.[^3][^5][^7] Engineering: ~1 week including tuning. You own component choices and can swap any of them; you also own five vendor relationships.

**Config C — raw stack (Pipecat + components, self-hosted orchestration).** Same components minus the platform fee ≈ **$0.077/min → $1,080/month**, plus hosting (~$50–150). Engineering: 2–4 weeks to production parity — barge-in handling, retry logic, telephony edge cases, observability — and permanent ownership of that code.

**The read.** A-to-B saves $1,020/month for a week of work — usually worth it. B-to-C saves $700/month for 2–3 more weeks of work plus permanent maintenance — worth it only past roughly 50,000 minutes/month, or when a requirement (data residency, custom endpointing, a component no platform offers) forces it. The platform fee is not rent, it is salary for an ops engineer you don't hire. This mirrors the framework conclusion the Week 5 build reached about agent frameworks — start managed, migrate on a named trigger, not on principle — and it's why Saturday builds on Vapi or Retell, not raw Pipecat.

**The lock-in counterargument, stated fairly.** Platform lock-in in voice is *real but shallow*: your prompt, tools, eval set, and phone number port trivially; what doesn't port is platform-specific conversation-flow configuration (Retell's node graphs, Vapi's squad JSON) and tuned latency behavior. Budget a re-tuning week for any migration, not a rebuild. The deeper lock-in is the one nobody prices: your *measurement history*. Three months of per-intent containment data on one platform is the asset that makes the next optimization possible, and it does not export cleanly. Start logging to your own store from day one (Saturday's build does).

## Worked example — fill in the vendor-selection worksheet

Take a voice use case you might actually ship — client work, your own product, or the dental line above if you have neither. Produce a one-page artifact with five sections:

1. **Three binary questions** from Layer 2 (transcript-as-record? voice-as-product? calls >5 min?), answered with a sentence of justification each. Architecture verdict.
2. **Monthly minutes estimate** with the arithmetic shown (calls/day × avg minutes × 30).
3. **Configs A/B/C priced** for your minutes, using the Layer 3 tables. Flag every number you copied without re-verifying — that flag is the habit, not busywork.
4. **The migration trigger**: the specific monthly-minutes number or requirement that would move you from your chosen config to the next one.
5. **The three numbers you'd re-verify before a client meeting** (hint: platform base rates move least; S2S token prices and bundled-minute plans move most).

Twenty minutes with Claude Code as a calculator, or a spreadsheet. Keep the artifact; Wednesday's squad design and Friday's channel economics both extend it.

## Common mistakes experts see

1. **Pricing the demo, not the distribution.** Vendor per-minute math at *average* call length hides the tail: 10% of calls at 15 minutes can be a third of your bill, and on S2S the tail is superlinear.
2. **Comparing platform base fees as if they were all-in costs.** $0.05 vs $0.07 is noise; $0.13 vs $0.31 all-in is the real spread, and it's driven by your LLM and TTS choices, not the platform.[^7]
3. **Treating vendor latency claims as end-to-end numbers.** Sub-90 ms TTFA (Cartesia, model-internal) and ~600 ms (Retell, measured end-to-end) are different quantities. Only end-to-end reaches the caller's ear.[^5][^6]
4. **Choosing S2S for a compliance workload and bolting on parallel transcription.** You now pay for both architectures and your "transcript" is a derivative artifact your auditor will question. Cascade from the start.
5. **Assembling the raw stack to save the platform fee at 5,000 minutes/month.** You saved $250 and bought a pager. Do the Layer 4 arithmetic first.
6. **Ignoring cached-audio pricing when modeling S2S.** The $0.30–0.40 cached rates change long-call economics materially; a model that ignores caching overstates S2S cost by 2×+ on realistic call shapes.[^1]
7. **Assuming these numbers hold next quarter.** Between April and July 2026 alone: a new Realtime generation, a Flux multilingual GA, and a p95 latency cut. Re-verify anything older than 90 days before it touches a contract.

## Reflection questions

1. Your use case scored "cascade" on all three Layer 2 questions, but your CEO heard a Realtime demo and wants S2S "because it sounds human." Write the two-paragraph memo: what you'd concede, what you'd measure, and the number that settles it.
2. Vapi monetizes HIPAA at $1,000/month; Retell bundles it. What does each choice tell you about who each platform believes its median customer is — and which platform's incentives align better with yours if you're selling into healthcare?
3. The S2S cost curve is superlinear in call length; the cascade's is linear. For which of your intents is *shortening the call* worth more than *cheapening the minute* — and what does that do to the architecture choice?
4. If Twilio's Flux integration makes Deepgram's turn-event vocabulary a de facto standard, who loses? Sketch the second-order effect on the STT market.
5. Which number in this lesson would you bet is wrong by 2× within six months, and in which direction?

## My take (reviewer lens)

**Karpathy** would go after the numbers' epistemics: half this lesson's latency figures are vendor-published, and the lesson admits vendor-vs-independent gaps of 50–100% — so why present tables at millisecond precision at all? Fair. The defense: operators need *relative* orderings to decide, and the orderings (Cartesia < Aura-2 < Eleven v3; S2S < cascade on latency; cascade < S2S on cost-at-length) are corroborated even where absolute values wobble. But he'd be right that the tables' precision exceeds their accuracy, and you should read them as ordinal.

**Seibel** would say the whole lesson is one paragraph long: "Sign up for Retell, ship the dental line this week, and switch when something hurts. You don't have a vendor-selection problem, you have a shipping problem." He's right for a first build — and Saturday obeys him. The counter is that this week's reader is often quoting a client engagement where the config choice *is* the margin, and Seibel's own case-study discipline (do things that don't scale, but know your unit economics cold) cuts the other way once money flows.

**swyx** would push on framing: the lesson treats "platform vs parts" as static, but the AI-engineering pattern of 2025–26 is that platforms absorb the parts layer within 18 months — Retell/Vapi already bundle what Pipecat assembles, and ConversationRelay is Twilio absorbing the platforms. On that view Config C is not a destination, it's a temporary arbitrage, and the durable skill is the *evaluation harness* that lets you re-platform cheaply — which is exactly why the measurement-history lock-in point may be the most important paragraph in the lesson, and it's buried in Layer 4.

## Further reading

**Must-read**
- OpenAI Realtime API pricing + model pages for gpt-realtime-2.1 / -mini — the primary source for the S2S economics.[^1]
- Gradium, *Cascaded Voice Agents vs Speech-to-Speech: Architecture Tradeoffs in 2026* — Position A at full strength; read with the availability-overclaim caveat.[^9]
- [[04-thu-voice-agents-architecture|Week 2 Thu]] — re-skim the latency table before Tuesday.

**Recommended**
- Deepgram, Flux Multilingual GA announcement (Apr 29, 2026).[^3]
- Devaland / Softcery per-minute cost comparisons — the best independent all-in modeling.[^7]
- Modulate, *Beat the Black Box* — the enterprise-buyer version of Position A.[^10]

**Optional**
- ElevenLabs Agents pricing page — study it as a *pricing design* artifact: bundled minutes, burst pricing, silence discounts.[^8]
- Twilio ConversationRelay changelog — watch this page to see the telephony layer absorb the platform layer in real time.[^11]

## Citations

[^1]: OpenAI, gpt-realtime-2.1 / gpt-realtime-2.1-mini release (July 6, 2026). Pricing: flagship $32/1M audio input ($0.40 cached), $64/1M audio output; mini $10/1M audio input ($0.30 cached), $20/1M audio output — corroborated across MarkTechPost, https://www.marktechpost.com/2026/07/06/openai-gpt-realtime-2-1-mini-reasoning-realtime-api/ ; AlphaSignal, https://alphasignal.ai/news/openai-s-gpt-realtime-2-1-mini-brings-reasoning-and-tool-use-at-6x-lower-cost ; AIReiter, https://aireiter.com/blog/openai-realtime-api-pricing ; OpenAI model/pricing pages, https://developers.openai.com/api/docs/models/gpt-realtime-2.1-mini and https://developers.openai.com/api/docs/pricing (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^2]: TechTimes, "OpenAI Realtime API Cuts Voice Agent Latency 25%, Adds Reasoning Mini Model" (July 7, 2026), https://www.techtimes.com/articles/319860/20260707/openai-realtime-api-cuts-voice-agent-latency-25-adds-reasoning-mini-model.htm — ≥25% p95 latency reduction, sub-300 ms median first-token US/EU; Realtime-Translate $0.034/min, Realtime-Whisper $0.017/min corroborated by TokenMix, https://tokenmix.ai/blog/openai-realtime-voice-api-2026-cost-latency (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^3]: Deepgram, Flux Multilingual GA press release (April 29, 2026), https://deepgram.com/learn/deepgram-launches-flux-multilingual-press-release — 10 languages, dynamic mid-conversation switching, $0.0078/min (English Flux $0.0065/min); corroborated by LLMReference, https://www.llmreference.com/model/flux-asr/deepgram and Yahoo Finance syndication, https://finance.yahoo.com/sectors/technology/articles/deepgram-launches-flux-multilingual-world-123000288.html (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^4]: Deepgram, "Introducing Aura-2" and TTS pricing, https://deepgram.com/learn/introducing-aura-2-enterprise-text-to-speech and https://deepgram.com/pricing — $0.030/1k characters ($0.027 Growth tier), vendor-claimed sub-200 ms at concurrency; vendor's own competitive table lists Cartesia Sonic ~$0.038/1k and ElevenLabs Flash ~$0.050/1k, corroborated by BusinessWire, https://www.businesswire.com/news/home/20250415446781/en/ and CallMissed, https://www.callmissed.com/en/models/aura-2-en . Independent Gradium 2026 measurement of ~313 ms P50 TTFA per [[04-thu-voice-agents-architecture|Week 2 Thu]] citations (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^5]: Cartesia, Sonic 3.5 docs and pricing, https://docs.cartesia.ai/build-with-cartesia/tts-models/latest and https://www.cartesia.ai/pricing — sub-90 ms latency claim, 42 languages, ~$0.03/min typical TTS cost, Sonic Turbo ~40 ms; corroborated by Cekura, https://www.cekura.ai/blogs/best-tts-for-ai-voice-agents and TextToLab, https://texttolab.com/blog/cartesia-pricing (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^6]: Retell pricing: $0.07/min base, phone numbers $2/mo, HIPAA included, ~600–620 ms measured, typical all-in $0.13–0.31/min — https://www.retellai.com/comparisons/retell-vs-vapi and https://www.retellai.com/blog/vapi-ai-review ; corroborated by CloudTalk, https://www.cloudtalk.io/retell-ai-vs-vapi-ai/ and Techsy, https://techsy.io/en/blog/retell-ai-vs-vapi-vs-bland , consistent with the July 2026 vault landscape refresh (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^7]: Vapi economics: $0.05/min platform fee; component stack ~$0.01 STT + $0.02–0.20 LLM + ~$0.04 TTS + ~$0.01 telephony → real all-in ~$0.13–0.31+/min; HIPAA $1,000/mo add-on on pay-as-you-go — F22 Labs, https://www.f22labs.com/blogs/difference-between-vapi-ai-vs-retell-ai-voice-ai-platforms/ ; Devaland, https://devaland.com/blog/voice-ai-pricing-comparison-2025 ; Softcery calculator, https://softcery.com/ai-voice-agents-calculator (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^8]: ElevenLabs Agents pricing: plan-bundled minutes (Free 15 → Business 12,375), $0.08/min overage, $0.16/min burst above concurrency cap, LLM + telephony billed separately, 95% discount on >10 s silence — https://elevenlabs.io/pricing/agents and https://help.elevenlabs.io/hc/en-us/articles/29298065878929 ; corroborated by Cekura, https://www.cekura.ai/blogs/elevenlabs-pricing and Flexprice, https://flexprice.io/blog/elevenlabs-pricing-breakdown (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^9]: Gradium, "Cascaded Voice Agents vs Speech-to-Speech: Architecture Tradeoffs in 2026," https://gradium.ai/content/cascaded-voice-agent-vs-speech-to-speech-2026 — cascade $0.0095–$0.17/min predictable vs S2S 182x cost range growing with conversation length; cascade-dominance framing corroborated by Speko, https://speko.ai/blog/s2s-vs-cascaded and Softcery, https://softcery.com/lab/ai-voice-agents-real-time-vs-turn-based-tts-stt-architecture . Note: its "no production S2S API" claim is contradicted by the GA Realtime API and is not relied on here (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^10]: Modulate, "Beat the Black Box: Why Cascade Beats Speech-to-Speech for Enterprise Voice Agents," https://www.modulate.ai/ebooks/beat-the-black-box-why-cascade-beats-speech-to-speech-for-enterprise-voice-agents — the enterprise auditability/control case for cascades (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^11]: Twilio, ConversationRelay product and changelog — STT/TTS/LLM orchestration over WebSocket; Deepgram Flux support added; HIPAA-eligible and PCI-compliant — https://www.twilio.com/en-us/products/conversational-ai/conversationrelay and https://www.twilio.com/en-us/changelog/conversation-relay-now-supports-deepgram-flux---new-features ; corroborated by Twilio's ConversationRelay evolution blog, https://www.twilio.com/en-us/blog/products/launches/the-evolution-of-conversation-relay (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

_last_verified: 2026-07-17_
