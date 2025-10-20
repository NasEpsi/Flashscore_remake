from fastapi import APIRouter, Depends, Query
from sqlmodel import select, Session
from app.deps import get_session
from app.models import Match

router = APIRouter(prefix="/api/matches", tags=["matches"])

@router.get("")
def list_matches(
    competition_id: int | None = Query(default=None),
    season_id: int | None = Query(default=None),
    limit: int = Query(default=100, le=500),
    session: Session = Depends(get_session),
):
    q = select(Match)
    if competition_id:
        q = q.where(Match.competition_id == competition_id)
    if season_id:
        q = q.where(Match.season_id == season_id)
    q = q.order_by(Match.kick_off.desc()).limit(limit)
    return session.exec(q).all()
