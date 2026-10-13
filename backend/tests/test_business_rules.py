"""Business rule and transaction regression tests against an isolated SQLite DB."""

import sqlite3
import sys
import tempfile
import unittest
from contextlib import closing
from io import BytesIO
from pathlib import Path
from unittest.mock import patch

from werkzeug.datastructures import FileStorage


BACKEND = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND))

from database import connection as database  # noqa: E402
from repositories import user_repository  # noqa: E402
from services import (  # noqa: E402
    auth_service, certificate_service, disc_service, mission_service,
    professional_profile_service, progress_reconciliation_service,
    project_service,
)
from services.achievement_service import get_user_achievements  # noqa: E402
from services.observed_disc_service import get_observed_disc_result  # noqa: E402
from services.profile_service import get_profile  # noqa: E402
from services.public_profile_service import get_public_profile  # noqa: E402


TABLES = (
    "users", "professional_profiles", "initial_disc_results", "missions",
    "user_missions", "projects", "certificates", "achievement",
    "user_achievement", "evolution_events", "observed_disc_results",
)


class BusinessRulesTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_database_path = database.DATABASE_PATH
        self.original_upload_root = certificate_service.UPLOAD_ROOT
        self.original_certificate_dir = certificate_service.CERTIFICATE_UPLOAD_DIR
        self.original_resume_dir = professional_profile_service.RESUME_DIR
        database.DATABASE_PATH = Path(self.temp_dir.name) / "business.sqlite3"
        certificate_service.UPLOAD_ROOT = Path(self.temp_dir.name) / "uploads"
        certificate_service.CERTIFICATE_UPLOAD_DIR = certificate_service.UPLOAD_ROOT / "certificates"
        professional_profile_service.RESUME_DIR = certificate_service.UPLOAD_ROOT / "resumes"
        database.init_database()
        self.user = auth_service.register_user("Pessoa", "pessoa@example.com", "segredo")

    def tearDown(self):
        database.DATABASE_PATH = self.original_database_path
        certificate_service.UPLOAD_ROOT = self.original_upload_root
        certificate_service.CERTIFICATE_UPLOAD_DIR = self.original_certificate_dir
        professional_profile_service.RESUME_DIR = self.original_resume_dir
        self.temp_dir.cleanup()

    def snapshot(self):
        with closing(sqlite3.connect(database.DATABASE_PATH)) as connection:
            return {
                table: connection.execute(f"SELECT * FROM {table} ORDER BY rowid").fetchall()
                for table in TABLES
            }

    def complete_disc(self):
        return disc_service.submit_initial_disc(
            self.user.id, {f"q{index}": "D" for index in range(1, 13)}
        )

    def add_project(self, number):
        return project_service.create_project(self.user.id, {
            "titulo": f"Projeto {number}", "descricao": "Descricao",
            "tecnologias": "Python", "link": "",
        })

    def add_certificate(self, number, file_storage=None):
        return certificate_service.create_certificate(self.user.id, {
            "nome": f"Curso {number}", "instituicao": "Instituicao",
            "carga_horaria": "8", "data_conclusao": "2026-10-01",
        }, file_storage)

    def test_reads_and_repeated_dashboard_do_not_write(self):
        before = self.snapshot()
        self.assertIsNone(get_profile(self.user.id)["user"].classe)
        get_public_profile(self.user.id)
        mission_service.get_user_missions(self.user.id)
        get_user_achievements(self.user.id)
        self.assertEqual(get_observed_disc_result(self.user.id)["scores"],
                         {"D": 0, "I": 0, "S": 0, "C": 0})
        self.assertEqual(before, self.snapshot())

        self.complete_disc()
        from app import create_app
        app = create_app()
        app.testing = True
        client = app.test_client()
        with client.session_transaction() as session:
            session["user_id"] = self.user.id
        after_startup = self.snapshot()
        for _ in range(3):
            self.assertEqual(client.get("/dashboard").status_code, 200)
            self.assertEqual(client.get("/perfil/json").status_code, 200)
            self.assertEqual(client.get("/missoes/json").status_code, 200)
            self.assertEqual(client.get(f"/profile/{self.user.id}/json").status_code, 200)
        self.assertEqual(after_startup, self.snapshot())

    def test_mission_conditions_idempotency_and_class(self):
        with self.assertRaises(mission_service.MissionError):
            mission_service.complete_user_mission_by_key(self.user.id, "complete_disc_quiz")
        with self.assertRaises(mission_service.MissionError):
            mission_service.complete_user_mission_by_key(self.user.id, "first_project")
        self.assertEqual(self.snapshot()["users"][0][6], 0)

        self.complete_disc()
        self.assertEqual(user_repository.find_by_id(self.user.id).xp, 150)
        self.assertEqual(user_repository.find_by_id(self.user.id).classe,
                         disc_service.CLASS_BY_DIMENSION["D"])
        self.assertEqual(get_profile(self.user.id)["evolution"]["level"]["current"], 1)
        with self.assertRaises(disc_service.DiscError):
            disc_service.submit_initial_disc(self.user.id, {})

        self.add_project(1)
        first = mission_service.complete_user_mission_by_key(self.user.id, "first_project")
        self.assertEqual(first.status, "Concluida")
        with self.assertRaises(mission_service.MissionError):
            mission_service.complete_user_mission_by_key(self.user.id, "second_project")
        before = self.snapshot()
        mission_service.complete_user_mission_by_key(self.user.id, "first_project")
        mission_service.complete_missions_for_event(self.user.id, "PROJECT_CREATED")
        self.assertEqual(before, self.snapshot())
        self.assertEqual(user_repository.find_by_id(self.user.id).xp, 300)
        self.assertEqual(get_profile(self.user.id)["evolution"]["level"]["current"], 2)

    def test_project_certificate_effects_levels_achievements_and_deletion(self):
        self.complete_disc()
        for number in range(1, 4):
            self.add_project(number)
            self.add_certificate(number)
        profile = get_profile(self.user.id)
        self.assertEqual(profile["user"].xp, 1050)
        self.assertEqual(profile["evolution"]["level"]["current"], 4)
        self.assertEqual(profile["evolution"]["indicators"]["missions_completed"], 8)
        self.assertEqual(profile["achievements"]["unlocked_count"], 5)
        self.assertEqual(profile["observed_disc_result"]["scores"],
                         {"D": 30, "I": 25, "S": 40, "C": 30})
        before = self.snapshot()
        get_profile(self.user.id)
        progress_reconciliation_service.reconcile_user_progress(self.user.id)
        self.assertEqual(before, self.snapshot())

        project_service.delete_project(self.user.id, profile["projects"][0].id)
        certificate_service.delete_certificate(self.user.id, profile["certificates"][0].id)
        after = get_profile(self.user.id)
        self.assertEqual(after["user"].xp, 1050)
        self.assertEqual(after["observed_disc_result"]["scores"],
                         {"D": 20, "I": 25, "S": 40, "C": 20})
        self.assertEqual(after["achievements"]["unlocked_count"], 5)

    def test_available_mission_advances_after_each_matching_action(self):
        def available():
            return [mission.mission_key for mission in mission_service.get_user_missions(self.user.id)
                    if mission.status == "Pendente"]

        self.assertEqual(available(), ["complete_disc_quiz"])
        self.complete_disc()
        self.assertEqual(available(), ["first_project"])
        for number, expected in ((1, "second_project"), (2, "third_project"),
                                 (3, "first_certificate")):
            self.add_project(number)
            self.assertEqual(available(), [expected])
        for number, expected in ((1, "second_certificate"),
                                 (2, "third_certificate"), (3, "continue_evolution")):
            self.add_certificate(number)
            self.assertEqual(available(), [expected])

    def test_project_failure_rolls_back_all_records(self):
        self.complete_disc()
        before = self.snapshot()
        with patch.object(mission_service, "evaluate_user_achievements",
                          side_effect=RuntimeError("injected failure")):
            with self.assertRaisesRegex(RuntimeError, "injected failure"):
                self.add_project(1)
        self.assertEqual(before, self.snapshot())

    def test_disc_failure_rolls_back_result_class_xp_and_history(self):
        before = self.snapshot()
        with patch.object(disc_service, "complete_missions_for_event",
                          side_effect=RuntimeError("injected failure")):
            with self.assertRaisesRegex(RuntimeError, "injected failure"):
                self.complete_disc()
        self.assertEqual(before, self.snapshot())

    def test_certificate_failure_rolls_back_and_removes_new_file(self):
        self.complete_disc()
        before = self.snapshot()
        file_storage = FileStorage(stream=BytesIO(b"certificate"), filename="course.pdf")
        with patch.object(mission_service, "evaluate_user_achievements",
                          side_effect=RuntimeError("injected failure")):
            with self.assertRaisesRegex(RuntimeError, "injected failure"):
                self.add_certificate(1, file_storage)
        self.assertEqual(before, self.snapshot())
        self.assertEqual(list(certificate_service.CERTIFICATE_UPLOAD_DIR.glob("*")), [])

    def test_registration_failure_does_not_leave_user_without_missions(self):
        before = self.snapshot()
        with patch.object(auth_service, "create_initial_missions_for_user",
                          side_effect=RuntimeError("injected failure")):
            with self.assertRaisesRegex(RuntimeError, "injected failure"):
                auth_service.register_user("Outra", "outra@example.com", "segredo")
        self.assertEqual(before, self.snapshot())

    def test_record_ownership_is_checked_before_update_and_delete(self):
        self.complete_disc()
        project = self.add_project(1)
        certificate = self.add_certificate(1)
        other = auth_service.register_user("Outra", "outra@example.com", "segredo")
        before = self.snapshot()
        with self.assertRaises(project_service.ProjectError):
            project_service.update_project(other.id, project.id, {
                "titulo": "Alterado", "descricao": "Descricao", "tecnologias": "Python",
            })
        with self.assertRaises(project_service.ProjectError):
            project_service.delete_project(other.id, project.id)
        with self.assertRaises(certificate_service.CertificateError):
            certificate_service.update_certificate(other.id, certificate.id, {
                "nome": "Alterado", "instituicao": "Instituicao",
                "carga_horaria": "8", "data_conclusao": "2026-10-01",
            })
        with self.assertRaises(certificate_service.CertificateError):
            certificate_service.delete_certificate(other.id, certificate.id)
        self.assertEqual(before, self.snapshot())

    def test_resume_failure_restores_previous_file_and_profile(self):
        first = FileStorage(stream=BytesIO(b"%PDF-1.4\nold\n%%EOF"), filename="resume.pdf")
        professional_profile_service.update_professional_profile(
            self.user.id, {"biografia": "Antes"}, first
        )
        path = professional_profile_service.RESUME_DIR / f"{self.user.id}.pdf"
        previous_bytes = path.read_bytes()
        before = self.snapshot()
        second = FileStorage(stream=BytesIO(b"%PDF-1.4\nnew\n%%EOF"), filename="resume.pdf")
        with patch.object(professional_profile_service.repository, "save",
                          side_effect=RuntimeError("injected failure")):
            with self.assertRaisesRegex(RuntimeError, "injected failure"):
                professional_profile_service.update_professional_profile(
                    self.user.id, {"biografia": "Depois"}, second
                )
        self.assertEqual(previous_bytes, path.read_bytes())
        self.assertEqual(before, self.snapshot())
        self.assertEqual([item.name for item in path.parent.iterdir()], [path.name])

    def test_reconciliation_is_explicit_and_idempotent_for_legacy_data(self):
        self.complete_disc()
        with database.get_connection() as connection:
            connection.execute("DELETE FROM observed_disc_results WHERE user_id = ?", (self.user.id,))
            connection.execute("DELETE FROM evolution_events WHERE user_id = ?", (self.user.id,))
            connection.execute("UPDATE users SET classe = NULL WHERE id = ?", (self.user.id,))
        before = self.snapshot()
        get_profile(self.user.id)
        self.assertEqual(before, self.snapshot())
        progress_reconciliation_service.reconcile_user_progress(self.user.id)
        after = self.snapshot()
        self.assertNotEqual(before, after)
        self.assertIsNotNone(user_repository.find_by_id(self.user.id).classe)
        progress_reconciliation_service.reconcile_user_progress(self.user.id)
        self.assertEqual(after, self.snapshot())

    def test_invalid_json_fields_return_400_without_writing(self):
        from app import create_app
        app = create_app()
        app.testing = True
        client = app.test_client()
        with client.session_transaction() as session:
            session["user_id"] = self.user.id
        before = self.snapshot()
        cases = (
            ("/auth/register", {"nome": 42, "email": "new@example.com", "senha": "segredo"}),
            ("/auth/register", {"nome": "Outra", "email": "new@example.com",
                                "senha": "segredo", "curso": ["Design"]}),
            ("/auth/register", ["Outra"]),
            ("/projetos/", {"titulo": 42, "descricao": "Descricao", "tecnologias": "Python"}),
            ("/projetos/", {"titulo": "Projeto", "descricao": "Descricao",
                             "tecnologias": "Python", "link": ["https://example.com"]}),
            ("/projetos/", ["Projeto"]),
            ("/certificados/", {"nome": ["Curso"], "instituicao": "Instituicao",
                               "carga_horaria": "8", "data_conclusao": "2026-10-01"}),
            ("/certificados/", {"nome": "Curso", "instituicao": "Instituicao",
                               "carga_horaria": [8], "data_conclusao": "2026-10-01"}),
            ("/certificados/", ["Curso"]),
            ("/perfil/profissional", {"biografia": ["Texto"]}),
            ("/perfil/profissional", {"disponivel_estagio": ["sim"]}),
            ("/perfil/profissional", ["Texto"]),
            ("/disc/", ["D"]),
        )
        for path, body in cases:
            with self.subTest(path=path):
                response = client.post(path, json=body)
                self.assertEqual(response.status_code, 400)
                self.assertIn("error", response.json)
                self.assertEqual(before, self.snapshot())


if __name__ == "__main__":
    unittest.main()
