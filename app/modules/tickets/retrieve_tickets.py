from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

# Import database models
from models.db import db
from models.users import Users
from models.tickets import TicketRecords

# Import helper modules
from app.utils.create_timestamp_str import create_timestamp_str


@jwt_required
def retrieve_tickets():
    """
    Get all the tickets created by the user.
    Identify the user from the id_user_hash stored inside the JWT_TOKEN.
    Returns:
        tickets (dictionary): Details of each ticket created by the user
    """
    # Get the id_user_hash from the jwt_token
    id_user_hash = get_jwt_identity()

    # Get the id_user
    id_user = db.session.query(Users.id_user).filter(
        Users.id_user_hash == id_user_hash
    ).first()

    # Define the default response message
    resp = {"open": [], "close": []}

    # Found the user
    if id_user:
        # Get all the tickets and sort by the status
        tickets = db.session.query(TicketRecords).filter(
            TicketRecords.id_creator == id_user
        ).order_by(
            TicketRecords.last_activity_timestamp,
            TicketRecords.status
        ).all()

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
                "create_timestamp": create_timestamp_str(ticket.create_timestamp),
                "last_activity": create_timestamp_str(ticket.last_activity_timestamp),
                "status": statusStr[ticket.status]
            }
            if ticket.status <= 0:
                resp["open"].append(base)
            else:
                resp["close"].append(base)
        return jsonify(resp), 200

    return jsonify({
        "message": "Invalid credential"
    }), 401
