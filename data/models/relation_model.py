from data.db_session import SqlAlchemyBase
import sqlalchemy
from sqlalchemy import orm


class RelationUserToClass(SqlAlchemyBase):
    __tablename__ = 'relation_user_to_class'

    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)
    id_class = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('classes.id'))
    id_user = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    user = orm.relationship('User')
    classes = orm.relationship('Classes')
