from sqlmodel import Session, create_engine
from os import getenv

# Par défaut: SQLite local (fichier ./statsbomb.db)
DATABASE_URL = getenv("DATABASE_URL", "sqlite:///statsbomb.db")
engine = create_engine(DATABASE_URL, echo=False)

def get_session():
    with Session(engine) as session:
        yield session
        session.close()