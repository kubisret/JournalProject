import json
import flask
from flask_login import login_required, logout_user, current_user, login_user
from flask import redirect, render_template
from flask import redirect, render_template

from data.reset_password_email import send_reset_password_email
from data.confirm_email import send_confirm_email
from data.models.users import User
from data import db_session
from forms.profile_settings import ProfileSettings
from forms.reset_forms import ResetPasswordRequestForm, ResetPasswordForm
from forms.confirm_email import ConfirmEmailForm
from forms.login_form import LoginForm
from forms.user import RegisterForm
from logics.check_validate import check_validate_password

blueprint = flask.Blueprint(
    'profile_blueprint',
    __name__,
    template_folder='templates'
)

with open('config.json', 'r', encoding='utf-8') as config_file:
    config = json.load(config_file)


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
