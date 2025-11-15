from flask import Blueprint, jsonify
from models.user import User
from models.patient_profile import PatientProfile
from extensions.db import db

user_bp = Blueprint("users", __name__, url_prefix="/api/users")


@user_bp.get("/")
def get_all_users():
    users = User.query.all()

    output = []

    for user in users:
        user_data = {
            "user_id": user.user_id,
            "email": user.email,
            "role": user.role,
            "slug": user.slug,
            "is_active": user.is_active,
        }

        # Add patient profile if user is a patient
        if user.role == "patient" and user.patient_profile:
            user_data["profile"] = {
                "fullname": user.patient_profile.fullname,
                "hospital_id": user.patient_profile.hospital_id,
                "phone": user.patient_profile.phone,
            }

        output.append(user_data)

    return jsonify({"users": output}), 200
