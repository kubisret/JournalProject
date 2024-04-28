import datetime
import sqlalchemy
from sqlalchemy import orm

from data.db_session import SqlAlchemyBase


class Homework(SqlAlchemyBase):
    __tablename__ = 'homework'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    text = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)
    recipient = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    date = sqlalchemy.Column(sqlalchemy.DateTime)

    id_class = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('classes.id'))
    file_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    classes = orm.relationship('Classes')
