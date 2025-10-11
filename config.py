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
    # Use a default dev key if not set
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    # Parse JWT_EXPIRES_MIN robustly
    raw_jwt = os.getenv("JWT_EXPIRES_MIN")
    if raw_jwt is None:
        JWT_EXPIRES_MIN = 60
    else:
        try:
            JWT_EXPIRES_MIN = int(raw_jwt)
        except Exception:
            m = re.search(r"\d+", raw_jwt)
            if m:
                JWT_EXPIRES_MIN = int(m.group())
            else:
                JWT_EXPIRES_MIN = 60  # fallback

    # --- Caching ---
    CACHE_TYPE = os.getenv("CACHE_TYPE", "SimpleCache")  # for dev
    CACHE_DEFAULT_TIMEOUT = 60

    # --- Rate limiting ---
    RATELIMIT_DEFAULT = os.getenv("RATELIMIT_DEFAULT", "100 per hour")
    if not re.match(r"^\d+ per \w+$", RATELIMIT_DEFAULT):
        RATELIMIT_DEFAULT = "100 per hour"  # fallback safe value

class Development(Config):
    DEBUG = True

class Production(Config):
    DEBUG = False
