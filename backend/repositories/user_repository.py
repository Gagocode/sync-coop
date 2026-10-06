from database.connection import get_connection
from models.user import User


_USER_SELECT = """
    SELECT u.id, u.nome, u.email, u.senha_hash, u.curso, u.classe, u.xp,
           u.created_at, u.organization_id, u.sector_id, u.role, u.last_activity_at,
           o.name AS organization_name, s.name AS sector_name
    FROM users u
    LEFT JOIN organizations o ON o.id = u.organization_id
    LEFT JOIN sectors s ON s.id = u.sector_id
"""


def create_user(nome, email, senha_hash, curso=None):
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO users (nome, email, senha_hash, curso, xp)
            VALUES (?, ?, ?, ?, 0)
            """,
            (nome, email, senha_hash, curso),
        )
        connection.commit()
        return find_by_id(cursor.lastrowid)


def find_by_email(email):
    with get_connection() as connection:
        row = connection.execute(
            f"""
            {_USER_SELECT}
            WHERE u.email = ?
            """,
            (email,),
        ).fetchone()
        return User.from_row(row) if row else None


def find_by_id(user_id):
    with get_connection() as connection:
        row = connection.execute(
            f"""
            {_USER_SELECT}
            WHERE u.id = ?
            """,
            (user_id,),
        ).fetchone()
        return User.from_row(row) if row else None


def find_public_by_id(user_id):
    return find_by_id(user_id)


def find_public_by_name(nome):
    with get_connection() as connection:
        rows = connection.execute(
            f"""
            {_USER_SELECT}
            WHERE u.nome = ? COLLATE NOCASE
            ORDER BY u.id
            LIMIT 2
            """,
            (nome,),
        ).fetchall()
        return [User.from_row(row) for row in rows]


def update_profile_class(user_id, classe):
    with get_connection() as connection:
        connection.execute(
            """
            UPDATE users
            SET classe = ?
            WHERE id = ?
            """,
            (classe, user_id),
        )
        connection.commit()
        return find_by_id(user_id)


def update_password_hash(user_id, senha_hash):
    with get_connection() as connection:
        connection.execute(
            """
            UPDATE users
            SET senha_hash = ?
            WHERE id = ?
            """,
            (senha_hash, user_id),
        )
        connection.commit()
        return find_by_id(user_id)


def add_xp(user_id, xp_amount):
    with get_connection() as connection:
        connection.execute(
            """
            UPDATE users
            SET xp = xp + ?
            WHERE id = ?
            """,
            (xp_amount, user_id),
        )
        connection.commit()
        return find_by_id(user_id)


def list_for_organization_or_unassigned(organization_id):
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT u.id, u.nome, u.email, u.organization_id, u.sector_id, u.role,
                   o.name AS organization_name, s.name AS sector_name
            FROM users u
            LEFT JOIN organizations o ON o.id = u.organization_id
            LEFT JOIN sectors s ON s.id = u.sector_id
            WHERE u.organization_id = ? OR u.organization_id IS NULL
            ORDER BY CASE WHEN u.organization_id IS NULL THEN 1 ELSE 0 END,
                     u.nome COLLATE NOCASE, u.id
            """,
            (organization_id,),
        ).fetchall()
        return [dict(row) for row in rows]


def assign_sector(user_id, organization_id, sector_id):
    with get_connection() as connection:
        cursor = connection.execute(
            """
            UPDATE users
            SET organization_id = ?, sector_id = ?, role = 'collaborator'
            WHERE id = ?
              AND (organization_id = ? OR organization_id IS NULL)
              AND (role IS NULL OR role = 'collaborator')
            """,
            (organization_id, sector_id, user_id, organization_id),
        )
        connection.commit()
        return cursor.rowcount == 1


def update_last_activity(user_id, activity_at, connection=None):
    if connection is None:
        with get_connection() as connection:
            return update_last_activity(user_id, activity_at, connection)
    connection.execute(
        """
        UPDATE users SET last_activity_at = ?
        WHERE id = ? AND (last_activity_at IS NULL OR last_activity_at < ?)
        """,
        (activity_at, user_id, activity_at),
    )


def list_collaborators_for_organization(organization_id):
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT u.id, u.nome, s.name AS sector_name, u.last_activity_at
            FROM users u
            LEFT JOIN sectors s ON s.id = u.sector_id
                               AND s.organization_id = u.organization_id
            WHERE u.organization_id = ? AND u.role = 'collaborator'
            ORDER BY u.nome COLLATE NOCASE, u.id
            """,
            (organization_id,),
        ).fetchall()
        return [dict(row) for row in rows]
