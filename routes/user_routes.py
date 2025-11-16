from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from models.user import User

user_bp = Blueprint("users", __name__, url_prefix="/api/users")


@user_bp.get("/")
@jwt_required()   
def get_all_users():
    users = User.query.all()

    if not users:
        return jsonify({
            "message": "No users found",
            "users": []
        }), 404

    output = []

    for user in users:
        profile = user.profile   

        user_data = {
            "user_id": user.user_id,
            "email": user.email,
            "role": user.role,
            "slug": user.slug,
            "is_active": user.is_active,
        }

        if profile:
            user_data["profile"] = {
                "fullname": profile.fullname,
                "hospital_id": profile.hospital_id,
                "internal_id": profile.internal_id,
                "phone": profile.phone,
            }

        output.append(user_data)

    return jsonify({"users": output}), 200
