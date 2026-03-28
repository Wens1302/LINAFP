# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


# ── Team schemas ─────────────────────────────────────────────────────────────

class TeamCreate(BaseModel):
    nom: str
    ville: str
    stade: str
    logo: Optional[str] = None


class TeamUpdate(BaseModel):
    nom: Optional[str] = None
    ville: Optional[str] = None
    stade: Optional[str] = None
    logo: Optional[str] = None


class TeamResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nom: str
    ville: str
    stade: str
    logo: Optional[str] = None


# ── Player schemas ────────────────────────────────────────────────────────────

class PlayerCreate(BaseModel):
    nom: str
    age: int
    nationalite: str
    poste: str
    numero: int
    goals: int = 0
    team_id: int


class PlayerUpdate(BaseModel):
    nom: Optional[str] = None
    age: Optional[int] = None
    nationalite: Optional[str] = None
    poste: Optional[str] = None
    numero: Optional[int] = None
    goals: Optional[int] = None
    team_id: Optional[int] = None


class PlayerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nom: str
    age: int
    nationalite: str
    poste: str
    numero: int
    goals: int
    team_id: int
    team: Optional[TeamResponse] = None


# ── Match schemas ─────────────────────────────────────────────────────────────

class MatchCreate(BaseModel):
    home_team_id: int
    away_team_id: int
    date: datetime
    stade: str
    home_score: int = 0
    away_score: int = 0


class MatchUpdate(BaseModel):
    home_team_id: Optional[int] = None
    away_team_id: Optional[int] = None
    date: Optional[datetime] = None
    stade: Optional[str] = None
    home_score: Optional[int] = None
    away_score: Optional[int] = None


class MatchResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    home_team_id: int
    away_team_id: int
    date: datetime
    stade: str
    home_score: int
    away_score: int
    home_team: Optional[TeamResponse] = None
    away_team: Optional[TeamResponse] = None


# ── Standings & Stats schemas ─────────────────────────────────────────────────

class StandingResponse(BaseModel):
    team_id: int
    team_name: str
    points: int
    played: int
    won: int
    drawn: int
    lost: int
    goals_for: int
    goals_against: int
    goal_difference: int


class TopScorer(BaseModel):
    player_id: int
    player_name: str
    team_name: str
    goals: int


class TeamGoals(BaseModel):
    team_id: int
    team_name: str
    goals_for: int
    goals_against: int


class StatsResponse(BaseModel):
    top_scorers: List[TopScorer]
    teams_goals: List[TeamGoals]
    standings: List[StandingResponse]


# ── Article schemas ───────────────────────────────────────────────────────────

class ArticleCreate(BaseModel):
    titre: str
    contenu: str
    image_url: Optional[str] = None
    categorie: str = "news"
    auteur: str = "Rédaction LINAFP"
    publie: bool = True


class ArticleUpdate(BaseModel):
    titre: Optional[str] = None
    contenu: Optional[str] = None
    image_url: Optional[str] = None
    categorie: Optional[str] = None
    auteur: Optional[str] = None
    publie: Optional[bool] = None


class ArticleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    titre: str
    contenu: str
    image_url: Optional[str] = None
    categorie: str
    date_publication: datetime
    auteur: str
    publie: bool


# ── Auth schemas ──────────────────────────────────────────────────────────────

class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
