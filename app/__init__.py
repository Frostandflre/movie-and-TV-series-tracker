from flask import Flask
from .extensions import database,migrate
from .routes import main

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    database.init_app(app)
    migrate.init_app(app, database)

    app.register_blueprint(main)

    return app