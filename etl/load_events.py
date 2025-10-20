from sqlmodel import Session
from app.models import Event
from .utils import DATA_DIR, load_json

def run(session: Session):
    events_dir = DATA_DIR / "events"
    if not events_dir.exists():
        raise RuntimeError(f"Dossier introuvable: {events_dir} — définis STATSBOMB_DATA_DIR ou clone open-data à côté du projet.")
    for event_file in events_dir.iterdir():
        if event_file.suffix != ".json":
            continue
        evs = load_json(event_file)
        try:
            match_id = int(event_file.stem)
        except ValueError:
            continue
        for idx, e in enumerate(evs):
            etype = (e.get("type") or {}).get("name")
            shot = e.get("shot") or {}
            pas = e.get("pass") or {}
            loc = e.get("location") or [None, None]
            end_loc = pas.get("end_location") or [None, None]
            event = Event(
                id=e["id"],
                match_id=match_id,
                index=idx,
                period=e.get("period"),
                minute=e.get("minute"),
                second=e.get("second"),
                team_id=(e.get("team") or {}).get("id"),
                player_id=(e.get("player") or {}).get("id"),
                type=etype,
                subtype=(shot.get("type") or {}).get("name") if etype == "Shot" else None,
                outcome=(shot.get("outcome") or {}).get("name") if etype=="Shot" else (pas.get("outcome") or {}).get("name"),
                x=loc[0], y=loc[1],
                xG=shot.get("statsbomb_xg"),
                pass_length=pas.get("length"),
                pass_end_x=end_loc[0], pass_end_y=end_loc[1],
                timestamp=e.get("timestamp"),
            )
            session.merge(event)
    session.commit()
