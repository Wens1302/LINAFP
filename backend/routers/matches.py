# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
from models import Match, Team, Season
from schemas import MatchCreate, MatchUpdate, MatchResponse
from auth import require_editor_or_admin

router = APIRouter(prefix="/api/matches", tags=["matches"])


@router.get("", response_model=List[MatchResponse])
def list_matches(
    season_id: Optional[int] = Query(default=None),
    journee: Optional[int] = Query(default=None),
    status: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(Match)
    if season_id is not None:
        query = query.filter(Match.season_id == season_id)
    if journee is not None:
        query = query.filter(Match.journee == journee)
    if status is not None:
        query = query.filter(Match.status == status)
    return query.order_by(Match.date.desc()).all()


@router.post("", response_model=MatchResponse, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(require_editor_or_admin())])
def create_match(payload: MatchCreate, db: Session = Depends(get_db)):
    if payload.home_team_id == payload.away_team_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Home and away teams must be different",
        )
    for team_id in (payload.home_team_id, payload.away_team_id):
        if not db.query(Team).filter(Team.id == team_id).first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Team {team_id} not found")
    if payload.season_id is not None and not db.query(Season).filter(Season.id == payload.season_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Season not found")
    match = Match(**payload.model_dump())
    db.add(match)
    db.commit()
    db.refresh(match)
    return match


@router.get("/{match_id}", response_model=MatchResponse)
def get_match(match_id: int, db: Session = Depends(get_db)):
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Match not found")
    return match


@router.put("/{match_id}", response_model=MatchResponse,
            dependencies=[Depends(require_editor_or_admin())])
def update_match(match_id: int, payload: MatchUpdate, db: Session = Depends(get_db)):
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Match not found")
    if match.locked:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Match is locked – no modifications allowed",
        )
    updates = payload.model_dump(exclude_unset=True)
    for team_field in ("home_team_id", "away_team_id"):
        if team_field in updates and not db.query(Team).filter(Team.id == updates[team_field]).first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    if "season_id" in updates and updates["season_id"] is not None:
        if not db.query(Season).filter(Season.id == updates["season_id"]).first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Season not found")
    home_id = updates.get("home_team_id", match.home_team_id)
    away_id = updates.get("away_team_id", match.away_team_id)
    if home_id == away_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Home and away teams must be different",
        )
    for field, value in updates.items():
        setattr(match, field, value)
    db.commit()
    db.refresh(match)
    return match


@router.delete("/{match_id}", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(require_editor_or_admin())])
def delete_match(match_id: int, db: Session = Depends(get_db)):
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Match not found")
    db.delete(match)
    db.commit()
