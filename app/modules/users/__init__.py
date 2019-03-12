from flask import Blueprint

# Import all the view function
from app.modules.users.Gauth import glogin
from app.modules.users.login import login, refresh, authenticate
from app.modules.users.register import register

# Define the blueprint name
module = Blueprint("users", __name__)

module.add_url_rule("/users/glogin",
                    view_func=glogin, methods=["POST"])
module.add_url_rule("/users/login",
                    view_func=login, methods=['POST'])
module.add_url_rule("/users/refresh",
                    view_func=refresh, methods=['GET'])
module.add_url_rule("/users/authenticate",
                    view_func=authenticate, methods=['GET'])
module.add_url_rule("/users/register",
                    view_func=register, methods=['POST'])
