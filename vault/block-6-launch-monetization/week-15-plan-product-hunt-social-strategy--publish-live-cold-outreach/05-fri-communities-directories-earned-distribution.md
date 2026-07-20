---
type: lesson
block: block-6-launch-monetization
week: week-15
day_of_cycle: 5
day_name: fri
session_slug: publish-live-cold-outreach
tags: [communities, reddit, discord, slack, give-before-take, ai-directories, marketplaces, geo, aeo, answer-engine-optimization, partnerships, compounding-vs-spike]
sources:
  - redship-best-subreddits-ai-2026
  - okara-find-subreddits-2026
  - github-ai-directories
  - aiso-best-directories-2026
  - aitoolscapital-best-places-launch-2026
  - jasper-geo-aeo-2026
  - emarketer-geo-aeo-2026
  - geo-princeton-arxiv-2024
  - frase-aeo-2026
last_verified: 2026-07-17
word_count_target: 5400
---

# Communities, directories, and earned distribution, where AI products actually get discovered in 2026

## Why this matters

The launch surfaces from Monday through Thursday are mostly *spike* surfaces: a burst of attention that decays in days. This lesson covers the *compounding* surfaces, the ones that keep sending buyers for months after launch day, and that increasingly determine whether an AI product is discoverable at all. Three of them matter in 2026: relevant communities (where your buyer already congregates, entered under give-before-take rules), directories and marketplaces (where category-shoppers find AI tools), and the newest and least-understood, AI answer engines (getting *cited* by ChatGPT and Perplexity, the discipline called GEO/AEO). By the end you can seed communities without getting banned, place your product in the directories that matter, run a first GEO pass on your page, and hold a position on whether answer-engine optimization is the new SEO or a hype cycle. Together these convert your launch from a two-day spike into a multi-month tail.

## Prerequisites

- The ethics-and-consent discipline for automated community interaction is canonical in [[03-wed-the-scraping-stack-legally-and-technically|Block 3 Week 8 Wednesday]]; this lesson assumes it when discussing community seeding.
- Marketplace take-rates and distribution surfaces for agent products are canonical in [[04-thu-distribution-surfaces-for-agent-products-in-2026|Block 4 Week 9 Thursday]]; this lesson wikilinks rather than re-teaching them.
- Monday's portfolio (communities/directories/GEO marked as compounding surfaces) and the launch page from [[05-fri-launch-day-instrumentation|Block 4 Week 10]].

## Layer 1: Communities: give-before-take or get banned

Communities — subreddits, Discords, Slacks, niche forums — are the highest-trust launch surface and the easiest to get banned from. The reason both are true is the same: these are real communities of humans with strong norms against self-promotion, so a genuine contribution earns disproportionate trust and a drive-by promotion earns disproportionate punishment. The discipline is give-before-take, and it is not a nicety; it is the entry requirement.

**Reddit's norms, specifically.** Reddit's long-standing self-promotion guidance (often summarized as the "9:1 rule", roughly nine genuine contributions for every one self-promotional post, and self-promotion should be a minor part of your participation) is the baseline, and individual subreddits enforce their own, often stricter, rules.[^1] The 2026-effective pattern for launching a product on Reddit is *not* a launch announcement; it is a **problem story**: you post about the problem you were solving and what you learned, and you link your tool in a comment only after someone asks. AI subreddits in particular are quick to flag hype and self-promo, so you lead with real outputs, not claims, and you read the subreddit's rules and recent thread history before posting anything.[^1][^2] Consumer and "AI for X" applied communities convert better than technical AI subs, where the crowd is builders, not buyers.[^2]

**The general community-seeding rule.** Across Reddit, Discord, and Slack: (1) be a real member before you launch — participate genuinely for weeks, so you have standing; (2) contribute value first and consistently; (3) when you share the product, share it as a *contribution to a conversation* (someone has the problem you solve), not as a broadcast; (4) respect explicit rules and get moderator permission where required; (5) never automate it — automated posting is both against platform norms and a fast route to a ban, echoing the consent-and-automation ethics of [[03-wed-the-scraping-stack-legally-and-technically|Block 3 Week 8]]. The operator who joins a community the week of launch to drop a link is the one who gets removed; the operator who has been genuinely helping for a month gets a warm reception when they finally mention what they built.

For a launch, this means community seeding is a *pre-launch* activity, not a launch-day one. You cannot parachute in on launch day; you earn the standing in the weeks before, then contribute the launch as one more genuine contribution when the day comes.

## Layer 2: Directories and marketplaces: the low-effort compounding tail

AI-tool directories are a low-effort, compounding discovery surface: buyers actively browse them to find tools in a category, and a listing keeps sending trickle traffic for months at near-zero maintenance cost. The 2026 landscape is dense — curated lists like the `best-of-ai/ai-directories` GitHub repo aggregate the directories worth submitting to, and platforms like There's An AI For That, Futurepedia, and dozens of niche category directories host thousands of AI products.[^3][^4] There are two honest caveats. First, many directories confer more *SEO/citation* value (a link, a listing that feeds answer engines — Layer 4) than direct traffic, so treat them as a compounding-discovery and GEO play, not a traffic spike. Second, submission-automation services exist (ListingBott and similar that submit to 100+ directories) but the low-quality directories they hit add little, so a hand-picked set of ten relevant, reputable directories beats a spray to a hundred junk ones, the same precision-over-volume principle as the rest of the week.[^4]

**Marketplaces** are a different animal: a marketplace (an app store, an AI-agent marketplace, a platform's plugin directory) offers built-in distribution in exchange for a take-rate and a dependency. The economics — take-rates, the build-vs-list decision, platform-dependency risk — are canonical in [[04-thu-distribution-surfaces-for-agent-products-in-2026|Block 4 Week 9 Thursday]], and the launch decision is whether a marketplace's built-in demand is worth its cut and its lock-in for your product. For a launch, a marketplace listing can be a real distribution surface if your buyers shop there; wikilink to Week 9 for the take-rate math before committing.

The directory-and-marketplace move for launch week: submit to ten hand-picked relevant directories (an hour of work that pays out for months), and make the marketplace decision on the Week 9 economics. Low effort, compounding return, the opposite profile from the spike surfaces.

## Layer 3: AI answer engines: the new discovery surface

This is the surface most operators are not yet optimizing for, and the one growing fastest. Around 31% of the US population uses generative AI search in 2026, and AI answer engines — ChatGPT Search, Perplexity, Gemini, Google AI Overviews, Copilot — now handle an estimated 12–18% of English-language informational queries.[^5][^6] When a buyer asks ChatGPT "what's the best AI support-triage tool?" or Perplexity "how do I automate tier-1 support tickets?", the engine names some products and not others. Being named is the new front page, and the discipline of getting named is **Generative Engine Optimization (GEO)** / **Answer Engine Optimization (AEO)**.

**The vocabulary, briefly.** The clean distinction from the 2026 literature: *SEO ranks you* (ten blue links), *AEO selects you* (you become the extracted direct answer), *GEO cites and recommends you* (the generative engine names you as a trusted source in its synthesized answer).[^7] In practice the tactics overlap and people use the terms loosely; what matters is the outcome, your product and your content get *cited* by the engines your buyers now ask.

**Why this is not just SEO.** The engines do not all draw from Google's rankings. One 2026 analysis found Google AI Mode and Perplexity each draw roughly 90% of their citations from Google's conventional top-10 results, but ChatGPT pulls only about 30% from that pool — meaning ranking well on Google no longer guarantees you appear where a growing share of buyers get answers, and each engine must be treated somewhat separately.[^6] Only about 11% of domains are cited by *both* ChatGPT and Perplexity, so citation is engine-specific and fragmented.[^8]

**What actually raises citation (the evidence).** The foundational study is Aggarwal et al.'s "GEO: Generative Engine Optimization" (KDD 2024), which tested content modifications against generative engines and found that adding **expert quotes raised source visibility by ~41%, adding statistics by ~30%, and adding citations by ~30%** — while keyword-stuffing, the old SEO reflex, *hurt*.[^9] The practitioner tactics that follow, corroborated across 2026 guides: lead every page with a 2–4 sentence direct answer to the primary question (inverted pyramid, conclusion first); structure content as clear claims with supporting evidence; add Q&A sections, TL;DR summaries, and data tables; make author, date, and update-date visible; and cite credible sources, because the engines favor content that is itself well-sourced.[^7][^10] The through-line: the engines cite content that reads as authoritative, specific, and evidence-backed, which is, again, the substance-over-slop pattern of the entire week, now enforced by a machine reader instead of a human one.

**How to measure it.** GEO is measurable: run a fixed set of buyer queries through ChatGPT, Claude, Perplexity, and Gemini weekly and log which sources each cites. First citations typically appear in Perplexity (it indexes fastest), with ChatGPT and AI Overviews following, and a focused effort tends to show measurable citation gains by week 8–10.[^7] Dedicated trackers (Profound, Otterly.ai, Peec AI, and others, roughly €50–150/month) automate this, but at launch a manual weekly query log is enough to start.[^10] For launch week, the GEO move is a *first pass*: restructure your launch page with a direct-answer intro, add real statistics and one expert-quotable line, ensure dates and sources are visible, and start the weekly citation log so the compounding begins.

## Layer 4: The controversy: is answer-engine optimization the new SEO, or a hype cycle?

The week's Friday debate. Both sides have real evidence.

**The "GEO is the new SEO, adapt now" side** argues that the shift is structural and fast: a third of the population already uses generative search, informational query share is moving to the engines, ranking on Google no longer guarantees visibility where buyers actually ask, and the operators who establish citation authority early will compound the same way early SEO winners did. In this reading, GEO is not optional for a content-driven business in 2026, and a launch that ignores it forfeits the fastest-growing discovery surface.[^5][^6]

**The "GEO is overhyped and unstable" side** argues that the discipline is a vendor-manufactured category (a wave of GEO tools all launched to sell a problem), that citation is so fragmented and engine-specific (only 11% domain overlap between ChatGPT and Perplexity) that optimizing for it is chasing a moving target, that the engines change their citation behavior constantly so any "optimization" is transient, and that for most products the honest answer is to keep doing good SEO and substantive content, which feeds the engines anyway — rather than to buy a GEO tool and a new vocabulary. In this reading GEO is real but immature, and the operator effort is better spent on the surfaces that convert today.

**My position:** GEO is real, early, and worth a *first pass but not a large budget* at launch. The evidence that generative search is a growing discovery surface is strong; the evidence that a specialized GEO *tooling* investment pays off at launch scale is weak. The resolution is that the tactics that raise citation — direct answers, real statistics, expert quotes, visible sourcing, well-structured evidence — are the *same* tactics that make good, credible content for humans, so you get the GEO benefit as a byproduct of writing substantively, which you were doing anyway. Do the first pass (restructure the page, start the citation log); skip the €150/month tracker until you have revenue and evidence it moves the needle. The "new SEO" camp is right about direction and premature about tooling urgency; the "hype cycle" camp is right about tooling and wrong to dismiss the direction. As with cold outreach and social, the winning move is substance, which the engines reward for the same reason humans do.

## Layer 5: Spike vs compounding: designing the whole distribution

Step back and see the shape of the full launch distribution. The surfaces divide cleanly:

- **Spike surfaces** (Product Hunt, Show HN, the launch-day social sequence, the outreach burst): concentrated attention that decays in days, producing the credibility assets and the warm list. High effort, front-loaded return.
- **Compounding surfaces** (communities you have standing in, directories, GEO/AEO citation, partnerships, evergreen content): lower per-unit attention that keeps trickling for months. Lower effort per unit, back-loaded return.

The strategic error is running only spikes — launching loud, decaying to zero, and having to launch loud again to get any traffic (the faucet problem from [[03-wed-building-in-public|Block 1 Week 2]]). The compounding surfaces are what make the launch a motion instead of a moment (Monday): while the spike surfaces manufacture the launch day, the compounding surfaces build the tail that is still sending buyers in month three. A well-designed launch spends launch *day* on the spikes and launch *week* seeding the compounders, the community standing built in advance, the ten directory submissions, the GEO first pass, the one or two partnership conversations, so that when the spike decays, the tail is already growing.

**Partnerships** deserve a line: a genuine integration or co-marketing relationship with a product your buyer already uses is a compounding surface that can outproduce every spike, because it borrows an established audience continuously rather than once. For launch week, a partnership is usually a conversation you *start*, not close, but starting it during the launch's momentum is the right time.

## Worked example: the triage-agent compounding plan

Continuing the support-triage agent. The compounding-surface plan, run alongside the spikes:

- **Communities:** the operator has been a genuine member of a customer-support Slack and a SaaS-operators subreddit for two months (standing earned in advance). Launch-week contribution: a problem-story post in each — "here's what I learned about tier-1 ticket volume building a triage tool", with the product linked only when asked, per the 9:1 and subreddit-specific rules. Applied "AI for support" communities, not technical AI subs.
- **Directories:** ten hand-picked relevant directories (customer-support-tool and AI-tool categories), submitted in an hour. No spray to junk directories.
- **GEO first pass:** the launch page restructured with a direct-answer intro ("[Product] resolves tier-1 support tickets automatically by…"), a real statistic (the 14h→1.1h result), one expert-quotable line, visible author/date, and cited sources. A weekly log started for the queries "best AI support triage tool" and "how to automate tier-1 support tickets" across ChatGPT, Perplexity, and Gemini.
- **Partnership:** one conversation started with a help-desk platform whose users are the exact buyer, exploring an integration listing.
- **Marketplace:** decision deferred to the Week 9 take-rate math ([[04-thu-distribution-surfaces-for-agent-products-in-2026|Block 4 Week 9]]).

Launch day is the spikes; launch week seeds the compounders; month three, the directories and citations and the community standing are still sending the right buyers, at near-zero ongoing cost.

## Runnable experiment: seed one community and run the GEO first pass

**Task.** Produce three artifacts.

1. **A community-seeding plan** for two communities where your buyer congregates: name each, your current standing (are you a genuine member, or would you be parachuting in?), the specific give-before-take contribution you will make, the subreddit/Discord/Slack rule you checked, and the problem-story framing for how you will mention the product. If your standing is "none," your plan's first step is joining and contributing for weeks *before* launch — write that honestly.
2. **Ten directory submissions**, hand-picked and relevant (not a spray). Name each and why it fits your category.
3. **A GEO first pass on your launch page**: rewrite the page intro as a 2–4 sentence direct answer to your buyer's primary question; add one real statistic and one expert-quotable line; ensure author/date/sources are visible. Then define five buyer queries and log which products ChatGPT and Perplexity currently cite for them (your baseline).

Then run the citation baseline: actually ask ChatGPT and Perplexity your five queries and record who they name. This is your week-0 GEO measurement.

**Pass bar.** (1) Your community plan is honest about standing — if you have none, the plan says "earn it first," not "post on launch day." (2) Your directories are ten relevant ones, not a hundred junk ones. (3) Your page intro answers the buyer's question in the first two sentences, and you added a real statistic (not a made-up one). (4) You have a week-0 citation baseline for five queries, so you can measure GEO progress at week 8–10. Time: 60–90 minutes.

## Common mistakes experts see

1. **Parachuting into a community on launch day.** No standing, instant removal; community seeding is a pre-launch activity — earn standing for weeks, then contribute the launch.[^1]
2. **A launch announcement instead of a problem story on Reddit.** AI subs flag hype fast; post the problem and what you learned, link only when asked.[^2]
3. **Spraying a hundred junk directories.** Ten relevant reputable directories beat a hundred junk ones; precision over volume, same as everywhere this week.[^4]
4. **Ignoring answer engines entirely.** A third of buyers now ask ChatGPT/Perplexity; a launch page with no direct-answer intro or evidence forfeits the fastest-growing discovery surface.[^5][^9]
5. **Buying a GEO tool before you have revenue.** The tactics that raise citation are the same as writing substantive content; do the first pass free, defer the €150/month tracker until it is proven to move the needle.
6. **Running only spikes.** Launch loud, decay to zero, repeat, the faucet trap; seed the compounding surfaces so the tail grows while the spike fades.[^3]
7. **Automating community posting.** Against norms and a fast ban, and it violates the consent-and-automation ethics from [[03-wed-the-scraping-stack-legally-and-technically|Block 3 Week 8]]; community work is manual and genuine or it backfires.

## Reflection questions

1. In which communities do you have *genuine standing* today, and in which would you be parachuting in? What does the honest answer imply about how far in advance your launch really needed to start?
2. Ask ChatGPT and Perplexity your buyer's top query right now. Who gets named? What would it take for your product to be in that answer, and is any of it achievable by launch?
3. The "GEO is the new SEO" and "GEO is hype" camps look at the same 31%-of-buyers-use-generative-search stat. What does each conclude, and which does your buyer's actual behavior support?
4. Which of your launch surfaces are spikes and which are compounders? If you listed only spikes, what will send traffic in month three?
5. The GEO study found expert quotes raise citation ~41% and keyword-stuffing hurts. What does that tell you about whether the engines reward the same thing humans do, and what does that imply for how much specialized "optimization" you actually need?
6. A partnership with a product your buyer already uses could outproduce every spike. Which specific product, and what is the one conversation you could start during the launch's momentum?

## My take (reviewer lens)

**Jerry Liu** would push on the GEO section from the retrieval-systems angle: the answer engines are RAG systems, and "getting cited" is really "getting retrieved and then judged authoritative by the generator," so the durable GEO strategy is less about copywriting tricks and more about being genuinely the best-sourced, most-structured content on your specific question, because as the engines' retrieval and ranking improve, the surface-level optimizations decay and only real authority survives. His caveat sharpens the lesson's "substance is the strategy" position: the operators gaming citation with quote-stuffing today are optimizing a proxy the engines will close, exactly as Google closed keyword-stuffing. **Ethan Mollick** would add that the community and answer-engine surfaces are where AI adoption research shows buyers *actually* form opinions now — in peer conversations and in AI-summarized answers, not in ad impressions, so the lesson's compounding surfaces are arguably becoming the *primary* surfaces, and the spike surfaces the secondary ones, which is a bigger reframing than the lesson fully commits to. **Seibel** would, characteristically, warn against the operator spending launch week building an elaborate GEO and directory apparatus while zero customers have paid, the compounding surfaces are real but they compound *slowly*, and a pre-revenue founder needs the fast signal of the spike surfaces and the direct conversations more than a citation that might appear in week 10. The synthesis the lesson holds: seed the compounders cheaply (an hour of directories, a free GEO first pass, community standing you were building anyway) but do not let them absorb the launch-week hours that belong to talking to buyers.

## Further reading

**Must-read**
- Aggarwal et al., "GEO: Generative Engine Optimization," KDD 2024 (arXiv:2311.09735), the foundational evidence for what actually raises answer-engine citation. Read §5.[^9]
- [[04-thu-distribution-surfaces-for-agent-products-in-2026|Block 4 Week 9 Thursday]] — marketplace take-rates and distribution-surface economics; the canonical home for the marketplace decision.

**Recommended**
- eMarketer, "FAQ on GEO and AEO: Where AI search and SEO overlap in 2026", the citation-source and adoption data behind Layer 3.[^6]
- The `best-of-ai/ai-directories` GitHub list, a hand-pickable set of directories worth submitting to.[^3]

**Optional**
- RedShip / Okara subreddit guides, for finding the applied "AI for X" communities where your buyer actually is.[^1][^2]

## Citations

[^1]: RedShip, "Best Subreddits for AI Tools & Products in 2026." https://redship.io/best-subreddits-for/ai — Reddit as highest-trust/easiest-to-ban surface; problem-story-not-announcement pattern; read rules and thread history first. Corroborated by Reddit's own self-promotion guidance ("9:1"/reddiquette) as documented in launch guides. Corroborated by Okara, "7 Best AI Tools to Find Subreddits in 2026." https://okara.ai/blog/best-ai-tool-to-find-subreddits (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^2]: Okara, "7 Best AI Tools to Find Subreddits in 2026." https://okara.ai/blog/best-ai-tool-to-find-subreddits — AI subs flag hype/self-promo fast; lead with real outputs; consumer/"AI for X" communities convert better than technical AI subs. Corroborated by RedShip (above) (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^3]: best-of-ai, "ai-directories" GitHub list. https://github.com/best-of-ai/ai-directories — curated aggregation of AI-tool directories to submit to. Corroborated by tomrzv/AI-Directories. https://github.com/tomrzv/AI-Directories (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending; community-maintained lists).

[^4]: AISO, "12 Best AI Tools Directories to Submit Your SaaS & Startup (2026 List)." https://aiso.blog/best-directories-ai-tools/ — directory landscape, ListingBott-style submission automation and its low-quality-directory caveat. Corroborated by AI Tools Capital, "Best Places to Launch Your AI Tool in 2026: 10 Platforms Compared." https://aitoolscapital.com/blog/best-places-to-launch-your-ai-tool-2026/ (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^5]: Jasper, "What is Generative Engine Optimization? GEO vs AEO vs SEO Guide 2026." https://www.jasper.ai/blog/geo-aeo — GEO definition; ~31.3% of US population using generative AI search in 2026; SEO-ranks/AEO-selects/GEO-cites framing. Corroborated by eMarketer (below, [^6]) (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^6]: eMarketer, "FAQ on GEO and AEO: Where AI search and SEO overlap in 2026." https://www.emarketer.com/content/faq-on-geo-aeo--where-ai-search-seo-overlap-2026 — ~31.3% using generative search; Google AI Mode/Perplexity ~90% citations from Google top-10 vs ChatGPT ~30%. Corroborated by Jasper (above) (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^7]: Surmado, "Answer Engine Optimization: The Complete AEO and GEO Guide for 2026." https://www.surmado.com/blog/answer-engine-optimization-aeo-geo-guide — direct-answer inverted-pyramid intros, Q&A/TL;DR/tables, visible author+date, cited sources; weekly citation-monitoring method; week 8–10 measurable gains. Corroborated by Frase, "Answer Engine Optimization: Complete AEO Guide [2026]." https://www.frase.io/blog/what-is-answer-engine-optimization-the-complete-guide-to-getting-cited-by-ai (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^8]: Naypache Studio, "GEO Guide 2026." https://www.naypache-studio.com/insights/generative-engine-optimization-guide-2026 — only ~11% of domains cited by both ChatGPT and Perplexity; citation is engine-specific/fragmented. Corroborated by eMarketer (above, [^6]) (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^9]: Aggarwal, Murahari, Rajpurohit, et al., "GEO: Generative Engine Optimization," KDD 2024, arXiv:2311.09735, §5. https://arxiv.org/abs/2311.09735 — expert quotes ~+41%, statistics ~+30%, citations ~+30% source visibility; keyword-stuffing hurts. Corroborated by eMarketer's report of the same Princeton-study figures (above, [^6]) (search-verified 2026-07-17; primary source is the arXiv paper).

[^10]: Frase, "Answer Engine Optimization: Complete AEO Guide [2026]." https://www.frase.io/blog/what-is-answer-engine-optimization-the-complete-guide-to-getting-cited-by-ai — citation-tracking tools (Profound, Otterly.ai, Peec AI) ~€50–150/mo; first citations in Perplexity. Corroborated by Surmado (above, [^7]) (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

_last_verified: 2026-07-17_
