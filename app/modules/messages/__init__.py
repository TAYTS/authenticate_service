from flask import Blueprint

# Import all the view function
from app.modules.messages.create_access_token import create_access_token
from app.modules.messages.create_chat_user import create_chat_user
from app.modules.messages.create_channel import create_channel
from app.modules.messages.join_channel import join_channel

# Define the blueprint name
module = Blueprint("messages", __name__)

module.add_url_rule("/messages/get_access_token",
                    view_func=create_access_token, methods=["GET"])
module.add_url_rule("/messages/create_chat_user",
                    view_func=create_chat_user, methods=["POST"])
module.add_url_rule("/messages/create_channel",
                    view_func=create_channel, methods=["POST"])
module.add_url_rule("/messages/join_channel",
                    view_func=join_channel, methods=["POST"])
