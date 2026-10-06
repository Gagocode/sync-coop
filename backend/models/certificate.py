from dataclasses import dataclass


@dataclass(frozen=True)
class Certificate:
    id: int
    user_id: int
    nome: str
    instituicao: str
    carga_horaria: int
    data_conclusao: str
    arquivo_path: str | None
    created_at: str

    @classmethod
    def from_row(cls, row):
        return cls(
            id=row["id"],
            user_id=row["user_id"],
            nome=row["nome"],
            instituicao=row["instituicao"],
            carga_horaria=row["carga_horaria"],
            data_conclusao=row["data_conclusao"],
            arquivo_path=row["arquivo_path"],
            created_at=row["created_at"],
        )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "nome": self.nome,
            "instituicao": self.instituicao,
            "carga_horaria": self.carga_horaria,
            "data_conclusao": self.data_conclusao,
            "arquivo_path": self.arquivo_path,
            "created_at": self.created_at,
        }
