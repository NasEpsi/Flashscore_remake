from fastapi import APIRouter, Depends
from sqlmodel import select, Session
from app.deps import get_session
from app.models import Event

router = APIRouter(prefix="/api/events", tags=["events"])

@router.get("/{match_id}")
def events_by_match(match_id: int, session: Session = Depends(get_session)):
    return session.exec(select(Event).where(Event.match_id == match_id).order_by(Event.index)).all()
