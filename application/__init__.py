from flask import Flask, jsonify
from .extensions import db, ma, limiter, cache, migrate
from .models import Customer, Mechanic, ServiceTicket, Inventory
from .blueprints.customers import customers_bp
from .blueprints.mechanics import mechanics_bp
from .blueprints.service_tickets import service_tickets_bp
from .blueprints.inventory import inventory_bp

def create_app(config_object="config.Development"):
    app = Flask(__name__)
    app.config.from_object(config_object)

    # Init extensions
    db.init_app(app)
    ma.init_app(app)
    cache.init_app(app, config=app.config)
    limiter.init_app(app)  # uses RATELIMIT_DEFAULT from config
    migrate.init_app(app, db)

    # Blueprints
    app.register_blueprint(customers_bp, url_prefix="/customers")
    app.register_blueprint(mechanics_bp, url_prefix="/mechanics")
    app.register_blueprint(service_tickets_bp, url_prefix="/service_tickets")
    app.register_blueprint(inventory_bp, url_prefix="/inventory")

    @app.get("/")
    def home():
        return jsonify({
            "message": "Mechanic API",
            "endpoints": {
                "customers": "/customers",
                "mechanics": "/mechanics",
                "service_tickets": "/service_tickets",
                "inventory": "/inventory",
            }
        })

    with app.app_context():
        db.create_all()

    return app
