import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-secret')
    FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///mood_tracking.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False