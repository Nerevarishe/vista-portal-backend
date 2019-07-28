from flask import jsonify, make_response
from app.errors import bp


@bp.app_errorhandler(400)
def bad_request(error):
    return make_response(jsonify({
        'error': '400 Bad Request'
    })), 400


@bp.app_errorhandler(401)
def not_found(error):
    return make_response(jsonify({
        'error': '401 Unauthorized'
    })), 401


@bp.app_errorhandler(404)
def not_found(error):
    return make_response(jsonify({
        'error': '404 Not Found'
    })), 404


@bp.app_errorhandler(500)
def bad_request(error):
    return make_response(jsonify({
        'error': '500 Internal Server Error'
    })), 500
