from extensions.db import db
import sqlalchemy as sa
from datetime import datetime

class AdminProfile(db.Model):
    __tablename__ = "admin_profile"

    admin_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), primary_key=True)

    full_name = db.Column(db.String(150), nullable=False)
    staff_id = db.Column(db.String(50), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", back_populates="admin_profile", uselist=False)
