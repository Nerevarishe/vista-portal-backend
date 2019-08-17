from flask import Blueprint


bp = Blueprint('spravka', __name__)

from app.spravka import routes
