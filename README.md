# LINAFP

A personal finance management application built with FastAPI and PostgreSQL.

## Backend Setup

### Prerequisites

- Python 3.10+
- PostgreSQL 14+ running on `localhost:5432`

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
> You can verify connectivity at any time via the `/health` endpoint.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Database connectivity check |
| POST | `/users/` | Create a user |
| GET | `/users/{user_id}` | Get a user |
| POST | `/users/{user_id}/transactions/` | Add a transaction |
| GET | `/users/{user_id}/transactions/` | List transactions |
