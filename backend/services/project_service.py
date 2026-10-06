from repositories import project_repository
from services.achievement_service import evaluate_user_achievements
from services.evolution_service import record_project_created
from services.mission_service import complete_user_mission_by_key
from services.observed_disc_service import update_observed_disc


class ProjectError(Exception):
    pass


def create_project(user_id, data):
    titulo = _require_text(data.get("titulo"), "Titulo obrigatorio")
    descricao = _require_text(data.get("descricao"), "Descricao obrigatoria")
    tecnologias = _require_text(data.get("tecnologias"), "Tecnologias obrigatorias")
    link = _optional_text(data.get("link"))

    current_project_count = project_repository.count_by_user_id(user_id)
    project = project_repository.create_project(
        user_id=user_id,
        titulo=titulo,
        descricao=descricao,
        tecnologias=tecnologias,
        link=link,
    )
    record_project_created(user_id, project)

    if current_project_count == 0:
        complete_user_mission_by_key(user_id, "first_project")
    elif current_project_count == 1:
        complete_user_mission_by_key(user_id, "second_project")
    elif current_project_count == 2:
        complete_user_mission_by_key(user_id, "third_project")

    evaluate_user_achievements(user_id)
    update_observed_disc(user_id)
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
    deleted = project_repository.delete_project(project_id, user_id)
    if not deleted:
        raise ProjectError("Projeto nao encontrado")
    return True


def _require_text(value, message):
    value = value.strip() if value else ""
    if not value:
        raise ProjectError(message)
    return value


def _optional_text(value):
    value = value.strip() if value else ""
    return value or None
