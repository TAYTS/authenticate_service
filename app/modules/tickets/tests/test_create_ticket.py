from flask import url_for
from app.tests.test_base import UserUnitTest
from unittest.mock import patch
import json
from uuid import uuid4

# Import database models
from models.db import db
from models.tickets import TicketRecords


class TestCreateTicket(UserUnitTest):

    def test_create_ticket_with_token_and_data(self):
        self.login_with_valid_credential()
        with patch("app.modules.tickets.create_ticket"):
            with patch("requests.post") as mock_post:
                mock_post.return_value.ok = True
                mock_post.return_value.json.return_value = {
                    "id_channel": str(uuid4()),
                    "id_member": str(uuid4())
                }
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
            {"id_ticket": ticket_records[0].id_ticket_hash}
        )
        self.assertEqual(ticket_count, 1)

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
            {"id_ticket": ""}
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
