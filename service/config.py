"""Configuration for the Accounts service."""

import os


class Config:
    """Base configuration."""

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "sqlite:///accounts.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False
    TALISMAN_FORCE_HTTPS = os.getenv("TALISMAN_FORCE_HTTPS", "false").lower() == "true"
