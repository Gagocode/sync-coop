from database.connection import get_connection
from models.certificate import Certificate


def create_certificate(user_id, nome, instituicao, carga_horaria, data_conclusao, arquivo_path=None):
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO certificates
              (user_id, nome, instituicao, carga_horaria, data_conclusao, arquivo_path)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (user_id, nome, instituicao, carga_horaria, data_conclusao, arquivo_path),
        )
        connection.commit()
        return find_by_id_for_user(cursor.lastrowid, user_id)


def list_by_user_id(user_id):
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT id, user_id, nome, instituicao, carga_horaria,
                   data_conclusao, arquivo_path, created_at
            FROM certificates
            WHERE user_id = ?
            ORDER BY data_conclusao DESC, id DESC
            """,
            (user_id,),
        ).fetchall()
        return [Certificate.from_row(row) for row in rows]


def count_by_user_id(user_id):
    with get_connection() as connection:
        return connection.execute(
            """
            SELECT COUNT(*)
            FROM certificates
            WHERE user_id = ?
            """,
            (user_id,),
        ).fetchone()[0]


def find_by_id_for_user(certificate_id, user_id):
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT id, user_id, nome, instituicao, carga_horaria,
                   data_conclusao, arquivo_path, created_at
            FROM certificates
            WHERE id = ? AND user_id = ?
            """,
            (certificate_id, user_id),
        ).fetchone()
        return Certificate.from_row(row) if row else None


def update_certificate(
    certificate_id,
    user_id,
    nome,
    instituicao,
    carga_horaria,
    data_conclusao,
    arquivo_path=None,
):
    with get_connection() as connection:
        connection.execute(
            """
            UPDATE certificates
            SET nome = ?,
                instituicao = ?,
                carga_horaria = ?,
                data_conclusao = ?,
                arquivo_path = ?
            WHERE id = ? AND user_id = ?
            """,
            (
                nome,
                instituicao,
                carga_horaria,
                data_conclusao,
                arquivo_path,
                certificate_id,
                user_id,
            ),
        )
        connection.commit()
        return find_by_id_for_user(certificate_id, user_id)


def delete_certificate(certificate_id, user_id):
    with get_connection() as connection:
        cursor = connection.execute(
            """
            DELETE FROM certificates
            WHERE id = ? AND user_id = ?
            """,
            (certificate_id, user_id),
        )
        connection.commit()
        return cursor.rowcount > 0
