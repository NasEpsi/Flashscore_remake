from sqlmodel import Session
from app.models import Match, Team
from .utils import DATA_DIR, load_json
from datetime import datetime

def run(session: Session):
    matches_root = DATA_DIR / "matches"
    if not matches_root.exists():
        raise RuntimeError(f"Dossier introuvable: {matches_root} — définis STATSBOMB_DATA_DIR ou clone open-data à côté du projet.")
    for comp_dir in matches_root.iterdir():
        if not comp_dir.is_dir(): 
            continue
        for season_file in comp_dir.iterdir():
            if season_file.suffix != ".json":
                continue
            matches = load_json(season_file)
            for m in matches:
                home = Team(id=m["home_team"]["home_team_id"], name=m["home_team"]["home_team_name"])
                away = Team(id=m["away_team"]["away_team_id"], name=m["away_team"]["away_team_name"])
                session.merge(home); session.merge(away)

                dt_str = m.get("match_datetime") or (m.get("match_date") + "T00:00:00")
                kick = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))

                match = Match(
                    id=m["match_id"],
                    competition_id=m["competition"]["competition_id"],
                    season_id=m["season"]["season_id"],
                    home_team_id=home.id,
                    away_team_id=away.id,
                    kick_off=kick,
                    stadium=(m.get("stadium") or {}).get("name"),
                    referee=(m.get("referee") or {}).get("name"),
                    home_score=m.get("home_score", 0),
                    away_score=m.get("away_score", 0),
                    status="finished",
                )
                session.merge(match)
    session.commit()
