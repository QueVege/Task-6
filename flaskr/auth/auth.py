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

@bp.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error':'Bad request'}), 400)

@auth.verify_password
def verify_password(username, password):

    db = get_db()

    user = get_user_by_username(db, username)

    if user and check_password_hash(user['password'], password):
        g.user = user
        return True

#curl -i -X POST -H "Content-Type: application/json"
# -d '{"username":"admin","password":"123"}' http://127.0.0.1:5000/auth/api/users
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
