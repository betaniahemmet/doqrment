import os

from dotenv import load_dotenv

# Calculate base directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# Determine the environment and load the correct .env file
env = os.getenv("FLASK_ENV", "development")
env_file = f".env.{env}"
load_dotenv(env_file)


class Config:
    BASE_DIR = BASE_DIR
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret")
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///mood_tracking.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
