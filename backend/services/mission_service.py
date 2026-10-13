from database.connection import transaction
from repositories import certificate_repository, disc_repository, mission_repository
from repositories import project_repository, user_repository
from services.achievement_service import evaluate_user_achievements
from services.evolution_service import record_mission_completed
from services.observed_disc_service import update_observed_disc


MISSION_CATALOG = [
    {
        "key": "complete_disc_quiz", "nome": "Realizar DISC Inicial",
        "descricao": "Responda o quiz narrativo para gerar seu DISC Inicial.",
        "xp_recompensa": 100, "ordem": 10, "tipo_evento": "DISC_COMPLETED",
    },
    {
        "key": "complete_profile", "nome": "Completar Perfil",
        "descricao": "Gere seu perfil inicial apos concluir o DISC.",
        "xp_recompensa": 50, "ordem": 20, "tipo_evento": "PROFILE_COMPLETED",
    },
    {
        "key": "first_project", "nome": "Adicionar Primeiro Projeto",
        "descricao": "Registre seu primeiro projeto no Curriculo Vivo.",
        "xp_recompensa": 150, "ordem": 30, "tipo_evento": "PROJECT_CREATED",
    },
    {
        "key": "second_project", "nome": "Adicionar Segundo Projeto",
        "descricao": "Registre seu segundo projeto no Curriculo Vivo.",
        "xp_recompensa": 150, "ordem": 40, "tipo_evento": "PROJECT_CREATED",
    },
    {
        "key": "third_project", "nome": "Adicionar Terceiro Projeto",
        "descricao": "Registre seu terceiro projeto no Curriculo Vivo.",
        "xp_recompensa": 150, "ordem": 50, "tipo_evento": "PROJECT_CREATED",
    },
    {
        "key": "first_certificate", "nome": "Adicionar Primeiro Certificado",
        "descricao": "Registre seu primeiro certificado no Curriculo Vivo.",
        "xp_recompensa": 150, "ordem": 60, "tipo_evento": "CERTIFICATE_CREATED",
    },
    {
        "key": "second_certificate", "nome": "Adicionar Segundo Certificado",
        "descricao": "Registre seu segundo certificado no Curriculo Vivo.",
        "xp_recompensa": 150, "ordem": 70, "tipo_evento": "CERTIFICATE_CREATED",
    },
    {
        "key": "third_certificate", "nome": "Adicionar Terceiro Certificado",
        "descricao": "Registre seu terceiro certificado no Curriculo Vivo.",
        "xp_recompensa": 150, "ordem": 80, "tipo_evento": "CERTIFICATE_CREATED",
    },
    {
        "key": "continue_evolution", "nome": "Continuar Evolucao",
        "descricao": "Continue adicionando evidencias ao Curriculo Vivo.",
        "xp_recompensa": 0, "ordem": 90, "tipo_evento": "CONTINUE_EVOLUTION",
    },
]


def create_initial_missions_for_user(user_id):
    with transaction():
        _ensure_catalog()
        existing = mission_repository.list_by_user_id(user_id)
        has_available = any(mission.status == "Pendente" for mission in existing)
        missions = [
            {
                **mission,
                "status": "Pendente" if index == 0 and not has_available else "Bloqueada",
            }
            for index, mission in enumerate(MISSION_CATALOG)
        ]
        mission_repository.create_user_missions(user_id, missions)
        ensure_available_mission(user_id)
        return mission_repository.list_by_user_id(user_id)


def get_user_missions(user_id):
    return mission_repository.list_by_user_id(user_id)


def complete_user_mission_by_key(user_id, mission_key):
    with transaction():
        mission = mission_repository.find_by_key_for_user(mission_key, user_id)
        if not mission:
            raise MissionError("Missao nao encontrada")
        if mission.status == "Concluida":
            return mission
        if not _condition_met(user_id, mission, mission_repository.list_by_user_id(user_id)):
            raise MissionError("Condicao da missao ainda nao atendida")
        completed = _complete_mission(user_id, mission)
        evaluate_user_achievements(user_id)
        update_observed_disc(user_id)
        return completed


def complete_missions_for_event(user_id, event_type):
    """Apply catalog missions whose event and evidence match the completed action."""
    with transaction():
        missions = mission_repository.list_by_user_id(user_id)
        if not missions:
            missions = create_initial_missions_for_user(user_id)
        completed = []
        for mission in missions:
            if (mission.tipo_evento == event_type
                    and mission.status != "Concluida"
                    and _condition_met(user_id, mission, missions)):
                completed.append(_complete_mission(user_id, mission))
        evaluate_user_achievements(user_id)
        update_observed_disc(user_id)
        return completed


def _complete_mission(user_id, mission):
    completed = mission_repository.complete_mission(mission.id, user_id)
    record_mission_completed(user_id, completed)
    ensure_available_mission(user_id)
    return completed


def _condition_met(user_id, mission, missions):
    event_type = mission.tipo_evento
    if event_type == "DISC_COMPLETED":
        count = int(disc_repository.find_initial_result_by_user_id(user_id) is not None)
    elif event_type == "PROFILE_COMPLETED":
        user = user_repository.find_by_id(user_id)
        count = int(bool(user and user.classe and disc_repository.find_initial_result_by_user_id(user_id)))
    elif event_type == "PROJECT_CREATED":
        count = project_repository.count_by_user_id(user_id)
    elif event_type == "CERTIFICATE_CREATED":
        count = certificate_repository.count_by_user_id(user_id)
    else:
        # CONTINUE_EVOLUTION has no documented completion threshold.
        return False
    same_event = [item for item in missions if item.tipo_evento == event_type]
    required_count = next(
        (index for index, item in enumerate(same_event, start=1)
         if item.mission_key == mission.mission_key),
        None,
    )
    return required_count is not None and count >= required_count


def ensure_available_mission(user_id):
    if not mission_repository.has_available_mission(user_id):
        mission_repository.activate_next_pending_mission(user_id)


def _ensure_catalog():
    mission_repository.sync_catalog(MISSION_CATALOG)


class MissionError(Exception):
    pass
