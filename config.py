import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'you-will-never-guess-jwt'
    STATIC_FOLDER = os.path.join(basedir, 'static')

    # Flask-MongoEngine Settings
    MONGODB_DB = 'vista_portal_api'
    # TODO: Remove on production!
    MONGODB_HOST = '192.168.1.11'
    # MONGODB_HOST = '10.0.0.1'
    # MONGODB_HOST = 'mongo'
    # MONGODB_USERNAME = os.environ.get('MONGO_INITDB_ROOT_USERNAME') or ''
    # MONGODB_PASSWORD = os.environ.get('MONGO_INITDB_ROOT_PASSWORD') or ''

    # News posts per page
    NEWS_POST_PER_PAGE = 3

    # Uploads DIR
    UPLOAD_PATH = os.path.join(STATIC_FOLDER, 'uploads')

    # Flask-Uploads
    UPLOADS_DEFAULT_DEST = UPLOAD_PATH
    UPLOADS_DEFAULT_URL = 'http://localhost:5000/static/uploads/'
