import json

import flask
from flask_login import login_required, logout_user, current_user, login_user
from flask import redirect, render_template, flash

from data.reset_password_email import send_reset_password_email
from data.confirm_email import send_confirm_email
from data.users import User
from data import db_session

from forms.reset_forms import ResetPasswordRequestForm, ResetPasswordForm
from forms.confirm_email import ConfirmEmailForm
from forms.login_form import LoginForm
from forms.user import RegisterForm
from logics.logics import check_validate_password

blueprint = flask.Blueprint(
    'users_function',
    __name__,
    template_folder='templates'
)

with open('config.json', 'r', encoding='utf-8') as config_file:
    config = json.load(config_file)


@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@blueprint.route('/login', methods=['GET', 'POST'])
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
                               message="Неправильная почта или пароль.",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@blueprint.route('/register', methods=['GET', 'POST'])
def reqister():
    if current_user.is_authenticated:
        return redirect("/index")

    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают.")

        response, message = check_validate_password(form.password.data)
        if not response:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message=message)

        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть.")
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


@blueprint.route('/reset_password', methods=['GET', 'POST'])
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
            send_reset_password_email(user, config)

            render_template('reset_password_request.html', form=form)

    return render_template('reset_password_request.html', form=form)


@blueprint.route("/reset_password/<token>/<int:user_id>", methods=["GET", "POST"])
def reset_password(token, user_id):
    if current_user.is_authenticated:
        return redirect("/index")
    db_sess = db_session.create_session()
    user = User.validate_token(token, user_id, db_sess, config)
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


@blueprint.route('/confirm_email', methods=['GET', 'POST'])
def confirm_email_request():
    if current_user.is_confirm:
        return redirect("/index")

    form = ConfirmEmailForm()
    if form.validate_on_submit():
        user = current_user
        send_confirm_email(user, config)

        render_template('confirm_email.html', form=form)

    return render_template('confirm_email.html', form=form)


@blueprint.route("/confirm_email/<token>/<int:user_id>", methods=["GET", "POST"])
def confirm_email(token, user_id):
    db_sess = db_session.create_session()
    user = User.validate_token(token, user_id, db_sess, config)
    if not user:
        return render_template(
            "reset_password_error.html", title="Reset Password error"
        )

    user_ = db_sess.query(User).filter(User.id == user_id).first()
    user_.is_confirm = True
    db_sess.commit()

    return render_template("confirm_email_success.html", title="Reset Password error")
