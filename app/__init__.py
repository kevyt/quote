import logging
import os
from logging.handlers import RotatingFileHandler
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_share import Share

# first create extension instances, which will be initialised in create_app
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = "auth.login"
bootstrap = Bootstrap()
share = Share()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # initialising extension instances
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    bootstrap.init_app(app)
    share.init_app(app)

    # register the blueprints
    from app.auth import bp as auth_bp

    app.register_blueprint(auth_bp)

    from app.core import bp as core_bp

    app.register_blueprint(core_bp)

    from app.errors import bp as errors_bp

    app.register_blueprint(errors_bp)

    if not app.debug and not app.testing:

        # now logging to file
        if not os.path.exists("logs"):
            os.mkdir("logs")
        file_handler = RotatingFileHandler(
            "logs/quote.log", maxBytes=10240, backupCount=10
        )
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
            )
        )
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info("Quote website")
    return app


from app import models
