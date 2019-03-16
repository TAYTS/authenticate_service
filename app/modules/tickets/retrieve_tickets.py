from flask import jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

# Import database models
from models.db import db
from models.users import Users
from models.tickets import TicketRecords


@jwt_required
def retrieve_tickets():
    # Get the id_user_hash from the jwt_token
    id_user_hash = get_jwt_identity()
    current_app.logger.info(id_user_hash)

    # Get the id_user
    id_user = db.session.query(Users.id_user).filter(
        Users.id_user_hash == id_user_hash
    ).first()

    # Define the default return message
    messages = {"open": [], "close": []}

    # Found the user
    if id_user:
        # Get all the tickets and sort by the status
        tickets = db.session.query(TicketRecords).filter(
            TicketRecords.id_creator == id_user
        ).order_by(
            TicketRecords.last_activity_timestamp,
            TicketRecords.status
        ).all()

        time_format = "%d %b %Y %I:%M %p"
        # Map status value to string
        statusStr = {
            -1: "Pending",
            0: "In Progress",
            1: "Solved"
        }
        for ticket in tickets:
            base = {
                "title": ticket.title,
                "ticketID": ticket.id_ticket_hash,
                "ticketCategory": ticket.category,
                "create_timestamp": ticket.create_timestamp.strftime(time_format),
                "last_activity": ticket.last_activity_timestamp.strftime(time_format),
                "status": statusStr[ticket.status]
            }
            if ticket.status <= 0:
                messages["open"].append(base)
            else:
                messages["close"].append(base)
        return jsonify(messages), 200

    return jsonify({
        "message": "Invalid credential"
    }), 401
