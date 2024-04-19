import json

import flask
from flask import jsonify, request
from flask_login import current_user, login_user
from flask_restful import reqparse, abort, Resource

from data import db_session
from data.models.users import User
from forms.user import RegisterForm
from tools.check_validate_password import check_validate_password
from tools.misc import make_resp


with open('config.json', 'r', encoding='utf-8') as config_file:
    config = json.load(config_file)


class UserResource(Resource):
    def post(self):
        if current_user.is_authenticated:
            return make_resp(jsonify({'message': 'You are already autorization'}), 403)
        data = request.form
        name = data.get('name')
        surname = data.get('surname')
        email = data.get('email')
        password = data.get('password')
        password_again = data.get('password_again')

        if not name or not surname or not email or not password or not password_again:
            return make_resp(jsonify({'message': 'Missing required fields'}), 400)

        if password != password_again:
            return make_resp(jsonify({'message': 'Passwords do not match'}), 400)

        # Проверка пароля на валидность и безопасность
        response, message = check_validate_password(password)
        if not response:
            return make_resp(jsonify({'message': message}), 400)

        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == email).first():
            return make_resp(jsonify({'message': 'User already exists'}), 400)

        user = User(
            name=name,
            surname=surname,
            email=email,
        )

        user.set_password(password)
        db_sess.add(user)
        db_sess.commit()

        return make_resp(jsonify({'message': 'User registered successfully'}), 201)

    # post - регистрация, get - авторизация
    def get(self):
        if current_user.is_authenticated:
            return make_resp(jsonify({'message': 'You are already autorization'}), 403)
        data = request.form
        email = data.get('email')
        password = data.get('password')
        remember_me = data.get('remember_me')

        if not email or not password:
            return make_resp(jsonify({'message': 'Missing required fields'}), 400)

        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == email).first()

        if user and user.check_password(password):
            login_user(user, remember=remember_me)
            return make_resp(jsonify({'message': 'Success', 'user_id': user.id}), 200)
        else:
            return make_resp(jsonify({'message': 'Invalid credentials'}), 401)
