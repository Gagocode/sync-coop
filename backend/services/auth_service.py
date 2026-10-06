from werkzeug.security import check_password_hash, generate_password_hash

from repositories import user_repository
from services.mission_service import create_initial_missions_for_user


class AuthError(Exception):
    pass


def register_user(nome, email, senha, curso=None):
    nome = _require_text(nome, "Nome obrigatorio")
    email = _normalize_email(email)
    senha = _require_text(senha, "Senha obrigatoria")
    curso = curso.strip() if curso else None

    if user_repository.find_by_email(email):
        raise AuthError("Email ja cadastrado")

    senha_hash = generate_password_hash(senha)
    user = user_repository.create_user(nome, email, senha_hash, curso)
    create_initial_missions_for_user(user.id)
    return user


def authenticate_user(email, senha):
    email = _normalize_email(email)
    senha = _require_text(senha, "Senha obrigatoria")
    user = user_repository.find_by_email(email)

    if not user or not check_password_hash(user.senha_hash, senha):
        raise AuthError("Email ou senha invalidos")

    return user


def get_user_by_id(user_id):
    if not user_id:
        return None
    return user_repository.find_by_id(user_id)


def _normalize_email(email):
    email = _require_text(email, "Email obrigatorio").lower()
    if "@" not in email or "." not in email.split("@")[-1]:
        raise AuthError("Email invalido")
    return email


def _require_text(value, message):
    value = value.strip() if value else ""
    if not value:
        raise AuthError(message)
    return value
