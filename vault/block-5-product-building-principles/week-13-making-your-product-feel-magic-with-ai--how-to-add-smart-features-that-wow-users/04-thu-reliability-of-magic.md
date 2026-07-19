---
type: lesson
block: block-5-product-building-principles
week: week-13
session_slug: how-to-add-smart-features-that-wow-users
day_of_cycle: 4
day_name: thu
date_due: 2026-08-13
tags:
  - feature-reliability
  - confidence-gating
  - abstention
  - graceful-degradation
  - fallback-path
  - eval-gating
  - feature-trust-metric
sources:
  - wen-abstention-survey-2024
  - openai-why-llms-hallucinate-2025
  - structured-outputs-reliability-2026
  - anthropic-building-effective-agents-2024
  - hamel-evals-faq-2026
  - nngroup-state-of-ux-2026
  - veracode-genai-code-security-2025
  - chartmogul-ai-churn-wave-2026
last_verified: 2026-07-17
word_count_target: 5600
---

# Reliability of magic: when features fail in public

## Why this matters

Magic that breaks in front of a user is worse than no magic at all. A feature
that never existed costs nothing; a feature that confidently produced a wrong
answer, sent a bad email, or hallucinated a number costs trust, and trust does
not come back on the next good output. This lesson is the engineering that lets
you ship magic without shipping the confident-wrong failures the jagged frontier
guarantees: confidence gating, abstention, graceful degradation to non-AI paths,
eval-gating a feature before it ships, and measuring feature trust as a
first-class metric. It is also where you resolve this week's second controversy:
how much magic to ship before it is reliable. On Saturday, this is the lesson
that keeps your one feature from becoming a cautionary tale.

## Prerequisites

- The jagged frontier from [[01-mon-what-magic-actually-is|Monday]] and the
  confidence-in-the-UI point from
  [[02-tue-the-proactive-ambient-pattern|Tuesday]]. Today makes them mechanical.
- Eval discipline is canonical in
  [[06-sat-rag-evaluation|Block 2 Week 4]] and unattended reliability in
  [[05-fri-reliability-engineering-for-unattended-agents|Block 3 Week 8]]. We
  apply both to a *user-facing feature*, which is a different blast radius than a
  backend agent.

## The core asymmetry: a wrong answer costs more than a missing one

Start from the asymmetry that governs every decision in this lesson. For a
user-facing AI feature, the cost of a confident wrong output is far higher than
the cost of no output. A missing suggestion is a non-event; a wrong-but-confident
suggestion that the user acts on is a failure they attribute to your product and
remember. OpenAI's own 2025 analysis of why language models hallucinate makes the
mechanism concrete: standard training and evaluation reward *guessing* over
*admitting uncertainty*, so models are systematically biased toward producing a
confident answer even when they should abstain, exactly the behavior that is most
dangerous in a product.[^1]

This asymmetry inverts the usual "maximize coverage" instinct. For most features
you want to **maximize precision, accept lower recall, and abstain when
uncertain.** Cursor Tab's design choice from Monday (21% fewer suggestions, higher
acceptance) is this asymmetry made product: suggest less, be right more.[^2] A
feature that abstains gracefully on the 20% of inputs it cannot handle well, and
nails the 80% it can, feels more magical than one that attempts all 100% and is
confidently wrong on a fifth of them.

## Confidence gating and abstention

The mechanism that implements the asymmetry is a gate: before showing a
generation, decide whether the model is confident enough to show it, and if not,
degrade. Abstention (the model or system declining to answer when unreliable) is
an active research area with a growing toolkit; Wen et al.'s survey catalogues
the approaches, from calibration-based thresholds to consistency checks to
learned abstention.[^3] You do not need the research frontier; you need a gate
that works. Here are the practical signals, cheapest first.

**1. Deterministic preconditions (cheapest, most reliable).** Before you call the
model at all, check whether the input is in the feature's competence. The CRM
draft-follow-up feature suppresses when the deal has fewer than two prior
messages: a deterministic "is there enough context?" check that needs no model
call. Most of your gating budget should live here, because a precondition you can
compute in code is more reliable than any confidence the model reports about
itself.

**2. Schema/validation gating.** If the structured output fails schema validation
(Zod/Pydantic), that is a hard gate: do not render it. Given OpenAI Structured
Outputs fails under 0.1% and Anthropic tool-use under 0.2%, this gate fires
rarely, but the sub-1% is exactly the case you must not render into UI.[^4]

**3. Self-reported confidence (useful, not trusted alone).** Ask the model to
return a confidence field alongside the output. It is a weak signal on its own —
models are poorly calibrated and biased toward confidence[^1] — but combined with
a threshold and validated against your eval set, it is a usable third gate. Never
make it the *only* gate.

**4. Consistency / cross-path checks (for high-stakes features).** Generate
twice (or with two prompts, or verify with a second cheap model) and gate on
agreement. Expensive, so reserve it for features where a wrong output is costly.
This mirrors the numerical cross-path check from
[[06-sat-build-the-weekly-report-generator|Block 2 Week 5's build]].

The gate's output is not binary "show/hide"; it is a *degradation level*. High
confidence: show the generation. Medium: show it marked as a draft with lower
visual confidence. Low: suppress the generation and fall back. Design the gate to
select among these, not just to toggle.

## Graceful degradation: the fallback to a non-AI path

The most important architectural rule in this entire week: **every magical
feature has a non-AI path it degrades to, and that path always works.** When the
model is unavailable (rate limit, outage, timeout), uncertain (gate says low
confidence), or wrong (validation fails), the feature does not error, does not
hang, and does not show broken output. It falls back to something useful and
deterministic.

What the fallback is depends on the feature:

- **Generation feature** → fall back to a template, a set of canned options, or
  the plain manual entry surface. The draft-follow-up feature falls back to a
  blank editable field with two template quick-replies. The user is exactly where
  they would have been without the feature: no worse off, never blocked.
- **Proactive suggestion** → fall back to *no suggestion*. Suppressing is a valid
  fallback. A quiet feature is better than a wrong one.
- **Personalization** → fall back to a sensible global default. If the
  per-user model call fails, serve the same good default everyone gets.
- **Structured-output-drives-UI** → fall back to the manual version of that UI
  (the empty form, the default view). Never render partial or invalid structure.

The degradation contract has three parts, and you should be able to state all
three for your feature: **detect** (how do you know to degrade — timeout,
gate, validation failure?), **degrade** (what is the non-AI path?), and
**disclose** (does the user know they got the fallback, and do they need to?).
For most features the fallback is silent (the user never needs to know the model
was skipped); for a few, disclosure matters ("we could not draft this one, here
is a blank template"). The design skill is choosing silence versus disclosure per
feature.

This is the same reliability discipline as
[[05-fri-reliability-engineering-for-unattended-agents|Block 3 Week 8]], with one
difference in blast radius: a backend agent's failure is seen by you (in a log);
a user-facing feature's failure is seen by the user (in the product). That raises
the stakes on the fallback path and lowers your tolerance for "it usually works."

## Eval-gating a feature before it ships

You do not ship a magical feature on vibes and hope; you ship it behind an eval
that says it clears a bar. The eval discipline is canonical in
[[06-sat-rag-evaluation|Block 2 Week 4]] — the pieces you reuse: a labeled test
set, a scoring function, binary rubrics over 1–5 scores, and a threshold that
blocks ship. The feature-specific adaptation:

**The test set is a golden set of real inputs with expected properties.** Not
expected exact outputs (generation is not deterministic) but expected
*properties*: for draft-follow-up, "mentions the deal's actual product," "does
not invent a price," "matches the concise tone," "would not embarrass the user."
20–50 real cases spanning the frontier: easy cases the feature must nail, hard
cases on the jagged edge where you expect abstention, and adversarial cases
(prompt injection in the contact's message, an empty deal, a hostile input).

**The metrics that gate ship:**

1. **Precision on shown outputs.** Of the generations the gate decided to show,
   what fraction cleared the quality bar? This is the number that determines
   whether the feature feels magical. Threshold: high — 0.85+ for most features,
   higher for consequential ones.
2. **Graceful-degradation rate.** Of the cases where the model failed, timed out,
   or was gated low, what fraction produced a valid, usable fallback with no
   error and no broken UI? Threshold: 100%. A single crash-to-error on the
   fallback path is a block-ship, because the whole promise of the feature is
   that it never leaves the user worse off.
3. **Coverage (secondary).** Of the cases where the feature *should* fire, how
   often did it? Lower coverage is acceptable (abstention is a feature); track it
   so you know how much magic you are leaving on the table, but do not optimize it
   at the expense of precision.
4. **No-harm on adversarial cases.** Zero cases where an adversarial input caused
   data leakage, an unauthorized action, or a confidently wrong high-stakes
   output. Threshold: zero. This is Simon Willison's prompt-injection reality
   applied as a gate.

Hamel Husain's core methodological point applies directly and is worth honoring:
do *error analysis first*, evals second. Run the feature on your golden set, read
every failure by hand, cluster the failure modes, and *then* write the rubric
from the failures you actually observed — do not pre-commit to a rubric that
imagines failures.[^5] The rubric you invent before seeing real errors is usually
wrong; the rubric you derive from twenty hand-read failures is usually right.

## The controversy: ship-and-see vs eval-gate

This is the week's second live controversy, and it does not have a single answer.
Two named positions:

**The eval-gate position (Hamel Husain, the reliability camp).** Do not ship an
AI feature to users until it clears an eval bar on a golden set, because
user-facing failures are expensive, memorable, and hard to walk back, and because
"ship and watch production" on a feature that can confidently do harm is how you
get the Veracode outcome — the 2025 GenAI code-security research found that
AI-generated code introduced security vulnerabilities in roughly 45% of cases,
the archetype of "shipped confident output that was quietly wrong."[^6] The eval
gate is cheap relative to the cost of a public failure.

**The ship-and-see position (the velocity camp, and a fair reading of early
Seibel-style advice).** Evals built before you have real users are built against
imagined inputs; the fastest way to learn what actually breaks is to ship the
ugly version to a small number of real users, instrument it heavily, and let
production tell you the failure modes you could not have guessed. Over-investing
in an eval harness pre-launch is a way to feel productive while delaying the only
feedback that matters.

**The synthesis, sized by blast radius.** These are not actually opposed once you
condition on the cost of a failure:

- **Low blast radius** (fully reversible, low-stakes, user clearly in control —
  e.g. an inline suggestion the user can ignore): ship-and-see is correct. The
  cost of a wrong output is a shrug; production is the fastest teacher. Instrument
  it, watch acceptance rate, iterate.
- **High blast radius** (irreversible, high-stakes, or acting on the user's
  behalf — e.g. anything that sends, deletes, spends, or produces a number the
  user will trust): eval-gate is correct, and non-negotiable. The cost of a wrong
  output is trust or money you cannot recover, so pay the eval cost first.
- **The gradient in between:** ship-and-see behind a smaller cohort with a tighter
  fallback, graduate to wider release as the eval set (built from the cohort's
  real failures) fills in and the metrics clear the bar.

So the honest rule is: **the rung determines the gate.** Rung 0–1 features
(defaults, ignorable suggestions) can ship-and-see. Rung 3–4 features (drafts you
present as done, autonomous actions) must eval-gate. The blast radius, not the
team's philosophy, sets the policy.

> My take: most first-time builders get this exactly backwards. They over-gate
> their harmless inline suggestion (delaying learning) and under-gate their
> auto-send (courting disaster), because gating *feels* like diligence and they
> apply it uniformly. Size the gate to the blast radius and you get both velocity
> and safety.

## Measuring feature trust

"Feature trust" sounds soft; make it a number. A feature the user does not trust
is a feature they stop using, so trust is a leading indicator of the retention
that Friday cares about. Concrete, instrument-able trust metrics:

- **Acceptance / edit-distance rate.** For generation features, what fraction of
  outputs does the user accept unchanged, lightly edit, or discard? Rising accept
  and falling edit-distance means rising trust. This is the single best
  feature-trust signal and it is cheap to log.
- **Override / undo rate.** For proactive actions, how often does the user
  reverse or override what the feature did? A high undo rate means the feature is
  acting where the user disagrees — a trust and calibration problem.
- **Opt-out rate.** How many users turn the feature off? The off-switch from
  Tuesday is also your bluntest trust metric.
- **Post-failure re-engagement.** After a user sees the feature fail (or fall
  back), do they use it again? A feature that survives its own failures has earned
  trust; one that users abandon after one bad output has a fragile fallback or too
  many failures.
- **Abstention appropriateness.** When the feature abstained, was that the right
  call? Sample abstentions and label them; over-abstention wastes magic,
  under-abstention courts confident-wrong failures.

NNG's *State of UX 2026* frames the meta-point: trust is now the central design
problem for AI features, built from transparency, control, consistency, and
graceful failure handling — the exact four things this lesson operationalizes.[^7]
The feature-trust number is how you know whether you built them.

## Worked example — the reliability spec for one feature

Complete the draft-follow-up feature's reliability layer, which you will
implement Saturday.

**Blast radius:** medium. The draft is presented (rung 3) but the *send* is
manual, so no irreversible action fires without the user. Policy: eval-gate the
draft quality, ship-and-see the exact wording.

**Gates, in order:**
1. Deterministic precondition: deal has ≥2 prior messages, else suppress (fall
   back to nudge-only).
2. Schema validation on `{subject, body, confidence, used_context_ids}`, else
   fall back to template.
3. Confidence threshold on the returned `confidence` field (calibrated against
   the golden set), below which show the draft marked "low confidence, review
   carefully" or suppress, per your tuned threshold.

**Fallback path:** blank editable field plus two template quick-replies. Always
works, needs no model, no error state. Silent (the user does not need to know the
model was skipped).

**Eval gate before ship:** 30 real deals as the golden set (10 easy, 10 jagged,
10 adversarial including an injected instruction inside a contact message and an
empty deal). Metrics: precision on shown drafts ≥ 0.85; graceful-degradation rate
= 100%; zero adversarial harms (no injected instruction changes the draft's
recipient or invents a price). Error-analysis first: hand-read all 30, cluster
failures, write the rubric from what you see.

**Feature-trust metric in production:** accept-unchanged rate + edit-distance,
logged per draft, plus opt-out rate for the whole nudge class.

**Pass bar for the exercise:** you have stated the blast radius and the gate
policy it implies, three ordered gates, a fallback that always works, an eval gate
with a golden set spanning the frontier and adversarial cases, and one production
trust metric. If your fallback can throw an error, or your eval set has no
adversarial cases, it does not pass.

## Common mistakes experts see

1. **Optimizing coverage over precision.** The asymmetry says abstain when
   uncertain; a feature that attempts everything and is confidently wrong on 20%
   feels worse than one that nails 80% and abstains on the rest.[^1]
2. **Trusting model self-reported confidence as the only gate.** Models are
   poorly calibrated and biased toward confidence; combine with deterministic
   preconditions and validation.[^1][^3]
3. **No fallback, or a fallback that can itself fail.** The non-AI path must
   always work; a fallback that throws is a block-ship.
4. **Uniform gating regardless of blast radius.** Over-gating harmless features
   (slow) and under-gating consequential ones (dangerous). Size the gate to the
   rung.
5. **Writing the eval rubric before reading real failures.** Error analysis
   first; the imagined rubric is usually wrong.[^5]
6. **No adversarial cases in the eval set.** Prompt injection in
   feature-consumed content is a real surface; test it or assume you are
   vulnerable.
7. **Not measuring feature trust.** Accept rate, undo rate, and opt-out rate are
   cheap to log and predict the retention Friday depends on.[^7]

## Reflection questions

1. What is the blast radius of your Saturday feature, honestly, and what gate
   policy does it imply?
2. What is your feature's deterministic precondition — the check you can run in
   code before ever calling the model?
3. Write your feature's degradation contract: detect, degrade, disclose. Can your
   fallback ever fail?
4. What three failure clusters would you bet you will find when you hand-read 30
   real outputs? How would you find out if you are wrong?
5. Which single production number would tell you whether users trust the feature,
   and how will you log it from day one?

## My take (reviewer lens)

**Hamel Husain** would broadly endorse this lesson (it is built on his method)
but push hard on the golden-set section: 20–50 cases is a starting point, not a
finish line, and the mistake he sees most is teams building the eval set *once*
and never growing it from production failures. His correction: the eval set is a
living artifact; every real-world failure becomes a new test case, and a feature
whose eval set has not grown in a month is a feature no one is actually watching.
The lesson says "error analysis first" but under-emphasizes that it is a
*continuous* loop, not a launch gate you pass once.

**Chip Huyen** would push on the precision/recall framing as too clean for
production. Her lens: the threshold that gates "show vs abstain" is not static —
it drifts as the model updates, as your input distribution shifts, and as user
expectations rise, so a confidence threshold you tuned in August is wrong by
October unless you re-calibrate. The lesson gives you a gate; Chip would insist
the gate needs its own monitoring, and that "set a threshold" quietly becomes
"maintain a threshold," which is real ongoing work most teams do not budget.

**Lilian Weng** would note that the abstention framing treats the model as a
black box you gate around, when a meaningful part of 2026 reliability comes from
*the model's own* uncertainty and reasoning being made legible and steerable —
building the abstention into the system's reasoning, not just bolting a threshold
on the output. The steelman for the lesson's approach: for a solo builder shipping
Saturday, a deterministic precondition plus a validation gate is more reliable and
more debuggable than any elicited-uncertainty scheme, so start there; but Weng is
right that the ceiling on graceful failure is higher than a bolt-on gate reaches.

## Further reading

**Must-read:**
- OpenAI, *Why Language Models Hallucinate* (2025) — the training-incentive
  mechanism behind confident wrong answers.[^1]
- Hamel Husain, *LLM Evals FAQ* (2026) — error-analysis-first, binary rubrics,
  living eval sets.[^5]

**Recommended:**
- Wen et al., *Know Your Limits: A Survey of Abstention in Large Language Models*
  (2024) — the abstention toolkit.[^3]
- NNG, *State of UX 2026* — trust as the central AI-feature design problem.[^7]

**Optional:**
- Veracode, *2025 GenAI Code Security Report* — the cost of shipping confident
  wrong output.[^6]

## Citations

[^1]: OpenAI, *Why Language Models Hallucinate*, 2025.
https://openai.com/index/why-language-models-hallucinate/. Training/eval rewards
guessing over abstention, biasing models toward confident answers. (search-verified
2026-07-17; fetch egress-blocked — liveness pass pending)

[^2]: Cursor Tab confidence gating (~21% fewer suggestions, higher acceptance):
RapidDevelopers, https://www.rapidevelopers.com/blog/how-does-cursors-ai-powered-autocomplete-feature-work-2026-guide.
Corroborated by Tech-Insider, https://tech-insider.org/cursor-vs-copilot-2026/.
(search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^3]: Yuxin Wen et al. (survey), *Know Your Limits: A Survey of Abstention in
Large Language Models*, 2024, arXiv:2407.18418, https://arxiv.org/abs/2407.18418.
Taxonomy of abstention methods (calibration thresholds, consistency, learned
abstention). (evergreen research; primary source)

[^4]: Structured-output reliability, 2026: TokenMix,
https://tokenmix.ai/blog/structured-output-json-guide (OpenAI <0.1%, Anthropic
<0.2% failure). Corroborated by Crazyrouter,
https://crazyrouter.com/en/blog/ai-structured-output-json-mode-guide-2026.
(search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^5]: Hamel Husain, *LLM Evals: Everything You Need to Know* (FAQ), hamel.dev,
2026. https://hamel.dev/blog/posts/evals-faq/ and *Should I practice
eval-driven development?* https://hamel.dev/blog/posts/evals-faq/should-i-practice-eval-driven-development.html.
Error-analysis-first, binary rubrics, living eval sets. (evergreen method;
primary source)

[^6]: Veracode, *2025 GenAI Code Security Report* — AI-generated code introduced
security vulnerabilities in ~45% of cases, per the course landscape delta
(`vault/00-program/_refresh-2026-07-master-report.md`, cross-cutting theme 4).
(verified 2026-07-17 in master report; two-source web-verified therein)

[^7]: Nielsen Norman Group, *State of UX 2026*,
https://www.nngroup.com/articles/state-of-ux-2026/ — trust (transparency,
control, consistency, graceful failure) as the central AI-feature design problem.
Corroborated by Ehab Fayez summary, https://ehabfayez.com/en/blog/state-of-ux-2026-nielsen-norman-report.
(search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

_last_verified: 2026-07-17_
