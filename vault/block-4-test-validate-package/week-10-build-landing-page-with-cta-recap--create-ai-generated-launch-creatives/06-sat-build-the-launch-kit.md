---
type: lesson
block: block-4-test-validate-package
week: week-10
day_of_cycle: 6
day_name: sat
session_slug: create-ai-generated-launch-creatives
date_due: 2026-07-25
tags: [build-day, launch-kit, landing-page-build, creative-kit, qa-gate, instrumentation, launch-checklist, claude-code, code-lab]
sources:
  - posthog-pricing
  - midjourney-docs-comparing-plans
  - elevenlabs-pricing
  - cursorclip-screen-studio-alternatives
  - auditsocials-meta-ai-label-2026
  - causo-product-hunt-traffic-2026
  - ftc-operation-ai-comply-2024
  - uscopyright-part2-copyrightability-2025
last_verified: 2026-07-17
word_count_target: 3400
---

# BUILD — the launch kit for your Week 9 package: page, creatives, instrumentation, checklist

## Why this matters

Today the week's five documents become one shipped artifact. You have Monday's copy and substantiation file, Tuesday's page spec, Wednesday's stack and brand spec, Thursday's four QA-passed assets, and Friday's instrumentation plan with pre-registered bands. Build day converts them into a live page with a full creative kit and working instruments, gated by the code-lab's QA runner, finished with a launch checklist and a scheduled decision date. The build is time-boxed by milestone because the alternative, polishing forever, is the most socially acceptable way to never launch.

A build-day framing note: everything today is assembly, not invention. If you find yourself inventing (new copy, new sections, a new aesthetic), you have left the build and re-entered a weekday lesson; write the idea down for iteration two and return to the milestone clock. Launches are experiments, and experiments run on the protocol they pre-registered.

## Prerequisites

- The five weekday outputs, actually done. Missing ones cost you their weekday's experiment time today; budget accordingly.
- The code-lab: `code-lab/06-launch-kit/` — brief generator + asset-QA runner, stdlib-only, no keys. Run its example once before starting (5 minutes) so the tools are familiar when you need them at milestone 3.
- Your deployment path from [[05-fri-prototype-pipeline|Block 2 Week 3 Friday]]: any stack you can ship with Claude Code (static + your host of choice is fine; the page has no backend requirement unless your sandbox needs one).

## Milestone 1 (90 min) — The page, from spec to deployed

Build from Tuesday's spec file; do not redesign en route.

**The Claude Code prompt shape that works** (adapt, don't copy blindly):

```
Read spec.md (page skeleton), brand.md (palette, type, imagery rules), and
copy.md (final copy: hero, eval section, objection blocks, pricing, FAQ).
Build a single-page site: [your stack]. Constraints:
- One primary CTA ([your CTA]); the only other link is the quiet
  secondary path named in spec.md. Count tappable elements; report the count.
- Design tokens from brand.md only; no new colors or fonts.
- Sections in spec order; eval section renders methodology visibly.
- OG meta tags wired to /assets/og_card.png (1200x630), title + description
  from copy.md.
- No placeholder text anywhere: if copy.md lacks a string, stop and ask.
```

The "report the count" line matters: attention-ratio drift is the codegen default, and making the agent count tappables turns Tuesday's recap discipline into a build gate. When the page is up, run the three checks that catch 80 percent of launch-page embarrassments: mobile viewport at 390px, thumbnail render of the OG card in a Slack/LinkedIn preview debugger, and the hero one-read test on a person who has not seen it (a housemate over coffee counts).

**Demo asset placement:** whichever rung Tuesday chose. If sandbox: confirm isolation (demo tenant, no side-effect tools), rate limits, and the spend breaker *before* it goes live, and rehearse the fallback flag that swaps the video in. That rehearsal is non-negotiable; you will not debug calmly at T+2h with traffic on the page.

## Milestone 2 (45 min) — The remaining kit, brief-first

You produced four assets Thursday. Generate the rest of the inventory (remaining ad variants, social cutdowns list, any missing crops) the pipeline way:

1. Fill `my/launch_kit.json` (copy from the example): package facts, brand spec verbatim from Wednesday, the asset list with hooks assigned.
2. `python brief_generator.py my/launch_kit.json` → read every brief once. The generator is deterministic on purpose: briefs are specs, and specs should not be sampled. Where a brief reads wrong, fix the *config*, regenerate, and only then generate assets.
3. Batch in your Wednesday tools per brief; select against brief; polish; archive records as you go (the manifest wants prompt/tool/settings/license per asset, and future-you wants them more[^1]).

Budget guard: if any single asset consumes more than 15 minutes of generation-and-selection, take the best current candidate and move on. Thursday's rule stands (never negotiate with a mediocre candidate), but build day adds its dual: never let one asset eat the kit.

## Milestone 3 (30 min) — The QA gate, mechanically and humanly

1. Fill `my/qa_manifest.json` and `my/claims.json` (the claims file is Monday's substantiation list, exact strings).
2. `python qa_runner.py my/qa_manifest.json` → fix until exit code 0. The runner enforces dimensions (OG exactness included), size budgets, filenames, alt text, archive completeness, disclosure consistency for photorealistic AI content,[^2] banned unsubstantiated phrases, and numeric-claims-versus-claims-file. Every check exists because a lesson this week showed the failure it prevents.
3. Run the human judgment pass per asset, out loud, from Thursday's list: artifact scan, brand match, thumbnail legibility, slop test, claim test, positioning test. Log results in the manifest as a `human_qa` note per asset; the point is the record, not the ceremony.

Exit code 0 plus a written judgment pass is the definition of "the kit is done." Prettier is not a milestone.

## Milestone 4 (30 min) — Instruments on, verified

Implement Friday's plan: the event taxonomy on the page, UTM scheme applied to every link you will post, the free-text "how did you hear about us" field at the qualified-action surface, the five war-room tiles, the sandbox spend tile if applicable. PostHog's free tier covers all of it without a card.[^3]

Verification is the milestone: fire every event yourself (view, scroll marks, demo engagement, objection blocks, qualified action) and watch each land in the tool. Then break one thing on purpose (rename an event in the page, not the plan) and confirm you *notice* on the dashboard. Instruments you have not seen fail are instruments you cannot trust on launch day.

## Milestone 5 (30 min) — The launch checklist and the dry run

The checklist, complete; every line gets a checked box or a written reason it does not apply:

**Page.** Hero one-read test passed by a stranger · one primary CTA, tappable count recorded · mobile at 390px · OG card renders in preview debugger · eval section shows methodology · security block states data flow, retention, credentials · pricing shows worked math · every claim traces to claims.json · no placeholder text.

**Demo.** Chosen rung live · sandbox isolation + rate limits + spend breaker verified (or n/a) · fallback video rehearsed · demo events firing.

**Kit.** qa_runner exit 0 · human judgment pass logged · disclosure flags set where triggered[^2] · archive complete per asset · licenses match plan tier actually paid for (the Midjourney revenue clause and the ElevenLabs free-tier exclusion are the two that bite operators[^4][^5]).

**Instruments.** All events verified · UTMs on every controlled link · HDYHAU field live · tiles built · decision-memo skeleton dated, bands written, calendar blocks for T+24h/72h/7d/14d exist.

**Channels.** Launch post drafted in your voice (not raw model text; the one platform where your buyers live demotes that[^6]) · channel list with posting order · Product Hunt decision made deliberately, with separate UTM and pass bar if yes[^7] · reply capacity protected for T+0 to T+6h.

**Claims hygiene.** One last pass: nothing on the page or in the kit you could not substantiate to a regulator or a skeptical buyer.[^8]

**The dry run:** post the page to one friendly human as if launching, watch the events arrive, receive their reply, and log them as interview-pool entry #1. Launch is tomorrow, or whenever your channel timing says; the artifact is done tonight.

## Ship log — what to record when it's live

Ten minutes, same night: deployed URL and commit hash · final tappable count · which proof rung shipped and why · total creative spend and hours by milestone · the three things you cut to make the clock · the single biggest deviation from spec and who approved it (you did; write down why). This log is Week 11 input and, per this block's running theme, the difference between an experiment and an anecdote.

## Common mistakes experts see

1. **Redesigning during assembly.** The weekday specs were the design; build day drift produces launches that are 90 percent done forever.
2. **Skipping the event verification because the code "obviously works."** Launch-day analytics bugs are silent and unrecoverable; the data just never existed.
3. **Sandbox live, spend breaker untested.** The one failure that converts a good launch into an invoice.
4. **QA exit code 0 treated as fully done.** The runner is the mechanical half; the judgment pass catches the six-fingered hand the parser cannot see.
5. **Launching the moment the build finishes, at 11pm, exhausted.** The artifact being done and the launch moment are separate decisions; T+0-to-T+6h is a reply-fast window that deserves your morning, not your dregs.
6. **Letting the checklist's "n/a" boxes go unwritten.** An unexplained n/a is a skipped check wearing a costume.

## Reflection questions

1. Which milestone ran longest over budget, and was the overrun invention or assembly? What does that say about which weekday's output was weakest?
2. The QA runner rejected something you liked. Did you fix the asset or edit the claims file? Which direction should the pressure flow, and when would the other direction be legitimate?
3. Your ship log's "three things cut" list: which of them will iteration two actually restore, honestly? What does that imply about default scope for your next launch?
4. If you had to rebuild the entire kit next month for a second package, what would you templatize from today, and what genuinely cannot be templatized?
5. Tomorrow at T+3h, one channel is outperforming and your sandbox tile shows an odd input pattern. You have 20 minutes of attention. Write your triage order now, while calm.

## My take (reviewer lens)

**Boris Cherny** would approve of the runner-gates-the-repo shape but point at the seam: the QA runner checks assets at rest, and nothing re-checks what platforms do to them after upload (Advantage+ mutations, preview recompression, metadata stripping); his fix is a T+1 verification pass on *served* creative, screenshots into the archive, which costs ten minutes and closes the last mile. **Seibel** would bless the time boxes and then say the quiet thing: most readers should have shipped a version of this page in Week 9 with a paragraph and a Calendly link, and today's kit is iteration three of a page that should already have talked to strangers; if today produced your *first* public artifact, the lesson to carry is that your default sequencing is too polished. **Hamel Husain** would note with approval that the claims file is load-bearing in the literal build (copy fails CI without substantiation) and then raise the bar once more: the golden set behind those claims was built weeks ago, and an agent that shipped features since then has an eval that is quietly stale; before the decision memo at T+14d, re-run the eval, because the only thing worse than no published number is a published number that is no longer true.

## Further reading

**Must-read**

- `code-lab/06-launch-kit/README.md` — run the example end-to-end before milestone 1; the deliberate failure teaches the report format in two minutes.
- [[06-sat-validation-instrumentation]] — the measurement canon your Friday plan implements; skim the decision-rule layer tonight.

**Recommended**

- Your own Tuesday spec and Friday memo, re-read cold before starting. Specs read differently when the clock is running.

**Optional**

- Causo Hub's Product Hunt traffic bands — if and only if the channel list includes PH, recalibrate expectations tonight, not at T+2h.[^7]

## Citations

[^1]: Archive discipline motivated by tool-mortality: OpenAI's two-stage Sora shutdown with post-deadline data deletion (app 2026-04-26, API 2026-09-24) — see Wednesday [^7]/[^8] for full citations (The Decoder; OpenAI Help Center).

[^2]: Meta AI-content disclosure and detection enforcement for ads: AuditSocials, "Meta AI Content Label Policy 2026," https://www.auditsocials.com/blog/meta-ai-generated-content-label-policy-2026 with corroboration per Thursday [^5] (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^3]: PostHog pricing: free monthly 1M events / 5,000 replays, usage-based beyond. https://posthog.com/pricing — corroboration per Friday [^2] (search-verified 2026-07-17).

[^4]: Midjourney commercial terms incl. the >$1M-revenue Pro/Mega requirement: https://docs.midjourney.com/hc/en-us/articles/27870484040333-Comparing-Midjourney-Plans — corroboration per Wednesday [^1] (search-verified 2026-07-17).

[^5]: ElevenLabs free tier's commercial-use exclusion; Starter as commercial floor: https://elevenlabs.io/pricing — corroboration per Wednesday [^4] (search-verified 2026-07-17).

[^6]: LinkedIn's demotion of generic AI-generated content: Social Media Today + ZoomSphere + course master refresh report — full citation Thursday [^7] (search-verified 2026-07-17).

[^7]: Product Hunt 2026 traffic bands and Featured-gating: Causo Hub, https://hub.causo.ai/guides/product-hunt-traffic-data-2026 — corroboration per Friday [^6] (search-verified 2026-07-17).

[^8]: FTC substantiation standard for AI capability claims (Operation AI Comply): https://www.ftc.gov/news-events/news/press-releases/2024/09/ftc-announces-crackdown-deceptive-ai-claims-schemes — see Monday [^6][^7]; copyright-registration disclosure duty per US Copyright Office guidance, Wednesday [^6].

_last_verified: 2026-07-17_
