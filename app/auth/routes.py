from flask import jsonify, request, abort
from flask_jwt_extended import jwt_required, jwt_refresh_token_required, get_jwt_identity, create_access_token, \
    create_refresh_token

from app.auth import bp
from app.models import User


@bp.route('/login', methods=['POST'])
def login():
    if not request.json['username'] or not request.json['password']:
        abort(400)
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    try:
        user = User.objects.get(username=username)
    except:
        abort(401)
    else:
        if user.check_password(password):
            access_token = create_access_token(identity=username)
            refresh_token = create_refresh_token(identity=username)
            user.refresh_token = refresh_token
            user.save()
            return jsonify(access_token=access_token, refresh_token=refresh_token)


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
