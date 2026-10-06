from database.connection import get_connection
from models.evolution_event import EvolutionEvent


def create_event(user_id, event_key, event_type, titulo, descricao, created_at=None):
    with get_connection() as connection:
        connection.execute(
            """
            INSERT OR IGNORE INTO evolution_events
              (user_id, event_key, event_type, titulo, descricao, created_at)
            VALUES (?, ?, ?, ?, ?, COALESCE(?, CURRENT_TIMESTAMP))
            """,
            (user_id, event_key, event_type, titulo, descricao, created_at),
        )
        connection.commit()
    return find_by_key_for_user(user_id, event_key)


def list_recent_by_user_id(user_id, limit=8):
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT id, user_id, event_key, event_type, titulo, descricao, created_at
            FROM evolution_events
            WHERE user_id = ?
            ORDER BY created_at DESC, id DESC
            LIMIT ?
            """,
            (user_id, limit),
        ).fetchall()
        return [EvolutionEvent.from_row(row) for row in rows]


def find_by_key_for_user(user_id, event_key):
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT id, user_id, event_key, event_type, titulo, descricao, created_at
            FROM evolution_events
            WHERE user_id = ? AND event_key = ?
            """,
            (user_id, event_key),
        ).fetchone()
        return EvolutionEvent.from_row(row) if row else None
