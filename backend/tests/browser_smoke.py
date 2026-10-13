"""Optional browser smoke test. Run with: python backend/tests/browser_smoke.py.

Requires Playwright and its Chromium browser. Uses only a temporary SQLite database.
"""

import logging
import sys
import tempfile
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright
from werkzeug.serving import make_server


BACKEND = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND))

from database import connection as database  # noqa: E402
from services import certificate_service, professional_profile_service  # noqa: E402


def run():
    logging.getLogger("werkzeug").setLevel(logging.ERROR)
    with tempfile.TemporaryDirectory() as temporary_directory:
        root = Path(temporary_directory)
        database.DATABASE_PATH = root / "browser.sqlite3"
        certificate_service.UPLOAD_ROOT = root / "uploads"
        certificate_service.CERTIFICATE_UPLOAD_DIR = certificate_service.UPLOAD_ROOT / "certificates"
        professional_profile_service.RESUME_DIR = certificate_service.UPLOAD_ROOT / "resumes"

        from app import create_app
        app = create_app()
        app.testing = True
        server = make_server("127.0.0.1", 0, app, threaded=True)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        base = f"http://127.0.0.1:{server.server_port}"
        errors = []
        external_font_errors = []
        try:
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(headless=True)
                page = browser.new_page(viewport={"width": 1280, "height": 900})
                page.on("pageerror", lambda error: errors.append(str(error)))
                def record_console(message):
                    if message.type != "error":
                        return
                    url = message.location.get("url", "")
                    if url.startswith("https://fonts.googleapis.com/") and "ERR_NETWORK_ACCESS_DENIED" in message.text:
                        external_font_errors.append(url)
                    else:
                        errors.append(f"console: {url} {message.text}")

                page.on("console", record_console)
                page.on("response", lambda response: errors.append(
                    f"HTTP {response.status}: {response.url}"
                ) if response.url.startswith(base) and response.status >= 400 else None)
                page.goto(base + "/cadastro", wait_until="domcontentloaded")
                page.locator('input[name="nome"]').fill("Pessoa Navegador")
                page.locator('input[name="email"]').fill("navegador@example.com")
                page.locator('input[name="senha"]').fill("senha-segura")
                page.locator('button[type="submit"]').click()
                page.wait_for_url("**/disc/")
                for index in range(12):
                    page.locator(".journey-question").nth(index).locator('input[value="D"]').check()
                    page.locator("[data-quiz-next]" if index < 11 else "[data-quiz-submit]").click()
                page.wait_for_url("**/disc/resultado")
                page.goto(base + "/dashboard", wait_until="domcontentloaded")
                page.wait_for_function("document.querySelector('#profile-email').textContent === 'navegador@example.com'")

                page.locator("#tab-projects").click()
                page.locator("#panel-projects [data-open-dialog]").first.click()
                page.locator('#project-form [name="titulo"]').fill("Projeto navegador")
                page.locator('#project-form [name="descricao"]').fill("Descricao do projeto")
                page.locator('#project-form [name="tecnologias"]').fill("Python")
                page.locator('#project-form [type="submit"]').click()
                page.locator("#project-list").get_by_text("Projeto navegador").wait_for()
                page.locator('#project-list [data-edit="project"]').click()
                page.locator('#project-form [name="titulo"]').fill("Projeto atualizado")
                page.locator('#project-form [type="submit"]').click()
                page.locator("#project-list").get_by_text("Projeto atualizado").wait_for()

                page.locator("#tab-certificates").click()
                page.locator("#panel-certificates [data-open-dialog]").first.click()
                page.locator('#certificate-form [name="nome"]').fill("Curso navegador")
                page.locator('#certificate-form [name="instituicao"]').fill("Instituicao")
                page.locator('#certificate-form [name="carga_horaria"]').fill("8")
                page.locator('#certificate-form [name="data_conclusao"]').fill("2026-10-01")
                page.locator('#certificate-form [type="submit"]').click()
                page.locator("#certificate-list").get_by_text("Curso navegador").wait_for()
                page.locator('#certificate-list [data-edit="certificate"]').click()
                page.locator('#certificate-form [name="nome"]').fill("Curso atualizado")
                page.locator('#certificate-form [name="arquivo"]').set_input_files({
                    "name": "curso.pdf", "mimeType": "application/pdf", "buffer": b"%PDF-1.4\n%%EOF",
                })
                page.locator('#certificate-form [type="submit"]').click()
                page.locator("#certificate-list").get_by_text("Curso atualizado").wait_for()
                file_path = page.locator('#certificate-list a[href$="/arquivo"]').get_attribute("href")
                assert page.request.get(base + file_path).body() == b"%PDF-1.4\n%%EOF"

                for tab in ("missions", "achievements", "evolution", "profile"):
                    page.locator(f"#tab-{tab}").click()
                    assert page.locator(f"#panel-{tab}").is_visible(), tab
                page.locator('#dashboard-professional-form [name="biografia"]').fill("Perfil no navegador")
                page.locator('#dashboard-professional-form [type="submit"]').click()
                page.locator("#dashboard-professional-status").get_by_text(
                    "Informações profissionais salvas."
                ).wait_for()

                public_link = page.locator('#panel-profile a.button[href^="/perfil/"]').get_attribute("href")
                page.goto(base + public_link, wait_until="domcontentloaded")
                assert "Projeto atualizado" in page.content()
                assert "Curso atualizado" in page.content()
                page.goto(base + "/dashboard", wait_until="domcontentloaded")
                page.wait_for_function("document.querySelector('#profile-email').textContent === 'navegador@example.com'")
                page.locator("#tab-projects").click()
                page.once("dialog", lambda dialog: dialog.accept())
                page.locator('#project-list [data-delete="project"]').click()
                page.locator("#project-list").get_by_text("Seu Curriculo Vivo ainda nao tem projetos.").wait_for()
                page.locator("#tab-certificates").click()
                page.once("dialog", lambda dialog: dialog.accept())
                page.locator('#certificate-list [data-delete="certificate"]').click()
                page.locator("#certificate-list").get_by_text("Seus certificados aparecerao aqui.").wait_for()
                page.locator('form[action="/auth/logout"] button').click()
                page.wait_for_url("**/login")
                page.locator('input[name="email"]').fill("navegador@example.com")
                page.locator('input[name="senha"]').fill("senha-segura")
                page.locator('button[type="submit"]').click()
                page.wait_for_url("**/dashboard")
                page.wait_for_function("document.querySelector('#profile-email').textContent === 'navegador@example.com'")
                page.set_viewport_size({"width": 390, "height": 844})
                page.reload(wait_until="domcontentloaded")
                page.wait_for_function("document.querySelector('#profile-email').textContent === 'navegador@example.com'")
                for tab in ("profile", "projects", "certificates", "missions", "achievements", "evolution"):
                    page.locator(f"#tab-{tab}").click()
                    assert page.locator(f"#panel-{tab}").is_visible(), tab
                assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 2")
                browser.close()
        finally:
            server.shutdown()
            thread.join(timeout=5)
        if errors:
            raise AssertionError("Browser errors: " + "; ".join(errors))
        print("Browser smoke passed: registration, DISC, dashboard tabs (desktop/mobile), project/certificate CRUD and download, profile, public profile, logout/login; no local HTTP or JS errors.")
        if external_font_errors:
            print(f"External Google Fonts blocked by sandbox: {len(external_font_errors)} requests.")


if __name__ == "__main__":
    run()
