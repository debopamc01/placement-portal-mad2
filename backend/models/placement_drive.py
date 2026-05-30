from backend.extensions import db
from backend.models.model_enums import PlacementDriveStatus


class PlacementDrive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(
        db.Integer, db.ForeignKey("company.id", ondelete="CASCADE"), nullable=False
    )
    status = db.Column(
        db.Enum(PlacementDriveStatus),
        default=PlacementDriveStatus.PENDING,
        nullable=False,
    )
    job_title = db.Column(db.String(100), nullable=False)
    job_description = db.Column(db.Text, nullable=True)
    eligibility_criteria = db.Column(db.Text, nullable=True)
    application_deadline = db.Column(db.DateTime, nullable=True)
    applications = db.relationship(
        "JobApplication", backref="placement_drive", cascade="all, delete-orphan"
    )
