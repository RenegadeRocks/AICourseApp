"""Re-verification scheduler — "what to re-verify and when".

Implements Thursday's re-verification practice as a runnable scheduler. You
register the decaying facts your business rests on, tag each with a half-life
class, and the tool tells you what is due for re-verification and what is
already overdue (i.e. probably stale).

Pure standard library. Python 3.10+.

Run:  python reverify_scheduler.py
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta


# Half-life classes -> re-verification cadence in days (Thursday's decay map).
CADENCE_DAYS = {
    "price": 30,        # model prices, token costs
    "model": 30,        # model names, defaults, context limits
    "platform": 90,     # platform rules, compliance, policy
    "competitor": 90,   # competitive landscape
    "benchmark": 60,    # "best in class" claims
    "principle": 0,     # durable; never scheduled (0 = never)
}


@dataclass
class Fact:
    name: str
    kind: str
    source: str                 # primary source URL you verify against
    last_verified: date

    def cadence(self) -> int:
        if self.kind not in CADENCE_DAYS:
            raise ValueError(f"unknown kind {self.kind!r}; expected {list(CADENCE_DAYS)}")
        return CADENCE_DAYS[self.kind]

    def next_due(self) -> date | None:
        c = self.cadence()
        if c == 0:
            return None  # durable principle; no re-verification schedule
        return self.last_verified + timedelta(days=c)

    def status(self, today: date) -> str:
        due = self.next_due()
        if due is None:
            return "DURABLE"
        if today > due:
            overdue = (today - due).days
            return f"OVERDUE by {overdue}d (assume stale — verify before acting)"
        remaining = (due - today).days
        return f"ok, due in {remaining}d"


def report(facts: list[Fact], today: date) -> str:
    # Sort: overdue first (most overdue at top), then soonest due, durable last.
    def sort_key(f: Fact):
        due = f.next_due()
        if due is None:
            return (2, date.max)
        return (0 if today > due else 1, due)

    lines = [
        "=" * 66,
        f"RE-VERIFICATION SCHEDULE   (as of {today.isoformat()})",
        "=" * 66,
    ]
    for f in sorted(facts, key=sort_key):
        due = f.next_due()
        due_str = due.isoformat() if due else "n/a"
        lines.append(f"[{f.kind:<10}] {f.name}")
        lines.append(f"             last: {f.last_verified.isoformat()}  next: {due_str}")
        lines.append(f"             {f.status(today)}")
        lines.append(f"             source: {f.source}")
        lines.append("")
    overdue = [f for f in facts if (d := f.next_due()) is not None and today > d]
    lines.append(f"Summary: {len(overdue)} fact(s) overdue and probably stale.")
    return "\n".join(lines)


def _demo() -> None:
    today = date(2026, 10, 20)
    facts = [
        Fact("Opus 4.8 price $5/$25 per Mtok", "price",
             "https://platform.claude.com/docs/en/about-claude/pricing", date(2026, 7, 17)),
        Fact("Sonnet 5 is my default model", "model",
             "https://www.anthropic.com/news/claude-sonnet-5", date(2026, 9, 30)),
        Fact("LinkedIn demotes AI-generated outreach", "platform",
             "linkedin policy page", date(2026, 7, 17)),
        Fact("EU AI Act fully applicable Aug 2 2026", "platform",
             "eur-lex.europa.eu", date(2026, 8, 5)),
        Fact("Retention-first beats growth-first", "principle",
             "Week 22 durable principles", date(2026, 7, 17)),
    ]
    print(report(facts, today))


if __name__ == "__main__":
    _demo()
