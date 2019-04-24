from flask import url_for
from app.tests.test_base import UserUnitTest
import json


class LoginTest(UserUnitTest):

    def test_with_valid_credentials(self):
        response = self.client.post(
            url_for("users.login"),
            data=json.dumps({
                "email": self.user.email,
                "password": "password"
            }),
            content_type="application/json"
        )
        cookies = response.headers.getlist("Set-Cookie")

        self.assert200(response)
        self.assertEqual(len(cookies), 4)
        self.assertEqual(
            response.get_json(),
            {"id_user_hash": self.user.id_user_hash}
        )

    def test_with_invalid_credentials(self):
        response = self.client.post(
            url_for("users.login"),
            data=json.dumps({
                "email": "test@gmail.com",
                "password": "password"
            }),
            content_type="application/json"
        )
        self.assert401(response)
        self.assertEqual(
            response.get_json(),
            {"id_user_hash": ""}
        )

    def test_with_empty_parameter(self):
        response = self.client.post(
            url_for("users.login"),
            data=json.dumps({
                "email": "",
                "password": ""
            }),
            content_type="application/json"
        )
        self.assert401(response)
        self.assertEqual(
            response.get_json(),
            {"id_user_hash": ""}
        )
