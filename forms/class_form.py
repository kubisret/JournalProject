from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class ClassForm(FlaskForm):
    title = StringField('Название учебного класса', validators=[DataRequired()])
    about = StringField('Описание', validators=[DataRequired()])
    submit = SubmitField('Создать')
