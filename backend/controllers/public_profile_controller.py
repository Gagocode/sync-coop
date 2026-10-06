from flask import Blueprint, jsonify, render_template, send_file

from services.public_profile_service import (
    PublicProfileError,
    get_public_profile,
    get_public_profile_by_name,
)
from services.professional_profile_service import ProfessionalProfileError, get_resume_path


public_profile_bp = Blueprint("public_profile", __name__, url_prefix="/profile")
public_profile_name_bp = Blueprint(
    "public_profile_name", __name__, url_prefix="/perfil"
)


def _render_public_profile(profile):
    return render_template(
        "perfil_publico.html",
        user=profile["user"],
        disc_result=profile["disc_result"],
        projects=profile["projects"],
        certificates=profile["certificates"],
        achievements=profile["achievements"],
        evolution=profile["evolution"],
        indicators=profile["indicators"],
        observed_disc_result=profile["observed_disc_result"],
        professional_profile=profile["professional_profile"],
    )


@public_profile_bp.get("/<int:user_id>")
def public_profile_page(user_id):
    try:
        profile = get_public_profile(user_id)
    except PublicProfileError as error:
        return str(error), 404

    return _render_public_profile(profile)


@public_profile_name_bp.get("/<path:username>")
def public_profile_by_name_page(username):
    try:
        profile = get_public_profile_by_name(username)
    except PublicProfileError as error:
        status_code = (
            409
            if str(error) == "Este nome corresponde a mais de um perfil"
            else 404
        )
        return str(error), status_code

    return _render_public_profile(profile)


@public_profile_bp.get("/<int:user_id>/json")
def public_profile_json(user_id):
    try:
        profile = get_public_profile(user_id)
    except PublicProfileError as error:
        return jsonify({"error": str(error)}), 404

    user = profile["user"]
    return jsonify(
        {
            "user": {
                "id": user.id,
                "nome": user.nome,
                "curso": user.curso,
                "sector_name": user.sector_name,
                "classe": user.classe,
                "xp": user.xp,
            },
            "disc_result": profile["disc_result"],
            "observed_disc_result": profile["observed_disc_result"],
            "projects": [project.to_dict() for project in profile["projects"]],
            "certificates": [
                certificate.to_dict() for certificate in profile["certificates"]
            ],
            "achievements": {
                "unlocked": [
                    achievement.to_dict()
                    for achievement in profile["achievements"]["unlocked"]
                ],
                "unlocked_count": profile["achievements"]["unlocked_count"],
                "total_count": profile["achievements"]["total_count"],
            },
            "evolution": {
                "level": profile["evolution"]["level"],
                "indicators": profile["evolution"]["indicators"],
            },
            "indicators": profile["indicators"],
            "professional_profile": {
                **{key: value for key, value in profile["professional_profile"].items()
                   if key != "curriculo_path" and value is not None and value != ""},
                **({"curriculo_url": f"/profile/{user_id}/curriculo"}
                   if profile["professional_profile"]["curriculo_path"] else {}),
            },
        }
    )


@public_profile_bp.get("/<int:user_id>/curriculo")
def public_resume(user_id):
    try:
        get_public_profile(user_id)
        path = get_resume_path(user_id)
    except (PublicProfileError, ProfessionalProfileError) as error:
        return str(error), 404
    return send_file(path, mimetype="application/pdf", as_attachment=True, download_name="curriculo.pdf")
