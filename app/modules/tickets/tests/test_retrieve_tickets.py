from flask import url_for
from app.tests.test_base import UserUnitTest
from uuid import uuid4
from datetime import datetime

# Import database models
from models.db import db
from models.users import Users
from models.tickets import TicketRecords


class TestRetrieveTickets(UserUnitTest):

    def populate_ticket_record(self):
        id_user = db.session.query(Users.id_user).first()
        title = "testing"
        category = "testing"
        # Create 5 ticket records
        for i in range(5):
            id_ticket_hash = str(uuid4())
            id_message = str(uuid4())
            timestamp = datetime.utcnow().replace(microsecond=0)

            ticket = TicketRecords(
                id_ticket_hash=id_ticket_hash,
                id_message=id_message,
                id_creator=id_user,
                title=title,
                category=category,
                create_timestamp=timestamp,
                last_activity_timestamp=timestamp
            )
            db.session.add(ticket)
            db.session.commit()

    def delete_all_ticket_record(self):
        db.session.query(TicketRecords).delete()
        db.session.commit()

    def test_get_tickets_with_token_and_no_data(self):
        self.login_with_valid_credential()

        """ TESTING """
        response = self.client.get(
            url_for("tickets.retrieve_tickets"),
            headers=self.csrf_headers
        )
        self.assert200(response)
        self.assertEqual(
            response.get_json(),
            {"close": [], "open": []}
        )

    def test_get_tickets_with_token_and_data(self):
        # Populate with some testing data
        self.populate_ticket_record()
        self.login_with_valid_credential()

        """ TESTING """
        response = self.client.get(
            url_for("tickets.retrieve_tickets"),
            headers=self.csrf_headers
        )

        resp_body = response.get_json()
        close_count = len(resp_body["close"])
        open_count = len(resp_body["open"])

        self.assert200(response)
        self.assertEqual(close_count, 0)
        self.assertEqual(open_count, 5)
        self.delete_all_ticket_record()

    def test_get_tickets_without_cookie(self):
        """ TESTING """
        response = self.client.get(
            url_for("tickets.retrieve_tickets")
        )

        self.assert401(response)
        self.assertEqual(
            response.get_json(),
            {"msg": "Missing cookie \"access_token_cookie\""}
        )

    def test_get_tickets_without_csrf_token(self):
        self.login_with_valid_credential()

        """ TESTING """
        response = self.client.get(
            url_for("tickets.retrieve_tickets")
        )

        self.assert401(response)
        self.assertEqual(
            response.get_json(),
            {"msg": "Missing CSRF token in headers"}
        )
