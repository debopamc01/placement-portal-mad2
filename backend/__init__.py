import os

from flask import Flask

from config import BASE_DIR, Config, ADMIN_EMAIL, ADMIN_PASSWORD
from backend.models.model_enums import UserRole
from backend.extensions import db, login_manager
from backend.routes.auth import auth_bp
from backend.routes.frontend import frontend_bp
from backend.routes.admin import admin_bp
from backend.routes.company import company_bp
from backend.models.company import Company
from backend.models.job_application import JobApplication
from backend.models.placement_drive import PlacementDrive
from backend.models.student import Student
from backend.models.user import User


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
    # Get the parent directory (project root) to locate templates folder
    template_dir = os.path.abspath(os.path.join(BASE_DIR, "backend", "templates"))
    static_dir = os.path.abspath(os.path.join(BASE_DIR, "backend", "static"))
    os.makedirs(os.path.join(BASE_DIR, "backend", "instance"), exist_ok=True)
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(frontend_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(company_bp)
    with app.app_context():
        db.create_all()
        create_admin()

    return app
