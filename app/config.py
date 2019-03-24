""" Development Configurations """
from datetime import timedelta

# SQL
SQLALCHEMY_DATABASE_URI = (
    ""
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_POOL_RECYCLE = 299
SQLALCHEMY_POOL_RECYCLE = 20
PREFERRED_URL_SCHEME = "https"

# Log
APP_LOG_FILE = "log/app.log"
APP_LOG_LEVEL = "DEBUG"

# JWT
JWT_SECRET_KEY = "secret-key"
JWT_TOKEN_LOCATION = "cookies"
JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7300)
JWT_CSRF_METHODS = ["GET", "POST", "PUT", "DELETE"]
JWT_COOKIE_SECURE = False
JWT_COOKIE_DOMAIN = ""

# GOOGLE
GOOGLE_LOGIN_CLIENT_ID = ""
GOOGLE_LOGIN_CLIENT_SECRET = ""
GOOGLE_AUTH_URI = "https://accounts.google.com/o/oauth2/auth"
GOOGLE_TOKEN_URI = "https://accounts.google.com/o/oauth2/token"
GOOGLE_USER_INFO = "https://www.googleapis.com/userinfo/v2/me"

# AWS
AWS_REGION = "ap-southeast-1"
AWS_KEY = ""
AWS_SECRET_ACCESS_KEY = ""
# DynamoDB
DYNAMO_TABLENAME = "MESSAGE_RECORDS"
