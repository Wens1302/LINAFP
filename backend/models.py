# -*- coding: utf-8 -*-
from datetime import datetime, timezone
from sqlalchemy import (
    Column, Integer, String, DateTime, ForeignKey, Text, Boolean, Date, Enum
)
import enum
from sqlalchemy.orm import relationship
from database import Base


# ── Enumerations ──────────────────────────────────────────────────────────────

class MatchStatus(str, enum.Enum):
    scheduled = "scheduled"
    in_progress = "in_progress"
    finished = "finished"
    postponed = "postponed"
    cancelled = "cancelled"


class MatchEventType(str, enum.Enum):
    goal = "goal"
    yellow_card = "yellow_card"
    red_card = "red_card"
    substitution = "substitution"


class PlayerStatus(str, enum.Enum):
    active = "active"
    injured = "injured"
    suspended = "suspended"


class UserRole(str, enum.Enum):
    admin = "admin"
    editor = "editor"
    reader = "reader"


# ── Competition ───────────────────────────────────────────────────────────────

class Competition(Base):
    __tablename__ = "competitions"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    actif = Column(Boolean, nullable=False, default=True)

    seasons = relationship("Season", back_populates="competition", cascade="all, delete-orphan")


# ── Season ────────────────────────────────────────────────────────────────────

class Season(Base):
    __tablename__ = "seasons"

    id = Column(Integer, primary_key=True, index=True)
    competition_id = Column(Integer, ForeignKey("competitions.id"), nullable=False)
    nom = Column(String, nullable=False)       # e.g. "2025-2026"
    date_debut = Column(Date, nullable=True)
    date_fin = Column(Date, nullable=True)
    archivee = Column(Boolean, nullable=False, default=False)

    competition = relationship("Competition", back_populates="seasons")
    matches = relationship("Match", back_populates="season")
    memberships = relationship("SquadMembership", back_populates="season")


# ── Team ──────────────────────────────────────────────────────────────────────

class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False)
    ville = Column(String, nullable=False)
    stade = Column(String, nullable=False)
    logo = Column(String, nullable=True)

    players = relationship("Player", back_populates="team", cascade="all, delete-orphan")
    home_matches = relationship("Match", foreign_keys="Match.home_team_id", back_populates="home_team")
    away_matches = relationship("Match", foreign_keys="Match.away_team_id", back_populates="away_team")
    memberships = relationship("SquadMembership", back_populates="team")


# ── Player ────────────────────────────────────────────────────────────────────

class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False)
    date_naissance = Column(Date, nullable=True)
    age = Column(Integer, nullable=True)          # kept for backward compat
    nationalite = Column(String, nullable=False)
    poste = Column(String, nullable=False)
    numero = Column(Integer, nullable=False)
    goals = Column(Integer, default=0, nullable=False)
    statut = Column(Enum(PlayerStatus), nullable=False, default=PlayerStatus.active)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)

    team = relationship("Team", back_populates="players")
    memberships = relationship("SquadMembership", back_populates="player")
    match_events = relationship("MatchEvent", foreign_keys="MatchEvent.player_id", back_populates="player")
    substitution_events = relationship("MatchEvent", foreign_keys="MatchEvent.player_in_id", back_populates="player_in")


# ── SquadMembership ───────────────────────────────────────────────────────────

class SquadMembership(Base):
    """Links a player to a team for a given season with optional dates."""
    __tablename__ = "squad_memberships"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    season_id = Column(Integer, ForeignKey("seasons.id"), nullable=False)
    date_debut = Column(Date, nullable=True)
    date_fin = Column(Date, nullable=True)
    pret = Column(Boolean, nullable=False, default=False)   # loan
    numero = Column(Integer, nullable=True)

    player = relationship("Player", back_populates="memberships")
    team = relationship("Team", back_populates="memberships")
    season = relationship("Season", back_populates="memberships")


# ── Match ─────────────────────────────────────────────────────────────────────

class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    season_id = Column(Integer, ForeignKey("seasons.id"), nullable=True)
    home_team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    away_team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    date = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    stade = Column(String, nullable=False)
    journee = Column(Integer, nullable=True)          # round number
    status = Column(Enum(MatchStatus), nullable=False, default=MatchStatus.scheduled)
    home_score = Column(Integer, default=0, nullable=False)
    away_score = Column(Integer, default=0, nullable=False)
    home_score_mi_temps = Column(Integer, nullable=True)
    away_score_mi_temps = Column(Integer, nullable=True)
    locked = Column(Boolean, nullable=False, default=False)

    season = relationship("Season", back_populates="matches")
    home_team = relationship("Team", foreign_keys=[home_team_id], back_populates="home_matches")
    away_team = relationship("Team", foreign_keys=[away_team_id], back_populates="away_matches")
    events = relationship("MatchEvent", back_populates="match", cascade="all, delete-orphan")


# ── MatchEvent ────────────────────────────────────────────────────────────────

class MatchEvent(Base):
    __tablename__ = "match_events"

    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(Integer, ForeignKey("matches.id"), nullable=False)
    type = Column(Enum(MatchEventType), nullable=False)
    minute = Column(Integer, nullable=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=True)
    player_in_id = Column(Integer, ForeignKey("players.id"), nullable=True)  # for substitutions
    assister_id = Column(Integer, ForeignKey("players.id"), nullable=True)   # for goals

    match = relationship("Match", back_populates="events")
    player = relationship("Player", foreign_keys=[player_id], back_populates="match_events")
    player_in = relationship("Player", foreign_keys=[player_in_id], back_populates="substitution_events")
    assister = relationship("Player", foreign_keys=[assister_id])


# ── Article ───────────────────────────────────────────────────────────────────

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    titre = Column(String, nullable=False)
    contenu = Column(Text, nullable=False)
    image_url = Column(String, nullable=True)
    categorie = Column(String, nullable=False, default="news")  # news | match | transfert
    date_publication = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    auteur = Column(String, nullable=False, default="Rédaction LINAFP")
    publie = Column(Boolean, nullable=False, default=True)


# ── AdminUser ─────────────────────────────────────────────────────────────────

class AdminUser(Base):
    __tablename__ = "admin_users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.admin)
