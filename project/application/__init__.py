from flask import Flask, jsonify
from flask_swagger_ui import get_swaggerui_blueprint

from .config.init import DevelopmentConfig, TestingConfig, ProductionConfig
from .extensions import db, ma, limiter, cache, migrate
from .models import Customer, Mechanic, ServiceTicket, Inventory

# Blueprints
from .blueprints.customers import customers_bp
from .blueprints.mechanics import mechanics_bp
from .blueprints.service_tickets import service_tickets_bp
from .blueprints.inventory import inventory_bp


# ----------------------------------------
# Swagger Configuration
# ----------------------------------------
SWAGGER_URL = "/api/docs"
API_URL = "/static/swagger.yaml"

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={"app_name": "Mechanic Service API"}
)


# ----------------------------------------
# Flask Application Factory
# ----------------------------------------
def create_app(config_name="DevelopmentConfig"):
    app = Flask(__name__, static_folder="static")

    # ------------------------
    # Load Correct Configuration
    # ------------------------
    if config_name == "TestingConfig":
        app.config.from_object(TestingConfig)
    elif config_name == "ProductionConfig":
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    # ❌ DO NOT RE-LOAD DEVELOPMENT CONFIG AGAIN
    # ❌ REMOVE THIS ENTIRE LINE:
    # app.config.from_object(DevelopmentConfig)
    #
    # That line overwrites TestingConfig and BROKE all your tests.
    # KEEP IT DELETED.


    # ------------------------
    # Initialize Extensions
    # ------------------------
    db.init_app(app)
    ma.init_app(app)
    cache.init_app(app, config=app.config)
    limiter.init_app(app)
    migrate.init_app(app, db)

    # ------------------------
    # Register Blueprints
    # ------------------------
    app.register_blueprint(customers_bp, url_prefix="/customers/")
    app.register_blueprint(mechanics_bp, url_prefix="/mechanics/")
    app.register_blueprint(service_tickets_bp, url_prefix="/service_tickets/")
    app.register_blueprint(inventory_bp, url_prefix="/inventory/")
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    # ------------------------
    # Default Home Route
    # ------------------------
    @app.get("/")
    def home():
        return jsonify({
            "message": "Mechanic API running ✅",
            "docs": f"Visit {SWAGGER_URL} for API documentation",
            "endpoints": {
                "customers": "/customers",
                "mechanics": "/mechanics",
                "service_tickets": "/service_tickets",
                "inventory": "/inventory"
            }
        })

    # Only auto-create tables in Testing mode
    if config_name == "TestingConfig":
        with app.app_context():
            db.create_all()


    return app
