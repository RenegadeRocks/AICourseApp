---
type: synthesis
block: block-0-basecamp
week: week-00
day_of_cycle: 7
day_name: sun
title: 'Week 0 Synthesis — The substrate under every later week'
date_due: 2026-04-26
tags: [synthesis, quiz, flashcards, mental-model, builder-stack, memory-architecture, model-specs, context-economics, git-worktrees]
last_verified: 2026-04-15
word_count_target: 3800
---

# Week 0 Synthesis — The substrate under every later week

## The one-sentence thesis of this week

The six topics you covered this week — mental model of LLMs, the AI-native builder stack, CLAUDE.md / memory architecture, reading model specs critically, context-window economics, and git worktrees for AI builders — are not a topic survey. They are the six assumptions that every later week of this program will silently depend on, installed now so the program can stop re-explaining them.

---

## The unifying frame: what is "substrate" and why front-load it

Weeks 1–25 teach techniques. Each technique assumes six things the practitioner has already internalized:

- **What the model actually is**, so failure modes make sense (Mon).
- **What tool you are operating the model through**, because tools differ in agent-loop shape, memory, and sandbox (Tue).
- **How the tool remembers**, because every non-trivial session relies on persistent context that lives outside the chat (Wed).
- **How to read the numbers vendors publish about models**, because model choice is a decision the practitioner will make dozens of times per year (Thu).
- **What tokens actually cost and what context-window length actually buys**, because both shape every architectural trade-off (Fri).
- **What git gives you when an agent writes code for you**, because without a recovery protocol, AI-directed development is AI-directed gambling (Sat).

If you have internalized this, you have a substrate. Week 1 starts the real techniques (prompting, RAG, vibe coding) on top of that substrate.

The substrate is not a warm-up and not a survey. It is the permanent layer you will re-open throughout the year. When Week 4 asks you to choose between Sonnet 4.6 and Gemini 2.5 Pro for a long-context summarization pipeline, you will re-open Friday's economics lesson. When Week 13 walks you through reasoning-models fine-tuning, you will re-open Monday's mental model. When Week 20 has you scoping a client project, you will re-open Thursday's spec-reading discipline to pick the right model for their budget.

---

## Where each day's content goes forward

| This week's lesson | Underwrites in later weeks |
|--------------------|---------------------------|
| Mon — Mental model of LLMs | Week 1 prompting from first principles; Week 4 fine-tuning; Week 13 reasoning models |
| Tue — AI-native builder stack | Every week you ship in Claude Code; Weeks 19–22 client-project stack decisions |
| Wed — CLAUDE.md / memory | Every session after today; Week 2 MCPs; Weeks 5+ skills-and-subagents patterns |
| Thu — Reading model specs critically | Every model-choice decision; Weeks 7–9 evaluation & fine-tune benchmarking |
| Fri — Context window economics | Week 1 RAG vs long context; Week 9 long-context agents; Week 14 cost optimization |
| Sat — Git worktrees for AI builders | Every week with agent-written code; Week 18 parallel-agent orchestration |

---

## The week's key moves

Fifteen highest-leverage operational takeaways across Mon–Sat. Each row: the move, the mechanism that explains why, when to apply it, when not to.

| # | Move | Mechanism | Apply when | Do NOT apply when |
|---|------|-----------|------------|-------------------|
| 1 | Treat pretraining / SFT / RLHF / reasoning-RL as four distinct layers when diagnosing failure | Each layer is a separate artifact with separate breakage modes; post-training is a thin coat of paint on a base that still wants to continue any document | Diagnosing unexpected model behavior, jailbreaks, sleeper-agent-like misbehavior | Simple prompt iteration — overanalysis costs more than it saves |
| 2 | Never treat T=0 output as bitwise deterministic | Batch-size-dependent kernel orchestration, numeric FP non-associativity, and MoE routing all introduce variance even at greedy decoding (Thinking Machines 2025) | Any regression test or benchmark you are comparing across time | You only care about qualitative similarity, not bit-for-bit reproducibility |
| 3 | Classify every model failure as hallucination, confabulation, or refusal | Different root causes, different fixes — hallucinations are distribution-out-of-sample; confabulations are RLHF-era social pressure; refusals are over-trained safety | Debugging production model output | Casual chat — nobody needs a taxonomy for a coffee-recipe error |
| 4 | Pick an AI coding tool on the six-axis framework (loop / memory / tools / sandbox / model / price), not on Twitter buzz | Each axis changes a different class of failure — sandbox affects security; memory affects session continuity; loop shape affects wall-time cost | Picking a tool for a real client or team engagement | Personal weekend play — try whatever looks fun |
| 5 | Never rely on a vendor headline SWE-bench number without reading harness, sample budget, and temperature | Benchmark numbers are eval-harness-dependent; Morph's analysis shows tool A's Aider-polyglot score can flip based on sampling strategy, not model strength | Evaluating a model for production | Ruling models in for further testing — headline is a reasonable first filter |
| 6 | Use the CLAUDE.md hierarchy deliberately: user → project → nested, each with a distinct purpose | Each tier has a different scope; mixing invariants across tiers causes the "why is Claude suddenly doing X" session debugging nightmare | Any project expected to run more than a few sessions | One-shot throwaway scripts |
| 7 | Let auto-memory (`memory/` + `MEMORY.md`) carry **surprising / non-obvious** project facts — not architecture or conventions | Architecture belongs in CLAUDE.md or docs; auto-memory is for facts the harness will need at recall time that aren't derivable from the code | When the fact is about the *user* or the *session state*, not the code | When the fact is already in a file the harness can grep |
| 8 | Skills carry procedures with checklists; subagents carry context isolation; hooks carry harness-enforced behavior | Each is a different memory mechanism — mis-placing content between them causes context bloat or policy gaps | Designing a team-wide Claude Code workflow | Personal single-user setup — just put everything in CLAUDE.md |
| 9 | Read a model card's limitations section *first*, summary *last* | Vendors write preambles optimistically and stash the bad news in limitations; reading in reverse order calibrates your expectation before the rhetoric hits | Any production model-selection decision | Press-release-driven tweet replies — that's what summary sections are for |
| 10 | Calibrate every vendor number against one you ran yourself on your actual task distribution | Benchmark-to-production gap is where projects die; Husain's eval-driven-development thesis is that operator-relevant eval beats headline score by a wide margin | Before committing to a model for a paid product | Before shipping a prototype — overhead is unjustified at that stage |
| 11 | Treat the 1M context window as a legal upper bound, not a guide | RULER and NoLiMa both show usable context decays sharply with task complexity well before the advertised ceiling; 32k is where GPT-4o drops from 99.3% to 69.7% | Any pipeline where the document is approaching 30% of the window | When you have validated your own retrieval quality against the specific task |
| 12 | Architect prompts for caching: static prefix first, dynamic middle, user content last | Prompt caching only saves you the *prefix* that is identical across calls; cache hits drop ~90% off input cost | High-call-count pipelines with a stable preamble | One-off calls or pipelines where the prefix changes every call |
| 13 | Commit per verified-green iteration when an agent is writing code; keep the reflog loaded with rollback points | Agents produce code whose behavioral correctness is not visible in a diff; commit-per-green-test means every bad run is one reset away from recovery | Agent-directed coding sessions lasting more than a few turns | Single-turn scaffolding where a diff review is the whole QA |
| 14 | Use worktrees for parallel agent experiments on medium-to-long sessions; separate clones for short parallel tasks | Worktrees share the git object DB (fast) but can contend on node_modules, ports, and DB state — the trade-off flips with session length | Multi-hour experiments against a real service | Five-minute parallel pokes — just use branches or clones |
| 15 | Make `git reflog` and `git reset --keep HEAD@{n}` your recovery reflex, not Stack Overflow lookup | When an agent run wipes work, the time-to-recovery depends on whether you already know the commands; rehearse once on a throwaway repo | Any serious AI-directed development practice | You are genuinely content-scale-replacing git with a different VCS workflow |

---

## 20 quiz questions

*Span: Mon–Sat. Mix of multiple-choice (MC), short-answer (SA), position (PQ). Answers at end.*

---

**Q1 (MC)** — Which of these is the best reason a greedy-decoding (T=0) call to Claude can return different tokens across runs of the same prompt?
A. The model weights change between calls during a deploy.
B. Batch-size-dependent kernel orchestration and numeric non-associativity cause identical logits to round differently across server states.
C. RLHF re-ranks the top token non-deterministically.
D. Temperature is never actually zero in production.

**Q2 (SA)** — In your own words, describe the functional difference between a *hallucination* and a *confabulation* as taxonomized on Monday, and give one distinct fix for each.

**Q3 (PQ)** — Position: are reasoning models (Opus extended thinking, o1, DeepSeek-R1) qualitatively different from non-reasoning models, or are they the same substrate with test-time compute + RL on traces? Take a side and cite at least one paper or vendor doc that supports it.

**Q4 (MC)** — The six-axis framework for comparing AI coding tools (Tue) includes loop shape, memory, tools, sandbox, model, and price. Which of these differences matters *least* for a one-off weekend side project?
A. Sandbox / permission model.
B. Pricing tier.
C. Memory model (CLAUDE.md, .cursorrules, etc).
D. None — all six matter equally regardless of project scope.

**Q5 (SA)** — Tuesday argued the IDE-vs-CLI divide is collapsing. Name one specific product move from 2024–2025 that supports this claim, and one that contradicts it.

**Q6 (MC)** — A CLAUDE.md sits at the project root and imports another file via `@./conventions/python.md`. You then open Claude Code inside a nested `subproject/` directory that contains its own `CLAUDE.md`. What loads?
A. Only the nested `CLAUDE.md`.
B. Nested `CLAUDE.md` + project root `CLAUDE.md` + conventions/python.md via the import.
C. Only the project root `CLAUDE.md` (imports do not traverse).
D. All four tiers (enterprise + user + root + nested) plus any imports from any tier.

**Q7 (SA)** — Wednesday claimed auto-memory's `memory/` directory should hold *surprising / non-obvious* facts, not architecture or conventions. Give two concrete examples of facts that should go in `memory/` and two that should stay in CLAUDE.md or project docs.

**Q8 (PQ)** — Position: should auto-memory be enabled by default, or should it be opt-in? Cite at least one real user position from GitHub issues or release-thread feedback.

**Q9 (SA)** — Thursday taught that a benchmark number without its eval-harness conditions is near-meaningless. For a hypothetical "Model X: 85.0% on SWE-bench Verified" claim, list three specific harness conditions you would require before treating the number as comparable to another vendor's number.

**Q10 (MC)** — According to Thursday's lesson, which model-card section should you read FIRST when deciding whether to use a model in production?
A. Summary / overview.
B. Benchmark results table.
C. Limitations / known-issues section.
D. Pricing / availability.

**Q11 (SA)** — Thursday described one specific war story from Shopify / Fernandez: an "internal eval moved <1 point on a benchmark that rose significantly after a model swap." In your own words, why is this pattern the single most important calibration a practitioner can internalize?

**Q12 (MC)** — RULER and NoLiMa both demonstrate which of the following?
A. The 1M token context window is a product of pure marketing; usable context is actually ~4k tokens.
B. Usable context decays sharply with task complexity well below the advertised window length.
C. Long-context models have replaced RAG for all enterprise use cases.
D. Lost-in-the-middle is a myth refuted by 2024–2025 benchmarks.

**Q13 (SA)** — Friday presented a worked example comparing uncached, 60%-cache-hit, and 99%-cache-hit scenarios at 500k-token inputs × 10k daily calls. In one sentence, what is the practical design rule this dollar math forces on your prompt architecture?

**Q14 (PQ)** — Position: in 2026, does a 1M context window render RAG obsolete? Take a side and cite at least one post-2024-01 data point.

**Q15 (MC)** — Saturday's lesson named a specific controversy between Boris Cherny (Claude Code) and Simon Willison on worktrees vs separate clones. Which of these best captures the synthesis the lesson arrived at?
A. Cherny is right — always use separate clones because worktrees share too much state.
B. Willison is right — always use worktrees because they are faster to provision.
C. Decide by session length: worktrees for medium-to-long sessions, separate clones for quick parallel experiments.
D. Neither worktrees nor clones — use Docker containers for every agent task.

**Q16 (SA)** — Name two specific AI-introduced bug classes that are easy to miss in a diff review, and for each, describe one heuristic for catching them.

**Q17 (PQ)** — Position: is "commit per verified-green iteration" the right discipline for agent-directed coding, or is it over-engineering? Defend your position.

**Q18 (MC)** — The `git reflog` / `git reset --keep HEAD@{n}` recovery pattern is most useful when:
A. You need to share a branch with a colleague.
B. A local agent run has destroyed uncommitted work you need back.
C. You are rebasing `main` onto a feature branch.
D. You are initializing a new repo.

**Q19 (SA)** — Describe the practical difference between a Claude Code *skill* and a *subagent*. Under what condition would you choose one over the other?

**Q20 (PQ)** — Position: of the six topics this week, which one is the *most* load-bearing for your first client engagement this year, and why? (Argue with evidence from the lesson, not preference.)

---

## Answers

**Q1** — B. Batch-size-dependent kernel orchestration + floating-point non-associativity cause identical logits to round differently based on concurrent-request state. See Thinking Machines Lab, *Defeating Nondeterminism in LLM Inference* (Sep 2025).

**Q2** — A *hallucination* is out-of-distribution confident output — the model produces a token sequence that doesn't correspond to any grounded fact because the task is outside its training distribution. Fix: ground the model with RAG or retrieval so the needed facts enter the context window. A *confabulation* is RLHF-era social pressure — the model was trained to be helpful, and produces plausible-sounding but fabricated detail rather than refuse. Fix: specific prompting ("if uncertain, say so") plus an evaluator-optimizer loop that detects fabrication. See Monday §Layer 5.

**Q3** — Either side is defensible if cited. Position A (same substrate, just sampled differently): cite Simon Willison's 2025 posts on reasoning models + Sebastian Raschka's 2025 analysis. Position B (qualitatively new capability): cite the o1 system card (2024) + DeepSeek-R1 paper (Jan 2025) + Anthropic's adaptive-thinking docs. A strong answer acknowledges RL-on-traces is a real training shift, while test-time compute is a sampling shift, and takes a position on which dominates.

**Q4** — A. Sandbox / permission model. For a one-off weekend project, you don't care about enterprise permission policies; you care about whether the tool produces good code and what it costs. Memory (C) and pricing (B) also matter less on a single-use project but can still bite if you accidentally burn credits.

**Q5** — Supports collapse: Cursor Composer (2024–2025) adopted a CLI-adjacent agent-loop pattern, and Claude Code shipped a JetBrains IDE integration in 2025. Contradicts: Aider remains deliberately CLI-native with no IDE ambitions, and Windsurf / Cascade doubles down on editor-embedded completion as its differentiator.

**Q6** — B. The nested `CLAUDE.md` + the project root `CLAUDE.md` + the imported conventions file all load. Enterprise/user tiers also load if configured, but imports *do* resolve (empirical as of Claude Code v2.x).

**Q7** — In `memory/`: (1) user's specific preferences learned this session ("always test on Windows, not WSL"), (2) that an initial migration approach was rejected because of a past incident. In CLAUDE.md or docs: (1) project architecture decisions, (2) coding conventions / lint rules. The rule: if a future session needs it and it's not derivable from the code, it goes in memory. If it's durable and derivable, it goes in a doc.

**Q8** — Either side. Position A (default on): Anthropic's design framing in the v2.1.59 release notes — auto-memory is essential infrastructure. Position B (opt-in): GitHub issues #23544 and #37314 document real user demand to disable auto-memory on privacy / predictability grounds.

**Q9** — Required: (1) specific eval harness (SWE-agent, Moatless, custom) and its version. (2) sample budget per problem (single sample, N=10 majority vote, parallel test-time compute). (3) decoding settings (temperature, top-p). Bonus: whether the number is vendor-run or third-party reproduced.

**Q10** — C. Limitations / known-issues section. Vendor preambles are optimized for press; limitations sections are where the real calibration lives.

**Q11** — Because every benchmark number reflects a distribution the vendor chose, not your production distribution. If your internal eval barely moved when the external benchmark jumped, the benchmark gains were not a capability you will use. This is the single most important calibration — it converts "model X is now better" into "model X is better *for workloads the vendor cares about*," which may or may not include yours.

**Q12** — B. Usable context decays sharply with task complexity before the advertised ceiling. RULER shows ~half of models fail at 32K; NoLiMa shows 11 models below 50% of their short-context baseline at 32K.

**Q13** — Put everything stable at the beginning of the prompt and everything dynamic (user query, per-call variables) at the end, because caching only saves you the prefix and the savings compound with call count.

**Q14** — Either side. Position "RAG is obsolete": cite the Gemini 1.5 technical report's NIAH results. Position "RAG still wins": cite Anthropic's Contextual Retrieval (2024-09) 49%–67% improvement numbers + Jason Liu's 2025 context-engineering shift. The stronger synthesis: long context and RAG are complementary — long context works when your signal-to-noise is high, RAG works when you need selective retrieval out of a huge corpus.

**Q15** — C. Decide by session length. Worktrees for medium-to-long sessions where the shared git-object-DB speed and tool affordances (Claude Code's `isolation: "worktree"`) matter; separate clones for quick parallel experiments where node_modules/port/DB contention would dominate.

**Q16** — Two examples: (1) *silent API-surface flips* — an agent renames a function argument but updates only some callers; catch with a `grep` for the old name before merging. (2) *swallowed errors* — agent wraps a risky operation in a try/except that catches everything and returns a stub; catch by scanning diffs for new bare `except:` blocks or broad-exception patterns.

**Q17** — Either side, but "it's right" is the stronger defense: agent runs produce code whose behavioral correctness is not visible in a diff; committing per-green-test makes every bad run a `reset --keep` away from recovery. The counter-argument is that commit noise makes history unreadable — but squash-merge at PR time handles that. The discipline is cheap and the recovery ROI is enormous.

**Q18** — B. When a local agent run has destroyed uncommitted work, `reflog` + `reset --keep` is the recovery primitive. Options A/C/D are unrelated.

**Q19** — A *skill* is a procedure with a checklist (e.g., "how to run a pre-flight before shipping an API change") that Claude can invoke on demand. A *subagent* is a tool-equipped agent spawned with isolated context to carry out a bounded task and return only a summary. Choose a skill when you need a reusable procedure the main agent executes inline; choose a subagent when the task has substantial research/tool overhead whose byproducts you do not want to bloat the main context.

**Q20** — Defensible answers: (a) *Thursday*, because model-choice errors cascade into cost and quality problems across the whole engagement; (b) *Wednesday*, because without a memory architecture, you will re-explain the project to Claude Code every session and your team will diverge; (c) *Saturday*, because one agent run that wipes work is an engagement-killing event. The strongest answer picks one with a specific operational argument and a named counter-position it defeats.

---

## 30 flashcards

*Format: front (question/prompt) ↔ back (answer). Anki-importable.*

1. Q: The four training phases of a modern LLM, in order? → A: Pretraining → SFT (supervised fine-tuning) → RLHF (or RLAIF/Constitutional AI) → reasoning-RL (for reasoning models).
2. Q: Karpathy's one-line framing of the base model? → A: "A lossy, frozen, probabilistic document simulator."
3. Q: Why is T=0 not bitwise deterministic in production? → A: Batch-size-dependent kernel orchestration + floating-point non-associativity + MoE routing effects (Thinking Machines 2025).
4. Q: The three named LLM failure modes from Monday? → A: Hallucination (out-of-distribution confident output), confabulation (RLHF-driven plausible fabrication), refusal (over-trained safety).
5. Q: The six axes for comparing AI coding tools? → A: Loop shape · memory · tools · sandbox · model · price.
6. Q: The four tiers of the CLAUDE.md hierarchy? → A: Enterprise policy → user (~/.claude/CLAUDE.md) → project root → nested directory CLAUDE.md.
7. Q: What goes in `memory/` vs. CLAUDE.md? → A: `memory/` holds surprising / non-obvious facts (user preferences, session state); CLAUDE.md holds durable project architecture, conventions, invariants.
8. Q: Skills vs subagents in Claude Code? → A: Skill = procedure with checklist, invoked inline. Subagent = tool-equipped agent with isolated context, returns summary.
9. Q: In what order should you read a model card? → A: Limitations section first, benchmark table next, summary/overview last.
10. Q: What makes a benchmark number near-meaningless? → A: Missing eval-harness version, sample budget, temperature, and whether it is vendor-run or third-party reproduced.
11. Q: What RULER (Hsieh 2024) shows? → A: Usable context decays sharply with task complexity before the advertised context window ceiling.
12. Q: GPT-4o's RULER score at 32K vs short-context baseline? → A: 99.3% → 69.7%.
13. Q: NoLiMa's headline finding (Modarressi 2025)? → A: 11 tested models fell below 50% of their short-context baseline at 32K.
14. Q: What is Anthropic prompt caching's headline discount? → A: ~90% off input tokens on cache hits (Anthropic, 2024-08).
15. Q: Prompt architecture rule for caching? → A: Static prefix first, dynamic middle, user content last.
16. Q: Contextual Retrieval headline numbers (Anthropic 2024-09)? → A: 49% reduction in top-20 retrieval failure with contextual embeddings + BM25; 67% with reranker.
17. Q: When does `git worktree` beat a separate clone? → A: Medium-to-long sessions where shared git-object-DB speed + Claude Code's `isolation: "worktree"` agent affordances matter more than node_modules / port / DB isolation.
18. Q: The `git reflog` recovery reflex? → A: `git reflog` to find the last good HEAD; `git reset --keep HEAD@{n}` to return without losing in-flight work.
19. Q: Two AI-specific diff-review failure modes to watch for? → A: Silent API-surface flips (grep old name pre-merge); swallowed errors in new broad try/except blocks.
20. Q: The commit-per-iteration discipline? → A: Commit per verified-green run during agent-directed coding so every bad run is a `reset --keep` from recovery.
21. Q: Willison's "lethal trifecta" for agent security? → A: Private data + untrusted content + exfiltration channel = exploitable.
22. Q: Anthropic's 1M context GA date (Opus 4.6 / Sonnet 4.6)? → A: 2026-03-13.
23. Q: Hubinger 2024 "Sleeper Agents" core finding? → A: Backdoor behaviors survive standard RLHF / SFT / adversarial red-teaming — post-training is a thin overlay.
24. Q: What is CVE-2025-59536 about (Check Point)? → A: Hooks in `.claude/settings.json` auto-executing on session events without approval prompts — a trust-boundary vulnerability.
25. Q: Boris Cherny's CLAUDE.md flywheel heuristic? → A: "Every time Claude does something wrong, add a line to CLAUDE.md so it doesn't happen again."
26. Q: When is a subagent the wrong tool? → A: When the task can be done inline and returning only a summary would lose information you'll actually need.
27. Q: Which CVE pattern should make you suspicious when reading a hook definition? → A: Hooks that run external commands on `SessionStart` or `Stop` without allowlist filtering.
28. Q: Chen / Benton et al. (Anthropic 2025) headline finding on reasoning models? → A: Reasoning traces disclose the actual influencing cue <20% of the time — CoT is not a faithful window into the model's decision.
29. Q: Three harness conditions required to make two SWE-bench numbers comparable? → A: Same harness version (SWE-agent / Moatless / custom), same sample budget, same decoding settings.
30. Q: The one-line rule for whether "AI catalyst" is installed in a practitioner? → A: They read the limitations section first, run their own eval, design for the lethal trifecta, and commit per green test.

---

## Further reading

**Must-read (≤5):**
- Karpathy, *Deep Dive into LLMs like ChatGPT* (Feb 2025, 3h31m). https://youtu.be/7xTGNNLPyMI
- Anthropic, *Claude Opus 4.6 release* (Feb 2026). https://www.anthropic.com/news/claude-opus-4-5 (Opus 4.5 template; 4.6 update covered via release notes).
- Anthropic, *Introducing Contextual Retrieval* (2024-09-19). https://www.anthropic.com/news/contextual-retrieval
- Hsieh et al., *RULER* (arXiv 2404.06654, 2024).
- Hamel Husain, *Your AI Product Needs Evals* (2024). https://hamel.dev/blog/posts/evals/

**Recommended:**
- Hubinger et al., *Sleeper Agents* (arXiv 2401.05566, 2024).
- Modarressi et al., *NoLiMa* (arXiv 2502.05167, 2025).
- Thinking Machines Lab, *Defeating Nondeterminism in LLM Inference* (Sep 2025).
- Simon Willison, parallel coding agents lifestyle posts (2025).
- Chen, Benton et al., *Reasoning Models Don't Always Say What They Think* (arXiv 2505.05410, 2025).

**Optional:**
- Deng et al., *Investigating Data Contamination* (NAACL 2024, arXiv 2311.09783).
- Jason Liu, context-engineering posts (2025).
- Boris Cherny (Claude Code) Threads posts on worktrees and CLAUDE.md discipline (2025).

---

## Citations

[^1]: Karpathy, A. (2025-02-05). *Deep Dive into LLMs like ChatGPT.* https://youtu.be/7xTGNNLPyMI — "Lossy, frozen, probabilistic document simulator" framing for base models.
[^2]: Thinking Machines Lab (2025-09). *Defeating Nondeterminism in LLM Inference.* https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/ — batch-size-dependent kernel orchestration as the root cause of T=0 variance.
[^3]: Hsieh et al. (2024). *RULER: What's the Real Context Size of Your Long-Context Language Models?* https://arxiv.org/abs/2404.06654 — half of tested models fail at 32K.
[^4]: Modarressi et al. (2025). *NoLiMa.* https://arxiv.org/abs/2502.05167 — 11 models below 50% of short-context baseline at 32K.
[^5]: Anthropic (2024-09-19). *Introducing Contextual Retrieval.* https://www.anthropic.com/news/contextual-retrieval — 49% / 67% retrieval-failure reduction numbers.
[^6]: Anthropic (2024-08). *Prompt caching general availability.* https://www.anthropic.com/news/prompt-caching — ~90% input-cost discount on cache hits.
[^7]: Husain, H. (2024). *Your AI Product Needs Evals.* https://hamel.dev/blog/posts/evals/ — eval-driven-development framework; binary LLM-as-judge.
[^8]: Hubinger et al. (2024). *Sleeper Agents.* https://arxiv.org/abs/2401.05566 — backdoor persistence through RLHF/SFT/red-teaming.
[^9]: Chen, Benton et al. (2025-05). *Reasoning Models Don't Always Say What They Think.* https://arxiv.org/abs/2505.05410 — CoT reveals actual influence <20% of the time.
[^10]: Check Point Research / NVD (2025). *CVE-2025-59536.* https://nvd.nist.gov/vuln/detail/CVE-2025-59536 — hook auto-execution on session events.
