from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.fields.choices import SelectField


class GradeForm(FlaskForm):
    grade = SelectField('Оценки', choices=[
        (5, '5'),
        (4, '4'),
        (3, '3'),
        (2, '2')
    ])
    submit = SubmitField('Поставить')
