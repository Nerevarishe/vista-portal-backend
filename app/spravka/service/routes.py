from flask import jsonify, request, abort, current_app

from app.spravka import bp
from app.models import ServiceCenterList


@bp.route('/service/', methods=['GET'])
def get_all_services():
    pass


@bp.route('/service/<service_id>', methods=['GET'])
def get_service(service_id):
    pass


@bp.route('/service/', methods=['POST'])
def add_service():
    pass


@bp.route('/service/<service_id>', methods=['PUT'])
def update_service(service_id):
    pass


@bp.route('/services/<service_id>', methods=['DELETE'])
def delete_service(service_id):
    pass
