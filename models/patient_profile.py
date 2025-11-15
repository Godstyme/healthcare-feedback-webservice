from extensions.db import db
import sqlalchemy as sa

class PatientProfile(db.Model):
    __tablename__ = "patient_profile"

    patient_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), primary_key=True)

    internal_id = db.Column(
        db.Integer,
        sa.Identity(start=1, increment=1),
        unique=True,
        nullable=False
    )

    hospital_id = db.Column(db.String(50), unique=True)
    fullname = db.Column(db.String(150))
    phone = db.Column(db.String(20))
    date_of_birth = db.Column(db.Date())
    gender = db.Column(db.String(10))
    address = db.Column(db.Text())

    # One-to-one back reference
    user = db.relationship("User", back_populates="profile")
