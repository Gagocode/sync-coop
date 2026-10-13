from flask import Blueprint, render_template, url_for

from controllers.auth_controller import login_required
from services.professional_profile_service import get_professional_profile


page_bp = Blueprint("pages", __name__)


def dashboard_section(section, action=None):
    fragment = section if action is None else f"{section}/{action}"
    return f"{url_for('pages.dashboard_page')}#{fragment}"


@page_bp.get("/login")
def login_page():
    return render_template("login.html")


@page_bp.get("/cadastro")
def register_page():
    return render_template("cadastro.html")


@page_bp.get("/dashboard")
@login_required
def dashboard_page(user):
    return render_template("index.html", user=user, professional_profile=get_professional_profile(user.id))
