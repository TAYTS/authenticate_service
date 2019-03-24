from flask_testing import TestCase
from app import make_app
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash
import hashlib
from datetime import datetime

# Import database models
from models.db import db
from models.users import Users


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
