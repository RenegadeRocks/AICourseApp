---
type: lesson
block: block-4-test-validate-package
week: week-10
day_of_cycle: 5
day_name: fri
session_slug: build-landing-page-with-cta-recap
date_due: 2026-07-24
tags: [launch-instrumentation, qualified-action-rate, event-taxonomy, utm, dark-social, self-reported-attribution, product-hunt, session-replay, kill-scale-thresholds, posthog, week-11-handoff]
sources:
  - posthog-pricing
  - userorbit-posthog-pricing-2026
  - causo-product-hunt-traffic-2026
  - puthusu-product-hunt-worth-it-2026
  - foundra-product-hunt-playbook-2026
  - heeet-blended-attribution
  - oktopost-dark-social
  - getrecast-hdyhau-limitations
  - stealery-dark-social-b2b
  - movingparade-attribution-broken
  - growthspree-demo-benchmarks-2026
last_verified: 2026-07-17
word_count_target: 4700
---

# Launch-day instrumentation — measuring a launch so it produces a decision instead of a feeling

## Why this matters

Tomorrow you ship. Without instrumentation, here is what launch day gives you: a traffic spike, some likes, three nice DMs, and a feeling. The feeling is not data. Next week ([[week-11-define-your-product-idea-validate-idea-using-ai--market-user-validation-interview-or-poll-potential-users|Week 11]]) runs the formal validation discipline, and it can only run on what launch week *recorded*. Today you wire the page and the channels so that fourteen days from launch you can answer, with numbers you pre-committed to: did the market respond enough to keep investing in this package, and specifically *where* is the response coming from?

The failure mode this lesson exists to prevent has a specific shape, and every cohort produces it: an operator launches, gets 1,900 visitors and 6 sign-ups, feels vaguely encouraged, iterates the hero copy for two weeks based on nothing, and never learns that 1,700 of those visitors came from one channel that will never repeat and that the 6 sign-ups all came from a different channel that is cheap to work weekly. Vanity aggregation hides the decision. Instrumentation is how you unhide it, and for an agent product with a sandbox on the page, the instrumentation also carries a security duty (Tuesday's isolation and abuse limits) that generic SaaS launches do not have.

## Prerequisites

- The measurement layer from [[06-sat-validation-instrumentation|Block 2 Week 3 Saturday]] is assumed wholesale: compact event taxonomy, the four-domain event model, replay's legal/consent regime, Wilson intervals for small samples, and the pre-registered decision rule. Today builds the *launch-specific* layer on top; if any of that list is fuzzy, re-read it before Saturday.
- Tuesday's page skeleton (sections, CTA, sandbox decision) and Thursday's ad variants: they define most of what gets tracked.
- A calendar: the decision date gets scheduled today, before you have data to be tempted by.

## Layer 1 — The launch's primary metric: qualified-action rate

Unique visitors are the weather. The metric that carries your Week 11 decision is the **qualified-action rate (QAR)**: qualified actions divided by unique visitors, where "qualified action" is defined *today, in writing*, as the cheapest visitor behavior that credibly predicts becoming a customer for your specific package and CTA.

For a demo-call CTA, the qualified action is a booked call that shows up (a booking that no-shows is a weaker signal, and you will track both). For a scoped trial, it is completing the evidence moment: uploading the sample tickets, seeing the resolution report. For the curated-input sandbox, it is *not* running one demo input (that is curiosity); it is something like running two-plus inputs and then clicking through to pricing, a composed behavior you define as one funnel. The principle: the qualified action must cost the visitor something (time, data, calendar space, an email they answer), because costless actions are noise at exactly the moment you most want signal. Launch traffic is the least-qualified traffic your page will ever see; a metric that counts cheap actions will produce its most flattering number on the day it is most misleading.

Set the pass bars now, using Tuesday's benchmark context honestly: demo-request pages average 1.5–4 percent conversion with top quartiles at 8–15 percent, and rates fall as ACV rises.[^1] Launch-week traffic converts below steady-state (cold, curious, wrong-ICP-heavy), so a sane pre-registered structure for a demo-CTA agent page is a three-band rule in the [[06-sat-validation-instrumentation|Week 3 Saturday]] pattern: **kill-signal** below some floor (e.g., QAR < 0.5 percent with n > 500 visitors *and* zero qualified conversations that excite you), **continue** in the middle, **scale-signal** above a ceiling (e.g., QAR > 3 percent or any week with 5+ shown-up calls). Your numbers will differ; that they are written *today* is the entire discipline, and it is Week 3's pre-registration rule doing its canonical job. One addition specific to launches: pre-register the *duration* too (14 days is the course default), because launches decay by design, and a decision rule without an end date invites waiting for a better week forever.

## Layer 2 — The launch event taxonomy

Week 3 Saturday's compact-taxonomy rule (few events, well-named, with properties doing the work) is assumed; here is the launch-specific event set, small enough to implement in an hour on Saturday:

- `page_view` with `channel` property (Layer 3's attribution machinery feeds it), plus scroll-depth markers at the eval block and pricing (two sections whose reach tells you whether the page's argument is being *consumed* or bounced off).
- `demo_engaged` for the demo asset, with properties: `kind` (video/tour/sandbox), `depth` (started/completed for video and tour; inputs-run count for sandbox), and for the sandbox `input_id`, so you learn *which* of your six curated inputs converts belief (the burst-pipe demo and the escalation demo will perform differently, and that difference is market information about which proof persuades).
- `objection_block_viewed` with `block` (security/when-wrong/integration/faq): tells you which disqualifier your traffic actually carries. If 60 percent of engaged visitors open the security block, Week 11's interview script just wrote its first question.
- `pricing_engaged` (view + calculator interaction if you built one).
- `qualified_action` (the Layer 1 definition, fired exactly once per visitor) and its weaker siblings (`cta_click`, `booking_created`, `booking_attended`), kept separate so the funnel's leak points are visible.
- `sandbox_abuse_tripped` (rate limit, spend breaker): Tuesday's defenses, instrumented. Also tag all sandbox traffic so it never contaminates product analytics, and give the sandbox its own spend dashboard for the war room.

Tooling: PostHog's free tier (1M events and 5,000 session replays monthly, no credit card) covers a launch several times over; paid overage starts at $0.00005/event and $0.005/replay, so even a heavy launch month is coffee money.[^2] Whatever tool you use, the taxonomy above is deliberately tool-agnostic.

On session replay for the launch page: the legal and consent regime (wiretap-theory litigation, consent banners, the collapse of quiet default-on replay) is [[06-sat-validation-instrumentation|Week 3 Saturday]] canon; apply it unchanged to the marketing page, and note the one launch-specific addition: replays of *sandbox* sessions are close to user-research gold (you watch a stranger try to break your agent), so sample them deliberately rather than drowning in page-scroll replays of bounced ad traffic.

## Layer 3 — Attribution across launch channels, honestly

A launch is multi-channel by nature: your LinkedIn post, a community share, maybe Product Hunt, maybe $200 of Thursday's ad variants, plus the channel you cannot see. The instrumentation stance that survives 2026 is **hybrid attribution**: mechanical tracking where it works, self-reported where it cannot.

**The mechanical layer.** UTM-tag every link you control (channel, variant), and accept the known blind spot: shares through Slack, WhatsApp, DMs, email forwards, and podcast mentions arrive as "direct" traffic. This is the dark-social problem, and it is not an edge case; the classic RadiumOne finding put 84 percent of outbound sharing in private channels, and 2026 B2B analyses consistently estimate that a third to half of pipeline originates in channels software attribution cannot see.[^3] For a launch specifically, the mechanically-invisible share is often your *best* signal (a founder DMing your page to another founder), so a launch measured by UTM alone systematically undercounts its highest-intent channel; the 2026 dark-funnel literature treats this undercount as structural, not fixable with better tagging.[^7]

**The self-reported layer.** One required field wherever a qualified action happens: "How did you hear about us?", free text, not a dropdown. Hybrid-attribution practice treats this as the correction factor for dark social, and the practitioner literature is emphatic that the free-text answers surface channels no software model detects.[^4] Also record it verbally on every demo call (you were going to ask anyway) and write it down in the same field. Two honesty notes so you use the instrument correctly: self-reported attribution has known biases (people cite the most memorable touch, not the first or the decisive one, a limitation the measurement-skeptic literature documents well), and at launch volumes your n will be small; you are reading it as qualitative channel discovery, not as a precise mix model.[^5] At your scale that is exactly the right use: one "saw your eval thread on LinkedIn, then my cofounder sent me the page" answer is worth more than a week of last-click reports.

**Product Hunt, since someone will ask.** The 2026 reality, corroborated across founder analyses: an editorial team curates the homepage; only roughly one launch in ten gets Featured, and non-featured launches see a fraction of the traffic regardless of upvotes. Featured top-3 finishes draw roughly 5,000–15,000 visitors and 100–400 sign-ups; top-10, roughly 1,000–3,000 visitors; outside the top 10, often under 500 visitors, with most volume in the first six hours. Links are nofollow, so SEO value is nil.[^6] The sober read for an agent-product operator: Product Hunt is a *credibility asset factory* (the badge, the reviews, the launch-day social proof reused in sales decks for a year) and a one-day traffic experiment, not a distribution strategy, and for B2B agent packages your buyers are likelier found through the channels [[06-sat-selling-ai-objections-and-closing|Block 1]] taught you to work directly. If you do launch there, the instrumentation consequence is simply: separate UTM, separate pass bar, and no averaging its spike into your channel comparison.

**The controversy, named.** Whether attribution is worth doing at all is a live fight. The dark-funnel school (Refine Labs' Chris Walker being the loudest voice of the "your software attribution is fiction, ask humans" position) holds that B2B buying happens in untrackable spaces and self-reported data should lead; the measurement-statistics school (Recast's critique of HDYHAU is the sharpest write-up) counters that self-reports are systematically biased memory artifacts and cannot support budget allocation either.[^4][^5] At launch scale, you get to sidestep the theology: you are not allocating a media budget, you are discovering which two channels deserve your next month. Hybrid, qualitative, small-n honest. Both schools agree software-only is wrong, and that is the only part you need.

## Layer 4 — The war room: launch-day operations

Instrumentation includes the humans watching it. The launch-day protocol, sized for one operator:

**T-minus 1 (tonight, Saturday):** dashboard with five tiles (visitors by channel, QAR funnel, demo engagement by kind/input, objection-block heatmap, sandbox spend). Alarms: sandbox spend breaker, error rate on the page, form failures. Test every event by firing it yourself and watching it land. A launch instrumented but untested is instrumented in Schrödinger's sense.

**T-zero to T+6h:** the high-volume window if any channel pops (Product Hunt's first-six-hours pattern generalizes: every channel's launch spike front-loads, and the 2026 launch playbooks converge on treating the first hours as a reply-speed contest rather than a broadcasting window).[^6][^8] Your job in this window is not watching dashboards; it is *replying*: to comments, DMs, and every single qualified action, personally, within the hour. The instrumentation's job is to make sure nothing you could learn in this window is lost while you are busy. One exception worth checking hourly: the sandbox tiles, because Tuesday's failure modes (abuse, cost, a bad viral input) are launch-hour phenomena, and your fallback video swap is a one-flag operation you rehearsed.

**T+24h, T+72h, T+7d, T+14d:** four scheduled looks, calendar-blocked today. Each look answers three questions against the pre-registered memo: is any band triggered, which channel leads on *qualified* actions (not visitors), and what are the free-text attribution answers saying. No other peeking, per the Week 3 statistics discipline; launch dashboards are engineered to be refreshed compulsively, and compulsive refreshing is how pre-registration dies.

**T+14d: the decision memo.** One page: QAR against bands, channel ranking by qualified action, the three most informative replays or sandbox sessions, every self-reported attribution answer verbatim, and the called band (kill-signal / continue / scale-signal) with the pre-registered consequence. This memo is the input artifact for Week 11's validation work, where its numbers meet actual user interviews, and where "continue" gets decomposed into what, exactly, to validate next.

## Layer 5 — What launch data cannot tell you (the Week 11 bridge)

Instrumentation's honest limits, stated so the memo does not overclaim. Launch data tells you *whether* and *where*, never *why*. Six sign-ups cannot say if the price is wrong, the ICP is wrong, or the security block scared people; the objection-block heatmap gives you a hypothesis, not an answer. Small-n statistics apply to everything above: with 800 visitors and a 2 percent QAR, your Wilson interval is wide enough that "1.4 percent vs 2.6 percent" channel differences are noise, which is why the memo ranks channels by qualified-action *counts and stories*, not by rate deltas. And the most valuable launch outputs may not be in the dashboard at all: the eleven people who replied to the launch post, the security lead who forwarded your data-flow page and asked one pointed question. Week 11's whole method (interviews and polls run with Mom-Test discipline) exists because measurement stops where motivation starts. Your instrumentation's final job is to *collect the humans*: every qualified action and every substantive reply goes into a list, because that list is Week 11's interview pool, warm, self-selected, and time-stamped launch week.

## Runnable experiment — write and wire the instrumentation plan

**Task.** Produce two artifacts. **(a) The instrumentation plan** (one page): QAR definition for your CTA, the event taxonomy above adapted to your page (with the sandbox events kept or struck per Tuesday's decision), channel list with UTM scheme, the self-reported-attribution field's placement, and the five war-room tiles. **(b) The pre-registered decision memo skeleton**: the three bands with your numbers, the 14-day window with calendar blocks created, and the consequence sentence for each band ("kill-signal → package pivots per Week 11's process, page stays up, no new creative spend"). Then wire what can be wired today: create the PostHog project (or equivalent), implement `page_view` + `qualified_action` on the skeleton page, and fire both by hand.

**Pass bar.** (1) The QAR definition names a behavior that costs the visitor something, and you can say in one sentence why cheaper actions were rejected. (2) Bands and dates are written and calendar-blocked *before* Saturday's build. (3) Two events verified end-to-end in the tool. (4) The plan fits on one page; if it does not, you are instrumenting to feel thorough rather than to decide, which is the vanity failure wearing an engineer's costume. Time: 60–90 minutes.

## Common mistakes experts see

1. **Counting cheap actions as conversion.** Email captures from a launch-day pop-up are applause, not intent; the QAR definition exists to keep applause out of the decision.
2. **UTM-only attribution.** Your best channel arrives labeled "direct," and you conclude your best channel does not exist.[^3]
3. **Dropdown "how did you hear about us."** Dropdowns return your own hypothesis list; free text returns the podcast you did not know mattered.[^4]
4. **Averaging the spike.** Product Hunt (or one viral post) merges into week-one numbers, and every rate becomes the mean of two different populations, meaningful for neither.[^6]
5. **Moving the bands mid-window.** Day 6, QAR is 0.4 percent, and suddenly there are good reasons the floor should be 0.3. Pre-registration exists because day-6 you is a motivated reasoner; day-0 you set the bands to protect the decision from them.
6. **Instrumenting the page and not the sandbox spend.** The one tile that can turn a great launch day into a four-figure invoice is the one generic analytics guides never mention.
7. **Letting the interview pool evaporate.** Fourteen days later, Week 11 begins, and the launch's respondents are cold and un-listed. Collect the humans as they arrive.

## Reflection questions

1. Your QAR definition is a claim about what predicts purchase. What is the cheapest piece of evidence that would prove your definition wrong (a high-QAR channel that never converts to revenue, say), and how long until you would see it?
2. If the objection-block heatmap shows security dominating, three explanations compete: your traffic is enterprise-heavy, your security block is weak, or security-curious visitors are just more thorough readers. Design the cheapest discriminating test.
3. The dark-funnel school says attribution software is fiction; the statistics school says self-reports are biased memory. Both are right. Write the two-sentence version of your launch's attribution epistemology that you could defend to either camp.
4. Which of your six sandbox inputs do you *predict* will have the highest completion-to-pricing rate? Write it down tonight. What does it mean for your positioning if you are wrong?
5. A scale-signal band triggers. What, concretely, do you scale in week three: the winning channel, the ad spend, the creative variants, or your own calendar? What does your answer reveal about which resource is actually your constraint?
6. What decision would you make differently at 14 days with 300 visitors versus 3,000? If the answer is "none," what traffic number *would* change your decisions, and does your channel plan have any credible path to it?

## My take (reviewer lens)

**Chip Huyen** would approve of pre-registration and small-n humility but would push on the metric's construct validity: QAR is a *proxy* for revenue, and proxies drift; the sandbox-heavy funnel especially can teach you to optimize for "people who enjoy playing with demos," a population with a nonzero but unproven overlap with buyers. Her fix: tag qualified actions through to revenue in a spreadsheet forever, even at n=5, so the proxy gets audited by the only metric that cannot lie. **Seibel** would look at this whole apparatus and say the quiet part: at your traffic levels, the dashboard is mostly theater, and the highest-yield instrumentation of launch week is answering every reply within ten minutes and asking each human two questions; he would keep the decision memo and the interview-pool list and shrug at the rest. The synthesis is honest: the plan above costs 90 minutes *because* Seibel is mostly right, and anything costlier would be instrumentation cosplay. **Ethan Mollick** would add the uncomfortable macro note: launch-week metrics measure your *distribution*, not your product, and in 2026 distribution is increasingly mediated by AI assistants summarizing your page to buyers who never visit it; the page-view-based funnel undercounts a growing class of buyer entirely, which is one more reason the free-text attribution field and the demo call, the two instruments that talk to humans, are the ones to protect as everything else changes.

## Further reading

**Must-read**

- [[06-sat-validation-instrumentation]] — the canonical measurement lesson this one stands on; re-read the Wilson-interval and pre-registration layers before setting your bands.
- Recast, "'How did you hear about us?' and the limitations of self-reported attribution" — the strongest steelman against your own new form field; calibrates how hard to lean on it.[^5]

**Recommended**

- Causo Hub, "Product Hunt traffic 2026: real numbers by daily rank" — the traffic bands that keep PH expectations sane.[^6]
- Heeet, "The Blended B2B Attribution Setup" — a clean writeup of the hybrid pattern this lesson endorses.[^4]

**Optional**

- PostHog pricing page — mostly as a worked example of usage-based pricing done transparently, which is also Monday's topic viewed from the buyer's side.[^2]
- Moving Parade, "Why B2B Marketing Attribution Is Broken" — the dark-funnel argument in full.[^3]

## Citations

[^1]: Growthspree. "B2B SaaS Demo Request Conversion Rate Benchmarks 2026." https://www.growthspreeofficial.com/blogs/b2b-saas-demo-request-conversion-rate-benchmarks-2026 — single benchmark publisher, used directionally for band-setting context (see Tuesday [^4]) (search-verified 2026-07-17).

[^2]: PostHog. Pricing. https://posthog.com/pricing — free monthly allowance: 1M analytics events, 5,000 session replays, 1M feature-flag requests, no credit card; overage from $0.00005/event and $0.005/replay with volume step-downs. Corroborated by UserOrbit, "PostHog Pricing 2026," https://userorbit.com/blog/posthog-pricing-guide and Flexprice, "PostHog Pricing Guide," https://flexprice.io/blog/posthog-pricing-guide (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^3]: Dark social scale and invisibility: Oktopost, "What is dark social in B2B marketing?" https://www.oktopost.com/blog/dark-social-in-b2b-marketing/ (private-channel shares arrive as direct traffic; RadiumOne's 84%-of-outbound-sharing finding) corroborated by Stealery, "What Is Dark Social? How It Affects B2B Pipeline Attribution," https://www.getstealery.com/blog/glossary/what-is-dark-social-b2b and Moving Parade, "Why B2B Marketing Attribution Is Broken," https://www.movingparade.com/blog/why-b2b-marketing-attribution-is-broken (30–50%-of-pipeline-invisible estimates) (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending; percentages are practitioner estimates, used directionally).

[^4]: Hybrid/blended attribution practice with free-text self-reporting: Heeet, "The Blended B2B Attribution Setup," https://www.heeet.io/blog/the-blended-b2b-attribution-setup-why-self-reported-attribution-is-in-your-star-studded-cast corroborated by 1827 Marketing, "Dark Social and Multi-Stakeholder B2B Attribution," https://1827marketing.com/smart-thinking/b2b-dark-social-attribution/ (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending). The dark-funnel position is associated publicly with Refine Labs / Chris Walker; framing corroborated by the same sources.

[^5]: Recast. "'How did you hear about us?' surveys and the limitations of self-reported attribution." https://getrecast.com/hdyhau/ — memory bias, most-memorable-touch substitution, and why HDYHAU cannot support precise mix decisions (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^6]: Product Hunt in 2026: Causo Hub, "Product Hunt traffic 2026: real numbers by daily rank," https://hub.causo.ai/guides/product-hunt-traffic-data-2026 (top-3 ≈ 5,000–15,000 visitors / 100–400 signups; top-10 ≈ 1,000–3,000; sub-top-10 often <500; first-six-hours concentration) corroborated by Puthusu, "Is Product Hunt worth it in 2026? An honest take," https://www.puthusu.com/blog/is-product-hunt-worth-it (editorial Featured curation ≈ 1 in 10; ~70% traffic penalty for non-featured; nofollow links) and Foundra, "The Product Hunt Playbook for First-Time Founders in 2026," https://www.foundra.ai/key-reads/product-hunt-playbook-first-time-founders-2026-after-algorithm-shift (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending; founder-analysis figures, directional).

[^7]: A88Lab. "Understanding the Dark Funnel in 2026: A Guide for B2B Tech Marketers." https://www.a88lab.com/blog/understanding-the-dark-funnel-a-guide-for-b2b-saas-marketers — the dark funnel as a structural (untaggable) feature of B2B buying, not an instrumentation gap (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^8]: Foundra. "The Product Hunt Playbook for First-Time Founders in 2026." https://www.foundra.ai/key-reads/product-hunt-playbook-first-time-founders-2026-after-algorithm-shift — post-algorithm-shift launch-day operations; front-loaded engagement and reply cadence (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending; founder-playbook source, directional).

_last_verified: 2026-07-17_
