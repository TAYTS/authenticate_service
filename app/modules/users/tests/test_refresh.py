from flask import url_for
from app.tests.test_base import UserUnitTest
import json

# Import helper functions
from app.tests.utils import get_cookie_from_response


class RefreshTest(UserUnitTest):

    def test_with_valid_cookies(self):
        # Get the JWT token cookie
        response = self.client.post(
            url_for("users.login"),
            data=json.dumps({
                "username": "testing1@gmail.com",
                "password": "password"
            }),
            content_type="application/json"
        )

        # Define the required cookie names
        csrf_token_name = "csrf_refresh_token"
        refresh_token_name = "refresh_token_cookie"

        # Extract the access token cookie
        refresh_token = get_cookie_from_response(
            response,
            refresh_token_name
        )

        # Set test client refresh_token_cookie
        self.client.set_cookie(
            server_name=refresh_token["domain"],
            key=refresh_token_name,
            value=refresh_token[refresh_token_name],
            path=refresh_token["path"])

        # Extract the csrf_refresh_token
        csrf_token = get_cookie_from_response(
            response,
            csrf_token_name
        )[csrf_token_name]

        # Create the header for csrf token
        csrf_headers = {
            "X-CSRF-TOKEN": csrf_token
        }

        """ TESTING """
        response = self.client.get(
            url_for("users.refresh"),
            content_type="application/json",
            headers=csrf_headers
        )

        self.assert200(response)
        self.assertEqual(
            response.get_json(),
            {"status": 1}
        )

    def test_without_cookies(self):
        # Get the JWT token cookie
        response = self.client.post(
            url_for("users.login"),
            data=json.dumps({
                "username": "testing1@gmail.com",
                "password": "password"
            }),
            content_type="application/json"
        )

        # Define the required cookie names
        csrf_token_name = "csrf_refresh_token"

        # Extract the csrf_refresh_token
        csrf_token = get_cookie_from_response(
            response,
            csrf_token_name
        )[csrf_token_name]

        # Create the header for csrf token
        csrf_headers = {
            "X-CSRF-TOKEN": csrf_token
        }

        """ TESTING """
        response = self.client.get(
            url_for("users.refresh"),
            content_type="application/json",
            headers=csrf_headers
        )

        self.assert401(response)
        self.assertEqual(
            response.get_json(),
            {"msg": "Missing cookie \"refresh_token_cookie\""}
        )

    def test_without_csrf_header(self):
        # Get the JWT token cookie
        response = self.client.post(
            url_for("users.login"),
            data=json.dumps({
                "username": "testing1@gmail.com",
                "password": "password"
            }),
            content_type="application/json"
        )

        # Define the required cookie names
        refresh_token_name = "refresh_token_cookie"

        # Extract the access token cookie
        refresh_token = get_cookie_from_response(
            response,
            refresh_token_name
        )

        # Set test client refresh_token_cookie
        self.client.set_cookie(
            server_name=refresh_token["domain"],
            key=refresh_token_name,
            value=refresh_token[refresh_token_name],
            path=refresh_token["path"])

        """ TESTING """
        response = self.client.get(
            url_for("users.refresh"),
            content_type="application/json"
        )

        self.assert401(response)
        self.assertEqual(
            response.get_json(),
            {"msg": "Missing CSRF token in headers"}
        )