from flask import jsonify, request, abort, current_app
# from flask_jwt_extended import jwt_required, get_jwt_identity

from app.news import bp
from app.models import NewsPost


@bp.route('/', methods=['GET'])
def get_news_posts():
    """ Return paginated news posts """
    return jsonify({
        "msg": "get_news_posts"
    })


@bp.route('/<news_post_id>', methods=['GET'])
def get_news_post(news_post_id):
    """ Return one News post by it ID """
    return jsonify({
        "msg": "get_news_post"
    })


@bp.route('/', methods=['POST'])
def add_news_post():
    """ Return status 201 if post added to DB """
    return jsonify({
        "msg": "add_news_post"
    })


@bp.route('/<news_post_id>', methods=['PUT'])
def update_news_post(news_post_id):
    """ Return True if post updated """
    return jsonify({
        "msg": "update_news_post"
    })


@bp.route('/<news_post_id>', methods=['DELETE'])
def delete_news_post(news_post_id):
    """ Return True if post deleted """
    return jsonify({
        "msg": "delete_news_post"
    })
