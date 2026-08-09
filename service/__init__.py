"""Flask application factory for the Customer Accounts service."""

from flask import Flask
from flask_cors import CORS
from flask_talisman import Talisman

from service.config import Config
from service.models import db


def create_app(config_class=Config):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    Talisman(
        app,
        force_https=app.config.get("TALISMAN_FORCE_HTTPS", False),
        content_security_policy={
            "default-src": "'self'",
            "object-src": "'none'",
        },
        referrer_policy="strict-origin-when-cross-origin",
    )
    CORS(app, resources={r"/(api/)?accounts.*": {"origins": "*"}})

    from service.routes import register_routes

    register_routes(app)

    with app.app_context():
        db.create_all()

    return app


app = create_app()
