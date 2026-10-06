from flask import Blueprint, jsonify, redirect, render_template, request, send_file, url_for

from controllers.auth_controller import login_required
from services.profile_service import get_profile
from services.professional_profile_service import (
    ProfessionalProfileError,
    get_professional_profile,
    get_resume_path,
    update_professional_profile,
)


profile_bp = Blueprint("profile", __name__, url_prefix="/perfil")


@profile_bp.get("/")
@login_required
def profile_page(user):
    profile = get_profile(user.id)
    return _render_profile(profile, get_professional_profile(user.id))


def _render_profile(profile, professional_profile, error=None):
    return render_template(
        "perfil.html",
        user=profile["user"],
        disc_result=profile["disc_result"],
        projects=profile["projects"],
        certificates=profile["certificates"],
        achievements=profile["achievements"],
        observed_disc_result=profile["observed_disc_result"],
        evolution=profile["evolution"],
        professional_profile=professional_profile,
        professional_error=error,
    )


@profile_bp.post("/profissional")
@login_required
def update_professional_profile_action(user):
    data = request.get_json(silent=True) if request.is_json else request.form
    data = data or {}
    try:
        professional_profile = update_professional_profile(
            user.id, data, request.files.get("curriculo")
        )
    except ProfessionalProfileError as error:
        if _wants_json():
            return jsonify({"error": str(error)}), 400
        draft = get_professional_profile(user.id)
        draft.update({key: data.get(key, "") for key in data.keys()})
        return _render_profile(get_profile(user.id), draft, str(error)), 400
    if _wants_json():
        return jsonify({"professional_profile": professional_profile})
    return redirect(url_for("profile.profile_page", saved=1))


def _wants_json():
    return request.is_json or (
        request.accept_mimetypes.accept_json
        and not request.accept_mimetypes.accept_html
    )


@profile_bp.get("/curriculo")
@login_required
def own_resume(user):
    try:
        path = get_resume_path(user.id)
    except ProfessionalProfileError as error:
        return str(error), 404
    return send_file(path, mimetype="application/pdf", as_attachment=True, download_name="curriculo.pdf")


@profile_bp.get("/json")
@login_required
def profile_json(user):
    profile = get_profile(user.id)
    current_user = profile["user"]
    disc_result = profile["disc_result"]
    return jsonify(
        {
            "user": current_user.to_public_dict(),
            "disc_result": disc_result,
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
                "history": [
                    event.to_dict()
                    for event in profile["evolution"]["history"]
                ],
            },
        }
    )
