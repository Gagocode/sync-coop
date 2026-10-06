from dataclasses import dataclass


@dataclass(frozen=True)
class Sector:
    id: int
    organization_id: int
    name: str
    created_at: str
    updated_at: str

    @classmethod
    def from_row(cls, row):
        return cls(
            id=row["id"],
            organization_id=row["organization_id"],
            name=row["name"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    def to_dict(self):
        return {
            "id": self.id,
            "organization_id": self.organization_id,
            "name": self.name,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
