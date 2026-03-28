# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import Match, Team
from schemas import MatchCreate, MatchUpdate, MatchResponse

router = APIRouter(prefix="/api/matches", tags=["matches"])


@router.get("", response_model=List[MatchResponse])
def list_matches(db: Session = Depends(get_db)):
    return db.query(Match).order_by(Match.date.desc()).all()


@router.post("", response_model=MatchResponse, status_code=status.HTTP_201_CREATED)
def create_match(payload: MatchCreate, db: Session = Depends(get_db)):
    if payload.home_team_id == payload.away_team_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Home and away teams must be different",
        )
    for team_id in (payload.home_team_id, payload.away_team_id):
        if not db.query(Team).filter(Team.id == team_id).first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Team {team_id} not found")
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


@router.put("/{match_id}", response_model=MatchResponse)
def update_match(match_id: int, payload: MatchUpdate, db: Session = Depends(get_db)):
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Match not found")
    updates = payload.model_dump(exclude_unset=True)
    for team_field in ("home_team_id", "away_team_id"):
        if team_field in updates and not db.query(Team).filter(Team.id == updates[team_field]).first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
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


@router.delete("/{match_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_match(match_id: int, db: Session = Depends(get_db)):
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Match not found")
    db.delete(match)
    db.commit()
