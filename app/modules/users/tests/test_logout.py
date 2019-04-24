from flask import url_for
from app.tests.test_base import UserUnitTest

# Import helper functions
from app.tests.utils import get_cookie_from_response


class LogoutTest(UserUnitTest):

    def test_logout(self):
        response = self.client.post(
            url_for("users.logout"),
            content_type="application/json"
        )

        access_token_cookie = get_cookie_from_response(
            response,
            "access_token_cookie"
        )["access_token_cookie"]
        refresh_token_cookie = get_cookie_from_response(
            response,
            "refresh_token_cookie"
        )["refresh_token_cookie"]
        csrf_access_token = get_cookie_from_response(
            response,
            "csrf_access_token"
        )["csrf_access_token"]
        csrf_refresh_token = get_cookie_from_response(
            response,
            "csrf_refresh_token"
        )["csrf_refresh_token"]

        self.assertEqual(access_token_cookie, "")
        self.assertEqual(refresh_token_cookie, "")
        self.assertEqual(csrf_access_token, "")
        self.assertEqual(csrf_refresh_token, "")
