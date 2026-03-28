# -*- coding: utf-8 -*-
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from database import get_db
from models import Article
from schemas import ArticleCreate, ArticleUpdate, ArticleResponse
from auth import get_current_admin

router = APIRouter(prefix="/api/articles", tags=["articles"])


@router.get("", response_model=List[ArticleResponse])
def list_articles(
    categorie: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """Public endpoint – returns published articles, newest first."""
    q = db.query(Article).filter(Article.publie == True)  # noqa: E712
    if categorie:
        q = q.filter(Article.categorie == categorie)
    return q.order_by(Article.date_publication.desc()).all()


@router.get("/{article_id}", response_model=ArticleResponse)
def get_article(article_id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id, Article.publie == True).first()  # noqa: E712
    if not article:
        raise HTTPException(status_code=404, detail="Article introuvable")
    return article


@router.post("", response_model=ArticleResponse, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(get_current_admin)])
def create_article(body: ArticleCreate, db: Session = Depends(get_db)):
    article = Article(**body.model_dump())
    db.add(article)
    db.commit()
    db.refresh(article)
    return article


@router.put("/{article_id}", response_model=ArticleResponse,
            dependencies=[Depends(get_current_admin)])
def update_article(article_id: int, body: ArticleUpdate, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article introuvable")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(article, field, value)
    db.commit()
    db.refresh(article)
    return article


@router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(get_current_admin)])
def delete_article(article_id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article introuvable")
    db.delete(article)
    db.commit()
