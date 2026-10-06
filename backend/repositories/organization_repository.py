from database.connection import get_connection
from models.organization import Organization


def has_any():
    with get_connection() as connection:
        return connection.execute("SELECT 1 FROM organizations LIMIT 1").fetchone() is not None


def create_first_for_manager(user_id, name):
    with get_connection() as connection:
        connection.execute("BEGIN IMMEDIATE")
        if connection.execute("SELECT 1 FROM organizations LIMIT 1").fetchone():
            return None

        user = connection.execute(
            "SELECT organization_id, role FROM users WHERE id = ?", (user_id,)
        ).fetchone()
        if not user or user["organization_id"] is not None or user["role"] is not None:
            return None

        cursor = connection.execute(
            "INSERT INTO organizations (name) VALUES (?)", (name,)
        )
        organization_id = cursor.lastrowid
        updated = connection.execute(
            """
            UPDATE users
            SET organization_id = ?, sector_id = NULL, role = 'manager'
            WHERE id = ? AND organization_id IS NULL AND role IS NULL
            """,
            (organization_id, user_id),
        )
        if updated.rowcount != 1:
            raise RuntimeError("Não foi possível associar o gestor à organização")
        row = connection.execute(
            "SELECT id, name, created_at, updated_at FROM organizations WHERE id = ?",
            (organization_id,),
        ).fetchone()
        return Organization.from_row(row)
