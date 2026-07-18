---
type: lesson
block: block-3-advanced-topics-voice
week: week-08
day_of_cycle: 3
day_name: wed
session_slug: automation-agent-integration-mcps
date_due: 2026-07-08
tags: [scraping, playwright, browserbase, firecrawl, stagehand, cloudflare, pay-per-crawl, robots-txt, hiq, eu-ai-act, tdm-opt-out, structured-extraction, legal, ethics]
sources:
  - cloudflare-content-independence-2026-07
  - cloudflare-press-your-content-your-rules-2026
  - techcrunch-cloudflare-mixed-use-2026-07
  - firecrawl-pricing-2026
  - firecrawl-v25-2026
  - browserbase-pricing-2026
  - playwright-1-61-2026
  - hiq-linkedin-wikipedia
  - eu-ai-act-tdm-2026
  - robots-txt-legal-2026
  - ietf-aipref-2026
  - reddit-perplexity-lawsuit-2026
last_verified: 2026-07-17
word_count_target: 5400
---

# The scraping stack, legally and technically — building a data supply against a web that now fights back

## Why this matters

Saturday's build reads the web. In 2024 that was a solved problem you barely thought about. In mid-2026 it is a live negotiation with three counterparties who did not exist as blockers two years ago: **Cloudflare**, which as of July 2026 meters and increasingly *blocks* AI crawlers by default; **the courts and regulators**, who spent 2025–2026 turning robots.txt and terms-of-service from etiquette into evidence; and **the sites themselves**, armored with anti-bot systems that treat your automation as an adversary until proven otherwise.

You need two literacies today, and skipping either gets you or your client hurt. **Technical**: the 2026 scraping stack — what Playwright, Browserbase, and Firecrawl each do, what they cost, and which to reach for. **Legal-ethical**: what you may scrape, what signals you must honor, and where the case law and the EU AI Act actually stand — not the folk version. By tonight you will have a written scraping policy for your niche that a lawyer would not immediately red-pen, and a stack choice you can defend on both cost and risk.

## Prerequisites

- [[01-mon-the-automation-spectrum-in-2026]] and [[02-tue-mcp-integration-patterns-for-unattended-agents]] — the runtime and integration your scraper plugs into.
- [[03-wed-rag-as-a-system]] — structured extraction here feeds the same downstream shapes retrieval does; the "schemas, not regex" discipline is shared.
- Comfort reading a `robots.txt` and an HTTP response's headers.

## Layer 1 — The 2026 scraping stack, tool by tool

Think of scraping as three separable jobs — **fetch** (get the bytes past whatever guards the page), **render** (execute JavaScript so the DOM is complete), and **extract** (turn the DOM into structured data). The stack is a menu across these jobs, and picking well means knowing which job each tool actually solves.

### Playwright — the open-source workhorse (fetch + render)

Microsoft's Playwright is the default browser-automation framework, at **v1.61 as of June 29, 2026**.[^7] The 2026 releases pivoted hard toward AI agents driving the browser rather than humans writing tests: v1.59 (April 2026) shipped a Screencast API, CLI debugging for agents, and — most relevant to this course — a **Playwright CLI designed to be token-efficient for coding agents like Claude Code**, avoiding the large accessibility-tree and tool-schema dumps that bloat model context.[^7] Playwright is free, runs Chromium/Firefox/WebKit on one API, and is the right floor for scraping when you control the infrastructure and the targets aren't aggressively defended. What it does *not* give you: managed IP rotation, CAPTCHA handling, or a hosted fleet — you run the browsers, you fight the anti-bot arms race, you own the cost.

### Browserbase + Stagehand — managed browsers for agents (fetch + render, hosted)

Browserbase is hosted headless-browser infrastructure priced per browser-minute: **free, Developer $20/mo, Startup $99/mo, and custom Scale**, with proxy traffic billed separately (residential ~$8/GB, stealth/datacenter ~$0.30/GB).[^6] Its open-source **Stagehand** SDK is the piece to understand: it wraps Playwright with four AI primitives — `act`, `extract`, `observe`, and `agent` — so you drive a browser with natural-language instructions instead of brittle CSS selectors, and it plugs into the major agent frameworks.[^6] This is the "managed infrastructure" tier: you reach for it when DIY stops making sense — when you need concurrency, when targets require residential IPs and stealth, when maintaining your own browser fleet costs more than paying someone who does it at scale.

### Firecrawl — the extraction-first API (fetch + render + extract)

Firecrawl is the highest-level option: an API that takes a URL and returns clean, model-ready Markdown or structured JSON, handling fetch, render, and extraction in one call. Pricing is credit-based across **Free (1,000 credits/mo), Hobby ($16/mo), Standard ($83/mo / 100K credits), Growth ($333/mo), Scale ($599/mo), and Enterprise**; scrape/crawl/map/monitor cost ~1 credit/page, JSON extraction adds ~4 credits/page, and — a real trap — **credits do not roll over**.[^4] The **v2.5** release (2026) added a Semantic Index (already serving ~40% of API calls) letting you request data "as of now" or "as of last known good copy" via a `maxAge` parameter, plus native change-tracking that git-diffs a page against its last scrape at no extra cost.[^5] That change-tracking feature is quietly perfect for Saturday's build: your monitor only pays full freight when a source actually changed.

### The selection rule

- **Control the targets and infra, targets undefended, cost-sensitive** → Playwright.
- **Need scale, stealth, concurrency, or the model to navigate** → Browserbase + Stagehand.
- **Want a URL to become clean structured data with change-tracking and minimal ops** → Firecrawl.
- **Realistically, for Saturday**: Firecrawl or `requests`+Playwright for the fetch/render/extract of RSS-and-article sources, because your niche's sources are mostly cooperative publications, not adversarial marketplaces. Reserve Browserbase for when a specific high-value source hides behind serious anti-bot. Do the honest cost math per source, at non-rollover credit rates.

Anthropic-native note: Claude's **web search tool** ($10 per 1,000 searches plus token costs) and **web fetch tool** (token costs only) are also in this stack — for *discovery* and *light retrieval* inside an agent turn, not for high-volume structured scraping.[^ws] For a daily digest they can replace a bespoke fetcher entirely; for a thousand-page crawl they'd bankrupt you. Right tool, right job.

## Layer 2 — The anti-bot reality: Cloudflare changed the rules in July 2026

Here is the fact that reorganizes the whole field. In its "Content Independence Day" push, **Cloudflare announced that starting September 15, 2026, its default settings will block "mixed-use" AI crawlers on any page that hosts ads** — applying automatically to new customers, new sites of existing customers, and all existing free-tier customers.[^1][^3] The mechanism is a taxonomy Cloudflare now enforces at the edge: crawlers are classified as **Search** (index to answer later — allowed by default), **Agent** (act in real time for a user), or **Training** (absorb content permanently into a model) — and for new domains, **Agent and Training are blocked by default on ad-carrying pages while Search stays allowed**.[^1][^3] Multi-purpose crawlers like Googlebot get judged by all their behaviors, most-restrictive-rule-wins.

The economics driving this: AI-related crawlers hit **52% of total crawler requests by June 2026** (up from 22% in spring 2025), and Cloudflare's data shows **over 50% of AI crawl traffic re-fetches unchanged pages** — wasted bandwidth for publishers, wasted compute for AI companies.[^2] That waste statistic is why Firecrawl's change-tracking and Cloudflare's freshness signals both exist, and why your scraper should never re-fetch blindly.

Cloudflare's "Pay Per Crawl" marketplace is evolving into **"Pay Per Use"**, shifting the charge from *when a bot fetches* to *when content creates value* — initial partners Ceramic.ai and You.com pay publishers when their content appears in AI results.[^1][^2] The direction of travel is unambiguous: **the free-scrape era is closing, and access to a large fraction of the web is becoming a metered, permissioned, or paid transaction.**

What this means operationally for your build:

- **Identify honestly.** Send a real User-Agent naming your bot and a contact URL. Cloudflare's regime rewards declared, well-behaved bots and punishes evasion. Spoofing a browser to dodge classification is exactly the behavior the September 15 defaults are built to catch — and the behavior that turns a civil dispute into a bad-faith one (Layer 3).
- **Prefer official access.** RSS/Atom feeds, sitemaps, public APIs, and licensed feeds are not just easier — they're the access paths that survive the new regime. A scraper that reads RSS where RSS exists is both cheaper and legally cleaner than one that renders the article page.
- **Assume the door can close.** Architect Saturday's build so a source going dark (403, block page, paywall) is a handled PERMANENT-class event that alerts and degrades gracefully — not a crash and not a silent empty brief.

## Layer 3 — The legal landscape, told straight

Disclaimer, and mean it: this is operator orientation, not legal advice; jurisdiction and facts change everything; for client work touching real money or personal data, get a lawyer. With that said, here is the honest 2026 state.

### US: hiQ is narrower than the memes

**hiQ Labs v. LinkedIn** is the most-cited US scraping precedent, and it is routinely overstated. The Ninth Circuit held that scraping *publicly available* data likely does not violate the Computer Fraud and Abuse Act (CFAA) — access to public pages isn't "unauthorized access" to a protected computer.[^8] But the case **settled in 2022 with hiQ paying damages and destroying the scraped data**, after LinkedIn won on *contract* and unfair-competition theories, not CFAA.[^8] The durable lesson: **the CFAA is a weak weapon against scraping public data, but breach-of-contract (violating Terms of Service you assented to) and related theories are live and winnable for the site.** Public-does-not-mean-permissionless. If you clicked "I agree" or the ToS binds by use, that contract can make your scraping "unauthorized" where the CFAA would not.

The 2026 front line is **Reddit v. Perplexity** (filed October 2025): Reddit alleges Perplexity's crawlers reached Reddit content through a Google-search backdoor, using a hidden honeypot post to build its evidence, and named data-scraping services (Oxylabs, AWMProxy, SerpApi) as co-defendants; Perplexity moved to dismiss, arguing its practices breach neither anti-hacking law nor platform contracts.[^12] As of mid-2026 it is **unresolved** — do not teach its outcome as settled, but do teach its shape: platforms are now litigating the *supply chain* of scraping, going after intermediaries and indirect-acquisition routes, not just the end scraper.

### EU: robots.txt and TDM opt-outs now carry copyright weight

The EU moved robots.txt from suggestion to legally significant signal. Under **Article 4 of the DSM Copyright Directive (2019/790)**, rights holders may reserve their works from text-and-data mining via *machine-readable* means — and the EU AI Act requires general-purpose AI providers to respect these opt-outs, publish training-data summaries, and honor robots.txt-style signals, with **GPAI enforcement (fines up to €15M or 3% of global turnover) applying from August 2, 2026**.[^9] The practical effect: **ignoring a TDM opt-out expressed in robots.txt can be copyright infringement in the EU**, a very different posture from the US "evidence of intent" treatment.[^10] Note the unsettled edge a Hamburg court raised — whether a *natural-language* ToS reservation counts as "machine-readable" now that AI can read it — which is doctrinally live and which you should not resolve in a client's favor on your own authority.[^9]

### robots.txt everywhere: not a contract, but not nothing

Globally, robots.txt is **not itself legally binding** — it's a voluntary protocol with no enforcement in the spec.[^10] But courts treat compliance as a signal: **honoring it evidences good faith; ignoring it evidences willfulness and knowledge that access was unwanted** — factors that swing contract, copyright, and unfair-competition claims.[^10] And the standard is professionalizing: the **IETF AIPREF working group** is standardizing a vocabulary (`train-ai`, `search` categories) and attachment mechanisms (a `Content-Usage` header and a robots.txt `Content-Usage` rule), with an August 2026 milestone to send a spec to the IESG — plus the emerging `ai.txt` convention.[^11] Machine-readable AI-usage preferences are becoming infrastructure; build to read them now.

## Layer 4 — The ethical scraping rules this course endorses

Below the legal floor sits a professional standard. These are the rules this course holds you to on the Saturday build and in client work — stricter than the law in places, because your reputation and your client's are the real stakes.

1. **Read and honor robots.txt and TDM signals — every run, not once.** Parse it, respect `Disallow`, respect `Crawl-delay`, and honor AIPREF/`ai.txt` opt-outs where present. Re-check periodically; sites change their minds.
2. **Identify truthfully.** Real User-Agent, bot name, contact URL. Never spoof a human browser to evade classification. If a site would block you knowing who you are, that is your answer.
3. **Prefer the front door.** RSS, sitemaps, official APIs, licensed feeds — in that order — before rendering a page. Cheaper, cleaner, more durable.
4. **Rate-limit like a guest.** Conservative concurrency, jittered delays, back off on 429/503, never hammer. Cloudflare's own data says most AI crawl traffic is wasteful re-fetches;[^2] don't be that traffic. Use conditional requests and change-tracking so you fetch only what changed.
5. **Take only what you need, keep it only as long as you need it.** Minimize scope; don't hoard. In the EU, personal data pulls you into GDPR regardless of how "public" it was.
6. **Never scrape behind auth or paywalls you don't have rights to.** That's where CFAA and contract claims have teeth, and where "public" stops applying.
7. **Attribute and link.** Saturday's brief cites and links every source. This is both good ethics and good product — it sends traffic back, which is the reciprocity the whole content economy is fighting over.
8. **When a site says no, stop.** A block, a cease-and-desist, an explicit ToS prohibition on automated access — honor it. The cost of one lost source is nothing next to the cost of a bad-faith finding.

> My take (labeled opinion): the operators who will still have a scraping-dependent business in 2028 are the ones who treat these rules as a moat, not a tax. As free scraping closes, "we access data cleanly, with permission, attributed" becomes a sellable differentiator — the same way deliverability compliance became one for cold outreach. The cowboys get rate-limited, blocked, sued, and de-platformed out of the market; the professionals inherit it.

## Layer 5 — Structured extraction: schemas, not regex

Once you have the bytes, extraction is where amateurs and professionals diverge hardest. The amateur writes regex against HTML and rewrites it every time the site ships a redesign. The professional defines a **target schema** and extracts against it, using the tool best suited to each source.

The 2026 move is **schema-constrained LLM extraction**. Anthropic's structured outputs are **generally available on the Claude API** (including Fable 5, Sonnet 5, Opus 4.8, Haiku 4.5): you supply a JSON Schema via `output_format`, the API compiles it into a grammar that constrains generation token-by-token (caching the compiled schema ~24h), and the model is *guaranteed* to return conformant JSON — plus `strict: true` on tool definitions for guaranteed-valid tool arguments.[^so] This eliminates the "the model returned almost-JSON and my parser died at 3 a.m." failure class that killed a generation of unattended pipelines. One caveat the docs flag: strict JSON-schema output conflicts with citation blocks (which interleave), so a stage that needs inline source citations and a stage that needs guaranteed schema are two different calls — a design constraint you'll feel Saturday.

The extraction ladder, cheapest-first (spend model tokens only where structure is genuinely irregular):

1. **Feeds and APIs** return structured data already — parse, don't extract. Zero model cost.
2. **Stable HTML** → CSS/XPath selectors or Firecrawl's built-in extraction. Deterministic, cheap, fast.
3. **Irregular/prose content** → schema-constrained LLM extraction with `output_format`. Reliable, structured, costs tokens.
4. **Layout that drifts** → LLM extraction *plus* a drift detector (Thursday) that flags when your selectors silently start returning empty.

The discipline that ties it together: **define the schema first, from what the downstream brief needs**, and make every source — feed, HTML, or prose — populate the *same* schema. That uniform contract is what lets dedup, ranking, and synthesis stay source-agnostic. It's the same "schemas, not regex" principle [[03-wed-rag-as-a-system]] applied to chunking, one layer upstream.

## Experiment — build and pressure-test the extraction front end

Direct Claude Code (45–60 min):

1. **Policy first.** *"For these 4 sources [paste your niche's real sources], fetch each robots.txt and summarize what it permits for an automated reader. Check for a `Crawl-delay`, an `ai.txt`, or AIPREF `Content-Usage` signals. Then classify each source's likely access path: RSS/API available? behind Cloudflare? behind auth/paywall? Recommend a per-source access method consistent with the ethical rules in today's lesson."* This artifact is the top of your Saturday `README`.
2. **Extract against a schema.** *"Define a JSON Schema for a news item: title, url, source, published_at, summary, topics[]. Then, using the Claude API structured-outputs `output_format`, extract that schema from [paste one real article's text or point at its RSS]. Show the guaranteed-conformant JSON."* Confirm it validates; try to break it with a malformed source and watch the schema hold.
3. **Cost the stack.** *"Price a daily crawl of my 4 sources three ways — pure Playwright on a $5 VPS, Firecrawl credits (non-rollover), and Browserbase browser-minutes — at July-2026 rates. Which wins at 1 run/day? At 24 runs/day? What changes the answer?"* Keep the table.
4. **Simulate the door closing.** *"Source 2 now returns a Cloudflare block page instead of content. Show how a well-designed pipeline classifies this (TRANSIENT vs PERMANENT), what it alerts, and how the brief degrades gracefully to 3 sources instead of crashing or shipping empty."* You are pre-building Friday's failure handling.

## Common mistakes experts see

- **Believing "public = free to take."** hiQ narrowed the CFAA; it did not repeal contract, copyright, or the EU's TDM regime.[^8][^9]
- **Spoofing a browser User-Agent to dodge detection.** Converts a civil gray area into a bad-faith, willfulness-tainted one — and September 15's Cloudflare defaults are built to catch exactly this.[^1]
- **Ignoring robots.txt because "it's not binding."** In the EU it can be copyright-relevant; everywhere it's evidence of intent.[^9][^10]
- **Regex against HTML.** Breaks on the next redesign, silently, at 3 a.m. Schema-constrained extraction or typed selectors.
- **Blind re-fetching.** Over half of AI crawl traffic is wasted re-fetches;[^2] use conditional requests and change-tracking or you're paying to be the problem.
- **Assuming credits roll over.** Firecrawl's don't — a burst month bills, a quiet month forfeits.[^4]
- **Scraping personal data in the EU without a GDPR basis.** "Publicly posted" is not a lawful basis; the AI Act and GDPR both bite from August 2, 2026.[^9]
- **No plan for a source going dark.** Sources will block you. Handle it as a first-class event, not a crash.

## Reflection questions

1. One of your niche's sources has no RSS and sits behind Cloudflare. Walk the decision tree: is there an API? a licensing contact? a Search-classified path? At what point do you conclude "this source is not ethically/legally available to me" and drop it — and what would it cost you to be wrong in each direction?
2. hiQ won on CFAA and lost on contract. Write the two sentences of your scraping policy that address *contract* risk specifically — the risk the memes ignore.
3. The EU treats a robots.txt TDM opt-out as copyright-relevant; the US treats it as evidence of intent. Your client sells into both markets. What's the single policy that satisfies the stricter regime, and what does it cost you in coverage?
4. Cloudflare's Search/Agent/Training taxonomy classifies *your* daily-digest scraper as which category — and does the honest answer change whether September 15's defaults block you?
5. You could get 30% more sources by spoofing browsers and ignoring robots.txt. Make the actual business case *against* doing so, in dollars and reputation, as if to a founder who wants the coverage. (If your case is only "it's wrong," you'll lose the argument when revenue is tight.)
6. Structured outputs guarantee schema conformance but conflict with citation blocks. Your brief needs both structured items *and* inline citations. How do you stage the calls so each gets what it needs?

## My take (reviewer lens)

**Simon Willison** — who scrapes constantly and writes about it honestly — would flag the lesson's tone as slightly too pious. His practiced position: a huge amount of valuable, ethical scraping happens on public data for personal and research use, and over-lawyering it scares beginners away from a legitimate, powerful skill. He'd want the disclaimer balanced by permission: *reading public RSS feeds and public articles for a personal digest, identifying yourself and honoring robots.txt, is a normal and defensible thing to do* — the heavy machinery is for scale and for other people's commercial data. Correct, and the lesson should hold both: proportionate caution, not fear.

**Chip Huyen** would attack the cost tables as under-specified in the way that actually bites: they price the fetch, not the *maintenance*. The expensive part of scraping isn't the credit — it's the engineer-hour every time a source redesigns and your extraction silently degrades. A Firecrawl subscription that eliminates selector maintenance can be cheaper than "free" Playwright once you price your own time honestly. The lesson gestures at this in Layer 5's drift point; she'd want it in the cost table as a line item, and she'd be right.

**A publisher-side reviewer** (the Cloudflare/Reddit position embodied) would say the "ethical scraping" section still frames the site as an obstacle to route around politely, when the actual 2026 shift is that content owners have *decided* AI access is theirs to price and permission — and reciprocity (attribution, traffic-back, or payment) is now the entry fee, not a nice-to-have. The lesson endorses attribution, but a publisher would push it further: in the Pay-Per-Use world, the durable move may be to *license* your key sources rather than scrape them, and a course teaching a sellable practice should say when licensing beats scraping outright. Fair — and for a client whose business depends on a handful of high-value sources, that's exactly the call.

## Further reading

**Must-read**

- Cloudflare blog — "Your site, your rules: new AI traffic options for all customers" (the Search/Agent/Training taxonomy and Sept 15 defaults).[^1]
- TechCrunch — "Cloudflare's new policy pushes AI companies to pay for publishers' content" (July 1, 2026).[^3]
- hiQ Labs v. LinkedIn — the Wikipedia summary is an unusually good, sourced primer on how narrow the holding actually is.[^8]

**Recommended**

- Firecrawl — "Introducing Firecrawl v2.5" (Semantic Index, change-tracking, maxAge).[^5]
- Browserbase — Stagehand docs (`act`/`extract`/`observe`/`agent`).[^6]
- Claude Platform docs — Structured outputs (`output_format`, `strict`).[^so]
- IETF — "IETF setting standards for AI preferences" (AIPREF).[^11]

**Optional**

- Playwright 1.61 release notes and the agent-oriented CLI.[^7]
- EU AI Act implementation timeline (August 2, 2026 GPAI enforcement).[^9]

## Citations

[^1]: Cloudflare blog. "Your site, your rules: new AI traffic options for all customers." https://blog.cloudflare.com/content-independence-day-ai-options/ — Search/Agent/Training crawler taxonomy; Training and Agent blocked by default on ad pages for new domains; Pay Per Crawl evolving into Pay Per Use (partners Ceramic.ai, You.com). Corroborated by Cloudflare press release "Cloudflare Allows the Agentic Internet to Flourish..." https://www.cloudflare.com/press/press-releases/2026/cloudflare-allows-the-agentic-internet-to-flourish-with-a-simple-philosophy-your-content-your-rules/ (search-verified 2026-07-17; direct fetch egress-blocked — liveness pass pending).

[^2]: AI-crawler traffic share and re-fetch waste: AI crawlers = 52% of total crawler requests in June 2026 (up from 22% spring 2025); >50% of AI crawl traffic re-fetches unchanged pages — Cloudflare data via PPC.land "Cloudflare ties AI payouts to citations as 50% of crawls waste" https://ppc.land/cloudflare-ties-ai-payouts-to-citations-as-50-of-crawls-waste/ and Digital Applied "AI Crawler & Bot Traffic Statistics 2026" https://www.digitalapplied.com/blog/ai-crawler-bot-traffic-statistics-2026-data-reference (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^3]: TechCrunch. "Cloudflare's new policy pushes AI companies to pay for publishers' content." https://techcrunch.com/2026/07/01/cloudflares-new-policy-pushes-ai-companies-to-pay-for-publishers-content/ — July 1, 2026. September 15 default block of mixed-use crawlers on ad pages; applies to new customers, new sites, and existing free customers. Corroborated by Technology.org "Cloudflare to Block Mixed-Use AI Crawlers on Ad Pages From September 15" https://www.technology.org/2026/07/03/cloudflare-blocks-mixed-use-ai-crawlers/ and Engadget https://www.engadget.com/2207360/cloudflare-will-filter-out-web-crawlers-that-serve-ai-companies/ (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^4]: Firecrawl pricing. https://www.firecrawl.dev/pricing — Free 1,000 credits/mo; Hobby $16/mo / 5,000; Standard $83/mo / 100,000; Growth $333/mo / 500,000; Scale $599/mo / 1,000,000; scrape/crawl/map/monitor ~1 credit/page, JSON extraction +4 credits/page; credits do not roll over. Corroborated by eesel AI "Firecrawl pricing in 2026" https://www.eesel.ai/blog/firecrawl-pricing and Costbench https://costbench.com/software/web-scraping/firecrawl/ (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^5]: Firecrawl. "Introducing Firecrawl v2.5 — The World's Best Web Data API." https://www.firecrawl.dev/blog/the-worlds-best-web-data-api-v25 — Semantic Index (~40% of API calls), `maxAge` "as of now / last known good copy," custom browser stack. Change-tracking: Firecrawl docs https://docs.firecrawl.dev/features/change-tracking (git-diff mode at no extra cost; compares against most recent scrape) (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^6]: Browserbase pricing and Stagehand. https://www.browserbase.com/pricing (Free / Developer $20 / Startup $99 / Scale custom; per browser-minute; residential proxy ~$8/GB, stealth ~$0.30/GB) and https://www.browserbase.com/stagehand (`act`/`extract`/`observe`/`agent` primitives over Playwright, framework integrations). Corroborated by Skyvern "Browserbase vs Stagehand" https://www.skyvern.com/blog/browserbase-vs-stagehand-which-is-better/ (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^7]: Playwright. Releases and release notes. https://github.com/microsoft/playwright/releases and https://playwright.dev/docs/release-notes — v1.61.0 (June 29, 2026) current stable; v1.59 (April 1, 2026) agent-oriented release with Screencast API, CLI debugging, and token-efficient Playwright CLI for coding agents. Corroborated by Bug0 "What's new in Playwright 1.59" https://bug0.com/blog/whats-new-playwright-1-59 (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^8]: hiQ Labs v. LinkedIn. Wikipedia (well-sourced summary). https://en.wikipedia.org/wiki/HiQ_Labs_v._LinkedIn — Ninth Circuit: scraping public data likely not a CFAA violation; case settled 2022 with hiQ paying damages and destroying data after LinkedIn prevailed on contract/unfair-competition grounds. Corroborated by California Lawyers Association "Ninth Circuit Holds Data Scraping is Legal in hiQ v. LinkedIn" https://calawyers.org/privacy-law/ninth-circuit-holds-data-scraping-is-legal-in-hiq-v-linkedin/ and Loeb & Loeb https://www.loeb.com/en/insights/publications/2022/05/ninth-circuit-provides-path-forward-for-web-scraping-of-public-data (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^9]: EU AI Act + DSM Directive Article 4 TDM opt-out. Directive 2019/790 Article 4(3) machine-readable rights reservations; AI Act GPAI obligations to respect TDM opt-outs / robots.txt and publish training-data summaries; GPAI enforcement (fines up to €15M or 3% of global turnover) from August 2, 2026 — per ProxyCove "EU AI Act from August 2, 2026: new scraping rules" https://proxycove.com/en/blog/eu-ai-act-august-2026-web-scraping and Coronium "The EU AI Act in 2026" https://www.coronium.io/blog/eu-ai-act-web-scraping-2026 ; Hamburg court natural-language-ToS question per TechnoLlama https://www.technollama.co.uk/we-need-to-talk-about-the-eu-tdm-exception-and-ai-training (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending). Enforcement date cross-checked against landscape delta §8 (URL-verified 2026-07-17).

[^10]: robots.txt legal status. Not a law/contract/enforceable directive, but courts treat compliance as good faith and non-compliance as willfulness/knowledge; EU Copyright Directive recognizes robots.txt as a TDM opt-out means — ByteTunnels "Is robots.txt Legally Binding?" https://bytetunnels.com/posts/is-robots-txt-legally-binding-scraping-law-explained/ and DataResearchTools "robots.txt in 2026: Legal Requirement Guide" https://dataresearchtools.com/robots-txt-2026-courtesy-to-legal-requirement/ (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^11]: IETF. "IETF setting standards for AI preferences" (AIPREF WG). https://www.ietf.org/blog/aipref-wg/ and vocabulary draft https://datatracker.ietf.org/doc/draft-ietf-aipref-vocab/ — `train-ai`/`search` categories; attachment draft defines a `Content-Usage` header and robots.txt `Content-Usage` rule, August 2026 milestone to IESG; `ai.txt` emerging convention (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^12]: Reddit v. Perplexity. Filed October 2025; honeypot-post evidence, Google-backdoor allegation, co-defendants Oxylabs/AWMProxy/SerpApi; Perplexity motion to dismiss; unresolved as of mid-2026 — Decrypt "Reddit Sues Perplexity AI, Alleging 'Industrial-Scale' Data Theft" https://decrypt.co/345613/reddit-sues-perplexity-ai-alleging-industrial-scale-data-theft and Bloomberg Law "Perplexity Blasts Reddit's 'Daisy Chain' Site-Scraping Claims" https://news.bloomberglaw.com/ip-law/perplexity-blasts-reddits-daisy-chain-site-scraping-claims (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^ws]: Anthropic web search / web fetch tools pricing. Web search $10 per 1,000 searches plus token costs; web fetch token costs only — per Anthropic docs "Web search tool" https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/web-search-tool and WebSearchAPI.ai breakdown https://websearchapi.ai/blog/anthropic-claude-web-search-api (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^so]: Anthropic. Structured outputs — Claude Platform docs. https://platform.claude.com/docs/en/build-with-claude/structured-outputs — GA across Fable 5 / Opus 4.8 / Sonnet 5 / Haiku 4.5 etc.; `output_format` JSON-schema mode compiled to a grammar and cached ~24h; `strict: true` for tool args; citation blocks conflict with strict schema (returns 400). Corroborated by Thomas Wiegold "Claude API Structured Output" https://thomas-wiegold.com/blog/claude-api-structured-output/ (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

_last_verified: 2026-07-17_
