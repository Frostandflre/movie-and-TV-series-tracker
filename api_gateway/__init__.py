from flask import Flask
from routes import gateway_bp

def create_gateway_app():
    app = Flask(__name__)

    app.register_blueprint(gateway_bp)

    return app
