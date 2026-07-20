"""A fake in-memory CRM so the lab runs with zero external dependencies.

Keyed on phone number (E.164). The same identifier is the caller's number and
the WhatsApp user's number — which is exactly what makes the one-brain /
many-channels identity bridge (Friday's lesson) possible.
"""
from __future__ import annotations

# phone -> customer record
_CUSTOMERS: dict[str, dict] = {
    "+919000000001": {
        "name": "Priya",
        "appointments": [
            {"id": "A-1014", "when": "Tue 14th, 3:00pm", "provider": "Dr. Rao", "status": "confirmed"}
        ],
        "balance_due": 0.0,
    },
    "+919000000002": {
        "name": "Arjun",
        "appointments": [
            {"id": "A-1021", "when": "Thu 16th, 10:00am", "provider": "Dr. Mehta", "status": "confirmed"}
        ],
        "balance_due": 1250.0,
    },
}


def lookup_appointment(phone: str) -> dict:
    """Read-only. Returns the caller's next appointment or a not-found marker."""
    cust = _CUSTOMERS.get(phone)
    if not cust or not cust["appointments"]:
        return {"found": False}
    appt = cust["appointments"][0]
    return {"found": True, "name": cust["name"], **appt}


def lookup_balance(phone: str) -> dict:
    cust = _CUSTOMERS.get(phone)
    if not cust:
        return {"found": False}
    return {"found": True, "name": cust["name"], "balance_due": cust["balance_due"]}


# --- WRITE tools stay behind the gateway's ALLOW_WRITES flag (Thursday) ---

def reschedule_appointment(phone: str, appt_id: str, new_when: str) -> dict:
    """State-changing. Only reachable when ALLOW_WRITES=true AND the caller has
    confirmed via a confirmation-read (enforced in tools/gateway.py)."""
    cust = _CUSTOMERS.get(phone)
    if not cust:
        return {"ok": False, "reason": "no_customer"}
    for appt in cust["appointments"]:
        if appt["id"] == appt_id:
            appt["when"] = new_when
            return {"ok": True, "id": appt_id, "when": new_when}
    return {"ok": False, "reason": "no_appt"}
