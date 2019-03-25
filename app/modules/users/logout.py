from flask import jsonify
from flask_jwt_extended import unset_jwt_cookies


def logout():
    """
    Return response to remove the JWT token saved in the browser

    Returns:
        {"status" : 1}
    """
    resp = jsonify({'status': 1})
    unset_jwt_cookies(resp)
    return resp, 200
