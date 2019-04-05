from flask import url_for
from app.tests.test_base import UserUnitTest
import json
import random
import string


class RegisterTest(UserUnitTest):
    def test_create_new_user_account(self):
        username = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=10))
        response = self.client.post(
            url_for("users.register"),
            data=json.dumps({
                "username": username,
                "email": username + "@gmail.com",
                "password": "password"
            }),
            content_type="application/json"
        )
        self.assert_status(response, 201)
        self.assertEqual(
            response.get_json(),
            {"status": 1}
        )

    def test_create_duplicate_account(self):
        response = self.client.post(
            url_for("users.register"),
            data=json.dumps({
                "username": self.user.username,
                "email": self.user.email,
                "password": "password"
            }),
            content_type="application/json"
        )

        self.assertStatus(response, 409)
        self.assertEqual(
            response.get_json(),
            {"status": -1}
        )
