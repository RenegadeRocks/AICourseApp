---
type: lesson
block: block-5-product-building-principles
week: week-13
session_slug: making-your-product-feel-magic-with-ai
day_of_cycle: 2
day_name: tue
date_due: 2026-08-11
tags:
  - proactive-ai
  - ambient-intelligence
  - ghost-text
  - smart-defaults
  - trust-design
  - perceived-latency
  - undo-transparency
sources:
  - cursor-tab-2026
  - copilot-inline-suggestions-2026
  - cdt-dark-patterns-chatbots-2026
  - nielsen-2026-predictions
  - streaming-perceived-latency-2026
  - nngroup-state-of-ux-2026
  - granola-recipes-2026
  - anthropic-building-effective-agents-2024
last_verified: 2026-07-17
word_count_target: 5400
---

# The proactive/ambient pattern: acting without being asked

## Why this matters

The highest form of magic is the feature that acts before the user asks and gets
it right. It is also the highest-risk form, because the same anticipation that
delights is one design decision away from feeling like surveillance or a
robot-that-touched-my-stuff. This lesson is the trust engineering of proactive
AI: how to earn the right to act on a user's behalf, how to calibrate the amount
of initiative, and where the line sits in 2026 between "helpful" and "creepy" —
a line the Center for Democracy & Technology just mapped in unflattering detail
across every major chatbot.[^1] On Saturday your feature will very likely be
proactive; today decides whether it lands as magic or as the thing users turn
off.

## Prerequisites

- [[01-mon-what-magic-actually-is|Monday's]] definition of magic and the four
  anti-patterns, especially "uncanny over-automation."
- Perceived-latency craft is canonical in
  [[02-tue-conversation-engineering|Block 3 Week 7 conversation engineering]];
  we apply it here, we do not re-derive it.
- The reliability machinery (confidence, fallbacks) is
  [[04-thu-reliability-of-magic|Thursday]] and
  [[05-fri-reliability-engineering-for-unattended-agents|Block 3 Week 8]]. Today
  is the interaction layer; Thursday is the safety layer.

## The proactivity spectrum

"Proactive" is not one thing. It is a spectrum of increasing initiative, and
each step up trades more magic potential for more trust risk. Naming the rungs
lets you pick the lowest one that delivers the value, which is almost always the
right call.

**Rung 0 — Smart defaults.** The product pre-fills the most likely choice. A
form field arrives populated, a setting is pre-selected, a category is guessed.
Zero interruption, fully reversible (just change it), and it collapses effort on
the most common path. This is the safest and most under-used rung. Most "we need
an AI feature" conversations should end here.

**Rung 1 — Suggestions (opt-in, inline).** The product offers something the user
can take or ignore with no cost. Ghost-text autocomplete, "did you mean," a
suggested reply, a recommended next action. The user is never blocked and never
surprised; the suggestion sits in peripheral vision. GitHub Copilot's inline
suggestions run at roughly a 38% acceptance rate in VS Code as of Q1 2026,
meaning users decline the majority and the feature is still beloved — because a
declined suggestion costs nothing.[^2] Low cost of rejection is the entire
design constraint of this rung.

**Rung 2 — Background enrichment.** The product does work in the margins and
presents the result when the user arrives at the relevant place. Granola
transcribing and structuring notes while you half-listen; a CRM enriching a new
contact with public data; an inbox pre-summarizing threads. The user did not ask
per-instance, but they opted into the behavior, and the output waits for them
rather than interrupting.

**Rung 3 — "We did this for you" summaries and drafts.** The product produces a
completed artifact and shows it: a drafted reply, a weekly digest, a
pre-filled report. Higher magic (real effort collapsed) and higher risk (the
artifact can be wrong, generic, or presumptuous). Safe only with a clean edit
path and honest sourcing.

**Rung 4 — Autonomous action.** The product acts in the world without a
per-action confirmation: sends, files, schedules, deletes. Maximum magic
potential, maximum trust risk, and the rung where "creepy" and "it broke my
stuff" live. This rung requires everything in this lesson plus everything in
Thursday's reliability lesson, and even then you ship it last and narrowly.

The design principle: **use the lowest rung that delivers the value.** Teams
over-reach to rung 3 or 4 for the demo impact and pay for it in trust. A smart
default (rung 0) that is right 80% of the time often out-delights an autonomous
action (rung 4) that is right 95% of the time, because the default costs the
user nothing when wrong and the autonomous action costs them cleanup and a
sense of lost control.

## Anatomy of the best proactive feature: ghost-text

Ghost-text autocomplete is worth studying in detail because it is the most
refined proactive pattern in shipping software, and its design choices
generalize.

The mechanics: as you type, a model predicts the likely continuation and renders
it in light grey inline, at the cursor. Press Tab to accept, keep typing to
ignore, and the suggestion silently updates or vanishes.[^3] Now notice every
trust decision baked into that tiny interaction:

- **The suggestion is visually subordinate.** Grey, not black. It reads as "a
  possibility," not "the answer." The typography itself communicates confidence
  level and reversibility.
- **Rejection is the default.** Doing nothing (continuing to type) declines the
  suggestion. The user never has to actively dismiss anything. Acceptance is the
  effortful action, which is correct: you want to make the *committed* action the
  deliberate one.
- **It is inline, not modal.** No popup, no context switch, no separate surface
  to manage. The intelligence is dissolved into the primary task.
- **It is precomputed for speed.** Cursor's Tab predictions feel instant partly
  because they are computed against local context with low latency; a proactive
  suggestion that arrives after the user has already typed the next word is worse
  than no suggestion.[^4]
- **It gates on confidence.** The best implementations suggest less when
  uncertain. Cursor's newer Tab model deliberately makes ~21% fewer suggestions
  to raise acceptance.[^4] Fewer, better interruptions beat more, worse ones.

Every one of those choices is portable to a non-text feature. A proactive nudge,
a suggested action, a smart default: make it visually subordinate until
accepted, make ignoring it free and default, keep it inline, make it feel
instant, and suppress it when confidence is low. If you can only remember one
sentence from this lesson, that is it.

## Designing trust for proactive AI

Proactivity is a loan of trust from the user. These are the terms that keep the
loan from being called.

### Transparency: legible context, not hidden context

Monday's magic/creepy line: anticipation on legible context is magic;
anticipation on hidden context is surveillance. Make the basis of every
proactive action legible. If your feature drafts a reply "based on this thread,"
say so and let the user see the thread. If a nudge fires because a deal went 14
days without contact, show "14 days quiet" as the reason. The user should never
have to wonder *how did it know that?* — because the honest answer to that
question is what separates a helpful product from a creepy one. CDT's taxonomy
names "informationally misleading design" and "data and memory exploitation" as
two of its five dark-pattern categories precisely because opacity about what the
system knows and did is the substrate of manipulation.[^1]

A concrete rule: **never reference, in one context, information the user gave you
in a different context, without surfacing the bridge.** If your app knows
something because the user typed it elsewhere, show that provenance when you use
it. Accurate-but-unexplained cross-context inference is the most reliable way to
make a good feature feel like spying.

### Control: undo, and the right to turn it off

Every rung above 0 needs a matching undo. Rung 3 drafts need a discard. Rung 4
actions need a reversal or, where reversal is impossible (an email is sent, a
message is posted), a confirmation *before* the irreversible step. The rule from
Monday: **each increment of agency requires a matching increment of
reversibility.** Agency without undo converts even correct output into distrust,
because the user learns the product can do things to their world that they
cannot take back.

Separately, proactive behaviors need a clean off-switch, and finding it must not
require a manual. A user who cannot easily stop a proactive feature experiences
it as something being done *to* them. The off-switch is not an admission of
failure; it is the thing that makes users comfortable leaving the feature on.

### Confidence: the right amount, honestly signaled

Proactive AI should express confidence proportional to its actual reliability,
and the interface should carry that signal. Grey ghost-text says "maybe." A
pre-filled default the user can change says "probably." An autonomous action
says "definitely," and had better be right. Mismatches are corrosive in both
directions: a hedged, apologetic UI on a reliable feature wastes the magic, and
a confident UI on an unreliable feature manufactures the confident-wrong failures
that the jagged frontier makes inevitable. Thursday operationalizes this with
confidence gating; today's point is that the *interface* must be able to express
the gate. Design the low-confidence state before the happy path, because the
low-confidence state is where trust is won or lost.

### Timing: interrupt only when the interruption is worth it

A proactive feature spends the user's attention. Spend it only when the expected
value clears the interruption cost. This is why rung 0 (defaults) and rung 1
(inline suggestions) are so strong: their interruption cost is near zero. The
moment a feature pushes a notification, a modal, or a banner, it has to justify
the tax. Jakob Nielsen's 2026 predictions flag exactly this: as AI makes it
cheap to generate proactive interruptions, the scarce resource becomes user
attention, and products that overspend it train users to ignore or disable the
whole class of feature.[^5]

## The magic/creepy line, with 2026 evidence

This is the week's first live controversy, and it is not resolved by taste
alone. The evidence:

**The case that proactive AI is structurally creepy.** CDT's May 2026 study
found 37 manipulative dark patterns across ChatGPT, Gemini, Claude, and
companion apps, organized into data/memory exploitation, misleading design,
autonomy compromise, false emotional connection, and coercive monetization.[^1]
The report's core argument is that the very features that make chatbots feel
personal (hyper-personalization, large-scale memory, frictionless interaction)
are the same features that enable manipulation.[^1] Nielsen has separately warned
of "behavioral" manipulation risks as personalization deepens.[^5] The
structural worry is real: proactivity is a capability, and capabilities get
pointed at engagement and monetization metrics unless deliberately fenced.

**The case that proactive AI is genuinely, durably loved.** Granola's users
describe its background transcription as indispensable, not invasive.[^6]
Ghost-text autocomplete is accepted tens of millions of times a day and users
choose the tools with the *more* aggressive prediction.[^2][^4] The difference is
not the amount of proactivity; it is *what it is pointed at*. Granola and Cursor
Tab are proactive in service of the user's own stated task, on legible context,
with free rejection. The CDT dark patterns are proactive in service of the
*vendor's* metrics, on hidden context, with costly or impossible rejection.

**The synthesis you should hold:** proactive AI is creepy when three conditions
combine — hidden context, vendor-serving goal, and costly rejection — and
magical when their opposites hold: legible context, user-serving goal, free
rejection. This is not a spectrum where you pick a point; it is a set of
conditions you can individually satisfy. You can build maximally proactive
features that are not creepy, if you keep all three conditions on the magic side.
That is the actionable resolution: audit every proactive feature against those
three axes before ship.

> My take: most teams get the "user-serving goal" axis right (they are not
> trying to manipulate) and lose on the other two by accident — hidden context
> because it was easier not to surface provenance, costly rejection because undo
> was a later ticket. Creepy is usually a bug of omission, not intent, which is
> good news: it is fixable with the interaction-design checklist above.

## Latency as feel: masking the wait

A proactive feature that arrives late is not proactive. Perceived latency is a
first-class part of whether proactivity feels magical, and the craft is
canonical in [[02-tue-conversation-engineering|Block 3 Week 7]]. The
product-feature-specific applications:

- **Streaming beats waiting, even at equal total time.** Rendering tokens as they
  arrive reduces perceived wait by roughly 55–70% in user testing versus a
  spinner on the same total generation time.[^7] For any generated artifact,
  stream it.
- **Skeleton states beat spinners.** A shimmer wireframe of the eventual result
  cuts perceived load time by around 40% and stops the "is it broken?"
  reaction.[^7] Before the first token, show the *shape* of what is coming.
- **Optimistic UI for reversible actions.** For a rung-1 or rung-2 action that is
  cheap to reverse, reflect the expected result immediately and reconcile with
  the server after.[^7] The user feels an instant product; the reconciliation is
  invisible unless it fails.
- **Precompute proactive suggestions.** The ghost-text lesson: a suggestion that
  is ready *before* the user reaches the decision point feels magical; one that
  arrives after feels laggy. For background enrichment (rung 2), do the work
  ahead of the user's arrival, not on their click.

The unifying idea: proactivity and latency-masking are the same design goal seen
from two angles. Both are about making intelligence *arrive at the moment the
user needs it*, so the seam between "the user wanted this" and "the product
provided it" disappears.

## Worked example — design the proactive layer for one feature

Take the "deal has gone quiet" feature from Monday's CRM example and design its
proactive layer across the rungs. No code yet; this is the interaction spec
you will implement Saturday.

**The deterministic detection (not AI):** a deal with no logged contact for N
days. Reliable, explainable, cheap. This is the trigger.

**Rung choice:** rung 1–3, never 4. Options:
- *Rung 0 flavor:* when the user opens the deal, the follow-up field is
  pre-filled with a draft (smart default). Lowest interruption.
- *Rung 1 flavor:* a subtle inline badge on the deal ("quiet 14d") with a
  one-click "draft follow-up." User pulls the suggestion.
- *Rung 3 flavor:* a weekly "3 deals need attention, drafts ready" digest. The
  product did the work; the user reviews and sends.

**Never rung 4:** auto-sending the follow-up. The email is irreversible, the
context is jagged, and one wrong send to a real client is a trust catastrophe
that outweighs a hundred saved minutes.

**Trust layer, applied:**
- *Transparency:* show "quiet 14 days" as the reason, and mark the draft as
  "based on your last 3 messages with this contact" with those messages one
  click away. Legible context.
- *Control:* the draft is fully editable; sending is a deliberate button; the
  whole nudge class has a settings toggle. Undo on everything short of the send,
  confirmation on the send.
- *Confidence:* if the deal history is thin (the jagged edge — a brand-new
  contact with no prior messages), the feature *suppresses the draft* and shows
  only the nudge, degrading from rung 3 to rung 1. Confidence gating expressed
  in the UI. Thursday builds this gate.
- *Timing/latency:* the drafts for the weekly digest are precomputed overnight,
  so the digest opens instantly with drafts already present. No spinner on the
  user's Monday morning.

**The result:** a feature that anticipates (detects the quiet deal), collapses
effort (drafts the fix), stays legible (shows its reasons), stays reversible
(edit and confirm), and degrades gracefully (suppresses the draft when the
frontier is jagged). Every axis on the magic side of every line. This is the
target shape for Saturday.

**Pass bar for the exercise:** you have written, for one feature, its
deterministic trigger, its chosen rung with a justification for not going
higher, and its four trust-layer decisions (transparency, control, confidence,
timing). If your rung choice is 4, you must justify the irreversibility or drop
to 3.

## Rung 0 deserves more of your attention than it gets

Smart defaults are the most under-invested rung, so they earn their own section.
A smart default is the product pre-selecting the most likely choice: the category
already guessed, the field already filled, the setting already right for this
user. It is proactive AI with a near-zero interruption cost and near-total
reversibility (the user just changes it), which makes it the highest
magic-per-unit-risk feature you can ship.

The reason teams skip it is the same reason they over-ship chatbots: a default is
invisible and un-demo-able. Nobody screenshots a form that arrived correctly
filled. But invisibility is the point. A default that is right 85% of the time
saves the user a decision 85% of the time and costs them a two-second correction
the other 15%, and because the correction is trivial, the *felt* experience is
"this product knows me," not "the AI was wrong." Contrast that with a rung-3 draft
that is right 85% of the time: the 15% of bad drafts each cost a review-and-fix
cycle, and the user remembers those.

Two design rules make smart defaults magical rather than annoying:

- **A default must be trivially correctable, and the correction must stick.** If
  the user changes the guessed category, the product should not re-guess and
  clobber it next time. A default that fights the user's correction is worse than
  no default. This is the memory-and-personalization discipline from
  [[02-tue-memory-and-compaction-architectures|Block 3 Week 6]] applied at the
  smallest scale: remember the correction.
- **A default should often be computed, not generated.** The cheapest smart
  default is a rule or a lookup (last value, most common value, the value a
  similar record used), not a model call. Reserve the model for the defaults a
  rule genuinely cannot produce. This keeps rung 0 instant and nearly free, which
  is exactly what makes it feel like magic rather than latency.

If you take one action from this lesson into Saturday, consider whether your
feature could be delivered as a smart default instead of a higher rung. It is
often the same value at a fraction of the risk.

## The magic/creepy audit: a field checklist

Turn the controversy resolution into something you can run in ten minutes on any
proactive feature before it ships. For each item, a "no" is a design bug to fix,
not a reason to kill the feature.

1. **Legible context.** Can the user see, at the moment of use, every piece of
   information the feature used? Is there any input that would make them ask "how
   did it know that?" If yes, surface the provenance or drop that input.
2. **User-serving goal.** Does the feature optimize the user's stated task, or a
   vendor metric (engagement, upsell, retention-by-friction)? If any part of the
   proactivity exists to serve *your* funnel rather than the user's task, it is on
   the dark-pattern side of the CDT taxonomy.[^1]
3. **Free rejection.** Can the user ignore or reverse the action at near-zero
   cost? What is the most expensive thing the feature can do that the user cannot
   cheaply undo? Is there a confirmation before it?
4. **Off-switch.** Can the user turn the whole behavior off without reading a
   manual or contacting support? Is the off-switch findable in under thirty
   seconds?
5. **Confidence honesty.** Does the UI look different when the feature is
   uncertain? Would a low-confidence output be visually distinguishable from a
   high-confidence one?
6. **Attention worth.** Does every interruption (notification, modal, banner) the
   feature generates clear the cost of the interruption? Could the same value be
   delivered at a lower rung with less interruption?

A feature that passes all six can be maximally proactive and still feel like
magic. A feature that fails two or more is on its way to the "creepy" or
"annoying" bucket regardless of how good the underlying model is. Run this audit
on your Saturday feature before you write the eval harness; it is cheaper to fix a
creepy design than a shipped one.

## Common mistakes experts see

1. **Reaching for rung 3 or 4 for demo impact.** The autonomous action demos
   better and retains worse. Use the lowest rung that delivers the value.
2. **Anticipating on hidden context without surfacing provenance.** Accurate but
   unexplained cross-context inference is the fastest route from magic to
   creepy.[^1]
3. **Shipping agency without undo.** Every rung above 0 needs a matching
   reversibility; the send/delete/post needs a confirmation.
4. **A confident UI on an unreliable feature.** The interface must be able to
   express low confidence (grey, hedged, suppressed) or it manufactures
   confident-wrong failures.
5. **Overspending attention.** Every notification and modal taxes the user; most
   proactive value can be delivered at rung 0–1 where the tax is near zero.[^5]
6. **Treating latency as an infra problem, not a feel problem.** A correct
   suggestion that arrives late is a failed suggestion. Stream, skeleton,
   precompute.[^7]
7. **No off-switch, or an off-switch that needs a manual.** A proactive feature
   the user cannot easily stop is something done *to* them.

## Reflection questions

1. For your Saturday feature, what is the lowest rung that still delivers the
   value? What would you lose by dropping one rung, honestly?
2. What context does your feature use, and is all of it legible to the user at
   the moment of use? Which piece would make a user ask "how did it know that?"
3. What is the irreversible action in your feature, if any, and what is the
   confirmation before it?
4. How does your feature's UI *look* different when it is uncertain versus
   confident? If it looks the same, that is a bug — what would you change?
5. Audit your feature against the three creepy conditions (hidden context,
   vendor-serving goal, costly rejection). Which one is closest to the line?

## My take (reviewer lens)

**Simon Willison** would push back on the trust of any autonomous rung given the
prompt-injection reality he has documented for years: a rung-4 feature that acts
on content it retrieved (an email, a scraped page, a document) is exposed to the
lethal trifecta, and no amount of undo design fixes a data-exfiltration or
unauthorized-action triggered by injected instructions. His correction is load
here: proactivity that acts on untrusted input is a security surface, not just a
UX one, and the mitigation lives in
[[03-wed-the-scraping-stack-legally-and-technically|Block 3's security material]].
The lesson's "use the lowest rung" advice is partly a security argument in
disguise, and I should have said so explicitly.

**Boris Cherny** would note that the "precompute proactive suggestions" advice is
easy to say and operationally expensive: precomputing drafts for every quiet
deal every night is real compute and real cost that scales with your user base,
and a naive implementation blows a cost budget fast (Friday's frontier). His
practical push: precompute lazily and cache aggressively, and be honest that
"feels instant" sometimes costs more than "is fast," so the latency-versus-cost
trade is a product decision, not a free win.

**A cohort peer shipping their first product** would reasonably say the whole
rung framework is over-engineered for someone with 12 users. The steelman: at 12
users you can hand-inspect every proactive action, so ship rung 1, watch what
users accept and ignore, and let the acceptance data tell you whether to climb.
The rung framework matters most at the scale where you *cannot* watch every
action, which is exactly when a wrong rung-4 choice becomes a public failure.

## Further reading

**Must-read:**
- CDT, *Dark Patterns in AI Chatbots: A Taxonomy to Inform Better Design* (May
  2026) — the definitive 2026 catalogue of proactive-AI failure modes.[^1]
- The ghost-text / inline-suggestion pattern as implemented by Cursor Tab and
  Copilot — the reference proactive interaction.[^2][^4]

**Recommended:**
- Jakob Nielsen, *18 Predictions for 2026* — attention as the scarce resource.[^5]
- The streaming/skeleton/optimistic-UI latency patterns for AI apps.[^7]

**Optional:**
- Nielsen Norman Group, *State of UX 2026* — the ambient-intelligence direction
  of travel.[^8]

## Citations

[^1]: Center for Democracy & Technology, *Dark Patterns in AI Chatbots: A
Taxonomy to Inform Better Design*, May 29 2026 (Joshi, Adjagbodjou, Luria).
https://cdt.org/insights/dark-patterns-in-ai-chatbots-a-taxonomy-to-inform-better-design/.
37 patterns; five risk categories. Corroborated by 404 Media,
https://www.404media.co/new-study-reveals-the-manipulative-dark-patterns-of-ai-chatbots/,
and MediaWell/SSRC, https://mediawell.ssrc.org/news-items/dark-patterns-in-ai-chatbots-a-taxonomy-to-inform-better-design/.
(search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^2]: GitHub Copilot inline suggestions in VS Code, ~38% acceptance rate (Q1
2026, up from ~30% in 2024), per RapidDevelopers/tech comparison,
https://www.rapidevelopers.com/blog/how-does-cursors-ai-powered-autocomplete-feature-work-2026-guide,
corroborated by VS Code docs, https://code.visualstudio.com/docs/editing/ai-powered-suggestions.
(search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^3]: Ghost-text interaction mechanics: GenText, *Ghost-text autocomplete: how
it actually works*, https://gentext.ai/blog/en/ghost-text-autocomplete-academic-writing/,
corroborated by VS Code inline-suggestions docs,
https://code.visualstudio.com/docs/editing/ai-powered-suggestions. (search-verified
2026-07-17; fetch egress-blocked — liveness pass pending)

[^4]: Cursor Tab next-edit prediction and confidence gating: RapidDevelopers,
https://www.rapidevelopers.com/blog/how-does-cursors-ai-powered-autocomplete-feature-work-2026-guide
(newer model ~21% fewer suggestions, higher acceptance; precomputed local
context for perceived speed). Corroborated by Tech-Insider,
https://tech-insider.org/cursor-vs-copilot-2026/. (search-verified 2026-07-17;
fetch egress-blocked — liveness pass pending)

[^5]: Jakob Nielsen, *18 Predictions for 2026*, jakobnielsenphd.substack.com,
https://jakobnielsenphd.substack.com/p/2026-predictions. Attention as scarce
resource; personalization/manipulation risk. Corroborated by NNG *State of UX
2026*, https://www.nngroup.com/articles/state-of-ux-2026/. (search-verified
2026-07-17; fetch egress-blocked — liveness pass pending)

[^6]: Granola AI reviews (2026), Efficient App, https://efficient.app/apps/granola,
and tl;dv, https://tldv.io/blog/granola-review/ — background transcription
described as indispensable, not invasive. (search-verified 2026-07-17; fetch
egress-blocked — liveness pass pending)

[^7]: Perceived-latency patterns for AI apps: TheFrontKit, *What Is Streaming UI
in AI Applications?*, https://thefrontkit.com/blogs/what-is-streaming-ui-in-ai-applications
(streaming reduces perceived wait ~55–70%; skeleton screens ~40%; optimistic UI
for reversible actions). Corroborated by GroovyWeb, *12 UI/UX Design Trends for
AI Apps in 2026*, https://www.groovyweb.co/blog/ui-ux-design-trends-ai-apps-2026.
(search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^8]: Nielsen Norman Group, *State of UX 2026*,
https://www.nngroup.com/articles/state-of-ux-2026/. Ambient/AI-mediated
interaction moving beneath the visible interface. (search-verified 2026-07-17;
fetch egress-blocked — liveness pass pending)

_last_verified: 2026-07-17_
