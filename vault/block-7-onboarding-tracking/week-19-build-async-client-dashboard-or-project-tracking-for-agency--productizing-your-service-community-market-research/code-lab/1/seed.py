"""Seed data + a runnable CLI demo.

Run:  python seed.py
It prints the two clients' dashboards (proving isolation), a grounded AI status
summary (offline mode), and the productized capacity/margin model.
"""

from __future__ import annotations

from pricing import ProductizedOffer, SopStep, capacity_model, next_lever
from store import (
    Client,
    DashboardStore,
    Deliverable,
    Metric,
    Project,
)
from summary import generate_summary


def build_seed_store() -> DashboardStore:
    store = DashboardStore()
    store.add_client(Client(id="acme", name="Acme Support", brand_color="#0a7"))
    store.add_client(Client(id="globex", name="Globex Ops", brand_color="#a30"))

    store.add_project(Project(
        id="p_acme", client_id="acme", name="AI support triage",
        status="on_track", phase="tuning", percent=70,
        status_reason="workflow live, tuning reply quality",
    ))
    store.add_project(Project(
        id="p_globex", client_id="globex", name="Ops automation",
        status="at_risk", phase="build", percent=30,
        status_reason="waiting on API access",
    ))

    store.add_deliverable(Deliverable(
        id="d1", client_id="acme", project_id="p_acme",
        name="Triage workflow v1", status="approved",
        link="https://example.com/d1", is_client_visible=True,
        blocked_on="none", created_at="2026-09-18",
    ))
    store.add_deliverable(Deliverable(
        id="d2", client_id="acme", project_id="p_acme",
        name="Reply-draft workflow", status="in_review",
        link="https://example.com/d2", is_client_visible=True,
        blocked_on="client", created_at="2026-09-22",
    ))
    # An internal-only deliverable the client must NOT see.
    store.add_deliverable(Deliverable(
        id="d3", client_id="acme", project_id="p_acme",
        name="Internal QA notes", status="draft",
        is_client_visible=False, created_at="2026-09-22",
    ))
    store.add_deliverable(Deliverable(
        id="d4", client_id="globex", project_id="p_globex",
        name="Data pipeline draft", status="draft",
        is_client_visible=True, blocked_on="client", created_at="2026-09-20",
    ))

    store.add_metric(Metric(
        id="m1", client_id="acme", project_id="p_acme",
        label="tickets deflected", value=312, unit="/wk", recorded_at="2026-09-22",
    ))
    store.add_metric(Metric(
        id="m2", client_id="acme", project_id="p_acme",
        label="median response", value=3.2, unit="min", recorded_at="2026-09-22",
    ))
    return store


def sample_offer() -> ProductizedOffer:
    """The Wednesday triage offer, with the Thursday SOP + verification hours."""
    offer = ProductizedOffer(
        name="AI support-triage build",
        price=6000.0,
        timeline_days=10,
        tooling_cost_per_client=75.0,
        steps=[
            SopStep("intake + access", "human", 2.0),
            SopStep("workflow build from template", "llm", 3.0),  # incl. review
            SopStep("AI-drafted test cases", "llm", 0.5),         # verification
            SopStep("QA against eval checklist", "human", 2.0),
            SopStep("client walkthrough", "human", 1.0),
            SopStep("two weeks tuning", "human", 4.0),
        ],
    )
    return offer


def _demo() -> None:
    store = build_seed_store()

    print("=== ACME dashboard (client-scoped) ===")
    acme = store.client_view("acme")
    print("visible deliverables:", [d["name"] for d in acme["deliverables"]])
    print("blocked on you:", acme["blocked_on_you"])
    print("metrics:", acme["metrics"])

    print("\n=== Isolation check ===")
    globex = store.client_view("globex")
    print("globex sees only:", [d["name"] for d in globex["deliverables"]])
    assert "Triage workflow v1" not in [d["name"] for d in globex["deliverables"]]
    assert "Internal QA notes" not in [d["name"] for d in acme["deliverables"]]
    print("PASS: no cross-tenant leak; internal deliverable hidden from client")

    print("\n=== Grounded AI status summary (offline draft) ===")
    summ = generate_summary(store, "acme", use_llm=False)
    print(f"[{summ['status']}/{summ['mode']}] {summ['summary']}")

    print("\n=== Productized capacity / margin model ===")
    offer = sample_offer()
    result = capacity_model(offer, available_delivery_hours_per_period=25.0)
    print(f"offer: {offer.name} @ ${offer.price:,.0f}")
    print(f"human hours/client: {result.human_hours_per_client} "
          f"(verification: {result.verification_hours_per_client})")
    print(f"max clients/period: {result.max_clients}  "
          f"revenue ceiling: ${result.revenue_ceiling:,.0f}  "
          f"gross margin: {result.gross_margin:.0%}")
    print("next lever:", next_lever(result, target_revenue=60000.0))


if __name__ == "__main__":
    _demo()
