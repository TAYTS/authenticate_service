from flask import request, jsonify, current_app
from twilio.rest import Client


def create_channel():
    id_ticket_hash = request.json.get("id_ticket_hash")
    title = request.json.get("title")
    message = {"id_channel": ""}

    if id_ticket_hash and title:
        # Create chat channel
        account_sid = current_app.config["TWILIO_ACCOUNT_SID"]
        auth_token = current_app.config["TWILIO_AUTH_TOKEN"]
        chat_sid = current_app.config["TWILIO_CHAT_SID"]
        client = Client(account_sid, auth_token)

        channel = client.chat.services(chat_sid) \
            .channels \
            .create(
            friendly_name=title,
            unique_name=id_ticket_hash, type="private")

        id_channel = channel.sid
        message["id_channel"] = id_channel
        return jsonify(message), 201
    else:
        return jsonify(message), 400
