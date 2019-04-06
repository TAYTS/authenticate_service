from flask import request, jsonify, current_app
from werkzeug.security import generate_password_hash
from datetime import datetime
import requests

# Import database models
from models.db import db
from models.users import Users

# Import helper function
from app.utils.create_user_hash import create_user_hash


def register():
    """
    Register new user account.

    Returns:
        {"status" : 0} if failed to create new account
        {"status" : -1} duplicate account
        {"status" : 1} if successfully create new account
    """
    username = str(request.json.get("username"))
    email = str(request.json.get("email"))
    password = str(request.json.get("password"))
    message = {"status": 0}
    if not(username and email and password):
        return jsonify(message), 400

    # Check if the account exist
    user = db.session.query(Users).filter(
        Users.email == email
    ).first()

    if not user:
        hashed_user = create_user_hash(email)
        hashed_password = generate_password_hash(password)
        timestamp = datetime.utcnow()

        # Create twilio chat user ID
        payload = {
            "id_user_hash": hashed_user
        }
        response = requests.post(
            current_app.config["MESSAGE_API"] + "create_chat_user",
            json=payload)
        id_chat = response.json().get("id_chat")

        if id_chat:
            user = Users(
                id_user_hash=hashed_user,
                id_chat=id_chat,
                username=username,
                password=hashed_password,
                email=email,
                create_timestamp=timestamp
            )

            try:
                db.session.add(user)
                db.session.commit()
                message["status"] = 1
                return jsonify(message), 201
            except Exception as e:
                current_app.logger.info('Failed to add new user: ' + str(e))

        return jsonify(message), 500
    else:
        message["status"] = -1
        return jsonify(message), 409
