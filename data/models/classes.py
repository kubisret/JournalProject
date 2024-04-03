import datetime
import sqlalchemy
from data.db_session import SqlAlchemyBase
from sqlalchemy import orm


class Classes(SqlAlchemyBase):
    __tablename__ = 'classes'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    id_owner = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    owner = orm.relationship('User')
