# LINAFP

A personal finance management application built with FastAPI and PostgreSQL.

## Backend Setup

### Prerequisites

- Python 3.10+
- PostgreSQL 14+ (must be running before executing `seed_data.py` or for full
  API functionality; the server itself starts even when the DB is unreachable)

### Installation

```bash
cd backend
pip install -r requirements.txt
```

### Configuration

Copy the example environment file and fill in your database credentials:

```bash
cp .env.example .env
```

Edit `.env`:

```env
DATABASE_URL=postgresql://<user>:<password>@<host>:<port>/<database>
```

> **Important – file encoding on Windows**  
> Save the `.env` file with **UTF-8** encoding (in Notepad: *File > Save As >
> Encoding: UTF-8*).  Saving in another encoding (e.g. ANSI / CP1252) causes a
> `UnicodeDecodeError` in psycopg2 when the URL contains accented characters.  
> If your password contains special characters, percent-encode them:
> ```
> python -c "from urllib.parse import quote; print(quote('your_password', safe=''))"
> ```

### Seed the database

Create the tables and load sample data:

```bash
# From the backend/ directory
python seed_data.py
```

### Running the server

```bash
# From the project root
uvicorn backend.main:app --reload --port 8000
```

The API will be available at <http://127.0.0.1:8000>.  
Interactive docs are served at <http://127.0.0.1:8000/docs>.

> **Common error — "Connection refused" on port 5432**  
> This means PostgreSQL is not running.  Start your PostgreSQL service and
> re-run the server.  The application will then connect on first request.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Database connectivity check |
| POST | `/users/` | Create a user |
| GET | `/users/{user_id}` | Get a user |
| POST | `/users/{user_id}/transactions/` | Add a transaction |
| GET | `/users/{user_id}/transactions/` | List transactions |