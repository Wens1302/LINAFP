# 📖 Guide GabonFootStats — Technologies, Architecture et Ajout de Vraies Données

> **Ce guide est entièrement en français.** Il explique comment le projet fonctionne, quelles technologies il utilise, et surtout comment remplacer les données de test par de vraies données.

---

## 🔑 Identifiants administrateur

| Identifiant | Mot de passe |
|-------------|--------------|
| `admin`     | `admin1234`  |

> ⚠️ **En production**, changez impérativement ces identifiants (voir section [Sécurité en production](#-sécurité-en-production)).

---

## 🗂️ Table des matières

1. [Vue d'ensemble du projet](#-vue-densemble-du-projet)
2. [Technologies utilisées](#-technologies-utilisées)
3. [Architecture — comment ça marche](#️-architecture--comment-ça-marche)
4. [Lancer le projet en local](#-lancer-le-projet-en-local)
5. [Comment mettre de vraies données](#-comment-mettre-de-vraies-données)
   - [Méthode 1 — Interface d'administration (recommandée)](#méthode-1--interface-dadministration-recommandée)
   - [Méthode 2 — Modifier le script `seed_data.py`](#méthode-2--modifier-le-script-seed_datapy)
   - [Méthode 3 — API REST directement (curl / Postman)](#méthode-3--api-rest-directement-curl--postman)
6. [Référence complète des données](#-référence-complète-des-données)
7. [Passer à PostgreSQL](#-passer-à-postgresql)
8. [Sécurité en production](#-sécurité-en-production)
9. [FAQ](#-faq)

---

## 🌍 Vue d'ensemble du projet

**GabonFootStats** est le site officiel de la LINAFP (Ligue Nationale de Football Professionnel du Gabon). Il offre :

- 🏠 **Page d'accueil publique** — actualités, classement rapide, prochains matchs, meilleurs buteurs
- 🛡️ **Clubs** — fiche de chaque équipe (logo, ville, stade, stats)
- 👟 **Joueurs** — classement des buteurs + liste complète par poste / équipe
- ⚽ **Résultats & Calendrier** — tous les matchs joués et à venir
- 🏆 **Classement** — tableau complet avec guide de forme (5 derniers matchs)
- 📈 **Statistiques** — buts marqués, buts encaissés, victoires par équipe
- 🔒 **Espace administrateur** — gestion complète (équipes, joueurs, matchs, articles) accessible après connexion

---

## 🧰 Technologies utilisées

### Frontend (interface utilisateur)

| Technologie | Rôle | Version |
|-------------|------|---------|
| **React 18** | Bibliothèque JavaScript pour construire l'interface | 18.3 |
| **Vite 6** | Outil de build ultra-rapide (remplace Webpack) | 6.4 |
| **React Router v6** | Navigation entre les pages (SPA — Single Page App) | 6.23 |
| **Axios** | Appels HTTP vers le backend (équivalent de `fetch` mais plus pratique) | 1.7 |
| **Chart.js + react-chartjs-2** | Graphiques interactifs (dashboard admin) | 4.4 / 5.2 |

**Comment le frontend fonctionne :**  
C'est une **Single Page Application** — une seule page HTML est chargée, et React met à jour l'affichage sans rechargement. Toutes les données viennent du backend via des requêtes HTTP (`GET`, `POST`, `PUT`, `DELETE`).

---

### Backend (serveur / API)

| Technologie | Rôle | Version |
|-------------|------|---------|
| **Python 3.11+** | Langage du serveur | 3.11+ |
| **FastAPI** | Framework web moderne, génère automatiquement la doc Swagger | 0.111 |
| **SQLAlchemy 2** | ORM (Object-Relational Mapper) — traduit le Python en SQL | 2.0 |
| **Pydantic v2** | Validation des données entrant dans l'API | 2.7 |
| **Uvicorn** | Serveur ASGI qui exécute l'application FastAPI | 0.29 |
| **python-jose + passlib** | Authentification JWT + hachage bcrypt des mots de passe | — |
| **python-dotenv** | Lecture des variables d'environnement depuis un fichier `.env` | 1.0 |

---

### Base de données

| Environnement | Base de données | Configuration |
|---------------|-----------------|---------------|
| **Développement** | SQLite | Fichier local `backend/gabonfootstats.db` — aucune installation requise |
| **Production** | PostgreSQL | Variable d'environnement `DATABASE_URL` |

**SQLite** est parfait pour démarrer : il crée automatiquement un fichier `.db` sur votre disque, sans serveur à installer.  
**PostgreSQL** est recommandé en production pour la fiabilité et les performances.

---

### Authentification

Le système utilise **JWT (JSON Web Tokens)** :

1. L'admin envoie son identifiant + mot de passe au backend (`POST /api/auth/login`)
2. Le backend vérifie le mot de passe (bcrypt) et renvoie un **token JWT** signé (valable 8 heures)
3. Le frontend stocke ce token dans `localStorage` et l'envoie dans l'en-tête `Authorization: Bearer <token>` à chaque requête sensible
4. Le backend vérifie la signature du token avant d'autoriser les opérations d'écriture

---

## 🏗️ Architecture — comment ça marche

```
Navigateur (React / Vite)
        │
        │  HTTP/JSON  (ex: GET /api/standings)
        ▼
  Backend FastAPI  ──►  SQLAlchemy ORM  ──►  Base de données
  (port 8000)                                 SQLite / PostgreSQL
        │
        │  (proxy Vite en dev)
        ▲
        │  Réponse JSON
```

### Flux de données — exemple « afficher le classement »

1. L'utilisateur ouvre `/classement` dans son navigateur
2. React appelle `GET /api/standings` via Axios
3. FastAPI reçoit la requête, calcule le classement à partir des matchs (via SQLAlchemy)
4. La réponse JSON est renvoyée au frontend
5. React met à jour l'affichage

### Structure des fichiers

```
LINAFP/
├── GUIDE.md                ← ce fichier
├── README.md
├── backend/
│   ├── main.py             ← point d'entrée FastAPI, CORS, inclusion des routers
│   ├── models.py           ← définition des tables (Team, Player, Match, Article, AdminUser)
│   ├── schemas.py          ← validation Pydantic (entrées/sorties API)
│   ├── database.py         ← connexion SQLAlchemy (SQLite par défaut)
│   ├── auth.py             ← JWT + bcrypt
│   ├── seed_data.py        ← données de démarrage (à modifier pour de vraies données)
│   ├── requirements.txt
│   └── routers/
│       ├── auth.py         ← POST /api/auth/login
│       ├── articles.py     ← CRUD /api/articles
│       ├── teams.py        ← CRUD /api/teams
│       ├── players.py      ← CRUD /api/players
│       ├── matches.py      ← CRUD /api/matches
│       ├── standings.py    ← GET  /api/standings (calculé depuis les matchs)
│       └── stats.py        ← GET  /api/stats
└── frontend/
    ├── index.html
    ├── vite.config.js
    └── src/
        ├── App.jsx          ← routage principal
        ├── index.css        ← styles globaux
        ├── main.jsx
        ├── components/
        │   ├── Navbar.jsx   ← navigation (publique vs admin)
        │   ├── Footer.jsx
        │   ├── ScoresTicker.jsx  ← bandeau défilant des scores
        │   └── ProtectedRoute.jsx
        ├── context/
        │   └── AuthContext.jsx   ← gestion état connexion admin
        ├── pages/
        │   ├── Home.jsx         ← accueil public
        │   ├── Clubs.jsx        ← /clubs
        │   ├── Joueurs.jsx      ← /joueurs
        │   ├── Resultats.jsx    ← /resultats
        │   ├── Standings.jsx    ← /classement
        │   ├── Statistiques.jsx ← /statistiques
        │   ├── Login.jsx        ← /login (admin)
        │   ├── Dashboard.jsx    ← /admin/dashboard
        │   ├── Teams.jsx        ← /admin/teams
        │   ├── Players.jsx      ← /admin/players
        │   ├── Matches.jsx      ← /admin/matches
        │   ├── Stats.jsx        ← /admin/stats
        │   └── Articles.jsx     ← /admin/articles
        └── services/
            └── api.js           ← toutes les fonctions d'appel API (Axios)
```

---

## 🚀 Lancer le projet en local

### Prérequis

- **Python 3.11+** — [télécharger](https://www.python.org/downloads/)
- **Node.js 18+** — [télécharger](https://nodejs.org/)
- **Git** — [télécharger](https://git-scm.com/)

### Étape 1 — Cloner le projet

```bash
git clone https://github.com/Wens1302/LINAFP.git
cd LINAFP
```

### Étape 2 — Démarrer le backend

```bash
cd backend

# Créer un environnement virtuel Python (recommandé)
python -m venv venv
source venv/bin/activate        # Linux/Mac
# venv\Scripts\activate.bat     # Windows

# Installer les dépendances
pip install -r requirements.txt

# Créer les tables et insérer les données de démarrage
python seed_data.py

# Démarrer le serveur
uvicorn main:app --reload --port 8000
```

Le backend est maintenant accessible sur : **http://localhost:8000**  
Documentation interactive de l'API : **http://localhost:8000/docs**

### Étape 3 — Démarrer le frontend

Dans un **nouveau terminal** :

```bash
cd frontend

# Installer les dépendances
npm install

# Démarrer en mode développement
npm run dev
```

Le site est maintenant accessible sur : **http://localhost:5173**

### Étape 4 — Se connecter en admin

1. Aller sur **http://localhost:5173/login**
2. Identifiant : `admin`
3. Mot de passe : `admin1234`

---

## 📥 Comment mettre de vraies données

Il existe **3 méthodes** selon vos préférences :

---

### Méthode 1 — Interface d'administration (recommandée)

C'est la méthode la plus simple. Aucune connaissance technique n'est requise.

**Ordre recommandé pour saisir les données :**

#### 1. Ajouter les équipes
1. Connectez-vous sur `/login`
2. Allez dans **Admin → Équipes** (`/admin/teams`)
3. Cliquez **« + Ajouter une équipe »**
4. Remplissez :
   - **Nom** : ex. `CF Mounana`
   - **Ville** : ex. `Mounana`
   - **Stade** : ex. `Stade de Mounana`
   - **URL du logo** : URL d'une image (ex. depuis Wikipedia ou le site officiel du club)

> 💡 Pour le logo, cherchez l'image sur Google Images → clic droit → « Copier l'adresse de l'image »

#### 2. Ajouter les joueurs
1. Allez dans **Admin → Joueurs** (`/admin/players`)
2. Cliquez **« + Ajouter un joueur »**
3. Remplissez :
   - **Nom complet**
   - **Équipe** (choisir dans la liste)
   - **Poste** : Gardien / Défenseur / Milieu / Attaquant
   - **Numéro de maillot**
   - **Âge**
   - **Nationalité**
   - **Buts** : nombre de buts marqués cette saison

#### 3. Ajouter les matchs et résultats
1. Allez dans **Admin → Matchs** (`/admin/matches`)
2. Cliquez **« + Créer un match »**
3. Remplissez :
   - **Équipe domicile** et **Équipe extérieure**
   - **Date** du match
   - **Stade**
   - **Score domicile** et **Score extérieur** *(laissez vide si le match n'est pas encore joué)*

> 💡 Le classement se calcule **automatiquement** à partir des scores des matchs. Inutile de le saisir manuellement.

#### 4. Ajouter les articles d'actualité
1. Allez dans **Admin → Articles** (`/admin/articles`)
2. Cliquez **« + Nouvel article »**
3. Remplissez :
   - **Titre**
   - **Contenu** (texte libre)
   - **Catégorie** : `Actualités`, `Matchs` ou `Transferts`
   - **URL d'image** : image illustrant l'article
   - **Auteur**

---

### Méthode 2 — Modifier le script `seed_data.py`

Si vous avez beaucoup de données à saisir d'un coup, il est plus efficace de **modifier directement le script Python** et de le réexécuter.

**⚠️ Important :** La vérification `if db.query(models.Team).count() > 0` empêche une double insertion. Pour repartir de zéro :

```bash
# Supprimer la base de données et la recréer
cd backend
rm gabonfootstats.db         # supprime toutes les données
python seed_data.py          # recrée les tables et insère vos nouvelles données
```

**Exemple — remplacer les équipes dans `seed_data.py` :**

```python
TEAMS = [
    # Remplacez par les vraies équipes de la LINAFP
    {"nom": "CF Mounana",        "ville": "Mounana",      "stade": "Stade de Mounana"},
    {"nom": "Mangasport",        "ville": "Moanda",       "stade": "Stade Municipal de Moanda"},
    {"nom": "AS Pélican",        "ville": "Libreville",   "stade": "Stade Omar Bongo"},
    {"nom": "Bouenguidi Sports", "ville": "Franceville",  "stade": "Stade de Franceville"},
    {"nom": "Stade Mandji",      "ville": "Port-Gentil",  "stade": "Stade Omnisports de Port-Gentil"},
    {"nom": "FC 105 Libreville", "ville": "Libreville",   "stade": "Stade Félix Houphouët-Boigny"},
    # ... autant d'équipes que vous voulez
]
```

**Exemple — ajouter des joueurs :**

```python
PLAYERS = [
    # Format : nom, age, nationalite, poste, numero, goals, team_idx
    # team_idx = position de l'équipe dans la liste TEAMS ci-dessus (commence à 0)
    {"nom": "Pierre Aubameyang",  "age": 32, "nationalite": "Gabonaise", "poste": "Attaquant",  "numero": 9,  "goals": 15, "team_idx": 0},
    {"nom": "Mario Lemina",       "age": 30, "nationalite": "Gabonaise", "poste": "Milieu",     "numero": 8,  "goals": 3,  "team_idx": 0},
    {"nom": "André Biyogo Poko",  "age": 28, "nationalite": "Gabonaise", "poste": "Gardien",    "numero": 1,  "goals": 0,  "team_idx": 0},
    # ... continuez pour toutes les équipes
]
```

**Exemple — saisir les matchs :**

```python
# Format : (index_equipe_domicile, index_equipe_exterieure, "YYYY-MM-DD HH:MM:SS", score_dom, score_ext)
# Laissez les scores pour les matchs à venir
MATCHES = [
    # Journée 1
    (0, 1, "2024-09-07 15:00:00", 2, 1),   # CF Mounana 2–1 Mangasport
    (2, 3, "2024-09-08 16:00:00", 0, 0),   # AS Pélican 0–0 Bouenguidi Sports
    # Journée 2
    (1, 2, "2024-09-14 15:00:00", 3, 2),   # Mangasport 3–2 AS Pélican
    (3, 0, "2024-09-15 16:00:00", 1, 1),   # Bouenguidi 1–1 CF Mounana
    # Match à venir (sans score)
    # Note : pour un match à venir, créez-le via l'interface admin sans score
]
```

**Pour relancer le script :**

```bash
cd backend
rm gabonfootstats.db
python seed_data.py
```

---

### Méthode 3 — API REST directement (curl / Postman)

Cette méthode est utile pour les intégrations automatiques ou si vous avez un autre système qui envoie les données.

#### 1. Obtenir un token d'authentification

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin1234"}'
```

Réponse :
```json
{"access_token": "eyJhbGciOiJIUzI1NiIs...", "token_type": "bearer"}
```

Copiez la valeur de `access_token` et utilisez-la pour les requêtes suivantes.

#### 2. Créer une équipe

```bash
curl -X POST http://localhost:8000/api/teams/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer VOTRE_TOKEN_ICI" \
  -d '{
    "nom": "CF Mounana",
    "ville": "Mounana",
    "stade": "Stade de Mounana",
    "logo": "https://example.com/logo-mounana.png"
  }'
```

#### 3. Créer un joueur

```bash
# Récupérez d'abord l'ID de l'équipe avec GET /api/teams/
curl -X POST http://localhost:8000/api/players/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer VOTRE_TOKEN_ICI" \
  -d '{
    "nom": "Patrick Biyogo",
    "age": 22,
    "nationalite": "Gabonaise",
    "poste": "Attaquant",
    "numero": 9,
    "goals": 8,
    "team_id": 1
  }'
```

Valeurs possibles pour `poste` : `"Gardien"`, `"Défenseur"`, `"Milieu"`, `"Attaquant"`

#### 4. Créer un match

```bash
curl -X POST http://localhost:8000/api/matches/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer VOTRE_TOKEN_ICI" \
  -d '{
    "home_team_id": 1,
    "away_team_id": 2,
    "date": "2024-09-07T15:00:00",
    "stade": "Stade de Mounana",
    "home_score": 2,
    "away_score": 1
  }'
```

> Pour un **match à venir** (sans score encore), laissez `home_score` et `away_score` à 0 ou omettez-les — vous pourrez les mettre à jour via `PUT /api/matches/{id}` après le match.

#### 5. Mettre à jour le score d'un match joué

```bash
curl -X PUT http://localhost:8000/api/matches/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer VOTRE_TOKEN_ICI" \
  -d '{
    "home_score": 2,
    "away_score": 1
  }'
```

#### 6. Créer un article

```bash
curl -X POST http://localhost:8000/api/articles \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer VOTRE_TOKEN_ICI" \
  -d '{
    "titre": "CF Mounana s'\''impose dans le derby",
    "contenu": "Dans un match électrique...",
    "image_url": "https://images.unsplash.com/photo-xxx",
    "categorie": "match",
    "auteur": "Rédaction LINAFP"
  }'
```

Valeurs possibles pour `categorie` : `"news"`, `"match"`, `"transfert"`

#### Documentation interactive

Toute l'API est documentée automatiquement par FastAPI. Accédez à :  
**http://localhost:8000/docs** — Interface Swagger (vous pouvez tester directement depuis le navigateur)

---

## 📋 Référence complète des données

### Équipe (`Team`)

| Champ | Type | Obligatoire | Description |
|-------|------|-------------|-------------|
| `nom` | texte | ✅ | Nom du club |
| `ville` | texte | ✅ | Ville du club |
| `stade` | texte | ✅ | Nom du stade |
| `logo` | URL | ❌ | URL du logo (image PNG/JPG) |

### Joueur (`Player`)

| Champ | Type | Obligatoire | Description |
|-------|------|-------------|-------------|
| `nom` | texte | ✅ | Nom complet du joueur |
| `age` | entier | ✅ | Âge en années |
| `nationalite` | texte | ✅ | ex. `"Gabonaise"` |
| `poste` | texte | ✅ | `"Gardien"` / `"Défenseur"` / `"Milieu"` / `"Attaquant"` |
| `numero` | entier | ✅ | Numéro de maillot |
| `goals` | entier | ❌ | Nombre de buts (défaut : 0) |
| `team_id` | entier | ✅ | ID de l'équipe |

### Match (`Match`)

| Champ | Type | Obligatoire | Description |
|-------|------|-------------|-------------|
| `home_team_id` | entier | ✅ | ID équipe domicile |
| `away_team_id` | entier | ✅ | ID équipe extérieure |
| `date` | datetime | ✅ | Format `"2024-09-07T15:00:00"` |
| `stade` | texte | ✅ | Nom du stade |
| `home_score` | entier | ❌ | Score domicile (défaut : 0) |
| `away_score` | entier | ❌ | Score extérieur (défaut : 0) |

### Article

| Champ | Type | Obligatoire | Description |
|-------|------|-------------|-------------|
| `titre` | texte | ✅ | Titre de l'article |
| `contenu` | texte long | ✅ | Corps de l'article |
| `categorie` | texte | ✅ | `"news"` / `"match"` / `"transfert"` |
| `auteur` | texte | ❌ | Auteur (défaut : `"Rédaction LINAFP"`) |
| `image_url` | URL | ❌ | Image d'illustration |
| `date_publication` | datetime | ❌ | Défaut : maintenant |

### Règles du classement (automatique)

Le classement est **recalculé automatiquement** à partir des matchs enregistrés :

| Résultat | Points |
|----------|--------|
| Victoire | **3 points** |
| Match nul | **1 point** |
| Défaite | **0 point** |

Tri : **Points → Différence de buts → Buts marqués**

---

## 🐘 Passer à PostgreSQL

Pour un site en production ou avec beaucoup de données, PostgreSQL est recommandé.

### Installation de PostgreSQL

```bash
# Ubuntu/Debian
sudo apt install postgresql postgresql-contrib

# macOS (avec Homebrew)
brew install postgresql
```

### Créer la base de données

```sql
-- Dans le terminal PostgreSQL (psql)
CREATE USER linafp WITH PASSWORD 'motdepasse_fort';
CREATE DATABASE gabonfootstats OWNER linafp;
```

### Configurer le backend

Créez un fichier `backend/.env` :

```env
DATABASE_URL=postgresql://linafp:motdepasse_fort@localhost/gabonfootstats
JWT_SECRET_KEY=une-cle-secrete-longue-et-aleatoire-minimum-32-caracteres
ADMIN_USERNAME=admin
ADMIN_PASSWORD=NouveauMotDePasseFort!
```

Puis relancez :

```bash
cd backend
python seed_data.py   # crée les tables PostgreSQL et insère les données
uvicorn main:app --reload --port 8000
```

---

## 🔒 Sécurité en production

**Avant de mettre le site en ligne, effectuez ces changements :**

### 1. Changer le mot de passe admin

Dans `backend/.env` :
```env
ADMIN_USERNAME=admin
ADMIN_PASSWORD=MotDePasseTresSecurise2024!
```
Puis : `rm gabonfootstats.db && python seed_data.py`  
*(ou via l'interface si vous utilisez PostgreSQL : supprimez l'entrée de la table `admin_users` et relancez `seed_data.py`)*

### 2. Changer la clé secrète JWT

Dans `backend/.env` :
```env
JWT_SECRET_KEY=une-longue-cle-aleatoire-unique-a-votre-projet-minimum-64-caracteres
```

### 3. Restreindre CORS

Dans `backend/.env`, remplacez `*` par votre domaine :
```env
CORS_ORIGINS=https://votre-domaine.com
```

### 4. Utiliser HTTPS

Placez un reverse proxy (Nginx, Caddy, Traefik) devant l'application qui gère le certificat TLS.

---

## ❓ FAQ

**Q : Comment réinitialiser toutes les données ?**  
```bash
cd backend
rm gabonfootstats.db     # supprime tout
python seed_data.py      # repart de zéro
```

**Q : Comment mettre à jour le score d'un match après qu'il a été joué ?**  
Allez dans **Admin → Matchs**, cliquez **✏️ Modifier** sur le match concerné et saisissez les scores.

**Q : Le classement est faux, que faire ?**  
Le classement est calculé automatiquement depuis les matchs. Vérifiez que les scores des matchs sont bien saisis. Pas besoin de toucher au classement manuellement.

**Q : Je veux ajouter des logos d'équipes. Comment ?**  
- Téléversez vos images sur un service gratuit (ex. [Imgur](https://imgur.com/), [Cloudinary](https://cloudinary.com/)) et copiez l'URL directe (se terminant par `.png` ou `.jpg`)
- Ou hébergez-les dans le dossier `frontend/public/logos/` et utilisez l'URL `/logos/nom-equipe.png`

**Q : Comment ajouter un deuxième administrateur ?**  
Actuellement l'application ne gère qu'un admin. Pour en ajouter un, connectez-vous à la base de données directement :
```python
# Dans backend/ (Python)
from database import SessionLocal
from models import AdminUser
from auth import hash_password

db = SessionLocal()
db.add(AdminUser(username="admin2", hashed_password=hash_password("mot_de_passe")))
db.commit()
db.close()
```

**Q : L'API me renvoie une erreur 401. Pourquoi ?**  
Le token JWT a expiré (durée : 8 heures). Reconnectez-vous via `/login`.

**Q : Peut-on importer des données depuis Excel/CSV ?**  
Pas directement depuis l'interface. Mais vous pouvez écrire un script Python qui lit votre fichier CSV et appelle les routes API. Voici un exemple minimal :

```python
import csv
import requests

# 1. Obtenir le token
r = requests.post("http://localhost:8000/api/auth/login",
                  json={"username": "admin", "password": "admin1234"})
token = r.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# 2. Lire un fichier CSV et créer les équipes
with open("equipes.csv", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        requests.post("http://localhost:8000/api/teams/",
                      json={"nom": row["nom"], "ville": row["ville"], "stade": row["stade"]},
                      headers=headers)
print("Équipes importées !")
```

---

*Document généré pour le projet GabonFootStats — LINAFP · Saison 2024*
