from flask import jsonify, request, abort, current_app
from flask_jwt_extended import jwt_required

from datetime import datetime

from app.news import bp
from app.models import NewsPost

from utils.check import is_request_json_field_exist, is_request_args_field_exist


@bp.route('/', methods=['GET'])
def get_news_posts():

    """ Return paginated news posts """

    # Set page and per_page vars from request for pagination or use default values
    page = 1
    per_page = current_app.config['NEWS_POST_PER_PAGE']

    if is_request_args_field_exist('page'):
        page = int(request.args['page'])
    if is_request_args_field_exist('per_page'):
        per_page = int(request.args['per_page'])

    # Get paginated posts page
    _posts = []

    # Get all paginated posts ordered by date descending and add them to _posts list
    posts = NewsPost.objects.order_by('-date_created').paginate(page=page, per_page=per_page)
    for post in posts.items:
        _posts.append(post)

    return jsonify({
        "posts": _posts,
        "postsPageHasNext": posts.has_next,
        "postsPageNextPageNumber": posts.next_num,
        "postsPageHasPrev": posts.has_prev,
        "postsPagePrevPageNumber": posts.prev_num
    })


@bp.route('/<news_post_id>', methods=['GET'])
def get_news_post(news_post_id):

    """ Return one record by it ID """

    post = NewsPost.objects.get_or_404(id=news_post_id)
    return jsonify({
        "post": post
    })


@bp.route('/', methods=['POST'])
@jwt_required
def add_news_post():

    """ Return created record ID """

    if is_request_json_field_exist('postBody') and request.json['postBody'] != '':
        post = NewsPost()
        post.post_body = request.json['postBody']
        post.save()

        return jsonify({
            "msg": "OK",
            "postId": str(post.id)
        }), 201
    abort(400)


@bp.route('/<news_post_id>', methods=['PUT'])
@jwt_required
def update_news_post(news_post_id):

    """ Update record by it ID and return OK """

    if is_request_json_field_exist('postBody') and request.json['postBody'] != '':
        post = NewsPost.objects.get_or_404(id=news_post_id)
        if post.post_body != request.json['postBody']:
            post.post_body = request.json['postBody']
            post.date_edited = datetime.utcnow()
            post.save()

            return jsonify({
                "msg": "OK"
            })
        return jsonify({
            "msg": "OK"
        })
    abort(400)


@bp.route('/<news_post_id>', methods=['DELETE'])
@jwt_required
def delete_news_post(news_post_id):

    """ Delete record by it ID and return OK """

    post = NewsPost.objects.get_or_404(id=news_post_id)
    post.delete()
    return jsonify({
        "msg": "OK"
    })
