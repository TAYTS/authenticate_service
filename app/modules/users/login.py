from flask import request, jsonify, current_app
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    create_refresh_token,
    set_access_cookies,
    set_refresh_cookies,
    jwt_refresh_token_required,
    get_jwt_identity,
)

# Import database models
from models.db import db
from models.user import Users


def login():
    # Get the data from the request JSON
    username = str(request.json.get("username"))
    password = str(request.json.get("password"))
    remember = request.json.get("remember")

    # Define return message
    message = {"status": 0}

    # Check if the data is present
    if username and password:
        user = db.session.query(Users).filter(Users.email == username).first()
        if user:
            if user.check_password(password):
                access_token = create_access_token(
                    identity=user.id_user_hash, fresh=True
                )
                refresh_token = create_refresh_token(
                    identity=user.id_user_hash)

                if remember:
                    access_expire = current_app.config["JWT_ACCESS_TOKEN_EXPIRES"]
                    refresh_expire = current_app.config["JWT_REFRESH_TOKEN_EXPIRES"]
                else:
                    access_expire = None
                    refresh_expire = None

                message["status"] = 1

                resp = jsonify(message)
                set_access_cookies(resp, access_token, max_age=access_expire)
                set_refresh_cookies(resp, refresh_token,
                                    max_age=refresh_expire)
                return resp, 200

    return jsonify(message), 401


@jwt_refresh_token_required
def refresh():
    # Create new access token
    current_user = get_jwt_identity()
    if current_user:
        access_token = create_access_token(identity=current_user, fresh=False)
        access_expire = current_app.config["JWT_ACCESS_TOKEN_EXPIRES"]

        resp = jsonify({"status": 1})
        set_access_cookies(resp, access_token, max_age=access_expire)
        return resp, 200
    else:
        resp = jsonify({"status": 0})
        return resp, 401


@jwt_required
def authenticate():
    current_user = get_jwt_identity()
    if current_user:
        return jsonify({"status": 1}), 200
    else:
        return jsonify({"status": 0}), 401
