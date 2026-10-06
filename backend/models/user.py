from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    id: int
    nome: str
    email: str
    senha_hash: str
    curso: str | None
    classe: str | None
    xp: int
    created_at: str
    organization_id: int | None
    sector_id: int | None
    role: str | None
    organization_name: str | None
    sector_name: str | None
    last_activity_at: str | None = None

    @classmethod
    def from_row(cls, row):
        return cls(
            id=row["id"],
            nome=row["nome"],
            email=row["email"],
            senha_hash=row["senha_hash"],
            curso=row["curso"],
            classe=row["classe"],
            xp=row["xp"],
            created_at=row["created_at"],
            organization_id=row["organization_id"],
            sector_id=row["sector_id"],
            role=row["role"],
            organization_name=row["organization_name"],
            sector_name=row["sector_name"],
            last_activity_at=row["last_activity_at"],
        )

    def to_public_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "curso": self.curso,
            "classe": self.classe,
            "xp": self.xp,
            "created_at": self.created_at,
            "organization_id": self.organization_id,
            "sector_id": self.sector_id,
            "role": self.role,
            "organization_name": self.organization_name,
            "sector_name": self.sector_name,
        }
