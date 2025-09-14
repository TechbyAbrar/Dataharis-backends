FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    netcat-openbsd \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the application
COPY . .

# Entrypoint for safe startup
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Run using entrypoint
ENTRYPOINT ["/entrypoint.sh"]

CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8001", "--workers", "4", "--threads", "2", "--timeout", "120"]
