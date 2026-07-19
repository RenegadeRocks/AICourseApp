---
type: lesson
block: block-6-launch-monetization
week: week-15
day_of_cycle: 6
day_name: sat
session_slug: publish-live-cold-outreach
tags: [launch-plan, build-day, launch-checklist, outreach-personalizer, go-live, first-hour-velocity, code-lab, compliant-drafting]
sources:
  - launchpact-ph-algorithm-2026
  - instantly-cold-email-benchmark-2026
  - litemail-gdpr-legitimate-interest-2026
  - producthunt-community-guidelines
last_verified: 2026-07-17
word_count_target: 4800
---

# BUILD: the dated launch plan, and go live

## Why this matters

This is the day the week becomes a thing that exists in the world. Everything from Monday to Friday was preparation; today you produce a single, dated, executable launch plan for your real product and you build the two tools that make it runnable rather than aspirational, a checklist runner that gives you a hard GO/NO-GO, and a compliant outreach personalizer that drafts your sequence for human review and refuses to blast it. The pass bar is deliberately strict and deliberately concrete: **a launch a stranger could execute on a date.** If you handed your plan to someone who had never met you, they could run your launch on the day you named, because every step is specific, dated, and unambiguous. That is the difference between a launch and a wish.

## Prerequisites

- All five weekday lessons, and the artifacts they produced: your launch-surface portfolio (Mon), your PH asset kit and first comment (Tue), your five-post social sequence and demo plan (Wed), your 20-prospect list and 3-touch sequence and LIA (Thu), your community-seeding and GEO first-pass plan (Fri).
- Your instrumented launch page ([[05-fri-launch-day-instrumentation|Block 4 Week 10 Friday]]) and packaged offer ([[05-fri-pricing-the-package|Block 4 Week 9 Friday]]).
- Python 3.10+ for the `code-lab/06-launch-runner/` tools (no third-party dependencies).

## Layer 1: The launch plan is a dated checklist, not a strategy doc

A strategy doc describes intentions; a launch plan is a list of dated, owned, checkable actions. The discipline that makes it executable is to phase every action against launch day and make each item pass/fail, so there is never ambiguity about whether it is done. The phases:

- **T-7 (a week out):** the assets. Page instrumented, PH kit built, first comment drafted and cut, social sequence written, demo produced, outreach list built and drafts prepared, LIA documented, community standing confirmed.
- **T-2 (two days out):** the warm-up. Notify your warm list (compliant phrasing — "try it and give honest feedback," never "upvote"), confirm every asset is staged, dry-run the instrumentation by firing events yourself.
- **T-0 / launch day:** the sequence. Self-hunt on PH at 12:01am PT and paste the first comment immediately; fire the social sequence across the day; drop the community contributions; send the outreach (or trigger the warm intros); and, the actual job of the day — reply to everything within the hour.
- **T+1:** bank the assets. PH badge and review quotes onto the page; every warm human into the outreach and interview pool.
- **T+14:** the decision memo, against the pre-registered bands from [[05-fri-launch-day-instrumentation|Block 4 Week 10]].

The blocking distinction matters: some items are *blocking* (the launch cannot proceed without them — instrumented page, first comment, warm-list notification) and some are *optional* (nice to have, a GEO first pass, a partnership conversation). The checklist runner enforces this: if any blocking item is incomplete, it returns NO-GO and exits non-zero. You do not launch on a NO-GO.

## Layer 2: The two tools, and why they are shaped this way

The `code-lab/06-launch-runner/` directory contains two tools that encode the week's discipline in code.

**`checklist.py`, the GO/NO-GO gate.** It loads your launch plan (a JSON list of phased, blocking-or-optional, done-or-not items) and prints a readiness report. If every blocking item is done, it prints GO and exits 0; if any blocking item is open, it prints NO-GO, lists exactly what is missing, and exits 1. This turns "am I ready to launch?" from a feeling into a testable gate you can even wire into a script. The value is not the code; it is that writing your plan as checkable items forces the specificity that makes the launch executable. A vague "do social" is not a checklist item; "5-post sequence written, link-in-comment, passes slop test" is.

**`personalizer.py`, the compliant draft generator.** This is the tool that matters most, because its *shape* is the week's thesis made executable. It renders your 3-touch sequence for each prospect, runs every draft through the compliance gates in `compliance.py` (CAN-SPAM footer present, no upvote solicitation, no generic-AI tell, sub-80-word first touch, real signal required, EU prospects require a documented LIA), and writes the passing drafts to `./drafts/`, each marked **FOR HUMAN REVIEW — DO NOT SEND**. It never sends. The `--send` flag exists only to refuse, loudly, and explain that generic AI blast-send is the exact motion that burns domains and gets buyers to delete on sight ([[04-thu-cold-outreach-post-ai-slop|Thursday]]).

The architectural choices are the lesson:

- **It drafts, never sends.** The human reads every line, verifies every signal is true, edits into their own voice, and sends by hand. This is the AI-for-research-and-review line from Thursday drawn in code: the tool does the tedious rendering and the compliance checking; the human does the judgment and the sending. A pipeline that sent automatically would be the slop machine the week warns against.
- **It blocks prospects without a real signal.** A prospect whose `signal` field is empty is refused, not templated — precision over volume, enforced. If you cannot name why you are writing someone, the tool cuts them for you.
- **It blocks vote solicitations and CAN-SPAM violations before drafting.** The rendered-email gate catches an "upvote" ask or a missing opt-out and refuses to write the draft, so a human never has to catch it downstream.

Run the sample and watch it work: Priya (US, strong signal) drafts cleanly; Tom (EU, strong signal) drafts only because the LIA is documented; Dana (empty signal) is blocked; Sam ("please upvote our launch") is blocked at the rendered-email gate. Every gate corresponds to a rule from the week.

## Layer 3: The build, step by step

**Step 1 — write your launch plan.** Copy `launch_plan.sample.json` and replace every item with your real, dated, product-specific actions. Mark each blocking or optional honestly. Set a real launch date. Run `python checklist.py --plan your_plan.json` and read the NO-GO; it is your to-do list for the week before launch. Your goal by the end of the day is a plan where every *asset* item is done (blocking items you control today), even if the *launch-day* items are still open (they happen on the day).

**Step 2 — build your outreach inputs.** Fill `config.json` with your sender identity, real physical address, real opt-out URL, and your LIA flag (true only once you have actually written the LIA). Fill `sequence_template.json` with your 3-touch sequence, keeping touch 1 tight. Build `prospects.json` from Thursday's 20-prospect list, every prospect with a real, specific signal.

**Step 3 — draft and review.** Run `python personalizer.py --prospects prospects.json --template sequence_template.json --config config.json`. Read the output: how many prospects blocked on `NO_SIGNAL`? Those are the prospects you had no real reason to contact — fix the signal or cut them. Then open `./drafts/` and read every draft. For each, do the thing the tool cannot: verify the signal is actually true, and edit the opener into something only a human who researched this person would write. If a draft looks send-ready without edits, your signal was too generic.

**Step 4 — go live (on the day).** On launch day, work the plan: self-hunt PH and paste the first comment; fire the social sequence across the day; drop the community contributions where you have standing; send the human-reviewed outreach and trigger the warm intros; and reply to everything within the hour. Re-run `checklist.py` on the morning of to confirm GO before you pull the trigger.

## Layer 4: What "a stranger could execute this" actually requires

The pass bar is a stranger-executability test, and it is harder than it sounds. Hand your plan to a peer and ask them to point at any item they could *not* execute without asking you a question. Every such item is underspecified. Common failures the test catches:

- **"Post on LinkedIn"**: a stranger cannot execute this. "Post 1 (founder story) at 9am, link in first comment, text in `posts/post1.md`", they can.
- **"Email the prospects"**: a stranger cannot execute this. "Run `personalizer.py`, review each draft in `drafts/`, verify the signal, send from the founder's email between 10am and noon", they can.
- **"Launch on Product Hunt"**: a stranger cannot execute this. "Self-hunt at 12:01am PT using the staged listing in `ph-listing.md`, paste the first comment from `ph-comment.md` immediately, then reply to comments every 15 minutes for the first four hours", they can.

The test is not academic. A launch plan you cannot hand off is a launch plan that lives only in your head, which means it degrades under launch-day stress exactly when you need it most. The stranger test forces the plan onto paper at a specificity that survives the day.

## Runnable experiment: produce the plan, pass the gates

**Task.** Produce three things and verify them with the tools.

1. **Your launch plan** (`your_plan.json`): real product, real date, phased blocking/optional items covering assets, warm-up, launch day, and post-launch. Run `checklist.py` and get every *asset* blocking item to done.
2. **Your outreach inputs** (`config.json`, `sequence_template.json`, `prospects.json`) built from your real Thursday artifacts, and a clean run of `personalizer.py` producing reviewed drafts.
3. **The stranger test**: hand the plan (or read it as if a stranger) and list every item that could not be executed without asking you a question. Rewrite each until the list is empty.

**Pass bar.**
1. `checklist.py your_plan.json` returns GO for the asset items you control today (blocking asset items done); launch-day items may remain open until the day.
2. `personalizer.py` on your real 20-prospect list produces drafts with **zero** `NO_SIGNAL` blocks (every prospect has a real signal), and any `AI_TELL` warnings are ones you consciously accepted and fixed.
3. You opened `drafts/` and can name the specific human edit each draft still needs. If any draft was send-ready as-is, your signal was generic; fix the list.
4. The stranger test list is empty: no item requires a question to execute.

Time: 90–120 minutes (this is the build day).

## Common mistakes experts see

1. **A strategy doc instead of a checklist.** Intentions do not survive launch-day stress; dated, checkable, owned items do.
2. **Launching on a NO-GO.** Skipping a blocking item ("I'll fire the first comment later") forfeits the first-hour velocity that decides the day.[^1]
3. **Prospects without signals sneaking through.** A `NO_SIGNAL` block is the tool doing you a favor; overriding it by inventing a generic signal recreates the slop the week warns against.[^2]
4. **Treating the personalizer output as send-ready.** It is a draft; the human edit that verifies the signal and adds voice is the non-negotiable step the tool deliberately cannot do.[^2]
5. **Skipping the LIA and emailing the EU anyway.** The tool blocks EU prospects without a documented LIA for a reason; a 30-minute assessment unlocks the market compliantly.[^3]
6. **A plan that lives in your head.** It fails the stranger test, degrades under stress, and has no handoff path if you get sick on launch day.
7. **No reply plan for the day.** The plan schedules the posts but not the replies; on every surface, responsiveness in the first hours is the ranked signal and the relationship, and it needs to be blocked on your calendar.[^1]

## Reflection questions

1. Hand your plan to a peer. Which item did they have a question about first? What does that reveal about where your plan still lives in your head rather than on paper?
2. How many of your 20 prospects did the personalizer block on `NO_SIGNAL`? Was the block a false alarm, or did the tool correctly catch that you had no real reason to contact them?
3. The personalizer refuses to send. If it *could* send, would you be tempted to skip the human review under launch-day time pressure? What does your honest answer say about why the refusal is built in?
4. Which of your launch-day items are blocking and which are optional? If you had to cut half of them due to time, which would you cut, and does that ranking match where your buyer actually is (Monday's portfolio)?
5. Your checklist returns GO. Name the one thing that could still make launch day fail that no checklist item captures. Can you turn it into an item?
6. If you got sick on launch morning, could someone else run your launch from the plan alone? If not, what is the single most important thing to specify further?

## My take (reviewer lens)

**Boris Cherny** would appreciate the draft-not-send architecture as exactly the right way to bound an AI tool's blast radius, the tool automates the reversible, tedious work (rendering, compliance-checking) and hard-stops before the irreversible action (sending), which is the correct safety boundary for any agentic pipeline. His pushback would be on the checklist runner: a JSON file of `done: true` flags is only as honest as the human editing it, and the failure mode is an operator flipping items to done to make the GO appear, which is checklist theater. The fix he'd want is to make blocking items point at *evidence* (a file that must exist, an event that must have fired) rather than a self-reported boolean, a direction the lab leaves as an extension, and rightly flags. **Michael Seibel** would look at the whole build day and ask the same question he asks every day this week: did building the launch runner steal time from talking to customers? His answer would be nuanced here, the personalizer is *directly* in service of talking to twenty customers, so it passes; the checklist runner is borderline, useful only insofar as it forces specificity and not as an end in itself. His rule: spend 20 minutes making the plan checkable, not two hours making the tool pretty. **Hamel Husain** would push on the pass bar: "zero NO_SIGNAL blocks" is a necessary but not sufficient bar, because a *present* signal can still be weak, and the real quality gate is whether a human reviewer, reading the draft cold, believes a genuine person researched this prospect, which is a judgment the tool's `AI_TELL` heuristic only approximates. The tool gets you to compliant-and-specific-enough-to-review; the human gets you to actually-good, and conflating the two is how you ship polished slop.

## Further reading

**Must-read**
- The code-lab `README.md`, the exact run commands, the gates each sample prospect exercises, and the safe-extension invariants. Run it before you build your own.
- [[05-fri-launch-day-instrumentation|Block 4 Week 10 Friday]], the instrumentation and pre-registered decision bands your T+14 memo runs against.

**Recommended**
- Product Hunt Community Guidelines, the compliant-phrasing rules the checklist and warm-list items must honor.[^4]
- [[04-thu-cold-outreach-post-ai-slop|Thursday]], the compliance and precision logic the personalizer encodes.

**Optional**
- Instantly / Amplemarket 2026 benchmarks — to sanity-check the realistic reply band you should expect from your 20-prospect sequence.[^2]

## Citations

[^1]: LaunchPact, "Product Hunt Algorithm in 2026." https://www.launchpact.io/blog/product-hunt-algorithm — first-hours velocity and maker responsiveness as decisive ranking signals; the reply-cadence discipline the launch-day plan schedules. Corroborated by Poindeo, "How Product Hunt's Ranking Really Works (2026 Edition)." https://poindeo.com/blog/product-hunt-upvote-ranking (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^2]: Instantly, "Cold Email Benchmark Report 2026." https://instantly.ai/cold-email-benchmark-report-2026 — precision-over-volume, sub-80-word first touch, signal-based specificity, and the deliverability cost of generic blasting the personalizer is designed to prevent. Corroborated by Amplemarket, "2026 cold email benchmarks." https://www.amplemarket.com/blog/cold-email-benchmarks (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^3]: Litemail, "GDPR Legitimate Interest for Cold Email in 2026." https://litemail.ai/blog/gdpr-legitimate-interest-cold-email-2026, the documented-LIA requirement the personalizer enforces for EU prospects. Corroborated by ModernInbound, "Cold Email Compliance 2026." https://moderninbound.com/blog/cold-email-compliance-guide (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^4]: Product Hunt Help Center, "Community Guidelines." https://help.producthunt.com/en/articles/3615694-community-guidelines, the "invite to try, never ask for upvotes" rule the checklist warm-list item and the personalizer's UPVOTE_ASK gate both encode (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending; primary source).

_last_verified: 2026-07-17_
