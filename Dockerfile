FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "-c", "gunicorn --log-level $LOG_LEVEL --workers 1 --bind $FLASK_HOST:$FLASK_PORT \"main:initialize_application()\""]