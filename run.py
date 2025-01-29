# run.py

import os
from dotenv import load_dotenv
from app import create_app

# Determine which environment to load
env = os.environ.get("FLASK_ENV", "production")

# Load the corresponding .env file
if env == "development":
    load_dotenv(dotenv_path=".env.development")
elif env == "testing":
    load_dotenv(dotenv_path=".env.testing")
else:
    load_dotenv(dotenv_path=".env.production")

# Select the appropriate config class
from app.config import DevelopmentConfig, TestingConfig, ProductionConfig

if env == "development":
    config_class = DevelopmentConfig
elif env == "testing":
    config_class = TestingConfig
else:
    config_class = ProductionConfig

app = create_app(config_class)

if __name__ == "__main__":
    app.run()
