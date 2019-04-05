from models.db import db
from sqlalchemy.dialects.mysql import TIMESTAMP, TINYINT
from datetime import datetime


class TicketRecords(db.Model):
    __tablename__ = 'TICKET_RECORDS'
    id_ticket = db.Column(db.Integer, primary_key=True)
    id_ticket_hash = db.Column(db.String(255), unique=True, default='')
    id_creator = db.Column(db.Integer, db.ForeignKey(
        'USERS.id_user', ondelete='RESTRICT', onupdate='RESTRICT'))
    id_admin = db.Column(db.Integer,
                         db.ForeignKey(
                             'USERS.id_user',
                             ondelete='RESTRICT',
                             onupdate='RESTRICT'),
                         nullable=True)
    id_channel = db.Column(db.String(255), unique=True, default='')
    # status: -1 => No admin has taken the ticket
    # status:  0 => Ticket is assigned to an admin
    # status:  1 => Ticket is marked as closed
    status = db.Column(TINYINT(1), default=-1)
    title = db.Column(db.String(255), default='')
    category = db.Column(db.String(100), default='')
    create_timestamp = db.Column(
        TIMESTAMP, default=datetime.utcnow().replace(microsecond=0))
    last_activity_timestamp = db.Column(
        TIMESTAMP, default=datetime.utcnow().replace(microsecond=0))
