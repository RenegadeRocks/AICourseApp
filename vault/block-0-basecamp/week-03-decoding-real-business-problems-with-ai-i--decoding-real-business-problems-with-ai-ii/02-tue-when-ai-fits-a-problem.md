---
type: lesson
block: block-0-basecamp
week: week-03
day_of_cycle: 2
day_name: tue
session_slug: decoding-real-business-problems-with-ai-i
date_due: 2026-05-12
tags: [fit-rubric, prioritization, rice, build-vs-buy, prediction-machines, agentic-ai, techno-solutionism, evals, product-discovery]
sources:
  - agrawal-gans-goldfarb-prediction-machines
  - mckinsey-state-of-ai-2025-agents
  - mckinsey-seizing-agentic-advantage
  - hamel-husain-evals-faq
  - husain-shankar-pm-evals
  - cagan-ai-pm-two-years-in
  - a16z-enterprise-ai-2025
  - metr-long-tasks-2025
  - bc-tribunal-moffatt-air-canada-2024
  - klarna-ai-rollback-2025
  - intercom-rice-framework
  - marily-rice-a-framework-2024
  - bcg-ai-at-work-2025
  - stanford-aicoop-prediction-machines-updated-2022
  - simon-willison-lethal-trifecta
last_verified: 2026-07-17
word_count_target: 6000
---

# When AI fits a problem — deciding AI vs deterministic code vs human, and how to prioritize the work

## Why this matters

You are the AI operator now. A founder, a COO, or a head of customer support will walk into your office this quarter with a deck that says "let's use AI for this." Roughly half the time, the problem is a terrible fit for AI. Another quarter, AI is a fit but not the *highest-leverage* fit on the portfolio. Your job is not to build what they asked for. Your job is to decide — in minutes, not weeks — whether this problem belongs to AI, to deterministic code, to humans, or to some partition across all three; and then to rank it against the eight other things you could be building.

This lesson is about the decision that happens before any prompt is written. Two moves: a **fit rubric** that tells you whether AI even belongs here, and a **prioritization frame** (a modified RICE with an eval-confidence column) that tells you where it sits in the queue. By the end you will produce, for a real problem you are holding right now, a one-page AI-fit evaluation: rubric score + build/buy/wrap recommendation + RICE with eval-confidence, ready to show a skeptical CFO.

## Prerequisites

- [[week-01-basecamp-part-1-prompting-rags--basecamp-part-2-vibe-coding/01-mon-prompting-first-principles|Prompting from first principles]] — because the fit question and the prompting question interact.
- [[01-mon-problem-discovery-frameworks|Monday's lesson on problem discovery]] — the fit question assumes a validated job.
- Working knowledge of at least one shipped deterministic system you own, and at least one AI feature you've shipped or seriously prototyped. If both are zero, this lesson will feel theoretical; go build something small first.

---

## Layer 1 — The three-option frame

For any candidate problem, there are exactly three implementation substrates, and a production system is almost always a *partition* across them, not a pure play:

1. **Deterministic code** — if/else, SQL, regex, solvers, typed APIs. Input X always produces output Y. Testable. Auditable. Cheap at runtime. Brittle under ambiguity.
2. **Human judgment** — a person, sometimes several, making a call. Expensive per unit, slow, inconsistent across operators, but infinitely flexible and socially legitimate. Courts, regulators, and angry customers prefer a human in the loop.
3. **AI (stochastic model)** — an LLM or specialized model that maps fuzzy input to fuzzy output via a learned distribution. Handles ambiguity and scale. Fails silently. Not reliably reproducible. Eval rather than test.

Any problem worth arguing about can be graded on five axes that determine which substrate wins each slice of it.

### Axis 1 — Failure cost asymmetry

What does a wrong output cost, and is the cost of a false positive equal to the cost of a false negative?

- **Symmetric, low cost**: "suggest a subject line for this email." Wrong answer costs nothing; user ignores it. AI wins.
- **Symmetric, high cost**: "categorize this legal document as privileged or not." Wrong answer is bad either way. Needs AI + human confirmation at a threshold.
- **Asymmetric, high-cost false negative**: "detect fraud in a wire transfer." Missing a fraud costs $50k; a false alarm costs 30 seconds of support time. Bias the threshold aggressively and accept human review on positives — AI is a *funnel*, not a decider.
- **Asymmetric, catastrophic failure**: "approve a loan," "dose a patient," "fly a plane." If there is any regime where a single wrong answer makes the front page of the newspaper or lands you in tribunal, the prediction must not be allowed to act unilaterally. Deterministic rules + human review must own the decision; AI can only *advise*.

The *Moffatt v. Air Canada* decision in February 2024 is the reference case for why failure cost matters more than accuracy.[^1] The airline's chatbot hallucinated a retroactive bereavement-fare policy. The British Columbia Civil Resolution Tribunal ruled — explicitly rejecting the "chatbot is a separate legal entity" defense as "remarkable" — that Air Canada was liable for every word the bot produced on its website. Damages were small ($812 CAD), but the precedent is huge: if your AI speaks on your behalf to a customer about a *refundable commitment*, you own the hallucination. This was not an accuracy problem (the base rate of hallucination was probably <5%); it was a failure-cost-asymmetry problem nobody had priced in.

### Axis 2 — Volume

- **High volume, low marginal value per case**: inbound support tickets, ad copy variations, product tagging on a million SKUs. AI's unit economics dominate. Humans cost too much.
- **Low volume, high marginal value**: M&A diligence on a single deal, a CEO's quarterly letter, a regulatory filing. Humans dominate; AI may assist. The question "should I use AI to write the S-1?" is the wrong question. The right question is "which of the 400 sub-tasks inside writing an S-1 are high-volume-enough and low-stakes-enough?"
- **Medium volume, medium value**: the interesting zone. This is where partitioning matters. Route 80% of cases through an AI triage → auto-handle the confident slice deterministically → escalate the uncertain slice to a human. Concrete instance: Zendesk's 2024–2025 AI Agents/Copilot pattern — inbound tickets triaged by an LLM classifier, the high-confidence slice auto-resolved, low-confidence tickets routed to a human agent with LLM-drafted suggestions attached rather than auto-sent.[^zendesk-triage]

### Axis 3 — Ambiguity tolerance

Can the problem be specified precisely, or does specification itself require judgment?

- A tax-bracket calculation has zero ambiguity. Use code.
- "Is this customer email angry?" has moderate ambiguity; humans disagree ~15% of the time. Fair game for AI, with inter-annotator-agreement benchmarks as the accuracy ceiling.
- "Is this marketing copy on-brand?" has high ambiguity. An AI can match an empirical distribution of *past* on-brand copy, but brand drift is a human-judgment problem. Hybrid.
- "Is this startup worth investing in?" has adversarial ambiguity; the best humans disagree wildly. No substrate wins cleanly. This is a place where AI will confidently produce a wrong answer that sounds right, which is worse than a human who admits uncertainty.

### Axis 4 — Consistency requirements

If the *same input* must yield the *same output* every time — for legal, regulatory, accounting, or fairness reasons — AI is the wrong substrate. LLMs are non-deterministic even at temperature 0 in practice (batching, kernel-level float ordering, version drift). A policy saying "applicants with identical credit files must get identical decisions" is incompatible with a raw LLM. You can regain consistency with caching, classical ML models, or a deterministic post-processing layer — but then AI is only the prototyping tool, not the runtime.

### Axis 5 — Auditability

- If a regulator, a plaintiff's lawyer, or a board member may one day ask *"why did the system do this?"* you need a traceable reason. LLM chain-of-thought is **not a reliable explanation** — the research is clear that models often *rationalize* answers they have already committed to rather than reason from the chain they produce.[^2]
- Deterministic code: auditable by inspection.
- Human: auditable by interview, with legal standing.
- AI: auditable only through logged inputs, logged outputs, eval artifacts, and a paper trail of evaluator notes. If you cannot commit to that paper trail, do not ship AI into the regulated slice of the problem.

### Putting the five axes together

A production decision-support system for a mid-market commercial lender might partition as follows:

- **Fetch and normalize 40 data fields from bank statements**: deterministic code (OCR + rules). Cost of error: small and recoverable. Consistency: required.
- **Draft a narrative summary of the applicant's business**: AI. Ambiguity: high. Failure cost: low (a human reads it next). Volume: one per application.
- **Score credit risk**: deterministic (classical ML or scorecard). Auditability: regulator-facing. Consistency: required by law.
- **Recommend ancillary products**: AI. Volume: high. Failure cost: near-zero.
- **Final credit decision**: human. Failure cost: catastrophic. Auditability: legal.

The naive answer ("let's use an LLM agent for the whole loan workflow") fails at axes 1, 4, and 5 simultaneously. The experienced answer is always a partition.

---

## Layer 2 — The good-fit / bad-fit rubric

Drawing on Agrawal, Gans, and Goldfarb's *Prediction Machines* frame — restated and updated for the 2024-2026 LLM era — every task decomposes into **prediction, judgment, action, outcome**.[^3] AI is a cheap prediction machine. The question "is this an AI problem?" reduces to: *can the interesting part of this task be cast as a prediction problem whose errors are tolerable?*

### Good-fit signatures

| Signature | Example | Why it fits |
|---|---|---|
| **Fuzzy matching** | Dedupe two customer records with typos | Humans disagree on edge cases; exact rules break |
| **Language translation / rephrasing** | Localize product descriptions | Quality distribution matters more than any single answer |
| **Summarization** | Compress a 200-page discovery dump to 3 pages | No unique "right" summary; fitness-for-use is the metric |
| **Pattern recognition at scale** | Classify 2M support tickets into 40 topics | Humans set the ontology; AI applies it consistently enough |
| **Taste / aesthetic judgment under a distribution** | Generate on-brand marketing variants | Humans reject the bad ones; volume dwarfs review time |
| **Soft extraction from unstructured text** | Pull 12 fields from an arbitrary contract | Deterministic parsers fail on long-tail formats |
| **Conversational triage** | Route customer messages to the right team | Low cost of being off-by-one; escalation path exists |

### Bad-fit signatures

| Signature | Example | Why it fails |
|---|---|---|
| **Exact arithmetic or financial calculation** | Compute a tax liability | LLMs confabulate digits; use a function call or code |
| **Safety-critical deterministic rule** | Interlock a physical machine | Non-determinism is disqualifying |
| **Novel regulatory compliance** | "Is this SEC filing compliant with a rule issued last week?" | Training cutoff + high cost of error + low tolerance for rationalization |
| **Exact retrieval from a known corpus** | "What did this patient's chart say on Feb 3?" | Retrieval beats generation; if you let the LLM hallucinate here, you ship a lawsuit |
| **Long-horizon planning with irreversible actions** | "Run payroll autonomously" | Agent reliability compounds badly over steps |
| **Decisions requiring social legitimacy** | Fire an employee | Even a perfectly correct AI decision is legally and morally indefensible without a human |
| **Truly novel reasoning under evidence** | Scientific discovery from first principles | LLMs interpolate within training; out-of-distribution is where they confabulate most |

The "obvious-but-wrong" pattern is almost always a **bad-fit signature dressed up as a good-fit one**. The "unintuitive-but-right" pattern is almost always a **good-fit signature inside a domain that feels too serious for AI** (e.g., legal summarization, medical discharge summaries, actuarial triage).

### Case: the obvious-but-wrong answer — Klarna's 2024 customer service AI

In February 2024 Klarna announced its AI assistant was doing "the work of 700 agents" and handling 2.3M conversations a month.[^4] Headlines followed. By 2025, CEO Sebastian Siemiatkowski admitted the rollout had gone too far: customer satisfaction scores dropped, complaints rose, and Klarna started hiring humans back under a new "Uber-style" flexible-agent model.[^5]

Run the rubric on what Klarna actually shipped:

- **Failure cost asymmetry**: high. A customer refund mishandled by a bot in front of a user with their money on the line is a brand event, not a ticket.
- **Ambiguity tolerance**: high in the tail. 80% of tickets are "where is my order." 20% are emotionally loaded, multi-step, or contain claims the bot cannot verify.
- **Consistency**: low requirement — variance is tolerable.
- **Auditability**: moderate — post-hoc review matters for repeat offenders.
- **Volume**: massive. This is why AI looked good.

The mistake was **skipping the partition**. The right system is: AI handles the 80% head, deterministic routing handles the unambiguous slice, humans own the 20% tail *where failure is expensive and ambiguity is highest*. Klarna's public narrative "AI replaces agents" forced a monolithic deployment that violated axes 1, 3, and 5. Siemiatkowski's 2025 walk-back is not an indictment of AI in customer service; it is an indictment of *unpartitioned* AI in customer service.

### Case: the unintuitive-but-right answer — long legal-document summarization

Every first instinct says law is too serious for a hallucinating model. But inside a litigation team, the highest-cost activity is *first-pass document review* — junior associates reading every page of a 500,000-document production, tagging for relevance and privilege. The task is:

- High volume (millions of pages per matter).
- Moderate ambiguity (relevance is a judgment call; privilege is a rule).
- Fuzzy matching (the same concept appears rephrased across documents).
- Low unit cost of a first-pass false positive (a second-pass human reviewer catches it).
- Auditability resolved *at the second-pass*, not the first.

This is why "contract AI" and "e-discovery AI" have real traction and customer service AI has bumpy traction: the partition is natural, the human-in-the-loop is already baked in, and the economics of the human-alone baseline are so bad that even 70%-accurate AI is a massive upgrade. The unintuition comes from *importing your gut feeling about the domain's seriousness* instead of *running the rubric*.

---

## Layer 3 — Build vs buy vs wrap

Once you have decided AI fits, there is a second question that kills more projects than the first: *where does the AI come from?*

Three options. In 2026 terms:

1. **Build** — train, fine-tune, or RLHF your own model. Reasonable only if you have proprietary data, regulatory constraints demanding on-prem, or genuinely novel capability needs. For 99% of enterprise teams this is the wrong answer in 2026; the capability gap between a frontier API and your custom model is enormous, and the maintenance burden crushes small teams.
2. **Wrap** — call a frontier API (Claude, GPT, Gemini) inside your own application, with your own prompts, retrieval, evals, and UX. This is the default for anything not commoditized.
3. **Buy** — purchase a vendor product that has already wrapped the model for your use case (e.g., Glean for enterprise search, Harvey for legal drafting, Cursor for code).

The a16z 2025 enterprise-AI survey of 100 CIOs captures the shift explicitly: the market moved from "build direct on models" in 2023 to a mature "buy the app, mix-and-match the model" pattern by 2025.[^6] Procurement now looks like traditional software buying — benchmarks, evals, hosting reviews. Switching costs are rising because workflows wrap deeply around tools.

### A decision tree that actually terminates

```
Q1: Is your edge the data or the distribution, not the model?
    └─ Yes → don't build. Wrap or buy.
    └─ No  → you probably don't have an edge; re-examine.

Q2: Does a credible vendor exist, ship-ready, for >60% of your use case?
    └─ Yes → buy; extend with a thin wrap for the residual 40%.
    └─ No  → wrap.

Q3: Would buying lock you out of the differentiated UX?
    └─ Yes → wrap; the UX IS the moat.
    └─ No  → buy.

Q4 (fine-tune gate, only if you're still thinking of training):
    Do you have:
      (a) >10k high-quality labeled examples you own,
      (b) a measurable eval showing frontier APIs hit a ceiling, AND
      (c) a runtime cost profile that makes API calls economically fatal?
    └─ All three yes → fine-tune a smaller model.
    └─ Anything no   → don't.
```

The failure mode people describe most — *"we trained our own model and it never caught up with GPT-4"* — almost always comes from Q4 being answered on vibes rather than on evidence. If you cannot produce the eval that shows the frontier API is actually hitting a task-specific ceiling, you are not ready to fine-tune.

### When "wrap" is better than "buy"

Wrap when any of the following hold:

- Your problem spans several vendor categories (none covers >60%).
- Your differentiator is the prompt library, the evals, the fine-grained retrieval, or the UX — things the vendor cannot see.
- Your data cannot leave your VPC, and no vendor offers a hosting model compatible with your risk posture.
- Your volume is large enough that vendor markup on top of model API cost becomes punitive.

### When "buy" beats "wrap"

- Vendor has category-specific data you don't (e.g., legal-specific training corpora behind agreements you cannot replicate).
- Integration surface is wide (e.g., 40+ connectors to SaaS apps); you will never build them all.
- Time to value is weeks and the ROI model only works if you ship this quarter.
- The vendor has an evaluator team, compliance paperwork, and a SOC2/ISO/HIPAA posture you would otherwise have to staff.

---

## Layer 4 — Prioritization: RICE with an eval-confidence column

Once you have a *portfolio* of AI-fit problems — and you always will, because every function in the business has three candidates — you need a frame that ranks them. The default in product orgs is RICE (Reach × Impact × Confidence / Effort), developed by Sean McBride at Intercom.[^7] It is a sound skeleton, but applied naively to AI projects it produces garbage for one specific reason: **the "Confidence" column silently conflates two different things for AI**.

### The confidence problem

For a deterministic project, "Confidence" means *"how sure am I that my estimates of Reach, Impact, and Effort are right?"* — roughly, how well-specified the work is. For an AI project, there is a second and larger source of uncertainty: **will the model actually be accurate enough on this task in production?** You can have perfectly-estimated Reach and Impact, and still face a 40% probability that eval accuracy will land below the threshold needed to ship.

So for AI project prioritization, split Confidence into two columns:

- **Estimate-confidence (C_est)** — the traditional RICE confidence: how well-specified are R, I, and E?
- **Eval-confidence (C_eval)** — what is your probability that the system will hit the eval bar required to ship to production?

**Modified RICE-for-AI**:

```
RICE_AI = (Reach × Impact × C_est × C_eval) / Effort
```

This is the quiet move that changes which projects rise in a portfolio. A project with massive Reach and Impact but *unknown eval-confidence* should not outrank a smaller project with high eval-confidence — because the first project has a fat left tail of "spent six months and shipped nothing." The classic RICE collapses this tail into Effort (badly) or Confidence (worse). Splitting it out forces the team to write down the probability.

There is an existing framework in this space, RICE-A, which adds an "AI Complexity" multiplier.[^8] It's a reasonable step but still conflates *complexity of the build* (already in Effort) with *probability of hitting eval bar* (the thing that actually kills AI projects). Separating eval-confidence as its own Bayesian term is sharper.

### Estimating eval-confidence honestly

The honest answer is: *run the evals before you commit.* Hamel Husain's operating position — echoed across a year of 2025 posts — is that **error analysis and evals come first, not last**. You cannot estimate eval-confidence without at least a minimum viable eval.[^9] His protocol, condensed:

1. Collect 20-50 realistic input examples, not toy ones, before building anything.
2. Produce expected-behavior annotations on each (you, a teammate, a domain SME).
3. Run the cheapest end-to-end system you can stand up — a single frontier-model prompt is fine.
4. Score the outputs. Read the failures with your eyes.
5. Group failures into categories. The category distribution *is* your prioritization input for the next iteration.
6. Your eval-confidence for the full project is roughly: *probability that the observed error categories can be driven below tolerance with reasonable effort* — estimated by the team, with numbers not vibes.

This is not expensive. It's a day of work before you write a PRD. The ROI is immediate: half of candidate AI projects fail step 4 so badly that the right decision is to stop, and the RICE sheet never needs to be filled out.

### A live controversy — is RICE even the right frame?

There is a real dispute in 2025-era AI product thinking. Two positions:

**Position A — keep RICE (with eval-confidence).** It is the common language of product, engineering, and finance. Your CFO understands it. Your head of product already uses it. Adding one column is a ten-minute change. Fighting the norm costs more than the frame is worth.

**Position B — replace RICE with an eval-driven prioritization.** Husain-style: *don't prioritize features at all; prioritize error categories in the eval dataset.* The project manager's output is not a roadmap of features, it is a ranked list of error categories with hypotheses about what prompt, retrieval, or data change will move each one.[^10] This is closer to how the best AI product teams actually operate in 2025-2026.

**My take.** Use both, at different altitudes. RICE-with-C_eval is the *portfolio* frame — which of my eight candidate projects do I staff next quarter, shown to the exec team. Husain's eval-category prioritization is the *within-project* frame — once the project is staffed, your day-to-day prioritization is error categories, not features. They do not compete; they sit on different levels of the org. Teams that insist on one or the other end up either (a) shipping incoherent AI features that never clear the eval bar but looked great in the roadmap deck, or (b) having crisp within-project workstreams while the exec team has no idea which three of those workstreams should even exist.

---

## Layer 5 — A second live controversy: does "agentic" change the fit question?

This is the harder fight in 2026. Two positions, both defensible, both with 2025 data behind them.

**Position A — agents expand the addressable problem space.** The McKinsey *State of AI in 2025* survey reports 62% of respondents are at least experimenting with AI agents, and the firm's agentic-advantage thesis is that agents unlock the "vertical" gen-AI use cases that have been stuck in pilot mode — function-specific workflows where a non-agentic copilot was insufficient because the work requires multi-step planning, tool use, and autonomous follow-through.[^11][^12] The implication for the fit rubric is that problems previously scored "bad fit — too long-horizon" move into "good fit — agent-sized task" because the substrate got more capable.

METR's long-task measurement supports this empirically: the length of task that a frontier model can complete with 50% reliability has been doubling roughly every 7 months over the past six years, with some 2024-2025 sub-trends (notably the SWE-Bench Verified slice) showing doubling times closer to three months — i.e., the trend may be accelerating on software tasks specifically.[^13] If the trend holds, the "long-horizon planning with irreversible actions" bad-fit signature in the rubric above will migrate toward "medium fit with guardrails" within the life of any system you design this year.

**Position B — agents are a cost multiplier with reliability issues; pick simpler patterns unless forced.** The same METR paper is explicit that *50% reliability is nowhere near production bar*. The best 2025 frontier models reliably complete tasks of only *a few minutes* — and reliability degrades sharply as horizon extends. Adoption data echoes this: 87% of IT executives rate interoperability as crucial for agentic AI, but only a minority of enterprises are in production — the rest are piloting or evaluating. The BCG 2025 survey of AI-at-work reports strong individual productivity gains from non-agentic copilots and much thinner, more skeptical adoption of autonomous agents.

Simon Willison's *lethal trifecta* problem (private data + untrusted content + exfiltration channel) gets worse, not better, as agents gain tool access.[^14] Every new tool in the agent's belt is a new prompt-injection vector.

**My take.** The honest L3 position is that *agentic* is a rubric-axis question, not a rubric-beating answer. For every candidate problem, ask:

1. Does the task decompose into <5 sequential steps with well-defined handoffs? (If yes, probably agentic-ready.)
2. Is every step reversible or cheaply undoable if wrong?
3. Do you control the tools the agent calls, or does the agent call an untrusted external surface?
4. Can you express a *per-step* success criterion, testable independently?
5. What is the compound reliability? (0.9 per step × 5 steps = 0.59 overall.) This is not just arithmetic: METR's March 2025 task-length study shows end-to-end success rates collapsing in exactly this pattern as agent horizons stretch from minutes to hours[^13], and 2024-era multi-step browser-agent evals landed in the 14–22% end-to-end range on OSWorld/WebArena — the compound-loss pattern, measured.[^osworld-webarena] (Frontier computer-use scores have climbed substantially since; treat those figures as the shape of the effect, not current state of the art, and re-pull the leaderboard before quoting them to a client.)

If any of 2-5 fails, you are not ready to deploy an agent on this problem; you are ready to deploy a *workflow* (deterministic orchestration with AI steps) that looks agent-like from the outside. Most "agentic" wins that shipped at scale in 2025 were, on inspection, scripted workflows with AI inside the steps — not autonomous planners — and the McKinsey-Deloitte-Gartner adoption numbers were measuring the former dressed as the latter.

One important 2026 amendment: **this claim is now domain-scoped, not general.** In the coding domain specifically, genuinely autonomous production agents graduated — OpenAI's Codex passed 5 million weekly users by June 2026 (roughly one in five of them not developers), Gartner published its first Magic Quadrant for Enterprise AI Coding Agents, and OpenAI reports 97.9% of its own employees now use agents (a self-reported number from the vendor, but directionally hard to dismiss).[^codex-2026] Delegated-ticket agents like Devin and headless Claude Code run real backlogs autonomously. Outside coding — customer operations, finance, general knowledge work — the workflow-in-a-trenchcoat diagnosis still holds for most shipped deployments. The fit-rubric consequence: score agent-compatibility against your domain's demonstrated ceiling, not against coding's.

The recommendation: **in the fit rubric, add "agent-compatibility" as a sixth axis, not a replacement for the first five.** Agents do not change whether AI fits the problem; they change *what shape* the AI system takes once it fits.

---

## Layer 6 — Failure modes in the wild

Five patterns you will see this year. Name them, and you will intervene earlier.

1. **Techno-solutionism.** The exec has read a McKinsey piece and wants "AI for X" where X is a bad-fit signature. Counter-move: run the rubric on a whiteboard, live, in the meeting. Do not let the conversation proceed without five axes scored.
2. **Trend-following.** A competitor launched an AI feature; your team wants parity. Counter-move: ask what *their* evaluation would look like if run honestly. Usually they have not run one.
3. **Human-in-the-loop cost denial.** The ROI model assumes 80% automation and a 20% human queue. The queue's operational cost — routing, training, SLA monitoring, shift coverage — is always 2-3× what the model predicted. Counter-move: demand a full-stack cost estimate including queue ops, not just "AI replaces X FTEs."
4. **Eval theater.** The team builds a benchmark that the system passes by construction. Counter-move: require an adversarial eval set written by someone not on the team, and a "red-team week" before launch.
5. **Ignoring the partition.** The Klarna pattern. Monolithic AI deployment when the right answer is AI + deterministic + human. Counter-move: in the rubric session, force a per-sub-task assignment. If every sub-task lands in "AI," your decomposition is too coarse.

---

## Reviewer lens — where I disagree with the received wisdom

Five specific disagreements you should hold as the AI operator:

1. **Against "*Prediction Machines* is foundational, not current."** The 2022 updated edition is foundational *and* current; the framing of "cheap prediction shifts the value of judgment and action" maps cleanly onto the LLM era.[^3] The common L1 critique that "it's pre-LLM" misses that the economics do not depend on the model architecture — they depend on the cost curve of prediction. LLMs just drove the cost down faster than the book's 2018 prediction. The framework holds harder than ever.

2. **Against Marty Cagan's "product discovery saves everything" frame.** Cagan's claim that the discovery discipline makes AI product management tractable is correct in spirit but under-specifies the eval problem.[^15] Classical discovery outputs — risk assessments, value hypotheses — do not answer "will the model be accurate enough on this task?" That gap is what Husain's eval-first position fills. You need both; Cagan alone is not enough for AI-era PM.

3. **Against the a16z "buy is winning" narrative.** The a16z 2025 enterprise survey frames the build-to-buy shift as maturity. Partly true — but partly a sampling artifact (they survey the enterprises mature enough to be buying). For startups and AI-native products, *wrap* is still the dominant mode, and the best wraps look like new categories, not vendor extensions. Reading a16z as "stop building" is the wrong read. The right read is "stop training models; keep building products on top of APIs."

4. **Against RICE-A's single-multiplier fix.** RICE-A adds "AI Complexity" as a fifth term, which is neat but wrong-shaped.[^8] AI risk is not one complexity number; it is a probability distribution over shipping. The eval-confidence split captures that better. If you must keep a single-multiplier frame for stakeholder simplicity, compute it *from* eval-confidence + estimate-confidence, don't invent a new vibes-based number.

5. **Against the McKinsey agentic-AI thesis as stated.** The *Seizing the Agentic AI Advantage* paper is a useful strategic frame but overstates how much of the "agentic" category is actually agentic as opposed to scripted workflow.[^12] Named instance: Salesforce Agentforce 1.0's 2024 launch was marketed as autonomous agents, but the production pattern shipping with most early customers is deterministic flow orchestration with LLM steps at classification/drafting nodes — Salesforce's own Agentforce 2dx/3 materials and the cautionary reporting around Gartner's June 2025 forecast that "over 40% of agentic AI projects will be cancelled by end of 2027" (still the operative Gartner forecast as of mid-2026) describe this gap directly.[^agentic-reality] Read alongside the METR reliability data.[^13] The honest mid-2026 posture: *scripted workflows with AI steps* remains the default for most enterprise risk profiles — with coding agents as the demonstrated exception (see Layer 5's 2026 amendment) and the leading indicator of where other domains may follow.

---

## Exercise — produce your 1-page AI-fit evaluation

This is the artifact. Pick a real problem — something a stakeholder has asked you about in the last 30 days, or something your own team is considering. Not a hypothetical.

Produce a single page with four sections:

### Section 1 — The rubric scorecard

Fill in this table (directly, with numbers, not prose):

| Axis | Score 1-5 (5 = strong AI fit) | One-line rationale |
|---|---|---|
| Failure cost asymmetry | | |
| Volume | | |
| Ambiguity tolerance | | |
| Consistency requirements | | (invert: high requirement = low score) |
| Auditability | | (invert: regulated = low score) |
| Agent-compatibility | | (only if multi-step) |

Any axis scoring ≤2 is a **stop-and-partition signal**: either the problem splits into sub-tasks where AI owns only the high-scoring slice, or you reject AI as the substrate for this project. Write the partition explicitly.

### Section 2 — Build vs buy vs wrap recommendation

Walk the decision tree from Layer 3. For each question (Q1-Q4), write one sentence of answer. Conclude with a single-line recommendation: *"Wrap a frontier API because X"* or *"Buy vendor Y because Z"* or *"Don't do this; here's the deterministic / human alternative."*

### Section 3 — RICE-AI with eval-confidence

| Column | Value | Notes |
|---|---|---|
| Reach (per quarter) | # of users or events | |
| Impact (0.25 / 0.5 / 1 / 2 / 3) | | per standard RICE |
| C_est (0-100%) | | confidence in R, I, E estimates |
| C_eval (0-100%) | | probability eval bar is cleared, based on minimum eval if run |
| Effort (person-months) | | fully loaded |
| **RICE_AI score** | (R × I × C_est × C_eval) / E | |

If you have not run the minimum eval (Husain protocol, Layer 4), mark C_eval as "NOT ESTIMATED — running day-of-work eval before committing" and return to the exercise in a week.

### Section 4 — The risks you are accepting

Three bullets, specific:

- The worst realistic failure mode, with a named example from your domain.
- The eval gap you are not closing, and why you are accepting it (cost, time, not worth it).
- The decision trigger that would cause you to kill the project (e.g., "if eval accuracy at end of month 1 is below 75%, we stop").

**Deliverable**: one PDF or markdown page, under 600 words total across the four sections, that you could hand a CFO in a 10-minute meeting. If it runs over 600 words, you are narrating instead of deciding. Cut.

---

## Common mistakes experts see

1. **Scoring the rubric on feelings.** The axes are quantitative. If you cannot put a dollar figure on failure cost, a per-quarter number on volume, or an inter-annotator-agreement rate on ambiguity, you are not done.
2. **Scoring the whole problem instead of the partition.** Most problems are heterogeneous. The rubric scores a *task*, not a *system*.
3. **Treating C_eval as a guess instead of an empirical number.** Run the minimum eval. It is a day of work. The guess version is worth nothing.
4. **Comparing AI to no-system instead of to the deterministic/human baseline.** Every RICE sheet should include a "baseline = current human or rule-based system" row for comparison. AI's RICE_AI must beat the baseline's RICE, not just be positive.
5. **Ignoring the queue.** Every partition with a human-in-the-loop implies a queue with ops cost. Budget it.
6. **Confusing "agent" with "workflow."** If your architecture diagram has fixed arrows between steps, you have a workflow. Do not market it as agentic, and do not price the reliability as agentic.
7. **Trusting the vendor demo.** Vendor demos are the cleanest possible case on the cleanest possible data. Your production data is the long tail. Always extend the vendor eval to your own dataset before signing.

---

## Reflection questions

1. Name a problem in your current org where AI is the *obvious-but-wrong* answer. Score it on the rubric. Which axis kills it?
2. Name a problem where AI is the *unintuitive-but-right* answer. What bias made it look wrong initially?
3. For the lending-workflow partition in Layer 1, which sub-task would you be most tempted to over-automate, and why?
4. Your CFO asks "why is eval-confidence a separate column?" — answer in one sentence, non-technical.
5. In your domain, what is the Moffatt-v-Air-Canada case? If there isn't one yet, what does one look like?
6. Pick one bad-fit signature. Design a partition that lets AI still contribute 20-30% of the value without owning the decision.
7. For an agentic problem you have considered, compute compound reliability at 0.9 per step for the actual step count. At what horizon does the product become unshippable?
8. When would you override the decision tree and *build* a model in 2026? Be specific about the three gates.

---

## Further reading

**Must-read**

- Agrawal, Gans, Goldfarb, *Prediction Machines* (updated 2022). The economic frame beneath everything in this lesson.[^3]
- Hamel Husain, *LLM Evals: Everything You Need to Know* (2025).[^9]
- Moffatt v. Air Canada, BC Civil Resolution Tribunal decision, Feb 2024.[^1]
- McKinsey, *The State of AI in 2025: Agents, innovation, and transformation.*[^11]

**Recommended**

- Andreessen Horowitz, *How 100 Enterprise CIOs Are Building and Buying Gen AI in 2025.*[^6]
- METR, *Measuring AI Ability to Complete Long Tasks* (Mar 2025).[^13]
- Marty Cagan, *AI Product Management 2 Years In* (SVPG, 2025).[^15]
- Simon Willison, *The Lethal Trifecta* posts (2023-2025).[^14]

**Optional**

- RICE-A framework write-up on AI PM Jobs.[^8]
- Klarna coverage in *Entrepreneur* and *CX Dive* (2025) for the rollback narrative.[^4][^5]

---

## Citations

[^1]: *Moffatt v. Air Canada*, 2024 BCCRT 149 (Feb 14, 2024). Summary and analysis: McCarthy Tétrault, "Moffatt v. Air Canada: A Misrepresentation by an AI Chatbot." https://www.mccarthy.ca/en/insights/blogs/techlex/moffatt-v-air-canada-misrepresentation-ai-chatbot. ABA Business Law Today, "BC Tribunal Confirms Companies Remain Liable for Information Provided by AI Chatbot" (Feb 2024). https://www.americanbar.org/groups/business_law/resources/business-law-today/2024-february/bc-tribunal-confirms-companies-remain-liable-information-provided-ai-chatbot/
[^2]: See [[week-01-basecamp-part-1-prompting-rags--basecamp-part-2-vibe-coding/01-mon-prompting-first-principles|Layer 3 of Monday's prompting lesson]] for the Lanham-2023 and Turpin-2023 citations on chain-of-thought unfaithfulness.
[^3]: Ajay Agrawal, Joshua Gans, Avi Goldfarb, *Prediction Machines: The Simple Economics of Artificial Intelligence* (updated and expanded edition, HBR Press, 2022). Framework page: https://www.predictionmachines.ai/
[^4]: Entrepreneur, "Klarna Is Hiring Customer Service Agents After AI Couldn't Cut It on Calls, According to the Company's CEO" (2025). https://www.entrepreneur.com/business-news/klarna-ceo-reverses-course-by-hiring-more-humans-not-ai/491396
[^5]: CX Dive, "Klarna changes its AI tune and again recruits humans for customer service" (2025). https://www.customerexperiencedive.com/news/klarna-reinvests-human-talent-customer-service-AI-chatbot/747586/
[^6]: Andreessen Horowitz, "How 100 Enterprise CIOs Are Building and Buying Gen AI in 2025." https://a16z.com/ai-enterprise-2025/
[^7]: Intercom, "RICE: Simple Prioritization for Product Managers" (Sean McBride). https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers/
[^8]: Marily Nika, "RICE-A: A Prioritization Framework for AI-Driven Features" (AI PM Jobs, Jan 21 2025). https://marily.substack.com/p/rice-a-a-prioritization-framework
[^9]: Hamel Husain, "LLM Evals: Everything You Need to Know" (Hamel's Blog, 2025). https://hamel.dev/blog/posts/evals-faq/ — see also "Your AI Product Needs Evals" https://hamel.dev/blog/posts/evals/
[^10]: Hamel Husain and Shreya Shankar, "The PM's Role in AI Evals: Step-by-Step" (Aakash Gupta, 2025). https://www.news.aakashg.com/p/hamel-shreya-podcast
[^11]: McKinsey, "The state of AI in 2025: Agents, innovation, and transformation." https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai
[^12]: McKinsey, "Seizing the agentic AI advantage" (2025). https://www.mckinsey.com/capabilities/quantumblack/our-insights/seizing-the-agentic-ai-advantage
[^13]: METR, "Measuring AI Ability to Complete Long Tasks" (March 2025). https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/ — arXiv preprint https://arxiv.org/html/2503.14499v1
[^14]: Simon Willison, "The Lethal Trifecta" — see Monday's prompting lesson for the citation chain.
[^15]: Marty Cagan, "AI Product Management 2 Years In" (Silicon Valley Product Group, 2025). https://www.svpg.com/ai-product-management-2-years-in/
[^zendesk-triage]: Zendesk, "AI Agents" and "Copilot for agents" product documentation (2024–2025). https://www.zendesk.com/service/ai/ai-agents/ ; https://www.zendesk.com/service/ai/copilot/ — partition pattern: LLM triage + auto-resolve confident slice + human-in-loop with drafted reply for the uncertain slice.
[^osworld-webarena]: OSWorld (Xie et al., NeurIPS 2024) https://arxiv.org/abs/2404.07972 and WebArena (Zhou et al., ICLR 2024) https://arxiv.org/abs/2307.13854 are the standard multi-step computer-use / web-agent benchmarks. Frontier models reported sub-25% end-to-end success in 2024–2025 evaluations — a measured instance of compound-reliability collapse across a multi-step trajectory rather than a per-step accuracy ceiling.
[^agentic-reality]: Salesforce, Agentforce product materials (2024–2025). https://www.salesforce.com/agentforce/ — Agentforce 2dx/3 release notes document the shift from "autonomous agent" marketing toward explicit flow-orchestration with human-in-loop hand-offs. Gartner, "Over 40% of Agentic AI Projects Will Be Canceled by End of 2027" (Jun 25, 2025). https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-predicts-over-40-percent-of-agentic-ai-projects-will-be-canceled-by-end-of-2027 — the "agent-washing" thesis cites the mismatch between marketed autonomy and shipped workflow.

[^codex-2026]: TechJack Solutions, *OpenAI Codex Passes 5 Million Weekly Users, and 1 in 5 Aren't Developers* (June 2026). https://techjacksolutions.com/ai-brief/openai-codex-passes-5-million-weekly-users-and-1-in-5-arent/ ; OpenAI, *OpenAI named a Leader in enterprise coding agents by Gartner* (2026 Gartner Magic Quadrant for Enterprise AI Coding Agents). https://openai.com/index/gartner-2026-agentic-coding-leader/ ; The Register, *OpenAI says 97.9 percent of its employees are now using agents* (Jun 25, 2026 — all figures self-reported by OpenAI). https://www.theregister.com/ai-and-ml/2026/06/25/openai-says-979-percent-of-its-employees-are-now-using-agents/5262499 All verified 2026-07-17.

_last_verified: 2026-07-17_
