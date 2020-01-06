from flask import jsonify, request, abort
from flask_uploads import UploadNotAllowed

from uuid import uuid4

from app import images
from app.uploads import bp
from flask import current_app

@bp.route('/', methods=['POST'])
def upload():
    image = request.files.get('upload')

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
            "url": current_app.config['UPLOADS_DEFAULT_URL'] + 'images/' + image.filename
        }), 201
    abort(400)


