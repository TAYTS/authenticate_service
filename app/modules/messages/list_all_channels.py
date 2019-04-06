from flask import current_app
from twilio.rest import Client


def list_all_channels():
    account_sid = current_app.config["TWILIO_ACCOUNT_SID"]
    auth_token = current_app.config["TWILIO_AUTH_TOKEN"]
    client = Client(account_sid, auth_token)
    chat_sid = current_app.config["TWILIO_CHAT_SID"]

    channels = client.chat.services(chat_sid)\
        .channels\
        .list()

    for record in channels:
        print(record.type)
