from backend.extensions import db
from backend.models.model_enums import CompanyApprovalStatus


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    name = db.Column(db.String(100), nullable=False)
    # hr_contact = db.Column(db.String(100), nullable=True)
    website = db.Column(db.String(200), nullable=True)
    approval_status = db.Column(
        db.Enum(CompanyApprovalStatus),
        default=CompanyApprovalStatus.PENDING,
        nullable=False,
    )
    placement_drives = db.relationship(
        "PlacementDrive", backref="company", cascade="all, delete-orphan"
    )
