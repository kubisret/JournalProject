import datetime
import sqlalchemy
from sqlalchemy import orm

from data.db_session import SqlAlchemyBase


class Homework(SqlAlchemyBase):
    __tablename__ = 'homework'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    id_class = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('classes.id'))
    is_end = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    classes = orm.relationship('Classes')
