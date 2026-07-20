"""FastAPI client-dashboard backend.

Endpoints are tenant-scoped: the caller's ``client_id`` comes from an auth
dependency (here faked via a header; in production it is a verified JWT claim,
per the Tuesday lesson). Every read goes through the store's single isolation
choke point, so a client can only ever see their own project.

Run:  uvicorn app:app --reload      (needs: pip install -r requirements.txt)
Then: GET /me/dashboard   with header  X-Client-Id: acme
      GET /me/summary     with header  X-Client-Id: acme

The whole app also runs offline: the AI summary falls back to a deterministic
template when no ANTHROPIC_API_KEY is set.
"""

from __future__ import annotations

from fastapi import Depends, FastAPI, Header, HTTPException

from pricing import CapacityResult, capacity_model, next_lever
from seed import build_seed_store, sample_offer
from store import DashboardStore, TenantAccessError
from summary import generate_summary

app = FastAPI(title="Client Dashboard Backend", version="1.0.0")
STORE: DashboardStore = build_seed_store()


def current_client_id(x_client_id: str = Header(...)) -> str:
    """Stand-in for auth. In production this is a verified JWT ``client_id``
    claim (see README: it becomes the RLS policy input, not app-layer code)."""
    if x_client_id not in STORE.clients:
        raise HTTPException(status_code=401, detail="unknown client")
    return x_client_id


@app.get("/me/dashboard")
def my_dashboard(client_id: str = Depends(current_client_id)) -> dict:
    try:
        return STORE.client_view(client_id)
    except TenantAccessError as exc:  # pragma: no cover - defense in depth
        raise HTTPException(status_code=403, detail=str(exc)) from exc


@app.get("/me/summary")
def my_summary(
    client_id: str = Depends(current_client_id), use_llm: bool = False
) -> dict:
    return generate_summary(STORE, client_id, use_llm=use_llm)


@app.get("/me/projects/{project_id}")
def my_project(
    project_id: str, client_id: str = Depends(current_client_id)
) -> dict:
    try:
        project = STORE.get_project(client_id, project_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="not found")
    except TenantAccessError:
        # Do not reveal that the project exists for another tenant.
        raise HTTPException(status_code=404, detail="not found")
    return project.__dict__


@app.get("/ops/capacity")
def capacity(available_hours: float = 25.0, target_revenue: float = 60000.0) -> dict:
    """Ops-only view: the productized capacity/margin model for the sample offer."""
    offer = sample_offer()
    result: CapacityResult = capacity_model(offer, available_hours)
    return {
        "offer": offer.name,
        "price": offer.price,
        "result": result.__dict__,
        "next_lever": next_lever(result, target_revenue),
    }
