import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

load_dotenv()
from config import (
    DB_PATH,
    UPLOAD_FOLDER_PATH,
    Config,
    ADMIN_EMAIL,
    ADMIN_PASSWORD,
)
from backend_app.models.model_enums import UserRole
from backend_app.extensions import db, login_manager, mail
from backend_app.routes.auth import auth_bp
from backend_app.routes.admin import admin_bp
from backend_app.routes.student import student_bp
from backend_app.routes.company import company_bp
from backend_app.models.company import Company
from backend_app.models.job_application import JobApplication
from backend_app.models.placement_drive import PlacementDrive
from backend_app.models.student import Student
from backend_app.models.user import User


def create_admin() -> None:
    admin = db.session.scalar(db.select(User).where(User.email == ADMIN_EMAIL))
    if not admin:
        new_user = User()
        new_user.email = ADMIN_EMAIL
        new_user.role = UserRole.ADMIN
        new_user.set_password(ADMIN_PASSWORD)
        db.session.add(new_user)
        db.session.commit()


def create_backend_app():
    os.makedirs(DB_PATH, exist_ok=True)
    os.makedirs(UPLOAD_FOLDER_PATH, exist_ok=True)
    app = Flask(__name__)

    CORS(
        app,
        supports_credentials=True,
        origins=["http://127.0.0.1:5173"],
    )
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(company_bp)
    app.register_blueprint(student_bp)
    with app.app_context():
        db.create_all()
        create_admin()
    return app
