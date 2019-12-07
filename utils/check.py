from flask import request, g


def is_request_json_field_exist(field):
    if request.json:
        if request.json[field]:
            return True
        return False
    return False


def is_g_obj_custom_http_error_msg_exist():
    try:
        g.custom_http_error_msg
    except AttributeError:
        return False
    else:
        return True
