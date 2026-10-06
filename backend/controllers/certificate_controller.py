from flask import Blueprint, jsonify, redirect, render_template, request, send_file, url_for

from controllers.auth_controller import login_required
from services.certificate_service import (
    CertificateError,
    create_certificate,
    delete_certificate,
    get_certificate,
    get_certificate_file_path,
    list_certificates,
    update_certificate,
)


certificate_bp = Blueprint("certificates", __name__, url_prefix="/certificados")


@certificate_bp.get("/")
@login_required
def certificates_page(user):
    certificates = list_certificates(user.id)
    return render_template("certificados.html", user=user, certificates=certificates)


@certificate_bp.get("/novo")
@login_required
def new_certificate_page(user):
    return render_template("certificado_form.html", certificate=None, error=None)


@certificate_bp.post("/")
@login_required
def create_certificate_action(user):
    try:
        certificate = create_certificate(user.id, _request_data(), request.files.get("arquivo"))
    except CertificateError as error:
        if _wants_json():
            return jsonify({"error": str(error)}), 400
        return render_template("certificado_form.html", certificate=None, error=str(error)), 400

    if _wants_json():
        return jsonify({"certificate": certificate.to_dict()}), 201
    return redirect(url_for("certificates.certificate_detail_page", certificate_id=certificate.id))


@certificate_bp.get("/json")
@login_required
def certificates_json(user):
    certificates = list_certificates(user.id)
    return jsonify({"certificates": [certificate.to_dict() for certificate in certificates]})


@certificate_bp.get("/<int:certificate_id>")
@login_required
def certificate_detail_page(user, certificate_id):
    try:
        certificate = get_certificate(user.id, certificate_id)
    except CertificateError as error:
        return str(error), 404
    return render_template("certificado_detalhe.html", certificate=certificate)


@certificate_bp.get("/<int:certificate_id>/arquivo")
@login_required
def certificate_file(user, certificate_id):
    try:
        certificate = get_certificate(user.id, certificate_id)
        file_path = get_certificate_file_path(certificate)
    except CertificateError as error:
        return str(error), 404
    return send_file(file_path)


@certificate_bp.get("/<int:certificate_id>/editar")
@login_required
def edit_certificate_page(user, certificate_id):
    try:
        certificate = get_certificate(user.id, certificate_id)
    except CertificateError as error:
        return str(error), 404
    return render_template("certificado_form.html", certificate=certificate, error=None)


@certificate_bp.post("/<int:certificate_id>/editar")
@login_required
def update_certificate_action(user, certificate_id):
    try:
        certificate = update_certificate(
            user.id,
            certificate_id,
            _request_data(),
            request.files.get("arquivo"),
        )
    except CertificateError as error:
        if _wants_json():
            return jsonify({"error": str(error)}), 400
        return str(error), 400

    if _wants_json():
        return jsonify({"certificate": certificate.to_dict()})
    return redirect(url_for("certificates.certificate_detail_page", certificate_id=certificate.id))


@certificate_bp.post("/<int:certificate_id>/excluir")
@login_required
def delete_certificate_action(user, certificate_id):
    try:
        delete_certificate(user.id, certificate_id)
    except CertificateError as error:
        if _wants_json():
            return jsonify({"error": str(error)}), 404
        return str(error), 404

    if _wants_json():
        return jsonify({"message": "Certificado excluido com sucesso"})
    return redirect(url_for("certificates.certificates_page"))


def _request_data():
    if request.is_json:
        return request.get_json(silent=True) or {}
    return request.form


def _wants_json():
    return request.is_json or (
        request.accept_mimetypes.accept_json
        and not request.accept_mimetypes.accept_html
    )
