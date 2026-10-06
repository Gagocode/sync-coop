from werkzeug.security import generate_password_hash

from repositories import certificate_repository
from repositories import disc_repository
from repositories import project_repository
from repositories import user_repository
from services.achievement_service import evaluate_user_achievements
from services.auth_service import register_user
from services.certificate_service import create_certificate
from services.disc_service import submit_initial_disc
from services.mission_service import complete_user_mission_by_key, create_initial_missions_for_user
from services.observed_disc_service import update_observed_disc
from services.profile_service import get_profile
from services.project_service import create_project


DEMO_PASSWORD = "demo123"

DEMO_USERS = [
    {
        "nome": "Ana Ribeiro",
        "email": "demo@syncdisc.local",
        "curso": "Sistemas de Informacao",
        "answers": {
            "q1": "D", "q2": "I", "q3": "S", "q4": "C",
            "q5": "D", "q6": "I", "q7": "C", "q8": "S",
            "q9": "I", "q10": "C", "q11": "D", "q12": "S",
        },
        "projects": [
            {
                "titulo": "Painel de Indicadores Academicos",
                "descricao": "Dashboard para acompanhar desempenho de turmas e atividades de extensao.",
                "tecnologias": "Python, Flask, SQLite",
                "link": "https://example.com/painel-academico",
            },
            {
                "titulo": "App de Organizacao de Estudos",
                "descricao": "Prototipo para registrar metas semanais e evidencias de aprendizagem.",
                "tecnologias": "HTML, CSS, JavaScript",
                "link": "https://example.com/estudos",
            },
            {
                "titulo": "Catalogo de Projetos Integradores",
                "descricao": "Repositorio visual para apresentar projetos desenvolvidos na faculdade.",
                "tecnologias": "Flask, Jinja, SQLite",
                "link": "https://example.com/catalogo",
            },
        ],
        "certificates": [
            {
                "nome": "Fundamentos de Gestao de Projetos",
                "instituicao": "Instituto Demo",
                "carga_horaria": "20",
                "data_conclusao": "2026-04-10",
            },
            {
                "nome": "Introducao a Analise de Dados",
                "instituicao": "Academia Aberta",
                "carga_horaria": "30",
                "data_conclusao": "2026-05-18",
            },
            {
                "nome": "Comunicacao Profissional",
                "instituicao": "Centro Universitario Demo",
                "carga_horaria": "12",
                "data_conclusao": "2026-06-02",
            },
        ],
    },
    {
        "nome": "Bruno Martins",
        "email": "bruno.demo@syncdisc.local",
        "curso": "Ciencia da Computacao",
        "answers": {
            "q1": "C", "q2": "C", "q3": "S", "q4": "C",
            "q5": "D", "q6": "I", "q7": "C", "q8": "C",
            "q9": "S", "q10": "C", "q11": "S", "q12": "D",
        },
        "projects": [
            {
                "titulo": "API de Portifolio Academico",
                "descricao": "Servico simples para listar experiencias, projetos e certificados.",
                "tecnologias": "Flask, REST, SQLite",
                "link": "https://example.com/api-portifolio",
            },
            {
                "titulo": "Monitor de Habitos de Estudo",
                "descricao": "Aplicacao para visualizar consistencia semanal em atividades de estudo.",
                "tecnologias": "JavaScript, CSS, LocalStorage",
                "link": "",
            },
        ],
        "certificates": [
            {
                "nome": "Logica de Programacao",
                "instituicao": "Plataforma Demo",
                "carga_horaria": "40",
                "data_conclusao": "2026-03-22",
            },
            {
                "nome": "Banco de Dados Relacional",
                "instituicao": "Instituto Demo",
                "carga_horaria": "24",
                "data_conclusao": "2026-07-15",
            },
        ],
    },
]


def seed_demo_data():
    seeded_users = []
    for demo_user in DEMO_USERS:
        user = _get_or_create_user(demo_user)
        create_initial_missions_for_user(user.id)
        _ensure_disc(user.id, demo_user["answers"])
        _ensure_projects(user.id, demo_user["projects"])
        _ensure_certificates(user.id, demo_user["certificates"])
        get_profile(user.id)
        evaluate_user_achievements(user.id)
        update_observed_disc(user.id)
        seeded_users.append(user)
    return seeded_users


def _get_or_create_user(demo_user):
    user = user_repository.find_by_email(demo_user["email"])
    if user:
        return user_repository.update_password_hash(
            user.id,
            generate_password_hash(DEMO_PASSWORD),
        )
    return register_user(
        nome=demo_user["nome"],
        email=demo_user["email"],
        senha=DEMO_PASSWORD,
        curso=demo_user["curso"],
    )


def _ensure_disc(user_id, answers):
    if disc_repository.find_initial_result_by_user_id(user_id):
        return
    submit_initial_disc(user_id, answers)


def _ensure_projects(user_id, projects):
    existing_titles = {project.titulo for project in project_repository.list_by_user_id(user_id)}
    for project in projects:
        if project["titulo"] not in existing_titles:
            create_project(user_id, project)


def _ensure_certificates(user_id, certificates):
    existing_names = {
        certificate.nome
        for certificate in certificate_repository.list_by_user_id(user_id)
    }
    for certificate in certificates:
        if certificate["nome"] not in existing_names:
            create_certificate(user_id, certificate)


if __name__ == "__main__":
    users = seed_demo_data()
    for user in users:
        complete_user_mission_by_key(user.id, "continue_evolution")
        print(f"Demo pronto: {user.email} / {DEMO_PASSWORD}")
