import json
import os
from flask import Flask, render_template
from flask_login import LoginManager
from flask_mailman import Mail
from blueprints import profile_blueprint, feadback

from blueprints import users_blueprint, classes_blueprint
from blueprints.api import users_api
from data import db_session
from data.models.users import User

app = Flask(__name__)

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
    app.register_blueprint(users_api.blueprint)
    app.register_blueprint(users_blueprint.blueprint)
    app.register_blueprint(classes_blueprint.blueprint)
    app.register_blueprint(profile_blueprint.blueprint)
    app.register_blueprint(feadback.blueprint)
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


if __name__ == '__main__':
    main()
