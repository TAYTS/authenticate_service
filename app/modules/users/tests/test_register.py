from flask import url_for
from app.tests.test_base import UserUnitTest
from unittest.mock import patch
import json
import random
import string
from uuid import uuid4


class RegisterTest(UserUnitTest):

    def test_create_new_user_account(self):
        with patch("app.modules.users.register"):
            with patch("requests.post") as mock_post:
                mock_post.return_value.ok = True
                mock_post.return_value.json.return_value = {
                    "id_chat": str(uuid4())
                }

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
