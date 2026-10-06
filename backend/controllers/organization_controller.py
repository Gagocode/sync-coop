from flask import Blueprint, jsonify, redirect, render_template, request, url_for

from controllers.auth_controller import login_required, manager_required
from services.organization_service import (
    OrganizationError,
    create_first_organization,
    organization_setup_available,
)
from services.sector_service import (
    OrganizationManagementError,
    assign_user_to_sector,
    create_sector,
    delete_sector,
    list_manageable_users,
    list_sectors,
    update_sector,
)


organization_bp = Blueprint("organization", __name__)


@organization_bp.get("/organizacao/configurar")
@login_required
def setup_page(user):
    if not organization_setup_available():
        return redirect(url_for("pages.dashboard_page"))
    return render_template("organization_setup.html", user=user, error=None)


@organization_bp.post("/organizacao/configurar")
@login_required
def setup_action(user):
    try:
        organization = create_first_organization(user.id, _request_data())
    except OrganizationError as error:
        if _wants_json():
            return jsonify({"error": str(error)}), 400
        if not organization_setup_available():
            return redirect(url_for("pages.dashboard_page"))
        return render_template("organization_setup.html", user=user, error=str(error)), 400

    if _wants_json():
        return jsonify({"organization": organization.to_dict()}), 201
    return redirect(url_for("organization.sectors_page"))


@organization_bp.get("/gestao/setores/")
@manager_required
def sectors_page(user):
    return _render_sectors(user)


@organization_bp.get("/gestao/setores/json")
@manager_required
def sectors_json(user):
    return jsonify({"sectors": [sector.to_dict() for sector in list_sectors(user)]})


@organization_bp.post("/gestao/setores/")
@manager_required
def create_sector_action(user):
    try:
        sector = create_sector(user, _request_data())
    except OrganizationManagementError as error:
        if _wants_json():
            return jsonify({"error": str(error)}), 400
        return _render_sectors(user, str(error), 400)

    if _wants_json():
        return jsonify({"sector": sector.to_dict()}), 201
    return redirect(url_for("organization.sectors_page"))


@organization_bp.post("/gestao/setores/<int:sector_id>/editar")
@manager_required
def update_sector_action(user, sector_id):
    try:
        sector = update_sector(user, sector_id, _request_data())
    except OrganizationManagementError as error:
        if _wants_json():
            return jsonify({"error": str(error)}), 400
        return _render_sectors(user, str(error), 400)

    if _wants_json():
        return jsonify({"sector": sector.to_dict()})
    return redirect(url_for("organization.sectors_page"))


@organization_bp.post("/gestao/setores/<int:sector_id>/excluir")
@manager_required
def delete_sector_action(user, sector_id):
    try:
        delete_sector(user, sector_id)
    except OrganizationManagementError as error:
        if _wants_json():
            return jsonify({"error": str(error)}), 400
        return _render_sectors(user, str(error), 400)

    if _wants_json():
        return jsonify({"message": "Setor excluído com sucesso"})
    return redirect(url_for("organization.sectors_page"))


@organization_bp.get("/gestao/usuarios/")
@manager_required
def users_page(user):
    return render_template(
        "organization_users.html",
        user=user,
        users=list_manageable_users(user),
        sectors=list_sectors(user),
        error=None,
    )


@organization_bp.post("/gestao/usuarios/<int:user_id>/setor")
@manager_required
def assign_user_sector_action(user, user_id):
    try:
        raw_sector_id = _request_data().get("sector_id", "")
        try:
            sector_id = int(raw_sector_id)
        except (TypeError, ValueError) as error:
            raise OrganizationManagementError("Selecione um setor válido") from error
        assign_user_to_sector(user, user_id, sector_id)
    except OrganizationManagementError as error:
        if _wants_json():
            return jsonify({"error": str(error) or "Setor inválido"}), 400
        return render_template(
            "organization_users.html",
            user=user,
            users=list_manageable_users(user),
            sectors=list_sectors(user),
            error=str(error) or "Setor inválido",
        ), 400

    if _wants_json():
        return jsonify({"message": "Setor do usuário atualizado com sucesso"})
    return redirect(url_for("organization.users_page"))


def _render_sectors(user, error=None, status_code=200):
    return (
        render_template(
            "organization_sectors.html",
            user=user,
            sectors=list_sectors(user),
            error=error,
        ),
        status_code,
    )


def _request_data():
    if request.is_json:
        return request.get_json(silent=True) or {}
    return request.form


def _wants_json():
    return request.is_json or (
        request.accept_mimetypes.accept_json
        and not request.accept_mimetypes.accept_html
    )
