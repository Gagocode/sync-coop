from database.connection import transaction
from repositories import project_repository
from services.evolution_service import record_project_created
from services.mission_service import complete_missions_for_event
from services.observed_disc_service import update_observed_disc


class ProjectError(Exception):
    pass


def create_project(user_id, data):
    titulo = _require_text(data.get("titulo"), "Titulo obrigatorio")
    descricao = _require_text(data.get("descricao"), "Descricao obrigatoria")
    tecnologias = _require_text(data.get("tecnologias"), "Tecnologias obrigatorias")
    link = _optional_text(data.get("link"))

    with transaction():
        project = project_repository.create_project(
            user_id=user_id, titulo=titulo, descricao=descricao,
            tecnologias=tecnologias, link=link,
        )
        record_project_created(user_id, project)
        complete_missions_for_event(user_id, "PROJECT_CREATED")
        return project


def list_projects(user_id):
    return project_repository.list_by_user_id(user_id)


def get_project(user_id, project_id):
    project = project_repository.find_by_id_for_user(project_id, user_id)
    if not project:
        raise ProjectError("Projeto nao encontrado")
    return project


def update_project(user_id, project_id, data):
    get_project(user_id, project_id)
    titulo = _require_text(data.get("titulo"), "Titulo obrigatorio")
    descricao = _require_text(data.get("descricao"), "Descricao obrigatoria")
    tecnologias = _require_text(data.get("tecnologias"), "Tecnologias obrigatorias")
    link = _optional_text(data.get("link"))
    return project_repository.update_project(
        project_id=project_id,
        user_id=user_id,
        titulo=titulo,
        descricao=descricao,
        tecnologias=tecnologias,
        link=link,
    )


def delete_project(user_id, project_id):
    with transaction():
        deleted = project_repository.delete_project(project_id, user_id)
        if not deleted:
            raise ProjectError("Projeto nao encontrado")
        update_observed_disc(user_id)
        return True


def _require_text(value, message):
    value = value.strip() if value else ""
    if not value:
        raise ProjectError(message)
    return value


def _optional_text(value):
    value = value.strip() if value else ""
    return value or None
