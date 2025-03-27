import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.config import Config

db = SQLAlchemy()  # ✅ Make sure this is here


def create_app(config_class=Config):
    app = Flask(
        __name__, instance_path=os.path.abspath(".")
    )  # 👈 forces it to use project root
    app.config.from_object(config_class)
    db.init_app(app)

    from app.routes import main_bp

    app.register_blueprint(main_bp)

    return app


# 🧠 This line is key to fix your ImportError:
# So that `from app import db` works in models.py and setup_db.py
__all__ = ["db", "create_app"]
