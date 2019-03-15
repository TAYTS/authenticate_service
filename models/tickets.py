from models.db import db
from sqlalchemy.dialects.mysql import TIMESTAMP, TINYINT
from datetime import datetime


class TicketRecords(db.Model):
    __tablename__ = 'TICKET_RECORDS'
    id_ticket = db.Column(db.Integer, primary_key=True)
    id_ticket_hash = db.Column(db.String(255), unique=True, default='')
    id_message = db.Column(db.String(255), unique=True, default='')
    id_creator = db.Column(db.Integer, db.ForeignKey(
        'USERS.id_user', ondelete='RESTRICT', onupdate='RESTRICT'))
    status = db.Column(TINYINT(1), default=-1)
    create_timestamp = db.Column(
        TIMESTAMP, default=datetime.utcnow().replace(microsecond=0))
    last_activity_timestamp = db.Column(
        TIMESTAMP, default=datetime.utcnow().replace(microsecond=0))
