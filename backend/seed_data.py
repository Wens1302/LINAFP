"""
seed_data.py – Populates the database with sample Gabonese football data.
Run with:  python seed_data.py
"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from datetime import datetime
from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)


TEAMS = [
    {"nom": "CF Mounana", "ville": "Mounana", "stade": "Stade de Mounana"},
    {"nom": "Mangasport", "ville": "Moanda", "stade": "Stade Municipal de Moanda"},
    {"nom": "AS Pelican", "ville": "Libreville", "stade": "Stade Omar Bongo"},
    {"nom": "Bouenguidi Sports", "ville": "Franceville", "stade": "Stade de Franceville"},
]

# 5 players per team (team index 0-based)
PLAYERS = [
    # CF Mounana (team index 0)
    {"nom": "Jean-Pierre Obame", "age": 27, "nationalite": "Gabonaise", "poste": "Gardien",    "numero": 1,  "goals": 0,  "team_idx": 0},
    {"nom": "Cédric Mouele",     "age": 24, "nationalite": "Gabonaise", "poste": "Défenseur",  "numero": 4,  "goals": 2,  "team_idx": 0},
    {"nom": "Hervé Nguema",      "age": 26, "nationalite": "Gabonaise", "poste": "Milieu",     "numero": 8,  "goals": 5,  "team_idx": 0},
    {"nom": "Patrick Biyogo",    "age": 22, "nationalite": "Gabonaise", "poste": "Attaquant",  "numero": 9,  "goals": 8,  "team_idx": 0},
    {"nom": "Thierry Mabika",    "age": 29, "nationalite": "Gabonaise", "poste": "Milieu",     "numero": 6,  "goals": 3,  "team_idx": 0},
    # Mangasport (team index 1)
    {"nom": "Serge Ondo",        "age": 25, "nationalite": "Gabonaise", "poste": "Gardien",    "numero": 1,  "goals": 0,  "team_idx": 1},
    {"nom": "Bruno Essono",      "age": 23, "nationalite": "Gabonaise", "poste": "Défenseur",  "numero": 3,  "goals": 1,  "team_idx": 1},
    {"nom": "Franck Nzigou",     "age": 28, "nationalite": "Gabonaise", "poste": "Milieu",     "numero": 7,  "goals": 6,  "team_idx": 1},
    {"nom": "Aubin Moussavou",   "age": 21, "nationalite": "Gabonaise", "poste": "Attaquant",  "numero": 11, "goals": 10, "team_idx": 1},
    {"nom": "Didier Mboula",     "age": 30, "nationalite": "Gabonaise", "poste": "Défenseur",  "numero": 5,  "goals": 0,  "team_idx": 1},
    # AS Pelican (team index 2)
    {"nom": "Gaël Ozouaki",      "age": 26, "nationalite": "Gabonaise", "poste": "Gardien",    "numero": 1,  "goals": 0,  "team_idx": 2},
    {"nom": "Stéphane Mba",      "age": 24, "nationalite": "Gabonaise", "poste": "Défenseur",  "numero": 2,  "goals": 1,  "team_idx": 2},
    {"nom": "Romaric Bibang",    "age": 27, "nationalite": "Gabonaise", "poste": "Milieu",     "numero": 10, "goals": 4,  "team_idx": 2},
    {"nom": "Christian Makanga", "age": 23, "nationalite": "Gabonaise", "poste": "Attaquant",  "numero": 9,  "goals": 7,  "team_idx": 2},
    {"nom": "Léon Nkoulou",      "age": 31, "nationalite": "Gabonaise", "poste": "Milieu",     "numero": 8,  "goals": 3,  "team_idx": 2},
    # Bouenguidi Sports (team index 3)
    {"nom": "Rémi Boundzanga",   "age": 28, "nationalite": "Gabonaise", "poste": "Gardien",    "numero": 1,  "goals": 0,  "team_idx": 3},
    {"nom": "Alexis Nzamba",     "age": 22, "nationalite": "Gabonaise", "poste": "Défenseur",  "numero": 4,  "goals": 2,  "team_idx": 3},
    {"nom": "Arnaud Ovono",      "age": 25, "nationalite": "Gabonaise", "poste": "Milieu",     "numero": 6,  "goals": 5,  "team_idx": 3},
    {"nom": "Guy-Roger Assoumou","age": 20, "nationalite": "Gabonaise", "poste": "Attaquant",  "numero": 11, "goals": 9,  "team_idx": 3},
    {"nom": "Martial Engone",    "age": 29, "nationalite": "Gabonaise", "poste": "Défenseur",  "numero": 3,  "goals": 0,  "team_idx": 3},
]

# Matches: (home_idx, away_idx, date_str, home_score, away_score)
MATCHES = [
    (0, 1, "2024-09-07 15:00:00", 2, 1),
    (2, 3, "2024-09-08 16:00:00", 0, 0),
    (1, 2, "2024-09-14 15:00:00", 3, 2),
    (3, 0, "2024-09-15 16:00:00", 1, 1),
    (0, 2, "2024-09-21 15:00:00", 2, 0),
]


def seed():
    db = SessionLocal()
    try:
        if db.query(models.Team).count() > 0:
            print("Database already seeded – skipping.")
            return

        # Insert teams
        db_teams = []
        for t in TEAMS:
            team = models.Team(**t)
            db.add(team)
            db_teams.append(team)
        db.flush()  # get team IDs

        # Insert players
        for p in PLAYERS:
            idx = p.pop("team_idx")
            player = models.Player(**p, team_id=db_teams[idx].id)
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
    except Exception as exc:
        db.rollback()
        print(f"Seeding failed: {exc}", file=sys.stderr)
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
