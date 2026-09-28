import sqlite3

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def get_db():
    connection = sqlite3.connect("data.db")
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = get_db()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()
projects = [
    {
        "name": "portfolio",
        "title": "Personal Portfolio",
        "description": "A personal portfolio website built with Flask.",
        "year": 2026
    },
    {
        "name": "blog",
        "title": "My Blog",
        "description": "A simple blog application using Flask and Jinja.",
        "year": 2026
    },
    {
        "name": "weather",
        "title": "Weather App",
        "description": "A small application that displays weather information.",
        "year": 2025
    }
]


@app.route("/")
def home():
    connection = get_db()

    entries = connection.execute(
        "SELECT * FROM entries ORDER BY created_at DESC"
    ).fetchall()

    connection.close()

    return render_template("home.html", entries=entries)


@app.route("/add", methods=["POST"])
def add_entry():
    name = request.form["name"].strip()
    message = request.form["message"].strip()

    if not name or not message:
        return "Name and message are required.", 400

    connection = get_db()

    connection.execute(
        "INSERT INTO entries (name, message) VALUES (?, ?)",
        (name, message)
    )

    connection.commit()
    connection.close()

    return redirect(url_for("home"))


@app.route("/delete/<int:id>", methods=["POST"])
def delete_entry(id):
    connection = get_db()

    connection.execute(
        "DELETE FROM entries WHERE id = ?",
        (id,)
    )

    connection.commit()
    connection.close()

    return redirect(url_for("home"))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/projects")
def projects_page():
    return render_template("projects.html", projects=projects)


@app.route("/projects/<name>")
def project_detail(name):

    for project in projects:
        if project["name"] == name:
            return render_template(
                "project_detail.html",
                project=project
            )

    return "Project not found", 404
if __name__ == "__main__":
    init_db()
    app.run(debug=True)