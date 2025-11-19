from extensions.db import db
from extensions.bcrypt import bcrypt
import uuid
from slugify import slugify

class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(200), unique=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="patient")
    is_active = db.Column(db.Boolean, default=True)

    
    profile = db.relationship("PatientProfile", back_populates="user", uselist=False)
    admin_profile = db.relationship("AdminProfile", back_populates="user", uselist=False)

    def __init__(self, email, password, role="patient"):
        self.email = email
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
        self.role = role
        self.slug = slugify(email) + "-" + uuid.uuid4().hex[:6]
