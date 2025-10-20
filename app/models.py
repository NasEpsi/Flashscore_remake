# app/models.py
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field
from typing import Optional
from sqlmodel import SQLModel, Field

class Competition(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    country: Optional[str] = None

class Season(SQLModel, table=True):
    id: int = Field(primary_key=True)
    competition_id: int = Field(foreign_key="competition.id")
    season_name: str

class Team(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str

class Match(SQLModel, table=True):
    id: int = Field(primary_key=True)
    competition_id: int = Field(foreign_key="competition.id")
    season_id: int = Field(foreign_key="season.id")
    home_team_id: int = Field(foreign_key="team.id")
    away_team_id: int = Field(foreign_key="team.id")
    kick_off: datetime
    stadium: Optional[str] = None
    referee: Optional[str] = None
    home_score: int = 0
    away_score: int = 0
    status: str = "finished"

class Event(SQLModel, table=True):
    id: str = Field(primary_key=True)
    match_id: int = Field(index=True, foreign_key="match.id")
    index: int = Field(index=True)

    period: Optional[int] = None
    minute: Optional[int] = None
    second: Optional[int] = None

    team_id: Optional[int] = Field(default=None, foreign_key="team.id")
    player_id: Optional[int] = None

    type: Optional[str] = None
    subtype: Optional[str] = None
    outcome: Optional[str] = None

    x: Optional[float] = None
    y: Optional[float] = None
    xG: Optional[float] = None

    pass_length: Optional[float] = None
    pass_end_x: Optional[float] = None
    pass_end_y: Optional[float] = None

    timestamp: Optional[str] = None
    assisting_player_id: Optional[int] = None 

class Player(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    country: Optional[str] = None
    footed: Optional[str] = None

class Lineup(SQLModel, table=True):
    id: int = Field(primary_key=True)  # auto local (on le génèrera)
    match_id: int = Field(index=True, foreign_key="match.id")
    team_id: int = Field(index=True, foreign_key="team.id")
    player_id: int = Field(index=True, foreign_key="player.id")
    player_name: str
    jersey_number: Optional[int] = None
    position: Optional[str] = None     
    is_starter: bool = False
    minute_on: Optional[int] = None     
    minute_off: Optional[int] = None    