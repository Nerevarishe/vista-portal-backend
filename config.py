import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'you-will-never-guess-jwt'
    STATIC_FOLDER = os.path.join(basedir, 'static')

    # Flask-MongoEngine Settings
    MONGODB_DB = 'vista_api'
    # MONGODB_HOST = '192.168.1.11'
    MONGODB_HOST = '10.0.0.1'

    # News posts per page
    NEWS_POST_PER_PAGE = 5

    # Uploads DIR
    UPLOAD_PATH = os.path.join(STATIC_FOLDER, 'uploads')

    # Flask-Uploads
    UPLOADS_DEFAULT_DEST = UPLOAD_PATH
    UPLOADS_DEFAULT_URL = 'http://localhost:5000/static/uploads/'
