"""Productized-service pricing and capacity/margin model.

Implements the Thursday capacity model and the Wednesday offer design. The one
non-negotiable design choice, straight from the lesson: verification hours are a
required, explicit input. A model with zero verification time is dishonest, so
we refuse it.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class SopStep:
    """One delivery step. ``doer`` is one of: code | llm | human.

    ``human_hours`` is the human time the step costs. For an ``llm`` step this
    is the VERIFICATION time (reviewing/fixing AI output), which the lesson
    insists you count.
    """

    name: str
    doer: str  # "code" | "llm" | "human"
    human_hours: float

    def __post_init__(self) -> None:
        if self.doer not in {"code", "llm", "human"}:
            raise ValueError(f"doer must be code|llm|human, got {self.doer!r}")
        if self.human_hours < 0:
            raise ValueError("human_hours cannot be negative")


@dataclass
class ProductizedOffer:
    """A fixed-scope, fixed-price offer with an annotated delivery SOP."""

    name: str
    price: float
    timeline_days: int
    steps: list[SopStep] = field(default_factory=list)
    tooling_cost_per_client: float = 0.0
    subcontractor_cost_per_client: float = 0.0

    def human_hours_per_client(self) -> float:
        return sum(s.human_hours for s in self.steps)

    def verification_hours_per_client(self) -> float:
        """Human hours spent verifying AI (llm) output. Must be > 0 if any
        step is an llm step, per the lesson's honesty rule."""
        return sum(s.human_hours for s in self.steps if s.doer == "llm")

    def assert_honest(self) -> None:
        """Reject a model that claims AI delivery with zero verification cost."""
        has_llm = any(s.doer == "llm" for s in self.steps)
        if has_llm and self.verification_hours_per_client() <= 0:
            raise ValueError(
                "offer has llm steps but zero verification hours: the lesson "
                "forbids pricing AI verification at zero"
            )


@dataclass
class CapacityResult:
    max_clients: float
    revenue_ceiling: float
    human_hours_per_client: float
    verification_hours_per_client: float
    gross_margin: float


def capacity_model(
    offer: ProductizedOffer,
    available_delivery_hours_per_period: float,
    clients_per_period: float | None = None,
) -> CapacityResult:
    """Compute the honest ceiling for a productized offer.

    ``available_delivery_hours_per_period`` is your REAL deliverable hours after
    sales/admin/support, not a fantasy 40. ``clients_per_period`` (optional) is
    how many new clients you actually onboard per period for the revenue/margin
    figures; defaults to the capacity ceiling.
    """
    offer.assert_honest()
    hours = offer.human_hours_per_client()
    if hours <= 0:
        raise ValueError("human_hours_per_client must be > 0")
    if available_delivery_hours_per_period <= 0:
        raise ValueError("available delivery hours must be > 0")

    max_clients = available_delivery_hours_per_period / hours
    served = clients_per_period if clients_per_period is not None else max_clients
    revenue = served * offer.price
    variable_cost = served * (
        offer.tooling_cost_per_client + offer.subcontractor_cost_per_client
    )
    gross_margin = (revenue - variable_cost) / revenue if revenue else 0.0

    return CapacityResult(
        max_clients=round(max_clients, 2),
        revenue_ceiling=round(revenue, 2),
        human_hours_per_client=round(hours, 2),
        verification_hours_per_client=round(offer.verification_hours_per_client(), 2),
        gross_margin=round(gross_margin, 4),
    )


def next_lever(result: CapacityResult, target_revenue: float) -> str:
    """Recommend the first lever to pull to reach a revenue target."""
    if result.revenue_ceiling >= target_revenue:
        return "you are within capacity at current price; sell more, do not scale"
    verification_share = (
        result.verification_hours_per_client / result.human_hours_per_client
        if result.human_hours_per_client else 0.0
    )
    if verification_share < 0.4:
        return (
            "raise price (protect your hours) or push more low-judgment steps "
            "onto AI to shrink hours-per-client"
        )
    return (
        "verification dominates your hours; you cannot safely automate the "
        "quality gate, so add capacity via a subcontractor running your SOP "
        "while you own the gate"
    )
