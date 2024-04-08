from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class ClassForm(FlaskForm):
    title = StringField('Название класса', validators=[DataRequired()])
    about = StringField('Описание', validators=[DataRequired()])
    identifier = StringField('Идентификатор')
    secret_key = StringField('Ключ доступа')
    submit = SubmitField('Создать')
