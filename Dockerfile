FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    apt-get update && apt-get install -y --no-install-recommends gcc

COPY . .

ENV FLASK_APP=main.py
ENV FLASK_ENV=production
ENV FLASK_DEBUG=0
ENV FLASK_HOST=0.0.0.0
ENV FLASK_PORT=5000
ENV FLASK_WORKERS=4
ENV LOG_LEVEL=INFO
ENV DATABASE_PATH=/data

CMD ["sh", "-c", "gunicorn --log-level $LOG_LEVEL --workers $FLASK_WORKERS --bind $FLASK_HOST:$FLASK_PORT main:app"]