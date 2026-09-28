from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required

from .extensions import db
from .models import Category, Note
from .integrations import send_note_webhook


notes_bp = Blueprint("notes", __name__, url_prefix="/api")


def note_to_dict(note):
    return {
        "id": note.id,
        "name": note.name,
        "message": note.message,
        "created_at": note.created_at.isoformat(),
        "category_id": note.category_id,
        "category": note.category.name
    }


@notes_bp.route("/notes", methods=["GET"])
def get_notes():
    notes = Note.query.order_by(Note.created_at.desc()).all()

    return jsonify({
        "notes": [note_to_dict(note) for note in notes]
    }), 200


@notes_bp.route("/notes/<int:id>", methods=["GET"])
def get_note(id):
    note = db.session.get(Note, id)

    if note is None:
        return jsonify({"error": "Note not found."}), 404

    return jsonify(note_to_dict(note)), 200


@notes_bp.route("/notes", methods=["POST"])
@login_required
def create_note():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Request body must contain valid JSON."
        }), 400

    name = data.get("name")
    message = data.get("message")
    category_id = data.get("category_id")

    if not isinstance(name, str) or not name.strip():
        return jsonify({
            "error": "Name is required and cannot be empty."
        }), 400

    if not isinstance(message, str) or not message.strip():
        return jsonify({
            "error": "Message is required and cannot be empty."
        }), 400

    if not isinstance(category_id, int):
        return jsonify({
            "error": "A valid category_id is required."
        }), 400

    category = db.session.get(Category, category_id)

    if category is None:
        return jsonify({"error": "Category not found."}), 400

    note = Note(
        name=name.strip(),
        message=message.strip(),
        category_id=category_id,
        user_id=current_user.id
    )

    db.session.add(note)
    db.session.commit()

    send_note_webhook(note)

    return jsonify(note_to_dict(note)), 201


@notes_bp.route("/notes/<int:id>", methods=["PUT"])
@login_required
def update_note(id):
    note = db.session.get(Note, id)

    if note is None:
        return jsonify({"error": "Note not found."}), 404

    if note.user_id != current_user.id:
        return jsonify({"error": "Forbidden."}), 403

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Request body must contain valid JSON."
        }), 400

    name = data.get("name")
    message = data.get("message")
    category_id = data.get("category_id")

    if not isinstance(name, str) or not name.strip():
        return jsonify({
            "error": "Name is required and cannot be empty."
        }), 400

    if not isinstance(message, str) or not message.strip():
        return jsonify({
            "error": "Message is required and cannot be empty."
        }), 400

    if not isinstance(category_id, int):
        return jsonify({
            "error": "A valid category_id is required."
        }), 400

    category = db.session.get(Category, category_id)

    if category is None:
        return jsonify({"error": "Category not found."}), 400

    note.name = name.strip()
    note.message = message.strip()
    note.category_id = category_id

    db.session.commit()

    return jsonify(note_to_dict(note)), 200


@notes_bp.route("/notes/<int:id>", methods=["DELETE"])
@login_required
def delete_note(id):
    note = db.session.get(Note, id)

    if note is None:
        return jsonify({"error": "Note not found."}), 404

    if note.user_id != current_user.id:
        return jsonify({"error": "Forbidden."}), 403

    db.session.delete(note)
    db.session.commit()

    return jsonify({
        "message": "Note deleted successfully."
    }), 200