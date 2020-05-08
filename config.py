import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'you-will-never-guess-jwt'
    STATIC_FOLDER = os.path.join(basedir, 'static')

    # Flask-MongoEngine Settings
    MONGODB_DB = 'vista-portal'
    MONGODB_HOST = 'db'
    # MONGODB_USERNAME = os.environ.get('MONGO_INITDB_ROOT_USERNAME') or ''
    # MONGODB_PASSWORD = os.environ.get('MONGO_INITDB_ROOT_PASSWORD') or ''
    # MONGODB_USERNAME = 'vista-portal'
    # MONGODB_PASSWORD = 'rfh98LKJh4a0x9u4Ld893mak211j'

    # News posts per page
    NEWS_POST_PER_PAGE = 3

    # Uploads DIR
    UPLOAD_PATH = os.path.join(STATIC_FOLDER, 'uploads')

    # Flask-Uploads
    UPLOADS_DEFAULT_DEST = UPLOAD_PATH
    UPLOADS_DEFAULT_URL = 'http://192.168.56.112:5000/static/uploads/'


class TestConfig(Config):
    TESTING = True

    # Flask-MongoEngine Settings
    MONGODB_DB = 'vista-portal-backend-test'
    # TODO: Remove on production!
    MONGODB_HOST = '10.0.0.1'

