"""
compliance.py — shared compliance + quality gates for the Week 15 launch runner.

These checks encode the rules taught in:
  - 02-tue (Product Hunt: never ask for upvotes)
  - 04-thu (cold outreach: CAN-SPAM opt-out + physical address, GDPR legitimate
    interest for EU prospects, precision-over-volume, sub-80-word first touch,
    genuine specificity not generic AI personalization)

Nothing here sends anything. The gates only *refuse to draft* material that would
be non-compliant, so a human never has to catch it downstream.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

# Phrases that indicate a prohibited direct upvote solicitation (Product Hunt /
# Hacker News community guidelines) or the generic-AI-personalization "tell"
# buyers now delete on sight (04-thu, Layer 2).
UPVOTE_SOLICITATION = (
    "upvote",
    "up-vote",
    "vote for us",
    "vote for me",
    "give us a vote",
    "hunt us",
)

GENERIC_AI_TELLS = (
    "i loved your recent post",
    "i came across your profile",
    "i hope this email finds you well",
    "i wanted to reach out",
    "as a fellow",
    "i've been following your work",  # when unaccompanied by a concrete specific
)

MAX_TOUCH1_WORDS = 80  # 04-thu: best-performing cold emails are < 80 words.


@dataclass
class Finding:
    level: str        # "block" or "warn"
    code: str
    message: str


@dataclass
class GateResult:
    ok: bool
    findings: list[Finding] = field(default_factory=list)

    @property
    def blocking(self) -> list[Finding]:
        return [f for f in self.findings if f.level == "block"]

    @property
    def warnings(self) -> list[Finding]:
        return [f for f in self.findings if f.level == "warn"]


def _contains_any(text: str, needles: Iterable[str]) -> str | None:
    low = text.lower()
    for n in needles:
        if n in low:
            return n
    return None


def check_config(config: dict) -> GateResult:
    """CAN-SPAM structural requirements live in config (04-thu, Layer 4)."""
    findings: list[Finding] = []
    if not config.get("sender_physical_address", "").strip():
        findings.append(Finding(
            "block", "CANSPAM_NO_ADDRESS",
            "config.sender_physical_address is empty — CAN-SPAM requires a valid "
            "physical postal address in every email.",
        ))
    if not config.get("unsubscribe_url", "").strip():
        findings.append(Finding(
            "block", "CANSPAM_NO_OPTOUT",
            "config.unsubscribe_url is empty — CAN-SPAM requires a working opt-out "
            "in every email.",
        ))
    if not config.get("lia_documented", False):
        findings.append(Finding(
            "warn", "GDPR_NO_LIA",
            "config.lia_documented is false — document a Legitimate Interest "
            "Assessment before emailing EU prospects (04-thu, Layer 4).",
        ))
    return GateResult(ok=not any(f.level == "block" for f in findings), findings=findings)


def check_prospect(prospect: dict, config: dict) -> GateResult:
    """A prospect without a specific, real signal is a template waiting to happen."""
    findings: list[Finding] = []
    signal = (prospect.get("signal") or "").strip()
    if not signal:
        findings.append(Finding(
            "block", "NO_SIGNAL",
            f"{prospect.get('name', '?')}: empty 'signal' — precision-over-volume "
            "means every prospect needs a real, specific reason you are writing "
            "them (04-thu, Layer 2). Cut them or add the signal.",
        ))
    elif len(signal.split()) < 4:
        findings.append(Finding(
            "warn", "THIN_SIGNAL",
            f"{prospect.get('name', '?')}: 'signal' is very short — make sure it is "
            "a concrete observation, not a placeholder.",
        ))
    region = (prospect.get("region") or "").strip().upper()
    if region in {"EU", "EEA", "UK"} and not config.get("lia_documented", False):
        findings.append(Finding(
            "block", "GDPR_EU_NO_LIA",
            f"{prospect.get('name', '?')}: EU/UK prospect but no LIA documented — "
            "set config.lia_documented once you have written your Legitimate "
            "Interest Assessment.",
        ))
    return GateResult(ok=not any(f.level == "block" for f in findings), findings=findings)


def check_rendered_email(subject: str, body: str, *, is_first_touch: bool,
                         config: dict) -> GateResult:
    """Runs on the fully-rendered draft, right before it is written for review."""
    findings: list[Finding] = []
    combined = f"{subject}\n{body}"

    hit = _contains_any(combined, UPVOTE_SOLICITATION)
    if hit:
        findings.append(Finding(
            "block", "UPVOTE_ASK",
            f"Rendered draft asks for a vote ('{hit}') — prohibited by PH/HN "
            "guidelines (02-tue). Invite people to try it and give honest "
            "feedback instead.",
        ))

    tell = _contains_any(combined, GENERIC_AI_TELLS)
    if tell:
        findings.append(Finding(
            "warn", "AI_TELL",
            f"Rendered draft contains a generic-AI-personalization tell "
            f"('{tell}') — rewrite around a real specific (04-thu).",
        ))

    addr = config.get("sender_physical_address", "").strip()
    if addr and addr not in body:
        findings.append(Finding(
            "block", "MISSING_ADDRESS_IN_BODY",
            "Rendered draft is missing the physical postal address (CAN-SPAM).",
        ))
    unsub = config.get("unsubscribe_url", "").strip()
    if unsub and unsub not in body:
        findings.append(Finding(
            "block", "MISSING_OPTOUT_IN_BODY",
            "Rendered draft is missing the opt-out link (CAN-SPAM).",
        ))

    if is_first_touch:
        # Count only the "message" portion, excluding the compliance footer, so the
        # sub-80-word target reflects the actual pitch a human reads first.
        message = body.split("\n\n--\n")[0]
        words = len(message.split())
        if words > MAX_TOUCH1_WORDS:
            findings.append(Finding(
                "warn", "TOUCH1_TOO_LONG",
                f"First-touch message body is {words} words (> {MAX_TOUCH1_WORDS}). "
                "Shorter, specific emails reply better (04-thu).",
            ))

    return GateResult(ok=not any(f.level == "block" for f in findings), findings=findings)
