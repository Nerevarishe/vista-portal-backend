from flask import jsonify, request, abort, current_app

from app.spravka import bp
from app.models import Drugstore


@bp.route('/drugstores/', methods=['GET'])
def get_all_drugstores():

    """ Return list of all drugstores """

    drugstores = Drugstore.objects.get_or_404()

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

    drugstore = enumerate(Drugstore())
    a = 2+2



    # ds_json_fields = ['dsName', 'dsAddress', 'dsWorkTime', 'dsPhone', 'dsIpPhone']
    # ds_model_fields = ['ds_name', 'ds_address', 'ds_worktime', 'ds_phone', 'ds_ip_phone']
    #
    # for index, field in enumerate(ds_json_fields):
    #     drugstore[ds_model_fields[index]] = request.json[field]
    # drugstore.save()
    # return jsonify({
    #     "msg": "OK",
    #     "dsId": str(drugstore.id)
    # })


@bp.route('/drugstores/<drugstore_id>', methods=['PUT'])
def update_drugstore(drugstore_id):
    pass


@bp.route('/drugstores/<drugstore_id>', methods=['DELETE'])
def delete_drugstore(drugstore_id):
    pass
