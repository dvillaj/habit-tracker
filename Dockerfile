FROM python:3.12-slim

WORKDIR /app

# Instalar dependencias necesarias
RUN apt-get update && apt-get install -y --no-install-recommends gosu && \
    rm -rf /var/lib/apt/lists/*

COPY Pipfile* ./
RUN pip install --no-cache-dir pipenv && \
    pipenv install && \
    pipenv requirements > requirements.txt && \
    pipenv --rm && \
    pip install -r requirements.txt

COPY . .

# Copiar el script de entrada y dar permisos
RUN mv /app/entrypoint.sh /entrypoint.sh && \
    chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

CMD ["sh", "-c", "gunicorn --log-level $LOG_LEVEL --workers $FLASK_WORKERS --bind $FLASK_HOST:$FLASK_PORT \"main:initialize_application()\""]