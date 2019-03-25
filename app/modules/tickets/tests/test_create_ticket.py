from flask import url_for, current_app
from app.tests.test_base import UserUnitTest
import json
import boto3

# Import database models
from models.db import db
from models.tickets import TicketRecords


class TestCreateTicket(UserUnitTest):

    def remove_data_from_dynamoDB(self, id_message, create_timestamp):
        dynamodb = boto3.client(
            "dynamodb",
            region_name=current_app.config["AWS_REGION"],
            aws_access_key_id=current_app.config["AWS_KEY"],
            aws_secret_access_key=current_app.config["AWS_SECRET_ACCESS_KEY"]
        )

        dynamodb.delete_item(
            TableName=current_app.config["DYNAMO_TABLENAME"],
            Key={
                "ID_MESSAGE": {
                    "S": id_message
                },
                "CREATE_TIMESTAMP": {
                    "N": str(create_timestamp.timestamp())
                }
            }
        )

    def test_create_ticket_with_token_and_data(self):
        self.login_with_valid_credential()

        response = self.client.post(
            url_for("tickets.create_ticket"),
            data=json.dumps({
                "title": "testing",
                "category": "testing",
                "message": "testing message"
            }),
            content_type="application/json",
            headers=self.csrf_headers
        )

        ticket_records = db.session.query(TicketRecords).all()
        ticket_count = len(ticket_records)

        self.assert_status(response, 201)
        self.assertEqual(
            response.get_json(),
            {"status": 1}
        )
        self.assertEqual(ticket_count, 1)

        # Remove test record from dynamoDB
        self.remove_data_from_dynamoDB(
            ticket_records[0].id_message,
            ticket_records[0].create_timestamp
        )

    def test_create_ticket_with_token_and_no_data(self):
        self.login_with_valid_credential()

        response = self.client.post(
            url_for("tickets.create_ticket"),
            data=json.dumps({
                "title": "",
                "category": "",
                "message": ""
            }),
            content_type="application/json",
            headers=self.csrf_headers
        )

        ticket_records = db.session.query(TicketRecords).all()
        ticket_count = len(ticket_records)

        self.assert400(response)
        self.assertEqual(
            response.get_json(),
            {"status": 0}
        )
        self.assertEqual(ticket_count, 0)

    def test_create_ticket_without_cookie(self):
        response = self.client.post(
            url_for("tickets.create_ticket"),
            data=json.dumps({
                "title": "testing",
                "category": "testing",
                "message": "testing message"
            }),
            content_type="application/json"
        )

        self.assert401(response)
        self.assertEqual(
            response.get_json(),
            {"msg": "Missing cookie \"access_token_cookie\""}
        )

    def test_create_ticket_without_csrf_token(self):
        self.login_with_valid_credential()

        response = self.client.post(
            url_for("tickets.create_ticket"),
            data=json.dumps({
                "title": "testing",
                "category": "testing",
                "message": "testing message"
            }),
            content_type="application/json"
        )

        self.assert401(response)
        self.assertEqual(
            response.get_json(),
            {"msg": "Missing CSRF token in headers"}
        )
