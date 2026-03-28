# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
from models import Player, Team
from schemas import PlayerCreate, PlayerUpdate, PlayerResponse

router = APIRouter(prefix="/api/players", tags=["players"])


@router.get("", response_model=List[PlayerResponse])
def list_players(
    team_id: Optional[int] = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(Player)
    if team_id is not None:
        query = query.filter(Player.team_id == team_id)
    return query.all()


@router.post("", response_model=PlayerResponse, status_code=status.HTTP_201_CREATED)
def create_player(payload: PlayerCreate, db: Session = Depends(get_db)):
    if not db.query(Team).filter(Team.id == payload.team_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    player = Player(**payload.model_dump())
    db.add(player)
    db.commit()
    db.refresh(player)
    return player


@router.get("/{player_id}", response_model=PlayerResponse)
def get_player(player_id: int, db: Session = Depends(get_db)):
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player not found")
    return player


@router.put("/{player_id}", response_model=PlayerResponse)
def update_player(player_id: int, payload: PlayerUpdate, db: Session = Depends(get_db)):
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player not found")
    updates = payload.model_dump(exclude_unset=True)
    if "team_id" in updates and not db.query(Team).filter(Team.id == updates["team_id"]).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    for field, value in updates.items():
        setattr(player, field, value)
    db.commit()
    db.refresh(player)
    return player


@router.delete("/{player_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_player(player_id: int, db: Session = Depends(get_db)):
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player not found")
    db.delete(player)
    db.commit()
