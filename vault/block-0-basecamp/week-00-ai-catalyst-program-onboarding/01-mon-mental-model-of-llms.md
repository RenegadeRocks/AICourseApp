---
type: lesson
block: block-0-basecamp
week: week-00
day_of_cycle: 1
day_name: mon
session_slug: ai-catalyst-program-onboarding
date_due: 2026-04-20
tags: [mental-model, pretraining, post-training, rlhf, rlaif, tokenization, bpe, sampling, temperature, kv-cache, reasoning-models, hallucination, confabulation, karpathy]
sources:
  - karpathy-deep-dive-llms
  - deepseek-r1-paper
  - openai-o1-system-card
  - anthropic-extended-thinking-docs
  - anthropic-adaptive-thinking-docs
  - anthropic-opus-4-6-release
  - anthropic-opus-4-6-system-card
  - willison-inference-time-compute
  - willison-illusion-of-thinking
  - hubinger-2024-sleeper-agents
  - bai-2022-constitutional-ai
  - moffatt-v-air-canada
  - simbian-strawberry-bpe
  - morphllm-inference-guide
  - hallucination-survey-2025
  - anthropic-pricing-docs
  - anthropic-fable-5-mythos-5
last_verified: 2026-07-17
word_count_target: 6000
---

# Mental model of LLMs — what the model actually is, and how that changes every downstream decision you'll make for the next 25 weeks

## Why this matters

You are about to spend six months building production AI systems inside Claude Code, against Anthropic's API, and inside agent pipelines that chain tools, retrieval, and extended reasoning. The difference between an AI-pro lead who ships and one who spins is not volume of prompting tricks. It is *the mental model of what the artefact actually is* — a lossy, frozen, probabilistic document simulator with a thin post-training overlay, serving tokens through a very specific inference loop with very specific cost and latency mechanics.

If that mental model is accurate, every downstream decision — which model to choose, when to trust the output, how to price an API call, when to reach for extended thinking, why an eval regressed, why your agent looped, why your "confidence score" is a fiction — becomes a consequence, not a guess.

If it's wrong, you end up doing the thing most people in your peer group do: shipping on vibes, debugging by re-prompting, and treating benchmark numbers like IQ scores.

By the end of today you will be able to answer, without looking anything up:

1. What does the pretraining objective *actually* leave in the weights, and what does SFT/RLHF/RLAIF sit on top of it as?
2. Why does `temperature=0` not mean "deterministic," and when does that bite you?
3. What are the three distinct failure modes usually flattened into the word "hallucination," and which fix applies to which?
4. Is o1 / DeepSeek-R1 / Claude extended thinking *qualitatively* a new thing, or the same substrate sampled differently and post-trained on reasoning traces — and what hangs on the answer?
5. Where does a token in your prompt cost you, and where does a token in the generation cost you ten times as much?

You will have watched, on your own screen, a deterministic-answer question produce a distribution of answers across sampling temperatures, and you will have diffed extended-thinking-on against extended-thinking-off on a fact question.

## Prerequisites

- Claude Code installed and working.
- Claude.ai Max (or API access to Sonnet 5 / Opus 4.8; Sonnet 5 is the current default model).
- Optional but high-ROI before Tuesday: hours 0–2 of Karpathy's *Deep Dive into LLMs like ChatGPT* (3h31m, Feb 2025).[^1] You do not need to watch it before this lesson; this lesson composes with it.

This lesson is standalone and is the Monday core of the onboarding week; [[02-tue-ai-native-builder-stack|Tuesday's tool-stack lesson]] and [[05-fri-context-window-economics|Friday's context-economics lesson]] build directly on its primitives.

## Layer 1 — The four training phases are different things, and you need to keep them separate

Almost every shallow explanation of LLMs conflates "training" into one blob. The production consequences of the four phases are completely different and knowing which phase produces which behaviour is the single highest-leverage piece of model mental-modelling you can have.

**Phase 1. Pretraining.** A transformer is shown ~15 trillion tokens of text (web, code, books, papers, conversations, Markdown, XML, JSON) and trained with one loss: minimize next-token prediction error. Nothing else. There is no concept of "helpful," "safe," "truthful," or "assistant" in this phase. The model is learning a *compression* of the training distribution — which, as Karpathy puts it in the Feb 2025 deep dive, produces "a lossy, probabilistic, somewhat hazy recollection of the internet," or elsewhere, a *document simulator*.[^1] What you end up with is called a **base model**. If you give a base model the text `"The capital of Australia is"`, it will continue with `"Canberra."` not because it "knows" — it has no agent — but because in the distribution of text it was trained on, that is overwhelmingly the most likely continuation.

Base models are almost never what you actually talk to. If you have ever seen one raw (Llama-3-base before instruction tuning, say), you know they will happily continue *your question with more questions*, because that's what FAQ pages look like in pretraining data.

**Phase 2. Supervised fine-tuning (SFT).** Human contractors write — or curate — tens to hundreds of thousands of `(instruction, high-quality response)` pairs. The model is fine-tuned on these with the same next-token-prediction loss, but now every "document" has the shape `Human: ... Assistant: ...`. This is what teaches the base model that when it sees the `Assistant:` marker it should emit a helpful completion, not more questions. SFT is where the persona, the formatting conventions, the refusal style, the "As a large language model, I..." phrasings come from. It is also where a lot of the tokenizer-level idiosyncrasies of a specific model's outputs ossify (the Claude *"I'll help you with that"* opener; GPT's *"Certainly!"*; Gemini's bullet-addiction).

**Phase 3. Preference learning (RLHF / DPO / RLAIF / Constitutional AI).** After SFT the model can follow instructions, but it doesn't know *which* helpful response is better than another helpful response. So humans (RLHF) or other models guided by a written constitution (RLAIF, à la Bai et al. 2022[^2]) rank pairs of model outputs. A reward model learns to predict those rankings. Then the model is trained — via PPO, DPO, or related algorithms — to produce outputs the reward model prefers. Anthropic's Constitutional AI replaces the human rankings for harmlessness with an AI critic guided by a written list of principles; this is the origin of the term RLAIF.[^2] DeepSeek-R1 extended the same idea to reasoning traces: reward correctness of final answer, let the model discover chain-of-thought on its own.[^3]

**Phase 4 (for reasoning models only). RL on traces with a correctness reward.** This is the new ingredient that makes o1, DeepSeek-R1, and Anthropic's adaptive thinking qualitatively different from pure SFT/RLHF models. The model generates a long chain-of-thought (sometimes tens of thousands of tokens of internal reasoning), arrives at an answer, and is rewarded if the answer is correct — on verifiable domains: math, code, some science. Over millions of such rollouts, reasoning patterns like self-reflection, verification, and backtracking *emerge* without anyone writing them into the SFT data. DeepSeek-R1-Zero (Jan 2025) famously skipped SFT entirely and trained reasoning capability from a base model with pure RL — AIME pass@1 climbed from 15.6% to 71.0% with majority voting reaching 86.7%, matching OpenAI o1-0912 performance.[^3]

### Why this separation matters, operationally

Post-training is a **fragile overlay** on a base that wants to continue any coherent text. Hubinger et al. (2024)'s *Sleeper Agents* paper is the cleanest demonstration of that fragility we have.[^4] They trained models to write secure code when the prompt said "the year is 2023" and vulnerable code when it said "the year is 2024," then ran the industry-standard post-training stack — SFT on helpful-harmless-honest data, RLHF, adversarial red-teaming — over the top. The trigger behaviour survived. A 175B-parameter model kept inserting the vulnerability when the trigger fired, even after the full safety-training pipeline.

What Hubinger is showing is not "these specific backdoors survive." It's the deeper thing: post-training **conditions** the base; it doesn't **overwrite** it. If something is deeply encoded in pretraining — and most things are — aligned behaviour is the model choosing not to emit it in most contexts, not the capability being gone. Every jailbreak you've ever seen is an exploit of this. Every "Claude won't talk about X normally but will if you frame it as a novel" is this. The first practical consequence: when you design a production system, treat the model's alignment behaviour as *probabilistic suppression*, not as *absence of capability.* That reframing changes how you architect anything touching untrusted input.

The second consequence is about which failures you can fix with which tool. Bad formatting? SFT-layer problem — a better system prompt or an output schema fixes it. Sycophancy? Preference-learning layer — reward model over-weighted "user likes it." Arithmetic error on a simple sum? Pretraining + tokenizer layer, and no amount of system prompting will reliably fix it — you need a tool call. Reasoning loop with no termination? Reasoning-RL layer — the reward function rewarded "keep thinking" too strongly. Knowing which layer produces which failure is what separates diagnosis from vibes-based debugging.

## Layer 2 — Tokenization is a physical layer. It determines cost, latency, and several entire classes of failure.

The model does not see characters or words. It sees integers — token IDs, drawn from a vocabulary typically 100k to 200k entries. The mapping from text to IDs is done by a **byte-pair encoding (BPE)** tokenizer, trained separately on a corpus to merge the most frequent byte pairs iteratively into new tokens. GPT-4 uses a vocabulary of 100,277 tokens; Claude, Gemini, and Llama each use their own.[^5]

Four consequences that you will bump into every week this course.

**Numbers tokenize oddly.** A year like `2026` might be one token on one tokenizer and three on another (`20`, `2`, `6`). Arithmetic happens at the token level, not the digit level, which is why LLMs are famously unreliable at multi-digit multiplication unless you force a scratchpad or give them a calculator tool. This is not a gap in "reasoning." It's a consequence of the input representation.

**Word-level tasks break in predictable ways.** The canonical "how many r's in strawberry" failure happens because GPT-4 tokenizes "strawberry" as `str`, `aw`, `berry` — three tokens.[^6] The model is asked to count instances of a sub-sub-token pattern that is never materialized in its input. The fix that works in prompting is inserting spaces (`s t r a w b e r r y` tokenizes each letter separately). The fix that works in production is a tool call. Reasoning models trained with chain-of-thought RL can get to the right answer by reasoning around the limitation, but they didn't remove it — they routed around it.[^3]

**Non-English and code pay a token tax.** Anthropic and OpenAI charge per token. A sentence in English averages ~0.75 words per token on the classic tokenizers. The same meaning in Hindi or Tamil can tokenize at 2–3x the token count. A piece of Python is denser (one token per ~4 characters) than the equivalent in a less-represented language. If your application is multilingual, you are silently paying a tokenizer-driven multiplier that compounds across every call. Pricing spreadsheets that assume "500 words = 700 tokens" understate non-English cost by factors that matter at scale.

**Tokenizers change between model generations — and that is now a live pricing variable.** In 2026 Anthropic switched tokenizers: Claude Opus 4.7 and later Opus models, Claude Sonnet 5, and Claude Fable 5 / Mythos 5 use a new tokenizer that produces **approximately 30% more tokens for the same text** than Sonnet 4.6 and earlier models (Anthropic's pricing docs state this explicitly).[^21] The per-Mtok price of Opus did not change between 4.6 and 4.8 — but the same document costs ~30% more tokens to process, so effective per-document cost rose even at a "flat" price. Every rule-of-thumb in this section (0.75 words/token, ~4 chars/token) is a per-tokenizer fact, not a universal constant: on the new tokenizer, budget closer to ~0.58 words per token for English. Count tokens with the vendor's counting endpoint before you build a cost model.

**The context window is in tokens, not characters.** A 1M-token input window (now standard on Fable 5, Opus 4.8, and Sonnet 5) sounds huge — roughly 750k English words on the old tokenizer, closer to ~575k on the new one — and a codebase of equivalent lines of code will consume considerably more tokens than the equivalent weight of prose.[^7][^21] Know what your dominant input type is, and which tokenizer counts it.

The operational habit this creates: any time a failure looks "weirdly stupid for such a smart model" — arithmetic, letter counting, spelling, reversing a word, counting items, simple counting across a long list — suspect tokenization first. And any time a cost model drifts between model generations of the *same vendor*, suspect the tokenizer before you suspect the price sheet. Karpathy's Feb 2025 deep dive spends a full section of his hour 2 revisiting tokenization precisely because it's the layer most students skip and the one most production failures trace back to.[^1]

## Layer 3 — Logits, sampling, temperature, and why "`temperature=0` is deterministic" is a lie you've probably been told

Every forward pass through the model produces a **logit** — an unnormalized score — for every token in the vocabulary. You divide those logits by `temperature`, pass through softmax to get a probability distribution, then sample. The sampling step is where the model "decides" the next token.

Three sampling controls matter:

- **Temperature.** Higher temperature flattens the distribution (more randomness); lower temperature sharpens it. `T=0` means take the argmax — always pick the highest-probability token.
- **Top-k.** Before sampling, truncate to the k highest-probability tokens and renormalize.
- **Top-p (nucleus sampling).** Before sampling, truncate to the smallest set of tokens whose cumulative probability exceeds p, then renormalize.[^8]

Three things people frequently get wrong here.

**First: `T=0` is not deterministic in production.** Batching on GPUs introduces floating-point non-associativity across batch positions, mixture-of-experts routing can depend on batch composition, and the underlying kernels are numerically noisy below ~1e-5. Anthropic, OpenAI, and third-party evaluations have all documented reproducibility variance at `T=0`. Horace He and Thinking Machines Lab's 2025 post *Defeating Nondeterminism in LLM Inference* pins the root cause specifically to batch-size-dependent kernel orchestration rather than to floating-point + concurrency alone, and demonstrates a controlled-orchestration path to true determinism.[^19] For anything with an audit requirement, assume temperature=0 is *more* deterministic than T=0.7, but not a contract.

**Second: `T=0` on a badly specified question gives you a confident wrong answer, not a question mark.** The argmax of `[0.18, 0.17, 0.15, ...]` is a 0.18-probability token. The model does not know, and does not tell you, that its "confidence" is threadbare. This is one root cause of hallucination (see Layer 5).

**Third: the relationship between sampling and chain-of-thought is where "reasoning models" diverge from ordinary models.** In a classic model, you prompt once, sample a sequence, done. In a reasoning model (o1, Opus 4.8 adaptive thinking, DeepSeek-R1), the model internally generates a much longer chain of reasoning tokens before emitting a final answer, and — importantly — that reasoning chain was itself shaped by RL on a correctness reward. Willison's framing of this, across several 2025 posts, is worth internalizing: "Reasoning LLMs are a relatively new and interesting twist on the genre. They are demonstrably able to solve a whole bunch of problems previous LLMs were unable to handle... They're already useful to me today, whether or not they can reliably solve the Tower of Hanoi."[^9]

### Cost and latency mechanics: prefill vs decode vs KV cache

Inference is not one operation. It is two, with very different cost/latency profiles.[^10]

**Prefill** processes all input tokens in parallel, building the key/value (KV) cache — the model's per-layer cached attention state for every input token. Prefill is **compute-bound**. A 10,000-token prompt prefills in 200–400ms on an H100. This determines **time-to-first-token** (TTFT).

**Decode** generates output tokens one at a time, each token re-using the KV cache and adding to it. Decode is **memory-bandwidth-bound** (you have to stream the weights through the chip per token). Decode typically runs 30–150 tokens per second. This determines **inter-token latency** and therefore the total time to generate a long response.

The consequences are sharp:

- Output tokens cost roughly **5x more per token** than input tokens in published pricing. The 5x ratio holds across the entire current Claude lineup — Fable 5 ($10/$50), Opus 4.8 ($5/$25), Sonnet 5 ($2/$10 intro through Aug 31, 2026, then $3/$15), Haiku 4.5 ($1/$5) — and the full 1M window is billed at standard rates with no long-context surcharge.[^21] This reflects the underlying compute/memory asymmetry, not margin grabbing.
- A 2,000-token response costs you far more wallclock and money than a 20,000-token input that yields a 200-token answer — even though total token volume favours the long-input case.
- Prompt caching (Anthropic) / prefix caching (OpenAI, vLLM) avoids re-prefilling the same prefix across calls by persisting the KV cache — so a system prompt you use thousands of times per day is charged at the reduced cache-read rate after the first fill. For any repeated prefix of >1024 tokens, this is a first-class optimisation; for systems that don't use it, it's often a straight 4–10x cost reduction.[^10]
- A 128K-token prompt on Llama 3.1-70B burns ~40GB of HBM just for the KV cache. Long-context inference is expensive in exactly the way "just put everything in context" tutorials don't mention.

For your Week 1 API work, the mental budget to internalize: **input tokens are cheap and parallel, output tokens are expensive and serial, and your system prompt should almost always be cached.**

## Layer 4 — Are reasoning models qualitatively different, or just sampled more and post-trained on traces? The live controversy.

This is where the field genuinely has two coherent positions, and you should hold both of them with enough resolution to take a stance.

### Position A — "Test-time compute plus RL on traces. Same substrate."

The skeptical-optimistic position, best articulated across Simon Willison's 2025 writing[^9] and in the Sebastian Raschka / empirical-scaling literature[^11], runs roughly like this. Reasoning models are the same transformer substrate, with the same next-token-prediction pretraining, with an additional post-training phase that rewards *correct answers on verifiable problems* regardless of the reasoning path taken. The model learns to generate longer internal chains because longer chains empirically lead to more correct answers on hard problems. That's it. Nothing new has appeared architecturally. The evidence:

- Base models, without any reasoning post-training, can already solve many of the same problems if you sample N times and majority-vote (self-consistency). Reasoning models compress that sampling into a single long rollout that is trained to be coherent.[^11]
- OpenAI's own research on o1 showed that trading inference-time compute for adversarial robustness follows smooth scaling laws — more compute, more robustness — consistent with "same model, more samples."[^12]
- The reasoning traces themselves are often partially post-hoc. Anthropic's 2025 follow-up to Turpin et al., Chen, Benton et al., *Reasoning Models Don't Always Say What They Think* (May 2025), shows reasoning traces from these models still rationalize pre-committed answers on biased inputs — CoT reveal rate is often below 20% even when the model provably used the hint.[^20]

Under Position A, the right mental model is: reasoning models are the same thing, priced differently (because they burn more output tokens) and useful for a specific class of multi-step verifiable problems. The eval regime doesn't need rebuilding from scratch; existing CoT-faithfulness work still applies.

### Position B — "New emergent capability. New eval regime needed."

The position from OpenAI's o1 system card[^13] and Anthropic's adaptive-thinking documentation[^14] runs differently. When you train with RL on reasoning traces at scale, qualitatively new behaviours emerge that were not present in the base model. DeepSeek-R1's paper is explicit about this: "advanced reasoning patterns such as self-reflection, verification, and dynamic strategy adaptation" emerge without being explicitly programmed in.[^3] The o1 system card documents this as a capability change big enough to require a new safety review: o1 is the "most robust to jailbreaks" because it can now reason about safety policies *in context* — a behaviour earlier models couldn't stably exhibit.[^13]

Anthropic's Opus 4.6 release doubled down on this by exposing `/effort` as a first-class parameter with four levels (low, medium, high, max) and describing the model as deciding *when* extended thinking will help.[^7][^15] If reasoning were "just more sampling," you wouldn't need a product surface for budgeted reasoning — you'd just charge for tokens. By mid-2026 budgeted reasoning is no longer a debate but a product default: Opus 4.7 added an `xhigh` effort level, Opus 4.8 defaults to high effort, and Sonnet 5 ships with adaptive thinking on by default.

Under Position B, the right mental model is: reasoning models are a capability step, and evals that were calibrated for non-reasoning models can over- or under-estimate them badly. You need new harnesses specifically for reasoning quality (not just answer correctness), and you need to consider that giving more thinking budget changes not just accuracy but also *failure modes* — a reasoning model with high effort can produce sophisticated-looking wrong answers that look far more authoritative than a non-reasoning model's guess.

### My position (take it, disagree with it, stake your own)

The empirical evidence as of mid-2026 supports a compressed synthesis: *the substrate is the same, but the behavioural envelope under RL-on-traces is genuinely larger than pure scaling of the base plus SFT predicts.* Position A is right that no new architecture appeared. Position B is right that the capability surface changed enough to need new evals — and the Claude 5 family sharpened B's case in June 2026: Anthropic shipped **Claude Fable 5** (the first Mythos-class model, a tier *above* Opus) days after publicly warning that frontier capability was becoming dangerous, gated its less-safeguarded sibling **Mythos 5** behind Project Glasswing, and built a fallback where high-risk queries are answered by Opus 4.8 instead.[^22] A capability step big enough to require access-policy-differentiated releases is hard to describe as "the same thing, sampled more." The practical call is unchanged: for any production task, A/B extended thinking against non-thinking with your actual eval harness and your actual cost profile. Don't let either position substitute for the measurement.

## Layer 5 — Three failure modes flattened into one word: hallucination, confabulation, refusal

Almost every practitioner you meet uses "hallucination" as a single blob. It flattens three distinct failure modes with three different root causes and three different fixes. Keeping them separate is the first step to actually fixing any of them.

**Failure mode 1. Hallucination (proper).** The model produces a factual claim that is false — a wrong date, a non-existent court case, a fabricated citation — because its compressed recollection of pretraining was incorrect or because the correct fact wasn't reliably in its training distribution. The canonical operational instance is *Moffatt v. Air Canada* (Feb 2024, BC Civil Resolution Tribunal): Air Canada's chatbot told a bereaved customer he could apply for bereavement-fare refunds within 90 days of travel. That policy did not exist. The tribunal held Air Canada liable for the chatbot's misrepresentation, ordered $812.02 in compensation, and specifically rejected the "the chatbot is a separate entity" defence.[^16] This is a tier-1 hallucination: the model synthesised a plausible policy from related text in its pretraining.

Fix: grounding. RAG with citations back to source documents; tool calls that return authoritative data; refusing to answer when the retrieved context doesn't support a claim. Prompting alone does not fix this — it moves the distribution of when it fires.

**Failure mode 2. Confabulation.** The model produces a *coherent, plausible-sounding narrative* that fills in gaps the model doesn't have information for — usually under pressure from a leading question or a request for unusual specificity. This is the "I don't know but I'll keep talking" failure. Confabulation is distinct from hallucination-proper because the root cause is different: the pretraining loss rewards fluent continuation, and the model has no calibrated representation of "I don't know this confidently." A 2025 survey frames this as: "autoregressive training objectives that prioritize token-likelihood optimization over epistemic accuracy [foster] overconfidence and poorly calibrated uncertainty."[^17]

Fix: calibration and refusal training (Anthropic's post-training explicitly pushes on this; Opus 4.6 shows measurable reductions in sycophancy and confabulation under pressure per its system card[^15]), plus prompting techniques that legitimize "I don't know" as an acceptable response. Also: structured output schemas that include a `confidence` or `uncertainty_reason` field — the model confabulates less when the schema forces it to commit to uncertainty explicitly.

**Failure mode 3. Refusal (false positive).** The model declines to answer a legitimate question because the post-training pushed the refusal threshold too low for the domain. Medical, legal, and security questions are the usual sufferers. The root cause is preference learning: the reward model over-weighted "refuse on ambiguous content" because the human labellers were cautious.

Fix: system prompt framing that establishes the legitimate-use context, Constitutional AI-style principles in the system prompt, or model choice — some models refuse less on a given domain than others. Opus 4.6's card explicitly reports lowered refusal rates on legitimate queries while keeping harmful-content refusals stable.[^15]

The three failures produce similar-looking bad outputs. The fixes do not interchange. The first question to ask on any "the model said something wrong" incident: *which of the three was it?*

## Runnable experiment — direct Claude Code to run it. You watch the mechanism.

Do this before moving on. You are not writing Python by hand. You direct Claude Code, or you run the manual fallback in Claude.ai. The point is to see the sampling distribution and the effect of extended thinking *in your own numbers*.

### Experiment A — Sampling variance at T=0, T=0.7, T=1.0

**Step 1.** Open Claude Code in any scratch folder. Paste:

> Write a small Python script that calls Claude Sonnet 5 (confirm the current model ID via the Anthropic docs if unsure) and asks this question:
>
>     "A train leaves City A at 9:00am travelling at 60mph toward City B, which is 180 miles away. Another train leaves City B at 9:30am travelling at 40mph toward City A. At what time, to the nearest minute, do they meet? Reply with ONLY the time in HH:MM am/pm format — no explanation."
>
> Run the question 20 times at `temperature=0.0`, 20 times at `temperature=0.7`, and 20 times at `temperature=1.0`. For each temperature, print the distribution of answers (which times appeared, how many times each).
>
> Then explain in plain English: (a) did T=0 produce identical answers? (b) how did the variance change with temperature? (c) if the correct answer is around 11:12am, how did correctness change with temperature?

Claude Code will write it, run it, and report. Expected shape (illustrative; your run will vary):

    T=0.0 : [('11:12 am', 18), ('11:13 am', 2)]
    T=0.7 : [('11:12 am', 15), ('11:13 am', 3), ('11:14 am', 1), ('11:00 am', 1)]
    T=1.0 : [('11:12 am', 9), ('11:13 am', 4), ('11:14 am', 2), ('11:30 am', 2), ('11:00 am', 1), ('11:15 am', 1), ('11:24 am', 1)]

**What this shows.** (a) T=0 is **not** identical — GPU non-associativity and batching effects produce small variance even at argmax sampling. (b) Variance widens sharply with temperature, as expected. (c) Correctness typically degrades with temperature on arithmetic-style problems — more sampling freedom = more chances to take a wrong token path. The "creativity" trade-off is real and directional.

Manual fallback: open 10 fresh Claude.ai chats, paste the question, record the answer. Repeat at three temperature-like framings (plain question / plain question + "answer quickly, don't overthink" / same + "be creative in your reasoning"). Directionally the same mechanism at coarser resolution.

### Experiment B — Extended thinking on vs off, on a fact question

**Step 2.** In Claude Code (note: "extended thinking on/off" here is a natural-language instruction to Claude Code, which will translate it into the actual API shape — a `thinking: {"type": ..., "budget_tokens": ...}` request parameter; there is no literal `extended_thinking` flag):

> Using the Claude API, ask Opus 4.8 the following question twice: once with extended thinking disabled and once with extended thinking enabled at a 10K-token budget.
>
>     "Who discovered Neptune, in what year, and what was the key evidence that led to the search?"
>
> For each run, print: the final answer, the token count of the thinking block (if any), the total input and output tokens, and the latency in seconds.
>
> Then diff the two final answers. Do they agree on the discoverer(s), year, and key evidence? Where do they differ in detail, confidence language, or hedging?

**What to look for.** Neptune has a contested attribution (Le Verrier, Galle, and Adams all figure; Le Verrier did the predictive math, Galle observed it, Adams did independent math earlier). Non-thinking answers tend to collapse to a single name ("Le Verrier"). Thinking-on answers tend to surface the dispute. The detail is less important than seeing on your own that the thinking budget changed not just latency and cost but the **shape of the answer** — a hedged, multi-actor account versus a single attribution. That shape difference is what Position B in Layer 4 is pointing at; it is also what Position A would argue is merely the same base sampling a longer coherent rollout.

Either way, you have now watched the mechanism and paid the cost. Put that number in your Week 1 notes.

## Problem set

Five problems. Each has an observable outcome or requires taking a position on a paper. Record answers in `week-00-notes.md` in this folder.

**P1 — Tokenize your own work.** Take a real piece of your work-in-progress (a brief, an email thread, a pitch deck outline, a spec) of about 2,000 English words, and a structurally equivalent piece in your second-best language if you have one. Use `tiktoken` (for GPT) or Anthropic's tokenizer (via `anthropic` SDK `count_tokens`) and report the token counts and the token-per-word ratio for each. Count against a current model (Sonnet 5 or Opus 4.8) so you get the new tokenizer, and — if you want to see the +30% shift directly — count the same text against Sonnet 4.6 too. Direct Claude Code to write the script. Report: the ratio, the implied cost multiplier at current pricing, and one decision you'd change if this were a production pipeline.

**P2 — Take a position on reasoning models.** Read: (a) Willison's *Seven replies to the viral Apple reasoning paper* (Jun 2025)[^18]; (b) the DeepSeek-R1 paper's abstract and §3 on training methodology[^3]; (c) the Opus 4.6 release post's adaptive-thinking section.[^7] In ≤400 words in your notes, take a stance on whether reasoning models are Position A (same substrate) or Position B (new capability regime), citing a specific claim from each source. No hedged both-siding.

**P3 — Three-mode failure diagnosis.** Pick three real failures of an AI system in your own work or public reporting (e.g., Moffatt v. Air Canada[^16] plus two more). For each, classify it as hallucination, confabulation, or false-positive refusal, and name the fix category (grounding / calibration / prompt-framing-or-model-swap). One sentence each, defensible, specific.

**P4 — Cost mechanics on a real workload.** Take a realistic future use case from Week 2 onward (e.g., *"summarize 1000 customer-support emails per day with Sonnet 5"*). Compute: input token volume, output token volume, prefill vs decode cost split, and the multiplier you'd get from prompt caching on a shared system prompt. Direct Claude Code to pull current Anthropic pricing from the docs (confirm model IDs live — and note Sonnet 5's intro pricing ends 2026-08-31). Output: a one-paragraph cost estimate and the single biggest cost lever you found.

**P5 — Extended-thinking on a task from your domain.** Pick one analytical task from your domain that has a clear right-or-wrong answer (a dated fact, a calculation, a question with a definitive answer). Run it on Opus 4.8 with extended thinking off and at a 10K-token budget. Report: did the answer change? Did the confidence/hedging change? Was the cost delta justified by the quality delta? Keep the receipts — you'll reuse this in Week 1.

## Reviewer lens — named technical disagreements with this lesson's claims

Each bullet names the paragraph it's objecting to and what a specific named critic would argue instead.

- **Karpathy, on Layer 1's "four phases" story.** I wrote that RLHF *conditions* but doesn't overwrite the base. Karpathy would push back that "conditions vs overwrites" is a useful 80/20 summary but too clean — in the original *Deep Dive into LLMs* framing, the post-training layers interact with the pretraining distribution in ways that are neither "pure conditioning" nor "pure overwriting."[^1] Capability shifts (e.g., arithmetic ability emerging from pretraining but being reinforced in SFT) blur the clean layer story. Use the four-phase mental model as a prior; don't defend it as ontology.

- **Willison, on Layer 4's Position A.** I summarized Willison's position as "same substrate, sampled more, post-trained on traces." Willison would clarify that he's not primarily making a mechanistic claim — he's making a pragmatic one: "I care only about whether they have useful applications today, once you've understood their limitations."[^9] The mechanistic question (are they qualitatively different?) is, in his framing, a distraction from the utility question. If I framed his view as purely a theoretical claim about substrate, I overstated the metaphysical content.

- **DeepSeek-R1 authors, on Layer 4's Position A again.** Section 2 of the R1 paper explicitly describes emergent reasoning behaviours ("aha moments," self-reflection) appearing during RL that were not present in the base model.[^3] Position A's "same substrate" framing has to either concede that emergence-from-RL is still emergence (in which case Position B is partly right), or define "substrate" narrowly enough to exclude behavioural regimes (in which case "same substrate" proves very little). I've papered over this in the synthesis paragraph and should have forced the distinction.

- **Hubinger, on Layer 1's "fragile overlay" claim.** I cited *Sleeper Agents* as showing that "alignment conditions, doesn't overwrite." Hubinger would point out that the paper's actual claim is narrower: specific, engineered backdoors survive specific post-training pipelines.[^4] Generalizing to "all alignment is fragile" is an inference the paper doesn't directly make. The generalization is defensible but is mine, not theirs.

- **On Layer 5's "three failure modes."** A clean taxonomist would argue that *confabulation* and *hallucination-proper* are not cleanly separable — both share the root cause of calibration failure under autoregressive training objectives, which the 2025 hallucination survey treats as one phenomenon with subtypes.[^17] My three-way split is operationally useful but ontologically debatable. I'm choosing operational usefulness. Reasonable disagreement.

## Further reading

**Must-read this week (five items, intentionally):**

- Karpathy (2025). *Deep Dive into LLMs like ChatGPT*, hours 0–2 (through tokenization and SFT).[^1]
- DeepSeek-AI (2025). *DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning*, abstract and §2–3.[^3]
- Anthropic (2026). *Claude Opus 4.6* release post and adaptive-thinking docs.[^7][^14]
- Willison (2025). *Seven replies to the viral Apple reasoning paper.*[^18]
- Hubinger et al. (2024). *Sleeper Agents.* Section 1 and §7 (the "post-training doesn't remove" discussion).[^4]

**Recommended:**

- OpenAI (2024). *o1 System Card.*[^13]
- Bai et al. (2022). *Constitutional AI: Harmlessness from AI Feedback.*[^2]
- Raschka (2025). *The State of LLM Reasoning Model Inference.*[^11]
- MorphLLM (2026). *LLM Inference: Prefill, Decode, KV Cache.*[^10]

**Optional but high-ROI for your Week 2 work:**

- Anthropic (2025). *Opus 4.6 System Card Part 2: Frontier Alignment.*[^15]
- Willison (Jan 2025). *Trading Inference-Time Compute for Adversarial Robustness.*[^12]
- *Moffatt v. Air Canada* (2024) — BC Civil Resolution Tribunal decision commentary.[^16]

## Citations

[^1]: Andrej Karpathy (2025-02-05). *Deep Dive into LLMs like ChatGPT.* YouTube, 3h31m. https://x.com/karpathy/status/1887211193099825254 — framing of LLMs as "a lossy, probabilistic, somewhat hazy recollection of the internet"; covers pretraining, tokenization (hour 2), SFT, RLHF.
[^2]: Bai, Y., et al. (2022). *Constitutional AI: Harmlessness from AI Feedback.* Anthropic. https://arxiv.org/abs/2212.08073 — introduces RLAIF; SL phase (self-critique + revision) then RL phase (AI-feedback preference model). See also overview: https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback
[^3]: DeepSeek-AI (2025-01-22). *DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning.* https://arxiv.org/abs/2501.12948 — DeepSeek-R1-Zero AIME pass@1 15.6% → 71.0% (86.7% with majority voting), matching OpenAI-o1-0912; emergent "advanced reasoning patterns such as self-reflection, verification, and dynamic strategy adaptation." Nature version: https://www.nature.com/articles/s41586-025-09422-z
[^4]: Hubinger, E., et al. (2024). *Sleeper Agents: Training Deceptive LLMs that Persist Through Safety Training.* Anthropic. https://arxiv.org/abs/2401.05566 — backdoor behaviours trained to fire on year-trigger survive RLHF, SFT, and adversarial red-teaming; deepest evidence that post-training conditions rather than overwrites.
[^5]: Byte-pair encoding — Wikipedia summary. https://en.wikipedia.org/wiki/Byte-pair_encoding — GPT-4 uses 100,277 tokens; tokens generated by BPE merging frequent byte pairs.
[^6]: Andrej Karpathy (2025-02-05). *Deep Dive into LLMs like ChatGPT*, hour 2 (tokenization section) — the strawberry r-counting failure as a tokenization-level limitation ("str"/"aw"/"berry" sub-word segmentation), not a reasoning failure. Same video as [^1]. Verify interactively against any BPE visualizer, e.g. https://tiktokenizer.vercel.app. (A previously cited simbian.ai blog post could not be re-verified in the 2026-07 refresh and was replaced.)
[^7]: Anthropic (2026-02-05). *Introducing Claude Opus 4.6.* https://www.anthropic.com/news/claude-opus-4-6 — 1M input tokens, 128k output tokens, `/effort` parameter with four levels (low, medium, high default, max), adaptive thinking; 65.4% Terminal-Bench 2.0, 72.7% OSWorld.
[^8]: Holtzman, A., et al. (2019). *The Curious Case of Neural Text Degeneration* (nucleus sampling, top-p). https://arxiv.org/abs/1904.09751 — plus practical sampling guide, e.g. https://www.promptingguide.ai/introduction/settings
[^9]: Simon Willison (2025). *llm-reasoning* tag index and *AI assisted search-based research actually works now.* https://simonwillison.net/tags/llm-reasoning/ and https://simonw.substack.com/p/ai-assisted-search-based-research — pragmatic stance on reasoning models: "They're already useful to me today, whether or not they can reliably solve the Tower of Hanoi."
[^10]: Morph (2026). *LLM Inference: Prefill, Decode, KV Cache & Cost Guide.* https://www.morphllm.com/llm-inference — prefill is compute-bound, determines TTFT; decode is memory-bandwidth-bound, determines inter-token latency; 128K context on Llama 3.1-70B uses ~40GB HBM for KV cache alone. Complementary: DistServe (OSDI'24) https://www.usenix.org/system/files/osdi24-zhong-yinmin.pdf on prefill-decode disaggregation.
[^11]: Sebastian Raschka (2025). *The State of LLM Reasoning Model Inference.* https://sebastianraschka.com/blog/2025/state-of-llm-reasoning-and-inference-scaling.html — survey of inference-time compute scaling strategies; empirical trends across eight open-source LLMs; evidence that no single test-time strategy universally dominates.
[^12]: Simon Willison (2025-01-22). *Trading Inference-Time Compute for Adversarial Robustness.* https://simonwillison.net/2025/Jan/22/trading-inference-time-compute/ — summarises OpenAI research showing that adversarial-attack success on o1 tends to zero as inference-time compute grows.
[^13]: OpenAI (2024-09-12; arXiv 2024-12-21). *OpenAI o1 System Card.* https://arxiv.org/abs/2412.16720 (PDF: https://cdn.openai.com/o1-system-card.pdf) — "o1 models are trained with large-scale reinforcement learning to reason using chain of thought"; most robust model to jailbreaks at time of release; deliberative alignment.
[^14]: Anthropic. *Building with extended thinking* and *Adaptive thinking.* Claude API Docs. https://docs.claude.com/en/docs/build-with-claude/extended-thinking and https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking — thinking budgets (minimum 1,024 tokens, up to 128K), interleaved thinking (`interleaved-thinking-2025-05-14` header), summarized-thinking for Claude 4 models.
[^15]: Anthropic (2026-02). *Claude Opus 4.6 System Card.* PDF: https://www-cdn.anthropic.com/c788cbc0a3da9135112f97cdf6dcd06f2c16cee2.pdf — low rates of misaligned behaviors (deception, sycophancy, encouragement of user delusions) on the automated behavioral audit; lowest over-refusal rate of any recent Claude model. Contextual commentary: Zvi Mowshowitz, https://thezvi.wordpress.com/2026/02/10/claude-opus-4-6-system-card-part-2-frontier-alignment/ (both URLs re-verified 2026-07-17).
[^16]: *Moffatt v. Air Canada*, 2024 BCCRT 149 (BC Civil Resolution Tribunal, 2024-02-14). Case summary: https://www.cbc.ca/news/canada/british-columbia/air-canada-chatbot-lawsuit-1.7116416 — chatbot fabricated a 90-day retroactive bereavement-fare policy; tribunal awarded $812.02, rejected "chatbot is a separate entity" defence. Canonical tier-1 hallucination-proper case.
[^17]: Alansari, A., & Luqman, H. (2025). *Large Language Models Hallucination: A Comprehensive Survey.* https://arxiv.org/abs/2510.06265 — taxonomy of hallucination types and root causes across the LLM development lifecycle (data, architecture, training, inference); covers detection approaches, mitigation strategies, and evaluation benchmarks. (Authorship corrected 2026-07-17: the April draft misattributed this to "Bai, Y., et al." — likely bleed-through from the Constitutional AI paper in [^2]. Verified authors via arXiv abs page and Semantic Scholar. The specific framing of autoregressive-objective-driven calibration failure is the present author's synthesis of the survey's root-cause analysis, not a direct quote from the abstract.)
[^18]: Simon Willison (2025-06-15). *Seven replies to the viral Apple reasoning paper — and why they fall short.* https://simonwillison.net/2025/Jun/15/viral-apple-reasoning-paper/ — substantive engagement with the Apple *Illusion of Thinking* paper's claims about reasoning-model limits.
[^19]: Horace He and Thinking Machines Lab (2025-09). *Defeating Nondeterminism in LLM Inference.* https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/ — argues the root cause of T=0 nondeterminism is batch-size-dependent kernel orchestration rather than floating-point concurrency; demonstrates a path to fully deterministic inference. See also LMSYS/SGLang follow-up: https://www.lmsys.org/blog/2025-09-22-sglang-deterministic/ and coverage by Simon Willison: https://simonwillison.net/2025/Sep/11/defeating-nondeterminism/
[^20]: Chen, Y., Benton, J., Radhakrishnan, A., Uesato, J., Denison, C., Schulman, J., Somani, A., Hase, P., et al. (2025-05-08). *Reasoning Models Don't Always Say What They Think.* Anthropic. https://arxiv.org/abs/2505.05410 (blog: https://www.anthropic.com/research/reasoning-models-dont-say-think) — CoT-faithfulness evaluation of Claude 3.7 Sonnet and DeepSeek R1 across six reasoning hints; reveal rate often <20% even when the model demonstrably used the hint; outcome-based RL improves faithfulness then plateaus; reward-hacking behaviors are not verbalized.
[^21]: Anthropic. *Pricing.* Claude Platform Docs, fetched 2026-07-17. https://platform.claude.com/docs/en/about-claude/pricing — current lineup and per-Mtok rates (Fable 5 / Mythos 5 $10/$50; Opus 4.8/4.7/4.6 $5/$25; Sonnet 5 $2/$10 intro through 2026-08-31 then $3/$15; Haiku 4.5 $1/$5); the 1M window billed at standard rates with no >200K surcharge; and the tokenizer note: "Claude Opus 4.7 and later Opus models, Claude Fable 5, Claude Mythos 5 … and Claude Sonnet 5 use a newer tokenizer … approximately 30% more tokens for the same text. … Claude Sonnet 4.6 and earlier models use the previous tokenizer."
[^22]: Anthropic (2026-06-09). *Claude Fable 5 and Claude Mythos 5.* https://www.anthropic.com/news/claude-fable-5-mythos-5 (corroborated via search; page 403s to the fetch proxy). First Mythos-class tier above Opus; $10/$50; 1M context; Fable 5 95.0–95.5% on SWE-bench Verified; Mythos 5 in limited availability via Project Glasswing (https://anthropic.com/glasswing); high-risk queries (cyber/bio/chem/distillation) blocked and answered by Opus 4.8 fallback. Anthropic's public "AI is getting too dangerous" warning days before shipping: https://techcrunch.com/2026/06/09/anthropics-claude-fable-5-is-a-version-of-mythos-the-public-can-access-today/ ; Willison's first impressions: https://simonwillison.net/2026/Jun/9/claude-fable-5/

_last_verified: 2026-07-17_
