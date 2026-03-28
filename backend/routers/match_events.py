# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import MatchEvent, Match, Player
from schemas import MatchEventCreate, MatchEventUpdate, MatchEventResponse
from auth import require_editor_or_admin

router = APIRouter(prefix="/api/matches", tags=["match-events"])


@router.get("/{match_id}/events", response_model=List[MatchEventResponse])
def list_match_events(match_id: int, db: Session = Depends(get_db)):
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Match not found")
    return db.query(MatchEvent).filter(MatchEvent.match_id == match_id).order_by(MatchEvent.minute).all()


@router.post("/{match_id}/events", response_model=MatchEventResponse,
             status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(require_editor_or_admin())])
def create_match_event(match_id: int, payload: MatchEventCreate, db: Session = Depends(get_db)):
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Match not found")
    if match.locked:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Match is locked – no modifications allowed",
        )
    # Validate player belongs to one of the match teams
    for pid_field in ("player_id", "player_in_id", "assister_id"):
        pid = getattr(payload, pid_field)
        if pid is not None:
            player = db.query(Player).filter(Player.id == pid).first()
            if not player:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Player {pid} not found")
            if player.team_id not in (match.home_team_id, match.away_team_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Player {pid} does not belong to either match team",
                )
    event = MatchEvent(match_id=match_id, **payload.model_dump())
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


@router.put("/{match_id}/events/{event_id}", response_model=MatchEventResponse,
            dependencies=[Depends(require_editor_or_admin())])
def update_match_event(match_id: int, event_id: int, payload: MatchEventUpdate, db: Session = Depends(get_db)):
    event = db.query(MatchEvent).filter(
        MatchEvent.id == event_id, MatchEvent.match_id == match_id
    ).first()
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    match = db.query(Match).filter(Match.id == match_id).first()
    if match and match.locked:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Match is locked – no modifications allowed",
        )
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(event, field, value)
    # Re-validate player associations after update
    for pid_field in ("player_id", "player_in_id", "assister_id"):
        pid = getattr(event, pid_field)
        if pid is not None:
            player = db.query(Player).filter(Player.id == pid).first()
            if not player:
                db.rollback()
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Player {pid} not found")
            if player.team_id not in (match.home_team_id, match.away_team_id):
                db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Player {pid} does not belong to either match team",
                )
    db.commit()
    db.refresh(event)
    return event


@router.delete("/{match_id}/events/{event_id}", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(require_editor_or_admin())])
def delete_match_event(match_id: int, event_id: int, db: Session = Depends(get_db)):
    event = db.query(MatchEvent).filter(
        MatchEvent.id == event_id, MatchEvent.match_id == match_id
    ).first()
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    match = db.query(Match).filter(Match.id == match_id).first()
    if match and match.locked:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Match is locked – no modifications allowed",
        )
    db.delete(event)
    db.commit()
