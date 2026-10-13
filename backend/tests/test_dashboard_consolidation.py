"""Regression coverage for canonical dashboard routes and existing CRUD contracts."""

import sys
import tempfile
import unittest
from io import BytesIO
from pathlib import Path


BACKEND = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND))

from database import connection as database  # noqa: E402


class DashboardConsolidationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.TemporaryDirectory()
        cls.database_path = Path(cls.temp_dir.name) / "test.sqlite3"
        cls.original_get_connection = database.get_connection
        cls.original_init_database = database.init_database
        cls.connections = []

        def test_connection(_path=None):
            connection = cls.original_get_connection(cls.database_path)
            cls.connections.append(connection)
            return connection

        cls.test_connection = test_connection
        cls.test_init_database = lambda _path: cls.original_init_database(cls.database_path)
        database.get_connection = cls.test_connection
        database.init_database = cls.test_init_database
        from services import certificate_service, professional_profile_service

        cls.certificate_service = certificate_service
        cls.professional_profile_service = professional_profile_service
        cls.original_upload_root = certificate_service.UPLOAD_ROOT
        cls.original_certificate_dir = certificate_service.CERTIFICATE_UPLOAD_DIR
        cls.original_resume_dir = professional_profile_service.RESUME_DIR
        certificate_service.UPLOAD_ROOT = Path(cls.temp_dir.name) / "uploads"
        certificate_service.CERTIFICATE_UPLOAD_DIR = certificate_service.UPLOAD_ROOT / "certificates"
        professional_profile_service.RESUME_DIR = certificate_service.UPLOAD_ROOT / "resumes"
        from app import create_app

        cls.app = create_app()
        cls.app.testing = True

    @classmethod
    def tearDownClass(cls):
        database.get_connection = cls.original_get_connection
        database.init_database = cls.original_init_database
        for module in tuple(sys.modules.values()):
            if getattr(module, "get_connection", None) is cls.test_connection:
                module.get_connection = cls.original_get_connection
            if getattr(module, "init_database", None) is cls.test_init_database:
                module.init_database = cls.original_init_database
        cls.certificate_service.UPLOAD_ROOT = cls.original_upload_root
        cls.certificate_service.CERTIFICATE_UPLOAD_DIR = cls.original_certificate_dir
        cls.professional_profile_service.RESUME_DIR = cls.original_resume_dir
        for connection in cls.connections:
            connection.close()
        cls.temp_dir.cleanup()

    def test_dashboard_routes_and_persistence(self):
        client = self.app.test_client()
        response = client.post("/auth/register", data={
            "nome": "Pessoa Teste", "email": "pessoa@example.com",
            "senha": "senha-segura", "curso": "Design",
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn("/disc/", response.location)
        self.assertEqual(client.get("/disc/").status_code, 200)
        response = client.post("/disc/", data={f"q{index}": "D" for index in range(1, 13)})
        self.assertTrue(response.location.endswith("/disc/resultado"))
        self.assertEqual(client.get("/disc/resultado").status_code, 200)

        for path, fragment in (
            ("/perfil/", "profile"),
            ("/missoes/", "missions"),
            ("/projetos/", "projects"),
            ("/projetos/novo", "projects/new"),
            ("/certificados/", "certificates"),
            ("/certificados/novo", "certificates/new"),
        ):
            with self.subTest(path=path):
                response = client.get(path)
                self.assertEqual(response.status_code, 302)
                self.assertTrue(response.location.endswith("/dashboard#" + fragment))

        self.assertEqual(client.get("/dashboard").status_code, 200)
        profile = client.get("/perfil/json").json
        self.assertEqual(profile["user"]["classe"], "Executor Estratégico")
        self.assertIn("evolution", profile)
        self.assertIn("achievements", profile)
        missions = client.get("/missoes/json").json["missions"]
        self.assertTrue(any(mission["status"] == "Concluida" for mission in missions))
        expected_methods = {
            "/dashboard": "GET", "/perfil/": "GET", "/missoes/": "GET",
            "/perfil/profissional": "POST", "/perfil/json": "GET",
            "/missoes/json": "GET", "/projetos/": "POST",
            "/projetos/json": "GET", "/certificados/": "POST",
            "/certificados/json": "GET", "/disc/": "POST",
        }
        for path, method in expected_methods.items():
            with self.subTest(method=method, path=path):
                self.assertTrue(any(rule.rule == path and method in rule.methods
                                    for rule in self.app.url_map.iter_rules()))

        response = client.post("/projetos/", json={
            "titulo": "Projeto", "descricao": "Descrição", "tecnologias": "Python",
            "link": "https://example.com",
        })
        self.assertEqual(response.status_code, 201)
        project_id = response.json["project"]["id"]
        self.assertEqual(client.get("/projetos/json").json["projects"][0]["titulo"], "Projeto")
        for path, fragment in (
            (f"/projetos/{project_id}", "projects"),
            (f"/projetos/{project_id}/editar", f"projects/edit/{project_id}"),
        ):
            self.assertTrue(client.get(path).location.endswith("/dashboard#" + fragment))
        self.assertEqual(client.post(f"/projetos/{project_id}/editar", json={
            "titulo": "Projeto editado", "descricao": "Descrição", "tecnologias": "Python",
        }).status_code, 200)
        self.assertEqual(client.get("/perfil/json").json["projects"][0]["titulo"], "Projeto editado")

        response = client.post("/certificados/", data={
            "nome": "Curso", "instituicao": "Instituição", "carga_horaria": "12",
            "data_conclusao": "2026-10-01", "arquivo": (BytesIO(b"certificado"), "curso.pdf"),
        }, headers={"Accept": "application/json"})
        self.assertEqual(response.status_code, 201)
        certificate_id = response.json["certificate"]["id"]
        download = client.get(f"/certificados/{certificate_id}/arquivo")
        self.assertEqual(download.data, b"certificado")
        download.close()
        self.assertEqual(client.get("/certificados/json").json["certificates"][0]["nome"], "Curso")
        for path, fragment in (
            (f"/certificados/{certificate_id}", "certificates"),
            (f"/certificados/{certificate_id}/editar", f"certificates/edit/{certificate_id}"),
        ):
            self.assertTrue(client.get(path).location.endswith("/dashboard#" + fragment))
        response = client.post(f"/certificados/{certificate_id}/editar", data={
            "nome": "Curso editado", "instituicao": "Instituição", "carga_horaria": "20",
            "data_conclusao": "2026-10-01",
        }, headers={"Accept": "application/json"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(client.get("/perfil/json").json["certificates"][0]["nome"], "Curso editado")

        response = client.post("/perfil/profissional", data={
            "biografia": "Minha trajetória", "curriculo": (BytesIO(b"%PDF-1.4\n%%EOF"), "curriculo.pdf"),
        },
                               headers={"Accept": "application/json"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["professional_profile"]["biografia"], "Minha trajetória")
        for path in ("/perfil/curriculo", "/profile/1/curriculo"):
            download = client.get(path)
            self.assertEqual(download.status_code, 200)
            download.close()
        self.assertEqual(client.get("/profile/1/json").status_code, 200)

        self.assertEqual(client.post(f"/projetos/{project_id}/excluir", headers={
            "Accept": "application/json",
        }).status_code, 200)
        self.assertEqual(client.post(f"/certificados/{certificate_id}/excluir", headers={
            "Accept": "application/json",
        }).status_code, 200)
        self.assertEqual(client.get("/projetos/json").json["projects"], [])
        self.assertEqual(client.get("/certificados/json").json["certificates"], [])

        self.assertEqual(client.get(f"/projetos/{project_id}").status_code, 404)
        self.assertEqual(client.get(f"/certificados/{certificate_id}").status_code, 404)
        self.assertEqual(client.get("/disc/").status_code, 200)
        self.assertEqual(client.get("/disc/resultado").status_code, 200)

        # Direct HTML form submissions retain their existing POST contract.
        response = client.post("/projetos/", data={
            "titulo": "Formulário", "descricao": "Descrição", "tecnologias": "Flask",
        })
        self.assertTrue(response.location.endswith("/dashboard#projects"))
        response = client.post("/certificados/", data={
            "nome": "Formulário", "instituicao": "Instituição", "carga_horaria": "8",
            "data_conclusao": "2026-10-02",
        })
        self.assertTrue(response.location.endswith("/dashboard#certificates"))
        response = client.post("/perfil/profissional", data={"biografia": "Formulário"})
        self.assertTrue(response.location.endswith("/dashboard#profile"))
        self.assertEqual(client.post("/projetos/", data={"titulo": ""}).status_code, 400)
        self.assertEqual(client.post("/certificados/", data={"nome": ""}).status_code, 400)


if __name__ == "__main__":
    unittest.main()
