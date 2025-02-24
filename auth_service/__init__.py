from flask import Flask
from .routes import auth_bp
from db_extensions import database

def create_auth_app():
    app = Flask(__name__)
    app.config.from_object('auth_service.config.Config')

    database.init_app(app)

    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app