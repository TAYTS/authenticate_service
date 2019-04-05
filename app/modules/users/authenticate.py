from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

# Import database models
from models.db import db
from models.users import Users


@jwt_required
def authenticate():
    """
    Validate the JWT token.
    Returns:
        {"id_user_hash" : "id-user-hash"}
    """
    id_user_hash = get_jwt_identity()
    message = {"id_user_hash": ""}

    if id_user_hash:
        user = db.session.query(Users).filter(
            Users.id_user_hash == id_user_hash
        ).first()
        if user:
            message["id_user_hash"] = id_user_hash
            return jsonify(message), 200
        else:
            return jsonify(message), 401
    else:
        return jsonify(message), 401
