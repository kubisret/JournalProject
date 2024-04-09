import datetime
import sqlalchemy
from werkzeug.security import generate_password_hash, check_password_hash

from data.db_session import SqlAlchemyBase
from sqlalchemy import orm

from logics.data_class_room import create_default_identifier, create_default_key


class Classes(SqlAlchemyBase):
    __tablename__ = 'classes'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    identifier = sqlalchemy.Column(sqlalchemy.String, unique=True)
    secret_key = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    id_owner = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    is_privat = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    owner = orm.relationship('User')
