import os

from flask import Flask, url_for, render_template, redirect, request, session, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_mailman import Mail

from data.reset_password_email import send_reset_password_email
from forms.login_form import LoginForm
from forms.reset_forms import ResetPasswordRequestForm, ResetPasswordForm
from forms.user import RegisterForm
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

    app.run()


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Электронный журнал')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect("/index")

    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильная почта или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    if current_user.is_authenticated:
        return redirect("/index")

    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect("/index")

    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if not user:
            return redirect('/register')
        else:
            send_reset_password_email(user, app)

            flash(
                "Instructions to reset your password were sent to your email address,"
                " if it exists in our system."
            )

            render_template('reset_password_request.html', form=form)

    return render_template('reset_password_request.html', form=form)


@app.route("/reset_password/<token>/<int:user_id>", methods=["GET", "POST"])
def reset_password(token, user_id):
    if current_user.is_authenticated:
        return redirect("/index")
    db_sess = db_session.create_session()
    user = User.validate_reset_password_token(token, user_id, db_sess, app)
    if not user:
        return render_template(
            "reset_password_error.html", title="Reset Password error"
        )

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db_sess.commit()

        return render_template(
            "reset_password_success.html", title="Reset Password success"
        )

    return render_template(
        "reset_password.html", title="Reset Password", form=form
    )


if __name__ == '__main__':
    main()
