from flask import jsonify, request, abort, current_app

from app.spravka import bp
from app.models import Drugstore


@bp.route('/drugstores/', methods=['GET'])
def get_all_drugstores():

    """ Return list of all drugstores """

    drugstores = Drugstore.objects.all()

    return jsonify({
        "drugstores": drugstores
    })


@bp.route('/drugstores/<drugstore_id>', methods=['GET'])
def get_drugstore(drugstore_id):

    """ Return one drugstore by it ID """

    drugstore = Drugstore.objects.get_or_404(id=drugstore_id)

    return jsonify({
        "drugstore": drugstore
    })


@bp.route('/drugstores/', methods=['POST'])
def add_drugstore():

    """ Return created drugstore ID """

    drugstore = Drugstore()
    drugstore_model_fields = []

    for field in dir(Drugstore):
        if field[:2] == 'ds':
            drugstore_model_fields.append(field)

    for field in drugstore_model_fields:
        drugstore[field] = request.json[field]
    drugstore.save()

    return jsonify({
            'msg': 'OK',
            'id': str(drugstore.id)
    })


@bp.route('/drugstores/<drugstore_id>', methods=['PUT'])
def update_drugstore(drugstore_id):
    pass


@bp.route('/drugstores/<drugstore_id>', methods=['DELETE'])
def delete_drugstore(drugstore_id):
    pass
