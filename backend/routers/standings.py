from collections import defaultdict
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import Match, Team
from schemas import StandingResponse

router = APIRouter(prefix="/api/standings", tags=["standings"])


def compute_standings(db: Session) -> List[StandingResponse]:
    teams = db.query(Team).all()
    matches = db.query(Match).all()

    stats: dict = defaultdict(lambda: {
        "points": 0, "played": 0, "won": 0,
        "drawn": 0, "lost": 0, "goals_for": 0, "goals_against": 0,
    })

    for match in matches:
        h = match.home_team_id
        a = match.away_team_id
        hs = match.home_score
        as_ = match.away_score

        stats[h]["played"] += 1
        stats[a]["played"] += 1
        stats[h]["goals_for"] += hs
        stats[h]["goals_against"] += as_
        stats[a]["goals_for"] += as_
        stats[a]["goals_against"] += hs

        if hs > as_:
            stats[h]["won"] += 1
            stats[h]["points"] += 3
            stats[a]["lost"] += 1
        elif hs < as_:
            stats[a]["won"] += 1
            stats[a]["points"] += 3
            stats[h]["lost"] += 1
        else:
            stats[h]["drawn"] += 1
            stats[h]["points"] += 1
            stats[a]["drawn"] += 1
            stats[a]["points"] += 1

    team_map = {t.id: t.nom for t in teams}

    results = []
    for team in teams:
        s = stats[team.id]
        results.append(StandingResponse(
            team_id=team.id,
            team_name=team_map.get(team.id, ""),
            points=s["points"],
            played=s["played"],
            won=s["won"],
            drawn=s["drawn"],
            lost=s["lost"],
            goals_for=s["goals_for"],
            goals_against=s["goals_against"],
            goal_difference=s["goals_for"] - s["goals_against"],
        ))

    results.sort(key=lambda x: (-x.points, -x.goal_difference))
    return results


@router.get("", response_model=List[StandingResponse])
def get_standings(db: Session = Depends(get_db)):
    return compute_standings(db)
