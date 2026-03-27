from contextlib import asynccontextmanager
import logging
import os

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from .database import get_db, init_db, check_db_connection
from . import models, schemas

logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler.

    Database table creation happens here – AFTER the process has started –
    so the server no longer crashes at import time when PostgreSQL is not yet
    available.  If the DB is unreachable the server still starts; the /health
    endpoint and individual routes will surface the connection error instead.
    """
    try:
        init_db()
    except Exception as exc:
        # Log the warning but do not abort startup so that the process stays
        # alive and can be probed (e.g. /health) or recovered later.
        logger.warning("Database initialization failed at startup: %s", exc)
    yield


app = FastAPI(
    title="LINAFP API",
    version="1.0.0",
    description="Backend API for the LINAFP application",
    lifespan=lifespan,
)

# Restrict allowed origins via environment variable in production.
# Example: ALLOWED_ORIGINS="https://myapp.example.com,https://admin.example.com"
_raw_origins = os.getenv("ALLOWED_ORIGINS", "")
allowed_origins = [o.strip() for o in _raw_origins.split(",") if o.strip()] or ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Health ────────────────────────────────────────────────────────────────────

@app.get("/health", response_model=schemas.HealthResponse, tags=["health"])
def health_check():
    db_ok = check_db_connection()
    return {
        "status": "ok",
        "database": "connected" if db_ok else "unreachable",
    }


# ── Users ─────────────────────────────────────────────────────────────────────

@app.post(
    "/users/",
    response_model=schemas.UserRead,
    status_code=status.HTTP_201_CREATED,
    tags=["users"],
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(
        (models.User.email == user.email) |
        (models.User.username == user.username)
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered.",
        )
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.get("/users/{user_id}", response_model=schemas.UserRead, tags=["users"])
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )
    return db_user


# ── Transactions ──────────────────────────────────────────────────────────────

@app.post(
    "/users/{user_id}/transactions/",
    response_model=schemas.TransactionRead,
    status_code=status.HTTP_201_CREATED,
    tags=["transactions"],
)
def create_transaction(
    user_id: int,
    transaction: schemas.TransactionCreate,
    db: Session = Depends(get_db),
):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )
    db_tx = models.Transaction(**transaction.model_dump(), owner_id=user_id)
    db.add(db_tx)
    db.commit()
    db.refresh(db_tx)
    return db_tx


@app.get(
    "/users/{user_id}/transactions/",
    response_model=list[schemas.TransactionRead],
    tags=["transactions"],
)
def list_transactions(
    user_id: int,
    db: Session = Depends(get_db),
):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )
    return db_user.transactions
