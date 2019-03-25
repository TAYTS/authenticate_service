from flask import jsonify, current_app
from flask_jwt_extended import (
    jwt_refresh_token_required,
    get_jwt_identity,
    create_access_token,
    set_access_cookies
)

# Import database models
from models.db import db
from models.users import Users


@jwt_refresh_token_required
def refresh():
    """
    Return new JWT token with update expired time

    Returns:
        {"status" : 0} if failed to authenticate the user
        {"status" : 1} if successfully authenticate the user
    """
    id_user_hash = get_jwt_identity()
    message = {"status": 0}

    if id_user_hash:
        user = db.session.query(Users).filter(
            Users.id_user_hash == id_user_hash
        ).first()
        if user:
            access_token = create_access_token(
                identity=id_user_hash, fresh=False)
            access_expire = current_app.config["JWT_ACCESS_TOKEN_EXPIRES"]

            message["status"] = 1
            resp = jsonify(message)
            set_access_cookies(resp, access_token, max_age=access_expire)
            return resp, 200
        else:
            return jsonify(message), 401
    else:
        return jsonify(message), 401