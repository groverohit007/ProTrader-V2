from fastapi import APIRouter

from schemas import TeamCreateRequest
from store import store

router = APIRouter(prefix="/org", tags=["org"])


@router.post("/teams")
def create_team(req: TeamCreateRequest):
    team = req.model_dump()
    store.teams.setdefault(req.org_id, []).append(team)
    store.add_audit(req.org_id, "system", "team_created", {"team_name": req.team_name})
    return team


@router.get("/teams/{org_id}")
def get_teams(org_id: str):
    return {"org_id": org_id, "teams": store.teams.get(org_id, [])}


@router.post("/audit/{org_id}")
def add_audit(org_id: str, actor: str, action: str):
    details = {"message": "manual audit event"}
    store.add_audit(org_id, actor, action, details)
    return {"status": "ok"}


@router.get("/audit/{org_id}")
def get_audit(org_id: str):
    events = [e.__dict__ for e in store.audit_logs.get(org_id, [])]
    return {"org_id": org_id, "events": events}
