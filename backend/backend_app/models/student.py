from __future__ import annotations

from typing import Optional, TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend_app.extensions import db

if TYPE_CHECKING:
    from backend_app.models.job_application import JobApplication
    from backend_app.models.user import User


class Student(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    name: Mapped[str] = mapped_column(nullable=False)
    resume_url: Mapped[Optional[str]] = mapped_column(nullable=True)
    description: Mapped[Optional[str]] = mapped_column(nullable=True)
    blacklisted: Mapped[bool] = mapped_column(default=False, nullable=False)
    applications: Mapped[list[JobApplication]] = relationship(
        "JobApplication", back_populates="student", cascade="all, delete-orphan"
    )
    user: Mapped[User] = relationship(
        "User",
        back_populates="student",
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "email": self.user.email,
            "name": self.name,
            "description": self.description,
            "blacklisted": self.blacklisted,
        }
