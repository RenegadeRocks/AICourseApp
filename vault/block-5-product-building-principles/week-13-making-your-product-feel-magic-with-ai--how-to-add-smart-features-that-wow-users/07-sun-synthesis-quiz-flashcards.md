---
type: lesson
block: block-5-product-building-principles
week: week-13
session_slug: how-to-add-smart-features-that-wow-users
day_of_cycle: 7
day_name: sun
date_due: 2026-08-16
tags:
  - synthesis
  - quiz
  - flashcards
  - week-review
sources:
  - chartmogul-ai-churn-wave-2026
  - cdt-dark-patterns-chatbots-2026
  - dellacqua-jagged-frontier-2023
  - structured-outputs-reliability-2026
  - hamel-evals-faq-2026
last_verified: 2026-07-17
word_count_target: 3200
---

# Synthesis, quiz, and flashcards — magic and smart features

## The week in one arc

Magic is not a bigger model; it is a design discipline you can decompose and
engineer. A feature feels magical when it collapses effort the user expected to
spend, produces a result inside the range the user considers correct, and does
so at the right timing and agency. Miss any one and magic becomes slop, creepy,
or forgettable.

The week built a single reusable architecture, and every day added a layer to it:

- **[[01-mon-what-magic-actually-is|Mon]]** — the definition, the four textures
  (anticipation, effort-collapse, invisible intelligence, appropriate agency),
  the four anti-patterns (chatbot bolt-on, needs-a-manual, uncanny
  over-automation, AI-slop), and the jagged frontier that makes magic uneven.
- **[[02-tue-the-proactive-ambient-pattern|Tue]]** — the proactivity rungs (0
  defaults → 4 autonomous), the trust layer (legible context, undo, honest
  confidence, worthwhile timing), and the magic/creepy line: creepy is hidden
  context + vendor-serving goal + costly rejection.
- **[[03-wed-generative-and-personalization-features|Wed]]** — the
  editable-output pattern, personalization without contamination or leakage,
  structured outputs that drive UI (static gen-UI as the default, declarative
  A2UI/MCP-Apps as the deliberate frontier), and per-feature cost/latency
  routing.
- **[[04-thu-reliability-of-magic|Thu]]** — the wrong-answer-costs-more
  asymmetry, confidence gating and abstention, the degrade-to-non-AI fallback,
  eval-gating with a golden set, and blast-radius-sized ship policy.
- **[[05-fri-prioritizing-smart-features|Fri]]** — retention value vs demo value,
  loaded effort, the value/(effort×risk) triage, the sequence of magic, feature
  validation, and the AI-feature graveyard.
- **[[06-sat-build-add-one-magical-feature|Sat]]** — you composed all of it into
  one shipped feature with a fallback, an eval harness, and a trust metric.

The reusable shape underneath everything: **the reliable part is deterministic,
the jagged part is AI, and the human holds the irreversible action.** If you
remember one sentence from Week 13, that is it.

## The two controversies, resolved

**Proactive AI: helpful or creepy?** Neither inherently. Proactivity is creepy
when three conditions combine (hidden context, vendor-serving goal, costly
rejection) and magical when their opposites hold. You can build maximally
proactive features that are not creepy by keeping all three on the magic side. The
CDT taxonomy of 37 chatbot dark patterns is the map of what happens when you do
not.[^1]

**How much magic to ship before it is reliable?** The rung determines the gate.
Low-blast-radius features (ignorable suggestions, reversible defaults) can
ship-and-see; high-blast-radius features (sends, deletes, spends, trusted
numbers) must eval-gate. Blast radius, not team philosophy, sets the policy.

**Are AI features retention drivers or churn gimmicks?** The variable is
integration depth and effort-collapse on the core loop. Woven-in features that
collapse real effort for committed users retain like normal software (85% NRR
above $250/mo); bolted-on novelties that displace effort into review, chasing
self-serve tourists at a low price, accelerate churn (23% GRR under $50/mo).[^2]

---

## Quiz (13 questions)

Take it cold, without re-reading. Answers follow.

**Q1 (MCQ).** Which three conditions must all hold for a feature to feel magical?
- a) Big model, low latency, nice UI
- b) Effort collapsed, result inside the acceptable range, right timing/agency
- c) Chat interface, example prompts, streaming
- d) Personalization, memory, autonomy

**Q2 (MCQ).** A product ships a floating "Ask AI" bubble that answers questions
about the app, with example prompts underneath. Which two anti-patterns is this?
- a) Uncanny over-automation and AI-slop
- b) Chatbot bolt-on and needs-a-manual
- c) Effort-collapse and anticipation
- d) Invisible intelligence and appropriate agency

**Q3 (short answer).** In one sentence, state the "jagged frontier" and why it
matters for feature design.

**Q4 (MCQ).** On the proactivity spectrum, which rung should you generally reach
for *first* when it delivers the value?
- a) Rung 4 (autonomous action) for maximum wow
- b) Rung 3 ("we did this for you")
- c) Rung 0 (smart defaults) / Rung 1 (inline suggestions)
- d) Whichever demos best

**Q5 (short answer).** State the magic/creepy line in terms of the three
conditions that make proactivity creepy.

**Q6 (MCQ).** GitHub Copilot's inline suggestions run around a 38% acceptance
rate and users love the feature anyway. Why is a majority-rejected feature still
magical?
- a) The model is very large
- b) A declined inline suggestion costs the user nothing
- c) It streams
- d) It personalizes

**Q7 (code/short answer).** You are generating a draft into a text field. Name
two properties of the "editable-output pattern" that keep it from feeling like
slop.

**Q8 (MCQ).** For a high-frequency, low-stakes feature (e.g. autocomplete), the
correct model-routing choice in 2026 is generally:
- a) Claude Opus 4.8 or Fable 5 for maximum quality
- b) Claude Haiku 4.5 (cheapest, fastest)
- c) Always the newest model
- d) Whatever the frontier leaderboard tops

**Q9 (short answer).** Why does the "wrong answer costs more than a missing
answer" asymmetry push most features toward *precision over recall*?

**Q10 (MCQ).** Which is a valid fallback for a proactive suggestion feature when
the model is unavailable or low-confidence?
- a) Show an error toast
- b) Retry the model five times
- c) Show no suggestion (suppress) or a deterministic template
- d) Render the partial model output

**Q11 (short answer).** Hamel Husain says do X before writing your eval rubric.
What is X, and why?

**Q12 (MCQ).** The ChartMogul 2026 data shows AI-native products under $50/month
retain how much gross revenue year-over-year, and what is the operator lesson?
- a) 70% — low price is fine
- b) 23% — integration depth and committed pricing beat cheap self-serve
- c) 82% — same as normal SaaS
- d) 48% — annual plans do not help

**Q13 (short answer).** State the reusable architecture of shippable magic in one
sentence (the shape every feature this week followed).

---

## Answer key

**A1.** b. Effort collapsed, result inside the acceptable range, and right
timing/agency. Missing any one yields slop, creepy, or forgettable — not magic.
([[01-mon-what-magic-actually-is|Mon]])

**A2.** b. Chatbot bolt-on (a surface competing with the real UI) and
needs-a-manual (the example prompts *are* the manual). ([[01-mon-what-magic-actually-is|Mon]])

**A3.** The jagged frontier is that AI is dramatically better than humans at some
tasks and worse at others, with an invisible, irregular boundary; it matters
because magic lives on one side and confident-wrong failure on the other, so you
must scope features to the reliable slice and detect when an input falls off the
edge.[^3] ([[01-mon-what-magic-actually-is|Mon]])

**A4.** c. Use the lowest rung that delivers the value; a smart default that is
right 80% of the time often out-delights an autonomous action that is right 95%,
because the default costs nothing when wrong. ([[02-tue-the-proactive-ambient-pattern|Tue]])

**A5.** Proactivity is creepy when three conditions combine — hidden context (the
user did not know you had it), a vendor-serving goal, and costly/impossible
rejection — and magical when their opposites hold (legible context, user-serving
goal, free rejection). ([[02-tue-the-proactive-ambient-pattern|Tue]])

**A6.** b. A declined inline suggestion costs the user nothing, so low acceptance
is not a failure; the design constraint of the suggestion rung is exactly that
rejection is free and default.[^4] ([[02-tue-the-proactive-ambient-pattern|Tue]])

**A7.** Any two of: generate into an editable surface (not read-only); mark the
generated content as a draft until touched; preserve one-action regenerate and
revert; never overwrite existing user work. Framing output as an editable
starting point converts inevitable model misses from product failures into "a
draft I improved." ([[03-wed-generative-and-personalization-features|Wed]])

**A8.** b. Route by stakes and frequency; a high-frequency low-stakes feature
goes to Haiku 4.5. Using Opus/Fable for autocomplete turns a loved feature into a
margin-eating line item.[^5] ([[03-wed-generative-and-personalization-features|Wed]])

**A9.** Because a confident wrong output is attributed to your product and
remembered (costly), while a missing output is a non-event (cheap); maximizing
precision and abstaining when uncertain minimizes the expensive failures at the
cost of some cheap ones. ([[04-thu-reliability-of-magic|Thu]])

**A10.** c. Suppress (show nothing) or fall back to a deterministic template.
Both are valid, always-working degradations; an error toast, infinite retries, or
partial output are not. ([[04-thu-reliability-of-magic|Thu]])

**A11.** Error analysis — read every real failure by hand and cluster the failure
modes *before* writing the rubric, because the rubric you imagine before seeing
real errors is usually wrong.[^6] ([[04-thu-reliability-of-magic|Thu]])

**A12.** b. 23% GRR under $50/month; the lesson is that integration depth and
committed (higher-priced, annual) pricing drive retention, while cheap self-serve
AI attracts tourists who churn.[^2] ([[05-fri-prioritizing-smart-features|Fri]])

**A13.** The reliable part is deterministic, the jagged part is AI, and the human
holds the irreversible action. ([[06-sat-build-add-one-magical-feature|Sat]])

**Scoring:** 11–13 correct, you are fluent — walk into the live session ready to
argue. 8–10, re-read the day that owns your misses. Below 8, re-run the week's
reflection questions before the live session.

---

## Flashcards (30)

Q: What three conditions must simultaneously hold for a feature to feel magical?
A: Effort collapsed (that the user expected to spend), result inside the
acceptable range, and right timing/agency.

Q: Name the four textures of magic.
A: Anticipation, effort-collapse, invisible intelligence, appropriate agency.

Q: Name the four anti-patterns of AI features.
A: Chatbot bolt-on, feature-that-needs-a-manual, uncanny over-automation,
AI-slop.

Q: What is the difference between effort-collapse and effort-displacement?
A: Collapse removes the task; displacement moves work from doing the task to
reviewing/fixing the AI's attempt — the signature of slop.

Q: What is the "jagged frontier"?
A: AI is dramatically better than humans at some tasks and worse at others, with
an invisible irregular boundary; magic lives on one side, confident-wrong failure
on the other.

Q: Why is "just use a better model" not a magic strategy?
A: A better model moves the frontier outward but it stays jagged; the
confident-wrong failures on the new far side are just as damaging.

Q: State the magic/creepy line in one sentence.
A: A proactive action is magical when the user would have chosen it and can
cheaply reverse it; creepy when it uses information the user did not know you had
or takes an action they cannot undo.

Q: Name the five rungs of the proactivity spectrum.
A: 0 smart defaults, 1 inline suggestions, 2 background enrichment, 3 "we did
this for you" summaries/drafts, 4 autonomous action.

Q: What is the proactivity design principle regarding rungs?
A: Use the lowest rung that delivers the value; reversibility and near-zero
interruption at low rungs often out-delight higher rungs.

Q: What five trust decisions are baked into ghost-text autocomplete?
A: Visually subordinate (grey), rejection is default, inline not modal,
precomputed for speed, gates on confidence (suggests less when unsure).

Q: What are the three creepy conditions for proactive AI?
A: Hidden context, vendor-serving goal, costly/impossible rejection.

Q: What is the rule about agency and reversibility?
A: Each increment of agency requires a matching increment of reversibility; the
send/delete/post needs a confirmation.

Q: What is the editable-output pattern?
A: Generate into an editable surface, mark it as a draft until touched, keep
one-action regenerate/revert, and never overwrite user work.

Q: Name the three failure modes of personalization.
A: Context contamination, cross-user leakage, creepy (inferred/cross-context)
personalization.

Q: How do you personalize without context contamination?
A: Use the smallest sufficient context retrieved for the current task, not the
largest available; more user data past a point is noise.

Q: How do you prevent cross-user data leakage?
A: Scope every retrieval, cache, and memory lookup to a server-verified user/org
identity; test it adversarially.

Q: Static vs declarative generative UI — which is the default and why?
A: Static (model picks among your pre-built, trusted components) is the default:
safe, testable, on-brand, no injection surface. Declarative (A2UI/MCP-Apps) is a
deliberate frontier choice.

Q: What is A2UI?
A: Google's open-sourced (2026) declarative, framework-agnostic generative-UI
spec where agents send component descriptions rendered from a client-held catalog
of trusted components.

Q: 2026 structured-output reliability: OpenAI vs Anthropic failure rates?
A: OpenAI Structured Outputs < 0.1%; Anthropic tool-use < 0.2% (single
end-of-stream block, no progressive field parsing). Always validate on your side.

Q: How should you route models per feature?
A: By stakes and frequency: Haiku for high-frequency/low-stakes (autocomplete),
Sonnet as default, Opus/Fable for rare high-stakes generation.

Q: State the wrong-answer asymmetry.
A: For a user-facing feature, a confident wrong output costs far more (attributed,
remembered) than a missing one (a non-event) — so favor precision over recall and
abstain when uncertain.

Q: List the four gates of a reliable feature, cheapest first.
A: Deterministic precondition, provider-call wrapped/timed so it cannot throw,
schema validation, confidence threshold.

Q: What is the degradation contract?
A: Detect (how you know to degrade), degrade (the non-AI path), disclose (whether
the user needs to know they got the fallback).

Q: What must always be true of a feature's fallback path?
A: It always works, needs no model, and can never itself throw.

Q: What decides ship-and-see vs eval-gate?
A: Blast radius. Low (reversible, low-stakes) → ship-and-see; high (irreversible,
trusted, acting on the user's behalf) → eval-gate.

Q: Name three metrics that gate a feature before ship.
A: Precision on shown outputs (≥ ~0.85), graceful-degradation rate (100%), zero
adversarial harms (no leakage/unauthorized action/confident high-stakes error).

Q: What does Hamel Husain say to do before writing an eval rubric?
A: Error analysis — read and cluster real failures first; the pre-imagined rubric
is usually wrong. And grow the golden set from production failures.

Q: Demo value vs retention value — which to build for?
A: Retention value (does the recurring core-loop task get easier so users return).
Demo value drives signups and evaporates under the disappearance test.

Q: The 2026 AI-retention split by price tier (ChartMogul)?
A: >$250/mo → 70% GRR/85% NRR (normal SaaS); $50–249 → 45%/61%; <$50 → 23%/32%.
Integration depth + committed pricing retain.

Q: State the reusable architecture of shippable magic.
A: The reliable part is deterministic, the jagged part is AI, and the human holds
the irreversible action.

---

## What to bring to the live session

- Your one shipped feature and its eval output. Be ready to defend the blast-radius
  call and the rung choice.
- A position on the proactive-AI controversy: where is *your* feature on the
  three creepy conditions?
- One thing that surprised you when you swapped the mock provider for the real
  model — the golden case that failed first.

## Citations

[^1]: Center for Democracy & Technology, *Dark Patterns in AI Chatbots*, May 2026,
https://cdt.org/insights/dark-patterns-in-ai-chatbots-a-taxonomy-to-inform-better-design/.
(search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^2]: ChartMogul, *The SaaS Retention Report: The AI churn wave*, 2026,
https://chartmogul.com/reports/saas-retention-the-ai-churn-wave/. Corroborated by
Growth Unhinged, https://www.growthunhinged.com/p/the-ai-churn-wave.
(search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^3]: Dell'Acqua et al., *Navigating the Jagged Technological Frontier*, HBS WP
24-013 (2023), https://www.hbs.edu/faculty/Pages/item.aspx?num=64700. (evergreen
research; primary source)

[^4]: GitHub Copilot inline-suggestion acceptance ~38% (Q1 2026): RapidDevelopers,
https://www.rapidevelopers.com/blog/how-does-cursors-ai-powered-autocomplete-feature-work-2026-guide,
and VS Code docs, https://code.visualstudio.com/docs/editing/ai-powered-suggestions.
(search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^5]: Current Anthropic model lineup/pricing per the course refresh,
`vault/00-program/_refresh-2026-07-master-report.md`. (verified 2026-07-17 in
master report)

[^6]: Hamel Husain, *LLM Evals FAQ*, hamel.dev, 2026,
https://hamel.dev/blog/posts/evals-faq/. (evergreen method; primary source)

_last_verified: 2026-07-17_
