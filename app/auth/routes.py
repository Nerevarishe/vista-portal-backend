from flask import jsonify, request, abort, g
from flask_jwt_extended import jwt_required, jwt_refresh_token_required, get_jwt_identity, create_access_token, \
    create_refresh_token

from flask_mongoengine import DoesNotExist
from app.auth import bp
from app.models import User
from utils.check import is_request_json_field_exist


@bp.route('/register', methods=['POST'])
def register():
    if is_request_json_field_exist('username') and is_request_json_field_exist('password'):
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        access_token = create_access_token(identity=username)
        refresh_token = create_refresh_token(identity=username)

        # Check username already exist
        try:
            User.objects.get(username=username)
        except DoesNotExist:
            user = User(username=username, refresh_token=refresh_token)
            user.hash_password(password=password)
            user.save()
            return jsonify(userId=str(user.id), username=username, access_token=access_token,
                           refresh_token=refresh_token), 201
        g.custom_http_error_msg = 'User already exist'
        abort(409)


@bp.route('/login', methods=['POST'])
def login():
    if is_request_json_field_exist('username') and is_request_json_field_exist('password'):
        username = request.json.get('username', None)
        password = request.json.get('password', None)

        user = User.objects.get_or_404(username=username)
        if user.check_password(password):
            access_token = create_access_token(identity=username)
            refresh_token = create_refresh_token(identity=username)
            user.refresh_token = refresh_token
            user.save()
            return jsonify(access_token=access_token, refresh_token=refresh_token)
        abort(401)
    abort(400)


@bp.route('/logout', methods=['DELETE'])
@jwt_required
def logout():
    current_user = User.objects.get_or_404(username=get_jwt_identity())
    current_user.refresh_token = ''
    current_user.save()

    return 'logout page'


@bp.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh_tokens():
    current_user = User.objects.get_or_404(username=get_jwt_identity())

    if request.headers['Authorization'].split(' ')[1] == current_user.refresh_token:
        access_token = create_access_token(identity=current_user.username)
        refresh_token = create_refresh_token(identity=current_user.username)
        current_user.refresh_token = refresh_token
        current_user.save()
        return jsonify(access_token=access_token, refresh_token=refresh_token)
    abort(401)


@bp.route('/test', methods=['GET'])
@jwt_required
def test_route():
    return jsonify({
        'msg': 'ok',
        'destination': 'test auth route'
    }), 200
