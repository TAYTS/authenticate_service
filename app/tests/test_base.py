from flask_testing import TestCase
from flask import url_for
from app import make_app
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash
from datetime import datetime
import hashlib
import json

# Import database models
from models.db import db
from models.users import Users

# Import helper functions
from app.tests.utils import get_cookie_from_response


class UserUnitTest(TestCase):
    def create_app(self):
        app = make_app(config="test_config.py")
        db.init_app(app)
        Migrate(app, db)
        return app

    def create_user(self):
        username = "testing1@gmail.com"
        password = "password"
        unhashed_user = "email: " + username + "ESC-Accenture"
        hashed_user = hashlib.sha512(unhashed_user.encode("UTF-8")).hexdigest()
        hashed_password = generate_password_hash(password)
        timestamp = datetime.utcnow()

        user = Users(
            id_user_hash=hashed_user,
            password=hashed_password,
            email=username,
            create_timestamp=timestamp
        )
        db.session.add(user)
        db.session.commit()

    def login_with_valid_credential(self):
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
        self.csrf_headers = {
            "X-CSRF-TOKEN": csrf_token
        }

    def setUp(self):
        self.app = self.create_app()
        self.client = self.app.test_client(use_cookies=True)
        try:
            db.create_all()
        except Exception as e:
            print(e)
        self.create_user()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
