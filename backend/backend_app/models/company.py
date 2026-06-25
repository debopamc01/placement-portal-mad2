from __future__ import annotations

from sqlalchemy.orm import Mapped, relationship, mapped_column
from typing import TYPE_CHECKING, Optional

from backend_app.extensions import db
from backend_app.models.model_enums import CompanyApprovalStatus

if TYPE_CHECKING:
    from backend_app.models.placement_drive import PlacementDrive
    from backend_app.models.user import User


class Company(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    name: Mapped[str] = mapped_column(nullable=False)
    hr_contact: Mapped[Optional[str]] = mapped_column(nullable=True)
    website: Mapped[Optional[str]] = mapped_column(nullable=True)
    approval_status: Mapped[CompanyApprovalStatus] = mapped_column(
        type_=db.Enum(CompanyApprovalStatus),
        default=CompanyApprovalStatus.PENDING,
        nullable=False,
    )
    placement_drives: Mapped[list[PlacementDrive]] = relationship(
        "PlacementDrive", back_populates="company", cascade="all, delete-orphan"
    )
    user: Mapped[User] = relationship(
        "User",
        back_populates="company",
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "email": self.user.email,
            "name": self.name,
            "hr_contact": self.hr_contact,
            "website": self.website,
            "approval_status": self.approval_status.value,
            "placement_drive_ids": [drive.id for drive in self.placement_drives],
        }
