# -*- coding: utf-8 -*-
from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel, ConfigDict

from models import MatchStatus, MatchEventType, PlayerStatus, UserRole


# ── Competition schemas ───────────────────────────────────────────────────────

class CompetitionCreate(BaseModel):
    nom: str
    description: Optional[str] = None
    actif: bool = True


class CompetitionUpdate(BaseModel):
    nom: Optional[str] = None
    description: Optional[str] = None
    actif: Optional[bool] = None


class CompetitionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nom: str
    description: Optional[str] = None
    actif: bool


# ── Season schemas ────────────────────────────────────────────────────────────

class SeasonCreate(BaseModel):
    competition_id: int
    nom: str
    date_debut: Optional[date] = None
    date_fin: Optional[date] = None
    archivee: bool = False


class SeasonUpdate(BaseModel):
    nom: Optional[str] = None
    date_debut: Optional[date] = None
    date_fin: Optional[date] = None
    archivee: Optional[bool] = None


class SeasonResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    competition_id: int
    nom: str
    date_debut: Optional[date] = None
    date_fin: Optional[date] = None
    archivee: bool
    competition: Optional[CompetitionResponse] = None


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
    date_naissance: Optional[date] = None
    age: Optional[int] = None
    nationalite: str
    poste: str
    numero: int
    goals: int = 0
    statut: PlayerStatus = PlayerStatus.active
    team_id: int


class PlayerUpdate(BaseModel):
    nom: Optional[str] = None
    date_naissance: Optional[date] = None
    age: Optional[int] = None
    nationalite: Optional[str] = None
    poste: Optional[str] = None
    numero: Optional[int] = None
    goals: Optional[int] = None
    statut: Optional[PlayerStatus] = None
    team_id: Optional[int] = None


class PlayerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nom: str
    date_naissance: Optional[date] = None
    age: Optional[int] = None
    nationalite: str
    poste: str
    numero: int
    goals: int
    statut: PlayerStatus
    team_id: int
    team: Optional[TeamResponse] = None


# ── SquadMembership schemas ───────────────────────────────────────────────────

class SquadMembershipCreate(BaseModel):
    player_id: int
    team_id: int
    season_id: int
    date_debut: Optional[date] = None
    date_fin: Optional[date] = None
    pret: bool = False
    numero: Optional[int] = None


class SquadMembershipUpdate(BaseModel):
    date_debut: Optional[date] = None
    date_fin: Optional[date] = None
    pret: Optional[bool] = None
    numero: Optional[int] = None


class SquadMembershipResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    player_id: int
    team_id: int
    season_id: int
    date_debut: Optional[date] = None
    date_fin: Optional[date] = None
    pret: bool
    numero: Optional[int] = None
    player: Optional[PlayerResponse] = None
    team: Optional[TeamResponse] = None


# ── Match schemas ─────────────────────────────────────────────────────────────

class MatchCreate(BaseModel):
    season_id: Optional[int] = None
    home_team_id: int
    away_team_id: int
    date: datetime
    stade: str
    journee: Optional[int] = None
    status: MatchStatus = MatchStatus.scheduled
    home_score: int = 0
    away_score: int = 0
    home_score_mi_temps: Optional[int] = None
    away_score_mi_temps: Optional[int] = None


class MatchUpdate(BaseModel):
    season_id: Optional[int] = None
    home_team_id: Optional[int] = None
    away_team_id: Optional[int] = None
    date: Optional[datetime] = None
    stade: Optional[str] = None
    journee: Optional[int] = None
    status: Optional[MatchStatus] = None
    home_score: Optional[int] = None
    away_score: Optional[int] = None
    home_score_mi_temps: Optional[int] = None
    away_score_mi_temps: Optional[int] = None
    locked: Optional[bool] = None


class MatchResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    season_id: Optional[int] = None
    home_team_id: int
    away_team_id: int
    date: datetime
    stade: str
    journee: Optional[int] = None
    status: MatchStatus
    home_score: int
    away_score: int
    home_score_mi_temps: Optional[int] = None
    away_score_mi_temps: Optional[int] = None
    locked: bool
    home_team: Optional[TeamResponse] = None
    away_team: Optional[TeamResponse] = None


# ── MatchEvent schemas ────────────────────────────────────────────────────────

class MatchEventCreate(BaseModel):
    type: MatchEventType
    minute: Optional[int] = None
    player_id: Optional[int] = None
    player_in_id: Optional[int] = None
    assister_id: Optional[int] = None


class MatchEventUpdate(BaseModel):
    minute: Optional[int] = None
    player_id: Optional[int] = None
    player_in_id: Optional[int] = None
    assister_id: Optional[int] = None


class MatchEventResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    match_id: int
    type: MatchEventType
    minute: Optional[int] = None
    player_id: Optional[int] = None
    player_in_id: Optional[int] = None
    assister_id: Optional[int] = None
    player: Optional[PlayerResponse] = None


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
    role: UserRole
