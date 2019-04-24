from flask import url_for
from app.tests.test_base import UserUnitTest
import json

# Import helper functions
from app.tests.utils import get_cookie_from_response


class AuthenticateTest(UserUnitTest):

    def test_with_valid_cookies(self):
        # Get the JWT token cookie
        response = self.client.post(
            url_for("users.login"),
            data=json.dumps({
                "email": self.user.email,
                "password": "password"
            }),
            content_type="application/json"
        )

        # Define the required cookie names
        csrf_token_name = "csrf_access_token"
        access_token_name = "access_token_cookie"

        # Extract the access token cookie
        access_token = get_cookie_from_response(
            response,
            access_token_name
        )

        # Set test client access_token_cookie
        self.client.set_cookie(
            server_name=access_token["domain"],
            key=access_token_name,
            value=access_token[access_token_name],
            path=access_token["path"])

        # Extract the csrf_access_token
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
            url_for("users.authenticate"),
            content_type="application/json",
            headers=csrf_headers
        )

        self.assert200(response)
        self.assertEqual(
            response.get_json(),
            {"id_user_hash": self.user.id_user_hash}
        )

    def test_without_cookies(self):
        # Get the JWT token cookie
        response = self.client.post(
            url_for("users.login"),
            data=json.dumps({
                "email": self.user.email,
                "password": "password"
            }),
            content_type="application/json"
        )

        # Define the required cookie names
        csrf_token_name = "csrf_access_token"

        # Extract the csrf_access_token
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
            url_for("users.authenticate"),
            content_type="application/json",
            headers=csrf_headers
        )

        self.assert401(response)
        self.assertEqual(
            response.get_json(),
            {"msg": "Missing cookie \"access_token_cookie\""}
        )

    def test_without_csrf_header(self):
        # Get the JWT token cookie
        response = self.client.post(
            url_for("users.login"),
            data=json.dumps({
                "email": self.user.email,
                "password": "password"
            }),
            content_type="application/json"
        )

        # Define the required cookie names
        access_token_name = "access_token_cookie"

        # Extract the access token cookie
        access_token = get_cookie_from_response(
            response,
            access_token_name
        )

        # Set test client access_token_cookie
        self.client.set_cookie(
            server_name=access_token["domain"],
            key=access_token_name,
            value=access_token[access_token_name],
            path=access_token["path"])

        """ TESTING """
        response = self.client.get(
            url_for("users.authenticate"),
            content_type="application/json"
        )

        self.assert401(response)
        self.assertEqual(
            response.get_json(),
            {"msg": "Missing CSRF token in headers"}
        )
