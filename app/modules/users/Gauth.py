from flask import current_app, request, jsonify
from requests_oauthlib import OAuth2Session
from datetime import datetime
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    set_access_cookies,
    set_refresh_cookies
)

# Import database models
from models.db import db
from models.users import Users

# Import helper function
from app.utils.create_user_hash import create_user_hash


def glogin():
    """
    Create user account/Login using Google credential.
    Return JWT token upon successfully login.

    Returns:
        {"status" : 0} if failed to get user details using the Google credentials
        {"status" : 1} if successful verify the user using the Google credentials
    """
    code = str(request.json.get("code"))

    # Define return message
    message = {"status": 0}

    if code:
        user_info = get_google_user(code=code)
        if user_info.get("email") and user_info.get("verified_email"):
            #  Find the user in the database
            user = db.session.query(
                Users
            ).filter(
                Users.email == user_info.get("email")
            ).first()

            # Check if the user exist
            if user is None:
                # User not found
                # Create new user for Google sign in
                user_email = user_info.get("email")
                hashed_user = create_user_hash(user_email)
                timestamp = datetime.utcnow()

                user = Users(
                    id_user_hash=hashed_user,
                    email=user_email,
                    create_timestamp=timestamp
                )

                db.session.add(user)
                db.session.commit()

            access_token = create_access_token(
                identity=user.id_user_hash, fresh=True
            )
            refresh_token = create_refresh_token(
                identity=user.id_user_hash)

            # Always remember the token for Google sign in
            access_expire = current_app.config["JWT_ACCESS_TOKEN_EXPIRES"]
            refresh_expire = current_app.config["JWT_REFRESH_TOKEN_EXPIRES"]

            message["status"] = 1

            resp = jsonify(message)
            set_access_cookies(resp, access_token, max_age=access_expire)
            set_refresh_cookies(resp, refresh_token,
                                max_age=refresh_expire)
            return resp, 200
        return jsonify(message), 401
    else:
        return jsonify(message), 400


def get_google_auth(state=None, token=None):
    if token:
        return OAuth2Session(
            current_app.config["GOOGLE_LOGIN_CLIENT_ID"],
            token=token
        )
    if state:
        return OAuth2Session(
            current_app.config["GOOGLE_LOGIN_CLIENT_ID"],
            state=state,
            redirect_uri=""
        )

    return OAuth2Session(
        current_app.config["GOOGLE_LOGIN_CLIENT_ID"],
        redirect_uri="postmessage"
    )


def get_google_user(code=""):
    google = get_google_auth()
    current_app.logger.info("checker: " + code)
    try:
        token = google.fetch_token(
            token_url=current_app.config["GOOGLE_TOKEN_URI"],
            client_secret=current_app.config["GOOGLE_LOGIN_CLIENT_SECRET"],
            code=code,
        )
        google = get_google_auth(token=token)
        response = google.get(current_app.config["GOOGLE_USER_INFO"])
        user_data = response.json()
        return user_data

    except Exception as e:
        current_app.logger.error(e)
        return {}
