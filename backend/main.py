import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine
import models  # noqa: F401 - registers all ORM models with Base
from routers import teams, players, matches, standings, stats
from routers import auth, articles

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="GabonFootStats API",
    description="Backend API for the GabonFootStats football statistics application",
    version="1.0.0",
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
    return {"status": "ok", "service": "GabonFootStats API"}
