from dataclasses import dataclass


@dataclass(frozen=True)
class MissionCatalogItem:
    id: int
    mission_key: str
    nome: str
    descricao: str
    xp_recompensa: int
    ordem: int
    tipo_evento: str

    @classmethod
    def from_row(cls, row):
        return cls(
            id=row["id"],
            mission_key=row["mission_key"],
            nome=row["nome"],
            descricao=row["descricao"],
            xp_recompensa=row["xp_recompensa"],
            ordem=row["ordem"],
            tipo_evento=row["tipo_evento"],
        )


@dataclass(frozen=True)
class Mission:
    id: int
    user_id: int
    mission_key: str
    nome: str
    descricao: str
    status: str
    xp_recompensa: int
    data_conclusao: str | None
    created_at: str
    ordem: int | None = None
    tipo_evento: str | None = None

    @classmethod
    def from_row(cls, row):
        return cls(
            id=row["id"],
            user_id=row["user_id"],
            mission_key=row["mission_key"],
            nome=row["nome"],
            descricao=row["descricao"],
            status=row["status"],
            xp_recompensa=row["xp_recompensa"],
            data_conclusao=row["data_conclusao"],
            created_at=row["created_at"],
            ordem=row["ordem"] if "ordem" in row.keys() else None,
            tipo_evento=row["tipo_evento"] if "tipo_evento" in row.keys() else None,
        )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "mission_key": self.mission_key,
            "nome": self.nome,
            "descricao": self.descricao,
            "status": self.status,
            "xp_recompensa": self.xp_recompensa,
            "data_conclusao": self.data_conclusao,
            "created_at": self.created_at,
            "ordem": self.ordem,
            "tipo_evento": self.tipo_evento,
        }
