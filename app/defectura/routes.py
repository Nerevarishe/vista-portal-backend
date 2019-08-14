from flask import jsonify, request, abort, current_app

from app.defectura import bp
from app.models import DefecturaCard


@bp.route('/', methods=['GET'])
def get_def_records():

    """ Return all defectura cards """

    records = DefecturaCard.objects
    records_list = records.filter(in_zd=False).order_by('-date')
    records_list_in_zd = records.filter(in_zd=True).order_by('drug_name')

    return jsonify({
        'drugs_in_zd': records_list_in_zd,
        'drugs': records_list
    })


@bp.route('/', methods=['POST'])
def create_new_def_record():

    """ Create new defectura record and return it ID """

    # DefecturaCard.drop_collection()

    record1 = DefecturaCard()
    record1.drug_name = '5-НОК : таб п/об 50мг n50'
    record1.comment = 'спрос'
    record1.employee_name = 'Олег'
    record1.save()

    record2 = DefecturaCard()
    record2.drug_name = 'ГЕПАЗОЛОН : супп. рект. n10'
    record2.comment = 'спрос'
    record2.employee_name = 'Олег'
    record2.save()

    record3 = DefecturaCard()
    record3.drug_name = 'АКВА МАРИС : устройство д/промывания носа + соль (саше) n30'
    record3.comment = 'спрос'
    record3.employee_name = 'Олег'
    record3.save()

    record4 = DefecturaCard()
    record4.drug_name = 'АКРИДЕРМ ГК : крем (туба) 15г'
    record4.comment = 'спрос'
    record4.employee_name = 'Олег'
    record4.save()

    record5 = DefecturaCard()
    record5.drug_name = 'АЛМОНТ : таб жев. 5мг n28'
    record5.comment = 'спрос'
    record5.employee_name = 'Олег'
    record5.save()

    record6 = DefecturaCard()
    record6.drug_name = 'АМБРОБЕНЕ : р-р орал. (фл.) 7.5мг/мл - 40мл n1'
    record6.comment = 'спрос'
    record6.employee_name = 'Олег'
    record6.save()

    record7 = DefecturaCard()
    record7.drug_name = 'АММИАК : р-р 10% 100мл'
    record7.comment = 'спрос'
    record7.employee_name = 'Олег'
    record7.save()

    record8 = DefecturaCard()
    record8.drug_name = 'АНАФЕРОН : взрослый таб n20'
    record8.comment = 'спрос'
    record8.employee_name = 'Олег'
    record8.save()

    record9 = DefecturaCard()
    record9.drug_name = 'АПИЗАРТРОН : мазь 20г'
    record9.comment = 'спрос'
    record9.employee_name = 'Олег'
    record9.save()

    record10 = DefecturaCard()
    record10.drug_name = 'АРТРОКЕР : капс. 50мг n30'
    record10.comment = 'спрос'
    record10.employee_name = 'Олег'
    record10.save()

    record11 = DefecturaCard()
    record11.drug_name = 'АРТРОКЕР : капс. 50мг n30'
    record11.comment = 'спрос'
    record11.employee_name = 'Олег'
    record11.in_zd = True
    record11.save()

    record12 = DefecturaCard()
    record12.drug_name = 'АРТРОКЕР : капс. 50мг n30'
    record12.comment = 'спрос'
    record12.employee_name = 'Олег'
    record12.save()

    record13 = DefecturaCard()
    record13.drug_name = 'АРТРОКЕР : капс. 50мг n30'
    record13.comment = 'спрос'
    record13.employee_name = 'Олег'
    record13.save()

    record14 = DefecturaCard()
    record14.drug_name = 'АРТРОКЕР : капс. 50мг n30'
    record14.comment = 'спрос'
    record14.employee_name = 'Олег'
    record14.save()

    record15 = DefecturaCard()
    record15.drug_name = 'АРТРОКЕР : капс. 50мг n30'
    record15.comment = 'спрос'
    record15.employee_name = 'Олег'
    record15.save()

    return 'true'


@bp.route('/<record_id>', methods=['DELETE'])
def delete_def_record(record_id):
    pass


@bp.route('/<record_id>', methods=['PUT'])
def toggle_zd(record_id):
    pass
