# Multi-stage production Dockerfile for Juhi Background Worker
FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY services/api/requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Final Runner
FROM python:3.11-slim AS runner

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /install /usr/local

RUN addgroup --system juhi && adduser --system --group juhi

COPY services/api /app/services/api
COPY services/worker /app/services/worker

ENV PYTHONPATH="/app/services/api:/app/services/worker"

RUN chown -R juhi:juhi /app
USER juhi

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1

CMD ["uvicorn", "services.worker.app.main:app", "--host", "0.0.0.0", "--port", "8080"]
