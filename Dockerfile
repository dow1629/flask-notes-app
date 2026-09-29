FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 10000

CMD ["sh", "-c", "flask --app 'app:create_app()' db upgrade && python seed.py && gunicorn --bind 0.0.0.0:${PORT:-10000} 'app:create_app()'"]