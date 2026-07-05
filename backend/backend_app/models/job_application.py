from __future__ import annotations
from typing import TYPE_CHECKING
from zoneinfo import ZoneInfo

from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from backend_app.extensions import db
from backend_app.models.model_enums import JobApplicationStatus

if TYPE_CHECKING:
    from backend_app.models.student import Student
    from backend_app.models.placement_drive import PlacementDrive


class JobApplication(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(db.ForeignKey("student.id"), nullable=False)
    placement_drive_id: Mapped[int] = mapped_column(
        db.ForeignKey("placement_drive.id", ondelete="CASCADE"),
        nullable=False,
    )
    application_date: Mapped[datetime] = mapped_column(nullable=False)
    status: Mapped[JobApplicationStatus] = mapped_column(
        type_=db.Enum(JobApplicationStatus),
        default=JobApplicationStatus.APPLIED,
        nullable=False,
    )
    student: Mapped[Student] = relationship("Student", back_populates="applications")
    placement_drive: Mapped[PlacementDrive] = relationship(
        "PlacementDrive", back_populates="applications"
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "student": self.student.to_dict() if self.student else None,
            "placement_drive_id": self.placement_drive_id,
            "application_date": (
                self.application_date.astimezone(
                    tz=ZoneInfo("Asia/Kolkata")
                ).isoformat()
                if self.application_date
                else None
            ),
            "status": self.status.value,
        }
