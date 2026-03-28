# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from collections import defaultdict

from database import get_db
from models import Match, Player, Team
from schemas import StatsResponse, TopScorer, TeamGoals
from routers.standings import compute_standings

router = APIRouter(prefix="/api/stats", tags=["stats"])


@router.get("", response_model=StatsResponse)
def get_stats(db: Session = Depends(get_db)):
    # Top scorers – ranked by goals field on Player
    players = (
        db.query(Player)
        .filter(Player.goals > 0)
        .order_by(Player.goals.desc())
        .limit(10)
        .all()
    )
    team_map = {t.id: t.nom for t in db.query(Team).all()}

    top_scorers = [
        TopScorer(
            player_id=p.id,
            player_name=p.nom,
            team_name=team_map.get(p.team_id, ""),
            goals=p.goals,
        )
        for p in players
    ]

    # Goals per team derived from match results
    team_goals_map: dict = defaultdict(lambda: {"goals_for": 0, "goals_against": 0})
    for match in db.query(Match).all():
        team_goals_map[match.home_team_id]["goals_for"] += match.home_score
        team_goals_map[match.home_team_id]["goals_against"] += match.away_score
        team_goals_map[match.away_team_id]["goals_for"] += match.away_score
        team_goals_map[match.away_team_id]["goals_against"] += match.home_score

    teams_goals = [
        TeamGoals(
            team_id=team_id,
            team_name=team_map.get(team_id, ""),
            goals_for=data["goals_for"],
            goals_against=data["goals_against"],
        )
        for team_id, data in sorted(team_goals_map.items(), key=lambda x: -x[1]["goals_for"])
    ]

    standings = compute_standings(db)

    return StatsResponse(
        top_scorers=top_scorers,
        teams_goals=teams_goals,
        standings=standings,
    )
