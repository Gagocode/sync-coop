from flask import Blueprint, redirect, render_template, url_for

from controllers.auth_controller import login_required
from services.professional_profile_service import get_professional_profile
from services.organization_service import organization_setup_available
from services.corporate_dashboard_service import get_corporate_dashboard


page_bp = Blueprint("pages", __name__)


@page_bp.get("/login")
def login_page():
    return render_template("login.html")


@page_bp.get("/cadastro")
def register_page():
    return render_template("cadastro.html")


@page_bp.get("/dashboard")
@login_required
def dashboard_page(user):
    if organization_setup_available():
        return redirect(url_for("organization.setup_page"))
    corporate_dashboard = (
        get_corporate_dashboard(user)
        if user.role == "manager" and user.organization_id is not None else None
    )
    return render_template(
        "index.html", user=user,
        professional_profile=get_professional_profile(user.id),
        corporate_dashboard=corporate_dashboard,
    )
