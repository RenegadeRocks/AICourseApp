"""Tests for the client-dashboard backend, AI summary, and pricing model.

Runs with plain `python test_dashboard.py` (no pytest, no network, no API key)
or under `python -m pytest`. All logic is exercised offline.
"""

from __future__ import annotations

from pricing import ProductizedOffer, SopStep, capacity_model, next_lever
from seed import build_seed_store, sample_offer
from store import DashboardStore, TenantAccessError
from summary import assemble_facts, generate_summary


def test_tenant_isolation_no_cross_leak() -> None:
    store = build_seed_store()
    acme = store.client_view("acme")
    globex = store.client_view("globex")
    acme_names = [d["name"] for d in acme["deliverables"]]
    globex_names = [d["name"] for d in globex["deliverables"]]
    assert "Triage workflow v1" in acme_names
    assert "Triage workflow v1" not in globex_names
    assert "Data pipeline draft" not in acme_names


def test_internal_deliverable_hidden_from_client() -> None:
    store = build_seed_store()
    acme = store.client_view("acme")
    assert "Internal QA notes" not in [d["name"] for d in acme["deliverables"]]


def test_get_project_cross_tenant_raises() -> None:
    store = build_seed_store()
    try:
        store.get_project("globex", "p_acme")
    except TenantAccessError:
        pass
    else:  # pragma: no cover
        raise AssertionError("expected TenantAccessError on cross-tenant read")


def test_blocked_on_you_surfaced() -> None:
    store = build_seed_store()
    acme = store.client_view("acme")
    assert "Reply-draft workflow" in acme["blocked_on_you"]


def test_summary_is_grounded_and_draft() -> None:
    store = build_seed_store()
    out = generate_summary(store, "acme", use_llm=False)
    assert out["status"] == "draft"           # never auto-sent
    assert out["mode"] == "offline"
    # summary only mentions approved (shipped) deliverables, not drafts
    assert "Triage workflow v1" in out["summary"]
    assert "Internal QA notes" not in out["summary"]
    assert "Acme Support" in out["summary"]


def test_summary_facts_match_store() -> None:
    store = build_seed_store()
    facts = assemble_facts(store, "acme")
    assert facts.shipped == ["Triage workflow v1"]
    assert "Reply-draft workflow" in facts.blocked_on_client


def test_capacity_model_math() -> None:
    offer = sample_offer()
    # 2+3+0.5+2+1+4 = 12.5 human hours/client
    assert abs(offer.human_hours_per_client() - 12.5) < 1e-9
    # llm steps: 3 + 0.5 = 3.5 verification hours
    assert abs(offer.verification_hours_per_client() - 3.5) < 1e-9
    result = capacity_model(offer, available_delivery_hours_per_period=25.0)
    assert abs(result.max_clients - 2.0) < 1e-9         # 25 / 12.5
    assert abs(result.revenue_ceiling - 12000.0) < 1e-9  # 2 * 6000


def test_capacity_rejects_zero_verification() -> None:
    dishonest = ProductizedOffer(
        name="hype offer", price=6000.0, timeline_days=10,
        steps=[SopStep("all AI, no checking", "llm", 0.0)],
    )
    try:
        capacity_model(dishonest, available_delivery_hours_per_period=25.0)
    except ValueError:
        pass
    else:  # pragma: no cover
        raise AssertionError("expected ValueError for zero-verification AI offer")


def test_next_lever_recommendation() -> None:
    offer = sample_offer()
    result = capacity_model(offer, available_delivery_hours_per_period=25.0)
    # verification share = 3.5 / 12.5 = 0.28 < 0.4 -> price/AI lever
    lever = next_lever(result, target_revenue=60000.0)
    assert "raise price" in lever or "AI" in lever


def _run_all() -> None:
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print(f"PASS {t.__name__}")
    print(f"\n{len(tests)} tests passed")


if __name__ == "__main__":
    _run_all()
