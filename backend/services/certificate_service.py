from pathlib import Path
from uuid import uuid4

from werkzeug.utils import secure_filename

from database.connection import transaction
from repositories import certificate_repository
from services.evolution_service import record_certificate_created
from services.mission_service import complete_missions_for_event
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
    arquivo_path = None
    try:
        with transaction():
            arquivo_path = _save_file(file_storage)
            certificate = certificate_repository.create_certificate(
                user_id=user_id, nome=nome, instituicao=instituicao,
                carga_horaria=carga_horaria, data_conclusao=data_conclusao,
                arquivo_path=arquivo_path,
            )
            record_certificate_created(user_id, certificate)
            complete_missions_for_event(user_id, "CERTIFICATE_CREATED")
            return certificate
    except Exception:
        _remove_new_file(arquivo_path)
        raise


def list_certificates(user_id):
    return certificate_repository.list_by_user_id(user_id)


def get_certificate(user_id, certificate_id):
    certificate = certificate_repository.find_by_id_for_user(certificate_id, user_id)
    if not certificate:
        raise CertificateError("Certificado nao encontrado")
    return certificate


def update_certificate(user_id, certificate_id, data, file_storage=None):
    nome = _require_text(data.get("nome"), "Nome obrigatorio")
    instituicao = _require_text(data.get("instituicao"), "Instituicao obrigatoria")
    carga_horaria = _parse_carga_horaria(data.get("carga_horaria"))
    data_conclusao = _require_text(data.get("data_conclusao"), "Data de conclusao obrigatoria")
    new_file = None
    try:
        with transaction():
            certificate = get_certificate(user_id, certificate_id)
            new_file = _save_file(file_storage)
            return certificate_repository.update_certificate(
                certificate_id=certificate_id, user_id=user_id,
                nome=nome, instituicao=instituicao,
                carga_horaria=carga_horaria, data_conclusao=data_conclusao,
                arquivo_path=new_file or certificate.arquivo_path,
            )
    except Exception:
        _remove_new_file(new_file)
        raise


def delete_certificate(user_id, certificate_id):
    with transaction():
        deleted = certificate_repository.delete_certificate(certificate_id, user_id)
        if not deleted:
            raise CertificateError("Certificado nao encontrado")
        update_observed_disc(user_id)
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
    try:
        file_storage.save(file_path)
    except Exception:
        file_path.unlink(missing_ok=True)
        raise
    return f"uploads/certificates/{filename}"


def _remove_new_file(arquivo_path):
    if arquivo_path:
        (UPLOAD_ROOT / Path(arquivo_path).relative_to("uploads")).unlink(missing_ok=True)


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
