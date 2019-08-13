from flask import jsonify, request, abort, current_app
# from flask_jwt_extended import jwt_required, get_jwt_identity

from app.news import bp
from app.models import NewsPost


@bp.route('/', methods=['GET'])
def get_news_posts():
    """ Return paginated news posts """

    # Set page and per_page vars from request for pagination
    page = 1
    per_page = current_app.config['NEWS_POST_PER_PAGE']

    if 'page' in request.args:
        if request.args['page'] != '':
            page = int(request.args['page'])
    if 'per_page' in request.args:
        if request.args['per_page'] != '':
            per_page = int(request.args['per_page'])

    # Get paginated posts
    _posts = []
    posts = NewsPost.objects.paginate(page=page, per_page=per_page)
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

    """ Return one News post by it ID """

    post = NewsPost.objects.get_or_404(id=news_post_id)
    return jsonify({
        "post": post
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
    post = NewsPost.objects.get_or_404(id=news_post_id)
    post.delete()
    return jsonify({
        "msg": "True"
    })
