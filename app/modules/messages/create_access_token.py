from flask import jsonify, current_app
from flask_jwt_extended import get_jwt_identity, jwt_required
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import ChatGrant

# Import database models
from models.db import db
from models.users import Users


@jwt_required
def create_access_token():
    id_user_hash = get_jwt_identity()

    id_user = db.session.query(Users.id_user).filter(
        Users.id_user_hash == id_user_hash
    ).first()

    if id_user:
        account_sid = current_app.config["TWILIO_ACCOUNT_SID"]
        api_sid = current_app.config["TWILIO_API_SID"]
        api_secret = current_app.config["TWILIO_API_SECRET"]
        chat_sid = current_app.config["TWILIO_CHAT_SID"]
        token = AccessToken(
            account_sid,
            api_sid,
            api_secret,
            identity=id_user_hash,
            ttl=7200)

        chat_grant = ChatGrant(service_sid=chat_sid)
        token.add_grant(chat_grant)

        return jsonify({
            "token": token.to_jwt().decode("utf-8")
        }), 200

    else:
        return jsonify({
            "message": "Invalid credential"
        }), 401
