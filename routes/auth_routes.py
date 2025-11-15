from flask import Blueprint, request, jsonify
from models.user import User
from models.patient_profile import PatientProfile
from extensions.db import db
from extensions.bcrypt import bcrypt
from flask_jwt_extended import create_access_token
from extensions.jwt import jwt
from flask_jwt_extended import create_access_token

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

@auth_bp.post("/register")
def register():
    data = request.json

    email = data.get("email")
    password = data.get("password")
    fullname = data.get("fullname")
    phone = data.get("phone")

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already exists"}), 409

    user = User(email=email, password=password, role="patient")
    db.session.add(user)
    db.session.commit()

    profile = PatientProfile(
        patient_id=user.user_id,
        fullname=fullname,
        phone=phone
    )

    db.session.add(profile)
    db.session.flush()  

    profile.hospital_id = f"HSP-{profile.internal_id:06d}"
    db.session.commit()

    return jsonify({
        "message": "Registration successful",
        "slug": user.slug,
        "hospital_id": profile.hospital_id
    }), 201

@auth_bp.post("/login")
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": "Invalid email or password"}), 401

   
    if not bcrypt.check_password_hash(user.password_hash, password):
        return jsonify({"message": "Invalid email or password"}), 401

    
    access_token = create_access_token(identity=user.user_id)

    return jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "user": {
            "user_id": user.user_id,
            "email": user.email,
            "role": user.role,
            "slug": user.slug
        }
    }), 200