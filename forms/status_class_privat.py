from flask_wtf import FlaskForm
from wtforms import SubmitField


class StatusPrivat(FlaskForm):
    submit = SubmitField('изменить статус')
