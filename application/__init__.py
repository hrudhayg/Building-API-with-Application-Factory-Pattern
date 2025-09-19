from flask import Flask, jsonify
from .extensions import db, ma
from .models import Customer, Mechanic, ServiceTicket  # ensure models are registered
from .blueprints.customers import customers_bp
from .blueprints.mechanics import mechanics_bp
from .blueprints.service_tickets import service_tickets_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # init extensions
    db.init_app(app)
    ma.init_app(app)

    # create tables
    with app.app_context():
        db.create_all()

    # blueprints
    app.register_blueprint(customers_bp, url_prefix="/customers")
    app.register_blueprint(mechanics_bp, url_prefix="/mechanics")
    app.register_blueprint(service_tickets_bp, url_prefix="/service_tickets")

    # simple home
    @app.get("/")
    def home():
        return jsonify({
            "message": "Welcome to the Mechanic API 🚗🔧",
            "endpoints": {
                "customers": "/customers",
                "mechanics": "/mechanics",
                "tickets": "/tickets"
            }
        })

    return app
