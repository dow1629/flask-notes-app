from flask import Blueprint, jsonify, request
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from .extensions import db
from .models import User


auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Request body must contain valid JSON."
        }), 400

    email = data.get("email")
    password = data.get("password")

    if not isinstance(email, str) or not email.strip():
        return jsonify({"error": "Email is required."}), 400

    if not isinstance(password, str) or not password:
        return jsonify({"error": "Password is required."}), 400

    email = email.strip().lower()

    existing_user = User.query.filter_by(email=email).first()

    if existing_user is not None:
        return jsonify({"error": "User already exists."}), 400

    user = User(
        email=email,
        password_hash=generate_password_hash(password)
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "Registration successful.",
        "user_id": user.id,
        "email": user.email
    }), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Request body must contain valid JSON."
        }), 400

    email = data.get("email")
    password = data.get("password")

    if not isinstance(email, str) or not isinstance(password, str):
        return jsonify({"error": "Invalid credentials."}), 401

    email = email.strip().lower()

    user = User.query.filter_by(email=email).first()

    if user is None or not check_password_hash(
        user.password_hash,
        password
    ):
        return jsonify({"error": "Invalid credentials."}), 401

    login_user(user)

    return jsonify({
        "message": "Login successful.",
        "user_id": user.id,
        "email": user.email
    }), 200


@auth_bp.route("/logout", methods=["POST"])
def logout():
    logout_user()

    return jsonify({
        "message": "Logout successful."
    }), 200