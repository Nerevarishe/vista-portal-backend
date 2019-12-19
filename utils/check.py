from flask import request, g


def is_request_json_field_exist(field):
    if request.json:
        try:
            if request.json[field] or request.json[field] == False:
                return True
        except KeyError:
            return False
    return False


def is_request_args_field_exist(field):
    if request.args:
        try:
            if request.args[field] and request.args[field] != '':
                return True
        except KeyError:
            return False
    return False


def is_g_obj_custom_http_error_msg_exist():
    try:
        g.custom_http_error_msg
    except AttributeError:
        return False
    else:
        return True
