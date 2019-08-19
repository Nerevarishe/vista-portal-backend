from flask import jsonify, request, abort

from app.spravka import bp
from app.models import ServiceCenter


@bp.route('/service/', methods=['GET'])
def get_all_services():

    """ Return all records """

    service_centers = ServiceCenter.objects.all()

    return jsonify({
        "service_centers": service_centers
    })


@bp.route('/service/<service_id>', methods=['GET'])
def get_service(service_id):

    """ Return one record by it ID """

    service_center = ServiceCenter.objects.get_or_404(id=service_id)

    return jsonify({
        "service_center": service_center
    })


@bp.route('/service/', methods=['POST'])
def add_service():

    """ Return created record ID """

    service_center = ServiceCenter()

    for field in ServiceCenter.fields(ServiceCenter):
        if field not in request.json:
            abort(400)
        service_center[field] = request.json[field]
    service_center.save()

    return jsonify({
        "msg": "OK",
        "id": str(service_center.id)
    }), 201


@bp.route('/service/<service_id>', methods=['PUT'])
def update_service(service_id):

    """ Update record by it ID and return OK """

    service_center = ServiceCenter.objects.get_or_404(id=service_id)
    need_write_to_db = False

    for field in ServiceCenter.fields(ServiceCenter):
        if field not in request.json:
            abort(400)

        if service_center[field] != request.json[field]:
            service_center[field] = request.json[field]
            need_write_to_db = True

    if need_write_to_db:
        service_center.save()

    return jsonify({
        "msg": "OK",
    })


@bp.route('/service/<service_id>', methods=['DELETE'])
def delete_service(service_id):

    """ Delete record by it ID and return OK """

    service_center = ServiceCenter.objects.get_or_404(id=service_id)
    service_center.delete()

    return jsonify({
        "msg": "OK"
    })
