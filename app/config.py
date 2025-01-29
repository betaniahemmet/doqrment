
import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "fallback-secret")
    FLASK_ENV = os.environ.get("FLASK_ENV", "production")
    DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///prod_db.sqlite3")
    DEBUG = os.environ.get("DEBUG", "False").lower() == "true"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Add other common configurations here

class DevelopmentConfig(Config):
    DEBUG = True
    FLASK_ENV = "development"
    DATABASE_URL = os.environ.get("DEV_DATABASE_URL", "sqlite:///dev_db.sqlite3")
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    # Development-specific configurations
    LOG_LEVEL = "DEBUG"

class ProductionConfig(Config):
    DEBUG = False
    FLASK_ENV = "production"
    DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///prod_db.sqlite3")
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    # Production-specific configurations
    LOG_LEVEL = "WARNING"

class TestingConfig(Config):
    TESTING = True
    FLASK_ENV = "testing"
    DATABASE_URL = os.environ.get("TEST_DATABASE_URL", "sqlite:///test_db.sqlite3")
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    # Testing-specific configurations
    LOG_LEVEL = "DEBUG"
