from database.connection import get_connection
from models.mission import Mission, MissionCatalogItem


def sync_catalog(catalog):
    with get_connection() as connection:
        for mission in catalog:
            connection.execute(
                """
                INSERT INTO missions
                  (mission_key, nome, descricao, xp_recompensa, ordem, tipo_evento)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(mission_key) DO UPDATE SET
                  nome = excluded.nome,
                  descricao = excluded.descricao,
                  xp_recompensa = excluded.xp_recompensa,
                  ordem = excluded.ordem,
                  tipo_evento = excluded.tipo_evento
                """,
                (
                    mission["key"], mission["nome"], mission["descricao"],
                    mission["xp_recompensa"], mission["ordem"], mission["tipo_evento"],
                ),
            )
        connection.commit()


def list_catalog():
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT id, mission_key, nome, descricao, xp_recompensa, ordem, tipo_evento
            FROM missions ORDER BY ordem
            """
        ).fetchall()
        return [MissionCatalogItem.from_row(row) for row in rows]


def create_user_missions(user_id, missions):
    with get_connection() as connection:
        connection.executemany(
            """
            INSERT OR IGNORE INTO user_missions
              (user_id, mission_key, nome, descricao, status, xp_recompensa)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    user_id, mission["key"], mission["nome"], mission["descricao"],
                    mission["status"], mission["xp_recompensa"],
                )
                for mission in missions
            ],
        )
        connection.commit()
        return list_by_user_id(user_id)


def list_by_user_id(user_id):
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT um.id, um.user_id, um.mission_key, um.nome, um.descricao,
                   um.status, um.xp_recompensa, um.data_conclusao, um.created_at,
                   m.ordem, m.tipo_evento
            FROM user_missions um
            LEFT JOIN missions m ON m.mission_key = um.mission_key
            WHERE um.user_id = ?
            ORDER BY COALESCE(m.ordem, um.id)
            """,
            (user_id,),
        ).fetchall()
        return [Mission.from_row(row) for row in rows]


def find_by_id_for_user(mission_id, user_id):
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT um.id, um.user_id, um.mission_key, um.nome, um.descricao,
                   um.status, um.xp_recompensa, um.data_conclusao, um.created_at,
                   m.ordem, m.tipo_evento
            FROM user_missions um
            LEFT JOIN missions m ON m.mission_key = um.mission_key
            WHERE um.id = ? AND um.user_id = ?
            """,
            (mission_id, user_id),
        ).fetchone()
        return Mission.from_row(row) if row else None


def find_by_key_for_user(mission_key, user_id):
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT um.id, um.user_id, um.mission_key, um.nome, um.descricao,
                   um.status, um.xp_recompensa, um.data_conclusao, um.created_at,
                   m.ordem, m.tipo_evento
            FROM user_missions um
            LEFT JOIN missions m ON m.mission_key = um.mission_key
            WHERE um.mission_key = ? AND um.user_id = ?
            """,
            (mission_key, user_id),
        ).fetchone()
        return Mission.from_row(row) if row else None


def complete_mission(mission_id, user_id):
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT um.id, um.user_id, um.mission_key, um.nome, um.descricao,
                   um.status, um.xp_recompensa, um.data_conclusao, um.created_at,
                   m.ordem, m.tipo_evento
            FROM user_missions um
            LEFT JOIN missions m ON m.mission_key = um.mission_key
            WHERE um.id = ? AND um.user_id = ?
            """,
            (mission_id, user_id),
        ).fetchone()
        if not row:
            return None

        mission = Mission.from_row(row)
        if mission.status == "Concluida":
            return mission

        update = connection.execute(
            """
            UPDATE user_missions
            SET status = 'Concluida', data_conclusao = CURRENT_TIMESTAMP
            WHERE id = ? AND user_id = ? AND status != 'Concluida'
            """,
            (mission_id, user_id),
        )
        if update.rowcount == 1:
            connection.execute(
                "UPDATE users SET xp = xp + ? WHERE id = ?",
                (mission.xp_recompensa, user_id),
            )
        connection.commit()

    return find_by_id_for_user(mission_id, user_id)


def has_available_mission(user_id):
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT 1 FROM user_missions
            WHERE user_id = ? AND status = 'Pendente'
            LIMIT 1
            """,
            (user_id,),
        ).fetchone()
        return row is not None


def activate_next_pending_mission(user_id):
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT um.id
            FROM user_missions um
            LEFT JOIN missions m ON m.mission_key = um.mission_key
            WHERE um.user_id = ? AND um.status = 'Bloqueada'
            ORDER BY COALESCE(m.ordem, um.id)
            LIMIT 1
            """,
            (user_id,),
        ).fetchone()
        if not row:
            return None

        connection.execute(
            "UPDATE user_missions SET status = 'Pendente' WHERE id = ?",
            (row["id"],),
        )
        connection.commit()
        return find_by_id_for_user(row["id"], user_id)
