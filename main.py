import os

from flask import Flask, render_template
from flask_login import LoginManager
from flask_mailman import Mail

from blueprints import users_blueprint
from data import db_session
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'journalproject_secret_key'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_DEFAULT_SENDER'] = 'idusernoreply@gmail.com'
app.config['MAIL_USERNAME'] = 'idusernoreply@gmail.com'
app.config['MAIL_PASSWORD'] = 'vfbxqikiznuhkncd'
app.config["RESET_PASS_TOKEN_MAX_AGE"] = 60 * 60 * 2

mail = Mail(app)
login_manager = LoginManager()
login_manager.init_app(app)


def main():
    if not os.path.exists('db'):
        os.makedirs('db')
    db_session.global_init("db/journal.db")
    app.register_blueprint(users_blueprint.blueprint)
    app.run()


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Электронный журнал')


if __name__ == '__main__':
    main()
