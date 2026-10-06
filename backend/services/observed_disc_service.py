from repositories import achievement_repository
from repositories import certificate_repository
from repositories import disc_repository
from repositories import mission_repository
from repositories import project_repository


PROJECT_D_WEIGHT = 10
CERTIFICATE_C_WEIGHT = 10
COMPLETED_MISSION_S_WEIGHT = 5
ACHIEVEMENT_I_WEIGHT = 5


def get_observed_disc_result(user_id):
    result = update_observed_disc(user_id)
    return build_observed_summary(result)


def update_observed_disc(user_id):
    scores = calculate_observed_scores(user_id)
    return disc_repository.upsert_observed_result(user_id, scores)


def calculate_observed_scores(user_id):
    project_count = project_repository.count_by_user_id(user_id)
    certificate_count = certificate_repository.count_by_user_id(user_id)
    completed_missions_count = len(
        [
            mission
            for mission in mission_repository.list_by_user_id(user_id)
            if mission.status == "Concluida"
        ]
    )
    achievements_count = len(achievement_repository.list_unlocked_by_user_id(user_id))

    return {
        "D": project_count * PROJECT_D_WEIGHT,
        "I": achievements_count * ACHIEVEMENT_I_WEIGHT,
        "S": completed_missions_count * COMPLETED_MISSION_S_WEIGHT,
        "C": certificate_count * CERTIFICATE_C_WEIGHT,
    }


def build_observed_summary(result):
    scores = {
        "D": result.d_observed,
        "I": result.i_observed,
        "S": result.s_observed,
        "C": result.c_observed,
    }
    total = sum(scores.values())
    percentages = {
        dimension: round((score / total) * 100) if total else 0
        for dimension, score in scores.items()
    }
    predominant_dimension = max(scores, key=scores.get) if total else None

    return {
        "user_id": result.user_id,
        "scores": scores,
        "total": total,
        "percentages": percentages,
        "predominant_dimension": predominant_dimension,
        "updated_at": result.updated_at,
        "rules": {
            "projects": f"+{PROJECT_D_WEIGHT} D por projeto cadastrado",
            "certificates": f"+{CERTIFICATE_C_WEIGHT} C por certificado cadastrado",
            "missions": f"+{COMPLETED_MISSION_S_WEIGHT} S por missao concluida",
            "achievements": f"+{ACHIEVEMENT_I_WEIGHT} I por conquista desbloqueada",
        },
    }
