from flask import jsonify
from flask_jwt_extended import unset_jwt_cookies


def logout():
    resp = jsonify({'status': 1})
    unset_jwt_cookies(resp)
    return resp, 200
