from backend.extensions import db


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    name = db.Column(db.String(100), nullable=False)
    resume_url = db.Column(db.String(200), nullable=True)
    # ids of the applications that the student has applied to, stored as a comma-separated string
    # application_ids = db.Column(db.String(200), nullable=True)
    description = db.Column(db.Text, nullable=True)
    blacklisted = db.Column(db.Boolean, default=False, nullable=False)
    applications = db.relationship(
        "JobApplication", backref="student", cascade="all, delete-orphan"
    )
