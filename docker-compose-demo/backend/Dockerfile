FROM python:3.11-slim

WORKDIR /app

# Instalacija potrebnih paketa
RUN pip install flask psycopg2-binary flask-cors

COPY app.py .
COPY wait_for_db.py .

CMD ["python", "wait_for_db.py"]

