from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class ClassJoinForm(FlaskForm):
    identifier = StringField('Идентификатор', validators=[DataRequired()])
    secret_key = StringField('Ключ доступа', validators=[DataRequired()])
    submit = SubmitField('Присоединиться')
