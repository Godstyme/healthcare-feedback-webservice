from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions.db import db
from models.user import User
from models.patient_profile import PatientProfile
from datetime import date 

patient_bp = Blueprint("patient", __name__, url_prefix="/api/patient")


# ------------------------------
# GET PROFILE (for logged-in patient)
# ------------------------------
@patient_bp.get("/profile")
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()

    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    profile = user.profile
    if not profile:
        return jsonify({"message": "Profile not found"}), 404

    return jsonify({
        "user_id": user.user_id,
        "email": user.email,
        "role": user.role,
        "profile": {
            "fullname": profile.fullname,
            "hospital_id": profile.hospital_id,
            "internal_id": profile.internal_id,
            "phone": profile.phone,
            "date_of_birth": str(profile.date_of_birth) if profile.date_of_birth else None,
            "gender": profile.gender,
            "address": profile.address
        }
    }), 200


# ------------------------------
# UPDATE PROFILE
# ------------------------------
@patient_bp.put("/profile")
@jwt_required()
def update_profile():
    # user_id = get_jwt_identity()
    user_id = int(get_jwt_identity())

    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    profile = user.profile
    if not profile:
        return jsonify({"message": "Profile not found"}), 404

    data = request.get_json()

    profile.fullname = data.get("fullname", profile.fullname)
    profile.phone = data.get("phone", profile.phone)
    profile.gender = data.get("gender", profile.gender)
    profile.address = data.get("address", profile.address)

    # Parse date if provided
    dob = data.get("date_of_birth")
    if dob:
        try:
            profile.date_of_birth = date.fromisoformat(dob)
        except:
            return jsonify({"message": "Invalid date format (expected YYYY-MM-DD)"}), 400

    db.session.commit()

    return jsonify({"message": "Profile updated successfully"}), 200
