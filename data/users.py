import datetime
import sqlalchemy
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from werkzeug.security import generate_password_hash, check_password_hash
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=True)
    is_confirm = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True, default=False)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def generate_token(self, config):
        serializer = URLSafeTimedSerializer(config["SECRET_KEY"])
        return serializer.dumps(self.email, salt=self.hashed_password)

    @staticmethod
    def validate_token(token: str, user_id: int, db_sess, config):
        user = db_sess.query(User).get(user_id)

        if user is None:
            return None

        serializer = URLSafeTimedSerializer(config["SECRET_KEY"])
        try:
            token_user_email = serializer.loads(
                token,
                max_age=config["RESET_PASS_TOKEN_MAX_AGE"],
                salt=user.hashed_password,
            )
        except (BadSignature, SignatureExpired):
            return None

        if token_user_email != user.email:
            return None

        return user
