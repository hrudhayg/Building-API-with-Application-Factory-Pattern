import os
import re

class Config:
    # --- DB ---
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"mysql+mysqlconnector://{os.getenv('DB_USER', 'root')}:{os.getenv('DB_PASSWORD', 'A4%40mysql')}@{os.getenv('DB_HOST', '127.0.0.1')}/{os.getenv('DB_NAME', 'mechanic_db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --- Secrets / Tokens ---
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    # --- JWT ---
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "supersecretjwtkey")
    JWT_ALGORITHM = "HS256"
    JWT_ISSUER = "mechanic_api"
    JWT_AUDIENCE = "mechanic_clients"


    # --- Expiry ---
    raw_jwt = os.getenv("JWT_EXPIRES_MIN")
    if raw_jwt is None:
        JWT_EXPIRES_MIN = 60
    else:
        try:
            JWT_EXPIRES_MIN = int(raw_jwt)
        except Exception:
            m = re.search(r"\d+", raw_jwt)
            JWT_EXPIRES_MIN = int(m.group()) if m else 60

    # --- Caching ---
    CACHE_TYPE = os.getenv("CACHE_TYPE", "SimpleCache")
    CACHE_DEFAULT_TIMEOUT = 60

    # --- Rate limiting ---
    RATELIMIT_DEFAULT = os.getenv("RATELIMIT_DEFAULT", "100 per hour")
    if not re.match(r"^\d+ per \w+$", RATELIMIT_DEFAULT):
        RATELIMIT_DEFAULT = "100 per hour"


class DevelopmentConfig(Config):
    DEBUG = True


class Production(Config):
    DEBUG = False
