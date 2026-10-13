import sqlite3
from contextlib import contextmanager
from contextvars import ContextVar
from pathlib import Path


DATABASE_PATH = Path(__file__).resolve().parent / "sync_disc.sqlite3"
SCHEMA_PATH = Path(__file__).resolve().parent / "schema.sql"
_active_transaction = ContextVar("sync_disc_transaction", default=None)


@contextmanager
def get_connection(database_path=None):
    if database_path is None:
        database_path = DATABASE_PATH
    database_path = Path(database_path)
    active = _active_transaction.get()
    if active is not None:
        yield active
        return

    database_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(str(database_path.resolve()))
    connection.row_factory = sqlite3.Row
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


@contextmanager
def transaction():
    if _active_transaction.get() is not None:
        yield _active_transaction.get()
        return

    with get_connection() as connection:
        connection.execute("BEGIN IMMEDIATE")
        token = _active_transaction.set(connection)
        try:
            yield connection
        finally:
            _active_transaction.reset(token)


def init_database(database_path=None):
    with get_connection(database_path) as connection:
        connection.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
        _ensure_users_profile_columns(connection)


def _ensure_users_profile_columns(connection):
    columns = {
        row["name"]
        for row in connection.execute("PRAGMA table_info(users)").fetchall()
    }
    if "classe" not in columns:
        connection.execute("ALTER TABLE users ADD COLUMN classe TEXT")
    if "xp" not in columns:
        connection.execute("ALTER TABLE users ADD COLUMN xp INTEGER NOT NULL DEFAULT 0")
