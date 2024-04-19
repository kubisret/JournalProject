import json
import os
from flask import Flask, render_template
from flask_login import LoginManager
from flask_mailman import Mail
from flask_restful import Api

from blueprints import users_blueprint, classes_blueprint
from blueprints.api.users_api import UserResource
from data import db_session
from data.models.users import User


app = Flask(__name__)
api = Api(app)


with open('config.json', 'r', encoding='utf-8') as config_file:
    config = json.load(config_file)
    for key, val in config.items():
        app.config[key] = val

mail = Mail(app)
login_manager = LoginManager()
login_manager.init_app(app)


def main():
    if not os.path.exists('db'):
        os.makedirs('db')
    db_session.global_init("db/journal.db")
    api.add_resource(UserResource, '/api/user')
    app.register_blueprint(users_blueprint.blueprint)
    app.register_blueprint(classes_blueprint.blueprint)
    app.run()


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
@app.route('/index')
def index() -> str:
    """
        Method for rendering the main page
        :return: str
    """
    return render_template('/basic/index.html', title='Электронный журнал')


@app.route('/profile')
def profile():
    return render_template('/basic/profile.html', title='Электронный журнал')


if __name__ == '__main__':
    main()
