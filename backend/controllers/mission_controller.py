from flask import Blueprint, jsonify, redirect

from controllers.auth_controller import login_required
from controllers.page_controller import dashboard_section
from services.mission_service import get_user_missions


mission_bp = Blueprint("missions", __name__, url_prefix="/missoes")


@mission_bp.get("/")
@login_required
def missions_page(user):
    return redirect(dashboard_section("missions"))


@mission_bp.get("/json")
@login_required
def missions_json(user):
    missions = get_user_missions(user.id)
    return jsonify({"missions": [mission.to_dict() for mission in missions]})
