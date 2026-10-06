from database.connection import get_connection
from models.disc_result import InitialDiscResult, ObservedDiscResult


def save_initial_result(user_id, scores):
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO initial_disc_results
              (user_id, d_score, i_score, s_score, c_score)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                user_id,
                scores["D"],
                scores["I"],
                scores["S"],
                scores["C"],
            ),
        )
        connection.commit()
        return find_initial_result_by_user_id(user_id)


def find_initial_result_by_user_id(user_id):
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT user_id, d_score, i_score, s_score, c_score, created_at
            FROM initial_disc_results
            WHERE user_id = ?
            """,
            (user_id,),
        ).fetchone()
        return InitialDiscResult.from_row(row) if row else None


def upsert_observed_result(user_id, scores):
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO observed_disc_results
              (user_id, d_observed, i_observed, s_observed, c_observed, updated_at)
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(user_id) DO UPDATE SET
              d_observed = excluded.d_observed,
              i_observed = excluded.i_observed,
              s_observed = excluded.s_observed,
              c_observed = excluded.c_observed,
              updated_at = CURRENT_TIMESTAMP
            """,
            (
                user_id,
                scores["D"],
                scores["I"],
                scores["S"],
                scores["C"],
            ),
        )
        connection.commit()
        return find_observed_result_by_user_id(user_id)


def find_observed_result_by_user_id(user_id):
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT user_id, d_observed, i_observed, s_observed, c_observed, updated_at
            FROM observed_disc_results
            WHERE user_id = ?
            """,
            (user_id,),
        ).fetchone()
        return ObservedDiscResult.from_row(row) if row else None
