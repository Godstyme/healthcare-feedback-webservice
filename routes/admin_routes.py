from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions.db import db
from models.user import User
from models.admin_profile import AdminProfile
from utils.decorators import admin_required
from datetime import datetime

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")


@admin_bp.post("/create")
@jwt_required()
@admin_required
def create_admin():
    data = request.json

    full_name = data.get("full_name")
    email = data.get("email")
    password = data.get("password")
    phone = data.get("phone")

    if not full_name or not email or not password:
        return jsonify({"message": "Full name, email, and password are required"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already exists"}), 409

  
    new_admin = User(email=email, password=password, role="admin")
    db.session.add(new_admin)
    db.session.flush()

    staff_id = f"STF-{new_admin.user_id:06d}"

    
    admin_profile = AdminProfile(
        admin_id=new_admin.user_id,
        full_name=full_name,
        staff_id=staff_id,
        phone=phone,
    )

    db.session.add(admin_profile)
    db.session.commit()

    return jsonify({
        "message": "Admin created successfully",
        "staff_id": staff_id,
        "slug": new_admin.slug
    }), 201


@admin_bp.get("/profile")
@jwt_required()
@admin_required
def get_admin_profile():
    admin_id = get_jwt_identity()

    user = User.query.get(admin_id)
    
    if not user:
        return jsonify({"message": "Admin not found"}), 404

    profile = user.admin_profile
    if not profile:
        return jsonify({"message": "Profile incomplete"}), 404

    return jsonify({
        "user_id": user.user_id,
        "email": user.email,
        "role": user.role,
        "profile": {
            "full_name": profile.full_name,
            "staff_id": profile.staff_id,
            "phone": profile.phone,
            "created_at": str(profile.created_at)
        }
    }), 200

@admin_bp.put("/profile")
@jwt_required()
@admin_required
def update_admin_profile():
    admin_id = get_jwt_identity()

    user = User.query.get(admin_id)
    if not user:
        return jsonify({"message": "Admin not found"}), 404

    profile = user.admin_profile
    if not profile:
        return jsonify({"message": "Profile incomplete"}), 404

    data = request.get_json()

    profile.full_name = data.get("full_name", profile.full_name)
    profile.phone = data.get("phone", profile.phone)

    db.session.commit()

    return jsonify({"message": "Profile updated successfully"}), 201