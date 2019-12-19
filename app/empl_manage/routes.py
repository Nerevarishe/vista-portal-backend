from flask import jsonify, request, abort

from app.empl_manage import bp
from app.models import Employee

from datetime import datetime
from utils.check import is_request_json_field_exist, is_request_args_field_exist


@bp.route('/', methods=['GET'])
def get_all_employees():

    """ Get all employees """

    employees = Employee.objects.order_by('last_name')

    if is_request_args_field_exist('active'):
        if request.args['active'] == 'false':
            return jsonify({
                'employees': employees.filter(active=False)
            })
        return jsonify({
            'employees': employees.filter(active=True)
        })

    return jsonify({
        'employees': employees
    })


@bp.route('/<employee_id>', methods=['GET'])
def get_employee(employee_id):

    """ Get employee by ID"""

    employee = Employee.objects.get_or_404(id=employee_id)

    return jsonify({
        'employee': employee
    })


@bp.route('/', methods=['POST'])
def create_employee():

    """ Create new employee """

    employee = Employee()

    if is_request_json_field_exist('firstName') and is_request_json_field_exist('lastName'):
        employee.first_name = request.json['firstName']
        employee.last_name = request.json['lastName']
        if is_request_json_field_exist('patronymic'):
            employee.patronymic = request.json['patronymic']
        if is_request_json_field_exist('prefferedTime'):
            employee.preffered_time = request.json['prefferedTime']
        employee.save()

        return jsonify({
            'msg': 'OK',
            'employeeId': str(employee.id)
        }), 201
    abort(400)


@bp.route('/<employee_id>', methods=['PUT'])
def edit_employee(employee_id):

    """ Edit employee """

    employee = Employee.objects.get_or_404(id=employee_id)

    if is_request_json_field_exist('firstName') and is_request_json_field_exist('lastName'):
        employee.first_name = request.json['firstName']
        employee.last_name = request.json['lastName']
        if is_request_json_field_exist('patronymic'):
            employee.patronymic = request.json['patronymic']
        if is_request_json_field_exist('prefferedTime'):
            employee.preffered_time = request.json['prefferedTime']
        if is_request_json_field_exist('active'):
            employee.active = request.json['active']
        if is_request_json_field_exist('dateOfDismissal'):
            employee.date_of_dismissal = request.json['dateOfDismissal']
        if is_request_json_field_exist('vacationDays'):
            employee.vacation_days = request.json['vacationDays']
        employee.date_edited = datetime.utcnow()
        employee.save()

        return jsonify({
            'msg': 'OK'
        })
    abort(400)


@bp.route('/<employee_id>/act_toggle', methods=['PUT'])
def activation_toggle(employee_id):

    """ Change activetion status of employee """

    employee = Employee.objects.get_or_404(id=employee_id)
    employee.active = not employee.active
    employee.date_edited = datetime.utcnow()
    employee.save()
    return jsonify({
        'msg': 'OK'
    })
