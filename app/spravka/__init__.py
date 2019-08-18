from flask import Blueprint


bp = Blueprint('spravka', __name__)

from app.spravka.drugstores import routes
from app.spravka.service import routes
