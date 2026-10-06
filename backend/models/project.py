from dataclasses import dataclass


@dataclass(frozen=True)
class Project:
    id: int
    user_id: int
    titulo: str
    descricao: str
    tecnologias: str
    link: str | None
    created_at: str

    @classmethod
    def from_row(cls, row):
        return cls(
            id=row["id"],
            user_id=row["user_id"],
            titulo=row["titulo"],
            descricao=row["descricao"],
            tecnologias=row["tecnologias"],
            link=row["link"],
            created_at=row["created_at"],
        )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "titulo": self.titulo,
            "descricao": self.descricao,
            "tecnologias": self.tecnologias,
            "link": self.link,
            "created_at": self.created_at,
        }
