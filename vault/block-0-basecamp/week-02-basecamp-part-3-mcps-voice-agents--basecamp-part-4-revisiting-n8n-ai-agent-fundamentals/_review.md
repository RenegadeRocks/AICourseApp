---
type: review
phase: 2
week: week-02
reviewer: multi-persona (Karpathy / Chip Huyen / Jerry Liu / Hamel Husain / Simon Willison + cohort peer)
spec: feedback_l3_content_spec.md
date: 2026-04-15
---

# Week 2 — Phase 2 Multi-Persona Review

Probe passed: 3 WebSearches (MCP spec, n8n 2026, voice latency) + 1 Read (L3 spec) + 1 Write (this file) all succeeded.

Scoring scale: 1-10. Weighted average gives Karpathy / Hamel / Simon each 1.0 weight; Chip, Jerry, and the peer each 0.8 — 5.4 total.

---

## 01-mon — MCP as a protocol

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 9 | Wire shape, four primitives, and transport deltas are named concretely; handshake JSON is correct; LSP analogy is engaged *and* critiqued. |
| Chip Huyen | 8 | Production server teardowns (GitHub, Notion, Supabase) with specific ops costs; token-budget implications named; missing cost-per-1k-tokens comparison for hosted vs local. |
| Jerry Liu | 8 | Fat-vs-thin surfaces later; here the spec is accurately scoped, A2A-vs-MCP tradeoff clean. Slight docs-adjacency in the spec recap section. |
| Hamel Husain | 7 | Step 5 regression harness is a real eval gesture, but "record refusal rate" isn't operationalized with N, confidence, or acceptance threshold. |
| Simon Willison | 10 | Cites his own April-2025 post, names lethal-trifecta-in-MCP form, walks the Invariant exfiltration attack end-to-end, acknowledges protocol can't fix it. |
| Cohort peer | 9 | Reads as expert peer-to-peer; domain examples mostly dev-centric but the "connect Claude Desktop to Notion in 5 min" framing lands for any field. |

**Weighted average: 8.4**

### Top 3 polish targets
1. **Layer 2, "Wire shape" JSON block (~line 98-112):** the handshake sample is good but lacks a one-line annotation showing where `protocolVersion` negotiation downgrades; add *"If server returns an older `protocolVersion`, the client speaks that version for the rest of the session."* (≤2 lines).
2. **Experiment Step 5 (~line 303):** "Have Claude Code write a small eval harness" — specify N=10 benign, N=10 injection; refusal-rate acceptance threshold (e.g., ≥95%). Currently vibes.
3. **Layer 4, Discovery section (~line 180):** add a single sentence naming the MCP Registry proposal (shipped Nov 2025 per the 2026 roadmap) so the section isn't stale.

### Citations to verify (Phase 4)
- [^13] InfoQ "OpenAI Adds Full MCP Support to ChatGPT Developer Mode" — October 2025. Verify URL resolves; confirm tier list (Pro/Plus/Business/Enterprise/Education).
- [^11] Invariant Labs disclosure date "May 26, 2025" — verify exact date of blog post.
- [^8] GitHub blog changelog URLs dated 2025-12-10 and 2026-01-28 — both post-cutoff-adjacent, verify.

---

## 02-tue — Building an MCP server

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | Schema-as-prompt section is mechanistic and right; TypeScript example is load-bearing; token-cost math for Playwright/Chrome DevTools concrete. |
| Chip Huyen | 9 | TRANSIENT/PERMANENT error convention with inline retry instructions is production-grade; Notion teardown has the right shape. |
| Jerry Liu | 9 | Fat-vs-thin controversy engaged with numbers (Reinhard 28% lift) and positions *both sides*; Markdown-as-interchange is a genuine insight. |
| Hamel Husain | 7 | P4 error-semantics problem asks for N=10 but no rubric; "eval harness for MCP" is gestured at as Wed's job, which is reasonable but leaves today light on measurement. |
| Simon Willison | 9 | Supabase lethal-trifecta war story retold with specifics; "defaults are policy" is sharp; tool-poisoning path named. |
| Cohort peer | 9 | 67k-token opening-state war story is vivid and actionable; Linear 21-tool example is the right second data point. |

**Weighted average: 8.4**

### Top 3 polish targets
1. **Layer 1, Reinhard citation [^3]:** the "28% higher task-completion" number needs a benchmark name or a link-visible methodology snippet; currently a blog cite doing heavy lifting. Add one line: *"Reinhard ran N=X tasks across Y domains using Z scoring."*
2. **Operator war stories, "67k-token opening state" (~line 309):** attribution is "a widely-shared Aakash Gupta thread in late 2025" — add an actual link or date to de-vibe the claim.
3. **Problem set P4 (~line 303):** specify success metric: e.g., "≤2 retries on TRANSIENT, 0 retries on PERMANENT across 10 trials." Currently "measure" without a bar.

### Citations to verify (Phase 4)
- [^3] Jannik Reinhard blog 2026-02-22 — verify URL and the 28%/13.7k/18.0k numbers.
- [^16] Claude Opus 4.5 release date 2025-11-24 — confirm against Anthropic news page.
- [^14] Linear MCP changelog 2025-05-01 — verify the "~21 tools" count.

---

## 03-wed — MCP security

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | Mechanism clarity on why models can't distinguish user-instruction from tool-output is sound and grounded in Week 1's post-training framing. |
| Chip Huyen | 9 | Mitigation-stack table with friction/fit is production-shaped; 66% AgentSeal finding anchors the "this is live" claim. |
| Jerry Liu | 7 | Not retrieval-heavy by nature; the multi-server threat model is the agent-tradeoff equivalent and handled well. |
| Hamel Husain | 8 | Layer 5 threat-modeling exercise is concrete; audit-log design in the reflection questions is real; missing an explicit red-team eval cadence. |
| Simon Willison | 10 | This is his beat. Lethal trifecta mapped onto MCP primitives precisely; CVEs cited with numbers; reviewer lens explicitly notes his "remove one corner" position. |
| Cohort peer | 9 | Company-support-agent walkthrough is exactly the "first week as AI catalyst" scenario; attack paths named concretely. |

**Weighted average: 8.5**

### Top 3 polish targets
1. **Layer 2, "Claude Code hook CVE" section (~line 96-104):** CVE-2026-21852 is dated "January 2026" and CVE-2025-59536 fix is dated "2025-09-22"; double-check these against Check Point's actual disclosure page. Numbers very specific, high-stakes if wrong.
2. **Layer 4.3 sandboxing table (~line 184):** the table is good but "sandbox-runtime" October 2025 claim needs a link to the npm package or Anthropic launch post in-text, not just citation.
3. **Runnable experiment Step 1 (~line 256):** the injected-instruction sample is fine but add an explicit note that readers should not run this against a production MCP or their own private filesystem — make the isolation instruction first-class, not implied.

### Citations to verify (Phase 4)
- [^4] Check Point Research URL "/2026/rce-and-api-token-exfiltration-.../" — verify this disclosure URL and both CVE IDs (CVE-2025-59536, CVE-2026-21852).
- [^10] "1,643 downloads" for counterfeit postmark-mcp — verify number.
- [^14] AgentSeal "1,808 MCP servers, 66% had findings" — verify both numbers.

---

## 04-thu — Voice agents architecture

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 7 | Pipeline decomposition is clean; 800ms budget table is concrete. Author's own reviewer-lens note admits the "300ms unconsciously notice" threshold is a citation loop — good honesty but leaves a known weakness. |
| Chip Huyen | 10 | This is the strongest lesson on cost/latency honesty in the week: per-stage budget table, telephony vs web split, real pilot failure numbers, unit-economics of $0.30-0.50/min vs $0.02-0.06/min. |
| Jerry Liu | 8 | Pipelined-vs-end-to-end controversy engaged with balanced positions; "hybrid is increasingly common" is the right-shaped answer. |
| Hamel Husain | 8 | Pilot war story has before/after numbers (23% → 6% drop-off, 85% support-ticket reduction); per-stage instrumentation is advocated in reviewer lens. |
| Simon Willison | 7 | Not his beat; security implications of voice (voice cloning, identity fraud, audio-channel prompt injection) entirely absent. Defensible scope but worth a sentence. |
| Cohort peer | 9 | "Drawing the napkin" frame and the healthcare pilot war story land hard; vendor recommendations are actionable. |

**Weighted average: 8.1**

### Top 3 polish targets
1. **Layer 2, 800ms budget (~line 90):** author's own reviewer lens admits the 300ms threshold is blog-on-blog. Either cite Stivers et al. directly with N and effect size, or soften the prose in Layer 2 to match the reviewer lens's honesty (≤2-sentence fix).
2. **Layer 4 vendor numbers (~line 165-173):** Deepgram "6.84% vs 14.92% median WER" is a Deepgram-self-reported benchmark. Add *"per Deepgram's own eval"* inline, not just in the citation.
3. **Missing: voice-specific security/injection.** One paragraph in Layer 5 or Common Mistakes: "audio prompt injection through tool-returned speech" is now an active attack class — worth one sentence and a pointer to Willison.

### Citations to verify (Phase 4)
- [^1] OpenAI gpt-realtime GA date "August 28, 2025" and pricing ($32/$64 per 1M tokens) — verify.
- [^7] LiveKit turn detector stats "85% TP, 97% TN" — verify these are still the current published numbers.
- [^2] Sesame CSM-1B release date "March 13, 2025" + "~1M hours English audio" training claim — verify.

---

## 05-fri — n8n for agent workflows

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 7 | Less mechanism-heavy by topic, but the workflow-vs-agent collapse-to-two-architectures insight is genuinely useful framing. |
| Chip Huyen | 8 | Head-to-head n8n vs LangGraph table is the kind of production-decision artifact ops leads actually need; regulatory war story with 7-year retention is real. |
| Jerry Liu | 9 | "Most teams have an integration-and-governance problem, not a LangGraph problem" is exactly the right-sized claim; framework-bias check works both ways. |
| Hamel Husain | 7 | Experiment's success criteria (structured-output validity, confidence calibration) are named but not quantified — no pass/fail threshold. |
| Simon Willison | 8 | Not his beat; the security implications of MCP Server Trigger exposing workflows to Claude Desktop get one sentence; could stand more. |
| Cohort peer | 9 | Shelf A/B/C/D taxonomy is the kind of thing a senior catalyst actually needs; "you do not wear Temporal to brunch" is the voice working. |

**Weighted average: 7.9**

### Top 3 polish targets
1. **Layer 3, "v1.113.3 release shipped more than seventy AI-related nodes" (~line 84):** verify this version number and count; single citation [^8] to Skywork AI is thin for a specific release-count claim.
2. **KYC war story (~line 267-280):** the regulator-audit scenario is vivid but attribution is "a mid-stage fintech I advised" — either sharpen to industry-and-region (e.g., "EU-regulated fintech Series B, names withheld") or mark explicitly as composite. Currently floats uncomfortably.
3. **Runnable experiment Path A (~line 232-246):** the workflow spec is clear but should specify *which* n8n release it's tested against — n8n versions drift fast and the spec naming (`AI Agent node`, `MCP Client Tool`) changed between 1.x releases.

### Citations to verify (Phase 4)
- [^8] Skywork AI "v1.113.3 release 70+ AI nodes" — verify the version and the count.
- [^6] LangGraph 1.0 release "October 2025" — verify.
- [^12] Delivery Hero "200+ engineer-hours saved per month" — verify attribution on n8n case-studies page.

---

## 06-sat — Agent fundamentals deeper

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 9 | ReAct-revisited-with-hindsight is exactly the mechanism-clarity teaching move; Lanham/Turpin tie-back to faithfulness is right; "observation formatter is the biggest quality lever" is a genuine insight. |
| Chip Huyen | 8 | Planning-vs-execution war story has concrete numbers (23 → 11 tool calls, 8% → <1% abort, 2.4× cost, 40% longer wall-clock, $34/day). That's the shape. |
| Jerry Liu | 9 | "Five patterns collapse to two" is the correct refactoring; memory-taxonomy complexity-test with cross-domain examples is on-brand. |
| Hamel Husain | 9 | "Benchmarks for triage, 50-example domain eval with LLM-as-judge validated by critique shadowing" is literally the Hamel protocol, credited correctly. Pass^k discussion is the sharpest take on eval reliability in the week. |
| Simon Willison | 8 | Not a security lesson but the "don't log Thought: as audit trail" point is a security insight in disguise and correct. |
| Cohort peer | 8 | Experiment is real (run both modes, save patches, grade). Domain examples (medical/sales/dev/support) cross fields cleanly. |

**Weighted average: 8.5**

### Top 3 polish targets
1. **Layer 3, plan-first vs interleaved war story (~line 158):** "Q1 2026 client engagement" with $34/day specificity is great; add the task domain (data-reconciliation is named; add industry or data-volume for grounding) in ≤1 line.
2. **Layer 6 benchmark numbers (~line 143-145):** Opus 4.5 "80.9% on Verified," Opus 4.6 "99.3% telecom / 91.9% retail," GPT-5 "96.7% telecom with 45% fewer tool calls" — all need spot-checks against the cited sources; numbers are specific and load-bearing.
3. **Memory section, "LangChain, OpenAI, and Oracle all reference roughly the same four" (~line 162):** add the citation inline or drop "Oracle" if it's not in the footnotes. Currently a three-vendor claim backed by one link.

### Citations to verify (Phase 4)
- [^8] Vellum AI "Claude Opus 4.6 benchmarks" page with 99.3%/91.9% numbers — verify these specific figures.
- [^9] GPT-5 "96.7% telecom with 45% fewer tool calls" — verify against OpenAI's actual release-post numbers.
- [^6]/[^7] Opus 4.5 "80.9% SWE-bench Verified" — verify the exact percentage.

---

## Overall Week 2

**Overall weighted score: 8.3 / 10** (average of six lesson weighted averages: 8.4, 8.4, 8.5, 8.1, 7.9, 8.5).

**Weakest lesson: 05-fri n8n for agent workflows (7.9).** Not because it's bad — it's the most usable decision-framework artifact in the week. The weakness is specificity: version numbers, the KYC war story's attribution, and the experiment's success criteria are softer than the rest of the week. Tightenable in Phase 3 without rewriting.

**Strongest lessons:** 03-wed security (8.5), 06-sat agent fundamentals (8.5). Both engage live controversies with named positions and operator numbers.

---

## Phase 3 polish list (12 items, bounded)

1. **Mon Layer 2:** 1-line annotation on `protocolVersion` downgrade behavior in the handshake JSON block.
2. **Mon Step 5 (experiment):** specify N=10/10 injection test + ≥95% refusal threshold.
3. **Mon Layer 4:** 1 sentence naming the MCP Registry proposal so discovery section isn't stale.
4. **Tue Layer 1 [^3]:** add methodology snippet for Reinhard 28% claim (N/benchmark/domain in ≤1 line).
5. **Tue war story "67k tokens":** add date and link for the Aakash Gupta thread, or mark as composite.
6. **Tue P4:** specify success metric (retry count bounds over N=10 trials).
7. **Wed Layer 4.3:** inline link to `@anthropic-ai/sandbox-runtime` npm in prose, not just citation.
8. **Wed experiment Step 1:** make "isolate from production MCPs / sensitive files" a first-class safety note.
9. **Thu Layer 2 (800ms):** reconcile Layer-2 prose with reviewer-lens honesty on the 300ms-blog-loop issue.
10. **Thu Layer 4:** inline "per Deepgram's own eval" caveat on the 6.84%/14.92% WER numbers.
11. **Thu: add one paragraph/sentence on audio prompt injection as an active 2026 attack class.**
12. **Fri KYC war story:** sharpen attribution ("EU-regulated fintech Series B, composite") or add industry/scale detail.

---

## Phase 4 citation-verify list (10 items)

1. **Mon [^13]:** InfoQ MCP Developer Mode tier rollout — URL + tier list.
2. **Mon [^8]:** GitHub blog changelog URLs 2025-12-10 and 2026-01-28 — both.
3. **Tue [^3]:** Jannik Reinhard 2026-02-22 "CLI vs MCP" — URL and the 28%/13.7k/18.0k numbers.
4. **Tue [^14]:** Linear MCP changelog 2025-05-01 — ~21-tool count.
5. **Wed [^4]:** Check Point Research CVE-2025-59536 + CVE-2026-21852 disclosure URL and IDs.
6. **Wed [^14]:** AgentSeal "1,808 MCP servers, 66% findings" — both numbers.
7. **Thu [^1]:** OpenAI gpt-realtime GA date 2025-08-28 and $32/$64 pricing.
8. **Thu [^7]:** LiveKit turn detector 85% TP / 97% TN — still current.
9. **Fri [^8]:** Skywork AI n8n v1.113.3 "70+ AI nodes" claim.
10. **Sat [^8]:** Vellum AI Claude Opus 4.6 τ²-bench 99.3% telecom / 91.9% retail.

---

_Review produced 2026-04-15. No lesson files were edited. No git commits made._
