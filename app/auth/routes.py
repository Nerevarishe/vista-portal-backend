from flask import jsonify, request, abort, g
from flask_jwt_extended import jwt_required, jwt_refresh_token_required, get_jwt_identity, create_access_token, \
    create_refresh_token

from flask_mongoengine import DoesNotExist
from app import jwt
from app.auth import bp
from app.models import User
from utils.check import is_request_json_field_exist


@bp.route('/register', methods=['POST'])
def register():
    # If fields correct:
    if is_request_json_field_exist('username') and is_request_json_field_exist('password'):
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        role = 'user'
        if is_request_json_field_exist('role'):
            role = request.json.get('role')
        # TODO: Add check for ip4_address field exist
        ip4_address = request.headers.environ.get('REMOTE_ADDR', None) # check HTTP_X_FORWARDED_FOR

        # Check username already exist
        try:
            User.objects.get(username=username)
        # If username does not exist create new user:
        except DoesNotExist:
            refresh_token = create_refresh_token(identity=username)
            user = User(username=username, role=role, ip4_address=ip4_address, refresh_token=refresh_token)
            user.hash_password(password=password)
            user.save()
            access_token = create_access_token(identity=username)
            return jsonify(userId=str(user.id), username=username, access_token=access_token,
                           refresh_token=refresh_token), 201
        # If username exist - abort with 409 error
        g.custom_http_error_msg = 'User already exist'
        abort(409)
    # If something wrong with fields
    abort(400)


@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    user = User.objects.get_or_404(username=identity)
    return {
        'role': user.role
    }


@bp.route('/login', methods=['POST'])
def login():
    # Check if fields correct
    if is_request_json_field_exist('username') and is_request_json_field_exist('password'):
        username = request.json.get('username', None)
        password = request.json.get('password', None)

        # Try to get user from DB by username or return 404:
        user = User.objects.get_or_404(username=username)

        # Check user password and if it correct return access and refresh tokens
        if user.check_password(password):
            access_token = create_access_token(identity=username)
            refresh_token = create_refresh_token(identity=username)
            user.refresh_token = refresh_token
            user.save()
            return jsonify(access_token=access_token, refresh_token=refresh_token)
        # If password wrong return 401
        abort(401)
    # If something wrong with fields
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
