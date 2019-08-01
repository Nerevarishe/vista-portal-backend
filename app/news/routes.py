from flask import jsonify, request, abort, current_app
# from flask_jwt_extended import jwt_required, get_jwt_identity

from app.news import bp
from app.models import NewsPost


@bp.route('/', methods=['GET'])
def get_news_posts():
    """ Return paginated news posts """
    _posts = []
    next_page_url = 'next_page_url'
    prev_page_url = 'prev_page_url'

    posts = NewsPost.objects.paginate(page=1, per_page=current_app.config['NEWS_POST_PER_PAGE'])
    for post in posts.items:
        _posts.append(post)

    return jsonify({
        "posts": _posts,
        "nextPageUrl": next_page_url,
        "prevPageUrl": prev_page_url
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

    post1 = NewsPost(post_body='post 1')
    post1.save()
    post2 = NewsPost(post_body='post 2')
    post2.save()
    post3 = NewsPost(post_body='post 3')
    post3.save()
    post4 = NewsPost(post_body='post 4')
    post4.save()
    post5 = NewsPost(post_body='post 5')
    post5.save()
    post6 = NewsPost(post_body='post 6')
    post6.save()
    post7 = NewsPost(post_body='post 7')
    post7.save()
    post8 = NewsPost(post_body='post 8')
    post8.save()
    post9 = NewsPost(post_body='post 9')
    post9.save()
    post10 = NewsPost(post_body='post 10')
    post10.save()

    return jsonify({
        "msg": "Created"
    }), 201


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
