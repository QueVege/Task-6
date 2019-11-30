from flask import Blueprint
from flask import g
from flask import request
from flask import jsonify
from flask import make_response
from werkzeug.exceptions import abort

from flaskr.auth.auth import auth
from flaskr.db import get_db
from flaskr.blog.queries import (
    get_last_id, create_post, delete_post, get_post, update_post, post_list
)

bp = Blueprint("blog", __name__,  url_prefix="/blog")


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


def check_post(id, check_author=True):
 
    post = get_post(get_db(), id)
    if post is None:
        abort(404)

    if check_author and post["author_id"] != g.user["id"]:
        abort(403)

    return post

#curl -i http://localhost:5000/blog/api/posts
@bp.route('/api/posts', methods=['GET'])
def get_all_posts():

    db = get_db()
    posts = post_list(db)

    posts = [dict(row) for row in posts]

    return jsonify({'posts': posts})


@bp.route('/api/posts/<int:id>', methods=['GET'])
def get_post_by_id(id):

    post = get_post(get_db(), id)

    if post is None:
        abort(404)

    post = dict(post)

    return jsonify({'post': post})

#curl -u admin:123 -i -H "Content-Type: application/json" -X POST
# -d '{"title":"MyFirstPost","body":"Post body"}' http://localhost:5000/blog/api/posts
@bp.route('/api/posts', methods=['POST'])
@auth.login_required
def new_post():

    if not request.json or not 'title' in request.json:
        abort(400)

    title = request.json['title']
    body = request.json.get('body', '')

    db = get_db()

    create_post(db, title, body, g.user['id'])

    last_id = get_last_id(db)[0]

    post = dict(get_post(db, last_id))

    return jsonify({'post': post}), 201


@bp.route('/api/posts/<int:id>', methods=['PUT'])
@auth.login_required
def upd_post(id):

    post = check_post(id)

    if not request.json:
        abort(400)

    if 'title' in request.json and not isinstance(requeast.json['title'], str):
        abort(400)

    if 'body' in request.json and not isinstance(request.json['body'], str):
        abort(400)

    title = request.json.get('title', post['title'])
    body = request.json.get('body', post['body'])

    db = get_db()
    update_post(db, title, body, id)

    post = dict(get_post(db, id))
    
    return jsonify({'post': post})

@bp.route('/api/posts/<int:id>', methods=['DELETE'])
@auth.login_required
def del_post(id):

    check_post(id)
    db = get_db()
    delete_post(db, id)

    return jsonify({'result': True})
