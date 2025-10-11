from datetime import datetime, timedelta, timezone
from functools import wraps
from typing import Callable, Any, Optional

from flask import current_app, request, jsonify
from jose import jwt, JWTError

def encode_token(customer_id: int) -> str:
    """
    Returns a JWT for the given customer_id.
    """
    now = datetime.now(timezone.utc)
    exp = now + timedelta(minutes=current_app.config["JWT_EXPIRES_MIN"])
    payload = {
        "sub": str(customer_id),
        "iss": current_app.config["JWT_ISSUER"],
        "aud": current_app.config["JWT_AUDIENCE"],
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp()),
        "role": "customer",
    }
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")

def token_required(fn: Callable[..., Any]):
    """
    Decorator that validates Bearer token and injects customer_id into the view.
    View must accept parameter `customer_id`.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return jsonify({"error": "Missing or invalid Authorization header"}), 401
        token = auth.split(" ", 1)[1].strip()
        try:
            payload = jwt.decode(
                token,
                current_app.config["SECRET_KEY"],
                algorithms=["HS256"],
                issuer=current_app.config["JWT_ISSUER"],
                audience=current_app.config["JWT_AUDIENCE"],
            )
            customer_id = int(payload.get("sub"))
        except JWTError:
            return jsonify({"error": "Invalid or expired token"}), 401

        kwargs["customer_id"] = customer_id
        return fn(*args, **kwargs)
    return wrapper
