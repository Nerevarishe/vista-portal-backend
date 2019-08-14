from flask import Blueprint


bp = Blueprint('defectura', __name__)

from app.defectura import routes
