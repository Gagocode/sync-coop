from database.connection import get_connection
from models.sector import Sector


def list_by_organization(organization_id):
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT id, organization_id, name, created_at, updated_at
            FROM sectors
            WHERE organization_id = ?
            ORDER BY name COLLATE NOCASE, id
            """,
            (organization_id,),
        ).fetchall()
        return [Sector.from_row(row) for row in rows]


def find_by_id_for_organization(sector_id, organization_id):
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT id, organization_id, name, created_at, updated_at
            FROM sectors
            WHERE id = ? AND organization_id = ?
            """,
            (sector_id, organization_id),
        ).fetchone()
        return Sector.from_row(row) if row else None


def create(organization_id, name):
    with get_connection() as connection:
        cursor = connection.execute(
            "INSERT INTO sectors (organization_id, name) VALUES (?, ?)",
            (organization_id, name),
        )
        row = connection.execute(
            """
            SELECT id, organization_id, name, created_at, updated_at
            FROM sectors WHERE id = ?
            """,
            (cursor.lastrowid,),
        ).fetchone()
        return Sector.from_row(row)


def update_name(sector_id, organization_id, name):
    with get_connection() as connection:
        cursor = connection.execute(
            """
            UPDATE sectors
            SET name = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ? AND organization_id = ?
            """,
            (name, sector_id, organization_id),
        )
        if cursor.rowcount != 1:
            return None
        row = connection.execute(
            """
            SELECT id, organization_id, name, created_at, updated_at
            FROM sectors WHERE id = ? AND organization_id = ?
            """,
            (sector_id, organization_id),
        ).fetchone()
        return Sector.from_row(row)


def delete_if_empty(sector_id, organization_id):
    with get_connection() as connection:
        cursor = connection.execute(
            """
            DELETE FROM sectors
            WHERE id = ? AND organization_id = ?
              AND NOT EXISTS (SELECT 1 FROM users WHERE users.sector_id = sectors.id)
            """,
            (sector_id, organization_id),
        )
        return cursor.rowcount == 1
