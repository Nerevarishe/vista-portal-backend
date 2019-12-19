from flask import jsonify, request, abort

from app.defectura import bp
from app.models import DefecturaCard

from utils.check import is_request_json_field_exist


@bp.route('/', methods=['GET'])
def get_def_records():

    """ Return all defectura cards """

    records = DefecturaCard.objects
    records_list = records.filter(in_zd=False).order_by('-date')
    records_list_in_zd = records.filter(in_zd=True).order_by('drug_name')

    return jsonify({
        'drugsInZd': records_list_in_zd,
        'drugs': records_list
    })


@bp.route('/', methods=['POST'])
def create_new_def_record():

    """ Create new defectura record and return it ID """

    record = DefecturaCard()

    if is_request_json_field_exist('drugName') and is_request_json_field_exist('employeeName'):
        record.drug_name = request.json['drugName']
        record.employee_name = request.json['employeeName']
        if is_request_json_field_exist('comment'):
            record.comment = request.json['comment']
        record.save()
        return jsonify({
            'msg': 'OK',
            'recordId': str(record.id)
        })
    abort(400)


@bp.route('/<record_id>', methods=['DELETE'])
def delete_def_record(record_id):

    """ Delete one defectura record by it ID and return OK """

    record = DefecturaCard.objects.get_or_404(id=record_id)
    record.delete()

    return jsonify({
        "msg": "OK"
    })


@bp.route('/<record_id>', methods=['PUT'])
def toggle_zd(record_id):

    """ Toggle in ZD value and return OK """

    record = DefecturaCard.objects.get_or_404(id=record_id)
    record.in_zd = not record.in_zd
    record.save()

    return jsonify({
        "msg": "OK"
    })
