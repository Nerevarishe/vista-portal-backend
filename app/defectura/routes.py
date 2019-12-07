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


@bp.route('/<record_id>', methods=['GET'])
def get_def_record(record_id):

    """ Return one defectura record by it ID """

    record = DefecturaCard.objects.get_or_404(id=record_id)

    return jsonify({
        'drug': record
    })


@bp.route('/', methods=['POST'])
def create_new_def_record():

    """ Create new defectura record and return it ID """

    record = DefecturaCard()
    try:
        if request.json['drugName'] != '' and request.json['employeeName'] != '':
            record.drug_name = request.json['drugName']
            record.employee_name = request.json['employeeName']
    except KeyError:
        abort(400)
    else:
        try:
            if 'comment' in request.json:
                record.comment = request.json['comment']
            if 'inZd' in request.json:
                record.in_zd = request.json['inZd']
        except KeyError:
            pass

        record.save()
        return jsonify({
            "msg": "OK",
            "recordId": str(record.id)
        }), 201
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
