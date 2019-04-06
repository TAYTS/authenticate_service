from flask import jsonify, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from uuid import uuid4
from datetime import datetime
import requests

# Import database models
from models.db import db
from models.users import Users
from models.tickets import TicketRecords


@jwt_required
def create_ticket():
    """
    Create ticket with the valid details received from frontend.

    Returns:
        {"status" : 0} if failed to create the ticket
        {"status" : 1} if successfully create the ticket
    """
    # Get all the parametes
    title = str(request.json.get("title"))
    category = str(request.json.get("category"))
    message = str(request.json.get("message"))

    # Get the id_user_hash from the jwt_token
    id_user_hash = get_jwt_identity()

    # Define template message
    resp_msg = {"id_ticket": ""}

    if (title and category and message):
        # Get the id_user
        id_user = db.session.query(Users.id_user).filter(
            Users.id_user_hash == id_user_hash
        ).first()

        if id_user:
            # Generate uuid for the id_ticket_hash
            id_ticket_hash = str(uuid4())
            timestamp = datetime.utcnow().replace(microsecond=0)

            # Catch the MESSAGE API call status error
            try:
                # Create new channel
                payload = {
                    "id_ticket_hash": id_ticket_hash,
                    "title": title
                }
                resp = requests.post(
                    current_app.config["MESSAGE_API"] + "create_channel",
                    json=payload)
                # Check the return status
                resp.raise_for_status()
                id_channel = resp.json().get("id_channel")

                if id_channel:
                    # Add user to the new channel
                    payload = {
                        "id_channel": id_channel,
                        "id_user_hash": id_user_hash
                    }
                    resp = requests.post(
                        current_app.config["MESSAGE_API"] + "join_channel",
                        json=payload)
                    # Check return status
                    resp.raise_for_status()
                    id_member = resp.json().get("id_member")

                    if id_member:
                        # Create ticket record entry
                        ticket = TicketRecords(
                            id_ticket_hash=id_ticket_hash,
                            id_creator=id_user,
                            id_channel=id_channel,
                            title=title,
                            category=category,
                            create_timestamp=timestamp,
                            last_activity_timestamp=timestamp
                        )
                        # if save_status:
                        db.session.add(ticket)
                        db.session.commit()
                        resp_msg["id_ticket"] = id_ticket_hash
                        return jsonify(resp_msg), 201
            except Exception as e:
                current_app.logger.info("Unable to create ticket: " + str(e))
        else:
            return jsonify(resp_msg), 401
    else:
        return jsonify(resp_msg), 400

    return jsonify(resp_msg), 500
