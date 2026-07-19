---
type: lesson
block: block-6-launch-monetization
week: week-17
session_slug: feedback-metrics-setup-retargeting-or-re-engagement
day_of_cycle: 1
day_name: mon
date_due: 2026-09-07
tags:
  - product-feedback
  - product-market-fit
  - sean-ellis-test
  - nps
  - review-mining
  - roadmap-prioritization
  - closing-the-loop
sources:
  - firstround-superhuman-pmf-engine
  - stackmatix-sean-ellis-pmf
  - formbricks-pmf-survey-questions
  - measuringu-nps-discredited
  - itamargilad-nps-part1
  - reforge-superhuman-reverse-engineered-pmf
  - fitsignal-sean-ellis-40-test
  - emerald-nps-statistical-validation
  - mollick-one-useful-thing-2026
last_verified: 2026-07-17
word_count_target: 3800
---

# The feedback engine: from signal to roadmap

## Why this matters

After a launch you get buried in feedback. Support tickets, tweets, a survey
nobody designed on purpose, three loud users in your Discord who want opposite
things, and a churn number that tells you people are leaving but not why. Most
founders respond by building whatever the loudest person asked for last, then
wonder why the retention curve does not move. This lesson gives you an engine
instead: a small set of instrumented channels that convert noisy signal into a
ranked, defensible roadmap. You will run a PMF survey that means something,
mine your support queue and reviews for the pattern under the noise, and learn
the one segmentation trick that turned Superhuman from a struggling product into
a growing one. Get this right and every later lesson this week has a target. Get
it wrong and you will optimize growth loops that pour users into a product they
do not actually want.

## Prerequisites

- [[block-4-test-validate-package/week-11-define-your-product-idea-validate-idea-using-ai--market-user-validation-interview-or-poll-potential-users/03-wed-interviews-that-dont-lie-to-you|Interviews that don't lie to you]]
  (Block 4). That is the canonical home for the discipline of hearing what
  people mean rather than what flatters you. This lesson assumes you already
  know why "would you use this?" is a worthless question and builds the
  post-launch feedback machine on top.
- [[block-5-product-building-principles/week-14-analytics-iteration-what-to-measure--scale-infra-auth-db-ui-polish/01-mon-product-analytics-for-ai-products|Product analytics for AI products]]
  (Block 5). Quantitative signal (retention, the six AI metrics) lives there.
  Today is the qualitative half: the "why" behind the charts.

## First principles: feedback is not the roadmap

The naive model is a straight pipe. Feedback goes in, features come out. That
model builds the wrong product faster. Feedback is raw ore. It contains signal,
but also recency bias (the last angry email feels urgent), volume bias (loud
users are not representative), and the deepest trap, the fact that users describe
solutions when what you need is their problem. A user who says "add a CSV export"
has quietly done your product design for you, badly. The job of a feedback engine
is to smelt the ore: separate the recurring underlying problem from the surface
request, weight it by who is saying it and how much it matters, and only then let
it touch the roadmap.

So a feedback engine has four stages, and skipping any one produces a
recognizable failure:

1. **Collect** across channels, deliberately, not just whatever arrives.
2. **Structure** the raw signal into problems, not feature requests.
3. **Prioritize** by evidence weight, not by volume or recency.
4. **Close the loop** so users see their input mattered, which produces more and
   better signal next time.

## Stage 1: the feedback channels, and what each is good for

No single channel tells the truth. Each has a bias, and the art is triangulating.

**In-product surveys (micro-surveys).** A one-question prompt fired at a
behavioral trigger. The trigger is the whole game. A survey fired after a user
completes the core action ("Did this summary save you time?") gets contextual,
honest answers. The same survey fired on a timer, or worse on page load, gets
noise and annoyance. Keep it to one question, make it dismissible, and cap
frequency so you do not train users to ignore you.

**The PMF survey (the Sean Ellis test).** The single most useful survey a
post-launch product can run, and the one most often run wrong. We give it its own
section below.

**Support-as-signal.** Your support queue is the richest, most underused
feedback source you own, because the person is describing a real problem they hit
in real usage, with no survey framing to distort it. The discipline is to tag
every ticket with a problem category so that "3 tickets about export this week"
becomes a countable signal instead of a vague feeling. Hamel Husain's refrain for
AI products applies double here: the highest-leverage feedback work is a human
reading actual transcripts and tickets with a spreadsheet open, because the tags
tell you *where* to look and the raw text tells you *what is wrong*.

**Review mining.** If you are on an app store, a marketplace, Product Hunt, G2,
or Reddit, your reviews are a public feedback corpus your competitors can read
too. Mine them for the recurring nouns and verbs, not the star ratings. This is
a genuinely good use of an LLM: paste a few hundred reviews and ask it to cluster
the complaints and praises into themes with representative quotes and rough
counts. You are not asking the model to decide; you are asking it to do the
tedious clustering so you can decide. Treat its output as a first pass to verify
against the raw text, never as ground truth.

**Churn and cancellation surveys.** The one moment a user will tell you the
unvarnished truth is when they are leaving and have nothing to lose. A single
open question on the cancel flow ("What made you cancel?") returns more usable
signal per response than any other survey you run. We use this again on Tuesday
when we design win-back.

## Stage 2: the Sean Ellis test, done the way Superhuman did it

Sean Ellis, who ran early growth at Dropbox, LogMeIn, and Eventbrite, introduced
a benchmark in 2009 after noticing a pattern across dozens of startups: the ones
that grew sustainably almost always had at least **40% of users say they would be
"very disappointed" if they could no longer use the product**, and the ones that
stalled almost always scored below it.[^1] The survey question is exactly:

> How would you feel if you could no longer use [product]?
> (a) Very disappointed (b) Somewhat disappointed (c) Not disappointed

The 40% line is an empirical rule of thumb, not a law of physics, but it is the
most widely used single proxy for product/market fit.[^1][^2] Two disciplines
separate a useful run from a vanity run:

**Ask the right people.** Survey only users who have recently experienced the
core value, typically active in the last two weeks and past onboarding, not
everyone who ever signed up.[^2] Surveying dead signups drags your score toward
zero and teaches you nothing. This is the single most common way the test is run
wrong.

**Segment, do not average.** This is the insight that made the test famous a
second time. Rahul Vohra, founder of Superhuman, documented in First Round Review
how his product's initial PMF score was a mediocre 22%. Instead of treating that
as a verdict, he segmented the "very disappointed" respondents to find who they
were, and built a "high-expectation customer" profile. Filtering to that segment
raised the score to 32% without changing the product at all. Then he split the
roadmap in half: one half doubling down on what the fans already loved, one half
addressing the specific blockers keeping the "somewhat disappointed" users on the
fence. Within a year the score climbed to 58%.[^3][^4] The key move is where he
pointed attention: **not at the "not disappointed" users** (they were never going
to love it, and would "request distracting features, present ill-fitting use
cases, and be very vocal, all before they churn"), and **not only at the fans**,
but at the on-the-fence "somewhat disappointed" segment where "the seed of
attraction is there."[^3]

That reframes feedback prioritization entirely. You are not counting requests.
You are asking two targeted questions of two segments: *what does the fan love
that I must protect and amplify*, and *what is the one blocker keeping the
fence-sitter from becoming a fan*. Superhuman's actual survey added exactly those
follow-ups: what type of person would most benefit, what is the main benefit you
receive, and how can we improve it for you.[^3]

## A word on NPS: know it, distrust it

Net Promoter Score ("how likely are you to recommend, 0 to 10") is the metric
your investors will ask for and the one you should trust least as a roadmap
input. The academic record is unkind. Independent peer-reviewed research has
repeatedly failed to validate NPS as a reliable predictor of future growth; in
Reichheld's own data and later replications it correlates with *historical*
growth, making it at best a trailing indicator, and in a head-to-head study the
11-point recommend scale had the *lowest* predictive validity of the scales
tested.[^5][^6] The mechanical problem is that it crushes an 11-point scale into
three buckets, so a 6 and a 0 both become "detractors" despite wildly different
experiences, and people are poor predictors of their own future behavior anyway,
so a 9 today is often a 6 in three months.[^5][^7] "Satisfaction" and "liking"
turn out to be better predictors of actual recommendation than "likelihood to
recommend."[^5]

> My take: use NPS as a coarse trend line and a conversation starter if a board
> insists on it, never as a prioritization input. The verbatim comment attached
> to the score is worth ten times the number itself. If you have to run one
> survey, run the Sean Ellis test, not NPS. It is more honest and more
> actionable, because "very disappointed" is a behavior proxy and "would
> recommend" is a hypothetical.

## Stage 3: prioritize by evidence weight, not volume

Now you have structured signal: problems, tagged and counted, from multiple
channels, segmented by user type. Prioritization is where founders regress to
building-for-the-loudest. Resist it with a simple weighting. For each candidate
problem, score:

- **Frequency**: how many distinct users hit it (distinct, not tickets, so one
  furious user filing ten tickets counts once).
- **Segment**: is it hurting your high-expectation customers or your
  fence-sitters, or only the "not disappointed" users you are choosing not to
  serve?
- **Severity**: does it block the core value, or is it a papercut?
- **Strategic fit**: does solving it strengthen the thing your fans love, or
  scatter your focus?

Anything a "not disappointed" user requested, loudly, that does not also serve
your core segment, goes to the bottom. This is the discipline that stops the
roadmap from being captured. Ethan Mollick's adoption research reinforces why the
segment lens matters for AI products specifically: trust is contextual, so users
extend and withdraw it feature by feature, and a complaint about one feature can
mask satisfaction with the rest.[^8] Weight the complaint by whether it comes
from someone whose overall relationship with the product is thriving or dying.

## Stage 4: close the loop

The stage everyone skips. When you ship something a user asked for, tell them.
When you decide not to, tell them why. A public changelog, a "you asked, we
shipped" email to the specific requesters, a reply on the original ticket. This
is not politeness. It is a compounding investment: users who see their feedback
change the product give you more and better feedback next time, and a few become
advocates, which feeds directly into Thursday's referral mechanics. A feedback
engine with no closing stage decays, because users learn their input vanishes
into a void and stop bothering.

## Worked example: a review-mining pass that produces a ranked problem list

Say you launched an AI meeting-notes product and have 180 reviews and 60
cancel-survey responses. The goal is not a word cloud. It is a ranked list of
problems, each tied to a segment and a count, that you could defend in a roadmap
meeting.

```python
# feedback_triage.py — cluster raw feedback into ranked problems. stdlib only.
# Run: python feedback_triage.py
# This is a DETERMINISTIC keyword-tagging pass you run BEFORE any LLM clustering,
# so you have a ground-truth count to check the LLM's themes against.
from collections import Counter, defaultdict
from dataclasses import dataclass

@dataclass(frozen=True)
class Feedback:
    user_id: str
    text: str
    segment: str          # 'fan' | 'fence' | 'churned' | 'unknown'

# problem taxonomy: theme -> trigger keywords (you own this list; grow it as you read)
TAXONOMY = {
    "accuracy":     ["wrong", "hallucin", "inaccurate", "missed", "made up"],
    "speed":        ["slow", "lag", "took forever", "waiting"],
    "export":       ["export", "csv", "download", "copy out"],
    "integrations": ["integrat", "zapier", "slack", "calendar", "connect"],
    "price":        ["expensive", "too much", "pricing", "cost", "worth it"],
}

def tag(text: str) -> set[str]:
    t = text.lower()
    return {theme for theme, kws in TAXONOMY.items() if any(k in t for k in kws)}

def rank_problems(items: list[Feedback]):
    # distinct users per theme, weighted by segment (fans/fence count double)
    users_by_theme: dict[str, set[str]] = defaultdict(set)
    weight_by_theme: Counter = Counter()
    for f in items:
        for theme in tag(f.text):
            if f.user_id not in users_by_theme[theme]:
                users_by_theme[theme].add(f.user_id)
                weight_by_theme[theme] += 2 if f.segment in ("fan", "fence") else 1
    rows = [(theme, len(users_by_theme[theme]), weight_by_theme[theme])
            for theme in users_by_theme]
    return sorted(rows, key=lambda r: r[2], reverse=True)

if __name__ == "__main__":
    data = [
        Feedback("u1", "The summaries are often wrong, it missed key decisions", "fan"),
        Feedback("u2", "Love it but I can't export to CSV for my report", "fence"),
        Feedback("u3", "hallucinated an action item that was never said", "fan"),
        Feedback("u4", "too expensive for what it does", "churned"),
        Feedback("u5", "wish it connected to my calendar", "fence"),
        Feedback("u1", "also it was slow this morning", "fan"),
    ]
    print(f"{'problem':14} {'users':>6} {'weight':>7}")
    for theme, n_users, weight in rank_problems(data):
        print(f"{theme:14} {n_users:>6} {weight:>7}")
```

**Pass bar:** running this ranks `accuracy` at the top (two distinct fans hit it,
weight 4), above `export` and `integrations` (one fence-sitter each, weight 2),
with `price` at the bottom (one churned user, weight 1). More important than the
output: you can defend every ranking decision. Accuracy outranks price not
because more people mentioned it, but because the people who mentioned it are the
fans whose love is your whole business. Now feed the same corpus to an LLM for
theme clustering and compare: if its themes match your deterministic counts, you
have a fast trustworthy pipeline; where they diverge, read the raw text and find
out which one is wrong.

## Common mistakes experts see

1. **Averaging the PMF score instead of segmenting it.** A 22% aggregate can hide
   a 58% core. Superhuman's entire turnaround was in the segmentation, not the
   number.[^3]
2. **Running the Sean Ellis test on everyone who ever signed up.** Dead accounts
   drag the score down and teach you nothing. Survey recently-active users
   only.[^2]
3. **Treating NPS as a roadmap input.** It is a weak trailing indicator that
   crushes signal into three buckets; the verbatim comment is worth more than the
   score.[^5][^6]
4. **Building for the loudest user.** Volume is not evidence weight. One furious
   "not disappointed" user is not a mandate; three quiet fans hitting the same
   wall is.
5. **Collecting solutions instead of problems.** "Add a CSV export" is a user
   doing your design badly. Ask what they were trying to accomplish, then design
   the fix yourself.
6. **Never closing the loop.** Feedback channels that visibly change nothing dry
   up. Tell users what you shipped and what you chose not to, and why.

## Reflection questions

1. Run the Sean Ellis test in your head: which users would you survey, and how
   would you define "recently experienced the core value" for your product
   specifically?
2. Who is your high-expectation customer, in one sentence? If you cannot name
   them, what would you have to measure to find them, the way Superhuman did?
3. Pick your last five feature requests. For each, what was the underlying
   *problem* the user was actually describing, and would you have designed the
   same solution they asked for?
4. What is the single most honest feedback channel you currently own, and are you
   tagging it so it produces counts instead of feelings?
5. If your PMF score is below 40%, is the problem the product, the segment you
   are surveying, or the segment you are serving? How would you tell the three
   apart?

## My take (reviewer lens)

**Michael Seibel** would push back on the whole apparatus for a very early
product: if you have 40 users, you do not need a survey pipeline, you need to
call ten of them this week and shut up while they talk. He is right that at the
smallest scale the survey is procrastination and the phone is the tool. The
engine in this lesson is for the moment right after launch when volume outstrips
your ability to talk to everyone, roughly a few hundred users and up. Below that,
skip to the interviews you learned in
[[block-4-test-validate-package/week-11-define-your-product-idea-validate-idea-using-ai--market-user-validation-interview-or-poll-potential-users/03-wed-interviews-that-dont-lie-to-you|Week 11]].

**Ethan Mollick** would note that the PMF survey's "very disappointed" signal can
be unstable for AI products in a way it is not for stable SaaS, because the
product's quality itself drifts as the model changes under you, so a 45% this
month can be a 35% next month for reasons that have nothing to do with your
roadmap.[^8] Fair. Pair the survey with the quality-drift metric from Week 14 so
you can tell a fit problem from a model-regression problem.

**Hamel Husain** would be blunt: most of the value here is in one human reading
50 raw tickets and transcripts, and everything else is a way to feel productive
without doing that. Agreed. The taxonomy and the counts tell you where to look;
they never substitute for looking. The code in this lesson is deliberately a
*pre*-pass to reading, not a replacement for it.

## Further reading

**Must-read**

- Rahul Vohra, "How Superhuman Built an Engine to Find Product/Market Fit,"
  First Round Review. The canonical treatment of segmenting the Sean Ellis
  test.[^3]

**Recommended**

- Formbricks, "Product Market Fit Survey Questions (The Sean Ellis Test + More)"
  for the exact question wording and follow-ups.[^2]
- MeasuringU, "Has the Net Promoter Score Been Discredited in the Academic
  Literature?" for the evidence against leaning on NPS.[^5]

**Optional**

- Itamar Gilad, "Net Promoter Score: Helpful or Harmful?" for a practitioner's
  case against NPS as a hero metric.[^7]

## Citations

[^1]: Stackmatix, "Sean Ellis Test: The 40% Product-Market Fit Survey Guide."
https://www.stackmatix.com/blog/sean-ellis-pmf-survey — origin (2009, Dropbox/
LogMeIn/Eventbrite), the 40% "very disappointed" benchmark as empirical rule of
thumb. (search-verified 2026-07-17; fetch egress-blocked — liveness pass
pending; corroborated by fitsignal below.)
[^2]: Formbricks, "20+ Product Market Fit Survey Questions (The Sean Ellis Test +
More)." https://formbricks.com/blog/product-market-fit-survey-questions — survey
only recently-active users past onboarding; the test measures whether not why.
(search-verified 2026-07-17; corroborated by Stackmatix and Zonka.)
[^3]: Rahul Vohra, "How Superhuman Built an Engine to Find Product/Market Fit,"
First Round Review. https://review.firstround.com/how-superhuman-built-an-engine-to-find-product-market-fit/
— 22%→32% via segmentation, 22%→58% within a year; focus on "somewhat
disappointed" fence-sitters and high-expectation customers. (search-verified
2026-07-17; corroborated by Reforge brief below.)
[^4]: Reforge, "How Superhuman's CEO Reverse-Engineered Product/Market Fit."
https://www.reforge.com/blog/brief-how-superhuman-s-ceo-reverse-engineered-product-market-fit
— independent summary of the same 22%→58% arc and methodology. (search-verified
2026-07-17.)
[^5]: MeasuringU (Jeff Sauro), "Has the Net Promoter Score Been Discredited in the
Academic Literature?" https://measuringu.com/nps-discredited/ — NPS correlates
with historical not future growth; 11-point recommend scale had lowest predictive
validity of scales tested; satisfaction/liking predict recommendation better.
(search-verified 2026-07-17; corroborated by Emerald TQM Journal below.)
[^6]: "Statistical validation of critical aspects of the Net Promoter Score," The
TQM Journal (Emerald, 2023). https://www.emerald.com/tqm/article/35/9/191/378999/
— peer-reviewed validation critique of NPS categorization and predictive claims.
(search-verified 2026-07-17.)
[^7]: Itamar Gilad, "Net Promoter Score — Helpful or Harmful? (part 1)."
https://itamargilad.com/net-promoter-score-part1/ — practitioner critique;
three-bucket compression loses signal; behavior beats stated intent.
(search-verified 2026-07-17; consistent with MeasuringU.)
[^8]: Ethan Mollick, *One Useful Thing* — contextual, fragile trust in AI tools;
users extend and withdraw trust feature by feature.
https://www.oneusefulthing.org/ (search-verified 2026-07-17; consistent with his
book *Co-Intelligence*.)

_last_verified: 2026-07-17_
