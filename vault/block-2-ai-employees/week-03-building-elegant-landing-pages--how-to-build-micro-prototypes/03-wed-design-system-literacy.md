---
type: lesson
block: block-2-ai-employees
week: week-03
day_of_cycle: 3
day_name: wed
session_slug: building-elegant-landing-pages
date_due: 2026-06-03
tags: [design-system-literacy, typography, color-system, spacing-scale, motion-design, shadcn-ui, geist, linear-aesthetic, ai-codegen-briefing, oklch, refactoring-ui, rauno-freiberg]
sources:
  - refactoring-ui-wathan-schoger-book-site
  - shadcn-tailwind-v4-changelog-feb-2025
  - shadcn-enterprise-designsystemscollective-2025
  - shadcn-maintainership-issue-6417-2024
  - vercel-geist-introduction-2024
  - vercel-geist-rauch-x-announce-2024
  - basement-studio-birth-of-geist-2024
  - rauno-devouring-details-2024
  - every-invisible-details-rauno-2023
  - linear-method-introduction-2024
  - linear-redesign-now-2024
  - figma-linear-method-opinionated-2024
  - tailwind-css-v4-release-2025
  - evilmartians-oklch-why-quit-rgb-hsl-2024
  - wcag-22-w3c-recommendation-2024
  - w3c-wai-c39-prefers-reduced-motion-2024
  - web-dev-learn-accessibility-motion-2024
  - chrome-devtools-non-composited-animations-2024
  - stripe-elements-appearance-api-docs-2024
  - raycast-developers-ui-2024
  - lexington-themes-andreuzza-tailwind-2025
last_verified: 2026-04-17
word_count_target: 6000
---

# Design-system literacy for operators who don't draw — the seven variables that separate a Vercel template from a Linear page

## Why this matters

You ship conversion surfaces through Claude Code, v0, Lovable, Bolt. Yesterday you learned how those tools translate a prompt into a page; Monday you learned what makes a page convert. Today closes a gap that silently kills both: you cannot brief an AI code-gen tool toward a specific aesthetic without the vocabulary. You type "make it clean and modern," the tool gives you a Vercel template because Vercel templates are what the model has seen most, and you iterate in the dark — "more minimal," "more premium," "more like Linear" — while the model guesses. You lose hours. The page ends up looking like every other AI-generated SaaS page in 2026.

Goal today: design-system **literacy**, not design. Enough vocabulary and variable-level control that you can (a) name the seven decisions that made any page look the way it does, (b) write a Claude Code brief that hits your intended aesthetic on the first or second pass, (c) identify exactly which variable is wrong when an AI-generated page looks off. A senior marketing director briefing a contractor can do this. A senior finance lead specifying a dashboard can do this. A 20-year creative director who ships via Claude Code absolutely can — provided the variables are named.

By the end you will be able to (1) audit any page on the seven load-bearing variables — typography, color, spacing, density, motion, imagery, voice — and state the specific value each uses, (2) translate a target aesthetic (Linear, Rauno, Raycast, Geist, Stripe) into a brief a code-gen model can execute without eight rounds of "no, less of that," (3) take a position on the shadcn-wholesale-adoption and motion-as-medium debates with cited evidence, (4) produce a reusable Claude Code prompt template for taste briefing, (5) override the Vercel-default look when an AI tool has dropped you in it.

## Prerequisites

- You have shipped at least one page through v0, Lovable, Bolt, or Claude Code in the last two weeks. If you haven't, Tuesday's lesson is the precondition — come back after that experiment.
- You can read a CSS variable declaration, a Tailwind utility class, and a simple JSON token file at the "what is this controlling" level. You do not need to write any of them.

## Layer 1 — The seven variables, and why most AI pages look the same

The default 2026 AI code-gen output for a "modern SaaS landing page" is predictable. Inter or Geist Sans, a slate-900-to-zinc-50 neutral ramp, one accent at hue 240–260 (indigo or violet), rounded-xl cards, shadow-sm elevation, lucide icons, 24-32px section padding, prefers-reduced-motion fade-ins, a stock hero illustration or gradient mesh, copy that says "Build better products, faster." Every YC W25 batch has eighty of these.

That page is not bad. It is *generic* — a weighted average of the ten thousand pages that trained the model. To push a generated page toward a specific aesthetic — Linear's opinionated sharpness, Rauno's motion-rich restraint, Raycast's chromatic density, Stripe's quiet consistency — name the knobs the generator is turning. Those knobs are the same seven variables every design system, explicit or implicit, encodes. Refactoring UI names five of them explicitly (hierarchy, layout and spacing, typography, color, imagery) and two more implicitly under personality and detail; we treat all seven as first-class because each produces an override prompt you can paste.[^1]

### Variable 1 — Typography

The most load-bearing variable and the one AI tools get wrong most often. Decide three things before you brief the model: **number of families** (one, or one sans plus one monospace), **scale ratio** (1.125, 1.25, 1.333, or custom), and **line-height policy** (tight for headlines, loose for body, specific numeric targets).

A one-family page with careful weight contrast (700 for H1, 400 for body, 500 for UI labels) reads more confident than a two-family page with mismatched x-heights. Linear, Vercel Geist, Raycast, and Stripe's dashboard all use one family as the dominant surface.[^2][^3][^4] Geist Sans was commissioned by Vercel from basement.studio in 2024 specifically because Inter — the default for most AI-generated pages — had, in Vercel's view, been normalized into a "generic SaaS" signal; Geist was designed to echo Univers, SF Pro, and ABC Diatype with a more mechanical rhythm that would register as distinct to the attentive viewer.[^5] The move is instructive: the choice of typeface is the single fastest way to escape the default-AI-page look, and it requires zero code-gen skill — you just name a font.

Scale ratio matters more than scale range. A 1.125 (major second) scale produces a dense, editorial page where H1 through body differ by small increments; Linear and Stripe use ratios in this range.[^6] A 1.333 (perfect fourth) scale produces a marketing-landing-page feel with a giant H1 and a chasm between headline and body — you see it on Vercel marketing, on YC company pages, on most v0 defaults. Neither is wrong, but they signal different product categories. If you ask an AI code-gen tool for "a Linear-inspired page" without specifying scale ratio, you will often get a 1.25 or 1.333 scale with Linear's font choices, and it will look nothing like Linear.

Line height is the variable that separates a shipped-looking page from a "something is off" page. The Refactoring UI rule is tight for large type (1.0–1.2 for H1, because long line-heights on large text create awkward vertical gaps), looser for body (1.5–1.7, with 1.6 a common sweet spot for 16px body at 65–75 character measure).[^1][^7] AI-generated pages routinely ship H1 with line-height 1.5 and body with line-height 1.2 — both inverted. If your generated page "feels wrong" and you cannot articulate why, inspect the line-heights first.

**Paste-ready override prompt (typography):**

> *"Typography: use one family only — [Geist Sans | Inter | JetBrains Mono for display | custom]. Scale ratio 1.125 (editorial density) with explicit px values H1 48, H2 32, H3 24, body 16, caption 14. Line-height: H1 1.1, H2 1.2, H3 1.3, body 1.6. Weights: H1 600, body 400, UI labels 500. Kill any second display family. Enforce measure of 65–75 characters on body paragraphs (max-width ~65ch)."*

Notice what this prompt does: it eliminates guesswork on all three axes the model otherwise picks randomly. You can swap in any named target and the brief holds.

### Variable 2 — Color

More decisions than non-designers expect. You need a **neutral ramp** (10–12 steps from near-white to near-black, usually a tinted gray — slate, zinc, stone, warm/cool), a **primary accent** (one hue, 3–5 shades), optionally a **secondary**, and **semantic colors** (success green, destructive red, warning amber).

The most important design-system advance of 2024–2025 was the migration from HSL to OKLCH. Evil Martians' 2024 "OKLCH in CSS: why we moved from RGB and HSL" is the canonical argument: HSL lightness is not perceptually uniform — HSL yellow at 50% reads as a different brightness than HSL blue at 50% — so the "300 step" of one hue looks darker than the "300 step" of another, undermining the whole ramp.[^8] OKLCH (Oklab lightness-chroma-hue) is perceptually uniform: lightness 50% reads the same brightness across hues.[^8][^9] Tailwind v4 ships OKLCH as default in 2025, shadcn/ui converted in February 2025, most serious 2024–2025 systems now use OKLCH tokens.[^10][^11][^12]

Why this matters for operators: a hex code (#6366f1) is a point with no relationships. An OKLCH ramp ("primary oklch(0.58 0.18 264), stops at L 0.95 / 0.85 / 0.70 / 0.58 / 0.45 / 0.30") is a system — your button, hover, focus ring are derivable by the model without guessing.

Narrower choice: hue count. Linear = one hue plus neutral ramp. Raycast 2024 was one red plus neutral plus subtle gradients; by 2025 they doubled down on red and dropped the gradients associated with the "linear design" trend.[^13] Stripe's dashboard is near-monochromatic with one narrow accent. Notion is multi-hue by policy — workspace emojis create chromatic noise a single-accent system would fight. Your aesthetic determines the hue count; specify it.

**Paste-ready override prompt (color):**

> *"Color system in OKLCH. Neutral ramp (12 steps) based on hue 240, chroma 0.01 (cool gray): L 0.98, 0.96, 0.92, 0.85, 0.72, 0.55, 0.42, 0.32, 0.22, 0.15, 0.10, 0.04. Single accent: oklch(0.58 0.18 264) with shades at L 0.95 / 0.85 / 0.70 / 0.58 / 0.45 / 0.30 / 0.20. No secondary accent. Semantic: success oklch(0.65 0.16 145), destructive oklch(0.62 0.21 25). No gradients except one subtle radial in hero. Background: L 0.98 day / L 0.12 night. Export as CSS custom properties in :root and .dark."*

### Variable 3 — Spacing

The 4/8 pixel grid is ubiquitous in 2024–2026 design systems. **All spacing should be multiples of 4 (preferably 8); vertical rhythm should be consistent across section → subsection → element.**[^14][^15] Refactoring UI's spacing chapter is explicit: inconsistent spacing makes a page look amateur even when typography and color are correct.[^1]

Scale: 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96, 128. Tailwind's default spacing scale is exactly this.[^14] The AI-page trap is not absence of scale — tools default to Tailwind — but **inconsistent scale selection**: the model picks 16px between hero and proof, 22px between proof and pricing, from two different training samples. When a page "feels off," measure vertical distances between sections and count distinct values. Linear: 2–3. Generated page: 6–8.

Second rule: **internal-less-than-external** — whitespace between related elements is smaller than between unrelated.[^1] Form label sits 4–8px above its input; input sits 24–32px above the next row; whole form sits 64px from the next section. Trivially stated, routinely violated by AI output.

**Paste-ready override prompt (spacing):**

> *"Spacing scale: multiples of 4 only, from the set {4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96, 128}. Vertical rhythm: section-to-section 96px, subsection-to-subsection 48px, card-to-card 24px, label-to-input 8px. Internal spacing inside any component less than external spacing around it. Enforce: if any vertical gap in the generated page is not in the scale, round to the nearest member. Also: consistent horizontal padding across all sections (max-w-6xl mx-auto px-6 on desktop, px-4 mobile)."*

### Variable 4 — Component density

How much information you pack into a fixed viewport. Linear, Raycast, Geist, and Stripe's dashboard are **dense**: UI labels 13–14px, button heights 32–36px, table rows 40px, minimal breathing room. Notion, Intercom, and most consumer SaaS landing pages are **loose**: labels 15–16px, buttons 44–48px, more vertical space. Neither is inherently better — but **mismatch** is lethal. Marketing-loose density around a Linear-style dense nav reads confused.

**Corner radius.** Geist and Linear use small (4–6px); Notion and Stripe marketing use medium (8–12px); consumer apps lean large (16–24px). Small reads professional, large reads friendly. AI defaults to `rounded-xl` (12px) — inoffensive consumer SaaS. If you want Linear, override.

**Border vs shadow.** Stripe and Linear use 1px borders at oklch(0 0 0 / 0.08) — architectural. Consumer pages use shadows — elevation over structure. Pick one; mixing produces the "cluttered" look.

**Paste-ready override prompt (density):**

> *"Density: Linear/Geist tier — UI label size 13px, button height 32px, input height 36px, table row height 40px, nav height 48px. Corner radius: 6px for buttons and inputs, 8px for cards, no pill shapes. Elevation via 1px borders at oklch(0 0 0 / 0.08) rather than shadows — shadows only on floating overlays (dropdowns, tooltips). No rounded-xl or rounded-2xl anywhere."*

### Variable 5 — Motion

The most contested variable. Two positions bracket the 2026 debate.

Position A — **motion as medium**. Rauno Freiberg's Devouring Details (launched 2024, updated 2025) argues motion is a first-class interface language: a button pressed-in on mousedown with 120ms transition communicates physicality, a list reordering with FLIP animation communicates causality, a drawer rubber-banding communicates constraint.[^16][^17] Every Inc's "Invisible Details of Interaction Design" argues the post-2020 web-app class (Linear, Notion, Raycast, Arc, Vercel dashboard) differentiates on motion craft the way earlier generations differentiated on typography. Motion is signal, not decoration.

Position B — **motion as tax**. Chrome DevRel performance voices and the WCAG 2.2 accessibility community: motion is cost — runtime (non-composited animations stall main-thread paint, hurting Core Web Vitals), cognitive (~35% of adults over 40 experience vestibular dysfunction triggered by motion), accessibility (users who set `prefers-reduced-motion: reduce` expect no parallax, no auto-play scroll animation).[^18][^19][^20] Chrome's guidance is explicit: animate only `transform` and `opacity` on the compositor; other properties are janky on low-end.[^21] WCAG 2.2 C39 requires non-essential motion to be wrapped in `@media (prefers-reduced-motion: no-preference)` with pause/stop on long-running animations.[^19]

Both are correct. Reconciliation: motion is worth its cost only when it **communicates state or causality**. A 100ms button press-in signals "I received your click." A pan-and-zoom gradient mesh signals "I need to look busy." Freiberg's examples are all category 1; motion-as-tax critiques target category 2. Operational rule: animate for *state change* (hover, press, focus, loading, success, error, reorder, enter, exit), not *ambience*. Strip ambient motion by default; add back only if you can articulate what state it communicates.

**Paste-ready override prompt (motion):**

> *"Motion policy: animate transform and opacity only. Durations: 120ms for micro-interactions (button press, input focus), 200ms for medium (modal enter, drawer slide), 300ms for macro (page transition). Easing: cubic-bezier(0.16, 1, 0.3, 1) for entrances, cubic-bezier(0.7, 0, 0.84, 0) for exits. All motion wrapped in @media (prefers-reduced-motion: no-preference). Kill any parallax, background-video, or ambient looping animation. Signal state change only — hover, focus, press, loading, error, reorder. Show me the final motion-rule CSS and the reduced-motion fallback."*

### Variable 6 — Imagery

Four options: custom photography, custom illustration, stock/generative, or no imagery. Each codes differently. Stripe uses custom photography for hero, custom illustration for docs; Linear uses no hero imagery and product screenshots below the fold; Raycast uses tight product shots with brand gradients.[^13] Geist ships no above-fold imagery on its Next.js marketing — typography and layout carry it.[^3]

The 2026 AI-generated default is **generative imagery** — Midjourney hero illustration with a dreamy gradient, sometimes isometric workspace — and it reads instantly dated. For serious operator audiences (finance, legal, enterprise SaaS), zero above-fold imagery plus strong typography outperforms almost any generative illustration. For consumer audiences (recruiting, wellness, education), custom illustration is worth commissioning. Stock photography is only acceptable as a temporary crutch.

**Paste-ready override prompt (imagery):**

> *"Imagery policy: zero imagery above the fold. Hero is typography and layout only. Below the fold use real product screenshots (not mockup frames — the actual UI in Chrome or similar). No stock photography, no AI-generated illustration, no dreamy gradients, no isometric workspace scenes. If a section requires imagery and no screenshot exists, use a placeholder block labeled 'TK: photo of [specific thing]' at the correct aspect ratio."*

### Variable 7 — Voice

Copy as design surface. Monday covered Shapiro's hook-promise-proof-action, but voice is also sentence structure, diction, punctuation, capitalization. Linear: "The system for product development." Stripe: "Half a billion products, infinite possibilities." Geist: "The React Framework for the Web." Raycast: "Your shortcut to everything."

**Title case vs sentence case.** Title case reads formal and 2015; sentence case reads modern and 2024. Linear, Stripe, Geist, Raycast all use sentence case; Salesforce, HubSpot remain title case. AI tools default to title case because 2015 training pages dominated. Override.

**Paste-ready override prompt (voice):**

> *"Voice: declarative, short sentences, sentence case (not title case) on all headings. First-person plural ('we') only when talking about the company; second-person ('you') when talking about the reader; no first-person singular anywhere. No marketing verbs like 'unlock,' 'unleash,' 'empower,' 'revolutionize,' 'transform.' No adjective stacks — at most one qualifier per noun. Punctuation: periods on headlines, no em-dashes in body copy, no exclamation points anywhere."*

## Layer 2 — Reading a target aesthetic as variables

You now have seven variables. The next skill is translating a target aesthetic ("make it look like Linear") into explicit values across all seven. This is the move that separates operators who get what they want from the model on the first pass from operators who iterate twelve times.

Take Linear. Reading its 2024 redesign post "How we redesigned the Linear UI" and Figma's 2024 writeup "The Linear Method: Opinionated Software," the design is:[^22][^23][^24]

| Variable | Linear value |
|---|---|
| Typography | Inter (sans), monospace fallback for code. Scale ~1.2. Line-height 1.1 on display, 1.5 on body. Weight contrast via 600/500/400. |
| Color | One primary hue (violet ~264) with narrow ramp; extensive neutral ramp from near-white to near-black; OKLCH-based. Dark mode as first-class, light mode secondary. |
| Spacing | 4/8 grid, Tailwind-spec. Tight. |
| Density | Dense. UI labels 13px, buttons 32px tall, thin 1px borders at low opacity instead of shadow. Corner radius 6–8px. |
| Motion | Rich but state-change-only. 120–200ms durations. Heavy use of Framer Motion / React Spring for list reorder and transitions. Press-in on buttons. |
| Imagery | Zero above-the-fold imagery; product screenshots below the fold; no illustration. |
| Voice | Short, declarative, sentence case. Periods on headlines. First-person plural for company. |

Take Raycast:[^13]

| Variable | Raycast value |
|---|---|
| Typography | Inter, one family. Large display scale. Sentence case. |
| Color | Dark-first canvas; one dominant red (2025) plus gradient accents; cooler neutrals. |
| Spacing | Tight on command palette surfaces, looser on marketing. |
| Density | Ultra-dense in product surfaces (command-palette rows); looser on landing. |
| Motion | Noisy overlay animations on landing as of 2025; product is state-change minimal. |
| Imagery | Product screenshots in tight crops with brand gradient accents. |
| Voice | Bold, conversational. |

Take Geist / Vercel:[^3][^5]

| Variable | Geist value |
|---|---|
| Typography | Geist Sans custom typeface, Geist Mono for code. One family rule. |
| Color | Black and white first, single accent narrow hue. OKLCH. |
| Spacing | Large scale for marketing surfaces, tight on dashboard. |
| Density | Marketing is loose (large display H1), dashboard is dense. |
| Motion | Minimal on marketing; state-change on dashboard. |
| Imagery | No above-the-fold imagery on most marketing pages; typography carries. |
| Voice | Mechanical, short, minimal, sentence case. |

When you ask Claude Code "build me a landing page in Linear's aesthetic," you are asking it to hit the middle column above across all seven rows simultaneously. Most code-gen tools will hit 2–3 of them and miss the rest; iterating without the table is chasing shadows. Iterating with the table, each override is surgical — you look at the generated page, see that the spacing scale is right but the density is wrong (buttons 44px instead of 32px) and fire the density override prompt from Layer 1.

**The master brief pattern** — a Claude Code brief that hits all seven variables simultaneously for any named target aesthetic:

```
Build a landing page in the [Linear | Raycast | Geist | Stripe | custom] aesthetic.

Target profile (fill in all seven):
1. Typography: [family, scale ratio, line-heights, weights]
2. Color: [neutral ramp definition, accent hue OKLCH, semantic colors, dark/light policy]
3. Spacing: [scale set, rhythm rules]
4. Density: [labels, buttons, radius, borders-vs-shadow policy]
5. Motion: [state-change rules, durations, reduced-motion policy]
6. Imagery: [above-fold policy, below-fold policy, generative ban]
7. Voice: [sentence/title case, verb list, banned vocabulary]

Before generating: echo back the profile in your own words and ask me to confirm one decision you would default differently. Then generate. After generating: list which of the seven variables you hit exactly vs approximately, and flag any you made up.
```

The "echo back" step is the detail that makes this brief land. Claude Code that has echoed back the profile cannot default to Vercel-template values without flagging the decision. You catch the drift before it ships.

## Layer 3 — Wholesale-adoption vs plunder: the shadcn controversy

Shadcn/ui is the dominant UI layer in 2026 code-gen. v0 defaults to it, Lovable and Bolt ship it in starters, Claude Code boilerplate assumes it. The operator question is not whether but how deeply — wholesale adoption as your design system, or selective plunder of specific components into a custom shell.

**For wholesale adoption (shadcn-maximalist):**

1. Copy-in-codebase. Unlike MUI or Ant Design, shadcn/ui is not an npm dependency — a CLI drops React source into your codebase; you own it.[^25] No version cliff, no locked styles, no vendor breaking your build.
2. Accelerating surface area, now moving faster than most teams can track. February 2025 brought the Tailwind v4 migration (OKLCH, `data-slot` selectors, forwardRef removal);[^10] October 2025 shipped charts and form primitives; then the platform cycle accelerated: **`npx shadcn create` (December 12, 2025)** introduced five named visual styles — **Vega (classic), Nova (compact), Maia (soft/rounded), Lyra (boxy/sharp), Mira (dense)** — that *rewrite component code*, not just theme colors, and let you pick Radix or Base UI as the primitive base; **shadcn/cli v4 (March 2026)** added **presets** (your whole design-system config packed into a short code you build on shadcn/create, preview live, and `init --preset` into any project) and a registry-directory build for distribution.[^25b][^26b] This is a materially different tool than the one this lesson originally described.
3. AI code-gen alignment. Every major code-gen tool is trained on shadcn components; briefing "build with shadcn/ui" gets higher-fidelity output than briefing a custom system the model has never seen. Alone, this is worth adoption for a solo operator.

**Against wholesale adoption (shadcn-skeptic):**

1. Maintainership concentration. The recurring single-maintainer bottleneck is real: Issue #6417 ("MORE MAINTAINERS," opened January 2025, citing 835+ open PRs) remains the canonical complaint.[^27] Radix UI — long the primary shadcn primitive — was built by Modulz, **acquired by WorkOS in June 2022**, after which many original maintainers left and contributions slowed; several went on to start Base UI at MUI, and **shadcn has since moved its default primitive toward Base UI**, which both mitigates and re-opens the upstream-risk question.[^28] Bus factor scales with product longevity.
2. Enterprise-scale drift. Design Systems Collective's 2025 "Shadcn Isn't Ready for Enterprise Design Systems": copy-in-codebase means local edits diverge from upstream; merging accessibility or security patches becomes manual AST-diffing.[^27] Negligible for solo; job-scale for a 20-person team.
3. Aesthetic homogeneity — the weakest of the three critiques in 2026. It used to be that every shadcn page looked like every other until you overrode color and typography. The **visual styles and presets now ship precisely to break that homogeneity**: Nova, Lyra, and Mira produce visibly different pages out of the box, and a preset *is* the shareable encoding of exactly the seven-variable taste brief this lesson teaches you to build by hand. The "Vercel template" default is still shadcn's Vega style — but it is now one of five, not the only one.

**Operator synthesis:** for a solo 2026 AI-services engagement, wholesale shadcn adoption is correct — accelerating surface area and AI-tool alignment pay for maintainership risk, and homogeneity is soluble with a preset or a 200-word override prompt. **The new operator move: encode your seven-variable taste brief as a shadcn preset, then hand that preset to your coding agents** — it is the same artifact, made portable. For a multi-product team maintaining long-lived systems, plunder still wins: take Base UI / Radix primitives, form patterns, chart components; wrap them in your own tokens and typography; own the baseline.

Michael Andreuzza's Lexington Themes (2025, Astro + Tailwind v4 themes for freelancers) is the shadcn-adjacent alternative — same copy-in-codebase philosophy applied to full marketing compositions, not component primitives.[^29] Andreuzza deliberately does not use shadcn/ui — he layers on bare Tailwind with opinionated compositions. That's a plunder move at one level up.

## Operator war stories

**Story 1 — shadcn Tailwind v4 migration (February–March 2025).** Teams that migrated shadcn components to Tailwind v4 report the documented sequence — run the CLI, update `tsconfig.json`, replace HSL variables with OKLCH, remove forwardRef wrappers — took ~2–4 hours for a ≤30-component library per the February 25, 2025 changelog and community reports.[^10] What took another ~2 weeks (roughly 30–40 engineer-hours across designers and reviewers) was retuning color ramps: a violet accent authored as `hsl(243 75% 59%)` and hover `hsl(243 75% 54%)` reads the 5-point HSL-lightness delta as a crisp state change, but the same two colors converted to `oklch(0.58 0.18 264)` base and `oklch(0.53 0.18 264)` hover read as muddy — OKLCH lightness 0.53 is perceptually darker than HSL 54% because OKLCH is perceptually uniform and HSL is not. Corrected hover: `oklch(0.50 0.18 264)` — an additional −0.03 L drop — to recover the same perceived button-press. Operator lesson: when you migrate color spaces, budget ~1 engineer-hour per accent × state (base, hover, active, focus, disabled); retune hover values, don't just convert base values.

**Story 2 — Rauno Freiberg's Devouring Details launch (2024, scaled 2025).** Rauno shipped Devouring Details — an interactive interaction-design course — with a cohort-window model (open ~2 weeks, closed months between cohorts) and by late 2025 had grown the catalog to 23 chapters with interactive demos at devouringdetails.com.[^16][^17] The launch page used zero above-fold imagery, custom typography (a single display family, ~1.15 scale ratio), and motion examples as interactive React components (not video or GIF) — the hover-press demo, the FLIP list-reorder demo, the rubber-band drawer demo are all live inline, each weighing <8KB gzipped. Rauno has not publicly disclosed revenue or completion metrics, but the cohort-gating signal is load-bearing for the operator takeaway: for a product where the *aesthetic* is the product, the landing page has to hit all seven variables at the tier the product claims — if the landing has JPEG illustrations and a dead parallax, the course cannot credibly sell motion craft. Honest note: no public conversion or CSAT number available; the operator evidence is the product's growth from ~10 chapters at 2024 launch to 23 chapters sustained through 2025.

**Story 3 — Linear's 2024 UI redesign.** Linear published "How we redesigned the Linear UI (part II)" in 2024 at linear.app/now, detailing a multi-month rework that touched typography scale, spacing grid, icon system (a bespoke 500+ icon set replacing a mix of Lucide + custom), and motion rules simultaneously.[^22] Linear disclosed shipping sequence and design rationale but — as of the 2026-04-17 verification pass — has not published quantified post-redesign metrics (activation, retention, time-on-page, or conversion). The publicly visible signal is business, not page-level: Linear raised a widely-reported Series C in 2024 at a unicorn-tier valuation (see TechCrunch and Crunchbase coverage for specifics) and the company publicly cites tens of thousands of paying teams, which is the kind of scale that either forces a design-system rework or gets forced by one — but the causal arrow on conversion specifically is not something Linear has disclosed. The team did not adopt a generalist framework — they wrote their own rules because Material / HIG / Bootstrap optimize for breadth and Linear wanted a dense, opinionated, narrow-audience system. Operator lesson: for a narrow high-taste audience (developers, designers, creatives), a bespoke token set costs ~40 engineer-hours of initial scaffolding (plus weeks of refinement) and saves you from generic. For a broad low-taste audience (SMB owners, enterprise middle-management), a well-configured shadcn with overrides wins. Honest calibration: the lack of disclosed page-level numbers means you should not quote Linear as a *conversion* win — quote it as a *taste-bar* win and an audience-fit win.

## Runnable experiment

Four-phase Claude Code experiment exercising all seven variables end-to-end. Block 3–4 hours.

**Phase 1 — Seven-variable audit.** Take any v0/Lovable/Bolt-generated hero from Tuesday (or generate fresh). In Claude Code:

> *"Audit the current landing page against the seven variables. For each, report: (1) current value with specific numbers (font size, line-height, spacing, color OKLCH, motion durations), (2) default aesthetic it signals (generic-SaaS, Vercel-template, Linear, Raycast, consumer-app, enterprise), (3) specific override to move it toward [Linear / Rauno / Geist]. Output as 7-row markdown table: Variable | Current | Signals | Override."*

Expected partial output:

| Variable | Current | Signals | Override |
|---|---|---|---|
| Typography | Inter, scale 1.25, H1 line-height 1.5, weight 700 | Generic-SaaS | Inter, scale 1.2, H1 line-height 1.1, weight 600 |
| Color | HSL neutral + indigo-500 accent | Vercel-template | OKLCH ramp, hue 264 violet, narrow |
| Spacing | Mix 16/20/24/28px between sections | Inconsistent | 4/8 scale, 96px section-to-section |

**Phase 2 — Apply overrides.**

> *"Apply the Override column to the page. Rewrite tailwind.config and component source. Preserve copy and layout; change only the seven variables. Show me the diff of tailwind.config and the three most-changed files."*

Expect OKLCH variables replacing HSL in `:root`, scale adjustments in heading utility classes, spacing pruned to 4/8.

**Phase 3 — Adversarial critic.**

> *"Roleplay three design critics: (a) Rauno Freiberg — do the motion rules signal state change or decoration? (b) Adam Wathan — is the color ramp OKLCH-coherent or is there a lightness inconsistency across hues? (c) Brian Lovin — does the density match Linear's or is there visual bloat? 5-line review each with one specific fix. Be brutal."*

Critic A typically flags motion-as-decoration; Critic B finds a hue that breaks ramp coherence; Critic C flags a density mismatch between nav and content.

**Phase 4 — One failed override.** Pick any single variable from Phase 2 where the result missed intent. Write 200 words on the taste judgment that went wrong. Goal: articulate the mismatch between brief and eye. This is the judgment that compounds.

**Closing move.** Save the master brief from Layer 2 as `~/claude-code-briefs/taste-brief.md`. Every future landing-page session starts there. Over 10 projects you refine it — that's your taste moat as an operator.

## Problem set

**Problem 1 — Seven-variable audit on a public page.** Pick one: linear.app, vercel.com, raycast.com, stripe.com, notion.com. Observe and record values for all seven variables using browser DevTools (Inspect → Computed). Deliverable: seven-row table. Pass: every value specific and measurable — "Geist Sans, scale 1.2, H1 48px line-height 1.1 weight 600," not "modern typography."

**Problem 2 — Position: shadcn wholesale adoption.** In 250 words, defend or refute *"In 2026, a solo operator running AI-services engagements should adopt shadcn/ui wholesale rather than build a custom component library."* Cite (a) maintainership concentration (Issue #6417, PR count), (b) Tailwind v4 migration timeline and cost, (c) your override strategy, (d) the specific break point where your answer flips. Pass: defensible position, four cited facts, stated flip condition.

**Problem 3 — Motion reconciliation.** Find one public page where motion improved a metric (cite the study — Rauno case studies, Stripe Appearance API demos, Unbounce or GoodUI conversion writeups) and one where stripping motion improved performance (Core Web Vitals migration writeups, prefers-reduced-motion retrofits). Write a 3-rule heuristic reconciling them. Pass: three rules, each with a named example.

**Problem 4 — Reverse-engineer a peer's page.** Pick a page shipped by an AI-services peer in the last 30 days. Reverse-engineer the seven variables. Write a 200-word note (do not send) naming one coherent choice and one incoherent choice with variable-level diagnosis. Pass: one coherent call, one incoherent call, both variable-specific.

**Problem 5 — The 200-word design brief.** Write a Claude-Code-ready brief specifying all seven variables at value level. Test it in two new projects 48 hours apart. Do the two pages agree on ≥5 of 7 variables? If not, iterate. Pass: two generated pages agreeing on ≥5 of 7 variables at value-level specificity.

**Scoring rubric for "agreement" per variable** (apply to each of the seven, mark each row pass/fail, count passes; ≥5 of 7 = overall pass):

| Variable | "Agree" = |
|---|---|
| Typography | Same family name on display + body; scale ratio within ±0.05 (e.g., 1.20 vs 1.25 = disagree); H1 px within ±4; body line-height within ±0.1 |
| Color | Same neutral hue (±10° OKLCH) and chroma tier (muted/saturated); accent within ±0.05 L and ±0.03 chroma; same dark/light policy |
| Spacing | Same base unit (4 or 8), same section-to-section gap within ±8px, same internal<external rule observed |
| Density | UI label size within ±1px, button height within ±2px, radius within ±2px, same border-vs-shadow policy |
| Motion | Same "state-change only" or "ambient-allowed" stance, durations within ±20ms, reduced-motion wrapper present/absent the same way |
| Imagery | Same above-fold policy (zero / product-screenshot / illustration / photo), no generative drift between runs |
| Voice | Same case (sentence/title), same banned-verb list respected, same punctuation policy on headlines |

Score honestly — the point is to find which variable your brief is under-specifying, not to pass. If Typography and Color agree but Motion and Imagery drift, rewrite those two override prompts with tighter values and re-test.

## Common failure modes at scale

**Failure 1 — Override drift across sessions.** You write a tight seven-variable override Monday. Thursday, in a different session, the model generates a new component using defaults, not your overrides — the design-system context did not carry. Mitigation: commit the override to `design-brief.md` at repo root; reference it in every session opener.

**Failure 2 — Hex-code briefing.** You paste `#6366f1`. The model uses it as primary and invents hover/focus states by guessing — not perceptually consistent because the model does not convert to OKLCH internally. Mitigation: always brief color as an OKLCH ramp with explicit stops, never a single hex.

**Failure 3 — Over-motion.** The model adds Framer Motion to every element because training data associates "modern landing page" with animation. You ship 14 motion rules, main-thread paint blows past 200ms, Core Web Vitals drops, Lighthouse flags non-composited animations.[^21] Mitigation: enumerate allowed durations and ban ambient motion explicitly.

**Failure 4 — Title-case regression.** Despite prompting sentence case, the model generates title case because most training data is title case. Mitigation: post-generate, ask the model to list every H1/H2/H3 and flag any that drifted to title case.

**Failure 5 — Aesthetic namedropping without variables.** "Make it look like Linear" → weighted average of 40 Linear-adjacent pages → not Linear. Never namedrop without specifying ≥3 of 7 variables at value-level.

**Failure 6 — Shadcn defaults leaking.** You customize primary color and typography; the page still reads "shadcn" because radius, border style, and button height are untouched. Mitigation: post-generation diff against `/components/ui` defaults; override radius, border opacity, button height if your target is not shadcn-aesthetic.

## Open questions / what's not settled

**(1) Does variable-level briefing survive model-update cycles?** The argument assumes the model executes precise specs. Some code-gen tools interpolate — the more specific your brief, the more they compress into their training distribution. No public benchmark on brief-fidelity across v0, Lovable, Bolt, Claude Code as of April 2026. Operator signal: Claude Code and v0 currently execute OKLCH briefs; Lovable and Bolt drift to HSL/hex more often. May invert with updates.

**(2) Is the Linear / Rauno / Geist aesthetic already dated?** The 2024–2025 "linear design" trend produced enough copycats (per LogRocket's multi-article coverage) that by late 2025 there was a visible backlash — indie designers moving toward mid-century revival, brutalist typography, saturated color on light. Safe move: hit the current dominant aesthetic well and re-evaluate every 18 months. Bold move: pick a differentiating direction. Both ship; only one stands out.

**(3) Shadcn maintainership risk.** The single-maintainer concentration (Issue #6417 open) is the recurring 2025–2026 design-system-risk concern. Ownership-in-codebase mitigates but doesn't eliminate — upstream security and accessibility fixes still come from the maintainer. No resolution yet.

## Reviewer lens — named critics with specific disagreements

**Adam Wathan (Refactoring UI co-author, Tailwind creator)** would push back on Layer 1's typography section. His position, per Refactoring UI, is that **scale ratio is less important than weight and size contrast**.[^1] He would argue the brief's "scale 1.125 with explicit px values" is over-engineered for operators — "large headline, medium subhead, default body, small caption from the Tailwind scale" hits 90% of the aesthetic without the cognitive cost. The 1.125-vs-1.333 distinction is something only designers notice.

**Steve Schoger (Refactoring UI co-author)** would push back on the color section. His position: **OKLCH is a technical improvement, but most operator pages ship wrong color choices, not wrong color spaces**.[^1] The common failure is oversaturated accents, pure black text (should be oklch 0.15–0.22 instead), and hover states with insufficient lightness delta. His override replaces the full OKLCH ramp prompt with "dim your accent by 10% saturation, never pure black, hover state needs ≥0.08 lightness delta."

**shadcn (shadcn/ui maintainer)** would push back on Layer 3's synthesis. His position: **the adoption-vs-plunder framing is a false binary** — shadcn is designed so that wholesale adoption and plunder are the same act, because copy-in-codebase turns every adopted component into an owned one.[^25] The "drift problem" the Design Systems Collective names is a feature: your components diverge from upstream because your product diverges.

**Brian Lovin (designer, Notion)** would push back on Layer 2's density table. His position: **density is the most audience-indexed of the seven variables**.[^30] What reads as "Linear-dense" to developers reads as "cluttered" to finance buyers. The density override should fork: dense for multi-hour-session audiences (developers, analysts); loose for dip-in-and-out audiences (sales, recruiting).

**Rauno Freiberg (Devouring Details, Vercel)** would push back on the motion reconciliation. His position: **the state-change-only rule is too conservative**.[^16][^17] Motion as ambient texture — subtle noise, slow gradient drift, cursor-tracked position — is valid design language when it contributes to perceived polish. Collapsing all non-state-change motion into "tax" trades craft for compliance. His stance: `prefers-reduced-motion` wrappers plus tasteful ambient motion, not ambient bans.

## Further reading

**Must (read this week):**
1. **Refactoring UI** — Adam Wathan and Steve Schoger. The 250-page PDF. The seven-variable literacy derives from this book; reading it moves you from "know the variables" to "have an instinct for when each is wrong." refactoringui.com.
2. **Devouring Details** — Rauno Freiberg. 23 chapters, interactive components, focus on motion and interaction. devouringdetails.com. Paid, worth it.
3. **Tailwind CSS v4.0 release post** — tailwindcss.com/blog/tailwindcss-v4. The OKLCH migration and theme variable model is what most 2026 code-gen tools target.

**Recommended:**
4. **Linear Method — Principles & Practices** — linear.app/method/introduction. The opinionated-software argument in full.
5. **shadcn/ui docs** — ui.shadcn.com/docs. Read the philosophy page and the Tailwind v4 changelog (ui.shadcn.com/docs/changelog/2025-02-tailwind-v4) together.
6. **Basement Studio — The Birth of Geist** — basement.studio/post/the-birth-of-geist-a-typeface-crafted-for-the-web. Case study on commissioning a bespoke typeface.
7. **Evil Martians — OKLCH in CSS** — evilmartians.com/chronicles/oklch-in-css-why-quit-rgb-hsl. The canonical technical argument for the color-space migration.

**Optional:**
8. WCAG 2.2 — w3.org/TR/WCAG22. Skim Success Criterion 2.3.3 and the prefers-reduced-motion guidance (C39).
9. Lexington Themes blog (Michael Andreuzza, 2025) — lexingtonthemes.com/blog. Applied Tailwind v4 / OKLCH work at the marketing-page layer.
10. Chrome for Developers — Avoid non-composited animations — developer.chrome.com/docs/lighthouse/performance/non-composited-animations. Performance side of the motion debate.

## Citations

[^1]: Adam Wathan and Steve Schoger, *Refactoring UI* (book and video series). refactoringui.com and steveschoger.com/book. The seven-variable framing directly maps to the book's chapters on hierarchy, layout/spacing, typography, color, and personality. Verified 2026-04-17.

[^2]: Linear, "Principles & Practices — Linear Method." linear.app/method/introduction. Sourced for the opinionated-software claim and Linear's quality-first framing. Verified 2026-04-17.

[^3]: Vercel, "Geist Design System Introduction." vercel.com/geist/introduction. Sourced for typography, color, and density claims about Vercel's system. Verified 2026-04-17.

[^4]: Raycast Developers, "User Interface API." developers.raycast.com/api-reference/user-interface. Sourced for Raycast's UI component model and density claims. Verified 2026-04-17.

[^5]: basement.studio, "The Birth of Geist: A Typeface Crafted for the Web." basement.studio/post/the-birth-of-geist-a-typeface-crafted-for-the-web. Sourced for Geist's origin as a bespoke Vercel typeface (with Univers, SF Mono, SF Pro, Inter, and Suisse International as acknowledged influences), its elevated x-height and abbreviated descenders, and its positioning as a brand signal distinct from the default Inter look. Verified 2026-04-17.

[^6]: Linear Design System on Figma Community, figma.com/community/file/1222872653732371433/linear-design-system. Sourced for the scale ratio and weight conventions. Verified 2026-04-17.

[^7]: Kirill Zmeev et al., various Refactoring UI summaries and 8pt-grid writeups — designsystems.com/space-grids-and-layouts, jacobshannon.com/blog/books/refactoring-ui/layout-and-spacing. Sourced for line-height conventions across display and body. Verified 2026-04-17.

[^8]: Evil Martians, "OKLCH in CSS: why we moved from RGB and HSL." evilmartians.com/chronicles/oklch-in-css-why-quit-rgb-hsl. Published 2024. The canonical technical argument for OKLCH adoption. Verified 2026-04-17.

[^9]: Guillermo Rauch (Vercel CEO), X post announcing Geist Design System. x.com/rauchg/status/1765851662617637230. March 7, 2024. Verified 2026-04-17.

[^10]: shadcn/ui, "February 2025 — Tailwind v4." ui.shadcn.com/docs/changelog/2025-02-tailwind-v4. Published February 2025. Sourced for the data-slot, forwardRef, OKLCH migration details. Verified 2026-04-17 via WebFetch.

[^11]: Tailwind CSS, "Tailwind CSS v4.0 release post." tailwindcss.com/blog/tailwindcss-v4. Published 2025. Sourced for default OKLCH adoption in v4. Verified 2026-04-17.

[^12]: CSS-Tricks OKLCH Almanac entry. css-tricks.com/almanac/functions/o/oklch/. Sourced for OKLCH function syntax and browser support as of 2024/25. Verified 2026-04-17.

[^13]: Raycast design evolution coverage — LogRocket, "Linear design: The SaaS design trend that's boring and bettering UI" (blog.logrocket.com/ux-design/linear-design) and Raycast UIKit Figma (figma.com/community/file/1239440022662828277/raycast-uikit). Sourced for the 2024 gradient-to-2025 red transition. Verified 2026-04-17.

[^14]: Zack MacTavish et al., "Designing in the 8pt grid system" (medium.com/design-bootcamp/designing-in-the-8pt-grid-system-f3c1183ea6e8) and Chris Godby, "The 8pt Grid: Consistent Spacing in UI Design with Sketch." Sourced for the canonical 4/8 spacing scale. Verified 2026-04-17.

[^15]: designsystems.com, "Spacing, grids, and layouts." Sourced for the internal-less-than-external principle. Verified 2026-04-17.

[^16]: Rauno Freiberg, "Devouring Details" course. devouringdetails.com. Launched 2024, updated 2025 to 23 chapters. Verified 2026-04-17.

[^17]: Rauno Freiberg, "Invisible Details of Interaction Design." every.to/p/invisible-details-of-interaction-design (Every Inc, 2023/2024). Also referenced on Rauno's LinkedIn activity-7084247753773432832. Sourced for the motion-as-medium position. Verified 2026-04-17.

[^18]: web.dev, "Animation and motion" (accessibility learn module). web.dev/learn/accessibility/motion. Sourced for the vestibular-dysfunction prevalence and motion-cost framing. Verified 2026-04-17.

[^19]: W3C WAI, "C39: Using the CSS prefers-reduced-motion query to prevent motion." w3.org/WAI/WCAG21/Techniques/css/C39 and WCAG 2.2 recommendation w3.org/TR/WCAG22. Sourced for Success Criterion 2.3.3 and the prefers-reduced-motion authoring rule. Verified 2026-04-17.

[^20]: Pope Tech, "Design accessible animation and movement with code examples." blog.pope.tech/2025/12/08/design-accessible-animation-and-movement. Sourced for WCAG-compliant motion patterns. Verified 2026-04-17.

[^21]: Chrome for Developers, "Avoid non-composited animations" (Lighthouse performance). developer.chrome.com/docs/lighthouse/performance/non-composited-animations. Also web.dev/articles/rendering-performance. Sourced for the compositor-vs-main-thread animation cost claim. Verified 2026-04-17.

[^22]: Linear, "How we redesigned the Linear UI (part II)." linear.app/now/how-we-redesigned-the-linear-ui. 2024. Sourced for Linear's in-house design-token system and density decisions. Verified 2026-04-17.

[^23]: Figma Blog, "The Linear Method: Opinionated Software." figma.com/blog/the-linear-method-opinionated-software. 2024. Sourced for the opinionated-software philosophy. Verified 2026-04-17.

[^24]: LogRocket Blog, "Linear design: The SaaS design trend that's boring and bettering UI." blog.logrocket.com/ux-design/linear-design. Sourced for the Linear design trend taxonomy. Verified 2026-04-17.

[^25]: shadcn/ui, "Introduction" docs. ui.shadcn.com/docs and ui.shadcn.com. Sourced for the copy-in-codebase philosophy. Verified 2026-04-17.

[^26]: shadcn/ui, "October 2025 — New Components." ui.shadcn.com/docs/changelog/2025-10-new-components. Sourced for the Q4 2025 component wave. Verified 2026-04-17.

[^27]: Design Systems Collective, "Why Shadcn/ui Struggles at Enterprise Scale." designsystemscollective.com/why-shadcn-ui-struggles-at-enterprise-scale-9f7416f3af3f. 2025. Sourced for the drift / merge-cost critique. Also shadcn-ui/ui GitHub Issue #6417 "MORE MAINTAINERS" and Discussion #1374. Verified 2026-04-17.

[^28]: Mashuk Tamim, "Is Your Shadcn UI Project at Risk? A Deep Dive into Radix's Future." mashuktamim.medium.com/is-your-shadcn-ui-project-at-risk-a-deep-dive-into-radixs-future-91af267c4bec. Sourced for the Radix / Modulz / WorkOS maintainership timeline. Verified 2026-04-17.

[^29]: Michael Andreuzza, Lexington Themes blog. lexingtonthemes.com/blog. 2025 posts on Tailwind v4 gradients, multi-theme toggles, and accessible carousels. Sourced as the shadcn-adjacent plunder alternative. Verified 2026-04-17.

[^30]: Brian Lovin, personal site. brianlovin.com. Sourced for design-writing reviewer lens; Brian currently designs AI products at Notion (per public bio). Verified 2026-04-17.
