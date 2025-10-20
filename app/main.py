from typing import Iterable

from fastapi import FastAPI, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from sqlmodel import SQLModel, Session, select
from sqlalchemy import func

from app.deps import engine, get_session
from app.utils.flags import iso2_for_team
from app.models import Competition, Season, Team, Match, Event, Lineup, Player
from fastapi.responses import RedirectResponse
from app.routers.competitions import router as competitions_router
from app.routers.matches import router as matches_router
from app.routers.events import router as events_router

TOP_LEAGUE_KEYWORDS = [
    "Premier League", "La Liga", "Serie A", "Bundesliga", "Ligue 1",
    "Champions League", "Europa League",
]
TOP_INTL_KEYWORDS = [
    "World Cup", "FIFA World Cup", "Euro", "European Championship", "Copa América",
    "UEFA European Championship", "UEFA Nations League",
]

app = FastAPI(title="Flashscore-like (StatsBomb)")
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

app.include_router(competitions_router)
app.include_router(matches_router)
app.include_router(events_router)


@app.get("/", response_class=HTMLResponse)
def index(request: Request, session: Session = Depends(get_session)):
    rows = session.exec(
        select(Match).order_by(Match.kick_off.desc()).limit(300)
    ).all()
    team_names = {t.id: t.name for t in session.exec(select(Team)).all()}

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "matches": rows,
            "teams": team_names,
            "iso2_for_team": iso2_for_team,
        },
    )

def seasons_for_comp(session: Session, comp_id: int) -> list[Season]:
    return session.exec(
        select(Season)
        .where(Season.competition_id == comp_id)
        .order_by(Season.season_name.desc())
    ).all()

def find_competitions_by_keywords(session: Session, keywords: Iterable[str]) -> list[Competition]:
    comps = session.exec(select(Competition)).all()
    kw = [k.lower() for k in keywords]
    out = []
    seen = set()
    for c in comps:
        name = (c.name or "").lower()
        if any(k in name for k in kw) and c.id not in seen:
            out.append(c)
            seen.add(c.id)
    return out

@app.get("/competitions", response_class=HTMLResponse)
def competitions_page(request: Request, session: Session = Depends(get_session)):
    top_leagues = find_competitions_by_keywords(session, TOP_LEAGUE_KEYWORDS)
    top_international = find_competitions_by_keywords(session, TOP_INTL_KEYWORDS)
    counts = dict(
        session.exec(
            select(Match.competition_id, func.count(Match.id)).group_by(Match.competition_id)
        ).all()
    )
    return templates.TemplateResponse(
        "competitions.html",
        {
            "request": request,
            "top_leagues": top_leagues,
            "top_international": top_international,
            "counts": counts,
            "seasons_for_comp": lambda cid: seasons_for_comp(session, cid),
        },
    )

@app.get("/matches", response_class=HTMLResponse)
def matches_page(
    request: Request,
    competition_id: int | None = None,
    season_id: int | None = None,
    limit: int = 2000,   
    session: Session = Depends(get_session),
):
    q = select(Match)
    selected_comp = None
    selected_seasons: list[Season] = []

    if competition_id:
        q = q.where(Match.competition_id == competition_id)
        selected_comp = session.get(Competition, competition_id)
        selected_seasons = seasons_for_comp(session, competition_id)

    if season_id:
        q = q.where(Match.season_id == season_id)

    rows = session.exec(q.order_by(Match.kick_off.desc()).limit(min(limit, 10000))).all()
    team_names = {t.id: t.name for t in session.exec(select(Team)).all()}

    return templates.TemplateResponse(
        "matchs_list.html",
        {
            "request": request,
            "matches": rows,
            "teams": team_names,
            "selected_comp": selected_comp,
            "selected_seasons": selected_seasons,
            "competition_id": competition_id,
            "season_id": season_id,
            "iso2_for_team": iso2_for_team,
        },
    )


@app.get("/match/{match_id}", response_class=HTMLResponse)
def match_detail(match_id: int, request: Request, session: Session = Depends(get_session)):
    match = session.get(Match, match_id)
    if not match:
        return templates.TemplateResponse("match_detail.html", {"request": request, "match": None})

    events_list = session.exec(
        select(Event).where(Event.match_id == match_id).order_by(Event.index)
    ).all()

    team_names = {t.id: t.name for t in session.exec(select(Team)).all()}

    home_lu = session.exec(
        select(Lineup)
        .where(Lineup.match_id == match_id, Lineup.team_id == match.home_team_id)
        .order_by(Lineup.is_starter.desc(), Lineup.jersey_number)
    ).all()
    away_lu = session.exec(
        select(Lineup)
        .where(Lineup.match_id == match_id, Lineup.team_id == match.away_team_id)
        .order_by(Lineup.is_starter.desc(), Lineup.jersey_number)
    ).all()

    related = session.exec(
        select(Match)
        .where(
            Match.competition_id == match.competition_id,
            Match.season_id == match.season_id,
            Match.id != match.id,
        )
        .order_by(Match.kick_off.desc())
        .limit(30)
    ).all()

    return templates.TemplateResponse(
        "match_detail.html",
        {
            "request": request,
            "match": match,
            "events": events_list,
            "teams": team_names,
            "home_lineup": home_lu,
            "away_lineup": away_lu,
            "related_matches": related,
            "iso2_for_team": iso2_for_team,
        },
    )


@app.get("/competitions/{comp_id}")
def comp_redirect(comp_id: int):
    return RedirectResponse(url=f"/matches?competition_id={comp_id}", status_code=302)

@app.get("/competitions/{comp_id}/seasons/{season_id}")
def comp_season_redirect(comp_id: int, season_id: int):
    return RedirectResponse(url=f"/matches?competition_id={comp_id}&season_id={season_id}", status_code=302)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
