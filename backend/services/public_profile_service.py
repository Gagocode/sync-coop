from repositories import user_repository
from services.achievement_service import get_user_achievements
from services.certificate_service import list_certificates
from services.disc_service import get_initial_disc_result
from services.evolution_service import get_user_evolution
from services.observed_disc_service import get_observed_disc_result
from services.profile_service import calculate_initial_class
from services.project_service import list_projects
from services.professional_profile_service import get_professional_profile


class PublicProfileError(Exception):
    pass


def get_public_profile(user_id):
    user = user_repository.find_public_by_id(user_id)
    if not user:
        raise PublicProfileError("Perfil publico nao encontrado")

    disc_result = get_initial_disc_result(user_id)
    if disc_result:
        classe = calculate_initial_class(disc_result["predominant_dimension"])
        if user.classe != classe:
            user = user_repository.update_profile_class(user_id, classe)

    projects = list_projects(user_id)
    certificates = list_certificates(user_id)
    achievements = get_user_achievements(user_id)
    evolution = get_user_evolution(
        user_id,
        user=user,
        projects=projects,
        certificates=certificates,
        achievements=achievements,
    )

    return {
        "user": user,
        "professional_profile": get_professional_profile(user_id),
        "disc_result": disc_result,
        "observed_disc_result": get_observed_disc_result(user_id),
        "projects": projects,
        "certificates": certificates,
        "achievements": achievements,
        "evolution": evolution,
        "indicators": {
            "projects_count": len(projects),
            "certificates_count": len(certificates),
            "missions_completed": evolution["indicators"]["missions_completed"],
            "achievements_unlocked": achievements["unlocked_count"],
            "xp_total": user.xp,
        },
    }


def get_public_profile_by_name(nome):
    matches = user_repository.find_public_by_name(nome)
    if not matches:
        raise PublicProfileError("Perfil publico nao encontrado")
    if len(matches) > 1:
        raise PublicProfileError("Este nome corresponde a mais de um perfil")
    return get_public_profile(matches[0].id)
