from flask import Blueprint

service_tickets_bp = Blueprint("service_tickets", __name__)

# Import routes AFTER the blueprint is created to avoid circular imports
from . import routes  # noqa: E402,F401
