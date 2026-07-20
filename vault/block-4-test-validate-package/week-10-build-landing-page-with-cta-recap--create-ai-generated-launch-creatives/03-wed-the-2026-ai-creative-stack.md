---
type: lesson
block: block-4-test-validate-package
week: week-10
day_of_cycle: 3
day_name: wed
session_slug: create-ai-generated-launch-creatives
date_due: 2026-07-22
tags: [ai-creative-stack, image-generation, video-generation, voiceover, midjourney, ideogram, recraft, veo, runway, kling, elevenlabs, sora-shutdown, ai-slop, authenticity-premium, brand-consistency, commercial-licensing]
sources:
  - laozhang-best-ai-video-2026
  - buildmvpfast-video-api-pricing-2026-07
  - openai-help-sora-discontinuation
  - the-decoder-sora-two-stage-shutdown
  - techxplore-sora-shutdown-economics
  - midjourney-docs-comparing-plans
  - eesel-midjourney-pricing-2026
  - elevenlabs-pricing
  - bigvu-elevenlabs-pricing-2026
  - nomadlab-image-generators-2026
  - buildmvpfast-image-generation-2026-07
  - iab-ai-ad-gap-widens
  - marketingbrew-harris-ai-fatigue
  - forbes-coca-cola-ai-ad-2025
  - nbcnews-coca-cola-ai-ad-2024
  - influencers-time-ai-backlash
  - stateofbrand-anti-ai-positioning
  - uscopyright-part2-copyrightability-2025
last_verified: 2026-07-17
word_count_target: 5000
---

# The 2026 AI creative stack — what to use, what it costs, what you may legally do with it, and why "obviously AI" is now a positioning error

## Why this matters

Thursday you run a production pipeline and Saturday you ship a launch kit: hero visuals, a demo video, ad variants, OG images, maybe a voiceover. Today you choose the machines, and the choice has three dimensions operators routinely collapse into one. **Capability** (which tool renders legible text, which video model holds a product shot steady) changes quarterly and is the least important of the three. **Commercial terms** (whose license actually permits your use, at your revenue, without a watermark) is where careless operators accumulate silent liabilities. And **perception** is the one that decides conversion: the AI-slop backlash of 2024–2026 has matured from grumbling into measured consumer behavior and named anti-AI brand campaigns, which means visibly-AI creative is no longer a neutral cost-saving choice. It is a positioning statement, and for you, a seller of AI agents, it is a *product* statement: buyers will read your creative quality as a proxy for your agent quality.

By tonight you will have selected a stack (one image tool, one video path, one voice tool, plus the copy model you already have), verified its commercial terms against your actual situation, and written the one-page brand-consistency spec that keeps every generated asset looking like one company made it.

## Prerequisites

- The design-system vocabulary from [[03-wed-design-system-literacy|Block 2 Week 3 Wednesday]]: the seven variables (type, color, spacing, density, motion, imagery, voice) are today's control surface for brand consistency.
- The audience-positioning work from [[04-thu-niche-as-a-hypothesis|Block 1 Week 2]]: whether obviously-AI creative hurts you depends on who you sell to, and that lesson is where you decided who that is.
- A budget number for launch creative. Write it down now; the stack selection exercise needs it. For most solo operators it should be under $150/month.

## Layer 1 — The stack, mapped and priced (July 2026)

Fast-moving territory; everything below is search-verified against at least two independent sources as of 2026-07-17, and the correct habit is to re-verify terms the week you subscribe, from the vendor's own pricing page.

### Image

- **Midjourney** ($10 Basic / $30 Standard / $60 Pro / $120 Mega per month): still the aesthetic-quality leader for mood, texture, and cinematic stills; still comparatively weak at in-image text.[^1] The commercial fine print is Layer 2's subject.
- **Ideogram** (freemium, paid tiers): the text-rendering leader. For assets where the words are *in* the image (ad cards, social graphics, OG images with headlines), it is the tool practitioners trust to ship without a design-tool touch-up pass.[^2]
- **Recraft** (freemium, paid tiers): the design-tool-shaped one. Native SVG vector output that survives Illustrator/Figma, and brand-style features: upload reference assets and hold palette and line style consistent across batches.[^2] For a launch kit that needs twenty assets that match, this is the consistency workhorse.
- **Frontier-lab image models** (GPT-Image class, Gemini-family image generation, FLUX.2): strong instruction-following and editing; useful when the asset is "modify this screenshot" rather than "imagine this scene."[^2]

The practitioner pattern worth stealing, reported across several 2026 tool roundups: **base image from the aesthetic leader, text pass in Ideogram or a design tool, vector/brand assets in Recraft.**[^2] One tool rarely wins all three jobs.

### Video

- **Google Veo 3.1**: current quality benchmark for short generated clips with audio; API-priced per second of output (fast-mode rates around $0.15/second, standard higher), which makes cost scale with ambition in a way subscription tools do not.[^3]
- **Runway (Gen-4.5)**: the editor-shaped choice; credit-based plans from roughly $12/month (Standard, ~625 credits) to $76/month (Pro), with commercial use on paid plans.[^3]
- **Kling (2.x/3.0)**: the budget entry among capable models, plans from around $10/month, popular for product-style shots.[^3]
- **The tool that is not on the list: Sora.** Layer 3.

For *your* launch the decision is simpler than the model race implies, because (Thursday's argument) the core demo video of an agent product should be screen capture of the real product, with generated video demoted to b-roll. Budget accordingly: most Week 9 launches need $0–30 of generated video.

### Voice and copy

- **ElevenLabs**: Free tier exists but **carries no commercial rights**; Starter ($6/month, ~30 minutes TTS) is the commercial floor; Creator ($22) and Pro ($99) add professional voice cloning and higher-quality API audio.[^4] For a launch voiceover, Starter or Creator covers it.
- **Copy**: you already own the best tool. Claude (Sonnet 5 as the current default tier, Fable/Mythos 5 above it) drafts variants; your Monday substantiation discipline edits them.[^5] No additional spend.

A note on the meta-pattern: every capable tier is now cheap. A complete launch-kit stack (Midjourney Basic + Ideogram/Recraft freemium + Runway Standard + ElevenLabs Starter) runs about $30–50/month. Cost stopped being the constraint sometime in 2025. Taste, terms, and consistency are the constraints, which is why the rest of today is about those.

## Layer 2 — The commercial terms that actually bite

Three classes of trap, all live in July 2026:

**Revenue-threshold clauses.** Midjourney's terms require companies with **gross annual revenue above $1M to be on Pro or Mega** for commercial use; Basic/Standard commercial rights only cover organizations under that threshold.[^1] Irrelevant to you today, sharply relevant to your *client work*: if you produce launch creative for a funded client on your $10 Basic plan, the license gap is yours. Also note stealth mode (private generations) starts at Pro; on cheaper tiers your client's unannounced product imagery sits in a public feed.

**Free-tier commercial exclusions and watermarks.** ElevenLabs' free tier excludes commercial use outright.[^4] Video tools watermark free output and generally reserve commercial rights for paid plans.[^3] The operational rule: **the plan you prototype on is not the plan you ship on**; before an asset goes into the launch kit, its generation account must be a paid tier whose terms you have read that month.

**The copyright hole under everything.** The US Copyright Office's Part 2 report on copyrightability (January 2025) settled the domestic framework: purely AI-generated output, prompted but not meaningfully authored by a human, is **not copyrightable**; protection attaches only to human contributions, such as creative selection, arrangement, or substantial modification, and applicants have a duty to disclose more-than-de-minimis AI-generated material when registering.[^6] Consequences for your launch kit, in descending order of practical weight: (1) your raw generated hero image is probably unprotectable, meaning a competitor can copy it without infringing *your* rights (the tool vendor's license governs what *you* may do, not what others may not); (2) your composited page, with human layout, copy, and arrangement, is protectable as a whole; (3) if any single creative asset becomes genuinely valuable to the business, that is your signal to commission or substantially rework it by hand. For launch-week ad variants with a two-week shelf life, none of this matters. Know which of your assets it matters for.

## Layer 3 — The Sora shutdown, read as an operator lesson

On March 24, 2026, OpenAI announced it was discontinuing Sora; the consumer app and sora.com closed April 26, 2026, and the API follows on September 24, 2026, with account data deleted after each stage.[^7] The reported economics explain it: operating costs around $1M per day against roughly $2.1M of *lifetime* in-app purchase revenue, with downloads collapsing from a 3.3M monthly peak (November 2025) to about 1.1M by February 2026.[^8]

Three lessons, in ascending order of importance for you:

1. **Consumer AI video was a subsidy, and subsidies end.** Per-generation costs in video are brutal; any tool whose price does not visibly cover its inference is a countdown. When choosing tools for anything durable, prefer vendors whose unit economics you can at least squint at (API per-second pricing is, perversely, a *good* sign: it means the price is real).
2. **Export discipline is not paranoia.** Sora users had a deletion deadline for their own generation history. Your launch kit's source files, prompts, and outputs belong in your repository, not in a vendor's workspace. Thursday's pipeline bakes this in: every accepted asset gets archived with its prompt and settings the day it is accepted.
3. **Don't confuse model quality with product durability.** Sora's model was excellent; the product died anyway. Stack selection is a bet on the *business* attached to the model. This is the same build-on-solid-ground judgment you exercised choosing runtimes in [[05-fri-reliability-engineering-for-unattended-agents|Block 3 Week 8]], applied to creative tooling.

## Layer 4 — The slop backlash is a positioning problem, and you are unusually exposed

[[01-mon-why-brand-matters-for-ai-consultants|Block 1 Week 2]] taught the authenticity mechanics of personal brand in the AI era; that remains the canonical home. What has changed since, and what today adds, is that the backlash now has numbers, named casualties, and a counter-positioning industry.

**The evidence, mid-2026.** The IAB's research finds, for the second consecutive year, that Gen Z and Millennial consumers feel materially less positive about AI-generated advertising than advertising executives believe they do; the industry is measurably miscalibrated about its own audience.[^9] Harris Poll data presented around Cannes found a majority of Americans reporting AI fatigue and reduced trust in AI-generated ads.[^10] Survey compilations put the headline behavioral numbers in the same direction: consumers reporting they trust brands less when they suspect an ad is AI-made (one widely-cited 2026 figure: 63 percent), and roughly half saying they disengage from content they suspect is synthetic.[^11] Hold the specific percentages loosely (methodologies vary, and backlash-measuring surveys have their own selection effects), but the direction is corroborated across every independent source this lesson could find, and the case studies are not survey artifacts: Coca-Cola's AI-generated Christmas campaigns drew broad public backlash in 2024 and again in 2025, with sentiment tracking showing positive reactions dropping by more than half post-launch;[^12] McDonald's Netherlands pulled an AI-generated holiday ad after public reaction;[^11] and by early 2026, brands including Aerie and Equinox were running explicitly *anti*-AI campaigns, making "no AI here" itself a market position.[^13]

**The nuance the backlash coverage misses.** Consumers are not reacting to AI; they are reacting to *slop*: content whose visible cheapness signals that the brand did not care enough to have a human look. Meta reports over 8 million advertisers using its AI creative tools, and its measured performance lifts (Thursday's topic) are real; the overwhelming majority of AI-assisted creative passes unnoticed because someone with taste directed and reviewed it.[^14] The backlash punishes *detectability plus laziness*, not assistance. That distinction is the whole game: AI for volume, humans for judgment, and nothing ships that a human with taste has not accepted. (This is the same human-in-the-loop shape you built for agent outputs; your creative pipeline gets the same QA gate your agent gets, and Thursday builds it.)

**Why you specifically cannot punt.** You sell AI systems. Your creative *is* a product demo, whether you intend it or not. If your launch imagery has six-fingered hands and your ad copy reads like unedited model output, the buyer's inference is not "they saved money on marketing"; it is "this is the quality bar they ship at." Conversely, creative that is obviously AI-assisted *and obviously directed* (consistent brand system, clean type, no artifacts, honest disclosure where required) demonstrates exactly the competence you are selling. For an agent vendor, the creative pipeline is a portfolio piece.

**The positioning decision.** Three defensible stances for your launch, pick one deliberately: (a) **Invisible assistance** (default): AI throughout production, human direction and QA, no aesthetic signaling either way; (b) **Demonstrative assistance**: for audiences of builders and early adopters, visibly AI-produced creative framed as capability proof ("this launch kit was produced by the pipeline we sell"); (c) **Human-made as premium signal**: for slop-fatigued audiences (consumer, creative-industry, or brand-sensitive enterprise buyers), deliberately hand-made creative as differentiation, per the anti-AI campaign trend.[^13] What is not defensible is the unchosen default: visibly AI, unacknowledged, unreviewed. That is the slop quadrant, and in 2026 it converts negatively.

## Layer 5 — Brand-consistency systems: making twenty assets look like one company

The launch kit's failure mode is not one bad asset; it is twenty good assets that do not match. Generated imagery drifts: every prompt is a fresh sample from a distribution, and without constraints your hero, your OG image, and your five ad variants will each look like a different agency made them. The fix is a **brand spec that travels with every prompt**, which is exactly your Week 3 design-system literacy converted into generation constraints:

1. **Palette lock.** Three hex values (primary, accent, neutral) stated in every image prompt and checked in QA. Generated assets that fight your page's palette make the page look wrong even when each asset is individually fine.
2. **Style anchor.** One reference mechanism per tool: Midjourney style references carry an aesthetic across generations; Recraft's brand-style upload does it from your actual assets.[^1][^2] Pick one anchor image set (3–5 exemplars) and reuse it everywhere; never freestyle the aesthetic per asset.
3. **Type stays out of the model, usually.** Text-in-image goes through Ideogram or gets set in your design tool over a clean generated background. Your wordmark and UI screenshots are never generated; they are real artifacts composited in.
4. **Imagery rules, written down.** Subjects, moods, what never appears (the seven-variables "imagery" and "voice" rows from [[03-wed-design-system-literacy]], made explicit). Example: "isometric illustrations of workflows, no photorealistic humans, no robot imagery, no blue-gradient brains." The negative list matters more than the positive one; it is what keeps you out of the stock-AI-look attractor basin.
5. **One brief format for every asset.** Saturday's code-lab generator emits briefs that carry the palette, anchor, and rules into every prompt mechanically, so consistency stops depending on your memory at 11pm on launch night.

## Runnable experiment — select and verify your stack

**Task.** (a) Choose your stack: one image tool, one video path (screen-capture-first counts, and should usually win), one voice tool or "none," within your written budget. (b) For each chosen tool, find and read the *current* commercial-use terms on the vendor's own site, and write a three-line terms note: what plan you need, what you may ship, what surprised you. (c) Write your one-page brand spec (palette, anchor set, type rule, imagery rules, negative list). (d) Generate one test pair in your image tool: the same asset concept once *with* the brand spec applied and once freestyle.

**Pass bar.** (1) The terms notes cite the vendor page you read, dated today; if any note says "couldn't find clear terms," the tool is out of the stack, which is the lesson working. (2) The stack's monthly cost is inside your written budget. (3) A third party shown your with-spec and freestyle test images can identify which one belongs to your brand's page (show them the page too). (4) Your positioning stance from Layer 4 is written in one sentence at the top of the brand spec, with the audience-based reason. Time budget: 75 minutes plus generation time.

## Common mistakes experts see

1. **Choosing tools by leaderboard instead of by job.** The best model at cinematic beauty is the wrong tool for a text-heavy ad card; the roundup-verified pattern is a small portfolio of specialists.[^2]
2. **Shipping from the free tier.** Watermarks, missing commercial rights (ElevenLabs free is the canonical trap), and public generation feeds.[^4]
3. **Ignoring revenue-threshold clauses when doing client work.** Your Basic plan does not cover your $2M-revenue client's campaign.[^1]
4. **Treating raw generations as owned IP.** Post-Part 2, purely generated assets are unprotectable; plan around it for anything durable.[^6]
5. **Per-asset freestyling.** Twenty aesthetics, one page. Consistency is a system property; without a spec, drift is the default.
6. **The unchosen slop quadrant.** Visibly AI, unreviewed, unacknowledged, aimed at an audience that punishes it. Every part of that sentence was a decision someone declined to make.
7. **Building brand assets inside a tool with no export discipline.** Sora's users got a deletion deadline; yours is a fire drill you can skip by archiving prompts and outputs on acceptance.[^7]

## Reflection questions

1. Which quadrant does your *buyer* live in: slop-fatigued or capability-curious? What evidence do you actually have, and what would Thursday's ad variants let you test about it?
2. The "demonstrative assistance" stance (this kit was made by the pipeline we sell) is strongest when the kit is excellent and catastrophic when it is mediocre. What is your honest current assessment, and who could tell you the truth about it?
3. If your hero image is legally uncopyrightable, what actually protects your launch's visual identity? (Hint: consistency and speed are defenses that do not depend on copyright.)
4. Veo-class API pricing means a 60-second fully-generated launch film costs real money per attempt; screen capture costs your time. At your current hourly value from the Week 9 packaging work, where is the crossover, honestly computed?
5. Coca-Cola repeated its AI campaign in 2025 *after* the 2024 backlash, presumably with eyes open. Steelman that decision. What might their data show that the sentiment coverage misses, and what would it take for your launch to have that kind of data?
6. Which single asset in your launch kit would benefit most from being conspicuously human-made? What would it cost?

## My take (reviewer lens)

**Ethan Mollick** would endorse the backlash nuance but sharpen it with his adoption research: the measurable gap is between organizations that *use AI with expertise* and those that use it as a substitute for expertise, and he would warn that this lesson's "human with taste reviews everything" rule quietly assumes you have taste, which for many technical operators is the actual missing capability; his fix would be to borrow taste explicitly (copy a named reference aesthetic wholesale, per Week 3's wholesale-adoption argument) rather than trust your eye. **Mira Murati's** lens (customization beats generality) reframes Layer 5: brand consistency is a customization problem, and the durable solution is not prompt discipline but tuned or reference-conditioned models that *cannot* drift off-brand; Recraft's brand styles are the consumer-grade version of that thesis, and she would bet the serious version (brands running their own tuned image models) eats this whole layer within two years. **Jeremy Howard** would push back on the stack maximalism: for a first launch, one $10 image plan, screen capture, and no voiceover is probably the right stack, and the hours this lesson could seduce you into spending on creative would return more as five more customer conversations; the anti-hype read of the slop backlash is that *plain* pages with true sentences are converting fine. He is right often enough that the Saturday build caps creative time by milestone.

## Further reading

**Must-read**

- US Copyright Office, *Copyright and Artificial Intelligence, Part 2: Copyrightability* (January 2025) — the report itself, sections II–IV; the human-authorship framework every asset decision sits on.[^6]
- IAB, "The AI Ad Gap Widens" — the exec-vs-consumer miscalibration data; short and uncomfortable.[^9]

**Recommended**

- The Decoder, "OpenAI sets two-stage Sora shutdown" — the cleanest factual account of the shutdown and its economics.[^7]
- Midjourney docs, "Comparing Midjourney Plans" — read the commercial-terms rows as a template for how to read *any* creative tool's terms.[^1]

**Optional**

- Kate O'Neill, "The Authenticity Premium" — the strongest essay-form version of the backlash-as-opportunity argument.[^11]
- BuildMVPFast's July 2026 image and video API pricing trackers — useful running comparison tables; verify against vendors before spending.[^2][^3]

## Citations

[^1]: Midjourney documentation. "Comparing Midjourney Plans." https://docs.midjourney.com/hc/en-us/articles/27870484040333-Comparing-Midjourney-Plans — plan tiers $10/$30/$60/$120; commercial terms including the >$1M gross-revenue Pro/Mega requirement; stealth mode Pro+. Corroborated by eesel, "Midjourney pricing in 2026," https://www.eesel.ai/blog/midjourney-pricing and PxlPeak, "Midjourney Pricing Plans 2026," https://pxlpeak.com/blog/ai-tools/midjourney-pricing-plans (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^2]: Image-tool landscape and division of labor (Midjourney aesthetics / Ideogram text rendering / Recraft SVG + brand styles / frontier-lab editing models): NomadLab, "Best AI Image Generators 2026," https://nomadlab.cc/blog/2026/05/best-ai-image-generators-2026-midjourney-flux-ideogram-recraft-firefly corroborated by BuildMVPFast, "Best AI Image Generation July 2026," https://www.buildmvpfast.com/articles/best-llms-2026-guide/image-generation-ai and XainFlow, "8 Best AI Image Generators in 2026," https://www.xainflow.com/blog/best-ai-image-generators-2026-comparison (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^3]: Video-tool landscape and pricing (Veo 3.1 per-second API ~$0.15/s fast mode; Runway ~$12 Standard/~$76 Pro credit plans; Kling ~$10 entry; commercial use on paid plans; watermarked free tiers): LaoZhang, "Best AI Video Model in 2026," https://blog.laozhang.ai/en/posts/best-ai-video-model corroborated by BuildMVPFast, "AI Video Generation API Pricing (July 2026)," https://www.buildmvpfast.com/api-costs/ai-video and GetAIPerks, "Best AI Video Generators 2026," https://www.getaiperks.com/en/blogs/44-best-ai-video-generators-2026 (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^4]: ElevenLabs. Pricing page. https://elevenlabs.io/pricing — Free (no commercial rights), Starter $6/mo (~30 min TTS, commercial license floor), Creator $22, Pro $99, Scale/Business above. Corroborated by BIGVU, "ElevenLabs Pricing (2026)," https://bigvu.tv/blog/elevenlabs-pricing-2026-plans-credits-commercial-rights-api-costs/ and Flexprice, "ElevenLabs pricing breakdown," https://flexprice.io/blog/elevenlabs-pricing-breakdown (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^5]: Current Claude lineup and defaults (Sonnet 5 default tier from 2026-06-30; Fable/Mythos 5 above Opus) per the course master refresh report, `vault/00-program/_refresh-2026-07-master-report.md` (2026-07-17, two-source verified), cross-cutting theme 1.

[^6]: US Copyright Office. *Copyright and Artificial Intelligence, Part 2: Copyrightability.* January 29, 2025. https://www.copyright.gov/ai/Copyright-and-Artificial-Intelligence-Part-2-Copyrightability-Report.pdf — human authorship required; prompts alone insufficient; protection for human selection/arrangement/modification; disclosure duty per the March 2023 registration guidance https://www.copyright.gov/ai/ai_policy_guidance.pdf . Analysis corroboration: Skadden, "Copyright Office Publishes Report on Copyrightability of AI-Generated Materials," https://www.skadden.com/insights/publications/2025/02/copyright-office-publishes-report and Authors Guild summary https://authorsguild.org/news/us-copyright-office-ai-report-part-2-what-authors-should-know/ .

[^7]: The Decoder. "OpenAI sets two-stage Sora shutdown with app closing April 2026 and API following in September." https://the-decoder.com/openai-sets-two-stage-sora-shutdown-with-app-closing-april-2026-and-api-following-in-september/ — announced 2026-03-24; app/site closed 2026-04-26; API discontinues 2026-09-24; data deletion after each stage. Corroborated by OpenAI Help Center, "What to know about the Sora discontinuation," https://help.openai.com/en/articles/20001152-what-to-know-about-the-sora-discontinuation (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^8]: TechXplore. "Sora shutdown reveals costly limits of AI video generation and creative use." https://techxplore.com/news/2026-04-sora-shutdown-reveals-limits-ai.html — ~$1M/day operating costs vs ~$2.1M lifetime IAP revenue; download decline from 3.3M (Nov 2025) to ~1.1M (Feb 2026). Corroborated by Futurum Group, "OpenAI Sora Discontinuation," https://futurumgroup.com/insights/openai-sora-discontinuation-what-the-end-of-a-platform-means-for-enterprise-ai-strategy/ (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending; cost/revenue figures are press-reported, not audited).

[^9]: IAB. "The AI Ad Gap Widens." https://www.iab.com/insights/the-ai-gap-widens/ — second consecutive year finding Gen Z/Millennial consumers less positive about AI-generated advertising than ad executives estimate (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^10]: Marketing Brew. "Consumers are sick and tired of hearing about AI all the time" (Harris Poll data, Cannes Lions coverage). https://www.marketingbrew.com/stories/harris-poll-ai-fatigue-less-trust-ai-generated-ads-cannes-lions — majority-level AI fatigue; reduced trust in AI-generated ads (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^11]: Backlash survey compilation and case list (63% trust brands less on suspected AI ads; ~half disengage from suspected synthetic content; McDonald's Netherlands ad withdrawal): Influencers Time, "AI-Generated Ad Backlash: A Permanent Trust Problem," https://www.influencers-time.com/ai-generated-ad-backlash-is-now-a-permanent-trust-problem/ corroborated directionally by Browser Media, "Consumer insights reveal negative sentiment about brands using AI," https://browsermedia.agency/blog/why-most-consumers-dont-trust-generative-ai/ and Kate O'Neill, "The Authenticity Premium," https://www.koinsights.com/the-authenticity-premium-why-consumers-are-rejecting-ai-generated-content/ (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending; specific percentages vary by survey and should be treated as directional).

[^12]: Coca-Cola AI Christmas ad backlash, 2024 and 2025: Dani Di Placido, Forbes, "Coca-Cola Sparks Backlash With AI-Generated Christmas Ad, Again," November 4, 2025, https://www.forbes.com/sites/danidiplacido/2025/11/04/coca-cola-sparks-backlash-with-ai-generated-christmas-ad-again/ ; NBC News, "Coca-Cola causes controversy with AI-made ad," https://www.nbcnews.com/tech/innovation/coca-cola-causes-controversy-ai-made-ad-rcna180665 ; sentiment figures (positive 23.8%→10.2% post-launch) per ContentGrip, https://www.contentgrip.com/coca-cola-ai-holiday-ad-backlash/ (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^13]: The State of Brand. "The Anti-AI Brand Is Becoming a Real Market Position." https://www.thestateofbrand.com/news/anti-ai-brand-market-positioning — Aerie, Equinox, and other explicitly anti-AI campaigns in early 2026. Corroborated by Influencers Time, "Anti-AI Beer Ad Reveals Backlash Against AI Marketing," https://www.influencers-time.com/anti-ai-beer-ad-exposes-consumer-backlash-against-ai-marketi/ (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^14]: Meta for Business. "Meta Advantage+ Creative." https://www.facebook.com/business/ads/meta-advantage-plus/creative — AI creative tooling scale; 8M+ advertisers using Meta AI creative tools as of mid-2026 per Benly, "Advantage+ 2026 Updates," https://benly.ai/learn/meta-ads/advantage-plus-updates-2026 (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending; adoption figures vendor-reported). Full treatment Thursday.

_last_verified: 2026-07-17_
