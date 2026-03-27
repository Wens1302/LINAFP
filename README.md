# GabonFootStats

Application web de gestion et d'analyse des statistiques du championnat national de football du Gabon.

## Fonctionnalités

- 🏟️ **Gestion des équipes** – Ajouter, modifier, supprimer et afficher les équipes
- 👤 **Gestion des joueurs** – CRUD complet avec filtrage par équipe
- ⚽ **Gestion des matchs** – Créer, enregistrer les scores, suivre les résultats
- 📊 **Classement automatique** – Points, V/N/D, buts, différence de buts
- 📈 **Statistiques** – Meilleurs buteurs, buts par équipe
- 📉 **Dashboard** – Graphiques interactifs (Chart.js)

## Stack Technique

| Composant | Technologie |
|-----------|-------------|
| Frontend  | React 18 + Vite 6 + Chart.js |
| Backend   | Python 3.11+ + FastAPI |
| ORM       | SQLAlchemy 2 |
| Base de données | PostgreSQL (SQLite en dev) |

## Structure du projet

```
LINAFP/
├── backend/
│   ├── main.py          # Application FastAPI
│   ├── models.py        # Modèles SQLAlchemy (Team, Player, Match)
│   ├── schemas.py       # Schémas Pydantic
│   ├── database.py      # Connexion base de données
│   ├── seed_data.py     # Données exemples
│   ├── requirements.txt
│   └── routers/
│       ├── teams.py     # CRUD /api/teams
│       ├── players.py   # CRUD /api/players
│       ├── matches.py   # CRUD /api/matches
│       ├── standings.py # GET  /api/standings
│       └── stats.py     # GET  /api/stats
└── frontend/
    └── src/
        ├── pages/       # Dashboard, Teams, Players, Matches, Standings, Stats
        ├── components/  # Navbar
        └── services/    # api.js (Axios)
```

## API Endpoints

| Méthode | Route | Description |
|---------|-------|-------------|
| GET/POST | `/api/teams` | Liste / Créer équipe |
| GET/PUT/DELETE | `/api/teams/{id}` | Lire / Modifier / Supprimer |
| GET/POST | `/api/players` | Liste (filtre `?team_id=`) / Créer joueur |
| GET/PUT/DELETE | `/api/players/{id}` | Lire / Modifier / Supprimer |
| GET/POST | `/api/matches` | Liste / Créer match |
| GET/PUT/DELETE | `/api/matches/{id}` | Lire / Modifier / Supprimer |
| GET | `/api/standings` | Classement calculé automatiquement |
| GET | `/api/stats` | Statistiques (buteurs, buts par équipe) |
| GET | `/api/health` | Santé du service |

## Lancer le projet

### Prérequis

- Python 3.11+
- Node.js 18+
- (Optionnel) PostgreSQL

### Backend

```bash
cd backend

# Installer les dépendances
pip install -r requirements.txt

# (Optionnel) Configurer PostgreSQL
export DATABASE_URL="postgresql://user:password@localhost/gabonfootstats"

# Lancer le serveur (utilise SQLite par défaut)
uvicorn main:app --reload --port 8000

# Charger les données exemples (4 équipes, 20 joueurs, 5 matchs)
python seed_data.py
```

Le backend sera disponible sur : http://localhost:8000  
Documentation Swagger : http://localhost:8000/docs

### Frontend

```bash
cd frontend

# Installer les dépendances
npm install

# Lancer le serveur de développement
npm run dev
```

L'application sera disponible sur : http://localhost:3000

### Build de production

```bash
cd frontend
npm run build
```

## Données exemples

Le script `seed_data.py` insère :

**4 équipes gabonaises :**
- CF Mounana (Mounana – Stade de Mounana)
- Mangasport (Moanda – Stade Municipal de Moanda)
- AS Pélican (Libreville – Stade Omar Bongo)
- Bouenguidi Sports (Franceville – Stade de Franceville)

**20 joueurs** (5 par équipe) avec postes, nationalités et statistiques de buts

**5 matchs** avec scores

## Règles du classement

- Victoire = **3 points**
- Match nul = **1 point**
- Défaite = **0 point**

Tri : Points → Différence de buts → Buts marqués
