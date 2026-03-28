"""seed_data.py – Create database tables and populate them with initial sample data.

Run from inside the ``backend/`` directory::

    python seed_data.py

Prerequisites
-------------
* PostgreSQL is running and reachable.
* A ``.env`` file exists in the ``backend/`` directory with a valid
  ``DATABASE_URL``.

  **Important – file encoding on Windows**: Save the ``.env`` file with
  **UTF-8** encoding (in Notepad: *File > Save As > Encoding: UTF-8*).
  Saving in another encoding (e.g. ANSI / CP1252) can cause a
  ``UnicodeDecodeError`` in psycopg2 when the URL contains accented
  characters.  If your password contains special characters that cannot be
  stored in UTF-8, percent-encode them instead::

      python -c "from urllib.parse import quote; print(quote('your_password', safe=''))"

  For example, ``motdepassé`` becomes ``motdepasse%C3%A9`` in the URL.
"""

import os
import sys

# ---------------------------------------------------------------------------
# Step 1 – load the .env file BEFORE importing any project module.
#
# Calling load_dotenv() with encoding='utf-8' ensures that the file is read
# as UTF-8.  This prevents the UnicodeDecodeError that psycopg2 raises when
# the DATABASE_URL contains accented characters (e.g. 'é', byte 0xe9 in
# CP1252 / Latin-1) that are not valid in a UTF-8 byte stream.
#
# If your .env file was accidentally saved with a non-UTF-8 encoding and you
# see "UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9", re-open the
# file in a text editor and re-save it as UTF-8.
# ---------------------------------------------------------------------------
from dotenv import load_dotenv

_env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
load_dotenv(dotenv_path=_env_path, encoding='utf-8')

# ---------------------------------------------------------------------------
# Step 2 – make sure the project root is on sys.path so that the ``backend``
# package can be imported when this script is executed directly with
# ``python seed_data.py`` from inside the backend/ directory.
# ---------------------------------------------------------------------------
_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

# ---------------------------------------------------------------------------
# Step 3 – import project modules (database and models).
# The database module reads DATABASE_URL from the environment that was just
# populated by load_dotenv().  It also applies make_url() to percent-encode
# any remaining non-ASCII characters in the URL, providing a second layer of
# defence against UnicodeDecodeError.
# ---------------------------------------------------------------------------
from backend import models  # noqa: F401 - registers all ORM classes
from backend.database import engine, Base, SessionLocal

# ---------------------------------------------------------------------------
# Step 4 – create all database tables (idempotent; safe to run repeatedly).
# ---------------------------------------------------------------------------
print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully.")

# ---------------------------------------------------------------------------
# Step 5 – seed initial data (skipped when the users table is not empty).
# ---------------------------------------------------------------------------
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

db = SessionLocal()
try:
    if db.query(models.User).count() == 0:
        print("Seeding initial data...")

        demo_user = models.User(
            username="admin",
            email="admin@linafp.local",
            hashed_password=pwd_context.hash("changeme"),
        )
        db.add(demo_user)
        db.flush()  # populate demo_user.id before creating transactions

        demo_transactions = [
            models.Transaction(
                description="Salaire",
                amount=2500.00,
                category="Revenu",
                owner_id=demo_user.id,
            ),
            models.Transaction(
                description="Loyer",
                amount=-800.00,
                category="Logement",
                owner_id=demo_user.id,
            ),
            models.Transaction(
                description="Courses",
                amount=-150.00,
                category="Alimentation",
                owner_id=demo_user.id,
            ),
        ]
        db.add_all(demo_transactions)
        db.commit()
        print(
            f"Seeded user '{demo_user.username}' with "
            f"{len(demo_transactions)} transactions."
        )
    else:
        print("Database already contains data – skipping seed.")
finally:
    db.close()

print("Done.")
