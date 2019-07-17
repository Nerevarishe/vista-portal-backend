from flask import Flask
from flask_mongoengine import MongoEngine
from flask_jwt_extended import JWTManager

from config import Config

db = MongoEngine()
jwt = JWTManager()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    jwt.init_app(app)

    # Blueprints:
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app
