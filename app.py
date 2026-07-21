import os
from flask import Flask

from config import Config
from database.db import db

from routes.upload import upload_bp
from routes.status import status_bp
from routes.results import results_bp

from workers.processor import start_worker

# Import models (required for SQLAlchemy to create tables)
from database.models import Advertisement, AnalysisReport


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize Database
    db.init_app(app)

    # Register API Routes
    app.register_blueprint(upload_bp, url_prefix="/api")
    app.register_blueprint(status_bp, url_prefix="/api")
    app.register_blueprint(results_bp)

    # Create database tables and start background worker
    with app.app_context():
        db.create_all()
        start_worker(app)

    # Health Check / Home Route
    @app.route("/")
    def home():
        return {
            "application": "Intelligent Media Processing Pipeline",
            "version": "1.0.0",
            "status": "Running",
            "database": "Connected",
        }

    return app


# Create Flask App
app = create_app()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",          # Required for Docker
        port=int(os.getenv("PORT", 5000)),
        debug=os.getenv("FLASK_ENV", "development") == "development"
    )