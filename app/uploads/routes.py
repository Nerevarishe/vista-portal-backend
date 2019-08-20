from flask import jsonify, request, abort, url_for
from flask_uploads import UploadNotAllowed

from uuid import uuid4

from app import images
from app.uploads import bp


@bp.route('/', methods=['POST'])
def upload():
    image = request.files.get('image')

    if not image:
        abort(400)

    # Rename file to random filename:
    file = image.filename.split('.')
    extension = file.pop()
    new_filename = str(uuid4())
    image.filename = '.'.join([new_filename, extension])

    try:
        images.save(image)
    except UploadNotAllowed:
        abort(403)
    else:
        return jsonify({
            "msg": "OK",
        }), 201
    abort(400)


