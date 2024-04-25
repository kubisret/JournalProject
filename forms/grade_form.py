from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.fields.choices import SelectField


class GradeForm(FlaskForm):
    grade = SelectField('Оценки', choices=[
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5')
    ])
    submit = SubmitField('Поставить')
