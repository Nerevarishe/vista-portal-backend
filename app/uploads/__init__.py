from flask import Blueprint


bp = Blueprint('uploads', __name__)

from app.uploads import routes
