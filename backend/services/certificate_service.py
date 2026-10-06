from pathlib import Path
from uuid import uuid4

from werkzeug.utils import secure_filename

from repositories import certificate_repository
from services.achievement_service import evaluate_user_achievements
from services.evolution_service import record_certificate_created
from services.mission_service import complete_user_mission_by_key
from services.observed_disc_service import update_observed_disc


UPLOAD_ROOT = Path(__file__).resolve().parent.parent / "uploads"
CERTIFICATE_UPLOAD_DIR = UPLOAD_ROOT / "certificates"


class CertificateError(Exception):
    pass


def create_certificate(user_id, data, file_storage=None):
    nome = _require_text(data.get("nome"), "Nome obrigatorio")
    instituicao = _require_text(data.get("instituicao"), "Instituicao obrigatoria")
    carga_horaria = _parse_carga_horaria(data.get("carga_horaria"))
    data_conclusao = _require_text(data.get("data_conclusao"), "Data de conclusao obrigatoria")
    arquivo_path = _save_file(file_storage)

    current_certificate_count = certificate_repository.count_by_user_id(user_id)
    certificate = certificate_repository.create_certificate(
        user_id=user_id,
        nome=nome,
        instituicao=instituicao,
        carga_horaria=carga_horaria,
        data_conclusao=data_conclusao,
        arquivo_path=arquivo_path,
    )
    record_certificate_created(user_id, certificate)

    if current_certificate_count == 0:
        complete_user_mission_by_key(user_id, "first_certificate")
    elif current_certificate_count == 1:
        complete_user_mission_by_key(user_id, "second_certificate")
    elif current_certificate_count == 2:
        complete_user_mission_by_key(user_id, "third_certificate")

    evaluate_user_achievements(user_id)
    update_observed_disc(user_id)
    return certificate


def list_certificates(user_id):
    return certificate_repository.list_by_user_id(user_id)


def get_certificate(user_id, certificate_id):
    certificate = certificate_repository.find_by_id_for_user(certificate_id, user_id)
    if not certificate:
        raise CertificateError("Certificado nao encontrado")
    return certificate


def update_certificate(user_id, certificate_id, data, file_storage=None):
    certificate = get_certificate(user_id, certificate_id)
    nome = _require_text(data.get("nome"), "Nome obrigatorio")
    instituicao = _require_text(data.get("instituicao"), "Instituicao obrigatoria")
    carga_horaria = _parse_carga_horaria(data.get("carga_horaria"))
    data_conclusao = _require_text(data.get("data_conclusao"), "Data de conclusao obrigatoria")
    arquivo_path = _save_file(file_storage) or certificate.arquivo_path

    return certificate_repository.update_certificate(
        certificate_id=certificate_id,
        user_id=user_id,
        nome=nome,
        instituicao=instituicao,
        carga_horaria=carga_horaria,
        data_conclusao=data_conclusao,
        arquivo_path=arquivo_path,
    )


def delete_certificate(user_id, certificate_id):
    deleted = certificate_repository.delete_certificate(certificate_id, user_id)
    if not deleted:
        raise CertificateError("Certificado nao encontrado")
    return True


def get_certificate_file_path(certificate):
    if not certificate.arquivo_path:
        raise CertificateError("Certificado sem arquivo")

    relative_path = Path(certificate.arquivo_path)
    file_path = UPLOAD_ROOT / relative_path.relative_to("uploads")
    if not file_path.exists():
        raise CertificateError("Arquivo nao encontrado")
    return file_path


def _save_file(file_storage):
    if not file_storage or not file_storage.filename:
        return None

    CERTIFICATE_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    original_name = secure_filename(file_storage.filename)
    if not original_name:
        raise CertificateError("Nome de arquivo invalido")

    filename = f"{uuid4().hex}_{original_name}"
    file_path = CERTIFICATE_UPLOAD_DIR / filename
    file_storage.save(file_path)
    return f"uploads/certificates/{filename}"


def _parse_carga_horaria(value):
    value = _require_text(value, "Carga horaria obrigatoria")
    try:
        carga_horaria = int(value)
    except ValueError as error:
        raise CertificateError("Carga horaria invalida") from error
    if carga_horaria <= 0:
        raise CertificateError("Carga horaria deve ser maior que zero")
    return carga_horaria


def _require_text(value, message):
    value = value.strip() if value else ""
    if not value:
        raise CertificateError(message)
    return value
