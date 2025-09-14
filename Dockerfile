# Dockerfile
FROM python:3.11-slim

# set working dir
WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y \
    libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Ensure staticfiles & media are writable
RUN mkdir -p /app/staticfiles /app/media \
    && chown -R 1000:1000 /app/staticfiles /app/media

# Run as non-root user (optional, good practice)
USER 1000

CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8001", "--workers", "2", "--threads", "2"]
