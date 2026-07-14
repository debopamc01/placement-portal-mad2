import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# ADMIN_EMAIL = "admin@example.com"
ADMIN_EMAIL = "22f1000777@ds.study.iitm.ac.in"
ADMIN_PASSWORD = "Admin@12345"
DB_PATH = os.path.join(BASE_DIR, "backend_app", "instance")
DB_FILE_NAME = "placement.db"
UPLOAD_FOLDER_PATH = os.path.join(BASE_DIR, "uploads", "resumes")
ALLOWED_RESUME_FILE_EXTENSIONS = {"pdf"}  # always in lowercase


class Config:
    SECRET_KEY = "secret-key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(DB_PATH, DB_FILE_NAME)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = UPLOAD_FOLDER_PATH
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024  # 8 MB for resume files, unused now

    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True

    MAIL_USERNAME = os.getenv("MAIL_ADDRESS")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
