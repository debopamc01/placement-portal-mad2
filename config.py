import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "Admin@12345"

class Config:
    SECRET_KEY = "secret-key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
        BASE_DIR, "backend", "instance", "placement.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False