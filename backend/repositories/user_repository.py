from database.connection import get_connection
from models.user import User


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
            """
            SELECT id, nome, email, senha_hash, curso, classe, xp, created_at
            FROM users
            WHERE email = ?
            """,
            (email,),
        ).fetchone()
        return User.from_row(row) if row else None


def find_by_id(user_id):
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT id, nome, email, senha_hash, curso, classe, xp, created_at
            FROM users
            WHERE id = ?
            """,
            (user_id,),
        ).fetchone()
        return User.from_row(row) if row else None


def find_public_by_id(user_id):
    return find_by_id(user_id)


def find_public_by_name(nome):
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT id, nome, email, senha_hash, curso, classe, xp, created_at
            FROM users
            WHERE nome = ? COLLATE NOCASE
            ORDER BY id
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
