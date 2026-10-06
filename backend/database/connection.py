import sqlite3
from pathlib import Path


DATABASE_PATH = Path(__file__).resolve().parent / "sync_disc.sqlite3"
SCHEMA_PATH = Path(__file__).resolve().parent / "schema.sql"


def get_connection(database_path=DATABASE_PATH):
    database_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(str(database_path.resolve()))
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_database(database_path=DATABASE_PATH):
    with get_connection(database_path) as connection:
        connection.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
        _ensure_users_profile_columns(connection)
        _ensure_users_organization_columns(connection)
        connection.commit()


def _ensure_users_profile_columns(connection):
    columns = {
        row["name"]
        for row in connection.execute("PRAGMA table_info(users)").fetchall()
    }
    if "classe" not in columns:
        connection.execute("ALTER TABLE users ADD COLUMN classe TEXT")
    if "xp" not in columns:
        connection.execute("ALTER TABLE users ADD COLUMN xp INTEGER NOT NULL DEFAULT 0")


def _ensure_users_organization_columns(connection):
    columns = {
        row["name"]
        for row in connection.execute("PRAGMA table_info(users)").fetchall()
    }
    if "organization_id" not in columns:
        connection.execute(
            "ALTER TABLE users ADD COLUMN organization_id INTEGER "
            "REFERENCES organizations (id) ON DELETE RESTRICT"
        )
    if "sector_id" not in columns:
        connection.execute(
            "ALTER TABLE users ADD COLUMN sector_id INTEGER "
            "REFERENCES sectors (id) ON DELETE RESTRICT"
        )
    if "role" not in columns:
        connection.execute(
            "ALTER TABLE users ADD COLUMN role TEXT "
            "CHECK (role IS NULL OR role IN ('manager', 'collaborator'))"
        )
    connection.execute(
        "CREATE INDEX IF NOT EXISTS idx_users_organization_sector "
        "ON users (organization_id, sector_id)"
    )
    connection.execute(
        "CREATE INDEX IF NOT EXISTS idx_users_role ON users (role)"
    )
