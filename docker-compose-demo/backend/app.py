from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Backend service is running via Docker Compose!"

@app.route("/db")
def db_test():
    conn = psycopg2.connect(
        host=os.environ["DB_HOST"],
        database=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASS"]
    )
    cur = conn.cursor()
    cur.execute("SELECT version();")
    version = cur.fetchone()
    cur.close()
    conn.close()
    return f"Connected to: {version}"

@app.route("/users", methods=["GET"])
def get_users():
    conn = psycopg2.connect(
        host=os.environ["DB_HOST"],
        database=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASS"]
    )
    cur = conn.cursor()

    cur.execute("""
        SELECT id, first_name, last_name, age, date_of_birth
        FROM users
    """)

    rows = cur.fetchall()

    users = []
    for row in rows:
        users.append({
            "id": row[0],
            "first_name": row[1],
            "last_name": row[2],
            "age": row[3],
            "date_of_birth": row[4].isoformat()
        })

    cur.close()
    conn.close()

    return jsonify(users)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
