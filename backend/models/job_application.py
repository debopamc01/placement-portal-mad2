from backend.extensions import db
from backend.models.model_enums import JobApplicationStatus


class JobApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)
    placement_drive_id = db.Column(
        db.Integer,
        db.ForeignKey("placement_drive.id", ondelete="CASCADE"),
        nullable=False,
    )
    application_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(
        db.Enum(JobApplicationStatus),
        default=JobApplicationStatus.APPLIED,
        nullable=False,
    )
