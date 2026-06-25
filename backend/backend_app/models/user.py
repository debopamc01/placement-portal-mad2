from __future__ import annotations

from typing import TYPE_CHECKING, Optional
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import Mapped, relationship, mapped_column, validates

from backend_app.extensions import db, login_manager
from backend_app.models.model_enums import UserRole

if TYPE_CHECKING:
    from backend_app.models.company import Company
    from backend_app.models.student import Student


class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[UserRole] = mapped_column(type_=db.Enum(UserRole), nullable=False)

    student: Mapped[Optional[Student]] = relationship(
        "Student", back_populates="user", cascade="all, delete-orphan", uselist=False
    )
    company: Mapped[Optional[Company]] = relationship(
        "Company", back_populates="user", cascade="all, delete-orphan", uselist=False
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "role": self.role.value,
        }

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
        if not isinstance(role, UserRole):
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
def load_user(user_id) -> User | None:
    return db.session.get(User, int(user_id))
