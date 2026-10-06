import os
from pathlib import Path
from urllib.parse import urlsplit
from uuid import uuid4

from repositories import professional_profile_repository as repository
from services.activity_service import record_activity


RESUME_DIR = Path(__file__).resolve().parent.parent / "uploads" / "resumes"
MAX_RESUME_BYTES = 5 * 1024 * 1024
TEXT_LIMITS = {
    "biografia": 600,
    "objetivo_profissional": 120,
    "tecnologias_favoritas": 250,
    "cidade": 100,
    "estado_regiao": 100,
}
URL_FIELDS = ("github", "linkedin", "portfolio")


class ProfessionalProfileError(Exception):
    pass


def get_professional_profile(user_id):
    return repository.find_by_user_id(user_id)


def update_professional_profile(user_id, data, resume=None):
    cleaned = {}
    for field, limit in TEXT_LIMITS.items():
        value = (data.get(field) or "").strip()
        if len(value) > limit:
            raise ProfessionalProfileError(f"{field.replace('_', ' ').capitalize()}: máximo de {limit} caracteres")
        cleaned[field] = value or None

    for field in URL_FIELDS:
        value = (data.get(field) or "").strip()
        if value:
            try:
                parts = urlsplit(value)
                valid_url = (
                    len(value) <= 500
                    and parts.scheme in ("http", "https")
                    and parts.hostname
                    and not parts.username
                    and not parts.password
                )
            except ValueError:
                valid_url = False
            if not valid_url:
                raise ProfessionalProfileError(f"Informe uma URL HTTP ou HTTPS válida para {field.capitalize()}")
        cleaned[field] = value or None

    availability = data.get("disponivel_estagio", "")
    if availability not in ("", "sim", "nao"):
        raise ProfessionalProfileError("Disponibilidade para estágio inválida")
    cleaned["disponivel_estagio"] = {"sim": 1, "nao": 0, "": None}[availability]

    current = get_professional_profile(user_id)
    cleaned["curriculo_path"] = current["curriculo_path"]
    if resume and resume.filename:
        if not resume.filename.lower().endswith(".pdf"):
            raise ProfessionalProfileError("O currículo deve ser um arquivo PDF")
        contents = resume.stream.read(MAX_RESUME_BYTES + 1)
        if len(contents) > MAX_RESUME_BYTES:
            raise ProfessionalProfileError("O currículo deve ter até 5 MB")
        if not contents.startswith(b"%PDF-") or b"%%EOF" not in contents[-1024:]:
            raise ProfessionalProfileError("O arquivo enviado não é um PDF válido")
        RESUME_DIR.mkdir(parents=True, exist_ok=True)
        path = RESUME_DIR / f"{user_id}.pdf"
        temporary = RESUME_DIR / f".{user_id}.{uuid4().hex}.tmp"
        try:
            temporary.write_bytes(contents)
            os.replace(temporary, path)
        finally:
            temporary.unlink(missing_ok=True)
        cleaned["curriculo_path"] = path.name
    changed = any(current.get(field) != value for field, value in cleaned.items())
    if not changed and not (resume and resume.filename):
        return current
    saved = repository.save(user_id, cleaned)
    record_activity(user_id)
    return saved


def get_resume_path(user_id):
    profile = get_professional_profile(user_id)
    filename = profile["curriculo_path"]
    if not filename:
        raise ProfessionalProfileError("Currículo não encontrado")
    path = RESUME_DIR / f"{user_id}.pdf"
    if filename != path.name or not path.is_file():
        raise ProfessionalProfileError("Currículo não encontrado")
    return path
