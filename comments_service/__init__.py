from flask import Flask
from .routes import comments_bp
from db_extensions import database


def create_comments_app():
    app = Flask(__name__)
    app.config.from_object('auth_service.config.Config')

    database.init_app(app)

    app.register_blueprint(comments_bp, url_prefix="/comments")

    return app