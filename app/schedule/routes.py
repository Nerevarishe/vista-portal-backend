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
    shiftType - type of employee shift: 22 (2/2) - 2 work days, 2 weekends, 52 (5/2) - 5 work days, 2 weekends
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
            # If all work, then update employee document with new data
            can_update_employee_document = False
            # Make variables from json fields
            # TODO: Implement checks if this fields exists
            shift_type = info['shiftType']
            shift_start_time = info['shiftStartTime']
            first_date_of_shift = datetime.strptime(info['firstDateOfShift'],
                                                    '%Y-%m-%d').date()  # info['firstDateOfShift']
            is_first_day_of_shift = info['isFirstDayOfShift']
            is_second_day_of_shift = info['isSecondDayOfShift']
            # If vacation in this month
            vacation_start_date = datetime.strptime(info['vacationStartDate'], '%Y-%m-%d').date()
            vacation_end_date = datetime.strptime(info['vacationEndDate'], '%Y-%m-%d').date()
            # Calc vacation days
            vacation_days = (vacation_end_date - vacation_start_date).days
            # Set day counter to zero
            day_counter = timedelta(days=0)
            # Get number of day in week to set day counter for 5/2 shift:
            if shift_type == 52:
                day_counter = timedelta(days=datetime(year, month, first_date_of_shift.day).weekday())
            # For day in range of days in month plus one day - because range func start count from zero
            for day in range(days_in_month):
                day = day + 1
                # Skip all days before first date of shift or vacation
                if first_date_of_shift < vacation_start_date:
                    if datetime(year, month, day).date() < first_date_of_shift:
                        continue
                    # If day between vacation start/end dates
                    if vacation_start_date <= datetime(year, month, day).date() <= vacation_end_date:
                        schedule = Schedule()
                        schedule.employee = employee
                        schedule.shift_start_time = 0
                        schedule.vacation_day = datetime(year=year, month=month, day=day).date()
                        schedule.save()
                        # if employee in 5/2 shift
                        if shift_type == 52:
                            # Set date counter to next week day from last vacation day
                            day_counter = timedelta(days=(datetime(year, month, vacation_end_date.day)
                                                          + timedelta(days=1)).weekday())
                        # if employee in 2/2 shift
                        if shift_type == 22:
                            # Set date counter to zero for first work day
                            day_counter = timedelta(days=0)
                        continue
                    # If shift type 2/2
                    if shift_type == 22:
                        # If firs day of 2/2 shift schedule:
                        if is_first_day_of_shift:
                            if day_counter == timedelta(days=0) or day_counter < timedelta(days=2):
                                schedule = Schedule()
                                schedule.employee = employee
                                schedule.work_day = datetime(year=year, month=month, day=day).date()
                                schedule.shift_start_time = shift_start_time
                                schedule.save()
                                day_counter += timedelta(days=1)
                            # If day counter equally 4, then this last weekend day - set it to zero
                            if day_counter == timedelta(days=4):
                                day_counter = timedelta(days=0)
                            # If day counter equally or bigger than 2, then weekend starts:
                            elif day_counter >= timedelta(days=2):
                                day_counter += timedelta(days=1)

                        # If second day of 2/2 shift schedule:
                        elif is_second_day_of_shift:
                            # Set day counter to 2, because this last work day of 2/2 shift
                            day_counter = timedelta(days=2)
                            schedule = Schedule()
                            schedule.employee = employee
                            schedule.work_day = datetime(year=year, month=month, day=day).date()
                            schedule.shift_start_time = shift_start_time
                            schedule.save()
                            day_counter += timedelta(days=1)
                            # Reverse to first day of shift flow
                            is_second_day_of_shift = False
                            is_first_day_of_shift = True
                    # If shift type 5/2
                    if shift_type == 52:
                        # If day counter < 5 - then this work days
                        if day_counter.days < 5:
                            schedule = Schedule()
                            schedule.employee = employee
                            schedule.work_day = datetime(year=year, month=month, day=day).date()
                            schedule.shift_start_time = shift_start_time
                            schedule.save()
                            day_counter += timedelta(days=1)
                        # If day counter >= 5 - then weekends start
                        elif day_counter.days >= 5:
                            day_counter += timedelta(days=1)
                        # If day counter equals 7 - weekends end, start new work week
                        if day_counter.days == 7:
                            day_counter = timedelta(days=0)
                    can_update_employee_document = True
                else:
                    pass

            # If all done - update employee document
            if can_update_employee_document:
                # Change vacation days and set vacation dates in employee document:
                employee.update(add_to_set__vacation_dates=[employee.VacationDates(
                    vacation_start_date=vacation_start_date,
                    vacation_end_date=vacation_end_date
                )])
                employee.vacation_days -= vacation_days
                employee.date_edited = datetime.utcnow()
                employee.save()
        return 'DONE!'
    abort(400)
