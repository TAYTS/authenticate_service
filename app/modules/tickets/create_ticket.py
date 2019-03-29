from flask import jsonify, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from uuid import uuid4
from datetime import datetime
import os

# Import database models
from models.db import db
from models.users import Users
from models.tickets import TicketRecords

# Import helper modules
from app.utils.save_to_dynamoDB import save_to_dynamoDB
from app.utils.save_to_local import save_to_local
from app.utils.save_to_s3 import save_to_s3


@jwt_required
def create_ticket():
    """
    Create ticket with the valid details received from frontend.

    Returns:
        {"status" : 0} if failed to create the ticket
        {"status" : 1} if successfully create the ticket
    """
    # Get all the parametes
    title = str(request.form.get("title"))
    category = str(request.form.get("category"))
    message = str(request.form.get("message"))
    files = request.files.getlist("files")

    # Get the id_user_hash from the jwt_token
    id_user_hash = get_jwt_identity()

    # Define template message
    resp = {"status": 0}

    # Message from user/client
    message_type = 1

    # Data structure for storing files
    fileDS = []

    if (title and category and message):
        # Get the id_user
        id_user = db.session.query(Users.id_user).filter(
            Users.id_user_hash == id_user_hash
        ).first()

        if id_user:
            # Generate uuid for the id_ticket_hash
            id_ticket_hash = str(uuid4())
            timestamp = datetime.utcnow().replace(microsecond=0)

            # Create ticket record entry
            ticket = TicketRecords(
                id_ticket_hash=id_ticket_hash,
                id_creator=id_user,
                title=title,
                category=category,
                create_timestamp=timestamp,
                last_activity_timestamp=timestamp
            )

            if files:
                # Save files to local
                dirname = id_ticket_hash + "_" + \
                    str(int(timestamp.timestamp()))
                directory_path = os.path.join(
                    current_app.config["TEMP_DIR"],
                    dirname)
                os.mkdir(directory_path)
                local_filepaths, fileDS = save_to_local(files, directory_path)

                # Upload files to S3
                if (local_filepaths, fileDS):
                    fileDS = save_to_s3(
                        local_filepaths,
                        fileDS,
                        directory_path
                    )

            # Add message record to dynamoDB
            save_status = save_to_dynamoDB(
                id_ticket_hash,
                message,
                message_type,
                timestamp,
                fileDS
            )
            if save_status:
                db.session.add(ticket)
                db.session.commit()
                resp["status"] = 1
                return jsonify(resp), 201
        else:
            return jsonify(resp), 401
    else:
        return jsonify(resp), 400

    return jsonify(resp), 500
