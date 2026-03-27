import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import init_db, check_db_connection
import models  # noqa: F401 – registers all ORM models with Base
from routers import teams, players, matches, standings, stats
from routers import auth, articles

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler.

    Database table creation happens here – AFTER the process has started –
    so the server no longer crashes at import time when the database is not
    yet available. If the DB is unreachable the server still starts; the
    /api/health endpoint and individual routes will surface the error instead.
    """
    try:
        init_db()
    except Exception as exc:
        logger.warning("Database initialization failed at startup: %s", exc)
    yield


app = FastAPI(
    title="GabonFootStats API",
    description="Backend API for the GabonFootStats football statistics application",
    version="1.0.0",
    lifespan=lifespan,
)

_raw_origins = os.getenv("CORS_ORIGINS", "*")
allowed_origins: list[str] = (
    ["*"] if _raw_origins == "*" else [o.strip() for o in _raw_origins.split(",") if o.strip()]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=allowed_origins != ["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(articles.router)
app.include_router(teams.router)
app.include_router(players.router)
app.include_router(matches.router)
app.include_router(standings.router)
app.include_router(stats.router)


@app.get("/api/health", tags=["health"])
def health_check():
    db_ok = check_db_connection()
    return {
        "status": "ok",
        "service": "GabonFootStats API",
        "database": "connected" if db_ok else "unreachable",
    }
