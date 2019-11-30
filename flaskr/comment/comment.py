from flask import Blueprint
from flask import g
from flask import request
from flask import jsonify
from flask import make_response
from werkzeug.exceptions import abort

from flaskr.auth.auth import auth
from flaskr.db import get_db
from flaskr.comment.queries import (
    get_last_id, create_comment, delete_comment, get_comment, update_comment, comment_list
)

bp = Blueprint("comment", __name__,  url_prefix="/blog")


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

@bp.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@bp.errorhandler(403)
def forbidden(error):
    return make_response(jsonify({'error': 'Forbidden'}), 403)


@bp.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error':'Bad request'}), 400)


def check_comment(post_id, comment_id, check_author=True):

    comment = get_comment(get_db(), post_id, comment_id)
    if comment is None:
        abort(404)

    if check_author and comment["author_id"] != g.user["id"]:
        abort(403)

    return comment

#curl -i http://localhost:5000/blog/api/posts/1/comments
@bp.route('/api/posts/<int:post_id>/comments', methods=['GET'])
def get_comments_for_post(post_id):

    db = get_db()
    comments = comment_list(db, post_id)

    comments = [dict(row) for row in comments]

    return jsonify({'comments': comments})


@bp.route('/api/posts/<int:post_id>/comments/<int:comment_id>', methods=['GET'])
def get_comment_by_id(post_id, comment_id):

    comment = get_comment(get_db(), post_id, comment_id)

    if comment is None:
        abort(404)

    comment = dict(comment)

    return jsonify({'comment': comment})

#curl -u admin:123 -i -H "Content-Type: application/json" -X POST
# -d '{"body":"Comment body"}' http://localhost:5000/blog/api/posts/1/comments
@bp.route('/api/posts/<int:post_id>/comments', methods=['POST'])
@auth.login_required
def new_comment(post_id):

    if not request.json or not 'body' in request.json:
        abort(400)

    body = request.json['body']

    db = get_db()

    create_comment(db, body, post_id, g.user['id'])

    last_id = get_last_id(db)[0]

    comment = dict(get_comment(db, post_id, last_id))

    return jsonify({'comment': comment}), 201


@bp.route('/api/posts/<int:post_id>/comments/<int:comment_id>', methods=['PUT'])
@auth.login_required
def upd_comment(post_id, comment_id):

    comment = check_comment(post_id, comment_id)

    if not request.json:
        abort(400)

    if 'body' in request.json and not isinstance(request.json['body'], str):
        abort(400)

    body = request.json.get('body', comment['body'])

    db = get_db()
    update_comment(db, body, post_id, comment_id)

    comment = dict(get_comment(db, post_id, comment_id))
    
    return jsonify({'comment': comment})

@bp.route('/api/posts/<int:post_id>/comments/<int:comment_id>', methods=['DELETE'])
@auth.login_required
def del_comment(post_id, comment_id):

    check_comment(post_id, comment_id)
    db = get_db()
    delete_comment(db, post_id, comment_id)

    return jsonify({'result': True})
