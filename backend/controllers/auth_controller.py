from functools import wraps

from flask import Blueprint, jsonify, redirect, request, session, url_for

from services.auth_service import AuthError, authenticate_user, get_user_by_id, register_user
from services.disc_service import get_initial_disc_result


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        user = get_user_by_id(session.get("user_id"))
        if not user:
            if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
                return jsonify({"error": "Autenticacao obrigatoria"}), 401
            return redirect(url_for("pages.login_page"))
        return view(user, *args, **kwargs)

    return wrapped_view


@auth_bp.post("/register")
def register():
    data = _request_data()
    try:
        user = register_user(
            nome=data.get("nome"),
            email=data.get("email"),
            senha=data.get("senha"),
            curso=data.get("curso"),
        )
    except AuthError as error:
        return _error_response(error, 400)

    session["user_id"] = user.id
    return _success_response(user, 201)


@auth_bp.post("/login")
def login():
    data = _request_data()
    try:
        user = authenticate_user(email=data.get("email"), senha=data.get("senha"))
    except AuthError as error:
        return _error_response(error, 401)

    session["user_id"] = user.id
    return _success_response(user)


@auth_bp.post("/logout")
def logout():
    session.clear()
    if _wants_json():
        return jsonify({"message": "Logout realizado com sucesso"})
    return redirect(url_for("pages.login_page"))


@auth_bp.get("/me")
@login_required
def me(user):
    return jsonify({"user": user.to_public_dict()})


def _request_data():
    if request.is_json:
        return request.get_json(silent=True) or {}
    return request.form


def _success_response(user, status_code=200):
    if _wants_json():
        return jsonify({"user": user.to_public_dict()}), status_code
    if not get_initial_disc_result(user.id):
        return redirect(url_for("disc.quiz_page"))
    if not user.classe:
        return redirect(url_for("profile.profile_page"))
    return redirect(url_for("pages.dashboard_page"))


def _error_response(error, status_code):
    if _wants_json():
        return jsonify({"error": str(error)}), status_code
    return str(error), status_code


def _wants_json():
    return request.is_json or (
        request.accept_mimetypes.accept_json
        and not request.accept_mimetypes.accept_html
    )
