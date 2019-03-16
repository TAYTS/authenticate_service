from flask import Blueprint

# Import all the view function
from app.modules.tickets.retrieve_tickets import retrieve_tickets

# Define the blueprint name
module = Blueprint("tickets", __name__)

module.add_url_rule("/tickets/retrieve-tickets",
                    view_func=retrieve_tickets, methods=["GET"])
