from database.connection import get_connection
from models.achievement import UserAchievement


def sync_catalog(catalog):
    with get_connection() as connection:
        for achievement in catalog:
            connection.execute(
                """
                INSERT INTO achievement (achievement_key, nome, descricao)
                VALUES (?, ?, ?)
                ON CONFLICT(achievement_key) DO UPDATE SET
                  nome = excluded.nome,
                  descricao = excluded.descricao
                """,
                (
                    achievement["key"],
                    achievement["nome"],
                    achievement["descricao"],
                ),
            )
        connection.commit()


def unlock_for_user(user_id, achievement_key):
    achievement, _created = unlock_for_user_with_status(user_id, achievement_key)
    return achievement


def unlock_for_user_with_status(user_id, achievement_key):
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT OR IGNORE INTO user_achievement (user_id, achievement_key)
            VALUES (?, ?)
            """,
            (user_id, achievement_key),
        )
        created = cursor.rowcount == 1
        connection.commit()
    return find_for_user(user_id, achievement_key), created


def list_unlocked_by_user_id(user_id):
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT ua.id, ua.user_id, ua.achievement_key, a.nome, a.descricao,
                   ua.data_desbloqueio
            FROM user_achievement ua
            INNER JOIN achievement a ON a.achievement_key = ua.achievement_key
            WHERE ua.user_id = ?
            ORDER BY ua.data_desbloqueio DESC, ua.id DESC
            """,
            (user_id,),
        ).fetchall()
        return [UserAchievement.from_row(row) for row in rows]


def count_catalog():
    with get_connection() as connection:
        return connection.execute("SELECT COUNT(*) FROM achievement").fetchone()[0]


def find_for_user(user_id, achievement_key):
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT ua.id, ua.user_id, ua.achievement_key, a.nome, a.descricao,
                   ua.data_desbloqueio
            FROM user_achievement ua
            INNER JOIN achievement a ON a.achievement_key = ua.achievement_key
            WHERE ua.user_id = ? AND ua.achievement_key = ?
            """,
            (user_id, achievement_key),
        ).fetchone()
        return UserAchievement.from_row(row) if row else None
