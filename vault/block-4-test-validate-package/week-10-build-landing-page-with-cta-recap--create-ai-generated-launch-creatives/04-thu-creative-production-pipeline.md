---
type: lesson
block: block-4-test-validate-package
week: week-10
day_of_cycle: 4
day_name: thu
session_slug: create-ai-generated-launch-creatives
date_due: 2026-07-23
tags: [creative-pipeline, launch-kit, demo-video, screen-capture, screen-studio, ad-variants, advantage-plus, andromeda, og-images, qa-gates, ai-disclosure, platform-labeling, c2pa, eu-ai-act]
sources:
  - cursorclip-screen-studio-alternatives
  - ngram-screen-studio-alternatives
  - matte-screen-studio-review
  - facebook-business-advantage-plus-creative
  - admove-advantage-plus-2026
  - benly-advantage-plus-2026
  - auditsocials-meta-ai-label-2026
  - virvid-ai-video-ad-disclosure-2026
  - ytzolo-youtube-ai-disclosure
  - influencermarketinghub-ai-disclosure-rules
  - socialmediatoday-linkedin-ai-content
  - zoomsphere-linkedin-algorithm-2026
  - eyesift-c2pa-2026
  - internetpros-provenance-2026
  - uscopyright-part2-copyrightability-2025
last_verified: 2026-07-17
word_count_target: 4800
---

# The creative production pipeline — prompt-to-asset workflows, QA gates, and the disclosure rules your launch must clear

## Why this matters

Yesterday you chose tools and wrote a brand spec. Today you build the production line that turns them into a finished launch kit, because the difference between "I can generate images" and "I shipped a coherent kit by Friday" is a pipeline: briefs in, assets out, with selection discipline, human QA gates, an archive, and a compliance pass that keeps your ads from being rejected (or quietly demoted) by the platforms they run on. That last part moved from theory to enforcement while this course was running: Meta now requires AI-content disclosure on ads and labels detected synthetic content, YouTube requires disclosure for realistic synthetic media, LinkedIn's feed actively demotes generic AI text, and the EU AI Act's transparency obligations for AI-generated content become applicable on August 2, 2026, sixteen days after this lesson's verification date.

The deeper reason this lesson exists: the pipeline is where the slop battle is actually won. Wednesday's positioning argument ("AI for volume, humans for judgment") is empty until it is operationalized as *gates a lazy asset cannot pass*. You already believe this for your agent, whose outputs go through validators and eval harnesses before touching a customer. Today applies the identical engineering instinct to marketing assets, and Saturday's code-lab turns the gates into runnable checks.

## Prerequisites

- Wednesday's outputs: chosen stack, verified terms notes, one-page brand spec, positioning stance. The pipeline consumes all four.
- Monday's substantiation file: every ad claim traces to it. Copy QA without it is vibes.
- [[05-fri-prototype-pipeline|Block 2 Week 3 Friday]]'s spec-first build habit. Same shape, different artifact: briefs are specs for creative.

## Layer 1 — The kit, the pipeline, and the one rule

**The launch kit inventory** for a Week 9 package, in priority order:

1. **Demo video** (60–120s, the real product running): the single highest-value asset, per Monday's proof hierarchy.
2. **Hero visual** (1 final, from many candidates): sets the page's aesthetic.
3. **OG/social share image set** (1200×630 for link previews, plus square and vertical crops): the asset most operators forget and the one every share of your launch renders through.
4. **Five ad variants** (hook × angle matrix, Layer 4): even if you never buy ads, these are your launch-week social posts.
5. **Social cutdowns** (2–3 clips, 15–30s, cut from the demo video): platform-native versions, captioned, because most feeds autoplay muted.

**The pipeline**, six stages, each with an output contract: **Brief → Generate → Select → Polish → QA gate → Archive & publish.** A brief specifies the asset (purpose, dimensions, brand-spec constraints, copy, claims used, disclosure status) before any generation happens. Generation is batch, never single-shot. Selection is a human choosing from candidates against the brief. Polish is the design-tool pass (type, crops, compositing real UI). The QA gate is a checklist the asset passes or fails (Layer 5). Archive means the accepted asset, its prompt, its tool, its settings, and its license basis are stored together in your repo, per Wednesday's Sora lesson.

**The one rule:** generation is cheap, so *never negotiate with a mediocre candidate*. The unit of work is the batch of twenty, not the image; if no candidate clears the brief, fix the brief and re-batch. Operators waste hours nudging a weak generation toward acceptable when a re-batched prompt would have produced a better candidate in ninety seconds. This is the same insight as re-sampling versus editing a bad agent output, and it is the main productivity delta between practiced and unpracticed AI-creative operators.

## Layer 2 — Hero visuals and OG images: the still-image workflow

The workflow, concretely, for the hero:

1. **Brief:** "Hero background, 1920×1080 safe-cropped to 16:9 and 4:5, isometric workflow illustration in palette #0F172A/#38BDF8/#F8FAFC, no humans, no text (type set separately), mood: calm infrastructure, anchor set A." Note what the brief does *not* contain: adjectives about quality. Constraints, not vibes.
2. **Batch:** 16–24 candidates across 2–3 prompt phrasings. In Midjourney-class tools, use your style anchor; in Recraft, your uploaded brand style.
3. **Select against the brief:** kill anything violating palette or negative list *before* judging beauty; a gorgeous off-brand candidate is a trap (it will seduce you into breaking the system that makes the other nineteen assets match).
4. **Polish:** composite real product UI (screenshots, never generated), set type in your design tool, export the crop set.
5. **QA and archive.**

The OG image is the same workflow with one added discipline: **it must read at thumbnail size.** Test at 240px wide; if the message needs squinting, it fails. Text inside OG images goes through Ideogram or your design tool (Wednesday's type rule), and the safe layout is brutal simplicity: wordmark, seven-word claim, one visual element. This is also the asset where the file-size and dimension checks in Saturday's QA runner earn their keep, because a wrong-ratio OG image silently renders as a cropped mess in every Slack and LinkedIn preview of your launch, and you typically discover it after the launch post is live.

## Layer 3 — The demo video: screen capture first, generated video last

For an agent product, the demo video's job is evidential: *this thing exists and works*. Generated video cannot do that job; only your actual product on screen can. So the spine of the launch video is **screen capture with production polish**, and the 2026 tooling makes polish nearly free.

**The capture-and-polish tier**, verified July 2026: Screen Studio (the category-definer: auto-zoom, cursor smoothing, device frames) moved to $29/month subscription or ~$108/year, after its one-time license jumped from $89 to $149, a price change that pushed many solo operators to alternatives.[^1] The credible alternatives: OBS Studio (free, powerful, no built-in polish), FocuSee (~$59/year, cross-platform auto-zoom), Tella (~$15/month, presentation-style editing), and a crop of one-time-purchase Mac tools in the $59–129 range.[^1] Any of them is sufficient; the polish features that matter for conversion are exactly two, auto-zoom on interaction points and smooth cursor movement, because they direct the viewer's eye the way an editor would.

**The storyboard** that fits agent products, 90 seconds, four beats:

1. **The pain, in the buyer's artifact (0–15s).** Not a narrator saying "support is hard"; an actual overflowing inbox, an actual ugly ticket. Real artifacts are the authenticity signal.
2. **The real run (15–60s).** Your agent processing a real (anonymized) input, at real speed or honestly labeled time-compression, with visible timestamps. Include one imperfect moment if you have the nerve; per Monday's trust logic, it buys more than it costs.
3. **The guardrail beat (60–75s).** The escalation firing, the human handoff rendering with context. This beat is unique to agent products and almost nobody films it; it answers the babysitting objection visually and differentiates instantly.
4. **The claim and CTA (75–90s).** The scoped promise from Monday's hero, spoken or set in type, then one action.

**Voiceover:** ElevenLabs Starter/Creator tier covers it (Wednesday's terms note applies: not the free tier).[^2] Or your own voice, one take, cleaned up; for founder-led launches, your real voice is on-positioning. **Generated video's role:** b-roll only, and only if Wednesday's budget allows: a 4-second Veo/Runway mood shot for the cold open. Never generate fake product footage; a synthesized UI in a demo video is the "live demo that is secretly canned" lie from Tuesday, in video form, with the same total credibility cost when noticed.

Social cutdowns fall out of the storyboard for free: beat 2 alone (15–30s, captioned) is your feed-native clip; beat 3 alone is the differentiated one nobody else posts.

## Layer 4 — Ad variants under Andromeda: creative diversity is the buying lever

Even a $200 launch-week ad budget teaches you things organic reach cannot (Friday instruments this). But the 2026 platform reality changes what "making ads" means. Meta's ranking infrastructure (Andromeda) evaluates enormously more creative variants in parallel than its predecessors, and since February 2026 new Sales/Leads campaigns launch with every Advantage+ creative enhancement enabled by default, meaning **the platform will actively mutate your assets** (recrops, brightness, text overlays, generated backgrounds) unless you opt out per-enhancement.[^3] Meta's own numbers claim a 22 percent average ROAS lift for Advantage+ sales campaigns and 12 percent CTR lift for Advantage+ creative; treat both as vendor-reported, but the structural shift is corroborated across practitioner coverage: **targeting optimization is saturated, so creative variety is now the primary performance lever**, with practitioner estimates putting the large majority of 2026 performance-marketing effort into creative operations rather than media buying.[^3][^4]

Operational consequences for your five variants:

1. **Build variants as a matrix, not five one-offs.** Three hooks (the pain hook, the proof hook, the objection hook) × two formats gives you six cells; ship five. The proof hook quotes your eval number; the objection hook leads with "what happens when it's wrong" (nobody else's ads do; yours can, because Monday gave you the substantiation).
2. **Every claim in every variant traces to the substantiation file.** Ad review is exactly where unsupported "resolves 90% of tickets" claims become FTC exposure (Monday, Operation AI Comply) and platform-rejection risk.
3. **Audit the default-on enhancements.** If brand consistency matters (it does; you spent Wednesday on it), review which Advantage+ enhancements you leave enabled; "generated backgrounds" and text overlays can violate your own brand spec.[^3]
4. **Expect and pre-clear the AI disclosure.** Which brings us to the compliance layer.

## Layer 5 — Disclosure, platform rules, and provenance: the compliance pass

The rules as they stand on 2026-07-17, in decreasing order of enforcement bite:

**Meta.** Two distinct mechanisms. First, ads with photorealistic AI-generated or significantly AI-altered content require disclosure, with Meta auto-labeling content produced by its own AI tools and applying detection-plus-enforcement (rejection or retroactive flagging) to undisclosed AI creative; advertiser disclosure requirements tightened through early 2026.[^5] Second, political/social-issue ads have stricter active-disclosure duties. For your launch ads: if a variant contains photorealistic generated imagery, tick the disclosure. Isometric illustrations and screen captures of your real product generally do not trigger it, which is one more quiet argument for Wednesday's "no photorealistic humans" negative list.[^5]

**YouTube.** Creators must disclose realistic synthetic or altered media that could mislead viewers about real events; disclosure renders as a label, with stronger placement for sensitive topics. Your product demo (real screen capture) needs nothing; a fully-generated cinematic spot would.[^6]

**LinkedIn.** No formal disclosure regime, but something operationally stronger: the feed's ranking systems demote generic AI-generated text, a shift reported since late 2025 and consistent with the platform's public statements about limiting low-quality AI content; independent analyses report organic reach collapsing for pages posting detectably-generic AI content, and hybrid human-edited content dramatically outperforming raw generation.[^7] The exact reach percentages circulating (e.g., "~2% reach for flagged pages") are analytics-vendor estimates, not LinkedIn statements; hold them loosely.[^7] The operator conclusion is the same either way, and it matches your [[03-wed-building-in-public|Block 1 Week 2]] discipline: launch posts get written or heavily rewritten by you, in your voice, with your real numbers.

**EU AI Act, Article 50 (future-framed: applicable August 2, 2026).** If your launch reaches EU users, transparency obligations for AI-generated and manipulated content arrive sixteen days after this lesson's date, including machine-readable marking expectations for synthetic content.[^8] For a solo operator the practical prep is light: know which of your assets are AI-generated (your archive already records it), and prefer tools that write provenance metadata.

**Provenance (C2PA).** The Content Credentials standard hit v2.3 in February 2026 and is now embedded across Adobe tooling, some frontier-lab outputs, Google surfaces, and shipping camera hardware; its weakness remains preservation, since many platform transformations strip metadata.[^8] Current status for you: attach credentials where your tools support it (cost: zero), treat them as a good-faith signal rather than protection, and expect this to matter more each quarter as EU enforcement and platform labeling converge on machine-readable provenance.

**Copyright registration.** Covered Wednesday; the pipeline hook is simply that your archive's per-asset AI-generation record is exactly the disclosure documentation the Copyright Office's guidance expects if you ever register.[^9]

## Layer 6 — The human QA gate, specified

The gate is a checklist, run by a human, with a hard rule: **no asset ships with an open failure.** Saturday's code-lab automates the mechanical half and leaves the judgment half to you. The checklist, complete:

**Mechanical (automatable):** correct dimensions and aspect ratio per asset type (incl. 1200×630 OG); file-size budgets (hero < 400KB served, OG < 300KB); filename convention carries asset type and variant ID; alt text present for every published surface; archive record complete (prompt, tool, settings, license basis, AI-generated flag); disclosure flag set for platforms that need it; every quantitative claim in copy matched against the substantiation file's claim list.

**Judgment (human, 60 seconds per asset):** artifact scan (hands, text gibberish, warped geometry, uncanny faces); brand-spec compliance (palette, negative list, aesthetic match to anchor set); thumbnail legibility; the slop test ("would I believe a competent human reviewed this?"); the claim test ("would I defend this sentence on a sales call?"); the positioning test (does this asset match Wednesday's declared stance?).

Two design notes. First, the gate runs *per asset*, not per kit; batch-approving a kit is how one six-fingered hand ends up in a paid placement. Second, log gate failures. Three assets failing palette compliance is not three bad assets; it is one bad brief or one drifting style anchor, and the log is what tells you which. You are running an eval harness over a generative system; all of your [[06-sat-rag-evaluation|Block 2 Week 4]] instincts transfer.

## Runnable experiment — produce four assets through the full pipeline

**Task.** Using yesterday's stack and brand spec: produce your launch's **hero visual, one OG image, and two ad variants** (one proof-hook, one objection-hook) through all six pipeline stages. Write the briefs first, batch-generate, select against brief, polish, run the full QA checklist by hand (Saturday automates it), archive with complete records.

**Pass bar.** (1) Four briefs exist as files, written before generation. (2) Selection discipline is evidenced: candidate count ≥ 12 for the hero, with the losing candidates' folder retained. (3) All four assets pass every mechanical check and every judgment check, with the checklist results written down. (4) The two ad variants' claims each cite a line in your substantiation file. (5) The archive contains prompt + tool + settings + license basis + AI-flag for all four. (6) Total elapsed time ≤ 3 hours; if you are over, you negotiated with mediocre candidates, and the retro should say so. Deliberately absent from the pass bar: subjective beauty. The system is the deliverable; taste improves with reps.

## Common mistakes experts see

1. **Single-shot generation.** One prompt, one image, ship it. The batch is the unit; selection is where quality comes from.
2. **Generated product footage.** Synthesizing UI for the demo video: the video-form canned-demo lie, discovered eventually, fatal to everything.
3. **Ignoring the default-on enhancements.** Advantage+ mutates un-opted-out creative; your carefully brand-locked asset ships with a generated background you never saw.[^3]
4. **Treating disclosure as shameful.** Ticking Meta's AI-disclosure box costs approximately nothing with a competent asset; an undisclosed detection or takedown during launch week costs the week.[^5]
5. **Posting raw model text on LinkedIn.** The one platform where your buyers congregate is the one algorithmically punishing exactly that.[^7]
6. **No archive.** Three weeks later a client asks "can we get the hero in 4:5?" and the prompt, seed, and style anchor are gone (or the tool is; see Sora).
7. **QA by mood.** No checklist, so the gate tightens when you are fresh and opens when you are tired, and launch night is when you are tired. Checklists exist because judgment degrades exactly when it is needed.

## Reflection questions

1. Beat 3 of the storyboard (filming your escalation path) is rare enough to be a differentiator. What does it say about the market that showing the failure path is a competitive advantage? How long do you expect that to last?
2. Your objection-hook ad variant leads with "what happens when it's wrong." Predict its CTR relative to the proof-hook variant, write the prediction down, and check it against Friday's data. What would each outcome teach you about your audience's position on Wednesday's slop-fatigue spectrum?
3. If Meta's ranking now explores creative variants at massive parallel scale, the scarce input is *meaningfully different* variants, not more variants. What is the difference between a variant and a permutation, in your matrix, concretely?
4. The QA gate's judgment half cannot be automated today. Which single judgment check would you trust a model to run first, and what golden set would you build to find out?
5. Your archive makes every asset reproducible. Whose problem does that solve in month 3: yours, your client's, or your acquirer's? What does that imply about archives as a professional habit generally?
6. EU AI Act Article 50 lands August 2. Sketch the minimal compliance delta between "US-only launch" and "EU-reachable launch" for your specific kit. Is geo-limiting your launch ever the rational answer?

## My take (reviewer lens)

**Karpathy** would like the batch-and-select discipline (it is just sampling with a human verifier) but would needle the pipeline's solemnity: six stages and two checklists to ship five images is process worship if the operator runs it once and abandons it, and the honest test is whether *your second* launch reuses the pipeline in an hour instead of a day; if not, you built ceremony, not tooling. **Boris Cherny's** current fleet-scale-agents lens would go further: the mechanical gate should not be a checklist you run but a check *suite* an agent runs on every asset the moment it lands in the repo, with you reviewing failures only, and Saturday's code-lab is deliberately built as exactly that seed. He would also flag the real tooling pitfall of the week: default-on platform enhancements are a silent mutation layer between your QA gate and the user, and any pipeline that ends at "uploaded" rather than "verified as served" has an unmonitored last mile. **Hamel Husain** would attack the softest spot: the judgment checks are unmeasured ("would I believe a human reviewed this?" is a vibe), and he would want the creative pipeline held to the same standard as the agent, with a small labeled set of pass/fail assets and periodic checks that your gate agrees with itself week to week. He is right that this is where the discipline is thinnest, and the honest state of the art in July 2026 is that almost nobody measures creative QA consistency; doing it even crudely would put you ahead of agencies.

## Further reading

**Must-read**

- Meta Business Help / Advantage+ creative documentation and one independent 2026 guide (AdMove or Benly) — know exactly what the platform does to your assets by default.[^3][^4]
- InfluencerMarketingHub, "AI Disclosure Rules by Platform" — the cross-platform disclosure map in one read.[^6]

**Recommended**

- ngram / CursorClip Screen Studio alternative roundups — the capture-tool landscape with real pricing; pick in ten minutes and move on.[^1]
- EyeSift, "C2PA Adoption Status 2026" — provenance's actual state versus its press releases.[^8]

**Optional**

- Social Media Today's LinkedIn AI-content coverage plus one algorithm analysis — the demotion mechanics, with appropriate salt for vendor-derived reach numbers.[^7]
- US Copyright Office registration guidance — the disclosure duty your archive already satisfies.[^9]

## Citations

[^1]: Screen-capture tooling and pricing: CursorClip, "Best Screen Studio Alternatives (2026)," https://cursorclip.com/blog/screen-studio-alternatives/ (Screen Studio $29/mo or ~$108/yr; one-time license history $89→$149); corroborated by ngram, "7 Screen Studio Alternatives (2026)," https://www.ngram.com/blog/screen-studio-alternatives-price-hike and Matte, "Screen Studio Pricing 2026 Review," https://matte.app/blog/screen-studio-review ; alternatives (OBS free; FocuSee ~$59/yr; Tella ~$15/mo) per the same roundups (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending; comparison posts are competitor-written, prices cross-checked across three domains).

[^2]: ElevenLabs pricing and commercial-rights floor: see Wednesday [^4] (Starter $6/mo commercial floor; free tier non-commercial).

[^3]: Meta Advantage+ creative in 2026: Meta for Business, "Meta Advantage+ Creative," https://www.facebook.com/business/ads/meta-advantage-plus/creative ; Andromeda ranking shift, February-2026 default-on enhancements, and vendor-reported lifts (22% ROAS Advantage+ sales; 12% CTR Advantage+ creative, Meta Marketing Science) per AdMove, "Meta Advantage+ Creative Best Practices for 2026," https://www.admove.ai/blog/meta-advantage-creative-best-practices-for-2026 and Benly, "Advantage+ 2026 Updates," https://benly.ai/learn/meta-ads/advantage-plus-updates-2026 (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending; lift figures vendor-reported).

[^4]: Creative-ops-over-media-buying shift ("~80% of performance work is creative operations," practitioner estimate): Xcceler, "Meta ads in 2026," https://xcceler.com/blog/meta-ads-in-2026-ai-creative-advantage-targeting-what-actually-converts/ corroborated by LeapBuzz, "Meta Advantage+ Creative in 2026," https://leapbuzz.com/blog/meta-advantage-plus-creative-ai/ (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending; treat the 80/20 split as practitioner consensus, not measurement).

[^5]: Meta AI-content labeling and advertiser disclosure: AuditSocials, "Meta AI Content Label Policy 2026," https://www.auditsocials.com/blog/meta-ai-generated-content-label-policy-2026 (detection + enforcement incl. rejection and retroactive flagging; auto-labeling of Meta-AI-generated ad content since Feb 2025; photorealistic-human triggers) corroborated by Virvid, "AI Video Ad Disclosure Requirements 2026: Meta, YouTube, TikTok & Legal Compliance," https://virvid.ai/blog/ai-video-ad-disclosure-requirements-2026-meta-youtube-tiktok and TechJack Solutions, "Meta Now Requires Advertisers to Disclose AI-Generated Content," https://techjacksolutions.com/ai-brief/meta-now-requires-advertisers-to-disclose-ai-generated-conte/ (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^6]: YouTube synthetic-media disclosure (realistic altered/synthetic content requires creator disclosure; labels applied, stricter for sensitive topics): InfluencerMarketingHub, "AI Disclosure Rules by Platform," https://influencermarketinghub.com/ai-disclosure-rules/ corroborated by YTZolo, "YouTube Policy on AI Generated Content Disclosure 2026," https://ytzolo.com/blog/youtube-policy-on-ai-generated-content-disclosure/ (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending; policy originated March 2024, still in force with 2025–26 refinements).

[^7]: LinkedIn demotion of generic AI content: Social Media Today, "LinkedIn wants to limit the reach of AI-generated content," https://www.socialmediatoday.com/news/linkedin-wants-to-limit-the-reach-of-ai-generated-content/820935/ corroborated by ZoomSphere, "LinkedIn Algorithm 2026: Why Generic AI Content Kills Your Organic Reach," https://www.zoomsphere.com/blog/linkedin-algorithm-2026-why-generic-ai-content-kills-your-organic-reach and by the course master refresh report (LinkedIn demoting AI-generated outreach, cross-cutting theme 4). Circulating reach figures (~2% for flagged pages, attributed to Hootsuite analysis; 156% hybrid-content outperformance, attributed to Sprout Social) are analytics-vendor estimates — directional only (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^8]: Provenance and EU timeline: EyeSift, "C2PA Adoption Status 2026," https://www.eyesift.com/faq/c2pa-content-credentials-2026-cryptographic-provenance-adoption/ (C2PA v2.3 published Feb 2026; Adobe/Google/camera-hardware adoption; metadata-stripping weakness) corroborated by Internet Pros, "AI Content Provenance & Watermarking 2026," https://internet-pros.com/blog/ai-content-provenance-watermarking-c2pa-2026/ (EU AI Act Article 50 machine-readable marking applicable 2026-08-02 — future-framed per course rules; date also verified in the July 2026 master refresh report) (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^9]: US Copyright Office. Registration guidance for works containing AI-generated material (disclosure duty for more-than-de-minimis AI content). https://www.copyright.gov/ai/ai_policy_guidance.pdf — see Wednesday [^6] for the Part 2 copyrightability report and corroborating analyses.

_last_verified: 2026-07-17_
