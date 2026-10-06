from database.connection import get_connection
from models.project import Project


def create_project(user_id, titulo, descricao, tecnologias, link=None):
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO projects (user_id, titulo, descricao, tecnologias, link)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user_id, titulo, descricao, tecnologias, link),
        )
        connection.commit()
        return find_by_id_for_user(cursor.lastrowid, user_id)


def list_by_user_id(user_id):
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT id, user_id, titulo, descricao, tecnologias, link, created_at
            FROM projects
            WHERE user_id = ?
            ORDER BY created_at DESC, id DESC
            """,
            (user_id,),
        ).fetchall()
        return [Project.from_row(row) for row in rows]


def count_by_user_id(user_id):
    with get_connection() as connection:
        return connection.execute(
            """
            SELECT COUNT(*)
            FROM projects
            WHERE user_id = ?
            """,
            (user_id,),
        ).fetchone()[0]


def find_by_id_for_user(project_id, user_id):
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT id, user_id, titulo, descricao, tecnologias, link, created_at
            FROM projects
            WHERE id = ? AND user_id = ?
            """,
            (project_id, user_id),
        ).fetchone()
        return Project.from_row(row) if row else None


def update_project(project_id, user_id, titulo, descricao, tecnologias, link=None):
    with get_connection() as connection:
        connection.execute(
            """
            UPDATE projects
            SET titulo = ?,
                descricao = ?,
                tecnologias = ?,
                link = ?
            WHERE id = ? AND user_id = ?
            """,
            (titulo, descricao, tecnologias, link, project_id, user_id),
        )
        connection.commit()
        return find_by_id_for_user(project_id, user_id)


def delete_project(project_id, user_id):
    with get_connection() as connection:
        cursor = connection.execute(
            """
            DELETE FROM projects
            WHERE id = ? AND user_id = ?
            """,
            (project_id, user_id),
        )
        connection.commit()
        return cursor.rowcount > 0
