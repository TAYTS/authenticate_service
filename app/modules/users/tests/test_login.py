from flask import url_for
from app.tests.test_base import UserUnitTest
import json


class LoginTest(UserUnitTest):

    def test_with_valid_credentials(self):
        response = self.client.post(
            url_for("users.login"),
            data=json.dumps({
                "username": "testing1@gmail.com",
                "password": "password"
            }),
            content_type="application/json"
        )
        cookies = response.headers.getlist("Set-Cookie")

        self.assert200(response)
        self.assertEqual(len(cookies), 4)
        self.assertEqual(
            response.get_json(),
            {"status": 1}
        )

    def test_with_invalid_credentials(self):
        response = self.client.post(
            url_for("users.login"),
            data=json.dumps({
                "username": "test@gmail.com",
                "password": "password"
            }),
            content_type="application/json"
        )
        self.assert401(response)
        self.assertEqual(
            response.get_json(),
            {"status": 0}
        )

    def test_with_empty_parameter(self):
        response = self.client.post(
            url_for("users.login"),
            data=json.dumps({
                "username": "",
                "password": ""
            }),
            content_type="application/json"
        )
        self.assert401(response)
        self.assertEqual(
            response.get_json(),
            {"status": 0}
        )
