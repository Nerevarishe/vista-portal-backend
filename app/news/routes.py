from flask import jsonify, request, abort, current_app

from datetime import datetime

from app.news import bp
from app.models import NewsPost

from utils.check import is_request_json_field_exist


@bp.route('/', methods=['GET'])
def get_news_posts():

    """ Return paginated news posts """

    # Set page and per_page vars from request for pagination or use default values
    page = 1
    per_page = current_app.config['NEWS_POST_PER_PAGE']

    if 'page' in request.args and request.args['page'] != '':
        page = int(request.args['page'])
    if 'perPage' in request.args and request.args['per_page'] != '':
        per_page = int(request.args['per_page'])

    # Get paginated posts page
    _posts = []
    posts = NewsPost.objects.order_by('-date_created').paginate(page=page, per_page=per_page)
    for post in posts.items:
        _posts.append(post)

    return jsonify({
        "posts": _posts,
        "postsPageHasNext": posts.has_next,
        "postsPageNextPageNumber": posts.next_num,
        "postsPageHasPrev": posts.has_prev,
        "postsPagePrevPageNumber": posts.prev_num,
        "dateCreated": '',
        "dateEdited": ''
    })


@bp.route('/<news_post_id>', methods=['GET'])
def get_news_post(news_post_id):

    """ Return one record by it ID """

    post = NewsPost.objects.get_or_404(id=news_post_id)
    return jsonify({
        "post": post,
        "dateCreated": '',
        "dateEdited": ''
    })


@bp.route('/', methods=['POST'])
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
def update_news_post(news_post_id):

    """ Update record by it ID and return OK """

    if 'postBody' in request.json and request.json['postBody'] != '':
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
def delete_news_post(news_post_id):

    """ Delete record by it ID and return OK """

    post = NewsPost.objects.get_or_404(id=news_post_id)
    post.delete()
    return jsonify({
        "msg": "OK"
    })
