from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class ConfirmEmailForm(FlaskForm):
    submit = SubmitField('Отправить письмо')
