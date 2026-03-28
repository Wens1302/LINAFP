# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
from models import Season, Competition
from schemas import SeasonCreate, SeasonUpdate, SeasonResponse
from auth import require_editor_or_admin

router = APIRouter(prefix="/api/seasons", tags=["seasons"])


@router.get("", response_model=List[SeasonResponse])
def list_seasons(
    competition_id: Optional[int] = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(Season)
    if competition_id is not None:
        query = query.filter(Season.competition_id == competition_id)
    return query.all()


@router.post("", response_model=SeasonResponse, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(require_editor_or_admin())])
def create_season(payload: SeasonCreate, db: Session = Depends(get_db)):
    if not db.query(Competition).filter(Competition.id == payload.competition_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Competition not found")
    season = Season(**payload.model_dump())
    db.add(season)
    db.commit()
    db.refresh(season)
    return season


@router.get("/{season_id}", response_model=SeasonResponse)
def get_season(season_id: int, db: Session = Depends(get_db)):
    season = db.query(Season).filter(Season.id == season_id).first()
    if not season:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Season not found")
    return season


@router.put("/{season_id}", response_model=SeasonResponse,
            dependencies=[Depends(require_editor_or_admin())])
def update_season(season_id: int, payload: SeasonUpdate, db: Session = Depends(get_db)):
    season = db.query(Season).filter(Season.id == season_id).first()
    if not season:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Season not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(season, field, value)
    db.commit()
    db.refresh(season)
    return season


@router.delete("/{season_id}", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(require_editor_or_admin())])
def delete_season(season_id: int, db: Session = Depends(get_db)):
    season = db.query(Season).filter(Season.id == season_id).first()
    if not season:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Season not found")
    db.delete(season)
    db.commit()
