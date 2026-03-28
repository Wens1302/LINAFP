# GabonFootStats

Application web de gestion et d'analyse des statistiques du championnat national de football du Gabon.

## Fonctionnalités

- 🏟️ **Gestion des équipes** – Ajouter, modifier, supprimer et afficher les équipes
- 👤 **Gestion des joueurs** – CRUD complet avec filtrage par équipe
- ⚽ **Gestion des matchs** – Créer, enregistrer les scores, suivre les résultats
- 📊 **Classement automatique** – Points, V/N/D, buts, différence de buts
- 📈 **Statistiques** – Meilleurs buteurs, buts par équipe
- 📰 **Articles** – Actualités du championnat (news, match, transfert)

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
│   ├── models.py        # Modèles SQLAlchemy (Team, Player, Match, Article, AdminUser)
│   ├── schemas.py       # Schémas Pydantic
│   ├── database.py      # Connexion base de données
│   ├── auth.py          # JWT + hachage des mots de passe
│   ├── seed_data.py     # Données exemples gabonaises
│   ├── requirements.txt
│   └── routers/
│       ├── teams.py     # CRUD /api/teams
│       ├── players.py   # CRUD /api/players
│       ├── matches.py   # CRUD /api/matches
│       ├── standings.py # GET  /api/standings
│       ├── stats.py     # GET  /api/stats
│       ├── articles.py  # CRUD /api/articles
│       └── auth.py      # POST /api/auth/login
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
| GET/POST | `/api/articles` | Articles publiés / Créer (admin) |
| GET/PUT/DELETE | `/api/articles/{id}` | Lire / Modifier / Supprimer (admin) |
| POST | `/api/auth/login` | Connexion admin (renvoie un JWT) |
| GET | `/api/health` | Santé du service |

## Lancer le projet

### Prérequis

- Python 3.11+
- Node.js 18+
- (Optionnel) PostgreSQL

---

### 🐍 Lancer avec Anaconda (recommandé)

> Ces étapes supposent qu'**Anaconda** (ou **Miniconda**) est installé et que
> la commande `conda` est disponible dans votre terminal.  
> Sur Windows, utilisez le **Anaconda Prompt** ou **Anaconda PowerShell Prompt**.

#### Étape 1 – Cloner le dépôt (si ce n'est pas encore fait)

```bash
git clone https://github.com/Wens1302/LINAFP.git
cd LINAFP
```

#### Étape 2 – Créer l'environnement Conda

Un fichier `environment.yml` prêt à l'emploi se trouve dans le dossier `backend/`.
Il installe Python 3.11 et toutes les dépendances Python du projet.

```bash
conda env create -f backend/environment.yml
```

> La première création peut prendre quelques minutes.

#### Étape 3 – Activer l'environnement

```bash
conda activate linafp
```

> Vous devriez voir `(linafp)` apparaître au début de votre invite de commandes.

#### Étape 4 – Configurer la base de données

**Option A – SQLite (aucune installation requise, parfait pour débuter)**

Aucune configuration supplémentaire n'est nécessaire. Le fichier
`gabonfootstats.db` sera créé automatiquement dans `backend/`.

**Option B – PostgreSQL**

```bash
# Copier le fichier de configuration
cp backend/.env.example backend/.env
```

Ouvrez `backend/.env` et renseignez vos informations PostgreSQL :

```env
DATABASE_URL=postgresql://postgres:VotreMotDePasse@localhost:5432/gabonfootstats
```

> ⚠️ **Encodage** : Enregistrez le fichier `.env` en **UTF-8**.  
> Si votre mot de passe contient des caractères spéciaux, encodez-le :
> ```bash
> python -c "from urllib.parse import quote; print(quote('VotreMotDePasse', safe=''))"
> ```

Créez ensuite la base de données PostgreSQL :

```bash
# Se connecter à PostgreSQL et créer la base
psql -U postgres -c "CREATE DATABASE gabonfootstats;"
```

#### Étape 5 – Initialiser la base de données et charger les données

```bash
cd backend

# Créer les tables dans la base de données
python -c "from database import engine; import models; models.Base.metadata.create_all(bind=engine)"

# Charger les données exemples (4 équipes, 20 joueurs, 5 matchs, 5 articles)
python seed_data.py
```

#### Étape 6 – Lancer le serveur backend

```bash
# Depuis le dossier backend/
uvicorn main:app --reload --port 8000
```

Le backend est disponible sur : **http://localhost:8000**  
Documentation Swagger interactive : **http://localhost:8000/docs**

#### Étape 7 – Lancer le frontend (si disponible)

```bash
# Depuis la racine du projet
cd frontend

# Installer les dépendances Node.js
npm install

# Lancer le serveur de développement
npm run dev
```

L'application sera disponible sur : **http://localhost:3000**

---

#### Résumé – commandes rapides (après la première installation)

```bash
# 1. Activer l'environnement
conda activate linafp

# 2. Lancer le backend
cd backend
uvicorn main:app --reload --port 8000

# 3. (Autre terminal) Lancer le frontend
cd frontend
npm run dev
```

#### Mettre à jour l'environnement Conda

Si le fichier `environment.yml` a été modifié après la création initiale :

```bash
conda env update -f backend/environment.yml --prune
```

#### Supprimer l'environnement Conda

```bash
conda deactivate
conda env remove -n linafp
```

---

### Backend (sans Anaconda)

```bash
cd backend

# Installer les dépendances
pip install -r requirements.txt

# (Optionnel) Configurer PostgreSQL
cp .env.example .env
# Éditer .env et renseigner DATABASE_URL

# Lancer le serveur (utilise SQLite par défaut)
uvicorn main:app --reload --port 8000

# Charger les données exemples (4 équipes, 20 joueurs, 5 matchs, 5 articles)
python seed_data.py
```

Le backend sera disponible sur : http://localhost:8000  
Documentation Swagger : http://localhost:8000/docs

> **Important – encodage sur Windows** : Si vous utilisez PostgreSQL et que
> votre mot de passe contient des caractères accentués (é, è…), enregistrez
> le fichier `.env` en **UTF-8** (dans Notepad : *Fichier > Enregistrer sous >
> Encodage : UTF-8*). Un encodage ANSI / CP1252 provoque une
> `UnicodeDecodeError` dans psycopg2. Le module `database.py` applique
> automatiquement un percent-encodage comme deuxième protection.

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

**5 articles** (actualités, matchs, transferts)

**1 utilisateur admin** (login : `admin` / mot de passe : `admin1234` — à changer en production)

## Règles du classement

- Victoire = **3 points**
- Match nul = **1 point**
- Défaite = **0 point**

Tri : Points → Différence de buts → Buts marqués
