from database.connection import get_connection


FIELDS = (
    "biografia", "objetivo_profissional", "tecnologias_favoritas", "github",
    "linkedin", "portfolio", "cidade", "estado_regiao", "disponivel_estagio",
    "curriculo_path",
)


def find_by_user_id(user_id):
    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM professional_profiles WHERE user_id = ?", (user_id,)
        ).fetchone()
    return dict(row) if row else {field: None for field in FIELDS}


def save(user_id, data):
    values = [data.get(field) for field in FIELDS]
    columns = ", ".join(FIELDS)
    placeholders = ", ".join("?" for _ in FIELDS)
    updates = ", ".join(f"{field} = excluded.{field}" for field in FIELDS)
    with get_connection() as connection:
        connection.execute(
            f"INSERT INTO professional_profiles (user_id, {columns}) "
            f"VALUES (?, {placeholders}) ON CONFLICT(user_id) DO UPDATE SET {updates}",
            (user_id, *values),
        )
        connection.commit()
    return find_by_user_id(user_id)
