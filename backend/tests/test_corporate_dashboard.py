import importlib
import io
from pathlib import Path
import pkgutil
import sqlite3
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

from flask import Flask
from werkzeug.datastructures import FileStorage

import repositories
from database.connection import get_connection, init_database
from repositories import user_repository
from services import auth_service, certificate_service, disc_service, mission_service
from services import professional_profile_service, project_service
from services.activity_service import calculate_engagement
from services.corporate_dashboard_service import get_corporate_dashboard
from services.profile_service import get_profile
from services.public_profile_service import get_public_profile
from services.sector_service import OrganizationManagementError, assign_user_to_sector


class ClosingConnection(sqlite3.Connection):
    def __exit__(self, *args):
        try:
            return super().__exit__(*args)
        finally:
            self.close()


class CorporateDashboardTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        connect = sqlite3.connect
        connection_patch = patch.object(
            sqlite3, 'connect', lambda *args, **kwargs: connect(*args, **kwargs, factory=ClosingConnection)
        )
        connection_patch.start()
        self.addCleanup(connection_patch.stop)
        self.path = Path(self.directory.name) / "test.sqlite3"
        init_database(self.path)
        for item in pkgutil.iter_modules(repositories.__path__):
            module = importlib.import_module(f"repositories.{item.name}")
            if hasattr(module, "get_connection"):
                mocked = patch.object(module, "get_connection", lambda: get_connection(self.path))
                mocked.start()
                self.addCleanup(mocked.stop)
        with get_connection(self.path) as connection:
            connection.executemany("INSERT INTO organizations (name) VALUES (?)", [("Empresa A",), ("Empresa B",)])
            connection.execute("INSERT INTO sectors (organization_id, name) VALUES (1, 'Desenvolvimento')")
        self.manager = self.create_user("Gestor", 1, "manager")
        self.employee = self.create_user("Colaborador", 1, "collaborator", 1)

    def create_user(self, name, organization=None, role=None, sector=None):
        user = user_repository.create_user(name, f"{name}@example.com", "unused")
        with get_connection(self.path) as connection:
            connection.execute(
                "UPDATE users SET organization_id=?, role=?, sector_id=? WHERE id=?",
                (organization, role, sector, user.id),
            )
        return user_repository.find_by_id(user.id)

    def activity(self):
        return user_repository.find_by_id(self.employee.id).last_activity_at

    def reset_activity(self):
        with get_connection(self.path) as connection:
            connection.execute("UPDATE users SET last_activity_at=NULL WHERE id=?", (self.employee.id,))

    def test_boundaries(self):
        now = datetime(2026, 10, 6, 12, tzinfo=timezone.utc)
        for age, expected in [(timedelta(0), "active"), (timedelta(days=7), "active"),
                              (timedelta(days=7, seconds=1), "attention"),
                              (timedelta(days=15), "attention"),
                              (timedelta(days=15, seconds=1), "inactive")]:
            with self.subTest(age=age):
                self.assertEqual(calculate_engagement((now-age).strftime("%Y-%m-%d %H:%M:%S"), now), expected)
        self.assertEqual(calculate_engagement(None, now), "inactive")

    def test_migration_preserves_legacy_and_is_idempotent(self):
        legacy = Path(self.directory.name) / "legacy.sqlite3"
        with sqlite3.connect(legacy) as connection:
            connection.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, nome TEXT, email TEXT, senha_hash TEXT, curso TEXT, created_at TEXT)")
            connection.execute("INSERT INTO users VALUES (42, 'Legado', 'old@example.com', 'hash', 'Curso', '2020-01-01')")
        init_database(legacy)
        init_database(legacy)
        with get_connection(legacy) as connection:
            user = connection.execute("SELECT * FROM users").fetchone()
            self.assertEqual((user['id'], user['curso'], user['created_at']), (42, 'Curso', '2020-01-01'))
            self.assertIsNone(user['last_activity_at'])
        init_database(self.path)
        self.assertIsNone(self.activity())

    def test_dashboard_scope_counts_and_single_query(self):
        self.create_user("Outra empresa", 2, "collaborator")
        self.create_user("Sem vínculo")
        self.create_user("Sem papel", 1)
        second = self.create_user("Sem setor", 1, "collaborator")
        third = self.create_user("Atenção", 1, "collaborator")
        user_repository.update_last_activity(second.id, "2026-10-06 12:00:00")
        user_repository.update_last_activity(third.id, "2026-09-25 12:00:00")
        statements = []
        def traced_connection():
            connection = get_connection(self.path)
            connection.set_trace_callback(statements.append)
            return connection
        with patch.object(user_repository, "get_connection", traced_connection):
            dashboard = get_corporate_dashboard(self.manager, datetime(2026, 10, 6, 12, tzinfo=timezone.utc))
        self.assertEqual(dashboard['metrics'], {'total': 3, 'active': 1, 'attention': 1, 'inactive': 1})
        self.assertEqual(len([sql for sql in statements if sql.lstrip().startswith('SELECT')]), 1)
        self.assertEqual({row['id'] for row in dashboard['collaborators']}, {self.employee.id, second.id, third.id})
        with self.assertRaises(OrganizationManagementError):
            get_corporate_dashboard(self.employee)
        empty_manager = self.create_user("Outro gestor", 2, "manager")
        with get_connection(self.path) as connection:
            connection.execute("UPDATE users SET organization_id=NULL WHERE nome='Outra empresa'")
        self.assertEqual(get_corporate_dashboard(empty_manager)['metrics']['total'], 0)

    def test_login_and_registration(self):
        user = auth_service.register_user("Novo", "new@example.com", "password")
        self.assertIsNotNone(user_repository.find_by_id(user.id).last_activity_at)
        with get_connection(self.path) as connection:
            connection.execute("UPDATE users SET last_activity_at=NULL WHERE id=?", (user.id,))
        with self.assertRaises(auth_service.AuthError):
            auth_service.authenticate_user(user.email, "wrong")
        self.assertIsNone(user_repository.find_by_id(user.id).last_activity_at)
        auth_service.authenticate_user(user.email, "password")
        self.assertIsNotNone(user_repository.find_by_id(user.id).last_activity_at)

    def test_record_crud_and_noop(self):
        cases = [
            (project_service, 'project', {'titulo': 'Projeto', 'descricao': 'Descrição', 'tecnologias': 'Python'}, 'titulo'),
            (certificate_service, 'certificate', {'nome': 'Curso', 'instituicao': 'Instituto', 'carga_horaria': '20', 'data_conclusao': '2026-01-01'}, 'nome'),
        ]
        for service, noun, data, title_key in cases:
            with self.subTest(noun=noun):
                record = getattr(service, f'create_{noun}')(self.employee.id, data)
                self.assertIsNotNone(self.activity())
                self.reset_activity()
                getattr(service, f'update_{noun}')(self.employee.id, record.id, data)
                self.assertIsNone(self.activity())
                getattr(service, f'update_{noun}')(self.employee.id, record.id, {**data, title_key: 'Alterado'})
                self.assertIsNotNone(self.activity())
                self.reset_activity()
                with self.assertRaises((project_service.ProjectError, certificate_service.CertificateError)):
                    getattr(service, f'create_{noun}')(self.employee.id, {})
                self.assertIsNone(self.activity())
                getattr(service, f'delete_{noun}')(self.employee.id, record.id)
                self.assertIsNotNone(self.activity())

    def test_profile_and_resume(self):
        professional_profile_service.update_professional_profile(self.employee.id, {'biografia': 'Bio'})
        self.assertIsNotNone(self.activity())
        self.reset_activity()
        professional_profile_service.update_professional_profile(self.employee.id, {'biografia': 'Bio'})
        self.assertIsNone(self.activity())
        with patch.object(professional_profile_service, 'RESUME_DIR', Path(self.directory.name) / 'resumes'):
            resume = FileStorage(stream=io.BytesIO(b'%PDF-1.4\n%%EOF'), filename='resume.pdf')
            professional_profile_service.update_professional_profile(self.employee.id, {'biografia': 'Bio'}, resume)
        self.assertIsNotNone(self.activity())

    def test_disc_missions_and_reads_do_not_renew_activity(self):
        answers = {question['id']: 'D' for question in disc_service.get_questions()}
        disc_service.submit_initial_disc(self.employee.id, answers)
        self.assertIsNotNone(self.activity())
        self.reset_activity()
        get_profile(self.employee.id)  # First actual completion of complete_profile.
        self.assertIsNotNone(self.activity())
        xp = user_repository.find_by_id(self.employee.id).xp
        self.reset_activity()
        get_profile(self.employee.id)
        get_public_profile(self.employee.id)
        mission_service.complete_user_mission_by_key(self.employee.id, 'complete_profile')
        self.assertIsNone(self.activity())
        self.assertEqual(user_repository.find_by_id(self.employee.id).xp, xp)
        assign_user_to_sector(self.manager, self.employee.id, 1)
        self.assertIsNone(self.activity())

    def test_dashboard_rendering_and_visibility(self):
        from controllers.page_controller import page_bp
        from controllers.auth_controller import auth_bp
        app = Flask(__name__, template_folder=str(Path(__file__).resolve().parents[2] / 'frontend' / 'pages'))
        app.secret_key = 'test'
        app.register_blueprint(page_bp)
        app.register_blueprint(auth_bp)
        client = app.test_client()
        self.assertEqual(client.get('/dashboard').status_code, 302)
        with client.session_transaction() as session:
            session['user_id'] = self.manager.id
        response = client.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Engajamento dos colaboradores', response.text)
        self.assertIn('Sem atividade registrada', response.text)
        with client.session_transaction() as session:
            session['user_id'] = self.employee.id
        with patch('services.corporate_dashboard_service.user_repository.list_collaborators_for_organization') as query:
            response = client.get('/dashboard')
        self.assertNotIn('corporate-dashboard-heading', response.text)
        query.assert_not_called()


if __name__ == '__main__':
    unittest.main()
