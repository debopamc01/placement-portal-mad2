from __future__ import annotations

from sqlalchemy.orm import Mapped, relationship, mapped_column
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional

from backend_app.extensions import db
from backend_app.models.model_enums import PlacementDriveStatus

if TYPE_CHECKING:
    from backend_app.models.company import Company
    from backend_app.models.job_application import JobApplication


class PlacementDrive(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(
        db.ForeignKey("company.id", ondelete="CASCADE"), nullable=False
    )
    status: Mapped[PlacementDriveStatus] = mapped_column(
        type_=db.Enum(PlacementDriveStatus),
        default=PlacementDriveStatus.PENDING,
        nullable=False,
    )
    job_title: Mapped[str] = mapped_column(nullable=False)
    job_description: Mapped[Optional[str]] = mapped_column(nullable=True)
    eligibility_criteria: Mapped[Optional[str]] = mapped_column(nullable=True)
    application_deadline: Mapped[Optional[str]] = mapped_column(nullable=True)
    applications: Mapped[list[JobApplication]] = relationship(
        "JobApplication", back_populates="placement_drive", cascade="all, delete-orphan"
    )
    company: Mapped[Company] = relationship(
        "Company", back_populates="placement_drives"
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "status": self.status.value,
            "job_title": self.job_title,
            "job_description": self.job_description,
            "eligibility_criteria": self.eligibility_criteria,
            "application_deadline": (
                datetime.fromisoformat(self.application_deadline).astimezone(
                    timezone.utc
                )
                if self.application_deadline
                else None
            ),
            "application_ids": [application.id for application in self.applications],
            "company": self.company.to_dict(),
        }
