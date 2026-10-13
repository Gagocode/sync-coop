from repositories import user_repository
from services.achievement_service import get_user_achievements
from services.certificate_service import list_certificates
from services.disc_service import get_initial_disc_result
from services.evolution_service import get_user_evolution
from services.observed_disc_service import get_observed_disc_result
from services.project_service import list_projects


def get_profile(user_id):
    user = user_repository.find_by_id(user_id)
    disc_result = get_initial_disc_result(user_id)

    projects = list_projects(user_id)
    certificates = list_certificates(user_id)
    achievements = get_user_achievements(user_id)

    return {
        "user": user,
        "disc_result": disc_result,
        "projects": projects,
        "certificates": certificates,
        "achievements": achievements,
        "observed_disc_result": get_observed_disc_result(user_id),
        "evolution": get_user_evolution(
            user_id,
            user=user,
            projects=projects,
            certificates=certificates,
            achievements=achievements,
        ),
    }
