import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.engine import make_url

# Load .env with an explicit UTF-8 encoding so that passwords containing
# accented characters (common on French/Windows systems using CP1252) are
# read correctly by Python before being handed to SQLAlchemy / psycopg2.
load_dotenv(encoding='utf-8')

_raw_url = os.getenv("DATABASE_URL", "sqlite:///./gabonfootstats.db")

# Re-parse and re-encode the URL so that any non-ASCII characters in the
# password (or other URL components) are percent-encoded.  Without this step,
# psycopg2 raises UnicodeDecodeError when the password contains characters
# such as accented French letters (e.g. 0xe9 = 'é' in Latin-1 / CP1252).
try:
    _parsed = make_url(_raw_url)
    DATABASE_URL = _parsed.render_as_string(hide_password=False)
except Exception:
    DATABASE_URL = _raw_url

connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
