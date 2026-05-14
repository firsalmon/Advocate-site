FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libjpeg-dev \
    zlib1g-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV SECRET_KEY=dummy-build-key-not-for-prod
RUN python manage.py collectstatic --noinput

RUN useradd -r -s /bin/bash appuser \
    && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000