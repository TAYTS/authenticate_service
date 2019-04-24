from models.db import db
from sqlalchemy.dialects.mysql import TIMESTAMP, TINYINT
from werkzeug.security import check_password_hash
from datetime import datetime


class Users(db.Model):
    __tablename__ = 'USERS'
    id_user = db.Column(db.Integer, primary_key=True)
    id_user_hash = db.Column(db.String(255), unique=True, default='')
    id_chat = db.Column(db.String(255), unique=True, default='')
    is_admin = db.Column(TINYINT(3), default=0)
    username = db.Column(db.String(255), default='')
    password = db.Column(db.String(255), default='')
    email = db.Column(db.String(255), unique=True, default='')
    create_timestamp = db.Column(
        TIMESTAMP, default=datetime.utcnow().replace(microsecond=0))
    # TODO: User tier and classification

    def check_password(self, password):
        return check_password_hash(self.password, password)
