from flask import Flask
from .routes import movie_status_bp
from db_extensions import database


def create_movie_status_app():
    app = Flask(__name__)
    app.config.from_object('auth_service.config.Config')

    database.init_app(app)

    app.register_blueprint(movie_status_bp, url_prefix="/movie_status")

    return app