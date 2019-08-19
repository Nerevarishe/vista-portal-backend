from flask import jsonify, request, abort

from app.spravka import bp
from app.models import Drugstore


@bp.route('/drugstores/', methods=['GET'])
def get_all_drugstores():

    """ Return created record ID """

    drugstores = Drugstore.objects.all()

    return jsonify({
        "drugstores": drugstores
    })


@bp.route('/drugstores/<drugstore_id>', methods=['GET'])
def get_drugstore(drugstore_id):

    """ Return one record by it ID """

    drugstore = Drugstore.objects.get_or_404(id=drugstore_id)

    return jsonify({
        "drugstore": drugstore
    })


@bp.route('/drugstores/', methods=['POST'])
def add_drugstore():

    """ Return created record ID """

    drugstore = Drugstore()

    for field in Drugstore.fields(Drugstore):
        if field not in request.json:
            abort(400)
        drugstore[field] = request.json[field]
    drugstore.save()

    return jsonify({
            'msg': 'OK',
            'id': str(drugstore.id)
    }), 201


@bp.route('/drugstores/<drugstore_id>', methods=['PUT'])
def update_drugstore(drugstore_id):

    """ Update record by it ID and return OK """

    drugstore = Drugstore.objects.get_or_404(id=drugstore_id)
    need_write_to_db = False

    for field in Drugstore.fields(Drugstore):
        if field not in request.json:
            abort(400)

        if drugstore[field] != request.json[field]:
            drugstore[field] = request.json[field]
            need_write_to_db = True

    if need_write_to_db:
        drugstore.save()

    return jsonify({
        "msg": "OK"
    })


@bp.route('/drugstores/<drugstore_id>', methods=['DELETE'])
def delete_drugstore(drugstore_id):

    """ Delete record by it ID and return OK """

    drugstore = Drugstore.objects.get_or_404(id=drugstore_id)
    drugstore.delete()

    return jsonify({
        "msg": "OK"
    })
