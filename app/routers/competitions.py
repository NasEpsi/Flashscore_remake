from fastapi import APIRouter, Depends
from sqlmodel import select, Session
from app.deps import get_session
from app.models import Competition

router = APIRouter(prefix="/api/competitions", tags=["competitions"])

@router.get("")
def list_competitions(session: Session = Depends(get_session)):
    return session.exec(select(Competition)).all()
