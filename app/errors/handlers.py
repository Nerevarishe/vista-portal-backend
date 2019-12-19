from flask import jsonify, make_response, g
from app.errors import bp

from utils.check import is_g_obj_custom_http_error_msg_exist


# TODO: Implement custom error msg to all errors handlers

@bp.app_errorhandler(400)
def bad_request(error):
    return make_response(jsonify({
        'error': '400 Bad Request'
    })), 400


@bp.app_errorhandler(401)
def unauthorized(error):
    return make_response(jsonify({
        'error': '401 Unauthorized'
    })), 401


@bp.app_errorhandler(404)
def not_found(error):
    return make_response(jsonify({
        'error': '404 Not Found'
    })), 404


@bp.app_errorhandler(405)
def method_not_allowed(error):
    return make_response(jsonify({
        'error': '405 Method Not Allowed'
    })), 405


@bp.app_errorhandler(409)
def conflict(error):
    if is_g_obj_custom_http_error_msg_exist():
        msg = g.custom_http_error_msg
        return make_response(jsonify({
            'error': '409 ' + msg
        })), 409

    return make_response(jsonify({
        'error': '409 Conflict'
    })), 409


@bp.app_errorhandler(500)
def internal_server_error(error):
    return make_response(jsonify({
        'error': '500 Internal Server Error'
    })), 500
