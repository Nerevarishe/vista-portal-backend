from flask import Flask
from flask_mongoengine import MongoEngine
from flask_jwt_extended import JWTManager
from flask_uploads import configure_uploads, patch_request_class, UploadSet, IMAGES
from flask_cors import CORS

from config import Config

db = MongoEngine()
jwt = JWTManager()

images = UploadSet('images', IMAGES)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.static_folder = app.config['STATIC_FOLDER']

    db.init_app(app)
    jwt.init_app(app)

    # Flask-Cors
    CORS(app)

    # Flask-Uploads configuration
    configure_uploads(app, images)
    patch_request_class(app)

    # Blueprints:
    from app.errors import bp as error_bp
    app.register_blueprint(error_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.uploads import bp as uploads_bp
    app.register_blueprint(uploads_bp, url_prefix='/uploads')

    from app.news import bp as news_bp
    app.register_blueprint(news_bp, url_prefix='/news')

    from app.defectura import bp as defectura_bp
    app.register_blueprint(defectura_bp, url_prefix='/defectura')

    from app.empl_manage import bp as empl_bp
    app.register_blueprint(empl_bp, url_prefix='/empl_manage')

    from app.schedule import bp as schedule_bp
    app.register_blueprint(schedule_bp, url_prefix='/schedule')

    return app
