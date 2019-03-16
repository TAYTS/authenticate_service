import logging
import logging.handlers

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from models.db import db


def make_app(config='config.py'):
    app = Flask(__name__)
    app.config.from_pyfile(config)

    # LOGGING CONSTANTS
    formatter = logging.Formatter(
        "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
    handler = logging.handlers.RotatingFileHandler(
        app.config['APP_LOG_FILE'], maxBytes=1024 * 1024 * 100, backupCount=20)
    handler.setFormatter(formatter)
    handler.setLevel(app.config['APP_LOG_LEVEL'])
    app.logger.addHandler(handler)
    app.logger.setLevel(app.config['APP_LOG_LEVEL'])

    # Allow CORS
    CORS(app, supports_credentials=True)

    # Initialise the app with the database setup
    db.init_app(app)

    # Setup the Flask-JWT-Extended
    JWTManager(app)

    # Degine all the moduls
    from app.modules import users
    from app.modules import tickets

    # Register the blueprint of each module
    app.register_blueprint(users.module)
    app.register_blueprint(tickets.module)

    return app
