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
