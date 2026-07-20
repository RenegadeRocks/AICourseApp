---
type: refresh-report
date: 2026-07-17
scope: all 9 built weeks (blocks 0-2), ~430K words
reviewers: 11 parallel agents — 9 per-week multi-persona reviewers (13 lenses), 1 vault-wide slop/repetition census, 1 landscape-delta researcher
---

# July 2026 Content Refresh — Master Findings Report

All 9 built weeks were generated 2026-04-14→18 and reviewed 2026-07-17.
Detailed per-week findings live in each week folder as `_refresh-2026-07.md`.
Cross-cutting inputs: `_refresh-2026-07-landscape-delta.md` (what changed
Apr→Jul 2026, URL-cited) and `_refresh-2026-07-slop-census.md` (slop patterns,
repetition map, slopsquatting sweep).

## Overall verdict

**The course's skeleton is sound; its skin is three months old in a field that
molts monthly.** Frameworks, mechanistic explanations, failure taxonomies, and
eval discipline consistently graded A-range across reviewers. The decay is
concentrated in exactly the layer a reader touches: model names, prices,
benchmarks, tool features, commands, and API surfaces. Several findings are
worse than drift — wrong at write time (Opus pricing 3× off, a deprecated
vulnerable MCP server taught as canonical, math that doesn't compute) — and a
recurring failure mode is that **April's own `_review.md` polish targets were
scored, filed, and never applied.**

## Severity totals

| Week | Grade | CRITICAL | MAJOR | Citation issues | Worst finding |
|---|---|---|---|---|---|
| b0 w00 onboarding | C− | 12 | 17 | ~13 | New tokenizer (+30% tokens) invalidates cost-math layer; quiz inverts its own week's lesson |
| b0 w01 prompting/RAG/vibe | C+ | 5 | 13 | ~15 | Invented arXiv author names; Karpathy tweet misdated + content inverted |
| b0 w02 MCP/voice/n8n | C+ | 4 | 7 | ~3 | MCP-vs-A2A controversy inverted by Linux Foundation events |
| b0 w03 business problems | C | 7 | 14 | ~13 | Opus priced $15/$75 vs cited page's $5/$25 — 3× COGS error in the cost curriculum |
| b1 w01 first client | B− | 4 | 13 | 8 | Fable 5 pricing breaks pass-through examples; Sun contradicts Tue with inverted stats |
| b1 w02 branding/niche | C+ | 6 | 14 | ~12 | X ranker rewrite makes posting advice counterproductive; exercises now breach LinkedIn policy |
| b2 w03 landing pages | C+ | 12 | 14 | ~20 | Tool-comparison lesson a "landscape fossil" (D+); CI kill-rule arithmetically false |
| b2 w04 sales/RAG agent | C+ | 5 | 13 | 14 | Artisan's 10× price cut invalidates seat-floor advice; experiments pin legacy models |
| b2 w05 report generator | C+ | 5 | 11 | 11 | Hands-on build on deprecated, SQL-injectable Postgres MCP server; fabricated McCardel quote (April P0, unfixed) |
| **Totals** | **C+** | **60** | **116** | **~110 spot-checked, ~35 problematic** | |

Slop census: no slopsquatting (all named products/packages verified real), no
classic slop vocabulary. House tics instead: "would push back" ×172,
"load-bearing" ×126, "operator" ×650, em-dash density 9–20/1k words everywhere.
Contrast-scaffold tic over threshold in ~60% of files. Root structural problem:
wikilink discipline collapsed (4 weeks have zero), so later weeks re-teach
instead of linking — Contextual Retrieval ladder taught AND quizzed twice, MCP
re-introduced from scratch in b2w05, "95% of pilots fail" in four weeks.

## Cross-cutting themes (every fix agent must internalize)

1. **Model landscape is 1–3 generations stale everywhere.** Current lineup
   (web-verified, two-source): Anthropic — Claude Fable 5 / Mythos 5 (Jun 9,
   $10/$50 per Mtok, 1M ctx, GA Jul 1 after a June export-directive suspension;
   new Mythos-class tier ABOVE Opus), Opus 4.8 (May 28, $5/$25), Sonnet 5
   (Jun 30, new default, $2/$10 intro), Haiku 4.5. New tokenizer on Opus
   4.7+/Sonnet 5/Fable: ~+30% tokens — all cost math changes. OpenAI —
   GPT-5.5 (Apr 23, 1M ctx), GPT-5.6 Sol/Terra/Luna (GA Jul 9). Google —
   Gemini 3.1 Pro (3.5 Pro announced, NOT GA). Open-weight frontier — Kimi K3
   (Jul 16), Thinking Machines Inkling (Jul 15). NOT released (do not teach as
   fact): Gemini 3.5 Pro GA, Grok 5, DeepSeek R2.
2. **Coding-agent market restructured:** Cursor acquired by SpaceX ($60B,
   Jun 16); Windsurf → Devin Desktop; Copilot → usage-based AI Credits
   (Jun 1); Claude Code programmatic usage → API-rate credit pools (Jun 15);
   OpenAI Codex at 5M weekly users. All April-era teardowns/anecdotes affected.
3. **MCP:** governed by Linux Foundation's Agentic AI Foundation (Dec 2025,
   with A2A — the "A2A faded" story is inverted); official Registry live;
   spec 2025-11-25 shipped (Tasks/OAuth); 2026-07-28 stateless-core RC is
   SCHEDULED, frame as upcoming. Security literature now quantified (OWASP
   Agentic Top 10 Jun 2026, CVE-2025-6514, postmark-mcp supply-chain incident,
   Datadog Postgres-MCP SQLi).
4. **Discourse shifts:** vibe-coding-without-review discredited (Veracode 45%
   vuln rate; "agentic engineering" reframe); LinkedIn actively demoting
   AI-generated outreach (exercises must be rewritten to comply); X ranker now
   Grok-based with diversity caps; EU AI Act fully applicable Aug 2, 2026.
5. **Anthropic entered the analyst-worker market** (Claude for Financial
   Services agent templates, May 5) — build-vs-buy framing changes in b2.
6. **Citation hygiene debt:** invented author names on real arXiv papers,
   fabricated/misattributed quotes, relative-vs-absolute stat distortions,
   numbers hung on URLs that say otherwise. Every fix must re-verify the
   citation it touches; never propagate a findings claim without its URL.

## Canonical-home dedup map (fix agents follow this)

| Repeated item | Canonical home | Everyone else |
|---|---|---|
| Contextual Retrieval ladder (5.7→2.9→1.9%) | b0w01 RAG lessons | b2w04 thu: wikilink + one-line recap; delete duplicate quiz items in b2w04 sun |
| MCP introduction | b0w02 mon | b2w05 wed: wikilink, cut re-teach |
| Lethal trifecta (Willison, coined Jun 16 2025) | b0w02 wed (security) | b2w05 wed: single mention + wikilink (also fix its internal double-explain) |
| MIT NANDA "95% of pilots fail" | b0w03 (when-AI-fits) | one-line + wikilink elsewhere; max 1 use per week |
| Brex/Ramp examples | first thorough use per block | later uses must add new information or link back |
| "sharp generalist" opener (b2w05) | keep once | vary the rest |

## Reviewer roster (updated July 2026)

Original: Karpathy · Chip Huyen · Jerry Liu · Hamel Husain · Simon Willison ·
Michael Seibel · Boris Cherny · cohort peer. Added this cycle: **Mira Murati**
(Thinking Machines — Tinker + open-weight Inkling shipped Jul 2026; lens:
customization beats generality) · **swyx** (AI-engineering zeitgeist) ·
**Ethan Mollick** (adoption research) · **Lilian Weng** (agent architectures)
· **Jeremy Howard** (pedagogy, anti-hype). Note for future lens accuracy:
Karpathy is now at Anthropic (pretraining); Boris Cherny's current public
record is fleet-scale agent management (Fortune, Jun 2026).

## Fix-phase plan

One fix agent per week, armed with: this report, the week's
`_refresh-2026-07.md`, the landscape delta, the slop census, and
`quality-standard.md`. Rules of engagement:

- Fix ALL CRITICALs and MAJORs; apply citation corrections; execute the dedup
  map; restore ≥2 wikilinks per lesson; reduce house tics in edited passages;
  rewrite (not patch) any file graded D-range; make Sunday synthesis/quiz/
  flashcards consistent with the fixed weekday lessons.
- Every new fact entering a lesson must be re-verified by the fix agent via
  live web search — findings files are leads, not truth; anything marked
  "suspected/unverified" must be confirmed or dropped.
- Future-dated items stay future-framed (MCP RC Jul 28, EU AI Act Aug 2,
  Bolt v1 deletion Aug 3).
- Update `_last_verified: 2026-07-17` on every touched lesson.
- Do not edit `_review.md` (historical record) or `_refresh-2026-07.md` (input).

Follow-up debt recorded: b2w03 dead-link checks incomplete (reviewer hit web
budget); several vendor domains 403'd through the proxy (verified via search
instead) — fix agents should retry direct fetches on the specific URLs they
rely on.
