---
type: lesson
block: block-5-product-building-principles
week: week-12
day_of_cycle: 2
day_name: tue
session_slug: frontend-basic-uiux-design-principles
date_due: 2026-08-08
tags: [ai-native-ux, streaming-ui, optimistic-ui, confidence-indicators, citations-ui, graceful-failure, empty-states, generative-ui, transparency-patterns, skeleton-screens]
sources:
  - nngroup-genai-ux-agenda-2025
  - nngroup-ai-chatbot-conversation-types
  - reloadux-ai-uncertainty-framework-2026
  - wavespace-ux-ai-products-2026
  - groovyweb-ai-ux-trends-2026
  - vercel-ai-elements-2026
  - anthropic-building-effective-agents-2024
  - thefrontkit-ai-chat-ui-2026
  - apple-hig-generative-ai-2025
last_verified: 2026-07-17
word_count_target: 5500
---

# UX patterns for AI-native products — designing for a system that is slow, probabilistic, and sometimes wrong

## Why this matters (operator framing)

Yesterday's principles apply to any software. Today is the part that does not transfer from twenty years of SaaS design, because the thing behind your buttons is now slow, non-deterministic, and occasionally confidently wrong. A traditional form submit returns in 200ms and is either right or throws an error. An AI generation takes 3 to 30 seconds, streams its answer token by token, and can return something plausible and false. Every UX convention built for fast-deterministic backends breaks against that reality. This lesson gives you the pattern library for AI-native surfaces so users trust the output enough to act on it, forgive the failures, and come back. The deliverable: you can design the loading, streaming, confidence, citation, failure, and empty states for an AI feature, and defend each against the transparency-versus-confidence tradeoff.

By the end you can (1) design latency UX so waiting feels like progress, not a hang, (2) show uncertainty without destroying trust, (3) surface sources and citations so claims are checkable, (4) handle the regeneration and graceful-failure loop that non-determinism forces, (5) onboard a user to value that is different every time, and (6) take a position on how much of the AI's uncertainty to expose.

## Prerequisites

- [[block-5-product-building-principles/week-12-frontend-basic-uiux-design-principles--build-mvp-backend-connect-with-ai-workflows/01-mon-ui-ux-first-principles|Monday's]] usability floor: hierarchy, contrast, affordances, and empty states. This lesson adds the AI-specific layer on top of that floor.
- [[block-2-ai-employees/week-03-building-elegant-landing-pages--how-to-build-micro-prototypes/02-tue-how-ai-code-gen-tools-work|The AI code-gen tools lesson]] (b2w03) for how the models behind these surfaces actually generate. You are now designing the front-of-house for that machinery.
- A working mental model of streaming from your agent builds in Block 2 and 3. Today is the UI for it.

## The core reframe: you are designing for a probabilistic system, not a deterministic one

Traditional UX assumes the backend is fast and correct. Click, wait briefly, get the right answer or a clear error. AI-native UX has to assume the backend is *slow, streaming, and fallible*. Nielsen Norman Group's research agenda for generative AI in UX names this squarely: the patterns are not settled, the interaction models are still forming, and the honest posture is that we are early.[^1] That is not a reason to wing it. It is a reason to learn the patterns that *have* stabilized, because they are stabilizing precisely as users learn to expect them (Jakob's law from Monday, now applied to a new category of convention).

Three properties drive every pattern below:

1. **Latency is high and variable.** Seconds, not milliseconds, and unpredictable. The UI must make waiting tolerable and legible.
2. **Output is non-deterministic.** The same input yields different output. Users need to understand this and have a cheap way to try again.
3. **Output can be wrong while looking right.** Confident hallucination is the defining failure mode. The UI has to support verification without drowning the user in doubt.

## Pattern 1 — Latency UX: make the wait feel like progress

An AI generation that takes 8 seconds behind a spinner feels broken. The same 8 seconds with streaming text feels alive. This is the single highest-leverage AI-native pattern, and the evidence is direct: users who see streaming output wait more patiently than users who see a static loader, and skeleton screens reduce perceived load time by around 40% compared to a blank panel with a spinner, while near-eliminating the "is this broken?" reload.[^2][^3]

The latency toolkit, in order of preference for AI output:

1. **Stream the answer.** Token-by-token rendering is the default expectation for text generation in 2026.[^3] The user sees words appearing, which reads as "the system is working and here is the answer forming." It also lets them start reading before generation finishes, cutting perceived latency to near zero for long outputs.
2. **Skeleton screens for structured output.** When the output is a card, table, or dashboard rather than free text, show a skeleton of the eventual layout, not a spinner. The skeleton communicates "here is the shape of what is coming," which reduces anxiety and perceived wait.[^2]
3. **Staged progress for multi-step agents.** A long agent run (retrieve, reason, draft, verify) should show its stages, not a single indeterminate bar. "Searching your documents… Found 12 sources… Drafting…" turns an opaque 20-second wait into a legible process. This doubles as transparency (Pattern 4).
4. **Spinners only for sub-2-second, unknowable waits.** A spinner is the weakest option and should be the fallback, not the default.

The anti-pattern is the bare spinner on a multi-second AI call. It maximizes perceived latency and the "did it hang?" reload, which on a metered API is a doubled cost and a doubled chance of failure.

## Pattern 2 — Optimistic UI, and where it is dangerous for AI

Optimistic UI updates the interface as if the action succeeded before the server confirms, then reconciles. For deterministic actions (liking a post, adding a to-do) it is a clean latency win and React 19 gives you `useOptimistic` and `useActionState` as first-class primitives for it, with automatic rollback on failure.[^4] Friday's lesson wires these.

The AI-specific caveat: **be optimistic about the *action*, not about the *content*.** You can optimistically show "Generating…" in the message list the instant the user hits send, because that the request was accepted is deterministic. You cannot optimistically show a *guessed answer*, because the content is non-deterministic and you would be fabricating. The pattern that works: optimistically render the user's own message and a streaming placeholder for the assistant, then stream the real content into the placeholder. The pattern that fails: optimistically rendering a predicted result that the model then contradicts, which is worse than a spinner because it teaches the user your UI lies.

## Pattern 3 — Showing confidence and uncertainty without breaking trust

This is the hardest AI-native pattern and the one with the sharpest tradeoff. The output can be wrong. How much do you tell the user, and how?

The 2026 pattern vocabulary that has stabilized:[^5][^6]

- **Percentage or score badges** ("92% confidence") work for *classification* outputs where a calibrated probability exists (spam/not-spam, category prediction). They are misleading for open-ended generation, where the "confidence" number is not a real calibrated probability and pretending it is erodes trust when it is wrong.
- **Source citation as implicit confidence.** For factual retrieval, the strongest confidence signal is not a number, it is a checkable source. "Here is the answer, and here is where it came from" lets the user calibrate for themselves. This is Pattern 4 and it is often the *right* uncertainty UI.
- **Color-coded borders or subtle indicators** (green high, amber medium) for generated recommendations, used sparingly.
- **Language over numbers for the fuzzy cases.** The reloadux framework's finding is sharp and worth memorizing: "AI is unsure" reads as failure, while "Limited data available for this recommendation" reads as useful context.[^5] Same underlying uncertainty, opposite trust effect. You are not hiding the uncertainty; you are framing it as information rather than apology.

The critical failure mode, named directly in the 2026 literature: **over-indication.** If every output carries an uncertainty signal, users stop reading them and lose trust in *all* outputs equally.[^5] Confidence UI has to be selective. Surface it where it changes what the user should do (verify before acting on a high-stakes claim), suppress it where it is noise.

## Pattern 4 — Citations and sources UI: the trust primitive

For any product that makes factual claims (research assistants, analysts, support bots over your docs), the citation is the load-bearing trust element. A claim with a checkable source is verifiable; a claim without one is a bet on the model. The pattern that works:

- **Inline, clickable citations** attached to the specific claim, not a bibliography dump at the end. The user should be able to check the sentence they doubt, not scroll a source list.
- **Source preview on hover or click** so verification does not require a full context switch. Show the relevant passage, highlighted.
- **Honest "no source found" states.** When the model generates from parametric knowledge rather than retrieved context, say so, or design the system so ungrounded claims are visibly distinct from grounded ones. This connects to the [[block-3-advanced-topics-voice/week-06-beyond-prompt-engineering-context-engineering--advanced-rags/04-thu-agentic-retrieval|agentic retrieval]] work from Block 3: the retrieval architecture and the citation UI are two halves of one trust system.

The commercial point: citations are the feature that lets a professional user *act* on your product's output, well beyond any compliance checkbox. A lawyer, analyst, or doctor will not use an ungrounded answer. A cited one they can verify and then trust. Anthropic's guidance on building effective agents treats verifiable, tool-grounded output as central for exactly this reason.[^7]

## Pattern 5 — Graceful failure and regeneration

Non-determinism guarantees that some fraction of outputs will be bad: wrong, off-tone, incomplete, or refused. Traditional error handling ("something went wrong") is inadequate because the failure is often not an error at all, it is a *low-quality success*. The AI-native failure toolkit:

1. **Cheap regeneration.** A one-click "Regenerate" or "Try again" that re-rolls the non-deterministic output. This is the single most important AI-native affordance, because it turns a bad output from a dead end into a minor annoyance. Make it obvious and instant.
2. **Steerable regeneration.** Better than a blind re-roll: "Make it shorter," "More formal," "Focus on X." This gives the user control over the non-determinism instead of gambling.
3. **Distinguish refusal from error from bad-output.** A safety refusal ("I can't help with that") needs different UI than a timeout ("The model took too long, retry") which needs different UI than a low-quality answer (regenerate/steer). Collapsing all three into "error" confuses users about what to do next.
4. **Preserve the user's input on failure.** Nothing enrages like losing a long prompt to a failed generation. The input must survive every failure mode so retry is free.
5. **Partial-output recovery.** If a stream dies at 80%, keep the 80% and let the user continue or retry the rest, rather than discarding everything.

## Pattern 6 — Onboarding to non-deterministic value, and empty states

Monday established that empty states teach. AI-native empty states have a harder job: they must onboard the user to value that is *different every time and not guaranteed*. A traditional empty state says "add your first item." An AI empty state has to say "here is the kind of thing this can do, here is how to ask, and here is a realistic example of what you'll get," while managing the expectation that output varies.

The patterns that work:

- **Example prompts as the empty state.** Instead of a blank input, show three concrete starter prompts the user can click. This solves the blank-canvas paralysis (Hick's law from Monday: reduce the choice from infinite to three) and demonstrates capability by example.
- **Show a real sample output, labeled as sample.** Let the user see what "good" looks like before they invest a prompt, while making clear their result will differ.
- **Progressive capability reveal.** Do not front-load every feature. Onboard to the one high-value action first, reveal the rest as the user succeeds. This is Hick's law plus the reality that AI products often have a large, intimidating capability surface.
- **Set the variance expectation gently.** "Results vary. Regenerate or refine anytime." One line that pre-frames non-determinism as a feature (you can re-roll) rather than a bug (why is it different).

NN/g's analysis of chatbot interactions found six distinct conversation types, from vague prompts to precise questions, each needing different interface support.[^8] The onboarding implication: your empty state is teaching the user which conversation type your product rewards. A product that wants precise queries should model precise queries in its examples.

## Pattern 7 — Transparency: the "AI did something" patterns

When AI acts on the user's behalf (edits their doc, sends a draft, takes an action), the user needs to know what happened and be able to undo it. The transparency toolkit:

- **Attribution.** Visibly mark AI-generated or AI-modified content so the user knows what the machine touched. This is trust and, increasingly, an EU AI Act transparency expectation for certain systems.
- **Diff and review before commit.** For consequential actions, show what the AI proposes and let the user approve, exactly the human-gate pattern from the [[block-2-ai-employees/week-04-building-a-sales-agent--building-comprehensive-rag-ai-agent/02-tue-agent-architectures|agent architectures]] work. The diff is the transparency UI for agentic action.
- **Undo everywhere.** Non-deterministic action plus one-click undo equals a user who will experiment. Non-deterministic action without undo equals a user who will not trust the feature with anything that matters.
- **Audit trail for high-stakes surfaces.** The 2026 pattern census lists visible audit trails among the highest-performing trust patterns for AI products.[^6] For a financial or legal product, "what did the AI do and when" is not optional.

## Controversy: how much of the AI's uncertainty do you show the user?

The sharpest live debate in AI-native design, with two coherent camps.

**The transparency camp.** Show the uncertainty. Surface confidence, mark AI-generated content, expose sources, admit when the model is guessing. The argument: users deserve to calibrate, hidden uncertainty is a dark pattern, and trust built on concealed fallibility collapses catastrophically the first time the user catches a confident lie. NN/g's finding that 36% of designers fear AI will normalize dark patterns sits behind this camp.[^1] Regulation is trending this way too.

**The confidence camp.** Over-showing uncertainty destroys the product. A user bombarded with confidence scores and hedges stops trusting anything and does the work themselves, at which point why did they buy your product. The argument: the product's job is to be *useful*, and a useful tool projects appropriate confidence, surfacing uncertainty only where it is decision-relevant. Over-indication is itself a documented failure mode.[^5]

**The synthesis this lesson commits to:** the tradeoff resolves on *stakes and verifiability*, not on a global transparency dial. Show uncertainty where (a) the stakes of acting on a wrong answer are high, and (b) the user can actually do something with the signal (verify a source, choose to double-check). Suppress it where the output is low-stakes or where the "confidence number" is not a real calibrated probability and would be theater. Prefer *checkable sources* over *abstract confidence scores* whenever the output is factual, because a source is uncertainty the user can resolve, while a score is uncertainty the user can only worry about. And frame residual uncertainty as information ("limited data available"), never as apology ("AI is unsure"). The dark-pattern line is bright: never hide uncertainty to manipulate the user into trusting a claim you know is shaky. That is the one move that ends the relationship.

## Worked example — designing the states for one AI feature

Take the feature you will build Saturday: a user submits a prompt and gets a streamed AI response over your own content. Enumerate every state before writing any UI.

| State | Pattern | Concrete UI |
|---|---|---|
| Idle / empty | Example prompts | Three clickable starters + one labeled sample output |
| Submitted | Optimistic action | User message renders instantly; assistant placeholder appears |
| Generating | Streaming + staged progress | Token stream; if agentic, "Searching… Drafting…" stages |
| Success | Citations | Answer with inline clickable sources, hover preview |
| Low-quality success | Regeneration | Visible "Regenerate" + "Make it shorter/more formal" |
| Refusal | Distinct refusal UI | "I can't help with that" + why + what to try instead |
| Error/timeout | Graceful failure | Preserve input, clear retry, partial-output recovery |
| Uncertain claim | Selective confidence | "Limited data available" framing, only where decision-relevant |

The discipline is that you designed *eight* states, not one. AI-generated UIs ship the "success" state and omit the other seven, which is exactly where new and stressed users live. The state table is the artifact; the UI is downstream of it.

## Runnable experiment — the AI state audit, with a pass bar

**Setup (10 min).** Pick one shipped AI product you use (a chat app, a research tool, an AI writing assistant). You will reverse-engineer its state design, then design yours.

**Phase 1 — reverse-engineer (30 min).** Trigger and screenshot as many of the eight states as you can: empty, submitted, generating, success, bad-output, refusal, error, uncertain. For each, name the pattern it uses and rate it. Which states did the product *not* handle? (Force an error by killing your network mid-generation. Force a refusal. Force a bad output with a vague prompt.)

**Phase 2 — design your eight states (40 min).** For the feature you will build Saturday, fill the state table above with concrete UI for all eight rows. Write the exact microcopy for the empty state, the refusal, and the uncertain-claim framing, applying the "information not apology" rule.

**Phase 3 — the transparency decision (15 min).** Write one paragraph deciding, for your specific product and user, where on the transparency-versus-confidence axis you land and why, referencing stakes and verifiability. This is a real product decision you will defend to a user.

**Pass bar:** All eight states have concrete UI (not "TODO"); the streaming/loading state is streaming or skeleton, never a bare spinner; the failure state preserves the user's input and offers a clear retry; the uncertain-claim copy passes the "information not apology" test; and your transparency decision names stakes and verifiability, not a vibe. If any of the eight states is unhandled, you have not passed.

## Common mistakes experts see

1. **Bare spinner on a multi-second generation.** Maximizes perceived latency and reload-driven double-cost. Stream or skeleton instead.[^2][^3]
2. **Optimistically rendering guessed content.** Being optimistic about the answer, not just the action, so the UI visibly contradicts itself when the real output arrives.
3. **Fake confidence scores on open generation.** Slapping "94%" on text output where no calibrated probability exists, which reads as precise and is theater.
4. **Over-indication.** Uncertainty signals on every output until users tune them all out.[^5]
5. **Collapsing refusal, error, and bad-output into "something went wrong."** Three different user situations needing three different next actions.
6. **Losing the user's input on failure.** The rage-quit generator. Input must survive every failure.
7. **Bibliography-dump citations.** Sources listed at the end instead of attached to the specific claim, so verification is expensive and nobody does it.
8. **AI empty states that say "start typing."** Blank canvas paralysis instead of example prompts and a labeled sample.

## Reflection questions

1. For your product, is the honest confidence signal a number, a source, a color, or a sentence? Justify why the others would mislead.
2. Where would optimistic UI help you, and where would being optimistic about *content* actively harm trust?
3. Force three failures in a competitor's AI product (error, refusal, bad output). Which did they design for and which did they ignore? What did the omission cost you as a user?
4. Your product surfaces an uncertain claim in a high-stakes context. Write the exact microcopy that frames the uncertainty as information, not apology.
5. What is the one action your AI product should require a diff-and-approve gate for, and what is the one it should just do with an undo? What makes them different?
6. NN/g says the patterns are not settled. Which of the eight states in your product are you least sure about, and how would you test the pattern with five real users?

## My take (reviewer lens)

**Nielsen Norman Group's** own posture is the useful corrective to this whole lesson: these patterns are early and under-researched, and anyone claiming a settled playbook is overselling.[^1] The lesson tries to honor that by teaching the patterns that *have* stabilized (streaming, skeleton, cheap regeneration, inline citations) while flagging the genuinely open ones (how much confidence to show, how to onboard to variance). The honest caveat: the 40%-perceived-load and similar figures come from 2026 practitioner writeups, not peer-reviewed studies, so treat them as directional evidence for a real effect, not as precise constants.[^2][^3]

**Simon Willison** would push on the citation pattern from the grounding side: a clickable citation is only a trust primitive if the citation is *real* and *actually supports the claim*, and models are perfectly capable of citing a source that does not say what they claim it says. The UI cannot fix a retrieval or grounding failure; it can only surface it. His pushback is correct and it is why this lesson links the citation UI back to the agentic-retrieval architecture: the front-of-house citation is worthless without back-of-house grounding, and shipping citation UI over ungrounded generation is a dark pattern that manufactures false trust.

**Michael Seibel** would push back on designing eight states for an MVP: "You have zero users. Build the happy path, ship it, and add the refusal state when a user actually hits a refusal." The steelman is real for the *taste* layer of these patterns. The line the lesson holds: the failure state that preserves input and the streaming-not-spinner choice are the difference between a demo and a product a stranger will tolerate, well short of polish. The empty-state example prompts are also load-bearing for a cold-start AI product, because without them the first-run conversion is a blank box nobody knows how to fill. Ship fewer of the eight if you must, but ship streaming, input-preservation, and example prompts on day one.

## Further reading

**Must-read (this week):**
1. **NN/g, "A Research Agenda for Generative AI in UX"** — the honest state of the field and the conversation-type taxonomy.[^1][^8]
2. **reloadux, "AI Uncertainty & Trust: Design Framework"** — the information-not-apology framing and the over-indication failure mode.[^5]
3. **Vercel AI Elements** — the prebuilt AI UI component set that encodes many of these patterns in code you can read.[^9]

**Recommended:**
4. **"UX Design for AI Products (2026)"** (wavespace) and **"12 UI/UX Design Trends for AI Apps in 2026"** (groovyweb) — the practitioner pattern census these numbers come from.[^2][^6]
5. **Anthropic, "Building Effective Agents"** — the back-of-house view; the staged-progress and tool-grounding patterns start here.[^7]

**Optional:**
6. **"AI Chat UI Best Practices for 2026"** (TheFrontKit) — a focused deep-dive on the chat surface specifically.[^3]

## Citations

[^1]: Nielsen Norman Group, "A Research Agenda for Generative AI in UX" (nngroup.com/articles/genai-ux-research-agenda) and 2025 AI-design articles. Source for "patterns not settled," the AI-as-supercharged-intern framing, and the 36%-of-designers-fear-dark-patterns figure. (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending.)

[^2]: "UX Design for AI Products (2026)" (wavespace.agency/blog/ux-design-for-ai-products). Source for skeleton screens reducing perceived load ~40% vs blank spinner panels and the highest-performing 2026 trust patterns. (search-verified 2026-07-17, corroborated by groovyweb[^6]; fetch egress-blocked — liveness pass pending.)

[^3]: "AI Chat UI Best Practices for 2026" (thefrontkit.com/blogs/ai-chat-ui-best-practices). Source for streaming output as standard 2026 expectation and users waiting more patiently for streamed vs static output. (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending.)

[^4]: React, "useOptimistic" and "useActionState" reference (react.dev/reference/react/useOptimistic). Source for React 19's first-class optimistic-update and action-state hooks with automatic rollback tied to the transition system. Detailed further in Friday's lesson. (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending.)

[^5]: reloadux, "AI Uncertainty & Trust: Design Framework" (reloadux.com/blog/ai-uncertainty-trust-design-framework). Source for the confidence-indicator vocabulary (badge/source/color/language), the over-indication failure mode, and the "information not apology" language finding. (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending.)

[^6]: "12 UI/UX Design Trends for AI Apps in 2026 (With Examples)" (groovyweb.co/blog/ui-ux-design-trends-ai-apps-2026). Source for the 2026 pattern census: streaming output, skeleton screens, confidence indicators, override controls, visible audit trails. (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending.)

[^7]: Anthropic, "Building Effective Agents" (anthropic.com/research/building-effective-agents), December 2024. Source for tool-grounded, verifiable output and staged agent workflows as the back-of-house pattern behind these UIs. Also cited in b2w05.

[^8]: Nielsen Norman Group, chatbot-interaction research finding six distinct conversation types across 425 analyzed interactions. Source for the onboarding implication that empty-state examples teach the rewarded conversation type. (search-verified 2026-07-17 via NN/g and parallelhq summaries; fetch egress-blocked — liveness pass pending.)

[^9]: Vercel, AI Elements and the AI SDK UI component set (part of the AI SDK ecosystem, 2026). Source for prebuilt AI UI components (message list, streaming, reasoning display) that encode these patterns. Detailed in Wednesday and Friday. (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending.)

_last_verified: 2026-07-17_
