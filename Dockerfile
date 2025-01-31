FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "-c", "gunicorn --log-level $LOG_LEVEL --workers 1 --bind 0.0.0.0:5000 api.app:app"]