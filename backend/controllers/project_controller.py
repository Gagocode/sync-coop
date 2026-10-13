from flask import Blueprint, jsonify, redirect, render_template, request

from controllers.auth_controller import login_required
from controllers.page_controller import dashboard_section
from services.project_service import (
    ProjectError,
    create_project,
    delete_project,
    get_project,
    list_projects,
    update_project,
)


project_bp = Blueprint("projects", __name__, url_prefix="/projetos")


@project_bp.get("/")
@login_required
def projects_page(user):
    return redirect(dashboard_section("projects"))


@project_bp.get("/novo")
@login_required
def new_project_page(user):
    return redirect(dashboard_section("projects", "new"))


@project_bp.post("/")
@login_required
def create_project_action(user):
    try:
        project = create_project(user.id, _request_data())
    except ProjectError as error:
        if _wants_json():
            return jsonify({"error": str(error)}), 400
        return render_template("projeto_form.html", project=None, error=str(error)), 400

    if _wants_json():
        return jsonify({"project": project.to_dict()}), 201
    return redirect(dashboard_section("projects"))


@project_bp.get("/json")
@login_required
def projects_json(user):
    projects = list_projects(user.id)
    return jsonify({"projects": [project.to_dict() for project in projects]})


@project_bp.get("/<int:project_id>")
@login_required
def project_detail_page(user, project_id):
    try:
        get_project(user.id, project_id)
    except ProjectError as error:
        return str(error), 404
    return redirect(dashboard_section("projects"))


@project_bp.get("/<int:project_id>/editar")
@login_required
def edit_project_page(user, project_id):
    try:
        get_project(user.id, project_id)
    except ProjectError as error:
        return str(error), 404
    return redirect(dashboard_section("projects", f"edit/{project_id}"))


@project_bp.post("/<int:project_id>/editar")
@login_required
def update_project_action(user, project_id):
    try:
        project = update_project(user.id, project_id, _request_data())
    except ProjectError as error:
        if _wants_json():
            return jsonify({"error": str(error)}), 400
        return str(error), 400

    if _wants_json():
        return jsonify({"project": project.to_dict()})
    return redirect(dashboard_section("projects"))


@project_bp.post("/<int:project_id>/excluir")
@login_required
def delete_project_action(user, project_id):
    try:
        delete_project(user.id, project_id)
    except ProjectError as error:
        if _wants_json():
            return jsonify({"error": str(error)}), 404
        return str(error), 404

    if _wants_json():
        return jsonify({"message": "Projeto excluido com sucesso"})
    return redirect(dashboard_section("projects"))


def _request_data():
    if request.is_json:
        return request.get_json(silent=True) or {}
    return request.form


def _wants_json():
    return request.is_json or (
        request.accept_mimetypes.accept_json
        and not request.accept_mimetypes.accept_html
    )
