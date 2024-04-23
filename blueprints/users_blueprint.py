import json
import flask
import requests
from flask_login import login_required, logout_user, current_user, login_user
from flask import redirect, render_template, request
from flask import redirect, render_template

from data.reset_password_email import send_reset_password_email
from data.confirm_email import send_confirm_email
from data.models.users import User
from data import db_session
from forms.reset_forms import ResetPasswordRequestForm, ResetPasswordForm
from forms.confirm_email import ConfirmEmailForm
from forms.login_form import LoginForm
from forms.user import RegisterForm
from tools.check_validate_password import check_validate_password

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

        return render_template('/basic/login.html',
                               title='Авторизация',
                               form=form,
                               message="Неправильная почта или пароль.")
    return render_template('/basic/login.html',
                           title='Авторизация',
                           form=form)


@blueprint.route('/register', methods=['GET', 'POST'])
def reqister():
    if current_user.is_authenticated:
        return redirect("/index")
    form = RegisterForm()
    if request.method == 'POST':
        response = requests.post(f'http://{config["domen"]}:5000/api/register', data=request.form)
        if response.status_code == 201:
            return redirect('/login')
        else:
            return render_template('/basic/register.html',
                                   title='Регистрация',
                                   form=form,
                                   message=response.json()['message'])
    return render_template('/basic/register.html',
                           title='Регистрация',
                           form=form)


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

            render_template('/reset_password/reset_password_request.html',
                            title="Сброса пароля",
                            form=form)

    return render_template('/reset_password/reset_password_request.html',
                           title="Сброса пароля",
                           form=form)


@blueprint.route("/reset_password/<token>/<int:user_id>", methods=["GET", "POST"])
def reset_password(token, user_id):
    if current_user.is_authenticated:
        return redirect("/index")
    db_sess = db_session.create_session()
    user = User.validate_token(token, user_id, db_sess, config)
    if not user:
        return render_template(
            "/reset_password/reset_password_error.html",
            title="Ошибка обновления пароля"
        )

    form = ResetPasswordForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('/reset_password/reset_password.html',
                                   title='Обновление пароля',
                                   form=form,
                                   message="Пароли не совпадают.")

        response, message = check_validate_password(form.password.data)
        if not response:
            return render_template('/reset_password/reset_password.html',
                                   title='Обновление пароля',
                                   form=form,
                                   message=message)

        user.set_password(form.password.data)
        db_sess.commit()

        return render_template(
            "/reset_password/reset_password_success.html",
            title="Успешное обновление пароля"
        )

    return render_template(
        "/reset_password/reset_password.html",
        title="Сброс пароля",
        form=form
    )


@blueprint.route('/confirm_email', methods=['GET', 'POST'])
def confirm_email_request():
    if current_user.is_confirm:
        return redirect("/index")

    form = ConfirmEmailForm()
    if form.validate_on_submit():
        user = current_user
        send_confirm_email(user, config)

        render_template('/confirm_email/confirm_email.html',
                        title="Подтверждения почты",
                        form=form)

    return render_template('/confirm_email/confirm_email.html',
                           title="Подтверждения почты",
                           form=form)


@blueprint.route("/confirm_email/<token>/<int:user_id>", methods=["GET", "POST"])
def confirm_email(token, user_id):
    db_sess = db_session.create_session()
    user = User.validate_token(token, user_id, db_sess, config)
    if not user:
        return render_template(
            "confirm_email_error.html",
            title="Ошибка подтверждения почты"
        )

    user_ = db_sess.query(User).filter(User.id == user_id).first()
    user_.is_confirm = True
    db_sess.commit()

    return render_template("/confirm_email/confirm_email_success.html",
                           title="Успешное подтверждение почты")
