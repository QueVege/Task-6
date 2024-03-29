import functools

from flask import Blueprint
from flask import g
from flask import request
from flask import jsonify
from flask import make_response
from werkzeug.security import check_password_hash
from werkzeug.exceptions import abort

from flaskr.db import get_db
from flask_httpauth import HTTPBasicAuth
from flaskr.auth.queries import (
    create_user, get_user_by_username
)

bp = Blueprint("auth", __name__, url_prefix="/auth")

auth = HTTPBasicAuth()

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

@auth.verify_password
def verify_password(username, password):

    db = get_db()

    user = get_user_by_username(db, username)

    if user and check_password_hash(user['password'], password):
        g.user = user
        return True

@bp.route('/api/users', methods = ['POST'])
def new_user():

    db = get_db()

    username = request.json.get('username')
    password = request.json.get('password')

    if username is None or password is None:
        abort(400)

    if get_user_by_username(db, username) is not None:
        abort(400, 'User with the same username already exists')
  
    create_user(db, username, password)
    user = get_user_by_username(db, username)

    return jsonify({'username': user['username'] }), 201
