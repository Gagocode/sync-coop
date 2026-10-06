import os
from pathlib import Path

from flask import Flask, jsonify, redirect, url_for

from controllers.auth_controller import auth_bp
from controllers.certificate_controller import certificate_bp
from controllers.disc_controller import disc_bp
from controllers.mission_controller import mission_bp
from controllers.organization_controller import organization_bp
from controllers.page_controller import page_bp
from controllers.profile_controller import profile_bp
from controllers.project_controller import project_bp
from controllers.public_profile_controller import (
    public_profile_bp,
    public_profile_name_bp,
)
from database.connection import init_database

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "database" / "sync_disc.sqlite3"
UPLOAD_FOLDER = BASE_DIR / "uploads"
FRONTEND_DIR = BASE_DIR.parent / "frontend"


def create_app():
    app = Flask(
        __name__,
        static_folder=str(FRONTEND_DIR / "assets"),
        static_url_path="/assets",
        template_folder=str(FRONTEND_DIR / "pages"),
    )
    app.config["DATABASE_PATH"] = DATABASE_PATH
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "sync-disc-dev-secret")

    init_database(DATABASE_PATH)
    app.register_blueprint(auth_bp)
    app.register_blueprint(certificate_bp)
    app.register_blueprint(disc_bp)
    app.register_blueprint(mission_bp)
    app.register_blueprint(organization_bp)
    app.register_blueprint(page_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(project_bp)
    app.register_blueprint(public_profile_bp)
    app.register_blueprint(public_profile_name_bp)

    @app.get("/")
    def home():
        return redirect(url_for("pages.dashboard_page"))

    @app.get("/health")
    def health_check():
        return jsonify(
            {
                "app": "Sync Disc",
                "status": "backend initialized",
            }
        )

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
