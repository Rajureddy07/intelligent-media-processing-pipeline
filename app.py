import os

from flask import Flask, render_template

from config import Config
from database.db import db

from routes.upload import upload_bp
from routes.status import status_bp
from routes.results import results_bp

from workers.processor import start_worker

# Import models (required for SQLAlchemy)
from database.models import Advertisement, AnalysisReport


def create_app():
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static"
    )

    app.config.from_object(Config)

    # -----------------------------
    # Initialize Database
    # -----------------------------
    db.init_app(app)

    # -----------------------------
    # Register Blueprints
    # -----------------------------
    app.register_blueprint(upload_bp, url_prefix="/api")
    app.register_blueprint(status_bp, url_prefix="/api")
    app.register_blueprint(results_bp, url_prefix="/api")

    # -----------------------------
    # Create Tables & Start Worker
    # -----------------------------
    with app.app_context():
        db.create_all()
        start_worker(app)

    # -----------------------------
    # Frontend Routes
    # -----------------------------

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/health")
    def health():
        return {
            "application": "Intelligent Media Processing Pipeline",
            "version": "1.0.0",
            "status": "Running",
            "database": "Connected"
        }

    return app


# ---------------------------------
# Create Flask Application
# ---------------------------------

app = create_app()


# ---------------------------------
# Run Application
# ---------------------------------

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000)),
        debug=os.getenv("FLASK_ENV", "development") == "development"
    )