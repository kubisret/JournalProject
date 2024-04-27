from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, SubmitField
from wtforms.fields.choices import SelectField
from wtforms.fields.datetime import DateField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired


class HomeWork(FlaskForm):
    text = TextAreaField('Текст задания', validators=[DataRequired()])
    date = DateField('Крайний срок сдачи', format='%Y-%m-%d', validators=[DataRequired()])
    file = FileField('Прикрепите файл')
    recipient = SelectField('Получатель задания', choices=[])
    submit = SubmitField('Выложить')
