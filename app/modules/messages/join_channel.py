from flask import request, jsonify, current_app
from twilio.rest import Client


def join_channel():
    id_channel = request.json.get("id_channel")
    id_user_hash = request.json.get("id_user_hash")
    message = {"id_member": ""}

    if id_channel and id_user_hash:
        account_sid = current_app.config["TWILIO_ACCOUNT_SID"]
        auth_token = current_app.config["TWILIO_AUTH_TOKEN"]
        chat_sid = current_app.config["TWILIO_CHAT_SID"]
        client = Client(account_sid, auth_token)

        member = client.chat.services(chat_sid) \
            .channels(id_channel) \
            .members \
            .create(identity=id_user_hash)
        message["id_member"] = member.sid
        return jsonify(message), 201
    else:
        return jsonify(message), 400
