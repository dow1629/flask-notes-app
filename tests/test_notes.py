from datetime import datetime

from app.models import Category, Note
from app.notes import note_to_dict

def test_get_notes_empty(client):
    response = client.get("/api/notes")

    assert response.status_code == 200
    assert response.get_json() == {"notes": []}

def test_register_user(client):
    response = client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "password": "password123"
        }
    )

    data = response.get_json()

    assert response.status_code == 201
    assert data["message"] == "Registration successful."
    assert data["email"] == "test@example.com"

def test_login_user(client):
    client.post(
        "/api/auth/register",
        json={
            "email": "login@example.com",
            "password": "password123"
        }
    )

    response = client.post(
        "/api/auth/login",
        json={
            "email": "login@example.com",
            "password": "password123"
        }
    )

    data = response.get_json()

    assert response.status_code == 200
    assert data["message"] == "Login successful."
    assert data["email"] == "login@example.com"

def test_create_note_requires_login(client):
    response = client.post(
        "/api/notes",
        json={
            "name": "Daniel",
            "message": "This should be blocked",
            "category_id": 1
        }
    )

    data = response.get_json()

    assert response.status_code == 401
    assert data["error"] == "Unauthorized."

def test_logged_in_user_can_create_note(client):
    client.post(
        "/api/auth/register",
        json={
            "email": "owner@example.com",
            "password": "password123"
        }
    )

    client.post(
        "/api/auth/login",
        json={
            "email": "owner@example.com",
            "password": "password123"
        }
    )

    response = client.post(
        "/api/notes",
        json={
            "name": "Daniel",
            "message": "Created from pytest",
            "category_id": 1
        }
    )

    data = response.get_json()

    assert response.status_code == 201
    assert data["message"] == "Created from pytest"
    assert data["category"] == "Work"

def test_create_note_bad_input_returns_400(client):
    client.post(
        "/api/auth/register",
        json={
            "email": "badinput@example.com",
            "password": "password123"
        }
    )

    client.post(
        "/api/auth/login",
        json={
            "email": "badinput@example.com",
            "password": "password123"
        }
    )

    response = client.post(
        "/api/notes",
        json={
            "name": "Daniel",
            "category_id": 1
        }
    )

    data = response.get_json()

    assert response.status_code == 400
    assert data["error"] == "Message is required and cannot be empty."

def test_missing_note_returns_404(client):
    response = client.get("/api/notes/999")

    data = response.get_json()

    assert response.status_code == 404
    assert data["error"] == "Note not found."

def test_user_cannot_edit_another_users_note(client):
    client.post(
        "/api/auth/register",
        json={
            "email": "owner@example.com",
            "password": "password123"
        }
    )

    client.post(
        "/api/auth/login",
        json={
            "email": "owner@example.com",
            "password": "password123"
        }
    )

    create_response = client.post(
        "/api/notes",
        json={
            "name": "Owner",
            "message": "Private note",
            "category_id": 1
        }
    )

    note_id = create_response.get_json()["id"]

    client.post("/api/auth/logout")

    client.post(
        "/api/auth/register",
        json={
            "email": "other@example.com",
            "password": "password123"
        }
    )

    client.post(
        "/api/auth/login",
        json={
            "email": "other@example.com",
            "password": "password123"
        }
    )

    response = client.put(
        f"/api/notes/{note_id}",
        json={
            "name": "Other User",
            "message": "Trying to edit it",
            "category_id": 1
        }
    )

    data = response.get_json()

    assert response.status_code == 403
    assert data["error"] == "Forbidden."

def test_note_crud_happy_path(client):
    # Register and log in
    client.post(
        "/api/auth/register",
        json={
            "email": "crud@example.com",
            "password": "password123"
        }
    )

    client.post(
        "/api/auth/login",
        json={
            "email": "crud@example.com",
            "password": "password123"
        }
    )

    # CREATE
    create_response = client.post(
        "/api/notes",
        json={
            "name": "Daniel",
            "message": "Original message",
            "category_id": 1
        }
    )

    assert create_response.status_code == 201

    note_id = create_response.get_json()["id"]

    # GET ONE
    get_response = client.get(f"/api/notes/{note_id}")

    assert get_response.status_code == 200
    assert get_response.get_json()["message"] == "Original message"

    # UPDATE
    update_response = client.put(
        f"/api/notes/{note_id}",
        json={
            "name": "Daniel Updated",
            "message": "Updated message",
            "category_id": 2
        }
    )

    assert update_response.status_code == 200
    assert update_response.get_json()["message"] == "Updated message"
    assert update_response.get_json()["category"] == "Personal"

    # DELETE
    delete_response = client.delete(f"/api/notes/{note_id}")

    assert delete_response.status_code == 200
    assert delete_response.get_json()["message"] == "Note deleted successfully."

    # Make sure it is actually gone
    missing_response = client.get(f"/api/notes/{note_id}")

    assert missing_response.status_code == 404

def test_delete_forbidden_for_other_user(client):
    client.post(
        "/api/auth/register",
        json={
            "email": "owner2@example.com",
            "password": "password123"
        }
    )

    client.post(
        "/api/auth/login",
        json={
            "email": "owner2@example.com",
            "password": "password123"
        }
    )

    create_response = client.post(
        "/api/notes",
        json={
            "name": "Owner",
            "message": "Do not delete",
            "category_id": 1
        }
    )

    note_id = create_response.get_json()["id"]

    client.post("/api/auth/logout")

    client.post(
        "/api/auth/register",
        json={
            "email": "other2@example.com",
            "password": "password123"
        }
    )

    client.post(
        "/api/auth/login",
        json={
            "email": "other2@example.com",
            "password": "password123"
        }
    )

    response = client.delete(f"/api/notes/{note_id}")

    data = response.get_json()

    assert response.status_code == 403
    assert data["error"] == "Forbidden."

def test_bad_login_returns_401(client):
    client.post(
        "/api/auth/register",
        json={
            "email": "wrongpass@example.com",
            "password": "password123"
        }
    )

    response = client.post(
        "/api/auth/login",
        json={
            "email": "wrongpass@example.com",
            "password": "wrongpassword"
        }
    )

    data = response.get_json()

    assert response.status_code == 401
    assert data["error"] == "Invalid credentials."

def test_note_to_dict_unit(app):
    with app.app_context():
        category = Category(
            id=1,
            name="Work"
        )

        note = Note(
            id=10,
            name="Daniel",
            message="Unit test note",
            created_at=datetime(2026, 9, 10, 12, 0, 0),
            category_id=1
        )

        note.category = category

        result = note_to_dict(note)

        assert result == {
            "id": 10,
            "name": "Daniel",
            "message": "Unit test note",
            "created_at": "2026-09-10T12:00:00",
            "category_id": 1,
            "category": "Work"
        }