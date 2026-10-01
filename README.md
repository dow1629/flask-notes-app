# Flask Notes App

A full-stack notes application built with Flask, SQLAlchemy, JavaScript, HTML and CSS.

## Live Application

https://flask-notes-app-nrd9.onrender.com/

## GitHub Repository

https://github.com/dow1629/flask-notes-app

## Features

- REST API for managing notes
- User authentication with password hashing
- User-owned notes and authorization
- Create, view and delete notes without a full page reload
- SQLAlchemy database models
- Flask-Migrate database migrations
- SQLite for local development
- PostgreSQL for production
- External webhook integration
- Automated testing with pytest
- Gunicorn production WSGI server
- Docker containerisation
- Environment-based configuration
- Deployment on Render

## Local Setup

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file using `.env.example` as a guide.

Run the database migrations:

```bash
flask --app "app:create_app()" db upgrade
```

Seed the database:

```bash
python seed.py
```

Start the development server:

```bash
python run.py
```

The local application runs at:

```text
http://127.0.0.1:5001
```

## Gunicorn

The application can also be served locally using Gunicorn:

```bash
gunicorn --bind 127.0.0.1:5001 "app:create_app()"
```

## Docker

Build the Docker image:

```bash
docker build -t flask-notes-app .
```

The production Docker container runs database migrations, seeds the required initial data, and then starts the application using Gunicorn.

## Testing

Run the automated test suite with:

```bash
python3 -m pytest
```

## Production Deployment

The application is deployed on Render as a Docker-based web service and uses a managed PostgreSQL database.

Production configuration is supplied through environment variables:

```text
FLASK_ENV
SECRET_KEY
DATABASE_URL
WEBHOOK_URL
```

Sensitive values are not committed to GitHub.

The deployment flow is:

```text
GitHub
   ↓
Render
  