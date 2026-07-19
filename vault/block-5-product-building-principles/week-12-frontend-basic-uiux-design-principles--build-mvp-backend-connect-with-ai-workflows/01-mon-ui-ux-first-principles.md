---
type: lesson
block: block-5-product-building-principles
week: week-12
day_of_cycle: 1
day_name: mon
session_slug: frontend-basic-uiux-design-principles
date_due: 2026-08-08
tags: [ui-ux-first-principles, visual-hierarchy, wcag-2-2, accessibility, fitts-law, hicks-law, jakobs-law, interaction-design, affordances, taste-as-skill]
sources:
  - laws-of-ux-yablonski-2020
  - wcag-22-w3c-2024
  - webaim-contrast-2026
  - nngroup-genai-ux-agenda-2025
  - refactoring-ui-wathan-schoger
  - deque-color-contrast-axe
  - fitts-1954-original
  - hick-1952-original
  - norman-design-everyday-things
last_verified: 2026-07-17
word_count_target: 5500
---

# UI/UX first principles for product builders — the difference between "looks designed" and "is usable," and why taste is a learnable skill

## Why this matters (operator framing)

You have shipped agents, landing pages, and packaged offers. This week you build the surface a stranger logs into and pays for. A converting landing page can hide bad UX behind one hero and one button. A product cannot. The moment a user has to *do work* inside your app, every hierarchy mistake, every ambiguous button, every 3.9:1 contrast ratio becomes a support ticket, a churn event, or a refund. This lesson gives you the load-bearing vocabulary and the measurable rules so that when you brief Claude Code, v0, or Lovable to build a product surface, you can specify usability the way [[block-2-ai-employees/week-03-building-elegant-landing-pages--how-to-build-micro-prototypes/03-wed-design-system-literacy|design-system literacy]] taught you to specify aesthetics. The deliverable: you can audit any screen against five principles and three laws, name what is broken, and write the fix as a spec a coding agent executes.

By the end you can (1) separate visual polish from operational usability and defend the distinction, (2) apply visual hierarchy, spacing, and contrast as measurable decisions rather than taste guesses, (3) meet WCAG 2.2 AA as a floor, not an afterthought, (4) use Fitts's, Hick's, and Jakob's laws to make concrete layout calls, and (5) design affordances so users know what is clickable without a tour.

## Prerequisites

- [[block-2-ai-employees/week-03-building-elegant-landing-pages--how-to-build-micro-prototypes/03-wed-design-system-literacy|Design-system literacy]] (b2w03): the seven aesthetic variables (typography, color, spacing, density, motion, imagery, voice). This lesson does not re-teach them. It moves one layer down, from "does this look intentional" to "can a stressed user accomplish a task on this screen in the dark." Aesthetics is table stakes; usability is the product.
- One page shipped through a code-gen tool. You need a real artifact to audit in the experiment.

## The core distinction: aesthetic-usability effect, and where it lies to you

Users judge attractive interfaces as more usable. That is the aesthetic-usability effect, documented since the 1990s and catalogued as one of Jon Yablonski's Laws of UX.[^1] It is real and it is a trap. A beautiful interface earns goodwill that survives minor friction, so users forgive small usability problems and even fail to report them. Good for your NPS. Bad for your learning loop: the effect *masks* usability problems during testing, because attractiveness suppresses the complaints that would tell you what to fix.[^1]

The operator consequence is specific. A landing page can trade almost entirely on the aesthetic-usability effect, because the only task is "read and click once." A product cannot, because the effect decays fast under repeated task friction. The user who forgave your ambiguous icon on day one files a ticket about it on day thirty. So "looks designed" and "is usable" are two different axes, and this week's product surfaces need both. Monday is the usability axis. The aesthetic axis you already own from b2w03.

Don Norman's foundational framing, from *The Design of Everyday Things*, is the cleanest way to hold the two apart: good design is discoverable and understandable.[^2] Discoverability answers "what can I do here and how." Understandability answers "what does this mean, what just happened." A page can be gorgeous and score zero on both. Your job this week is to score high on both while keeping the b2w03 aesthetic bar.

## Principle 1 — Visual hierarchy: the eye should be led, not left to search

Visual hierarchy is the deliberate ordering of elements by importance so the eye lands where you want it first, second, third. It is the single highest-leverage usability variable because it operates before the user reads a word. Refactoring UI's core teaching applies directly: hierarchy is created by *contrast in weight, size, and color*, not by making the important thing big and everything else default.[^3] Amateurs make the primary action large. Professionals make the secondary and tertiary elements *recede*, so the primary reads as primary by comparison.

Three concrete moves that a coding agent will not make unless you specify them:

1. **De-emphasize supporting text.** Body copy at full-black on white fights the headline. Drop it to a muted foreground (around `oklch(0.45 0 0)` on a light surface) so the headline wins without being oversized. Refactoring UI calls this "using color and weight to establish hierarchy instead of font size alone."[^3]
2. **One primary action per view.** If two buttons look equally weighted, you have no hierarchy, you have a fork. Give the primary action solid fill and the secondary a ghost or outline treatment. This is a hierarchy decision that also happens to raise conversion.
3. **Group by proximity, separate by space.** Elements that belong together sit close; unrelated groups get more space between them than within them. This is the internal-less-than-external rule from b2w03 spacing, applied to whole layout regions, not just form fields.

The failure signature in AI-generated product screens is *flat hierarchy*: every card the same weight, every heading the same size relative to its body, three call-to-action buttons competing. The page reads "busy" and the user's eye has nowhere to land. When you see this, the fix is not "make it prettier." The fix is "cut the number of things asking for attention to one per region."

## Principle 2 — Typography and spacing as a reading system

You own the seven aesthetic variables already. Here is the usability lens on two of them. Typography and spacing are not decoration on a product surface; they are the reading system, and reading is most of what a user does inside an app.

**Measure controls comprehension.** Line length (the "measure") should sit around 45 to 75 characters for body text. Too wide and the eye loses the line return; too narrow and it jumps too often. This is a comprehension rule, not an aesthetic one. On a product dashboard where users scan tables and read notifications, a 120-character measure quietly raises error rates.

**Vertical rhythm reduces cognitive load.** Consistent spacing on a 4 or 8 pixel grid means the eye does not have to recalibrate between sections. Inconsistent spacing forces micro-decisions ("is this related to that?") on every scroll. The 8-point grid is the 2026 default across serious systems for exactly this reason.[^3]

**Density is an audience decision, not a global setting.** A financial analyst wants dense tables and small labels because they session for hours. A first-time consumer wants airy layouts and large tap targets. The mistake is applying one density everywhere. Brian Lovin's point from b2w03 holds here too: density is the most audience-indexed variable you touch.

## Principle 3 — Color and contrast: WCAG 2.2 AA is the floor, and it is legally load-bearing

Contrast is where taste and law meet. WCAG 2.2 is the current W3C standard, and its Level AA contrast requirements are the practical floor for any product you sell, especially into the EU and to any organization with a procurement checklist.[^4]

The numbers, verified current for 2026 and unchanged from WCAG 2.1:[^4][^5]

- **Normal text: 4.5:1** minimum contrast against its background (Success Criterion 1.4.3).
- **Large text: 3:1** minimum. Large is defined as 18pt (24px) regular or 14pt (19px) bold.
- **Non-text UI components: 3:1** minimum. This covers button boundaries, form-field borders, focus indicators, and the boundaries of icons that convey meaning (Success Criterion 1.4.11).

That third rule is the one AI-generated interfaces fail most. A code-gen tool loves a `slate-400` placeholder on a `slate-50` background, or a focus ring at `oklch(0.7 0 0)` that measures 2.1:1. It looks clean and it fails AA. The moment a keyboard user tabs through your form, they cannot see where focus is. That is not a polish issue; in the EU it is a compliance issue once the AI Act and existing accessibility directives bite, and it excludes real users regardless of jurisdiction.[^4]

The operational rule for briefing an agent: **state contrast as a hard constraint, not a preference.** "All text ≥ 4.5:1, all interactive borders and focus rings ≥ 3:1, verify with a contrast checker and list any element that fails." WebAIM's contrast checker is the canonical verification tool.[^5] Treat AA as the floor and reserve AAA (7:1 text) for the specific surfaces where reading is the whole job.

A note on the WCAG version to cite: WCAG 2.2 is the current W3C Recommendation as of 2026, adding criteria around focus appearance, target size, and dragging movements on top of 2.1. The contrast ratios themselves did not change between 2.1 and 2.2, so any older material quoting 4.5:1 and 3:1 is still correct on the numbers.[^4][^5] The newer 2.2 criterion worth knowing for products: **Target Size (Minimum) 2.5.8** asks for 24x24 CSS pixel targets or adequate spacing, which connects directly to Fitts's law below.

## Principle 4 — Affordances and signifiers: users should not need a tour

An affordance is a possible action (a button can be pressed). A signifier is the visible cue that communicates the affordance (the button *looks* pressable). Norman's distinction matters because AI-generated UIs routinely ship affordances without signifiers: a clickable card with no hover state, a text field that looks like a label, an icon-only button whose meaning you are expected to guess.[^2]

Four signifier rules for product surfaces:

1. **Clickable things look clickable.** Buttons have fill or border and change on hover. Links are distinguishable from body text by more than color alone (color-only distinction fails colorblind users). Cards that navigate get a hover elevation or border shift.
2. **Icon-only controls carry a label or a tooltip.** An icon without text is a guessing game. If space forces icon-only, provide an accessible name and a tooltip. The hamburger and the gear are learned; almost nothing else is.
3. **State is visible.** Disabled, loading, selected, and error states each need a distinct signifier. A button that is disabled but looks enabled is a rage-click generator.
4. **Empty states teach.** The first time a user hits a screen with no data, that screen should tell them what goes here and how to make something appear. A blank table is a dead end; a blank table with "No reports yet. Generate your first one." is onboarding.

## The three laws that turn opinions into layout decisions

Jon Yablonski's *Laws of UX* collects psychology and HCI findings into named heuristics designers can apply.[^1] Three of them convert vague layout debates into decisions you can defend and spec.

### Fitts's Law — target size and distance govern time-to-click

Paul Fitts showed in 1954 that the time to acquire a target is a function of its size and its distance from the pointer: bigger and closer is faster and less error-prone.[^1][^6] The product-builder implications are concrete:

- **Primary actions get large targets.** A 32px-tall button might match your Linear-dense aesthetic, but the primary submit on a mobile checkout wants 44 to 48px because thumbs are imprecise and errors cost conversions. WCAG 2.2's 24px target-size minimum is a floor, not a goal.[^4]
- **Put frequent actions near where the cursor already is,** or at screen edges and corners, which Fitts's law makes effectively infinite-size targets (you cannot overshoot a corner). This is why the macOS menu bar sits at the top edge.
- **Destructive actions get distance.** Put "Delete account" far from "Save," and never make them the same size and weight. Fitts's law working against you is a mis-click that deletes data.

### Hick's Law — every added choice costs decision time

Hick and Hyman showed in 1952 that decision time increases logarithmically with the number of choices.[^1][^7] For products this is the argument against the everything-on-one-screen dashboard:

- **Reduce choices at each step.** A five-option primary nav beats a fifteen-option one. Progressive disclosure (show advanced options behind a toggle) keeps the common path short.
- **Onboarding is where Hick's law bites hardest.** A new user facing twelve equally-weighted actions freezes. Pick the one action that delivers first value and make the rest recede or wait.
- **Beware the false economy of "flexible."** Every configuration option you expose is a decision you have handed the user. Sometimes that is right (power tools). For the first-run experience it is almost always wrong.

### Jakob's Law — users expect your product to work like the ones they already know

Jakob Nielsen's observation: users spend most of their time on *other* products, so they prefer yours to work the same way.[^1] This is the most commercially important law for a solo product builder, because it tells you where *not* to be creative:

- **Put things where users expect them.** Logo top-left links home. Account menu top-right. Primary nav across the top or down the left. Search where search goes. Novel placement is a tax you pay in confusion for no benefit.
- **Reserve your originality for your actual differentiator.** Be conventional on structure, distinctive on the thing that makes your product worth paying for. A weird settings layout does not make you memorable; it makes you annoying.
- **AI-native surfaces still obey Jakob's law.** Even a novel AI feature should sit inside a familiar shell. Tomorrow's lesson on AI-native UX patterns is largely about *new* conventions that are stabilizing precisely because users are learning to expect them.

## Taste as a learnable skill for engineers

The pervasive myth is that taste is innate, that you either have an eye or you do not. That myth is expensive because it makes engineers outsource every visual decision or, worse, ship whatever the code-gen tool defaulted to. Taste is a *learnable pattern-recognition skill*, and the mechanism for learning it is the same as any other: exposure plus feedback plus reps.

The concrete practice, which compounds:

1. **Build a reference library.** Screenshot ten products you find usable and beautiful. For each, name why using this week's vocabulary: the hierarchy move, the spacing rhythm, the contrast decision, the affordance treatment. Refactoring UI is the fastest on-ramp to the vocabulary.[^3]
2. **Audit before you generate.** When a code-gen tool hands you a screen, run the five-principle audit before you accept it. Naming what is wrong is the rep that builds the eye.
3. **Copy deliberately, then diverge.** Jakob's law gives you permission to start from convention. Reproduce a known-good pattern, then change one variable at a time and watch what breaks. This is how the eye calibrates.

Nielsen Norman Group's framing of the AI-era designer is the honest one for engineers who ship through agents: treat the AI as a "supercharged intern" that drafts variations and writes microcopy, while you supply the judgment, validation, and strategic alignment the model lacks.[^8] The judgment is exactly the taste this lesson builds. You do not need to draw. You need to *diagnose*.

## Controversy: is "AI-generated default good enough," or is taste a durable moat?

Two defensible positions, both held by serious people, and the answer changes what you invest in.

**Position A — the default is good enough, ship it.** Michael Seibel's instinct, generalized: your first product does not need beautiful UX, it needs to solve a real problem for a real user who will pay. Time spent perfecting hierarchy on a product nobody wants is the most seductive form of procrastination. The AI-generated shadcn default is clean, accessible-ish, and familiar (Jakob's law satisfied). Ship it, get users, let their behavior tell you which screen actually needs work. In this view, taste is a late-stage optimization, and premature polish is a founder failure mode.

**Position B — taste is one of the last durable moats.** When anyone can generate a working app in an afternoon, the generated baseline is a commodity and the differentiation lives in the last 20%: the interaction details, the empty states, the way errors are handled, the density tuned to your specific user. Brian Lovin and Rauno Freiberg argue versions of this. The generated default reads "generic AI product," and in a market full of generic AI products, the one that feels crafted wins trust and retention.

**The synthesis this lesson commits to:** both are right at different stages, and the discriminator is *the task friction axis, not the aesthetic axis*. Ship the default aesthetics (Position A) but never ship broken *usability*: flat hierarchy, sub-AA contrast, unlabeled controls, and dead empty states are not "polish," they are defects that cost you the users you paid to acquire. The five principles here are the non-negotiable floor even for an MVP. The taste moat of Position B is a real but later investment, earned once users prove the product is worth crafting for. Do not confuse the two. A stressed user on a 3.9:1 focus ring is not a taste problem you can defer; it is a usability defect that fails silently.

## Worked example — auditing an AI-generated dashboard

You prompt v0 for "a dashboard where a user sees their past AI-generated reports and generates a new one." It returns a clean shadcn layout. Before accepting, run the audit:

| Principle | What to check | Common AI failure | The fix (as a spec line) |
|---|---|---|---|
| Hierarchy | Is there one clear primary action? | Three equal-weight buttons | "One solid-fill primary (Generate report). Everything else ghost or link." |
| Typography/spacing | Consistent 8px rhythm? Body measure ≤75ch? | Mixed 12/16/20px gaps | "Snap all vertical gaps to the 4/8 scale. Body max-width 65ch." |
| Contrast | All text ≥4.5:1, borders/focus ≥3:1? | Muted placeholder at 3:1, invisible focus ring | "Raise placeholder to ≥4.5:1. Focus ring ≥3:1, visible on keyboard tab." |
| Affordances | Clickable things look clickable? Icons labeled? | Icon-only actions, no hover on cards | "Add hover state to nav cards. Label or tooltip every icon-only button." |
| Empty/error states | Does the empty table teach? | Blank table on first run | "Empty state: 'No reports yet' + primary CTA. Error state on failed generation." |

The output of this audit is not a vibe. It is a five-to-eight-line addendum you paste back into the tool. That is the whole skill: convert "something feels off" into named, measurable, spec-able fixes.

## Runnable experiment — the five-principle audit, with a pass bar

**Setup (10 min).** Take one product screen you generated in b2w03 or generate a fresh dashboard screen through v0, Lovable, or Claude Code. It must be a *product* screen with at least one form and one data region, not a marketing hero.

**Phase 1 — audit (30 min).** Run the five-principle table above. For each principle, record the current value with specifics (button heights in px, the two worst contrast ratios measured in WebAIM's checker, the count of unlabeled icons, whether the empty state exists). No vibes; numbers and counts only.

**Phase 2 — Fitts/Hick/Jakob pass (20 min).** Answer three questions in writing: (a) Fitts: is the primary action large enough and are destructive actions distanced? (b) Hick: how many choices does the first-run user face, and can you cut it to one primary path? (c) Jakob: name one place you deviated from convention and decide whether the deviation earns its confusion cost.

**Phase 3 — fix and re-measure (30 min).** Write the fixes as a spec addendum, apply it via the tool, and re-run the two contrast measurements and the choice-count.

**Pass bar:** Every text element ≥4.5:1 and every interactive border/focus ring ≥3:1 (measured, not eyeballed); exactly one primary action per view; every icon-only control has an accessible label; the empty state teaches. If any of those four fail, you have not passed, regardless of how good the screen looks. That is the aesthetic-usability effect being held at bay on purpose.

## Common mistakes experts see

1. **Confusing polish with usability.** Spending an hour on gradient tuning while the focus ring is invisible and the empty state is blank. The order is usability floor first, taste second.
2. **Contrast as a preference, not a constraint.** Accepting the tool's muted grays because they "look clean" without measuring them. `slate-400` on `slate-50` is roughly 3:1 and fails AA for text.[^5]
3. **Flat hierarchy from equal-weight everything.** Making the important thing big instead of making everything else recede, so nothing wins.
4. **Icon-only controls with no label.** Shipping a toolbar of ambiguous glyphs and calling it minimal. It is minimal for you and a guessing game for the user.
5. **Over-configuring the first run.** Exposing twelve options to a user who has not yet gotten any value, triggering Hick's-law freeze.
6. **Novelty on structure.** Being creative with nav placement or button conventions, paying Jakob's-law confusion tax for zero differentiation.
7. **Dead empty and error states.** The most common AI-generated omission: the happy path is built, the empty and failure paths are not, and those are exactly where new users and stressed users live.

## Reflection questions

1. Take a product you use daily. Where does the aesthetic-usability effect make you forgive a usability problem you would otherwise report? What is the actual defect underneath the goodwill?
2. Your product has a destructive action and a primary action. Using Fitts's law, specify their relative size and distance, and justify the numbers.
3. Where in your first-run experience does Hick's law bite hardest? Which single action delivers first value, and what would you hide to expose only it?
4. Name one place your product *should* break Jakob's law because the deviation is your actual differentiator. Now name three places you were tempted to be creative but should not be.
5. WCAG 2.2 AA is a floor. Which one surface of your product deserves AAA (7:1) and why? Which surface can you not ship below AA under any circumstances?
6. If taste is learnable, what is your concrete rep this week? Name the ten-screen reference library you will build and the vocabulary you will annotate each with.

## My take (reviewer lens)

**Michael Seibel** would push hardest on the whole framing. His pushback: "You are teaching contrast ratios to people who do not have a product anyone wants yet. Ship the ugly thing, get ten users, and let them tell you what is broken. Every hour on hierarchy is an hour not spent talking to a customer." The steelman is real and this lesson concedes it explicitly in the controversy section: the taste moat is late-stage. But Seibel's own bar is "solve a real problem," and a product where keyboard users cannot see focus or colorblind users cannot find the button is not solving the problem for those users. The line I hold: usability floor is not polish, it is correctness. Aesthetics can wait; a 3:1 focus ring cannot, because it is a silent defect.

**Andrej Karpathy** would push back on the "taste is learnable like any skill" claim as slightly too clean. His likely counter: pattern recognition for visual design is learnable, yes, but the feedback signal is much noisier and slower than for code, where the test either passes or fails. You can grind reps on hierarchy for a month and still not know if you improved, because the aesthetic-usability effect and small sample sizes corrupt the signal. Fair. The mitigation in the lesson is to anchor on the *measurable* subset (contrast, target size, choice count, hierarchy-of-one) precisely because those give a clean pass/fail, and to treat the un-measurable taste layer as the slower, noisier skill it is.

**A named design voice, Rauno Freiberg,** would push back from the opposite side: that reducing UX to five principles and three laws under-serves the interaction-detail layer where real product feel lives, the motion curves and micro-interactions that a WCAG checklist never captures. He is right that this lesson is deliberately the floor, not the ceiling. Tomorrow's AI-native UX patterns and the b2w03 motion material carry the ceiling. Today's job is to make sure the floor is not on fire.

## Further reading

**Must-read (this week):**
1. **Refactoring UI** — Wathan and Schoger. The fastest path to the hierarchy, spacing, and contrast vocabulary. refactoringui.com.[^3]
2. **Laws of UX** — Jon Yablonski. lawsofux.com and the 2020 book. Fitts, Hick, Jakob, aesthetic-usability, and 17 more, each with a design implication.[^1]
3. **WCAG 2.2 Quick Reference** — w3.org/WAI/WCAG22/quickref. Filter to Level AA and read 1.4.3, 1.4.11, 2.5.8.[^4]

**Recommended:**
4. **The Design of Everyday Things** — Don Norman. Affordances, signifiers, discoverability, the vocabulary underneath everything here.[^2]
5. **WebAIM Contrast Checker** — webaim.org/resources/contrastchecker. Bookmark it; use it on every screen.[^5]
6. **NN/g, "A Research Agenda for Generative AI in UX"** — the honest map of what is and is not settled in AI-era design.[^8]

**Optional:**
7. **Deque axe rules — color contrast** — dequeuniversity.com/rules/axe. The developer-facing version of the contrast rules.[^9]

## Citations

[^1]: Jon Yablonski, *Laws of UX: Using Psychology to Design Better Products & Services* (O'Reilly, 2020) and the companion site lawsofux.com. Source for the aesthetic-usability effect, Fitts's Law, Hick's Law, and Jakob's Law as named, applicable design heuristics, and for the "21 laws across heuristics, Gestalt, cognitive bias, and principles" structure. (search-verified 2026-07-17 via ResearchGate/Blinkist/Looppanel summaries; fetch egress-blocked — liveness pass pending.)

[^2]: Don Norman, *The Design of Everyday Things*, revised edition (Basic Books, 2013). Source for affordances vs signifiers, discoverability, and understandability as the two properties of good design. Foundational HCI text.

[^3]: Adam Wathan and Steve Schoger, *Refactoring UI* (refactoringui.com). Source for hierarchy via weight/size/color contrast, the de-emphasize-supporting-text move, the 8-point spacing grid, and density as an audience decision. Also cited in b2w03 design-system literacy.

[^4]: W3C, *Web Content Accessibility Guidelines (WCAG) 2.2* W3C Recommendation, and the WCAG 2.2 Quick Reference. w3.org/TR/WCAG22. Source for AA contrast (SC 1.4.3 text 4.5:1, large 3:1; SC 1.4.11 non-text 3:1), Target Size Minimum SC 2.5.8 (24px), and WCAG 2.2 as the current standard with contrast ratios unchanged from 2.1. (search-verified 2026-07-17 across web-accessibility-checker.com, makethingsaccessible.com, WebAIM; fetch egress-blocked — liveness pass pending.)

[^5]: WebAIM, "Contrast and Color Accessibility" and the WebAIM Contrast Checker. webaim.org/articles/contrast and webaim.org/resources/contrastchecker. Source for the practical 4.5:1 / 3:1 thresholds, large-text definition (18pt/24px or 14pt bold/19px), and the canonical checking tool. (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending.)

[^6]: Paul M. Fitts, "The information capacity of the human motor system in controlling the amplitude of movement," *Journal of Experimental Psychology*, 47(6), 1954. The original derivation of the speed-accuracy tradeoff in target acquisition. Summarized in Laws of UX.[^1]

[^7]: William E. Hick (1952) and Ray Hyman (1953), the Hick-Hyman law on choice reaction time increasing logarithmically with number of alternatives. Summarized in Laws of UX.[^1]

[^8]: Nielsen Norman Group, "A Research Agenda for Generative AI in UX" and related 2025 articles (nngroup.com/articles/genai-ux-research-agenda). Source for the "AI as supercharged intern," outcome-oriented design, the 425-interaction conversation-type study, and the designer-judgment-still-required framing. (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending.)

[^9]: Deque University, axe color-contrast rule (dequeuniversity.com/rules/axe/color-contrast). Developer-facing statement of the minimum contrast thresholds enforced by the axe accessibility engine. (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending.)

_last_verified: 2026-07-17_
