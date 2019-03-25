from flask import request, jsonify, current_app
from werkzeug.security import generate_password_hash
from datetime import datetime
from sqlalchemy import exc

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
    password = str(request.json.get("password"))

    if not(username and password):
        return jsonify({"status": 0}), 400

    hashed_user = create_user_hash(username)

    hashed_password = generate_password_hash(password)
    timestamp = datetime.utcnow()

    user = Users(
        id_user_hash=hashed_user,
        password=hashed_password,
        email=username,
        create_timestamp=timestamp
    )

    try:
        db.session.add(user)
        db.session.commit()
        status = 1
        return jsonify({"status": status}), 201
    except exc.IntegrityError:
        status = -1
        return jsonify({"status": status}), 409
    except Exception as e:
        current_app.logger.info('Failed to add new user: ' + str(e))
        status = 0
        return jsonify({"status": status}), 500
