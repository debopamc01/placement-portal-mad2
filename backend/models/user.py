from flask_login import UserMixin
from backend.extensions import db, login_manager
from backend.models.model_enums import UserRole
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import validates


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False)

    student = db.relationship(
        "Student", backref="user", cascade="all, delete-orphan", uselist=False
    )
    company = db.relationship(
        "Company", backref="user", cascade="all, delete-orphan", uselist=False
    )

    @validates("password_hash")
    def validate_password_hash(self, key, value):
        """
        Ensure `password_hash` contains a password hash (not raw text).

        This ensures passwords are set using `set_password()` which produces
        an scrypt-prefixed hash (e.g. "scrypt:").
        """

        if not isinstance(value, str) or not value.startswith("scrypt:"):
            raise ValueError(
                "Password must be set using set_password() method, not raw text"
            )
        return value

    def set_password(self, password_str: str) -> None:
        """
        Set password using scrypt hashing algorithm and set the password_hash field to the hashed password.

        Returns None.
        """

        self.password_hash = generate_password_hash(
            password=password_str, method="scrypt"
        )

    def check_password(self, password: str) -> bool:
        """
        Checks if the provided password matches the stored password hash.

        Returns True if the password is correct, False otherwise.
        """

        return check_password_hash(self.password_hash, password)

    @validates("role")
    def validate_role(self, key, role):
        """
        Ensure the provided role is a member of the UserRole enum.

        The validator receives the incoming value (`role`), so we should
        check that rather than accessing `self.role`, which may still be
        ``None`` during object construction.  A NoneType would otherwise
        trigger a ``TypeError`` when used with ``in``.
        """
        if role not in UserRole:
            raise ValueError("Invalid user role")
        return role

    @validates("email")
    def validate_email(self, key, email):
        """
        Validates the email format.

        Returns the email if it is valid, raises ValueError otherwise.
        """
        valid = True
        parts = email.split("@")

        if len(parts) != 2:
            valid = False
        else:
            domain_parts = parts[-1].split(".")
            if len(domain_parts) < 2:
                valid = False
        if not valid:
            raise ValueError("Invalid email format")
        return email


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
