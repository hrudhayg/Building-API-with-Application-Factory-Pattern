import os

class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:yourpassword@localhost/mechanicdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RATELIMIT_DEFAULT = "60 per minute"
    CACHE_TYPE = "SimpleCache"
    SECRET_KEY = os.environ.get("SECRET_KEY", "devsecret")

    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "supersecretjwtkey")
    JWT_ALGORITHM = "HS256"
    JWT_ISSUER = "mechanic_api"
    JWT_EXPIRES_MIN = 60
    JWT_AUDIENCE = "mechanic_api_users"



class TestingConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CACHE_TYPE = "SimpleCache"
    SECRET_KEY = "testsecret"

    RATELIMIT_ENABLED = False    # disable rate limiting for tests
    RATELIMIT_DEFAULT = "1000/minute"

    # JWT settings needed so encode_token doesn't break
    JWT_SECRET_KEY = "testjwtsecret"
    JWT_ALGORITHM = "HS256"
    JWT_ISSUER = "mechanic_api_test"
    JWT_EXPIRES_MIN = 999
    JWT_AUDIENCE = "mechanic_api_test_users"

