import json

import flask
from flask import jsonify, request
from flask_login import current_user

from data import db_session
from data.models.users import User
from tools.check_validate_password import check_validate_password
from tools.misc import make_resp

with open('config.json', 'r', encoding='utf-8') as config_file:
    config = json.load(config_file)

blueprint = flask.Blueprint(
    'api_function',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/register', methods=['POST'])
def register():
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
