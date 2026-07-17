---
type: lesson
block: block-0-basecamp
week: week-00
day_of_cycle: 5
day_name: fri
session_slug: ai-catalyst-program-onboarding
date_due: 2026-04-24
tags: [context-window, tokens, pricing, prompt-caching, kv-cache, long-context, ruler, nolima, lost-in-the-middle, extended-thinking, rag, economics]
sources:
  - anthropic-prompt-caching-2024-08
  - anthropic-pricing-docs
  - anthropic-1m-context-ga
  - anthropic-contextual-retrieval-2024-09
  - anthropic-extended-thinking-docs
  - google-gemini-pricing
  - openai-pricing
  - liu-2023-lost-in-the-middle
  - hsieh-2024-ruler
  - modarressi-2025-nolima
  - jxnl-context-engineering-2025
  - lighton-rag-is-dead-long-live-rag
  - anthropic-pricing-docs-2026-07
last_verified: 2026-07-17
word_count_target: 6000
---

# Context window economics — what tokens actually cost, what a 1M window really gives you, and when caching wins

## Why this matters

You are about to start Week 1. You will spend the next six months pointing Claude Code at real codebases, running Claude.ai against 200-page PDFs, stuffing RAG pipelines with retrieved chunks, and routing long transcripts through agents that reason, tool-call, and reason again. Every one of those actions has a unit cost measured in tokens — and a unit *quality* measured by how well the model actually uses the tokens you shove into its context.

Most AI-pro leads lose money and lose quality in the same place: they treat the context window as free memory. It is not. It is a rate-limited, quality-degrading, provider-specific resource whose pricing changes monthly and whose *useful* capacity is strictly smaller than the advertised number on the model card. Opus 4.8, Sonnet 5, and Fable 5 all advertise 1M; so does Gemini 3.1 Pro. On controlled benchmarks (RULER, NoLiMa) every frontier model loses 20-60 percentage points of accuracy somewhere between 32K and 200K — long before you hit the advertised ceiling.[^1][^2] And a subtler trap since 2026: the new Anthropic tokenizer means the *same document* now consumes ~30% more of that window than it did on Sonnet 4.6, so both your quality budget and your cost math shifted under you.

This lesson is the economics you should have had before your first production prompt. By the end of it you will:

1. Price a token in your head for the four providers you actually use, and know which direction the output-to-input ratio cuts on each.
2. Know what "1M context" means operationally — including that Anthropic bills the full 1M window at standard rates (no >200K surcharge) while Gemini still steps at 200K.[^3]
3. Be able to predict when long-context retrieval will silently degrade by citing Liu 2023, Hsieh 2024, and Modarressi 2025 by result, not just by name.[^4][^1][^2]
4. Have the prompt-caching mental model cold — cache writes cost 1.25× (5-min) or 2× (1-hour), cache reads cost 0.10×, break-even is **one** read for the 5-min cache and **two** for the 1-hour cache, and the breakpoint is positional.[^5]
5. Have taken a defensible position on the "RAG is dead, long context wins" debate, grounded in a specific Anthropic result (49% / 67% on Contextual Retrieval) and Jason Liu's context-engineering framing.[^6][^7]
6. Have watched, on your own screen, a single fact placed at 5 / 50 / 95% of a 200K-token prompt be retrieved at dramatically different rates — because you will have directed Claude Code to run the experiment.

This builds directly on [[01-mon-mental-model-of-llms|Monday's tokenization and prefill/decode mechanics]] and [[02-tue-ai-native-builder-stack|Tuesday's per-tool cost axis]]. Bring these mechanics into Week 1.

## Prerequisites

- Claude.ai access (Max tier is fine) and Claude Code installed in a scratch folder.
- An Anthropic API key with at least $5 of credit on it. The experiment will spend roughly $0.40-$1.50 depending on which version you run. You will not write Python by hand; you will direct Claude Code to build, run, and explain.
- Comfort reading a pricing table. That is genuinely the hardest prerequisite.

## Layer 1 — Tokens as currency: the asymmetry nobody flags loudly enough

A token is not a word and not a character. For English text on the classic tokenizers it is roughly 0.75 words, or about 4 characters; on Anthropic's new tokenizer (Opus 4.7+, Sonnet 5, Fable/Mythos 5) the *same* English is ~30% more tokens, so budget closer to ~0.58 words per token there. Code ranges from 2 to 5 characters per token. All frontier providers bill in tokens, charge separately for **input** and **output**, and charge output at a large multiple of input.

Here is the pricing table that matters as of the currency-stamp on this lesson (2026-07-17). Standard tier, no cache, no batch discount. Per million tokens, USD.[^8][^9][^10]

| Model | Input $/MTok | Output $/MTok | Output/Input ratio | Max context | Tokenizer |
|---|---|---|---|---|---|
| Claude Fable 5 / Mythos 5 | 10.00 | 50.00 | 5.0× | 1M | new (+~30%) |
| Claude Opus 4.8 | 5.00 | 25.00 | 5.0× | 1M | new (+~30%) |
| Claude Sonnet 5 (intro, ≤Aug 31 2026) | 2.00 | 10.00 | 5.0× | 1M | new (+~30%) |
| Claude Sonnet 5 (from Sep 1 2026) | 3.00 | 15.00 | 5.0× | 1M | new (+~30%) |
| Claude Haiku 4.5 | 1.00 | 5.00 | 5.0× | 200K | classic |
| GPT-5.6 Sol | 5.00 | 30.00 | 6.0× | 1.05M | — |
| GPT-5.6 Terra | 2.50 | 15.00 | 6.0× | 1.05M | — |
| GPT-5.6 Luna | 1.00 | 6.00 | 6.0× | 1.05M | — |
| Gemini 3.1 Pro (≤200K in) | 2.00 | 12.00 | 6.0× | 1M | — |
| Gemini 3.1 Pro (>200K in) | 4.00 | 18.00 | 4.5× | 1M | — |
| Gemini 3.5 Flash | 1.50 | 9.00 | 6.0× | 1M | — |

Sources: Anthropic pricing docs, OpenAI pricing, Google Gemini API pricing, all fetched 2026-07-17.[^8][^9][^10]

Four things in this table deserve to be burned in:

**The output ratio is not 1×. It is almost never 2×. It is between 4.5× and 6×.** The expensive part of any call is not the 200K-token codebase you attach — it is the 3,000-token diff or explanation the model writes back. An Opus 4.8 call with 100K input and 3K output costs $0.50 for input and $0.075 for output — double the output to 6K and you've added another $0.075 against a $0.50 input that didn't move. For any workflow where outputs can grow — code generation, long-form writing, extended thinking, agent loops — output is the variable you optimize first.

**Anthropic has no long-context surcharge; Gemini still steps at 200K.** Anthropic bills the full 1M window at standard rates — a 900K-token request costs the same per token as a 9K one — for Fable 5, Opus 4.8/4.7, Sonnet 5, and Sonnet 4.6.[^3] Gemini 3.1 Pro retains a cliff: $2.00/$12.00 up to 200K prompt, $4.00/$18.00 above it.[^10] And OpenAI, which had *dropped* to a 400K window with GPT-5, went back to ~1M with GPT-5.5 in April 2026 and carries a >272K-input surcharge on some tiers — so the "only Gemini has a cliff" story from April is no longer clean.

**The cheapest input token is not the cheapest call.** Sonnet 5's $2 intro input beats Opus 4.8's $5 by 2.5× on paper; once you factor output, cache hits (Anthropic reads at 0.10× input), and the ~30% tokenizer tax that hits *both* Anthropic models equally, the real comparison is workload-shaped. Pricing comparisons that cite a single number per model are useless. Build the mental model around ratios, not absolutes — and always date-stamp Sonnet 5 quotes, since its intro price expires 2026-08-31.

An example to sharpen the point. You're running a nightly code-review agent. Every run: 80K tokens of code and test diff in, 4K tokens of review out. No cache yet. 30 runs/month. (Token counts here are on the new tokenizer; the same source text would have been ~30% fewer tokens on Sonnet 4.6.)

- On Opus 4.8: (80K × $5 + 4K × $25) / 1M × 30 = $15.00/month.
- On Sonnet 5 (intro $2/$10): (80K × $2 + 4K × $10) / 1M × 30 = $6.00/month.
- On Gemini 3.1 Pro (under the 200K tier, $2/$12): (80K × $2 + 4K × $12) / 1M × 30 = $6.24/month.

Now attach the entire 350K-token codebase — not just the diff — because the reviewer keeps missing cross-file call-site impact:

- On Opus 4.8 (no surcharge): (350K × $5 + 4K × $25) / 1M × 30 = $55.50/month.
- On Gemini 3.1 Pro, tier-stepped (>200K → $4/$18): (350K × $4 + 4K × $18) / 1M × 30 = $44.16/month.

The Gemini tier step matters: crossing 200K doubles its input rate. If you are reading legacy 2025–early-2026 pricing articles that describe an Anthropic >200K cliff, that cliff is gone; on Google it is alive.

## Layer 2 — The 1M context beta and what "1M" actually means

Fable 5, Opus 4.8, and Sonnet 5 all claim 1M-token windows; Gemini 3.1 Pro claims the same; GPT-5.5/5.6 claim ~1.05M. Here is what "1M" actually means, operationally:

**It means the server won't reject your request.** Nothing more. A 1M advertised window is a structural property of the attention implementation plus the positional encoding scheme (RoPE scaling, YaRN, interpolation, whatever the provider uses internally). The model's weights were trained on sequences of a certain length; inference-time position scaling extends that range at the cost of accuracy that decays with distance from the training distribution. The window is a physical fact. Quality inside the window is a separate, benchmarked question — see Layer 3.

**Anthropic bills the full 1M at standard rates.** For Fable 5, Opus 4.8/4.7, Sonnet 5, and Sonnet 4.6, a 900K-token request is billed at exactly the same per-token rate as a 9K one — no >200K surcharge.[^3] (This corrects a real historical wrinkle: Opus 4.6's 1M *beta* in 2025 carried a 2×/1.5× premium above 200K, removed at GA on 2026-03-13. If you built a cost model under that beta, the cliff is gone — but so is the model.)

**Gemini still has a cliff.** On Google's Developer API, Gemini 3.1 Pro prompts up to 200K hit the standard tier ($2.00 input / $12.00 output per MTok); above 200K the rate doubles to $4.00 / $18.00.[^10] If your pipeline routinely crosses 200K — RAG with large chunks, whole-codebase analysis, long transcripts — that step should appear explicitly in your cost model.

**The "windows aren't monotonically up" argument resolved — upward.** In 2025 OpenAI had *shrunk* to a 400K window with GPT-5, and it was reasonable to bet that a smaller window with higher usable quality beat 1M with worse quality-per-token. That bet was abandoned: GPT-5.5 (April 2026) went back to a ~1M (1.05M) API window, and GPT-5.6 kept it. So 1M is now table stakes at every major lab — which sharpens, rather than settles, the Layer-3 question of whether that capacity is *usable*.

**Extended thinking eats your context window too.** On current Claude models, when you enable extended thinking with a `budget_tokens` parameter, those reasoning tokens count as both (a) output tokens for billing and (b) context-window consumption for the duration of the current turn.[^11] A 200K-token prompt plus a 50K-token thinking budget leaves you 750K of headroom, not 800K. One relief: across multi-turn conversations, the API automatically strips previous turns' thinking blocks, so thinking doesn't accumulate.[^11] For single-turn long-context work, budget thinking against the window explicitly.

Takeaway: treat the advertised context window as a legal upper bound on request size, not as a guide to where your pipeline should live. Stay as far under it as your task permits, both for quality reasons (Layer 3) and cost reasons (tier steps on Gemini, output-token amplification everywhere).

## Layer 3 — Lost in the middle: Liu 2023, RULER 2024, NoLiMa 2025

Here is the part most AI-catalyst leads are foggy on, because the benchmarks keep landing faster than the practitioner Twitter discourse processes them.

### Liu et al. 2023 — the original finding

Nelson Liu and colleagues at Stanford / Berkeley / Samaya / U Washington published *Lost in the Middle: How Language Models Use Long Contexts* in July 2023.[^4] The experimental setup was deliberately simple. Give a model a multi-document QA task or a key-value retrieval task; vary the position of the relevant document (or key) across 1, 5, 10, 20 positions in the context; measure accuracy as a function of position.

The finding — now the most-cited result in applied long-context work — was a U-shaped accuracy curve. Models retrieved reliably when the relevant content was near the beginning or the end of the context, and substantially worse when it was in the middle. On a 20-document QA setup, GPT-3.5-Turbo's accuracy was ~75% at position 1, dipped to ~50% at position 10, and recovered to ~60% at position 20. Claude-1.3 and MPT-30B-Instruct showed the same curve. Critically, the dip got worse as total context grew — a longer context stretches the middle and the middle gets lost harder.

For practitioners, the Liu result implies something concrete about prompt construction: the most important content goes at the top (system prompt territory) or the bottom (right before the model answers). Middle positions are weaker-signal territory. Any time a retrieval pipeline returns, say, 15 chunks in relevance order and concatenates them top-to-bottom, the 7th-to-10th chunks sit in the dip zone.

Liu 2023 tested models from 2023. The field's reaction across 2024-2025 was: "does this still hold on 100K, 200K, 1M-context models?" Two benchmarks answered.

### RULER (Hsieh et al. 2024) — stress-testing the "real" context size

Cheng-Ping Hsieh and colleagues at NVIDIA released RULER in April 2024.[^1] RULER extends the simple needle-in-a-haystack test with 13 task variants across four categories: needle-in-haystack variants, variable tracking, aggregation, and multi-hop QA. It scales from 4K to 128K in the original paper (longer in subsequent extensions).

The operationally important finding: **while most frontier models advertised 32K+ context, only about half maintained a "qualitative threshold" of accuracy (defined as Llama-2-7B's performance at 4K, 85.6%) out to 32K.** Several models that advertised 128K or 200K collapsed on harder RULER tasks at 32K-64K. The aggregation tasks — *"count how many times X appears across these documents"* — were the first to break. Multi-hop QA was second. Vanilla NIAH — *"here's one literal sentence hidden in a long haystack, find it"* — stayed nearly perfect and was therefore a bad proxy for real long-context quality.

This is the empirical foundation for the claim you will hear senior builders make: "I don't trust context above 32K without an eval." RULER is where that claim comes from.

### NoLiMa (Modarressi et al. 2025) — the complexity axis

Ali Modarressi and colleagues (Adobe Research) published NoLiMa in February 2025, published at ICML 2025.[^2] NoLiMa's contribution is an extension of NIAH where *questions and needles share no literal lexical overlap* — the model has to infer the association. For example: needle text mentions "a gate from which Shinjuku's trains depart"; question asks "which station is Taro commuting from?" The model must know, and retrieve, that Shinjuku is a station.

Results are starker than Liu's. At 1K context, most frontier models scored near their baseline (often 90%+). **At 32K, 11 of the tested models fell below 50% of their short-context baseline. GPT-4o fell from 99.3% at short context to 69.7% at 32K.** Modarressi's interpretation: the attention mechanism depends more heavily on literal match cues than practitioners assume; when those cues are absent, long-range retrieval breaks well before the advertised window limit.

The combined takeaway — Liu + RULER + NoLiMa — is unambiguous. **Usable context is substantially shorter than advertised context, and the gap widens as tasks require aggregation, multi-hop inference, or association without literal overlap.** A 1M model whose NoLiMa performance at 32K drops 30 points is not a 1M retrieval system. It's a 1M-input attention system with a 16-32K high-fidelity core.

### What that implies for the prompt you ship on Monday

- Do not conflate "fits in the context" with "will be retrieved accurately." Run RULER-style or NoLiMa-style checks on your own data if the stakes are real.
- Put the most important content at the edges of the prompt. The Liu U-shape has not been refuted by any subsequent benchmark I have read; it has been sharpened.
- For any task that requires aggregation across a long context (*"summarize the decisions across these 50 meeting notes"*), expect degradation that a needle-in-haystack eval will not catch. Build an eval that matches your task shape.

## Layer 4 — The KV cache and why prompt caching wins

To understand why Anthropic's prompt caching feature produces a 90% discount, you need the KV-cache mental model.

When a transformer processes a prompt, every layer attends over all previous tokens. For each token at each layer, attention requires a Key and a Value vector (hence KV). On autoregressive generation, the model caches these K and V tensors across the generation sequence — each new output token attends over the KV of every prior token without recomputing them. This cache is the "KV cache." It lives in GPU memory during a single request.

Inside a single request, the KV cache is automatic — you don't pay extra for it, and you don't manage it. Between requests, though, the cache is normally discarded. If you send the same 100K-token system prompt back on the next request, the server recomputes every K and V from scratch. That recompute is what you are paying for on standard input tokens.

**Prompt caching**, which Anthropic launched in public beta in August 2024, lets you reuse the computed KV tensors for a stable prefix instead of re-prefilling it every call. There are now two modes: **automatic caching** — add a single top-level `cache_control` field and the system manages breakpoints as the conversation grows (the recommended default for most use cases) — and **explicit breakpoints** — place `cache_control` on individual content blocks for fine-grained control.[^5] Either way the server stores the KV for the matched prefix and, on the next request within the TTL, skips recomputation.

The economics (verified against Anthropic's pricing docs, 2026-07-17):

- **Cache write (5-min TTL, default)**: 1.25× standard input rate.
- **Cache write (1-hour TTL, extended)**: 2.0× standard input rate.
- **Cache read (hit)**: 0.10× standard input rate — a 90% discount on every subsequent hit within TTL.[^5]

Break-even is closer than the intuition suggests. Per Anthropic: *"caching pays off after just **one** cache read for the 5-minute duration (1.25× write), or after **two** cache reads for the 1-hour duration (2× write)."*[^5] (The arithmetic: one write plus one read at 5-min costs 1.25 + 0.10 = 1.35× versus 2× for two uncached reads — it already wins on the *first* reuse. The April draft's "roughly 2 reads" and "3–4 reads for 1-hour" were both wrong.) In practice, any workload that reuses a long prefix even once inside the TTL is cheaper with caching on — which covers nearly every real agentic workflow: tool-loop agents, RAG with a stable instruction block, multi-turn conversations with a long system prompt, code-review bots with fixed guidelines.

**Breakpoint positioning matters (in explicit mode).** You can set up to 4 breakpoints per request. The cache is prefix-matched — only tokens up to the last matching breakpoint reuse KV. So the structure is: stable-system-prompt → [breakpoint] → stable-tool-definitions → [breakpoint] → stable-context/docs → [breakpoint] → variable-user-query. If you put the variable content first, nothing matches. Automatic caching handles this for the common case; reach for explicit breakpoints when you need to control exactly which region is the cacheable prefix.

**TTL choice is a volume bet.** High-volume continuous pipelines (agent loops hitting the same prefix every few seconds): 5-min TTL dominates. Human-in-the-loop workflows where the same large context gets reused over minutes to hours (code-review session, research assistant, long document analysis): 1-hour TTL dominates.

### Worked example: 500K-token RAG pipeline, 10K invocations/day

This is the specific scenario the L3 content spec calls for. Setup:

- Static retrieved context: 500K tokens per invocation (say, a full knowledge base index plus the top 30 retrieved chunks — large but within Opus 4.8's 1M window).
- Variable user query: ~500 tokens.
- Output: ~1,500 tokens per invocation.
- Volume: 10,000 invocations/day.
- Provider: Claude Opus 4.8. Input $5, output $25, cache write (5-min) $6.25, cache read $0.50, per MTok.[^8][^5]

**Without prompt caching:**
- Input: 500,000 tokens × 10,000 invocations = 5,000,000,000 tokens/day = 5,000 MTok.
- Input cost: 5,000 × $5 = $25,000/day.
- Output: 1,500 × 10,000 = 15,000,000 tokens/day = 15 MTok.
- Output cost: 15 × $25 = $375/day.
- **Daily total: $25,375. Monthly (30d): $761,250.**

**With 5-minute prompt caching**, assuming the 500K context is stable enough that cache hits account for 99% of invocations (at 10K/day there are ~35 calls in each rolling 5-min window, so the first writes the cache and the next ~34 read it before the TTL rolls):
- Cache writes: 0.01 × 5,000 MTok/day = 50 MTok at $6.25 = $313/day.
- Cache reads: 0.99 × 5,000 MTok/day = 4,950 MTok at $0.50 = $2,475/day.
- Output: $375/day (unchanged).
- **Daily total: $3,163. Monthly: $94,890.**

**Monthly savings from prompt caching: ~$666,000.** That is not a typo. At this volume and reuse pattern, caching is the difference between an AI feature with a viable unit economics and one that bleeds the P&L.

**A more realistic scenario: 60% cache hits.** The 99% number is the hero case. Many production workloads sit closer to 60% because only part of the 500K prefix is stable (system + fixed KB) and the retrieved chunks churn. Same workload, same 500K × 10K/day volume, 60% hit-rate:

- Cache writes: 0.40 × 5,000 MTok/day = 2,000 MTok at $6.25 = $12,500/day.
- Cache reads: 0.60 × 5,000 MTok/day = 3,000 MTok at $0.50 = $1,500/day.
- Output: $375/day (unchanged).
- **Daily total: $14,375. Monthly: $431,250.**

| Scenario | Daily input-side cost | Monthly total | Savings vs uncached |
|---|---|---|---|
| No caching | $25,000 | $761,250 | — |
| 60% hit rate | $14,000 | $431,250 | 43% |
| 99% hit rate | $2,788 | $94,890 | 88% |

The gap between 60% and 99% is where prompt *architecture* earns its keep: pushing breakpoints to capture the last stable region, batching retrieval into a cacheable block, running the dynamic user-specific content last. Every 10 points of hit rate is tens of thousands of dollars per month at this volume.

Two things worth flagging about this worked example:

1. **The 99% cache-hit rate is the heroic assumption.** In practice, your cache-hit rate depends on how stable your static context actually is. If the retrieved chunks change every call (which is the default in naïve RAG), you get 0% hits on the chunks portion. Caching pays off when you architect your prompt so that the *first* large stable region (system + retrievers-config + fixed KB chunks) is cached and only the *last* region (dynamic chunks + user query) varies.
2. **At lower volumes the absolute savings shrink but the percentage stays.** At 100 invocations/day the uncached cost is $254/day and cached is $32/day — same 87.5% reduction, different absolute stakes. The discipline is the same.

## Layer 5 — The live controversy: long context vs RAG in 2025

Position A — **long context is making RAG obsolete** — is the loud position in late-2024 and early-2025 discourse. Proponents point to three things: (1) Gemini 1.5's technical report demonstrating near-perfect recall on needle-in-haystack at 1M-10M tokens, (2) the arrival of Opus 4.6 and Sonnet 4.6 at 1M GA pricing, and (3) the operational simplicity of "just paste the whole knowledge base into the prompt" versus maintaining a vector store, embedding pipeline, chunk strategy, and reranker. The argument: if the model can attend to a 1M-token knowledge base directly, every retrieval pipeline is strictly worse than a 1M-token prompt.

Position B — **RAG (or its successor, context engineering) is alive, and long context alone loses** — is the operator position, associated most visibly with Jason Liu and implicitly with Anthropic's own Contextual Retrieval release.[^7][^6] Three pieces of evidence:

First, Anthropic published *Introducing Contextual Retrieval* in September 2024 — squarely *after* Gemini 1.5's 1M claims — and the headline numbers were specific: adding per-chunk contextual prefixes before embedding reduced top-20 retrieval failure by 49% (5.7% → 2.9%); adding a Cohere reranker pushed the reduction to 67%.[^6] Anthropic is not a disinterested party on retrieval (they sell prompt caching which makes large prompts cheap); they published this anyway, because on their eval suite, retrieval wins.

Second, the Liu / RULER / NoLiMa findings in Layer 3 tell you *why* long context alone loses on production workloads. Stuffing 500K tokens of "probably relevant" content into context burns input cost, burns attention on the middle-position dip, and produces demonstrably worse retrieval than a well-indexed 5K-token top-k. Long context gives you more *capacity*; it does not give you better *signal-to-noise*.

Third, Jason Liu's 2025 writing has shifted the framing from "RAG vs long context" to "retrieval as a component of context engineering."[^7] His argument: agents don't need "the right chunk"; they need situational awareness over the information landscape — which tools, which document collections, which sub-collections are available, what each contains at high level, how to drill down. The retrieval system is *how the agent navigates*, not *where the answer lives*. That framing kills the "RAG is dead" frame — retrieval didn't die, it became a tool-use primitive — and it also kills the "just stuff everything into 1M context" frame, because now you have 20 million tokens of available information across tools and stuffing isn't an option.

**My position, for this lesson: both framings have truth; the operator-actionable synthesis is closer to B.** Specifically:

- Long context is a *quality budget* for the small number of tasks where keeping a full artifact (a codebase, a book, a trial transcript) together matters more than selecting from it. Pick Opus 4.6 1M for a legal-review workflow where excising context changes the answer.
- Retrieval (in its modern form — contextual embeddings, rerankers, agentic tool calls) is how you handle everything else. The economics of prompt caching plus the quality economics of RULER/NoLiMa both argue for keeping the stable prompt large and cacheable, and the variable content small and high-precision.
- "RAG is dead" is a slogan that is useful for selling a 2026 SaaS; it is not a claim Anthropic's own research supports, and it is not a claim that survives a careful read of 2024-2025 long-context benchmarks.

Treat any vendor who tells you "you don't need RAG anymore, just use our 1M window" as selling capacity, not results. Ask them for their NoLiMa scores.

## Runnable experiment — direct Claude Code, see it on your screen

You have two options. Pick one. Each is a direction Claude Code executes; you do not write Python by hand.

### Option A — Prompt caching economics, live

Goal: measure the token cost and wallclock cost of 10 sequential questions against a 50K-token codebase, with and without prompt caching. Confirm on your bill that caching does what Layer 4 claims.

Open Claude Code in any scratch folder and paste:

> I want to run a prompt-caching economics experiment. Please:
>
> 1. Pick a real 50K-token Python project (FastAPI source, Flask, the requests library, anything on disk ≥200KB of source). Concatenate all its `.py` files into one string. Confirm the token count is between 45K and 60K using Anthropic's token counting endpoint; trim or pad until it is.
> 2. Write a script that uses the Anthropic Python SDK against `claude-sonnet-4-6` (confirm the exact model ID against Anthropic's docs). The script should run two phases:
>    - **Phase 1 (uncached):** Send 10 diverse questions about the codebase in sequence, each as a fresh request, with the full 50K-token codebase in the user message every time. No `cache_control`. Record `usage.input_tokens`, `usage.output_tokens`, and wall time per call.
>    - **Phase 2 (cached):** Same 10 questions, same codebase prefix, but include a `cache_control: {"type": "ephemeral"}` breakpoint after the codebase block and before the question. 5-min TTL. Record `usage.input_tokens`, `usage.cache_creation_input_tokens`, `usage.cache_read_input_tokens`, `usage.output_tokens`, wall time.
> 3. Compute and print: (a) total input tokens, cache-write tokens, cache-read tokens, output tokens across all 10 calls, per phase; (b) dollar cost per phase at current pricing ($3/$15 input/output, $3.75 cache-write-5m, $0.30 cache-read); (c) wall-time-per-call averaged across calls 2-10 per phase (ignore call 1, which is the write).
> 4. Explain the result in plain English in 3-5 sentences. In particular, comment on whether the savings you saw match the theoretical ~87% reduction on input cost.

Expected shape: Phase 1 input cost ~$1.50. Phase 2 cache-write on call 1, then 9 cache reads. Total input cost ~$0.30. Output cost same in both. Wall time per call typically drops 20-40% on cached calls because the server skips prefill compute.

The number you want to commit to long-term memory is the one Claude Code prints for your own run — not mine.

### Option B — Your own lost-in-the-middle replication

Goal: confirm Liu 2023's finding on a current 2026 model. Place a single fact at 5%, 50%, and 95% of a 200K-token prompt; measure retrieval accuracy across 20 samples each.

Paste into Claude Code:

> I want to replicate the lost-in-the-middle finding from Liu et al. 2023 on a current model. Please:
>
> 1. Generate or fetch ~200K tokens of distractor text (e.g., concatenated Wikipedia articles on geography, or arXiv abstracts — anything semantically distant from the fact I'll insert). Confirm token count.
> 2. Insert this exact sentence into the distractor text: `"The secret code for this experiment is PURPLE-ELEVEN-HORIZON."` Place it at three positions: 5% into the distractors, 50%, and 95%. Generate three versions of the 200K prompt.
> 3. For each position, run 20 samples against `claude-sonnet-4-6` at temperature=1.0 with the question `"What is the secret code for this experiment? Respond with only the code."` Record whether the response contains `PURPLE-ELEVEN-HORIZON` (case-insensitive).
> 4. Print the recall rate per position, along with the distribution of failure modes (hallucinated codes, refusals, answers citing distractor text).
> 5. Comment on whether you see the U-shape Liu predicts, and how stark it is on Sonnet 4.6 relative to the GPT-3.5-Turbo curves in the original paper.

Expected shape on Sonnet 4.6 mid-2026: end positions (5% and 95%) near 95-100% recall; 50% position somewhere between 70% and 95% depending on the exact prompt and distractor set. The U is shallower than Liu 2023 reported on 2023 models, but it still exists. Running this is the way you convert the benchmark citation into a felt fact about the model you are about to ship on.

Cost estimate for option B: 3 positions × 20 samples × 200K input × $3/MTok ≈ $36 of Sonnet 4.6 spend. Run it only if you have the budget; otherwise reduce to N=5 per position for a ~$9 version that still shows the effect directionally.

## Problem set — five operator-shaped problems

**P1 — Token price a real workflow.** Pick a Claude Code workflow you actually ran this week. From the terminal or the dashboard, pull the session's input/output token counts. Compute the cost at Opus 4.6 rates, Sonnet 4.6 rates, Haiku 4.5 rates, and Gemini 2.5 Pro rates (splitting at the 200K cliff if relevant). Write a one-paragraph note on which model you'd use for this workflow in production and what eval you'd want before committing. Do not guess — look up current prices from the provider.

**P2 — Run the caching experiment OR the lost-in-the-middle experiment above.** Paste the final numbers into `week-00-notes.md`. Do not summarize; paste the actual values Claude Code printed.

**P3 — Critique a published long-context claim.** Find a vendor blog post or Twitter thread from the last 6 months claiming "context windows replace RAG." Identify three claims in the post that would not survive a RULER or NoLiMa eval. Write two sentences each on what the post elides. This is reviewer-lens practice. If you can't find one in 10 minutes of looking you're not looking — they are everywhere.

**P4 — Design a breakpoint architecture for a real workflow.** Take a prompt you're using in a live Claude Code custom command or a Claude API integration. Mark in the prompt text where you would place `cache_control` breakpoints to maximize cache hits across typical invocation patterns. Justify each breakpoint in one sentence. If you have no current prompt that exceeds the 1,024-token prompt-caching minimum, build one — a stable system prompt plus a large code chunk or document — for a workflow you'll start in Week 1.

**P5 — Cost a pipeline at two volumes.** Take the 500K-RAG worked example in Layer 4. Re-run the math at 100 invocations/day and at 100,000 invocations/day, both with and without caching. Note the inflection where caching shifts from "nice-to-have" to "mandatory." For your own products — what volume do you actually expect, and where does that land on the curve? Write one paragraph.

## Operator war stories — specific numbers, specific dates

**Anthropic's prompt-caching launch, August 2024.** Anthropic launched prompt caching on 2024-08-14 with a headline "up to 90% cost reduction" on cached input, and named early adopters (Notion among them). Treat the "90%" as the *feature ceiling* — the 0.10× cache-read rate is literally a 90% discount on the cached portion — not as a specific reported figure for any one customer; the April draft attached the 90% to a "Notion-reported" number that could not be verified, so read it as the generic ceiling. Within weeks, OpenRouter, Bedrock, and Vertex shipped matching features, and the 90% discount on cache reads became an industry-wide expectation.[^5]

**Gemini 1.5's 10M-context demo and what it did not prove.** In February 2024, Google DeepMind published Gemini 1.5's technical report showing near-perfect NIAH recall at 1M and passable recall at 10M.[^12] The demo reshaped discourse overnight. What the paper did *not* demonstrate — and this is the gap RULER and NoLiMa filled over the next 12 months — was retrieval quality on complex tasks at those lengths. Vanilla NIAH was the easy problem. Aggregation, multi-hop, and association without literal overlap were the hard ones. RULER scores for Gemini 1.5 Pro dropped well below the Llama-2-7B 4K threshold by 32K on several task classes.[^1] The operational lesson: one benchmark at one scale is a demo, not a deployment story.

**Anthropic's 2026-03-13 1M GA as a pricing correction.** For seven months (beta period from mid-2025 through 2026-03-13), the 1M Opus 4.6 window carried a 2×/1.5× input/output premium on tokens above 200K.[^3] That premium was operationally a message: "we don't want you to casually cross 200K." Teams that built pipelines around >200K contexts in that window were paying a dedicated surcharge. The GA announcement unified pricing — a 900K request is now the same per-token cost as a 9K one — and rewrote the economic math for whole-codebase and long-document workflows overnight. If your cost model was built under beta pricing, revisit it this week. I have seen teams continue to assume the 2× cliff months after it went away.

## Common mistakes AI-catalyst leads still make

1. **Quoting input price as *the* price.** You will read a post claiming "Gemini 2.5 Pro is 4× cheaper than Opus." That's true on input under 200K. On a workflow heavy on output (code generation, long-form writing, multi-turn agents) the gap is much smaller. On a workflow with stable cacheable prefixes, it can invert. Never cite one-number-per-model comparisons.

2. **Trusting the advertised context window as the useful window.** RULER and NoLiMa exist because every frontier model lies here by omission. *"1M-token window"* is marketing. *"1M tokens accepted, 32-64K of high-fidelity retrieval on complex tasks"* is the engineering claim. Your evals should measure the second.

3. **Putting variable content early in the prompt, stable content late.** Pure cache-hit killer. Reverses the stable-first, variable-last structure that cache-aware prompts need. Also a Liu-2023 killer — important variable content near the top competes for primacy with system-prompt content.

4. **Treating prompt caching as free money without measuring it.** Caching writes cost 1.25× or 2× input rate. If your usage pattern has 1.1 reads per write on average (i.e., you rewrite the cache almost every request because your "stable" prefix keeps shifting), caching costs you money. Measure cache-hit rate as a first-class operational metric.

5. **Ignoring the extended-thinking budget in context math.** Opus 4.6 with a 32K extended-thinking budget and a 900K prompt leaves no headroom for output — the generation will truncate or error. The thinking tokens are real context consumption within the turn.[^11]

6. **Assuming one provider's cache semantics generalize.** Anthropic cache reads cost 0.10× of input; Gemini's context caching is billed at half input rate (0.5×), not 10%; OpenAI's automatic prompt caching kicks in at different thresholds with different discount structures.[^5][^10] Cross-provider architectures need per-provider cache math.

7. **Shipping a long-context pipeline without a NoLiMa-style eval.** If your workload requires association across long distances without literal match, and you have not tested it with an eval that probes that, you are going to lose silently in production. Build a 50-item synthetic NoLiMa for your own task shape as part of the pipeline.

## Open questions — what is not settled as of 2026-04-15

**Does the attention-compute scaling of 1M windows degrade silently as the weights drift across model updates?** Opus 4.5 and Opus 4.6 both advertise 1M (4.5 at beta, 4.6 at GA). Whether the quality curve at 500K or 900K is identical across those releases, or whether minor post-training shifts move the usable ceiling around, is not publicly benchmarked by Anthropic. Teams running long-context workloads should re-run their evals on every model update.

**Will per-provider tier-step pricing come back?** Anthropic removed the Opus 4.6 200K cliff in March 2026 citing improved serving efficiency. Under heavier demand or a new architecture with steeper memory curves, tier steps could return. Gemini 2.5 Pro still has one. The industry default is unstable; price against documented rates on the day you ship.

**Is context engineering (Jason Liu's frame) a durable discipline or a transitional one?** The optimistic view is that agents will get good enough that they can navigate messy information landscapes with simpler tool interfaces — the skill decays. The skeptical view (which I lean toward) is that as stakes rise and information density grows, the skill gets larger, not smaller — closer to information architecture than to prompt-craft. Week 2 onward assumes the second framing.

## Reviewer lens — specific named disagreements

Each bullet below names a paragraph and a specific critic who would push back.

- **Nelson Liu, on Layer 3's summary of his paper.** I've described the Liu 2023 finding as a U-shaped curve with the mid-position dip as the dominant effect. Liu would argue — correctly — that the original paper reports both a recency-primacy effect *and* a monotonic degradation with total context length, and that presenting the U as the whole story understates the length axis. The length effect has been sharpened by NoLiMa; the U has been sharpened by RULER's position-aware subtasks. I have compressed two findings into one mental model. The compression is pedagogically useful; it is technically incomplete.[^4]

- **Cheng-Ping Hsieh, on Layer 3's treatment of RULER.** I've summarized RULER's headline finding as "only half the models hold quality to 32K." Hsieh would push back that the paper's contribution is really the *task suite* — the 13 variants that distinguish surface retrieval from aggregation and multi-hop. Readers who take the summary without reading the task-by-task breakdown will underweight how task-dependent long-context quality is. A model can ace NIAH-variant tasks and fail on aggregation at the same length. Run the task-class breakdown, not just the composite score.[^1]

- **Jason Liu, on Layer 5's position synthesis.** I have ended Layer 5 with a synthesis that gives retrieval the operator-actionable win. Liu would argue the framing is still too binary — "RAG vs long context" — and that the actual practitioner frame is "what information shape does my agent need at each step of its loop, and which primitive (cached prefix, tool call, semantic search, in-context documentation) delivers that shape most economically?" That framing is Liu's post-August-2025 pivot from RAG-specifically to context-engineering-generally, and the lesson captures it partially but not fully. The one-paragraph synthesis is directionally right and architecturally light.[^7]

- **Boris Cherny, on the runnable-experiment section.** I have written the experiments as direct-Claude-Code instructions without a versioning scaffold. Cherny would argue that any experiment worth running once is worth committing to a `prompts/` folder with a `README.md` describing the exact model ID, date, and expected shape — otherwise the numbers decay silently as models change. I've gestured at this in Problem 2 but not codified it in the experiment itself. In a live version of this workflow, the first thing Claude Code should be told to do is `mkdir experiments/fri-context-economics && cd $_` and write the script into a version-controlled file.

- **Honest uncertainty on the 99%-cache-hit-rate assumption in Layer 4.** I used a 99% hit rate for the 500K-RAG worked example. That assumes near-perfect prefix stability across 10K invocations/day, which is a heroic assumption for naïve RAG pipelines where the retrieved chunks change every call. For workflows where only the system prompt and tool definitions are stable (~50-80K tokens), and the retrieved chunks vary (~420-450K tokens), the cache-hit rate on the *variable* portion is 0 and the effective discount drops accordingly. A more realistic blended number is 30-60% cache-hit rate on input, yielding a 40-70% total-input-cost reduction rather than 87.5%. Still large. Less dramatic. Model against your actual prefix stability, not the headline number.

## Further reading

**Must-read this week (kept to five items intentionally):**

- Anthropic (2024-08-14). *Prompt caching.* API docs + launch announcement.[^5]
- Liu et al. (2023). *Lost in the Middle.* Read §§3-4 and Figure 1.[^4]
- Hsieh et al. (2024). *RULER.* Read §§2-3 and the task-taxonomy table.[^1]
- Anthropic (2024-09-19). *Introducing Contextual Retrieval.*[^6]
- Anthropic (2026-03-13). *1M context is now GA for Opus 4.6 and Sonnet 4.6.*[^3]

**Recommended (before Week 2):**

- Modarressi et al. (2025). *NoLiMa.* ICML 2025.[^2]
- Jason Liu (2025-08-27). *Beyond Chunks: Why Context Engineering is the Future of RAG.*[^7]
- Gemini 1.5 Technical Report (2024). Long-context capabilities section only.[^12]

**Optional:**

- Anthropic. *Context windows* and *Building with extended thinking.* API docs — read once to internalize how thinking interacts with the window.[^11]
- LightOn (2025). *RAG is Dead, Long Live RAG: Retrieval in the Age of Agents.* Useful second voice on the live controversy.[^13]

## Citations

[^1]: Hsieh, C.-P., Sun, S., Kriman, S., et al. (2024-04-09). *RULER: What's the Real Context Size of Your Long-Context Language Models?* NVIDIA. arXiv:2404.06654. https://arxiv.org/abs/2404.06654 — 13-task long-context benchmark (NIAH variants, variable tracking, aggregation, multi-hop QA); of 17 models tested at 32K+ advertised windows, only half sustained the Llama-2-7B-at-4K accuracy threshold. Code: https://github.com/NVIDIA/RULER

[^2]: Modarressi, A., et al. (2025-02-07). *NoLiMa: Long-Context Evaluation Beyond Literal Matching.* Adobe Research / LMU Munich. arXiv:2502.05167. https://arxiv.org/abs/2502.05167 — at 32K, 11 of the tested frontier models fell below 50% of their short-context baseline; GPT-4o fell from 99.3% to 69.7%. ICML 2025. Code: https://github.com/adobe-research/NoLiMa

[^3]: Anthropic (2026-03-13). *1M context is now generally available for Opus 4.6 and Sonnet 4.6.* https://claude.com/blog/1m-context-ga — GA removes the previous >200K tier step; standard input/output pricing applies across the full 1M window.

[^4]: Liu, N. F., Lin, K., Hewitt, J., Paranjape, A., Bevilacqua, M., Petroni, F., Liang, P. (2023-07-06). *Lost in the Middle: How Language Models Use Long Contexts.* Stanford / Berkeley / Samaya / UW. arXiv:2307.03172. https://arxiv.org/abs/2307.03172 — U-shaped accuracy curve over document position; GPT-3.5-Turbo drops ~25 points between position 1 and position 10 on 20-doc QA. TACL 2024. Code: https://github.com/nelson-liu/lost-in-the-middle

[^5]: Anthropic (2024-08-14 launch; docs retrieved 2026-04-15). *Prompt caching.* Claude API Docs. https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching — cache write (5-min) 1.25× input; cache write (1-hour) 2.0× input; cache read 0.10× input; up to 4 breakpoints per request.

[^6]: Anthropic (2024-09-19). *Introducing Contextual Retrieval.* https://www.anthropic.com/news/contextual-retrieval — Contextual Embeddings + Contextual BM25 reduce top-20 retrieval failure from 5.7% → 2.9% (49% relative reduction); adding a reranker pushes the reduction to 67%.

[^7]: Jason Liu (2025-08-27). *Beyond Chunks: Why Context Engineering is the Future of RAG.* https://jxnl.co/writing/2025/08/27/facets-context-engineering/ — framing shift from "retrieve the right chunk" to "design tool responses that give agents situational awareness across the information landscape." See also index: https://jxnl.co/writing/2025/08/28/context-engineering-index/

[^8]: Anthropic. *Pricing.* Claude API Docs, retrieved 2026-04-15. https://platform.claude.com/docs/en/about-claude/pricing — Opus 4.6 $5/$25; Sonnet 4.6 $3/$15; Haiku 4.5 $1/$5 per MTok input/output.

[^9]: OpenAI. *API Pricing*, retrieved 2026-04-15. https://openai.com/api/pricing/ — GPT-5 (high) $1.25/$10; GPT-5.4 $2.50/$15; GPT-5.4-nano $0.20/$1.25 per MTok.

[^10]: Google. *Gemini Developer API pricing*, retrieved 2026-04-15. https://ai.google.dev/gemini-api/docs/pricing — Gemini 2.5 Pro (Standard tier): $1.25/$10.00 per MTok for prompts ≤200K; $2.50/$15.00 per MTok for prompts >200K. (The higher $3.60/$21.60 or $4.00/$18.00 figures circulating in older posts correspond to the Priority tier of Gemini 3.1 Pro Preview, not Gemini 2.5 Pro Standard.) Context caching at ~0.5× input rate.

[^11]: Anthropic. *Context windows* + *Building with extended thinking.* Claude API Docs, retrieved 2026-04-15. https://platform.claude.com/docs/en/build-with-claude/context-windows and https://docs.claude.com/en/docs/build-with-claude/extended-thinking — thinking tokens count toward max_tokens, are billed as output, count against context window within a turn; prior-turn thinking blocks are auto-stripped across turns.

[^12]: Google DeepMind (2024-02-15, updated across 2024). *Gemini 1.5 Technical Report.* https://storage.googleapis.com/deepmind-media/gemini/gemini_v1_5_report.pdf — near-perfect NIAH recall at 1M tokens, passable recall at 10M; subsequent benchmarks (RULER, NoLiMa) sharpened the gap between NIAH recall and task-weighted long-context quality.

[^13]: LightOn (2025). *RAG is Dead, Long Live RAG: Retrieval in the Age of Agents.* https://lighton.ai/lighton-blogs/rag-is-dead-long-live-rag-retrieval-in-the-age-of-agents — second-voice summary of the 2025 retrieval-in-agents debate; aligns with the Jason-Liu context-engineering frame.

_last_verified: 2026-04-15_
