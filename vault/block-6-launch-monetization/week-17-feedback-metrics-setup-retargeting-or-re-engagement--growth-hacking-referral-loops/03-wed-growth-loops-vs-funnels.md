---
type: lesson
block: block-6-launch-monetization
week: week-17
session_slug: growth-hacking-referral-loops
day_of_cycle: 3
day_name: wed
date_due: 2026-09-09
tags:
  - growth-loops
  - funnels
  - viral-loops
  - content-loops
  - product-loops
  - loop-efficiency
  - ai-distribution
  - law-of-shitty-clickthroughs
sources:
  - reforge-growth-loops
  - baincapital-elena-verna-plg
  - andrewchen-shitty-clickthroughs
  - andrewchen-viral-loops-braindump
  - productschool-ai-plg
  - venturecurator-ugc-loops
  - canva-made-with-attribution
  - firstround-kfactor-glossary
last_verified: 2026-07-17
word_count_target: 3800
---

# Growth loops vs funnels: why loops compound and funnels leak

## Why this matters

A funnel is a machine for turning money into users. You pour attention in the
top, some fraction converts, and you get users out the bottom. Stop paying and it
stops. A loop is a machine for turning users into more users. The output of one
cycle becomes the input of the next, so it compounds without you refilling the
top every day. The single most important strategic decision in your post-launch
growth is which of these you are building, because a product with a real loop
grows while you sleep and a product with only funnels grows only while you spend.
This lesson teaches you to see your product as a system of loops, identify the one
loop your product can actually run, and instrument its efficiency so you know
whether it is compounding or quietly decaying. Thursday builds the sharpest loop
(referral) in detail; today is the map.

## Prerequisites

- [[block-5-product-building-principles/week-14-analytics-iteration-what-to-measure--scale-infra-auth-db-ui-polish/03-wed-the-iteration-loop|The iteration loop]]
  (Block 5). The product-improvement loop lives there. This lesson is about
  *growth* loops, a different animal: the user helps produce the next user, not
  just a better product.
- [[block-5-product-building-principles/week-13-making-your-product-feel-magic-with-ai--how-to-add-smart-features-that-wow-users/06-sat-build-add-one-magical-feature|The magical feature]]
  (Block 5). The shareable AI artifact you built there is the raw material for
  the output-as-marketing loop we design today.

## First principles: the shape of growth

Brian Balfour, together with Casey Winters, Kevin Kwok, and Andrew Chen,
crystallized the reframe in Reforge's "Growth Loops are the New Funnels": the
fastest-growing products are best represented not as funnels but as loops, closed
systems where inputs run through a process that generates an output which is
*reinvested* back into the input.[^1] The funnel is not wrong, it is too small: it
describes one step inside a loop, but misses the reinvestment that produces
compounding.[^1] Balfour's core distinction is the one to memorize: funnels
operate in one direction and produce linear, diminishing returns, while loops
reinvest their output and produce compounding returns.[^1]

Elena Verna, who has run growth at Amplitude, Miro, SurveyMonkey, and Dropbox and
is now Head of Growth at Lovable, sharpens the practical version: funnels at best
are *fuel* to ignite loops, not the primary engine of growth, and the fastest
companies build loops to make growth predictable and sustainable rather than
rented.[^2] Her "Racecar" framing is a useful mental model: growth loops are the
engine, optimizations are the lubricant, one-off tactics are turbo boosts, and
funnels are the fuel.[^2] Notice what that demotes. Most of what people call
"growth hacking" (the one-off tactics, the clever paid campaign) is a turbo boost
or fuel, not the engine. If you only have turbo boosts, you do not have an engine.

## The four loop families

Loops come in four broad families. Most durable products run one dominant loop
and maybe a supporting one. Trying to run all four at once is how small teams
spread themselves into running none.

**1. Viral / referral loops.** A user brings in another user directly, through an
invitation, a share, or a referral incentive. Output (a new user) feeds directly
back to input. This is the loop everyone dreams of because it can be nearly free,
and the one most often faked, because true virality is rare. Thursday is entirely
about making this one honest.

**2. Content loops.** Usage of the product generates content (or the company
generates content) that attracts new users, who use the product and generate more
content. User-generated content loops are the strongest version: every user who
creates something public creates a new acquisition surface. Programmatic SEO,
where product usage generates indexed pages, is a content loop. The Venture
Curator analysis of YC's AI-heavy 2025 batch flagged user-generated distribution
loops as the pattern that separated the fast movers.[^3]

**3. Paid loops.** Revenue from acquired users funds acquisition of more users.
This *is* a loop, not just a funnel, if the unit economics close: a user pays you
more than they cost to acquire, and you reinvest the margin. The compounding is
real but slower and bounded by your payback period and the law of rising ad
costs. Paid loops are the most reliable and the least defensible, because anyone
with capital can run them.

**4. Product loops.** The product gets more valuable, or more visible, the more
it is used, pulling in new users as a byproduct of normal usage. Collaboration is
the classic engine: you use the product with a colleague, who now has an account.
Network effects are product loops. For AI products there is a specific and
powerful variant below.

## The AI-product loop: output as marketing

AI products have a native loop that most SaaS products envy: the output *is* the
marketing. When your product generates something a user shares, and that artifact
carries your brand or a link back, every use becomes a potential acquisition
event. This is the loop you seeded in
[[block-5-product-building-principles/week-13-making-your-product-feel-magic-with-ai--how-to-add-smart-features-that-wow-users/06-sat-build-add-one-magical-feature|Week 13]]
when you built a shareable artifact.

The canonical execution is Canva's "Made with Canva" attribution: one-click
export to social, a watermark or credit that travels with the design, and the
result is billions of designs created and millions shared, each an organic
exposure surface.[^4] Elena Verna, describing AI-native growth at Lovable, frames
the mechanic directly: the AI can nudge users to share templates, invite
collaborators, or export something that carries your watermark into other
tools.[^5] The AI twist is that the output is often novel and impressive on its
own, so people *want* to share it, which is exactly the condition a content or
viral loop needs.

Designing this loop well means answering three questions:

- **What does the user produce that they would share anyway?** The summary, the
  generated image, the analysis, the deck. If they would not share it without an
  incentive, a watermark will not save it.
- **What travels with it?** A "made with [you]" credit, a link back, a preview
  that renders your brand when pasted. The attribution must survive the share,
  not sit in a footer nobody sees.
- **What does a recipient do when they see it?** The loop only closes if the
  recipient can become a user in one click. A shared artifact that dead-ends is a
  broken loop.

> My take: the output-as-marketing loop is genuinely the best growth asset an AI
> product has, and it is also the most over-promised. It only works if the output
> is good enough that a real person is proud to attach their name to it. If your
> summaries are mediocre, watermarking them just spreads evidence that your
> product is mediocre. Fix the output first (that is Monday's feedback engine),
> then instrument the loop.

## Why loops compound and funnels leak

The mechanical difference is reinvestment. In a funnel, each user is a terminal
output: you spent to acquire them, you got them, and to get the next user you
spend again. In a loop, each user is also an input: they produce something (a
referral, a piece of content, a collaborator, revenue) that helps acquire the
next user at no additional acquisition cost. Over many cycles this is the
difference between addition and multiplication.

But loops are not magic perpetual-motion machines, and this is the part the
growth-hype crowd omits. Every loop decays, because of what Andrew Chen named the
**Law of Shitty Clickthroughs**: over time, every marketing channel degrades.
Banner ads once had click-through rates around 70%; today they are a tiny
fraction of that. The mechanism is that users habituate and tune out, and channels
saturate.[^6] Applied to loops, this means two forces erode your loop over time:
**saturation** (a viral loop eventually burns through its addressable market, so
each cycle reaches fewer new people and the effective viral factor falls) and
**habituation** (the share that felt novel becomes noise, so conversion per
exposure drops).[^6][^7] A loop that compounds at 1.3x this quarter will not
compound at 1.3x forever without work. The job is not to build a loop and walk
away; it is to build a loop and keep fighting its decay.

## Instrumenting loop efficiency

You cannot manage a loop you have not instrumented, and a loop is not measured
the way a funnel is. A funnel has a conversion rate. A loop has three numbers:

1. **Loop amplification (the branching factor).** How many new inputs does one
   full cycle produce? For a viral loop this is the k-factor (Thursday's math).
   For a content loop it is roughly new-users-attracted per piece-of-content per
   cycle. Above 1 and the loop grows on its own; below 1 and it decays toward a
   steady state that still amplifies your other channels but does not run away.
2. **Cycle time.** How long is one full turn of the loop? A loop with modest
   amplification but a fast cycle can out-grow a loop with high amplification but
   a slow cycle, because compounding frequency matters as much as the rate. This
   is why cycle time is a first-class metric, not an afterthought.[^8]
3. **Loop efficiency / conversion at each handoff.** Where in the loop do you lose
   the most: users who never produce output, output that never gets seen, viewers
   who never convert? The weakest handoff is where a single improvement moves the
   whole loop.

The discipline: pick one loop, name its input and output explicitly, measure the
branching factor and cycle time, and find the weakest handoff. That is the entire
program. We build the simulator that does this math in Saturday's `code-lab`.

## Worked example: mapping your product's dominant loop

Take the AI meeting-notes product again. Walk the candidate loops:

| Loop | Input | Process | Output reinvested? | Verdict |
|---|---|---|---|---|
| Viral/referral | Active user | Invites teammates to shared notes | Yes: teammate becomes user | Strong (collaboration-native) |
| Content | Active user | Public shareable meeting recap w/ credit | Yes: recipients click through | Medium (depends on share rate) |
| Paid | Revenue | Ads to lookalike audiences | Only if payback closes | Weak early (thin margins) |
| Product | Active user | More meetings summarized = more colleagues invited | Yes: overlaps viral | Strong |

The dominant loop is clearly collaboration-driven (viral + product overlap):
every meeting has other attendees, and inviting them to the shared notes both
delivers value and acquires users. That is the loop to instrument and optimize.
The content loop is a promising supporting loop once share quality is high. The
paid loop waits until unit economics close. Naming this explicitly stops you from
scattering effort across four half-built loops.

Now find the weakest handoff. Suppose 60% of users produce shareable notes, 40%
of those actually invite a colleague, and 70% of invited colleagues sign up. The
weakest handoff is the invite step (40%). A change that lifts invites from 40% to
60% moves the whole loop more than any improvement to the already-strong signup
conversion. That is the insight instrumentation buys you: it tells you the one
place to push.

## Common mistakes experts see

1. **Confusing a funnel optimization for a loop.** Improving your signup
   conversion is good, but it does not create compounding. Ask whether the output
   reinvests into the input; if not, it is a funnel step, not a loop.
2. **Trying to run all four loop families at once.** Small teams that spread
   across viral, content, paid, and product loops usually run none of them well.
   Pick the dominant one.
3. **Assuming loops are perpetual.** Every loop decays via saturation and
   habituation.[^6] Budget ongoing work to fight the decay, or watch your viral
   factor bleed out quarter over quarter.
4. **Watermarking mediocre output.** The output-as-marketing loop amplifies
   whatever quality you have. Spread bad output and you spread bad word of mouth.
5. **Measuring loop amplification but ignoring cycle time.** A slow loop with high
   amplification loses to a fast loop with modest amplification. Instrument
   both.[^8]
6. **Calling a paid channel a loop when the economics do not close.** A paid loop
   is only a loop if margin funds the next acquisition. Otherwise it is a funnel
   you are subsidizing.

## Reflection questions

1. Name your product's dominant loop in one sentence: what is the input, the
   process, and the output that reinvests? If you cannot, you may only have
   funnels.
2. For your output-as-marketing loop, what does the user produce that they would
   share *without* any incentive? If the answer is "nothing," what would you have
   to improve?
3. Which handoff in your dominant loop is weakest, and how would you measure it
   this week?
4. How is your loop decaying right now (saturation, habituation, or both), and
   what would you do to counter it?
5. If you had to kill three of your four candidate loops and bet everything on
   one, which survives, and what evidence supports the choice?

## My take (reviewer lens)

**Michael Seibel** would push back that "growth loops" is a framework that can
become an excuse to theorize instead of ship: the fastest way to know if you have
a viral loop is to build the share button and watch, not to draw a four-quadrant
diagram. He is right that the map is not the territory. Use the loop framework to
decide *which* button to build first, then build it and measure, rather than
perfecting the diagram.

**Andrew Chen** would insist you internalize the decay, not just nod at it: most
loops that look like they are compounding are actually riding a one-time
saturation wave that will flatten, and founders consistently over-extrapolate the
early curve.[^6][^7] Fair, and it is why Saturday's simulator explicitly models
saturation rather than assuming a constant k-factor. Do not project a straight
line off three good weeks.

**Chip Huyen** would note that the AI output-as-marketing loop has a cost the SaaS
version does not: every shared artifact was generated with tokens, so a viral
content loop can scale your inference bill faster than your revenue if the loop
brings in free-tier lookers rather than payers. Instrument cost-per-loop-cycle
alongside amplification, or a "successful" loop can bankrupt you. That ties
straight back to the cost-per-active-user discipline from Week 14.

## Further reading

**Must-read**

- Brian Balfour et al., "Growth Loops are the New Funnels," Reforge. The founding
  text of the loop reframe.[^1]

**Recommended**

- Elena Verna, on the growth-model menu and loops-as-engine (Bain Capital
  Ventures interview / her newsletter). The clearest practitioner framing.[^2]
- Andrew Chen, "The Law of Shitty Clickthroughs," for why every loop decays.[^6]

**Optional**

- Venture Curator, "How to build user-generated distribution loops," for the
  AI-batch pattern evidence.[^3]

## Citations

[^1]: Brian Balfour, Casey Winters, Kevin Kwok, Andrew Chen, "Growth Loops are the
New Funnels," Reforge Blog. https://www.reforge.com/blog/growth-loops — loops as
closed reinvesting systems; funnels linear/diminishing, loops compounding.
(search-verified 2026-07-17; fetch egress-blocked — liveness pass pending;
corroborated by Aakash Gupta's growth-loops guide and Balfour's own X thread.)
[^2]: Elena Verna, PLG and growth-loops framing (Bain Capital Ventures, "PLG
Expert Elena Verna Breaks Down the New B2B Growth Standard").
https://baincapitalventures.com/insight/plg-expert-elena-verna-breaks-down-the-new-b2b-growth-standard/
— funnels as fuel not engine; Racecar framework (loops=engine). Verna is Head of
Growth at Lovable, formerly Amplitude/Miro/SurveyMonkey/Dropbox. (search-verified
2026-07-17; corroborated by her newsletter elenaverna.com and Reforge PLG piece.)
[^3]: Venture Curator, "How to build user-generated distribution loops" (YC 2025
AI batch analysis). https://www.venturecurator.com/p/how-to-build-user-generated-distribution
— UGC distribution loops as the differentiating pattern. (search-verified
2026-07-17.)
[^4]: Canva, "Introducing Canva's Creative Operating System" / newsroom on
"Made with Canva" attribution. https://www.canva.com/newsroom/news/creative-operating-system/
— one-click social export, "Made with Canva" attribution, billions of designs,
millions shared as organic exposure. (search-verified 2026-07-17; corroborated by
OpenAI's Canva Magic Studio case note.)
[^5]: Elena Verna via Product School, "How AI Is Transforming Product-Led Growth."
https://productschool.com/blog/artificial-intelligence/how-ai-is-transforming-product-led-growth
— AI nudging users to share templates / export watermarked artifacts as a growth
loop. (search-verified 2026-07-17.)
[^6]: Andrew Chen, "The Law of Shitty Clickthroughs." https://andrewchen.com/the-law-of-shitty-clickthroughs/
— every marketing channel degrades over time via habituation and saturation;
banner CTR ~70% originally to a tiny fraction today. (search-verified 2026-07-17;
corroborated by his Substack "Every marketing channel sucks right now.")
[^7]: Andrew Chen, "Braindump on viral loops," andrewchen.substack.com.
https://andrewchen.substack.com/p/braindump-on-viral-loops — viral loops burn
through the addressable market; saturation lowers effective viral factor.
(search-verified 2026-07-17.)
[^8]: First Round Review, "K-factor: The Metric Behind Virality" (glossary).
https://review.firstround.com/glossary/k-factor-virality/ — viral cycle time as
co-equal with k-factor; faster cycles compound faster. (search-verified
2026-07-17; corroborated by getlaunchlist k-factor guide.)

_last_verified: 2026-07-17_
