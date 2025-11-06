from flask import Flask, jsonify
from .extensions import db, ma, limiter, cache, migrate
from .models import Customer, Mechanic, ServiceTicket, Inventory
from .blueprints.customers import customers_bp
from .blueprints.mechanics import mechanics_bp
from .blueprints.service_tickets import service_tickets_bp
from .blueprints.inventory import inventory_bp
from application.config import DevelopmentConfig  # ✅ Import config once at the top


def create_app():
    app = Flask(__name__)

    # ✅ Load configuration from config class
    app.config.from_object(DevelopmentConfig)

    # ✅ Initialize extensions
    db.init_app(app)
    ma.init_app(app)
    cache.init_app(app, config=app.config)
    limiter.init_app(app)
    migrate.init_app(app, db)

    # ✅ Register blueprints
    app.register_blueprint(customers_bp, url_prefix="/customers")
    app.register_blueprint(mechanics_bp, url_prefix="/mechanics")
    app.register_blueprint(service_tickets_bp, url_prefix="/service_tickets")
    app.register_blueprint(inventory_bp, url_prefix="/inventory")

    # ✅ Default route
    @app.get("/")
    def home():
        return jsonify({
            "message": "Mechanic API running ✅",
            "endpoints": {
                "customers": "/customers",
                "mechanics": "/mechanics",
                "service_tickets": "/service_tickets",
                "inventory": "/inventory",
            }
        })

    # ✅ Ensure tables exist
    with app.app_context():
        db.create_all()

    return app
