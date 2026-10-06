from flask import Blueprint, jsonify, render_template

from controllers.auth_controller import login_required
from services.mission_service import get_user_missions


mission_bp = Blueprint("missions", __name__, url_prefix="/missoes")


@mission_bp.get("/")
@login_required
def missions_page(user):
    missions = get_user_missions(user.id)
    return render_template("missoes.html", user=user, missions=missions)


@mission_bp.get("/json")
@login_required
def missions_json(user):
    missions = get_user_missions(user.id)
    return jsonify({"missions": [mission.to_dict() for mission in missions]})

