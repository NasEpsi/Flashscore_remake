from sqlmodel import Session
from app.models import Competition, Season
from .utils import DATA_DIR, load_json

def run(session: Session):
    comps = load_json(DATA_DIR / "competitions.json")
    for c in comps:
        session.merge(Competition(
            id=c["competition_id"],
            name=c["competition_name"],
            country=c.get("country_name")
        ))
        session.merge(Season(
            id=c["season_id"],
            competition_id=c["competition_id"],
            season_name=c["season_name"]
        ))
    session.commit()
