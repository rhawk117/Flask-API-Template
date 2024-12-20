from flask import (
    Blueprint, request, jsonify, current_app, Response
)
from utils.db import db
from models.user import User
import bcrypt
import jwt

auth_bp = Blueprint('auth', __name__)


class AuthErrors:
    @staticmethod
    def missing_field() -> Response:
        return jsonify({'error': 'Both a username and password are required '}), 400

    @staticmethod
    def unknown_user() -> Response:
        return jsonify({'error': 'The username provided does not exist'}), 401

    @staticmethod
    def bad_pwd() -> Response:
        return jsonify({'error': 'Invalid password, try again'}), 401


@auth_bp.route('/register', methods=['POST'])
def register() -> Response:
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return AuthErrors.missing_field()

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 409

    password_hash = bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')
    user = User(username=username, password_hash=password_hash)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'Account registered successfully!'}), 201


@auth_bp.route('/login', methods=['POST'])
def login() -> Response:
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return AuthErrors.missing_field()

    user = User.query.filter_by(username=username).first()
    if not user:
        return AuthErrors.unknown_user()

    valid_pwd = bcrypt.checkpw(
        password.encode('utf-8'),
        user.password_hash.encode('utf-8')
    )

    if not valid_pwd:
        return AuthErrors.bad_pwd()
    token = jwt.encode(
        {'user_id': user.id},
        current_app.config['SECRET_KEY'],
        algorithm='HS256'
    )
    return jsonify({'token': token})
