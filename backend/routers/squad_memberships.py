# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
from models import SquadMembership, Player, Team, Season
from schemas import SquadMembershipCreate, SquadMembershipUpdate, SquadMembershipResponse
from auth import require_editor_or_admin

router = APIRouter(prefix="/api/squad-memberships", tags=["squad-memberships"])


@router.get("", response_model=List[SquadMembershipResponse])
def list_memberships(
    season_id: Optional[int] = Query(default=None),
    team_id: Optional[int] = Query(default=None),
    player_id: Optional[int] = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(SquadMembership)
    if season_id is not None:
        query = query.filter(SquadMembership.season_id == season_id)
    if team_id is not None:
        query = query.filter(SquadMembership.team_id == team_id)
    if player_id is not None:
        query = query.filter(SquadMembership.player_id == player_id)
    return query.all()


@router.post("", response_model=SquadMembershipResponse, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(require_editor_or_admin())])
def create_membership(payload: SquadMembershipCreate, db: Session = Depends(get_db)):
    if not db.query(Player).filter(Player.id == payload.player_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player not found")
    if not db.query(Team).filter(Team.id == payload.team_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    if not db.query(Season).filter(Season.id == payload.season_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Season not found")
    membership = SquadMembership(**payload.model_dump())
    db.add(membership)
    db.commit()
    db.refresh(membership)
    return membership


@router.get("/{membership_id}", response_model=SquadMembershipResponse)
def get_membership(membership_id: int, db: Session = Depends(get_db)):
    membership = db.query(SquadMembership).filter(SquadMembership.id == membership_id).first()
    if not membership:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Membership not found")
    return membership


@router.put("/{membership_id}", response_model=SquadMembershipResponse,
            dependencies=[Depends(require_editor_or_admin())])
def update_membership(membership_id: int, payload: SquadMembershipUpdate, db: Session = Depends(get_db)):
    membership = db.query(SquadMembership).filter(SquadMembership.id == membership_id).first()
    if not membership:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Membership not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(membership, field, value)
    db.commit()
    db.refresh(membership)
    return membership


@router.delete("/{membership_id}", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(require_editor_or_admin())])
def delete_membership(membership_id: int, db: Session = Depends(get_db)):
    membership = db.query(SquadMembership).filter(SquadMembership.id == membership_id).first()
    if not membership:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Membership not found")
    db.delete(membership)
    db.commit()
