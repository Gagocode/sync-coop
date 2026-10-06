from dataclasses import dataclass


@dataclass(frozen=True)
class Achievement:
    id: int
    achievement_key: str
    nome: str
    descricao: str

    @classmethod
    def from_row(cls, row):
        return cls(
            id=row["id"],
            achievement_key=row["achievement_key"],
            nome=row["nome"],
            descricao=row["descricao"],
        )


@dataclass(frozen=True)
class UserAchievement:
    id: int
    user_id: int
    achievement_key: str
    nome: str
    descricao: str
    data_desbloqueio: str

    @classmethod
    def from_row(cls, row):
        return cls(
            id=row["id"],
            user_id=row["user_id"],
            achievement_key=row["achievement_key"],
            nome=row["nome"],
            descricao=row["descricao"],
            data_desbloqueio=row["data_desbloqueio"],
        )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "achievement_key": self.achievement_key,
            "nome": self.nome,
            "descricao": self.descricao,
            "data_desbloqueio": self.data_desbloqueio,
        }
