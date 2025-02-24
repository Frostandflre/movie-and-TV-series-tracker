from flask import Flask
from .extensions import migrate
from db_extensions import database
from .routes import main

def create_main_app():
    app = Flask(__name__)
    app.config.from_object('main_service.config.Config')

    database.init_app(app)
    migrate.init_app(app, database)

    app.register_blueprint(main)

    return app