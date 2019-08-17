from flask import jsonify, request, abort, current_app

from app.spravka import bp
from app.models import DrugstoreList


@bp.route('/drugstores/', metods=['GET'])
def get_all_drugstores():
    pass


@bp.route('/drugstores/<drugstore_id>', methods=['GET'])
def get_drugstore(drugstore_id):
    pass


@bp.route('/drugstores/', methods=['POST'])
def add_drugstore():
    pass


@bp.route('/drugstores/<drugstore_id>', methods=['PUT'])
def update_drugstore(drugstore_id):
    pass


@bp.route('/drugstores/<drugstore_id>', methods=['DELETE'])
def delete_drugstore(drugstore_id):
    pass
