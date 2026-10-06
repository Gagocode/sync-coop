from repositories import mission_repository
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
        "descricao": "Acesse o perfil inicial apos concluir o DISC.",
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
    _ensure_catalog()
    missions = mission_repository.list_by_user_id(user_id)
    if not missions or len(missions) < len(MISSION_CATALOG):
        create_initial_missions_for_user(user_id)
    ensure_available_mission(user_id)
    return mission_repository.list_by_user_id(user_id)


def complete_user_mission_by_key(user_id, mission_key):
    _ensure_catalog()
    mission = mission_repository.find_by_key_for_user(mission_key, user_id)
    if not mission:
        create_initial_missions_for_user(user_id)
        mission = mission_repository.find_by_key_for_user(mission_key, user_id)

    if not mission:
        raise MissionError("Missao nao encontrada")
    if mission.status == "Concluida":
        return mission

    completed_mission = mission_repository.complete_mission(mission.id, user_id)
    record_mission_completed(user_id, completed_mission)
    ensure_available_mission(user_id)
    evaluate_user_achievements(user_id)
    update_observed_disc(user_id)
    return completed_mission


def ensure_available_mission(user_id):
    if not mission_repository.has_available_mission(user_id):
        mission_repository.activate_next_pending_mission(user_id)


def _ensure_catalog():
    mission_repository.sync_catalog(MISSION_CATALOG)


class MissionError(Exception):
    pass
