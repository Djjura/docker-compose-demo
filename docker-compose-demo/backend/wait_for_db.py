import time
import psycopg2
import os
import subprocess

# Čekaj dok baza ne bude spremna
db_ready = False


print(" WAIT_FOR_DB SCRIPT STARTED", flush=True)

print("Attempting to connect to DB:", os.environ["DB_HOST"], os.environ["DB_NAME"],flush=True)

while not db_ready:
    try:
        conn = psycopg2.connect(
            host=os.environ["DB_HOST"],
            database=os.environ["DB_NAME"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASS"]
        )
        conn.close()
        db_ready = True
        print("PostgreSQL is ready!",flush=True)
    except psycopg2.OperationalError:
        print("Waiting for PostgreSQL...",flush=True)
        time.sleep(1)

# Pokreni backend aplikaciju
subprocess.run(["python", "app.py"])
