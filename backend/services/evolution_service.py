from repositories import achievement_repository
from repositories import certificate_repository
from repositories import disc_repository
from repositories import evolution_repository
from repositories import mission_repository
from repositories import project_repository
from repositories import user_repository


LEVEL_THRESHOLDS = [
    {"level": 1, "xp": 0},
    {"level": 2, "xp": 200},
    {"level": 3, "xp": 500},
    {"level": 4, "xp": 900},
    {"level": 5, "xp": 1400},
]


def get_user_evolution(user_id, user=None, projects=None, certificates=None, achievements=None):
    user = user or user_repository.find_by_id(user_id)
    projects = projects if projects is not None else project_repository.list_by_user_id(user_id)
    certificates = (
        certificates
        if certificates is not None
        else certificate_repository.list_by_user_id(user_id)
    )
    unlocked_achievements = (
        achievements["unlocked"]
        if achievements is not None
        else achievement_repository.list_unlocked_by_user_id(user_id)
    )
    missions = mission_repository.list_by_user_id(user_id)
    completed_missions = [
        mission for mission in missions if mission.status == "Concluida"
    ]

    _ensure_history_for_current_state(
        user_id=user_id,
        projects=projects,
        certificates=certificates,
        completed_missions=completed_missions,
        unlocked_achievements=unlocked_achievements,
    )

    return {
        "level": calculate_level(user.xp),
        "indicators": {
            "xp_current": user.xp,
            "missions_completed": len(completed_missions),
            "projects_created": len(projects),
            "certificates_added": len(certificates),
            "achievements_unlocked": len(unlocked_achievements),
        },
        "history": evolution_repository.list_recent_by_user_id(user_id),
    }


def calculate_level(xp):
    current_threshold = LEVEL_THRESHOLDS[0]
    next_threshold = None

    for index, threshold in enumerate(LEVEL_THRESHOLDS):
        if xp >= threshold["xp"]:
            current_threshold = threshold
            next_threshold = (
                LEVEL_THRESHOLDS[index + 1]
                if index + 1 < len(LEVEL_THRESHOLDS)
                else None
            )

    if not next_threshold:
        return {
            "current": current_threshold["level"],
            "current_min_xp": current_threshold["xp"],
            "next": None,
            "next_min_xp": None,
            "xp_to_next": 0,
            "progress_percent": 100,
        }

    interval = next_threshold["xp"] - current_threshold["xp"]
    progress_xp = xp - current_threshold["xp"]
    progress_percent = round((progress_xp / interval) * 100) if interval else 100

    return {
        "current": current_threshold["level"],
        "current_min_xp": current_threshold["xp"],
        "next": next_threshold["level"],
        "next_min_xp": next_threshold["xp"],
        "xp_to_next": max(next_threshold["xp"] - xp, 0),
        "progress_percent": min(max(progress_percent, 0), 100),
    }


def record_disc_completed(user_id, created_at=None):
    return evolution_repository.create_event(
        user_id=user_id,
        event_key="disc_completed",
        event_type="DISC_COMPLETED",
        titulo="DISC concluido",
        descricao="Voce concluiu o DISC Inicial.",
        created_at=created_at,
    )


def record_mission_completed(user_id, mission):
    return evolution_repository.create_event(
        user_id=user_id,
        event_key=f"mission_completed:{mission.mission_key}",
        event_type="MISSION_COMPLETED",
        titulo="Missao concluida",
        descricao=mission.nome,
        created_at=mission.data_conclusao,
    )


def record_project_created(user_id, project):
    return evolution_repository.create_event(
        user_id=user_id,
        event_key=f"project_created:{project.id}",
        event_type="PROJECT_CREATED",
        titulo="Projeto criado",
        descricao=project.titulo,
        created_at=project.created_at,
    )


def record_certificate_created(user_id, certificate):
    return evolution_repository.create_event(
        user_id=user_id,
        event_key=f"certificate_created:{certificate.id}",
        event_type="CERTIFICATE_CREATED",
        titulo="Certificado criado",
        descricao=certificate.nome,
        created_at=certificate.created_at,
    )


def record_achievement_unlocked(user_id, achievement):
    return evolution_repository.create_event(
        user_id=user_id,
        event_key=f"achievement_unlocked:{achievement.achievement_key}",
        event_type="ACHIEVEMENT_UNLOCKED",
        titulo="Conquista desbloqueada",
        descricao=achievement.nome,
        created_at=achievement.data_desbloqueio,
    )


def _ensure_history_for_current_state(
    user_id,
    projects,
    certificates,
    completed_missions,
    unlocked_achievements,
):
    disc_result = disc_repository.find_initial_result_by_user_id(user_id)
    if disc_result:
        record_disc_completed(user_id, disc_result.created_at)

    for mission in completed_missions:
        record_mission_completed(user_id, mission)

    for project in projects:
        record_project_created(user_id, project)

    for certificate in certificates:
        record_certificate_created(user_id, certificate)

    for achievement in unlocked_achievements:
        record_achievement_unlocked(user_id, achievement)
