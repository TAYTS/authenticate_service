from flask import request, jsonify, current_app
from twilio.rest import Client


def create_chat_user():
    id_user_hash = request.json.get("id_user_hash")
    message = {"id_chat": ""}

    if id_user_hash:
        # Create Twilio chat user
        account_sid = current_app.config["TWILIO_ACCOUNT_SID"]
        auth_token = current_app.config["TWILIO_AUTH_TOKEN"]
        chat_sid = current_app.config["TWILIO_CHAT_SID"]

        client = Client(account_sid, auth_token)
        twilio_user = client.chat.services(chat_sid) \
            .users \
            .create(identity=id_user_hash)
        id_chat = twilio_user.sid

        message["id_chat"] = id_chat

        return jsonify(message), 201
    else:
        return jsonify(message), 400
