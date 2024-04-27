import json
import flask
from flask_login import current_user
from flask import redirect, render_template
from data.models.users import User
from data import db_session
from forms.new_password import NewPassword
from forms.profile_settings import ProfileSettings
from tools.check_validate import check_validate_password

blueprint = flask.Blueprint(
    'profile_blueprint',
    __name__,
    template_folder='templates'
)

with open('config.json', 'r', encoding='utf-8') as config_file:
    config = json.load(config_file)


@blueprint.route('/profile')
def profile():
    return render_template('/profile/profile.html',
                           title='Профиль')


@blueprint.route('/profile_settings', methods=['GET', 'POST'])
def profile_settings():

    form = ProfileSettings()

    if form.validate_on_submit():

        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        user.name = form.name.data
        user.surname = form.surname.data
        if form.email.data != user.email:
            user.email = form.email.data
            user.is_confirm = 0
        db_sess.commit()

        return redirect('/profile_settings')

    form.name.data = current_user.name
    form.surname.data = current_user.surname
    form.email.data = current_user.email

    return render_template('/profile/profile_settings.html',
                           title='Настройки профиля',
                           form=form)


@blueprint.route('/new_password', methods=['GET', 'POST'])
def new_password():
    form = NewPassword()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        # Проверка пароля на валидность и безопасность
        response, message = check_validate_password(form.new_password.data)
        if not response:
            return render_template('/profile/new_password.html',
                                   title='Новый пароль',
                                   message=message,
                                   form=form)
        if user.check_password(form.old_password.data):
            if form.new_password.data == form.new_password_again.data:
                user.set_password(form.new_password.data)
                db_sess.commit()
                return redirect('/profile_settings')
            else:
                return render_template('/profile/new_password.html',
                                       title='Новый пароль',
                                       message='Пароли не совпадают',
                                       form=form)
        else:
            return render_template('/profile/new_password.html',
                                   title='Новый пароль',
                                   message='Пароль не совпадает с Вашим текущем паролем',
                                   form=form)

    return render_template('/profile/new_password.html',
                           title='Новый пароль',
                           form=form)
