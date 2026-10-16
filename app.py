import os
from flask import Flask, jsonify
from dotenv import load_dotenv
import psycopg2
from prometheus_flask_exporter import PrometheusMetrics
from urllib.parse import quote

load_dotenv()

app = Flask(__name__)
metrics = PrometheusMetrics(app)

@app.route("/")
def home():
    return "Hello from DevOps demo app"

@app.route("/health")
def health():
    database_ok = database_check()
    status = "ok" if database_ok else "error"

    return jsonify({
        "status": status,
        "environment": os.getenv("APP_ENV", "unknown"),
        "database": "up" if database_ok else "down"
    }), 200 if database_ok else 503

def get_db_connection():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        user = os.getenv("POSTGRES_USER", "devops")
        password = quote(os.environ["POSTGRES_PASSWORD"], safe="")
        host = os.getenv("POSTGRES_HOST", "postgres")
        database = os.getenv("POSTGRES_DB", "demoapp")

        database_url = f"postgresql://{user}:{password}@{host}:5432/{database}"

    return psycopg2.connect(database_url)

@app.route("/messages")
def messages():
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT id, text FROM messages;")
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(rows)

def database_check():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT 1;")
        cursor.fetchone()

        cursor.close()
        connection.close()

        return True

    except Exception:
        return False

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    