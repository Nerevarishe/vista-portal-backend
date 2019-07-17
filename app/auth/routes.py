from flask import jsonify, request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
# from flask_mongoengine import BaseQuerySet

from app.models import User
from app.auth import bp


@bp.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({
            'msg': 'Missing JSON in request 400'
        }), 400
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username or not password:
        return jsonify({
            'msg': 'Missing username or password parameter 400'
        }), 400
    user = User.objects.get(username=username)
    if not user or user.check_password(password):
        return jsonify({
            'msg': 'Invalid username or password 401'
        }), 401
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200


@bp.route('/logout', methods=['POST'])
@jwt_required
def logout():
    return 'protected by JWT'
