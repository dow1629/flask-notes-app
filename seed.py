from app import create_app
from app.extensions import db
from app.models import Category, Note


app = create_app()


with app.app_context():
    if Category.query.count() == 0:
        work = Category(name="Work")
        personal = Category(name="Personal")
        ideas = Category(name="Ideas")

        db.session.add_all([work, personal, ideas])
        db.session.commit()

        note1 = Note(
            name="Daniel",
            message="Finish the REST API assignment",
            category_id=work.id
        )

        note2 = Note(
            name="Daniel",
            message="Buy groceries",
            category_id=personal.id
        )

        note3 = Note(
            name="Daniel",
            message="Build another Flask project",
            category_id=ideas.id
        )

        db.session.add_all([note1, note2, note3])
        db.session.commit()

        print("Seed data added successfully.")

    else:
        print("Seed data already exists.")