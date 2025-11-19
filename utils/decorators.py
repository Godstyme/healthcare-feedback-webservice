from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from models.user import User

def admin_required(fn):
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user or user.role != "admin":
            return jsonify({"message": "Admins only"}), 403

        return fn(*args, **kwargs)
    wrapper.__name__ = fn.__name__
    return wrapper
