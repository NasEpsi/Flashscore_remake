from sqlmodel import SQLModel, Session, create_engine
from app.deps import DATABASE_URL
from .load_competitions import run as load_competitions
from .load_matches import run as load_matches
from .load_events import run as load_events
from .load_lineups import run as load_lineups


def main():
    engine = create_engine(DATABASE_URL, echo=False)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        print(">> Load competitions & seasons")
        load_competitions(session)
        print(">> Load matches")
        load_matches(session)
        print(">> Load events")
        load_events(session)
        print(">> Done")
        print(">> Load lineups")
        load_lineups(session)

if __name__ == "__main__":
    main()
