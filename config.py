import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'you-will-never-guess-jwt'

    # Flask-MongoEngine Settings
    MONGODB_DB = 'vista_api'
    MONGODB_HOST = '192.168.1.11'

    # News posts per page
    NEWS_POST_PER_PAGE = 5
