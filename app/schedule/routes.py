from flask import jsonify, request, abort

from app.schedule import bp
from app.models import Schedule, Employee

from datetime import datetime, timedelta

from utils.check import is_request_json_field_exist, is_request_args_field_exist


# Get last day of schedule for selected month
def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + timedelta(days=4)
    return next_month - timedelta(days=next_month.day)


@bp.route('/', methods=['GET'])
def get_schedule():

    """
    By default get schedule for current month.
    Can be changed by setting arguments in get request
    """
    pass


@bp.route('/', methods=['POST'])
def generate_schedule():

    """
    Generate new schedule from json data from request
    year and month - of month that need to be generated,
    employeeIds - employees ID's
    shiftStartTime - Time to start employee's work day
    firstDateOfShift - What is the first employee shift date in a month
    isFirstDayOfShift, isSecondDayOfShift if firstDateOfShift get in first day of 2\2 shift, or second day
    """
    if is_request_json_field_exist('employeeIds') and is_request_json_field_exist('year') \
            and is_request_json_field_exist('month'):
        year = request.json['year']
        month = request.json['month']
        date_object = datetime(year=year, month=month, day=1)
        days_in_month = last_day_of_month(date_object).day
        for employee_id, info in request.json['employeeIds'].items():
            # Get employee from DB
            employee = Employee.objects.get_or_404(id=employee_id)
            # Make variables from json fields
            shift_start_time = info['shiftStartTime']
            first_date_of_shift = info['firstDateOfShift']
            is_first_day_of_shift = info['isFirstDayOfShift']
            is_second_day_of_shift = info['isSecondDayOfShift']
            # Set day counter to zero
            day_counter = 0
            # For day in range of days in month plus one day - because range func start count from zero
            for day in range(days_in_month + 1):
                # Skip day 0 and all days before first date of shift
                if day < first_date_of_shift or day == 0:
                    continue
                # If firs day of 2/2 shift schedule:
                if is_first_day_of_shift:
                    if day_counter == 0 or day_counter < 2:
                        schedule = Schedule()
                        schedule.employee = employee
                        schedule.work_day = datetime(year=year, month=month, day=day).date()
                        schedule.shift_start_time = int(shift_start_time)
                        schedule.save()
                        day_counter += 1
                    # If day counter equally 4, then this last weekend day - set it to zero
                    if day_counter == 4:
                        day_counter = 0
                    # If day counter equally or bigger than 2, then weekend starts:
                    elif day_counter >= 2:
                        day_counter += 1

                # If second day of 2/2 shift schedule:
                elif is_second_day_of_shift:
                    # Set day counter to 2, because this last work day of 2/2 shift
                    day_counter = 2
                    schedule = Schedule()
                    schedule.employee = employee
                    schedule.work_day = datetime(year=year, month=month, day=day).date()
                    schedule.shift_start_time = int(shift_start_time)
                    schedule.save()
                    day_counter += 1
                    # Reverse to first day of shift flow
                    is_second_day_of_shift = False
                    is_first_day_of_shift = True
        return 'DONE!'
    abort(400)
