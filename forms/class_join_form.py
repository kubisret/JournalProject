from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class ClassJoinForm(FlaskForm):
    identifier = StringField('Идентификатор')
    secret_key = StringField('Ключ доступа')
    submit = SubmitField('Присоединиться')
