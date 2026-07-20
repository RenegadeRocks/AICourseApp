---
type: lesson
block: block-6-launch-monetization
week: week-15
day_of_cycle: 2
day_name: tue
session_slug: plan-product-hunt-social-strategy
tags: [product-hunt, show-hn, launch-mechanics, featured-gate, first-comment, hunter-maker, vote-manipulation, launch-assets, ranking-velocity]
sources:
  - launchpact-ph-algorithm-2026
  - poindeo-ph-upvote-ranking-2026
  - startupik-ph-featured-2026
  - producthunt-help-fair-voting
  - producthunt-community-guidelines
  - favors-ph-honest-guide-2026
  - flowjam-hn-frontpage-2026
  - okara-show-hn-frontpage
  - lucasfcosta-hn-launch
  - hn-guidelines
last_verified: 2026-07-17
word_count_target: 5400
---

# The Product Hunt playbook, honestly, and when a smaller surface fits better

## Why this matters

Yesterday you decided *whether* Product Hunt belongs in your portfolio and at what budget. Today you learn to execute it competently if you chose to run it, so that your one PH day produces the assets and the list it can produce instead of the flat non-event most first launches get. This is a mechanics lesson: how ranking actually works in 2026, what the editorial Featured gate rewards, how the hunter/maker roles and the first-comment function, what a realistic asset kit contains, and, the part that matters most for your long-term account — exactly which gray-area tactics get you unfeatured or banned. It closes with the harder strategic question: for many AI products, a well-run Show HN or a tight community launch fits the buyer better than PH, and you should be able to tell which surface deserves the day.

## Prerequisites

- Monday's launch-surface portfolio, with Product Hunt marked Primary or Secondary and a pass bar set on assets rather than rank. If PH is Skipped for your buyer, read this lesson anyway for the mechanics, the ranking-velocity and first-comment principles transfer to every surface, and spend Saturday's build on your Primary surfaces.
- A launch page with instrumentation ([[05-fri-launch-day-instrumentation|Block 4 Week 10 Friday]]); PH links are nofollow and traffic is spiky, so you need a separate UTM and a separate pass bar for it, per that lesson.

## Layer 1: How Product Hunt ranking actually works in 2026

Forget "get the most upvotes." The 2026 system weighs several signals, and raw upvote count is only one of them.[^1] The mechanics that decide your day:

**Upvote velocity beats upvote volume.** The algorithm rewards early momentum, the first two to four hours disproportionately set your rank for the rest of the day, and it rewards a *steady* rate over an instantaneous spike. A cadence of roughly 25–50 votes per hour reads as organic traction; 400 votes in the first ten minutes reads as coordination and gets discounted.[^1][^2] There is also a time-decay function, much like Reddit's: a vote early in the day is worth more than the same vote at 10pm, which is why launch time (12:01am PT, when the PH day resets) is a real decision.

**Voter credibility is weighted.** An upvote from a three-year-old account with a history of quality contributions carries real weight; an upvote from a Gmail account created ten minutes ago can count for *zero* points.[^1][^3] This single mechanic destroys the entire "recruit a horde of new accounts" strategy, the horde's votes are discounted to nothing, and the coordinated pattern flags your launch for review.

**Comment depth is a first-class signal.** Comment count and *depth* matter, and maker responsiveness matters enormously. One widely-cited pattern from 2026 launch analyses: 40 thoughtful comments can outrank 800 upvotes paired with 20 generic replies; makers who reply to comments within about ten minutes see a measurable ranking boost; and among top-5 finishers, roughly 89% replied to every comment.[^2] The platform is optimizing for genuine engagement, not applause, and it can tell the difference.

**The editorial Featured gate sits on top of all of it.** Since 2024, a human editorial team curates which products appear on the homepage, the mobile app, and the daily newsletter. If you are not Featured, you sit in the "All" tab, which gets a fraction of the traffic, and by founder analyses of 2024–26 data, only about one launch in ten gets Featured, with non-featured launches seeing roughly 70% less traffic regardless of upvote count.[^1][^4] PH's own editorial framing is that Featured products look **Useful, Credible, Novel, and Engaging**. For an AI product in 2026, "Novel" is the hard one: "AI-powered X" is not novel, and the editors have seen a thousand of them. Verticalized, specific, workflow-solving products read as novel; horizontal AI wrappers do not.

The synthesis: PH ranking in 2026 rewards a genuinely engaged first-hour audience of *credible* accounts having *real conversations* with a responsive maker, on a product an editor finds specific enough to feature. Every legitimate tactic below serves that; every prohibited tactic tries to fake it and gets discounted or punished.

## Layer 2: Hunter, maker, and the first comment

**Maker vs hunter.** The *maker* is you, the person who built it. The *hunter* is whoever submits the product. In PH's early years a well-connected hunter with a large following conferred a real distribution boost, and "getting hunted by someone famous" was a strategy. In 2026 that effect is much weaker: the editorial gate and the follower-notification changes mean a big-name hunter no longer reliably moves your rank, and self-hunting (submitting your own product as the maker) is now standard and often preferable because it keeps you in full control of timing, assets, and the first comment.[^5] Unless you have a genuine relationship with a hunter whose audience is *your buyer*, hunt it yourself.

**The first comment (the maker's comment) is your most important asset on the page**, and most first launches waste it. It is the pinned, top-of-thread message that every visitor reads, and it does three jobs: it tells the human story (why you built this, what itch it scratches), it makes a specific ask that is *not* "please upvote," and it opens a conversation the algorithm rewards. A strong 2026 first comment:

- Opens with the *problem*, not the product. One or two sentences of the specific pain your buyer feels.
- Tells a short, true origin story — why *you* built this, which is the "Credible" signal an editor and a reader both look for.
- States what the product does in plain language, then names one honest limitation (what it does *not* do yet). Naming a limitation is counterintuitive and it works: it reads as credible in a feed full of overclaiming, and it invites exactly the "what about X?" comments that feed the depth signal.
- Ends with an engagement ask that is compliant: "I'd love your honest feedback, especially if you've tried to solve [problem] another way, tell me what worked." Not "upvote if you like it."
- Includes an offer that gives the PH audience a reason to become your warm list: an extended trial, a launch-day discount, a founder's-office-hours link. This is how the traffic byproduct converts into the list that is the actual prize (Monday, Layer 2).

Write the first comment *before* you submit. Draft it days ahead, cut it to something a stranger reads in 30 seconds, and have it ready to paste the instant the product goes live, because the first hour is a reply-speed contest and you do not want to be writing it live.

## Layer 3: The realistic asset kit

The PH listing has a fixed set of slots, and each is an asset you prepare in advance. The 2026 kit:

- **Name + tagline (60 chars).** The tagline is the highest-leverage text on the page, it appears in the feed. It should name the specific outcome for the specific buyer, not describe the technology. "Resolve 40% of support tickets before a human sees them" beats "AI-powered support automation." Avoid "AI" in the tagline if you can carry the meaning without it; the word is noise now.[^6]
- **Gallery (first image is the thumbnail).** The first image is what stops the scroll. It should show the *product doing the thing*, with a one-line value overlay, not a logo or an abstract hero. Subsequent images walk through the core workflow. A short demo GIF or video as the second slot substantially raises engagement — PH visitors want to see it work, not read about it.
- **Description.** Short, scannable, benefit-led. The editors read this for the Featured decision, so make the "Novel" and "Useful" case explicit and specific.
- **Topics/categories.** Choose the most specific relevant categories, not the broadest. Vertical categories are less saturated and more likely to surface you.
- **Maker's first comment.** Layer 2. The single most-neglected asset.
- **The offer.** A launch-day discount, extended trial, or bonus, with a clear mechanism to claim it that captures the person into your list.
- **A press/launch page on your own site** with the "featured on Product Hunt" strip ready to populate, because the badge is one of the durable assets you launched *for*.

The kit is also where AI creative tools earn their keep, with a human on judgment: you can generate gallery variations, the demo video, and the copy drafts fast ([[03-wed-the-2026-ai-creative-stack|Block 4 Week 10 Wednesday]] is canonical on the 2026 creative stack), then select and polish. The meta-signal from that lesson applies with force here: PH's audience is unusually good at spotting unreviewed AI slop, and a listing that looks machine-generated undercuts the "Credible" signal you need.

## Layer 4: The gray-area tactics that kill your account

This is the part that protects you for years. PH has a specific, enforced set of rules, and the tactics that look like shortcuts are the ones that get launches unfeatured and accounts restricted.[^3][^7]

**Prohibited, and detected:**
- **Directly asking for upvotes.** PH's community guidelines draw the line precisely: you may invite people to *check it out, try it, and leave honest feedback*; you may **not** ask them to upvote. "Please upvote my launch" in a DM, a tweet, or a Slack is a violation, and coordinated versions of it get the launch unfeatured.[^3]
- **Asking for votes off-platform in a coordinated way.** Vote-for-vote pods, "upvote my launch and I'll upvote yours" exchanges, and paid-vote services are coordinated manipulation. PH's systems flag brand-new accounts, coordinated voting patterns, and purchased votes, discount them to near-zero, and can unfeature the launch entirely.[^3][^7]
- **Fake or purchased accounts.** Beyond being discounted to zero points, these trip the ring-detection systems and can suspend your account.[^3]
- **Branded/company accounts posting or voting.** Accounts flagged as company/brand accounts have limited access and cannot post products, comment, or vote. Launch and comment as *you*, a real person.[^3]

**Legitimate, and effective:**
- **Notifying your own audience that you launched, and inviting them to try it and leave honest feedback.** This is explicitly allowed and is exactly how you get the credible-account first-hour velocity the algorithm rewards. The distinction is "come try this and tell me what you think" (allowed) vs "go upvote this" (prohibited). Say the former, mean it, and let the votes follow from people who actually like it.
- **Building the warm list in advance** (Monday's pre-launch phase, Wednesday's build-in-public engine) so your first-hour audience is real people who genuinely care, not a recruited horde.
- **Replying to every comment fast and substantively.** The single highest-return legitimate tactic, because it feeds the depth-and-responsiveness signal directly.[^2]

The mental model: PH is trying to measure genuine traction. Every legitimate tactic *creates* genuine traction and lets the system see it; every prohibited tactic *fakes* traction and the system is built to catch the fake. In 2026 the detection is good enough that manipulation is negative-expected-value, you risk your account and the launch to buy votes that get discounted to zero anyway. Do not do it, and be wary of any "growth" service that offers to do it for you.

## Layer 5: When a smaller surface fits better: Show HN and the tight community launch

For many AI products, especially developer tools, technical infrastructure, and anything whose buyer is an engineer, a **Show HN** on Hacker News is a higher-signal launch than Product Hunt, and its mechanics are different enough to matter.

**Show HN mechanics in 2026.** Front-page placement is decided by *early vote velocity against a time-decay curve*: a post with 10 upvotes in the first 15 minutes outranks one with 50 spread over six hours, because HN's ranking gravity rises every ~45 minutes.[^8] Practical thresholds from 2026 analyses: you need roughly 8–10 genuine upvotes and 2–3 thoughtful comments in the first 30 minutes to reach the top 10, and roughly 30–50 upvotes in the first hour for a real shot at the front page.[^8][^9] Timing matters: Tuesday–Thursday 8–10am PT (engineers checking before standup) and Sunday evening PT (low competition) are the windows; Friday afternoon and early Monday are graveyards.[^8]

**The rules are stricter and the crowd is harsher.** Show HN is for something people can *actually try* — software they can run, a site they can use, a demo they can see. Blog posts, waitlists, sign-up pages, and newsletters are off-topic and get removed. HN's ring-detection is strong and unforgiving: coordinated voting or paid upvotes will shadowban your URL or ban your domain for life, which is a far heavier penalty than PH's.[^9][^10] And there is an account-credibility gate of its own, a brand-new, zero-karma account posting a Show HN can be auto-removed within minutes, so you warm up the account first (comment substantively, earn 20+ karma) before you post.[^8]

**The payoff and the risk.** A front-page Show HN sends a spike of the most technically-literate visitors on the internet, who will find every flaw and say so publicly. For a ready developer tool that is the best free QA and credibility event available; for an unpolished product it is a public bruising. The first comment matters as much as on PH — write it before you submit, make it the honest technical story with the limitations named, and be present to reply for the first several hours.

**The tight community launch.** For a B2B AI product whose buyer is a support executive or an ops leader (not on HN, and drowning on PH), the highest-signal "launch surface" is often a single relevant community where that buyer already congregates, a Slack, a subreddit, a niche forum — entered under give-before-take rules (Friday's whole lesson). A thoughtful post to 2,000 exactly-right people can out-convert a top-10 PH day of 3,000 mostly-wrong ones. The decision rule: **launch on the surface whose default audience overlaps your buyer, and run the theatrical surfaces only for assets.** This is Monday's portfolio logic applied to the venue choice.

## Worked example: a PH day, hour by hour, for the triage-agent product

Continuing Monday's support-ticket triage agent (buyer: VP of Support). PH is a *Secondary* surface here, the buyer is not a PH regular — run for the badge, reviews, and 30 warm signups, with the primary effort on LinkedIn and outbound.

- **T-7 days:** listing drafted in preview; gallery (product-in-action thumbnail + 3 workflow shots + 20-sec demo GIF); tagline "Resolve 40% of support tickets before a human sees them"; first comment written and cut to 30 seconds; launch-day offer set (60-day extended trial for PH visitors, claim link captures email + role).
- **T-2 days:** notify the 200-person email list and 900 LinkedIn followers that the launch is coming, invite them to *try it and leave honest feedback* on the day (compliant phrasing), and tell them roughly when.
- **12:01am PT (T-0):** launch goes live (self-hunted). Paste the first comment immediately.
- **First 4 hours:** the velocity window. The operator's only job is replying — to every comment on PH within minutes, to every DM, to every LinkedIn reply. No dashboard-watching. Pre-recruited warm list trickles in as genuine 25–50/hr velocity, not a spike.
- **Midday:** post the "we're live" content on LinkedIn and X (Wednesday's sequence), pointing to the *page* (not just the PH listing), timed to the PH momentum.
- **Evening:** keep replying; thank commenters; capture every warm human into the list with their role and context.
- **T+1:** populate the "featured on Product Hunt" strip and any review quotes onto the page; move the warm list into the interview pool and the outreach sequence. The badge and the list, the assets you launched for — are now banked, regardless of where you finished on the leaderboard.

Notice the pass bar was never rank. It was assets and 30 warm humans, both of which are achievable off a modest finish, which is why this launch cannot "fail" in the switch-model sense.

## Runnable experiment: draft the listing and stress-test the first comment

**Task.** Produce three artifacts.

1. **The full asset kit** for your product: name, tagline (≤60 chars, outcome-led, "AI" removed if possible), the ordered gallery shot list (what each image shows), the description, the specific categories, and the launch-day offer with its capture mechanism.
2. **The maker's first comment**, written to the Layer-2 spec: problem-first, true origin story, plain-language what-it-does, one honest limitation named, a compliant engagement ask, and the offer. Cut it until a stranger reads it in 30 seconds.
3. **A compliance self-audit.** List every way you plan to drive first-hour velocity, and label each Allowed or Prohibited against Layer 4's rules. If any line says "ask people to upvote," rewrite it to "invite people to try it and give honest feedback."

Then run an adversarial pass in Claude: paste your first comment and prompt, *"You are a Product Hunt editor deciding whether to Feature this, and a skeptical maker in the comments. As the editor, is this Useful/Credible/Novel/Engaging, where does the Novel claim fail? As the skeptic, what is the sharpest 'what about X' objection my first comment invites, and is that good (it feeds depth) or bad (it exposes a real hole)?"*

**Pass bar.** (1) Your tagline names an outcome a buyer wants, not a technology, and survives the "so what?" test. (2) Your first comment names a real limitation — if it names none, it reads as overclaiming and you have not internalized the Credible signal. (3) Your compliance audit contains zero "ask for upvotes" lines. (4) You can state in one sentence why your product reads as Novel to an editor who has seen a thousand AI wrappers this month; if you cannot, that is the finding, and it is better to learn it today than on the leaderboard. Time: 60–90 minutes.

## Common mistakes experts see

1. **Recruiting new accounts for votes.** Their votes count for near-zero and the coordinated pattern flags you; you spent social capital to buy discounted noise and risk an unfeature.[^1][^3]
2. **Asking for upvotes.** A direct guidelines violation; say "try it and give feedback" instead, which is both compliant and better for the ranking signal.[^3]
3. **A logo or abstract hero as the thumbnail.** The first image must show the product doing the thing; a scroll-stopping thumbnail is worth more than a dozen recruited votes.
4. **Writing the first comment live.** The first hour is a reply-speed contest; a first comment written under pressure is weak exactly when it is most-read. Draft it days ahead.
5. **"AI-powered" in the tagline.** It is noise in 2026 and it fails the Novel test with editors who have seen it a thousand times; lead with the specific outcome.[^6]
6. **Launching to PH when your buyer lives on Show HN or in a Slack.** The saturated-lottery outcome is worse than a tight launch to the right 2,000 people; match the surface to the buyer.[^8]
7. **Show HN with a waitlist or a cold, zero-karma account.** Off-topic posts get removed and unwarmed accounts get auto-flagged; HN's penalties (URL shadowban, lifetime domain ban) are heavier than PH's.[^9][^10]

## Reflection questions

1. Write your product's Novel claim in one sentence, as an editor would need to believe it. If it contains "AI" as the source of novelty, rewrite it around the specific workflow or vertical — what changes?
2. Your first comment invites a "what about X?" objection. Is that objection one you *want* (it feeds depth and you have a good answer) or one you fear (it exposes a real hole)? What does your honest answer tell you about launch-readiness?
3. The gray-area line is "invite to try" vs "ask to upvote." Where, specifically, in your notification plan does that line sit, and are you certain every message is on the right side of it?
4. For your buyer, is Product Hunt or Show HN or a single community the surface whose default audience actually overlaps them? Defend the choice without appealing to which surface is more prestigious.
5. If you finished outside the top 10 with 400 visitors, which of your launched assets would you still have banked, and does that list justify the day? If it does not, your pass bar or your surface choice is wrong.
6. HN's penalty for coordinated voting is a lifetime domain ban. Knowing that, what does the risk/reward of *any* vote coordination look like, on any surface, once you price in the downside?

## My take (reviewer lens)

**Boris Cherny** would flag the tooling-and-automation trap: the ecosystem around launches is full of "PH growth" and "auto-upvote" services, and an operator moving fast will be tempted to bolt one on the way they'd bolt on any tool. His pushback, the one to internalize — is that these tools are not time-savers; they are account-risk generators, because the exact behavior they automate (coordinated votes, off-platform upvote asks, warmed fake accounts) is the exact behavior the detection systems are built to catch, and the failure mode is silent until your launch is unfeatured or your domain is banned. Automate the *asset production* (gallery variants, copy drafts, the demo render) where the cost of a mistake is an ugly image; never automate the *engagement* where the cost of a mistake is your account. **Hamel Husain** would push on Layer 3's demo asset: for an AI product the demo has a specific failure mode, the cherry-picked best run, and a technically-literate PH or HN crowd will assume your GIF is the luckiest output you ever got. His fix: show a *typical* run, or better, show the product handling a hard/edge case honestly, because on these surfaces demonstrated robustness is the Credible signal, and a too-perfect demo reads as a lie. **Seibel** would zoom out and ask whether this whole PH apparatus is worth the day at all for a pre-revenue product, and — consistent with Monday, the honest answer is "only if PH is Secondary and your primary hours went to the twenty customer conversations." If drafting the perfect first comment is stealing time from talking to buyers, you are optimizing the wrong surface.

## Further reading

**Must-read**
- Product Hunt Help Center, "How does Product Hunt ensure fair voting and prevent spam or vote manipulation?" and "Community Guidelines", the actual rules, from the platform, that Layer 4 operationalizes. Read them before you launch.[^3]
- Flowjam / Okara Show HN playbooks, the honest mechanics of the alternative surface, including the account-warming and off-topic rules.[^8][^9]

**Recommended**
- LaunchPact, "Product Hunt Algorithm in 2026", the ranking-signal breakdown behind Layer 1.[^1]
- [[03-wed-the-2026-ai-creative-stack|Block 4 Week 10 Wednesday]], the creative stack that produces your asset kit fast, with the human-on-judgment discipline that keeps it from reading as slop.

**Optional**
- Lucas F. Costa, "How to do a successful Hacker News launch", an operator's first-person Show HN account.[^10]

## Citations

[^1]: LaunchPact, "Product Hunt Algorithm in 2026." https://www.launchpact.io/blog/product-hunt-algorithm — upvote velocity over volume, voter-credibility weighting, comment depth, time-decay, editorial Featured gate (~1 in 10), ~70% non-featured traffic penalty. Corroborated by Poindeo, "How Product Hunt's Ranking Really Works (2026 Edition)." https://poindeo.com/blog/product-hunt-upvote-ranking (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^2]: Poindeo, "What is an upvote? How Product Hunt's Ranking Really Works (2026 Edition)." https://poindeo.com/blog/product-hunt-upvote-ranking — 25–50 votes/hr reads organic; 40 thoughtful comments can outrank 800 upvotes with generic replies; makers replying within ~10 min gain rank; ~89% of top-5 makers replied to every comment; maker first comments averaged ~166% more upvotes. Corroborated by Startupik, "How to Get Featured on Product Hunt and Actually Rank." https://startupik.com/how-to-get-featured-on-product-hunt-and-actually-rank/ (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending; analyst figures, directional).

[^3]: Product Hunt Help Center, "How does Product Hunt ensure fair voting and prevent spam or vote manipulation?" https://help.producthunt.com/en/articles/11869098 and "Community Guidelines." https://help.producthunt.com/en/articles/3615694-community-guidelines — may invite people to try/feedback, may not ask for upvotes; brand-new-account votes discounted to ~0 points; coordinated/purchased votes flagged and can unfeature; branded accounts barred from posting/voting; "Resolving Account Restrictions." https://help.producthunt.com/en/articles/11869621 (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending; primary source, the platform's own help center).

[^4]: Startupik, "How to Get Featured on Product Hunt and Actually Rank." https://startupik.com/how-to-get-featured-on-product-hunt-and-actually-rank/ — editorial curation of homepage/app/newsletter since 2024; "All" tab low traffic; Useful/Credible/Novel/Engaging framing. Corroborated by LaunchPact (above) (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^5]: Favors.dev, "How to Launch on Product Hunt in 2026: The Honest Guide." https://favors.dev/blog/how-to-launch-on-product-hunt-2026 — weakened hunter effect, self-hunting now standard, first-comment importance. Corroborated by Blazon Agency, "How to launch on Product Hunt in 2026: algorithm and strategy." https://blazonagency.com/post/product-hunt-algorithm-2026-software-launch (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^6]: Exponanta, "What's Actually Trending on Product Hunt in 2025–2026." https://exponanta.com/blog/trending-producthunt-categories-for-startups.html — "AI-powered" is table stakes/noise in 2026, vertical specificity reads as novel. Corroborated by Crawlora, "Product Hunt Trends 2013–2026." https://crawlora.net/blog/product-hunt-trends-2013-2026 (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^7]: Blazon Agency, "How to launch on Product Hunt in 2026." https://blazonagency.com/post/product-hunt-algorithm-2026-software-launch — vote pods and paid votes detected, discounted, and penalized with unfeaturing. Corroborated by Product Hunt Help Center (above, [^3]) (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^8]: Flowjam, "Hacker News Front Page in 2026: The Honest Playbook." https://www.flowjam.com/blog/how-to-get-on-the-front-page-of-hacker-news-in-2025-the-complete-up-to-date-playbook — early-velocity ranking with rising gravity, ~8–10 upvotes + 2–3 comments in first 30 min for top 10, ~30–50 upvotes in first hour for front page, Tue–Thu 8–10am PT / Sun evening windows, account-warming requirement. Corroborated by Okara, "How to Get to the Front Page of Hacker News (Show HN)." https://okara.ai/blog/show-hn-front-page (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^9]: Okara, "How to Get on Hacker News Front Page Without Being a Spammer." https://okara.ai/blog/how-to-get-on-hacker-news-front-page-without-being-a-spammer — Show HN must be something people can try (no waitlists/newsletters); ring-detection shadowbans URLs / bans domains for coordinated voting. Corroborated by the official HN guidelines. https://news.ycombinator.com/showhn.html and https://news.ycombinator.com/newsguidelines.html (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending; second corroborant is HN's own primary docs).

[^10]: Lucas F. Costa, "How to do a successful Hacker News launch." https://www.lucasfcosta.com/blog/hn-launch — first-person Show HN account; first-comment and presence discipline; ring-detection warnings. Corroborated by DEV Community, "How to crush your Hacker News launch." https://dev.to/dfarrell/how-to-crush-your-hacker-news-launch-10jk (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

_last_verified: 2026-07-17_
