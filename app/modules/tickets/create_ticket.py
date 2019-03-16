from flask import jsonify, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from uuid import uuid4
from datetime import datetime

# Import database models
from models.db import db
from models.users import Users
from models.tickets import TicketRecords

# Import helper modules
from app.utils.save_to_dynamoDB import save_to_dynamoDB


@jwt_required
def create_ticket():
    # Get all the parametes
    title = str(request.json.get("title"))
    category = str(request.json.get("category"))
    message = str(request.json.get("message"))

    current_app.logger.info(request.json)

    current_app.logger.info("Title: " + title)
    current_app.logger.info("Category: " + category)
    current_app.logger.info("Message: " + message)

    # Get the id_user_hash from the jwt_token
    id_user_hash = get_jwt_identity()
    current_app.logger.info(id_user_hash)

    # Define template message
    resp = {"status": 0}

    if (title and category and message):
        # Get the id_user
        id_user = db.session.query(Users.id_user).filter(
            Users.id_user_hash == id_user_hash
        ).first()

        if id_user:
            # Generate uuid for the id_ticket_hash and id_message
            id_ticket_hash = str(uuid4())
            id_message = str(uuid4())
            timestamp = datetime.utcnow().replace(microsecond=0)

            # Create ticket record entry
            ticket = TicketRecords(
                id_ticket_hash=id_ticket_hash,
                id_message=id_message,
                id_creator=id_user,
                title=title,
                category=category,
                create_timestamp=timestamp,
                last_activity_timestamp=timestamp
            )

            # Add message record to dynamoDB
            save_status = save_to_dynamoDB(
                id_message,
                id_ticket_hash,
                message,
                timestamp
            )

            if save_status:
                db.session.add(ticket)
                db.session.commit()
                resp["status"] = 1
                return jsonify(resp), 200
        else:
            return jsonify(resp), 401
    else:
        return jsonify(resp), 400

    return jsonify(resp), 500
