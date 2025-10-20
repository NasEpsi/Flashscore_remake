# etl/load_lineups.py
from sqlmodel import Session
from app.models import Lineup, Player, Team
from .utils import DATA_DIR, load_json

def _to_min(t: str | None) -> int | None:
    if not t:
        return None
    try:
        h, m, s = t.split(":")
        return int(h) * 60 + int(m)
    except Exception:
        return None

def run(session: Session):
    lineups_dir = DATA_DIR / "lineups"
    if not lineups_dir.exists():
        raise RuntimeError(f"Dossier introuvable: {lineups_dir} — définis STATSBOMB_DATA_DIR ou clone open-data.")
    auto_id = 1
    for f in lineups_dir.iterdir():
        if f.suffix != ".json":
            continue
        try:
            match_id = int(f.stem)
        except ValueError:
            continue

        data = load_json(f)  # [{ "team": {...}, "lineup": [...] }, ...]
        for block in data:
            team = block.get("team") or {}
            team_id = team.get("id") or team.get("team_id")  # parfois "id", parfois "team_id"
            team_name = team.get("name") or team.get("team_name") or (f"Team {team_id}" if team_id else "Unknown")
            if team_id:
                session.merge(Team(id=team_id, name=team_name))

            for p in block.get("lineup", []):
                p_obj = p.get("player") or {}
                pid = p_obj.get("id") or p.get("player_id")
                pname = p_obj.get("name") or p.get("player_name") or (f"Player {pid}" if pid else "Unknown")
                jersey = p.get("jersey_number")

                if pid:
                    session.merge(Player(id=pid, name=pname))

                pos_list = p.get("positions") or []
                pos0 = pos_list[0] if pos_list else {}
                position = pos0.get("position") or None
                is_starter = (pos0.get("from") == "00:00:00.000") or (pos0.get("start_reason") == "Starting XI")
                minute_on = _to_min(pos0.get("from"))
                minute_off = _to_min(pos0.get("to"))

                lu = Lineup(
                    id=auto_id,
                    match_id=match_id,
                    team_id=team_id or 0,
                    player_id=pid or 0,
                    player_name=pname,
                    jersey_number=jersey,
                    position=position,
                    is_starter=is_starter,
                    minute_on=minute_on,
                    minute_off=minute_off,
                )
                auto_id += 1
                session.merge(lu)
    session.commit()
