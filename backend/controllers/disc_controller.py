from flask import Blueprint, jsonify, redirect, render_template, request, url_for

from controllers.auth_controller import login_required
from services.disc_service import DiscError, get_initial_disc_result, get_questions, submit_initial_disc


disc_bp = Blueprint("disc", __name__, url_prefix="/disc")


@disc_bp.get("/")
@login_required
def quiz_page(user):
    result = get_initial_disc_result(user.id)
    if result:
        return render_template("disc_result.html", user=user, result=result)
    return render_template("disc_quiz.html", user=user, questions=get_questions(), error=None)


@disc_bp.post("/")
@login_required
def submit_quiz(user):
    answers = _request_data()
    try:
        result = submit_initial_disc(user.id, answers)
    except DiscError as error:
        existing_result = get_initial_disc_result(user.id)
        if existing_result and str(error) == "DISC inicial ja realizado":
            if _wants_json():
                return jsonify({"result": existing_result})
            return redirect(url_for("disc.result_page"))
        if _wants_json():
            return jsonify({"error": str(error)}), 400
        return render_template(
            "disc_quiz.html",
            user=user,
            questions=get_questions(),
            error=str(error),
        ), 400

    if _wants_json():
        return jsonify({"result": result}), 201
    return redirect(url_for("disc.result_page"))


@disc_bp.get("/resultado")
@login_required
def result_page(user):
    result = get_initial_disc_result(user.id)
    if not result:
        return redirect(url_for("disc.quiz_page"))
    return render_template("disc_result.html", user=user, result=result)


@disc_bp.get("/resultado.json")
@login_required
def result_json(user):
    result = get_initial_disc_result(user.id)
    if not result:
        return jsonify({"error": "Resultado DISC inicial nao encontrado"}), 404
    return jsonify({"result": result})


def _request_data():
    if request.is_json:
        return request.get_json(silent=True) or {}
    return request.form


def _wants_json():
    return request.is_json or (
        request.accept_mimetypes.accept_json
        and not request.accept_mimetypes.accept_html
    )
