---
type: review
phase: 2
week: week-15
reviewer: multi-persona 13-lens
date: 2026-07-17
---

# Week 15 — Phase 2 Multi-Persona Review (+ surgical polish applied)

Scale 1–10. Weights: Karpathy / Hamel / Simon = 1.0; the other ten personas = 0.8 (total 11.0). Reviewed cold against `quality-standard.md`, `.claude/block-6-briefs/_generator-base.md` (anti-slop + canonical-home map + amended verification protocol), and `week-15-briefs.md`.

Mechanical checks run this session: `python3 -m py_compile checklist.py personalizer.py compliance.py` — **clean**. `checklist.py --plan launch_plan.sample.json` prints NO-GO listing the five incomplete blocking items and **exits 1** as claimed. `personalizer.py` on the sample: **Priya (US, strong signal) and Tom (EU, LIA=true) draft 3 touches each; Dana blocked `NO_SIGNAL`; Sam blocked `UPVOTE_ASK`** — every gate fires exactly as the Saturday lesson and README claim. `personalizer.py --send` **refuses and exits 3**. Config gate (CAN-SPAM address + opt-out) and the EU-LIA gate both confirmed by inspection and by flipping fields. All 9 distinct wikilink targets resolve to real vault files (b1w01, b1w02 ×2, b3w08, b4w09 ×2, b4w10 ×2, and the same-week Thu). **No `(pending)` markers** anywhere — this week has no forward links into Weeks 16/17 (which exist), so no upgrades were needed. Em-dash density 4.3–11.3/1k across all eight files (under the ~12 bar; Sun 11.3 and Fri 10.7 are the ceilings, acceptable). Contrast-scaffold tics: seven files at ≤2; **Wed was at 3 — trimmed to 2 this session**. Internal-consistency audit (dailies vs Sunday vs code-lab, all reproduce identically): PH AI-share 5%→40%, avg upvotes ~190→144, ~1-in-10 Featured, ~70% non-featured traffic penalty, PH traffic bands (top-3 5–15K/100–400 signups, top-10 1–3K, sub-top-10 <500), velocity 25–50/hr, 40-comments>800-upvotes, ~89% top-5 reply; cold-email reply ~3.4%, opens ~27.7/28% (from ~36%), ~17% never-inbox, signal-based 15–25% (~5×), CAN-SPAM $517+/email; LinkedIn 41% machine-written, link penalty 30–50%; GEO 31.3% adoption, quotes +41% / stats +30% / citations +30%, ChatGPT ~30%-from-Google-top-10, 11% ChatGPT/Perplexity domain overlap; HN 8–10 upvotes + 2–3 comments/30min, 30–50/hr for front page; recurring triage example 40%-tickets and 14h→1.1h — all consistent across every file where they appear. Canonical homes checked against the brief's map: b1w02 (algorithm state + build-in-public), b4w10 (launch page/instrumentation + creative stack), b4w09 (packaging + distribution-surface take-rates), b3w08 (scraping/consent ethics), b1w01 (outbound mechanics) are each one-line-recapped and wikilinked, never re-taught. Mon, Wed, Thu, Fri each state explicitly that they build on the prior lesson rather than re-teach it.

**NAME-VERIFICATION (required this week):** three non-core-roster named entities, all real and correctly attributed — no "Max Freiberg" repeat.

- **Pieter Levels** — indie hacker (Nomad List, Remote OK, Photo AI). Wed cites him for PhotoAI reaching six figures/month "with no Product Hunt launch, no Hacker News submission, no press release — just Twitter" and a distinctive voice. Corroborated ≥2 independent domains (indiehackers.com deep-dive, thebootstrappedfounder.com). The lesson correctly frames it as a product-shipper's path and cross-references b1w02's faucet caveat — accurate. **Verified.**
- **Justin Welsh** — LinkedIn solopreneur/creator, used in Wed only as the "you don't have this many followers" foil. Corroborated ≥2 domains (linkedin.com/in/justinwelsh, growthinreverse.com, favikon). The "360k" figure is his 3.5-year milestone; he is now ~853k (2026), so the number is stale but understates — the rhetorical point is unaffected. **Verified (see concern 2).**
- **GEO paper (Aggarwal, Murahari, Rajpurohit, et al.), KDD 2024, arXiv:2311.09735** — real, correctly attributed; corroborated by Princeton, dblp, and the arXiv PDF. Reported figures (quotes ~+41%, statistics/citations ~+30%, keyword-stuffing hurts) match the paper's method families. **Verified.**

---

## 00-overview

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | "Launch is a demand-gen event, not a switch" is the real mechanism, stated up front. |
| Chip Huyen | 8 | Day table maps each day to a concrete artifact and the through-line question. |
| Jerry Liu | 8 | Correctly subordinates every surface to the "where is my buyer" decision. |
| Hamel Husain | 8 | "Revenue signal and a warm list, not a spike and a feeling" is a measured bar. |
| Simon Willison | 8 | Every fast-moving stat carries a search-verified stamp, not hype. |
| Seibel | 9 | Sells the week in two paragraphs; the through-line is the right operating question. |
| Boris Cherny | 8 | Points at the code-lab's draft-not-send discipline without over-explaining. |
| Cohort peer | 8 | The switch-vs-motion reframing lands for a first-time launcher. |
| Mira Murati | 7 | Commercial framing sound; light on capability-frontier context. |
| swyx | 8 | The "surfaces changed shape since 2024" meta-point signals non-naivety. |
| Ethan Mollick | 8 | "Study one day, study Saturday" is real behavior design. |
| Lilian Weng | 8 | Terminology (portfolio, spike/compounding, assets) consistent with dailies. |
| Jeremy Howard | 8 | Prereq wikilinks (b4w09/b4w10, b1w02) carry the load correctly. |

**Weighted average: 8.1**

---

## 01-mon — What "launch" means in 2026

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | Switch→continuous reframing is a genuine model shift, not a slogan; failure-chain is honest. |
| Chip Huyen | 8 | Pre-registered floor/median/ceiling distribution is the correct discipline. |
| Jerry Liu | 8 | Portfolio-as-jobs framing is a spec, not a vibe. |
| Hamel Husain | 8 | Experiment pass bar forces a named Skip and a bettable median. |
| Simon Willison | 8 | PH bands flagged "directional, analyst blogs" — correct hedge. |
| Seibel | 9 | His "go talk to 20 customers" pushback IS the reviewer lens and Position A. |
| Boris Cherny | 8 | Tooling risk deferred to Tue where it belongs. |
| Cohort peer | 8 | "Assets and a warm list, not traffic" is the honest reframing. |
| Mira Murati | 7 | Little on how the surface map shifts with product maturity; defensible. |
| swyx | 8 | His "narrative is the real output" objection is named and forwarded to Wed. |
| Ethan Mollick | 8 | His "re-derive the map from buyer attention" caveat is in the lens. |
| Lilian Weng | 8 | Three-phase motion (pre/launch/post) consistent with Sunday's cards. |
| Jeremy Howard | 8 | b4w10/b4w09 recapped in one line, wikilinked, not re-taught. |

**Weighted average: 8.1**

---

## 02-tue — The Product Hunt playbook, honestly

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | The mechanism (velocity × credibility × comment-depth × editorial gate) is the real system, not "get upvotes." |
| Chip Huyen | 8 | Ranking signals quantified (25–50/hr, ~89% reply, ~1-in-10) with directional hedges. |
| Jerry Liu | 8 | First-comment framed as the highest-leverage asset with a concrete spec. |
| Hamel Husain | 9 | His cherry-picked-demo warning is the lens; experiment demands a typical/hard run. |
| Simon Willison | 8 | Uses PH's own help-center as primary source for the rules, not a blog. |
| Seibel | 8 | His "is the apparatus worth the day" pushback bounded to PH-as-Secondary. |
| Boris Cherny | 9 | His "growth/auto-upvote tools are account-risk generators" pushback is the sharpest lens. |
| Cohort peer | 8 | Hour-by-hour worked example is directly copyable. |
| Mira Murati | 7 | Vertical-novelty point sound; light on frontier framing. |
| swyx | 8 | Show HN mechanics current and correctly differentiated from PH. |
| Ethan Mollick | 8 | Adversarial "PH editor + skeptic" Claude drill is real behavior design. |
| Lilian Weng | 8 | Prohibited/legitimate taxonomy consistent with Sunday's cards. |
| Jeremy Howard | 8 | b4w10 creative-stack wikilinked with the slop caveat, not re-taught. |

**Weighted average: 8.3**

---

## 03-wed — Social launch strategy

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | "Launch-day outcome is pre-determined by the pre-launch list" is the real mechanism. |
| Chip Huyen | 8 | Algorithm constraints turned into concrete launch-sequence design inputs. |
| Jerry Liu | 8 | Five-post sequence is a structured artifact, not "post more." |
| Hamel Husain | 8 | Demo-video "typical not best run" rule has a credibility rationale. |
| Simon Willison | 9 | His reproducible-demo pushback is the sharpest lens; format-vs-content tension named. |
| Seibel | 8 | "Concentrate, don't spread" is his instinct for a small operator. |
| Boris Cherny | 8 | Link-in-comment pattern is the concrete tooling discipline. |
| Cohort peer | 8 | The "what if you have no receipts at N=0" objection is answered honestly. |
| Mira Murati | 7 | Platform-mechanics-heavy; light on capability framing. |
| swyx | 8 | Build-in-public-as-launch-instrument is the right 2026 read. |
| Ethan Mollick | 8 | His "would this teach something true even if they never buy" test is the lens. |
| Lilian Weng | 8 | 41%/link-penalty figures consistent with b1w02 and Sunday. |
| Jeremy Howard | 8 | b1w02 algorithm state recapped, explicitly not re-taught. |

**Weighted average: 8.1**

---

## 04-thu — Cold outreach post-AI-slop

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | Bifurcation thesis (generic dead / precise better) is the correct mechanism-level read. |
| Chip Huyen | 8 | Benchmarks set the strategy; precision-over-volume derived, not asserted. |
| Jerry Liu | 8 | AI-for-research-not-blasting line is the durable distinction. |
| Hamel Husain | 9 | His "qualified positive replies at N=16 is qualitative, not a rate" pushback is the lens. |
| Simon Willison | 9 | His draft-for-review line named as the lesson's thesis made executable in the lab. |
| Seibel | 9 | His "don't hide from sales inside DMARC setup" pushback is the reviewer lens. |
| Boris Cherny | 8 | Deliverability hygiene framed as operational discipline, not fear. |
| Cohort peer | 8 | Worked example (16 emails + 4 warm intros) is concrete and executable. |
| Mira Murati | 7 | Compliance-heavy; light on frontier context, defensible for the topic. |
| swyx | 8 | Signal-based outbound landscape current. |
| Ethan Mollick | 8 | Measure-positive-reply-not-open is real behavior design. |
| Lilian Weng | 8 | CAN-SPAM/GDPR/LinkedIn taxonomy consistent with the code-lab gates. |
| Jeremy Howard | 8 | b1w01 outbound + b1w02 policy wikilinked, not re-taught. |

**Weighted average: 8.3**

---

## 05-fri — Communities, directories, earned distribution

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | Spike-vs-compounding is the right structural decomposition of the portfolio. |
| Chip Huyen | 8 | GEO measurement (weekly citation log, week 8–10) is a concrete method. |
| Jerry Liu | 9 | His "answer engines are RAG; only real authority survives" pushback is the sharpest lens. |
| Hamel Husain | 8 | GEO first-pass has a measurable week-0 baseline bar. |
| Simon Willison | 8 | GEO paper used as the primary; vendor GEO tools correctly deferred. |
| Seibel | 8 | His "compounders compound slowly, pre-revenue needs the spike" pushback is the lens. |
| Boris Cherny | 8 | No-automation community rule tied to b3w08 consent ethics. |
| Cohort peer | 8 | Give-before-take framed as an entry requirement, not a nicety. |
| Mira Murati | 7 | Directory/GEO tactical; light on frontier. |
| swyx | 8 | GEO/AEO/SEO distinction is the current 2026 vocabulary, used with skepticism. |
| Ethan Mollick | 8 | His "compounders may be becoming primary" reframing is named. |
| Lilian Weng | 8 | 31.3%/+41%/11%-overlap figures consistent with overview and Sunday. |
| Jeremy Howard | 8 | b4w09 take-rates + b3w08 ethics wikilinked, not re-taught. |

**Weighted average: 8.1**

---

## 06-sat — BUILD: the launch plan + go live

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | "Plan as dated checkable items, not a strategy doc" is the right discipline; maps to the lab. |
| Chip Huyen | 8 | Blocking/optional distinction with a non-zero-exit gate is measurable. |
| Jerry Liu | 8 | Personalizer wires exactly the Thursday motion, not a generic tool. |
| Hamel Husain | 9 | His "zero-NO_SIGNAL is necessary-not-sufficient; a present signal can be weak" pushback is the lens and the pass bar's honest limit. |
| Simon Willison | 8 | Draft-for-review architecture is the thesis in code; verified refuses to send. |
| Seibel | 8 | His "did the tool steal time from customers" test applied and answered per-tool. |
| Boris Cherny | 9 | His "checklist bool is theater; point items at evidence" pushback is the sharpest lens, flagged as a safe extension. |
| Cohort peer | 8 | Stranger-executability test is the discipline most build-days skip. |
| Mira Murati | 7 | No model-choice stage; inherited, defensible. |
| swyx | 8 | Self-hunt-at-12:01-PT + phased plan is the correct ship shape. |
| Ethan Mollick | 8 | Stranger test is a real behavior check ("could someone run it if you got sick?"). |
| Lilian Weng | 8 | Phases (T-7…T+14) consistent with the sample plan and the checklist output. |
| Jeremy Howard | 8 | b4w10 decision-bands + Thursday wikilinked forward. |

**Weighted average: 8.2**

---

## 07-sun — Synthesis + quiz + flashcards

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | Synthesis compresses to "substance beats slop, precision beats volume" — the real through-line. |
| Chip Huyen | 8 | Q5/Q8 force the code-lab's gate semantics, not recall. |
| Jerry Liu | 8 | Four-controversy "where to land" section keeps positions defensible. |
| Hamel Husain | 8 | Answer key precise; scoring bands direct rereads to weakest days. |
| Simon Willison | 8 | Q7/Q11 reward the AI-for-research and evidence-over-keyword rules exactly. |
| Seibel | 8 | Post-mortem prompt converts the week into a concrete next action. |
| Boris Cherny | 8 | Q8 personalizer-refuses answer matches Saturday and the code. |
| Cohort peer | 9 | 15-question quiz + 34 cards calibrated; cold-quiz instruction correct. |
| Mira Murati | 7 | Forward pointers commercial; no frontier note. |
| swyx | 8 | GEO/AEO/SEO card current. |
| Ethan Mollick | 8 | "How the days connect" schedules the mental model. |
| Lilian Weng | 8 | All 34 cards checked against weekday lessons; no contradictions. |
| Jeremy Howard | 8 | No duplicate territory with earlier quizzes; builds forward. |

**Weighted average: 8.0**

Consistency audit (Sunday vs weekdays vs code-lab, all identical): confirmed for every figure listed in the header. Quiz (15Q + key) and flashcards (34) all trace to weekday lessons; Q5/Q8/Q9/Q10 and cards 31–32 trace precisely to the verified code-lab behavior.

---

## code-lab/06-launch-runner (README, requirements, config, sequence_template, prospects.sample, launch_plan.sample, checklist.py, personalizer.py, compliance.py)

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 9 | Zero-dependency stdlib Python; every gate readable; the SSE-free simplicity is the point. |
| Chip Huyen | 8 | Blocking/optional and per-gate findings give a real readiness signal. |
| Jerry Liu | 8 | Compliance gates map 1:1 to the Thu/Tue rules; lesson→code table honest. |
| Hamel Husain | 9 | `py_compile` clean; four sample prospects exercise every gate exactly as documented. |
| Simon Willison | 9 | Draft-to-`./drafts/`, never send; `--send` refuses (exit 3); footer/opt-out enforced before write. |
| Seibel | 8 | Personalizer directly serves "talk to 20 customers"; checklist forces specificity, no gold-plating. |
| Boris Cherny | 9 | Blast radius bounded: automates the reversible (render/check), hard-stops the irreversible (send). |
| Cohort peer | 8 | README runnable top-to-bottom; sample teaches by blocking Dana and Sam. |
| Mira Murati | 7 | No LLM backend wired; correctly left as a guarded extension. |
| swyx | 8 | Standard-library-only, offline-runnable; correct floor pinned (3.10+). |
| Ethan Mollick | 8 | Pass bar ties tool output to a human-judgment step the tool cannot do. |
| Lilian Weng | 8 | Gate taxonomy (NO_SIGNAL, GDPR_EU_NO_LIA, UPVOTE_ASK, CAN-SPAM) consistent with the lessons. |
| Jeremy Howard | 8 | Small, deterministic, no network; compiles clean. |

**Weighted average: 8.4**

---

## Overall Week 15: **8.2 / 10**

(File averages: 8.1, 8.1, 8.3, 8.1, 8.3, 8.1, 8.2, 8.0, code-lab 8.4.) Strongest: Thursday, Tuesday, and the code-lab — reviewer lenses that genuinely argue against the text (Simon and Hamel on N=16 outbound being qualitative not a rate, Boris on checklist-theater and auto-upvote tools, Jerry on answer-engines-as-RAG) and a lab that compiles clean and demonstrates the exact draft-not-send discipline the week preaches, with every documented gate firing on the sample. Anti-slop: em-dash 4.3–11.3/1k (under ~12); contrast-tics ≤2/file after trimming Wed; house tics inside budget. Canonical homes (b1w01, b1w02, b3w08, b4w09, b4w10) all wikilinked with one-line recaps — no re-teaching found. All three non-core names (Pieter Levels, Justin Welsh, GEO paper authors) verified real and correctly attributed.

---

## Surgical fixes applied this session (Phase 3, done)

1. **03-wed Layer intro:** "a verifiably human founder voice is not a nicety; it is your cheapest competitive edge" → "a verifiably human founder voice is your cheapest competitive edge, well beyond a nicety" (contrast-scaffold-tic trim, 3→2 for the file; meaning preserved).

No wikilink upgrades needed — all 9 targets resolve to existing files, no `(pending)` markers present, and this week carries no forward links into Weeks 16/17. No git commits made.

## Unresolved concerns (recommendations, not applied)

1. **Fast-moving facts carry `search-verified … fetch egress-blocked — liveness pass pending` stamps** per the amended protocol, and the PH traffic bands and cold-email benchmarks are correctly hedged as "directional / analyst-blog / vendor-benchmark." A Phase-4 liveness pass should re-hit the live URLs for: PH Featured-rate and traffic bands (Causo/Puthusu/LaunchPact), cold-email benchmarks (Instantly/Amplemarket/Mailforge), GEO adoption + citation figures (eMarketer/Jasper), and the Poindeo ranking specifics (25–50/hr, ~89% top-5, +166% first-comment).
2. **Justin Welsh's "360k" (Wed, Layer 5) is stale** — that was his ~3.5-year milestone; he is ~853k on LinkedIn in 2026. The figure only serves as a "you don't have this many followers" foil so the point holds, but a Phase-4 pass could update it or drop the number. Left unfixed to avoid substituting an unverified precise figure into a rhetorical aside.
3. **Several 2026 practitioner sources are secondary/SEO-tier** (Exponanta, Crawlora, Poindeo, Foundra, Puthusu, Causo, Naypache, Surmado, Frase, Sendr, Mailforge, Litemail, etc.). Load-bearing figures are each corroborated across two domains and hedged directionally, and the two strongest claims lean on primaries (PH help-center for the rules, the arXiv GEO paper for the citation lifts). Phase-4 could hunt stronger primaries for the PH traffic distribution and the cold-email reply benchmarks, or keep the directional framing.
4. **Minor cosmetic in `personalizer.py`:** Sam's `UPVOTE_ASK` block prints twice (the `{signal}` renders into both touch-1 subject and body, and findings accumulate across touches before the prospect is reported). Behavior is correct (prospect is blocked); only the duplicated console line is redundant. Not worth a code change at this scope — flagged for awareness.

---

_Review + surgical polish produced 2026-07-17. File edited: 03-wed-social-launch-strategy.md. No git commits made._
</content>
</invoke>
