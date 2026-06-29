# Étape 1 : Construction des dépendances
FROM python:3.11-slim as builder

WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY app/requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Étape 2 : Image d'exécution finale
FROM python:3.11-slim

# Installation de libpq pour PostgreSQL
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copie des packages Python installés depuis le builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Copie du code applicatif
COPY app/ /app/app/
COPY tests/ /app/tests/
COPY init_db.py /app/
COPY .env.example /app/.env

# Port d'écoute interne de Flask/Gunicorn dans le conteneur
EXPOSE 80

# Lancement de l'application via Gunicorn sur le port 80
CMD ["gunicorn", "--bind", "0.0.0.0:80", "--workers", "4", "app.app:app"]
