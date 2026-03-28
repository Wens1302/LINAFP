# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import Competition
from schemas import CompetitionCreate, CompetitionUpdate, CompetitionResponse
from auth import require_editor_or_admin

router = APIRouter(prefix="/api/competitions", tags=["competitions"])


@router.get("", response_model=List[CompetitionResponse])
def list_competitions(db: Session = Depends(get_db)):
    return db.query(Competition).all()


@router.post("", response_model=CompetitionResponse, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(require_editor_or_admin())])
def create_competition(payload: CompetitionCreate, db: Session = Depends(get_db)):
    competition = Competition(**payload.model_dump())
    db.add(competition)
    db.commit()
    db.refresh(competition)
    return competition


@router.get("/{competition_id}", response_model=CompetitionResponse)
def get_competition(competition_id: int, db: Session = Depends(get_db)):
    competition = db.query(Competition).filter(Competition.id == competition_id).first()
    if not competition:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Competition not found")
    return competition


@router.put("/{competition_id}", response_model=CompetitionResponse,
            dependencies=[Depends(require_editor_or_admin())])
def update_competition(competition_id: int, payload: CompetitionUpdate, db: Session = Depends(get_db)):
    competition = db.query(Competition).filter(Competition.id == competition_id).first()
    if not competition:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Competition not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(competition, field, value)
    db.commit()
    db.refresh(competition)
    return competition


@router.delete("/{competition_id}", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(require_editor_or_admin())])
def delete_competition(competition_id: int, db: Session = Depends(get_db)):
    competition = db.query(Competition).filter(Competition.id == competition_id).first()
    if not competition:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Competition not found")
    db.delete(competition)
    db.commit()
