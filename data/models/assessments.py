import datetime
import sqlalchemy
from data.db_session import SqlAlchemyBase
from sqlalchemy import orm


class Assessments(SqlAlchemyBase):
    __tablename__ = 'Assessments'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    id_class = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('classes.id'))
    data = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    value = sqlalchemy.Column(sqlalchemy.Integer)
    id_student = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    student = orm.relationship('User')
    classes = orm.relationship('Classes')
