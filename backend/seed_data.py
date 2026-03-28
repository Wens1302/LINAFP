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

from datetime import datetime
from database import SessionLocal, engine
import models
from auth import hash_password

# Create all tables (idempotent).
models.Base.metadata.create_all(bind=engine)


TEAMS = [
    {"nom": "CF Mounana",       "ville": "Mounana",     "stade": "Stade de Mounana"},
    {"nom": "Mangasport",       "ville": "Moanda",      "stade": "Stade Municipal de Moanda"},
    {"nom": "AS Pelican",       "ville": "Libreville",  "stade": "Stade Omar Bongo"},
    {"nom": "Bouenguidi Sports","ville": "Franceville", "stade": "Stade de Franceville"},
]

# 5 players per team (team_idx is 0-based index into TEAMS)
PLAYERS = [
    # CF Mounana (team index 0)
    {"nom": "Jean-Pierre Obame",  "age": 27, "nationalite": "Gabonaise", "poste": "Gardien",   "numero": 1,  "goals": 0,  "team_idx": 0},
    {"nom": "Cédric Mouele",      "age": 24, "nationalite": "Gabonaise", "poste": "Défenseur", "numero": 4,  "goals": 2,  "team_idx": 0},
    {"nom": "Hervé Nguema",       "age": 26, "nationalite": "Gabonaise", "poste": "Milieu",    "numero": 8,  "goals": 5,  "team_idx": 0},
    {"nom": "Patrick Biyogo",     "age": 22, "nationalite": "Gabonaise", "poste": "Attaquant", "numero": 9,  "goals": 8,  "team_idx": 0},
    {"nom": "Thierry Mabika",     "age": 29, "nationalite": "Gabonaise", "poste": "Milieu",    "numero": 6,  "goals": 3,  "team_idx": 0},
    # Mangasport (team index 1)
    {"nom": "Serge Ondo",         "age": 25, "nationalite": "Gabonaise", "poste": "Gardien",   "numero": 1,  "goals": 0,  "team_idx": 1},
    {"nom": "Bruno Essono",       "age": 23, "nationalite": "Gabonaise", "poste": "Défenseur", "numero": 3,  "goals": 1,  "team_idx": 1},
    {"nom": "Franck Nzigou",      "age": 28, "nationalite": "Gabonaise", "poste": "Milieu",    "numero": 7,  "goals": 6,  "team_idx": 1},
    {"nom": "Aubin Moussavou",    "age": 21, "nationalite": "Gabonaise", "poste": "Attaquant", "numero": 11, "goals": 10, "team_idx": 1},
    {"nom": "Didier Mboula",      "age": 30, "nationalite": "Gabonaise", "poste": "Défenseur", "numero": 5,  "goals": 0,  "team_idx": 1},
    # AS Pelican (team index 2)
    {"nom": "Gaël Ozouaki",       "age": 26, "nationalite": "Gabonaise", "poste": "Gardien",   "numero": 1,  "goals": 0,  "team_idx": 2},
    {"nom": "Stéphane Mba",       "age": 24, "nationalite": "Gabonaise", "poste": "Défenseur", "numero": 2,  "goals": 1,  "team_idx": 2},
    {"nom": "Romaric Bibang",     "age": 27, "nationalite": "Gabonaise", "poste": "Milieu",    "numero": 10, "goals": 4,  "team_idx": 2},
    {"nom": "Christian Makanga",  "age": 23, "nationalite": "Gabonaise", "poste": "Attaquant", "numero": 9,  "goals": 7,  "team_idx": 2},
    {"nom": "Léon Nkoulou",       "age": 31, "nationalite": "Gabonaise", "poste": "Milieu",    "numero": 8,  "goals": 3,  "team_idx": 2},
    # Bouenguidi Sports (team index 3)
    {"nom": "Rémi Boundzanga",    "age": 28, "nationalite": "Gabonaise", "poste": "Gardien",   "numero": 1,  "goals": 0,  "team_idx": 3},
    {"nom": "Alexis Nzamba",      "age": 22, "nationalite": "Gabonaise", "poste": "Défenseur", "numero": 4,  "goals": 2,  "team_idx": 3},
    {"nom": "Arnaud Ovono",       "age": 25, "nationalite": "Gabonaise", "poste": "Milieu",    "numero": 6,  "goals": 5,  "team_idx": 3},
    {"nom": "Guy-Roger Assoumou", "age": 20, "nationalite": "Gabonaise", "poste": "Attaquant", "numero": 11, "goals": 9,  "team_idx": 3},
    {"nom": "Martial Engone",     "age": 29, "nationalite": "Gabonaise", "poste": "Défenseur", "numero": 3,  "goals": 0,  "team_idx": 3},
]

# Matches: (home_idx, away_idx, date_str, home_score, away_score)
MATCHES = [
    (0, 1, "2024-09-07 15:00:00", 2, 1),
    (2, 3, "2024-09-08 16:00:00", 0, 0),
    (1, 2, "2024-09-14 15:00:00", 3, 2),
    (3, 0, "2024-09-15 16:00:00", 1, 1),
    (0, 2, "2024-09-21 15:00:00", 2, 0),
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


def seed():
    db = SessionLocal()
    try:
        if db.query(models.Team).count() > 0:
            print("Database already seeded – skipping teams/players/matches.")
        else:
            # Insert teams
            db_teams = []
            for t in TEAMS:
                team = models.Team(**t)
                db.add(team)
                db_teams.append(team)
            db.flush()  # get team IDs

            # Insert players
            for p in PLAYERS:
                player_data = {**p}
                team_idx = player_data.pop("team_idx")
                player = models.Player(**player_data, team_id=db_teams[team_idx].id)
                db.add(player)
            db.flush()

            # Insert matches
            for home_idx, away_idx, date_str, hs, as_ in MATCHES:
                match = models.Match(
                    home_team_id=db_teams[home_idx].id,
                    away_team_id=db_teams[away_idx].id,
                    date=datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S"),
                    stade=db_teams[home_idx].stade,
                    home_score=hs,
                    away_score=as_,
                )
                db.add(match)

            db.commit()
            print(f"Seeded: {len(TEAMS)} teams, {len(PLAYERS)} players, {len(MATCHES)} matches.")

        # Seed admin user
        if db.query(models.AdminUser).count() == 0:
            admin = models.AdminUser(
                username=ADMIN_USERNAME,
                hashed_password=hash_password(ADMIN_PASSWORD),
            )
            db.add(admin)
            db.commit()
            print(f"Admin user created: {ADMIN_USERNAME} (change password in production!)")
        else:
            print("Admin user already exists – skipping.")

        # Seed articles
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
