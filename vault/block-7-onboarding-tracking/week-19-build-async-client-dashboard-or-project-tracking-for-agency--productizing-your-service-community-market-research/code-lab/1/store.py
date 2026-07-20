"""Tenant-scoped in-memory data store for a client dashboard.

This module demonstrates the multi-tenant access pattern from the Tuesday
lesson in a dependency-free, testable way. In production you would push this
guarantee into the database with PostgreSQL Row-Level Security (see README).
Here we enforce the same rule in one place, fail-closed: every read is scoped
to a caller's ``client_id`` and cross-tenant access raises rather than leaking.

The point of the design: isolation lives in a single choke point
(``_require_same_tenant``), not scattered across every query, so a caller can
never accidentally forget the tenant filter.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

ProjectStatus = Literal["on_track", "at_risk", "blocked"]
DeliverableStatus = Literal["draft", "in_review", "approved"]
BlockedOn = Literal["none", "us", "client"]


class TenantAccessError(PermissionError):
    """Raised when a caller requests data outside their own tenant."""


@dataclass(frozen=True)
class Client:
    id: str
    name: str
    brand_color: str = "#111111"
    logo_url: str = ""


@dataclass
class Project:
    id: str
    client_id: str
    name: str
    status: ProjectStatus = "on_track"
    phase: str = "kickoff"
    percent: int = 0
    status_reason: str = ""


@dataclass
class Deliverable:
    id: str
    client_id: str
    project_id: str
    name: str
    status: DeliverableStatus = "draft"
    link: str = ""
    is_client_visible: bool = False
    blocked_on: BlockedOn = "none"
    created_at: str = ""


@dataclass
class Metric:
    id: str
    client_id: str
    project_id: str
    label: str
    value: float
    unit: str = ""
    recorded_at: str = ""


@dataclass
class DashboardStore:
    """A tiny multi-tenant store. Every accessor requires a caller tenant."""

    clients: dict[str, Client] = field(default_factory=dict)
    projects: dict[str, Project] = field(default_factory=dict)
    deliverables: dict[str, Deliverable] = field(default_factory=dict)
    metrics: dict[str, Metric] = field(default_factory=dict)

    # ---- writes (server-side / trusted) ------------------------------------
    def add_client(self, client: Client) -> None:
        self.clients[client.id] = client

    def add_project(self, project: Project) -> None:
        self._require_known_client(project.client_id)
        self.projects[project.id] = project

    def add_deliverable(self, deliverable: Deliverable) -> None:
        self._require_known_client(deliverable.client_id)
        self.deliverables[deliverable.id] = deliverable

    def add_metric(self, metric: Metric) -> None:
        self._require_known_client(metric.client_id)
        self.metrics[metric.id] = metric

    # ---- tenant-scoped reads (the choke point) -----------------------------
    def projects_for(self, caller_client_id: str) -> list[Project]:
        return [
            p for p in self.projects.values()
            if self._same_tenant(caller_client_id, p.client_id)
        ]

    def deliverables_for(
        self, caller_client_id: str, client_visible_only: bool = True
    ) -> list[Deliverable]:
        rows = [
            d for d in self.deliverables.values()
            if self._same_tenant(caller_client_id, d.client_id)
        ]
        if client_visible_only:
            rows = [d for d in rows if d.is_client_visible]
        return rows

    def metrics_for(self, caller_client_id: str) -> list[Metric]:
        return [
            m for m in self.metrics.values()
            if self._same_tenant(caller_client_id, m.client_id)
        ]

    def get_project(self, caller_client_id: str, project_id: str) -> Project:
        project = self.projects.get(project_id)
        if project is None:
            raise KeyError(project_id)
        self._require_same_tenant(caller_client_id, project.client_id)
        return project

    def client_view(self, caller_client_id: str) -> dict:
        """The read-only client-facing surface: the four Monday sections."""
        self._require_known_client(caller_client_id)
        client = self.clients[caller_client_id]
        deliverables = self.deliverables_for(caller_client_id)
        return {
            "client": {"id": client.id, "name": client.name,
                       "brand_color": client.brand_color},
            "progress": [
                {"project": p.name, "status": p.status, "phase": p.phase,
                 "percent": p.percent, "reason": p.status_reason}
                for p in self.projects_for(caller_client_id)
            ],
            "deliverables": [
                {"name": d.name, "status": d.status, "link": d.link,
                 "created_at": d.created_at}
                for d in deliverables
            ],
            "blocked_on_you": [
                d.name for d in deliverables if d.blocked_on == "client"
            ],
            "metrics": [
                {"label": m.label, "value": m.value, "unit": m.unit}
                for m in self.metrics_for(caller_client_id)
            ],
        }

    # ---- isolation helpers -------------------------------------------------
    @staticmethod
    def _same_tenant(caller: str, owner: str) -> bool:
        return caller == owner

    def _require_same_tenant(self, caller: str, owner: str) -> None:
        if not self._same_tenant(caller, owner):
            raise TenantAccessError(
                f"caller '{caller}' may not access data owned by '{owner}'"
            )

    def _require_known_client(self, client_id: str) -> None:
        if client_id not in self.clients:
            raise KeyError(f"unknown client '{client_id}'")
