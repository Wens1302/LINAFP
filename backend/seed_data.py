# -*- coding: utf-8 -*-
"""
seed_data.py – Populates the database with sample Gabonese football data.

Run from inside the ``backend/`` directory::

    python seed_data.py

Prerequisites
-------------
* A ``.env`` file exists in the ``backend/`` directory (optional – SQLite is
  used by default so no PostgreSQL setup is required for development).

  **Important – file encoding on Windows**: If you use PostgreSQL and your
  ``DATABASE_URL`` password contains accented characters (é, è, ê…), save
  the ``.env`` file with **UTF-8** encoding (in Notepad: *File > Save As >
  Encoding: UTF-8*).  Saving in ANSI / CP1252 causes a ``UnicodeDecodeError``
  in psycopg2.  The database module automatically percent-encodes non-ASCII
  characters in the URL as a second line of defence.
"""
import sys
import os

# Make sure the backend/ directory is on sys.path so the local modules
# (database, models, auth) are importable when running as a plain script.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, date
from database import SessionLocal, engine
import models
from auth import hash_password

# Create all tables (idempotent).
models.Base.metadata.create_all(bind=engine)


COMPETITIONS = [
    {"nom": "Ligue 1 Gabon", "description": "Championnat national de première division du Gabon", "actif": True},
    {"nom": "Coupe du Gabon", "description": "Coupe nationale du Gabon", "actif": True},
]

SEASONS = [
    # (competition_idx, nom, date_debut, date_fin)
    (0, "2024-2025", date(2024, 8, 1), date(2025, 5, 31)),
]

TEAMS = [
    {"nom": "CF Mounana",       "ville": "Mounana",     "stade": "Stade de Mounana"},
    {"nom": "Mangasport",       "ville": "Moanda",      "stade": "Stade Municipal de Moanda"},
    {"nom": "AS Pelican",       "ville": "Libreville",  "stade": "Stade Omar Bongo"},
    {"nom": "Bouenguidi Sports","ville": "Franceville", "stade": "Stade de Franceville"},
]

# 5 players per team (team_idx is 0-based index into TEAMS)
PLAYERS = [
    # CF Mounana (team index 0)
    {"nom": "Jean-Pierre Obame",  "date_naissance": date(1997, 3, 15), "nationalite": "Gabonaise", "poste": "Gardien",   "numero": 1,  "goals": 0,  "team_idx": 0},
    {"nom": "Cédric Mouele",      "date_naissance": date(2000, 7, 22), "nationalite": "Gabonaise", "poste": "Défenseur", "numero": 4,  "goals": 2,  "team_idx": 0},
    {"nom": "Hervé Nguema",       "date_naissance": date(1998, 1, 10), "nationalite": "Gabonaise", "poste": "Milieu",    "numero": 8,  "goals": 5,  "team_idx": 0},
    {"nom": "Patrick Biyogo",     "date_naissance": date(2002, 9, 5),  "nationalite": "Gabonaise", "poste": "Attaquant", "numero": 9,  "goals": 8,  "team_idx": 0},
    {"nom": "Thierry Mabika",     "date_naissance": date(1995, 11, 30),"nationalite": "Gabonaise", "poste": "Milieu",    "numero": 6,  "goals": 3,  "team_idx": 0},
    # Mangasport (team index 1)
    {"nom": "Serge Ondo",         "date_naissance": date(1999, 4, 18), "nationalite": "Gabonaise", "poste": "Gardien",   "numero": 1,  "goals": 0,  "team_idx": 1},
    {"nom": "Bruno Essono",       "date_naissance": date(2001, 6, 12), "nationalite": "Gabonaise", "poste": "Défenseur", "numero": 3,  "goals": 1,  "team_idx": 1},
    {"nom": "Franck Nzigou",      "date_naissance": date(1996, 2, 28), "nationalite": "Gabonaise", "poste": "Milieu",    "numero": 7,  "goals": 6,  "team_idx": 1},
    {"nom": "Aubin Moussavou",    "date_naissance": date(2003, 8, 14), "nationalite": "Gabonaise", "poste": "Attaquant", "numero": 11, "goals": 10, "team_idx": 1},
    {"nom": "Didier Mboula",      "date_naissance": date(1994, 12, 3), "nationalite": "Gabonaise", "poste": "Défenseur", "numero": 5,  "goals": 0,  "team_idx": 1},
    # AS Pelican (team index 2)
    {"nom": "Gaël Ozouaki",       "date_naissance": date(1998, 5, 20), "nationalite": "Gabonaise", "poste": "Gardien",   "numero": 1,  "goals": 0,  "team_idx": 2},
    {"nom": "Stéphane Mba",       "date_naissance": date(2000, 10, 8), "nationalite": "Gabonaise", "poste": "Défenseur", "numero": 2,  "goals": 1,  "team_idx": 2},
    {"nom": "Romaric Bibang",     "date_naissance": date(1997, 7, 17), "nationalite": "Gabonaise", "poste": "Milieu",    "numero": 10, "goals": 4,  "team_idx": 2},
    {"nom": "Christian Makanga",  "date_naissance": date(2001, 3, 25), "nationalite": "Gabonaise", "poste": "Attaquant", "numero": 9,  "goals": 7,  "team_idx": 2},
    {"nom": "Léon Nkoulou",       "date_naissance": date(1993, 1, 14), "nationalite": "Gabonaise", "poste": "Milieu",    "numero": 8,  "goals": 3,  "team_idx": 2},
    # Bouenguidi Sports (team index 3)
    {"nom": "Rémi Boundzanga",    "date_naissance": date(1996, 9, 11), "nationalite": "Gabonaise", "poste": "Gardien",   "numero": 1,  "goals": 0,  "team_idx": 3},
    {"nom": "Alexis Nzamba",      "date_naissance": date(2002, 4, 6),  "nationalite": "Gabonaise", "poste": "Défenseur", "numero": 4,  "goals": 2,  "team_idx": 3},
    {"nom": "Arnaud Ovono",       "date_naissance": date(1999, 12, 19),"nationalite": "Gabonaise", "poste": "Milieu",    "numero": 6,  "goals": 5,  "team_idx": 3},
    {"nom": "Guy-Roger Assoumou", "date_naissance": date(2004, 2, 7),  "nationalite": "Gabonaise", "poste": "Attaquant", "numero": 11, "goals": 9,  "team_idx": 3},
    {"nom": "Martial Engone",     "date_naissance": date(1995, 8, 23), "nationalite": "Gabonaise", "poste": "Défenseur", "numero": 3,  "goals": 0,  "team_idx": 3},
]

# Matches: (home_idx, away_idx, season_idx, journee, date_str, home_score, away_score, status)
MATCHES = [
    (0, 1, 0, 1, "2024-09-07 15:00:00", 2, 1, models.MatchStatus.finished),
    (2, 3, 0, 1, "2024-09-08 16:00:00", 0, 0, models.MatchStatus.finished),
    (1, 2, 0, 2, "2024-09-14 15:00:00", 3, 2, models.MatchStatus.finished),
    (3, 0, 0, 2, "2024-09-15 16:00:00", 1, 1, models.MatchStatus.finished),
    (0, 2, 0, 3, "2024-09-21 15:00:00", 2, 0, models.MatchStatus.finished),
]

# Match events: (match_idx, type, minute, player_team_idx, player_in_squad_idx)
# player_in_squad_idx is the index in PLAYERS list for the relevant team
MATCH_EVENTS = [
    # Match 0: CF Mounana 2-1 Mangasport (J1)
    # Mounana goals: Patrick Biyogo (idx 3), Patrick Biyogo (idx 3)
    # Mangasport goal: Aubin Moussavou (idx 8)
    (0, models.MatchEventType.goal, 23, 3, None),   # Biyogo 23'
    (0, models.MatchEventType.goal, 67, 3, None),   # Biyogo 67'
    (0, models.MatchEventType.goal, 81, 8, None),   # Moussavou 81'
    # Match 2: Mangasport 3-2 AS Pelican (J2)
    (2, models.MatchEventType.goal, 12, 8, None),   # Moussavou 12'
    (2, models.MatchEventType.goal, 34, 7, None),   # Nzigou 34'
    (2, models.MatchEventType.goal, 55, 13, None),  # Makanga 55'
    (2, models.MatchEventType.goal, 72, 8, None),   # Moussavou 72'
    (2, models.MatchEventType.goal, 88, 13, None),  # Makanga 88'
    (2, models.MatchEventType.yellow_card, 45, 11, None),  # Mba yellow
    # Match 4: CF Mounana 2-0 AS Pelican (J3)
    (4, models.MatchEventType.goal, 30, 3, None),   # Biyogo 30'
    (4, models.MatchEventType.goal, 78, 2, None),   # Nguema 78'
]

ARTICLES = [
    {
        "titre": "CF Mounana remporte le derby gabonais face à Mangasport",
        "contenu": (
            "Dans un match électrique disputé au Stade de Mounana, CF Mounana s'est imposé 2-1 "
            "face à Mangasport. Patrick Biyogo a inscrit un doublé pour offrir la victoire à son "
            "équipe devant plus de 5 000 supporters. Ce succès conforte CF Mounana en tête du "
            "classement avec 7 points après trois journées."
        ),
        "image_url": "https://images.unsplash.com/photo-1574629810360-7efbbe195018?w=800&q=80",
        "categorie": "match",
        "auteur": "Rédaction LINAFP",
        "date_publication": datetime(2024, 9, 7, 18, 0),
    },
    {
        "titre": "Aubin Moussavou, meilleur buteur de la saison",
        "contenu": (
            "À seulement 21 ans, l'attaquant de Mangasport Aubin Moussavou s'impose comme le "
            "grand artisan offensif de la saison avec 10 buts en championnat. Convoité par "
            "plusieurs clubs du continent, le joueur a déclaré vouloir finir la saison à Moanda "
            "avant d'étudier d'éventuelles offres."
        ),
        "image_url": "https://images.unsplash.com/photo-1543326727-cf6c39e8f84c?w=800&q=80",
        "categorie": "news",
        "auteur": "Rédaction LINAFP",
        "date_publication": datetime(2024, 9, 16, 10, 0),
    },
    {
        "titre": "AS Pélican accueille Bouenguidi Sports à Omar Bongo",
        "contenu": (
            "La prochaine journée du championnat mettra aux prises AS Pélican et Bouenguidi "
            "Sports au mythique Stade Omar Bongo de Libreville. Un match crucial pour les deux "
            "équipes qui cherchent à remonter au classement. Coup d'envoi prévu à 16h00."
        ),
        "image_url": "https://images.unsplash.com/photo-1522778119026-d647f0596c20?w=800&q=80",
        "categorie": "match",
        "auteur": "Rédaction LINAFP",
        "date_publication": datetime(2024, 9, 18, 9, 30),
    },
    {
        "titre": "La LINAFP annonce la réforme du championnat national",
        "contenu": (
            "La Ligue Nationale de Football Professionnel (LINAFP) a annoncé une réforme "
            "majeure du championnat national à partir de la saison prochaine. Le nombre "
            "d'équipes participantes passera de 16 à 18, avec l'intégration de deux clubs "
            "des provinces. Une décision saluée par l'ensemble des acteurs du football gabonais."
        ),
        "image_url": "https://images.unsplash.com/photo-1431324155629-1a6deb1dec8d?w=800&q=80",
        "categorie": "news",
        "auteur": "Direction LINAFP",
        "date_publication": datetime(2024, 9, 20, 14, 0),
    },
    {
        "titre": "Transfert : Guy-Roger Assoumou prolonge à Bouenguidi Sports",
        "contenu": (
            "Malgré les rumeurs de départ, l'attaquant Guy-Roger Assoumou a paraphé un nouveau "
            "contrat de deux ans avec Bouenguidi Sports. Le joueur de 20 ans, auteur de 9 buts "
            "cette saison, a confirmé son attachement au club de Franceville lors d'une "
            "conférence de presse organisée ce vendredi."
        ),
        "image_url": "https://images.unsplash.com/photo-1579952363873-27f3bade9f55?w=800&q=80",
        "categorie": "transfert",
        "auteur": "Rédaction LINAFP",
        "date_publication": datetime(2024, 9, 22, 11, 0),
    },
]

# Default admin credentials – override via env vars in production
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin1234")

# Additional users for role demonstration
EXTRA_USERS = [
    {"username": "editor", "password": "editor1234", "role": models.UserRole.editor},
    {"username": "reader", "password": "reader1234", "role": models.UserRole.reader},
]


def seed():
    db = SessionLocal()
    try:
        # ── Competitions & Seasons ──────────────────────────────────────────
        if db.query(models.Competition).count() == 0:
            db_competitions = []
            for c in COMPETITIONS:
                comp = models.Competition(**c)
                db.add(comp)
                db_competitions.append(comp)
            db.flush()

            db_seasons = []
            for comp_idx, nom, date_debut, date_fin in SEASONS:
                season = models.Season(
                    competition_id=db_competitions[comp_idx].id,
                    nom=nom,
                    date_debut=date_debut,
                    date_fin=date_fin,
                )
                db.add(season)
                db_seasons.append(season)
            db.flush()
            print(f"Seeded: {len(COMPETITIONS)} competitions, {len(SEASONS)} seasons.")
        else:
            print("Competitions already seeded – skipping.")
            db_competitions = db.query(models.Competition).order_by(models.Competition.id).all()
            db_seasons = db.query(models.Season).order_by(models.Season.id).all()

        # ── Teams, Players, Matches ─────────────────────────────────────────
        if db.query(models.Team).count() > 0:
            print("Database already seeded – skipping teams/players/matches.")
            db_teams = db.query(models.Team).order_by(models.Team.id).all()
            db_players = db.query(models.Player).order_by(models.Player.id).all()
            db_matches = db.query(models.Match).order_by(models.Match.id).all()
        else:
            # Insert teams
            db_teams = []
            for t in TEAMS:
                team = models.Team(**t)
                db.add(team)
                db_teams.append(team)
            db.flush()

            # Insert players
            db_players = []
            for p in PLAYERS:
                player_data = {**p}
                team_idx = player_data.pop("team_idx")
                player = models.Player(**player_data, team_id=db_teams[team_idx].id)
                db.add(player)
                db_players.append(player)
            db.flush()

            # Insert matches
            db_matches = []
            for home_idx, away_idx, season_idx, journee, date_str, hs, as_, match_status in MATCHES:
                season_id = db_seasons[season_idx].id if db_seasons else None
                match = models.Match(
                    season_id=season_id,
                    home_team_id=db_teams[home_idx].id,
                    away_team_id=db_teams[away_idx].id,
                    date=datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S"),
                    stade=db_teams[home_idx].stade,
                    journee=journee,
                    status=match_status,
                    home_score=hs,
                    away_score=as_,
                )
                db.add(match)
                db_matches.append(match)
            db.flush()

            db.commit()
            print(f"Seeded: {len(TEAMS)} teams, {len(PLAYERS)} players, {len(MATCHES)} matches.")

        # ── Match Events ────────────────────────────────────────────────────
        if db.query(models.MatchEvent).count() == 0 and db_matches:
            for match_idx, event_type, minute, player_idx, player_in_idx in MATCH_EVENTS:
                if match_idx >= len(db_matches):
                    continue
                event = models.MatchEvent(
                    match_id=db_matches[match_idx].id,
                    type=event_type,
                    minute=minute,
                    player_id=db_players[player_idx].id if player_idx is not None else None,
                    player_in_id=db_players[player_in_idx].id if player_in_idx is not None else None,
                )
                db.add(event)
            db.commit()
            print(f"Seeded {len(MATCH_EVENTS)} match events.")
        else:
            print("Match events already seeded – skipping.")

        # ── Admin user ──────────────────────────────────────────────────────
        if db.query(models.AdminUser).count() == 0:
            admin = models.AdminUser(
                username=ADMIN_USERNAME,
                hashed_password=hash_password(ADMIN_PASSWORD),
                role=models.UserRole.admin,
            )
            db.add(admin)
            for u in EXTRA_USERS:
                user = models.AdminUser(
                    username=u["username"],
                    hashed_password=hash_password(u["password"]),
                    role=u["role"],
                )
                db.add(user)
            db.commit()
            print(f"Admin user created: {ADMIN_USERNAME} (change password in production!)")
            print("Extra users created: editor / reader")
        else:
            print("Admin user already exists – skipping.")

        # ── Articles ────────────────────────────────────────────────────────
        if db.query(models.Article).count() == 0:
            for a in ARTICLES:
                db.add(models.Article(**a))
            db.commit()
            print(f"Seeded {len(ARTICLES)} articles.")
        else:
            print("Articles already seeded – skipping.")

    except Exception as exc:
        db.rollback()
        print(f"Seeding failed: {exc}", file=sys.stderr)
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
