import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Load .env with an explicit UTF-8 encoding so that passwords containing
# accented characters (common on French/Windows systems using CP1252) are
# read correctly by Python before being handed to SQLAlchemy / psycopg2.
load_dotenv(encoding='utf-8')

_raw_url = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/linafp",
)

# Re-parse and re-encode the URL so that any non-ASCII characters in the
# password (or other URL components) are percent-encoded.  Without this step,
# psycopg2 raises UnicodeDecodeError when the password contains characters
# such as accented French letters (e.g. 0xe9 = 'é' in Latin-1 / CP1252).
try:
    _parsed = make_url(_raw_url)
    DATABASE_URL = _parsed.render_as_string(hide_password=False)
except Exception:
    DATABASE_URL = _raw_url

# pool_pre_ping=True makes SQLAlchemy test each connection before using it,
# so stale connections are refreshed rather than raising an error mid-request.
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency that provides a database session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create all tables.  Called from the application lifespan, NOT at import time."""
    from . import models  # noqa: F401 - ensures models are registered
    Base.metadata.create_all(bind=engine)


def check_db_connection() -> bool:
    """Return True if the database is reachable, False otherwise."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False
