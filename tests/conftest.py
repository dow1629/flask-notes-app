import pytest

from app import create_app
from app.extensions import db
from app.models import Category


@pytest.fixture
def app():
    app = create_app({
    "TESTING": True,
    "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    "SECRET_KEY": "test-secret-key"
})

    with app.app_context():
        db.drop_all()
        db.create_all()

        work = Category(name="Work")
        personal = Category(name="Personal")

        db.session.add_all([work, personal])
        db.session.commit()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()