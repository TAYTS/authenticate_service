from flask import request, jsonify, current_app
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    set_access_cookies,
    set_refresh_cookies
)

# Import database models
from models.db import db
from models.users import Users


def login():
    """
    Login user account.
    Return JWT token if the user credential is valid.

    Returns:
        {"id_user_hash" : "id-user-hash"}
    """
    # Get the data from the request JSON
    email = str(request.json.get("email"))
    password = str(request.json.get("password"))
    remember = request.json.get("remember")

    # Define return message
    message = {"id_user_hash": ""}

    # Check if the data is present
    if email and password:
        user = db.session.query(Users).filter(Users.email == email).first()
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

                message["id_user_hash"] = user.id_user_hash

                resp = jsonify(message)
                set_access_cookies(resp, access_token, max_age=access_expire)
                set_refresh_cookies(resp, refresh_token,
                                    max_age=refresh_expire)
                return resp, 200

    return jsonify(message), 401
