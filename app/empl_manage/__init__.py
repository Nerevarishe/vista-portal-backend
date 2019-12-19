from flask import Blueprint


bp = Blueprint('empl_manage', __name__)

from app.empl_manage import routes
