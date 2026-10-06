from dataclasses import dataclass


@dataclass(frozen=True)
class EvolutionEvent:
    id: int
    user_id: int
    event_key: str
    event_type: str
    titulo: str
    descricao: str
    created_at: str

    @classmethod
    def from_row(cls, row):
        return cls(
            id=row["id"],
            user_id=row["user_id"],
            event_key=row["event_key"],
            event_type=row["event_type"],
            titulo=row["titulo"],
            descricao=row["descricao"],
            created_at=row["created_at"],
        )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "event_key": self.event_key,
            "event_type": self.event_type,
            "titulo": self.titulo,
            "descricao": self.descricao,
            "created_at": self.created_at,
        }
