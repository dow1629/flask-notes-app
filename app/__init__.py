import os
import logging

from flask import Flask, render_template
from dotenv import load_dotenv

load_dotenv()

from .extensions import db, migrate, login_manager
from config import DevelopmentConfig, TestingConfig, ProductionConfig


def create_app(test_config=None):
    app = Flask(__name__)

    config_name = os.environ.get("FLASK_ENV", "development")

    config_options = {
        "development": DevelopmentConfig,
        "testing": TestingConfig,
        "production": ProductionConfig,
    }

    config_class = config_options.get(config_name, DevelopmentConfig)
    app.config.from_object(config_class)

    logging.basicConfig(
        level=getattr(logging, app.config["LOG_LEVEL"]),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)

    if test_config is not None:
        app.config.update(test_config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    @login_manager.unauthorized_handler
    def unauthorized():
        return {"error": "Unauthorized."}, 401

    from . import models

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(models.User, int(user_id))

    from .notes import notes_bp
    app.register_blueprint(notes_bp)

    from .auth import auth_bp
    app.register_blueprint(auth_bp)

    @app.route("/")
    def notes_page():
        return render_template("notes.html")

    return app