# Juhi — VPS Deployment and Operations Guide

**Document type:** Deployment and Operations Specification  
**Product:** Juhi AI Companion  
**Target Environment:** Virtual Private Server (VPS) with Docker Compose  
**Reverse Proxy / TLS:** Caddy (automated Let's Encrypt TLS) or Nginx  
**Version:** 1.0  
**Prepared:** 17 October 2026  

---

## 1. Overview & Architecture

Juhi uses a **modular monolith** backend built with FastAPI, PostgreSQL (with optional `pgvector` extension) for persistent relational and semantic memory storage, and an asynchronous worker for background media and memory extraction.

For production VPS hosting, services are containerized via Docker and orchestrated with **Docker Compose**.

```text
                  Internet (HTTPS :443 / HTTP :80)
                                 │
                                 ▼
                     ┌───────────────────────┐
                     │   Caddy Reverse Proxy │ (Automated TLS via Let's Encrypt)
                     └───────────┬───────────┘
                                 │
                     ┌───────────┴───────────┐
                     │   Internal Docker Net │
                     └───────────┬───────────┘
                                 │
           ┌─────────────────────┼─────────────────────┐
           ▼                     ▼                     ▼
┌────────────────────┐ ┌───────────────────┐ ┌────────────────────┐
│   FastAPI API      │ │ PostgreSQL 16     │ │ Async Worker       │
│  (services/api)    │ │   (+ pgvector)    │ │ (services/worker)  │
│ Port 8000 internal │ │ Port 5432 internal│ │ Worker process     │
└────────────────────┘ └───────────────────┘ └────────────────────┘
```

---

## 2. Server Prerequisites

A modern Linux VPS (Ubuntu 22.04 LTS or 24.04 LTS recommended):
- Minimum: 2 vCPU, 4GB RAM, 40GB SSD
- Recommended for production: 4 vCPU, 8GB RAM, 80GB NVMe SSD
- Docker Engine version 24+ and Docker Compose v2+ installed
- Domain name with DNS `A` records pointing to the VPS public IP

---

## 3. Directory Layout on VPS

```text
/opt/juhi/
├── .env.production          # Secret environment variables (chmod 600)
├── docker-compose.prod.yml  # Production Docker Compose definition
├── Caddyfile                # Web server & reverse proxy configuration
├── backups/                 # Automated PostgreSQL dumps
└── data/
    ├── postgres/            # Persistent PostgreSQL volume
    └── caddy/               # TLS certificates and Caddy data
```

---

## 4. Environment Variables Configuration

Copy `.env.production.example` to `/opt/juhi/.env.production` and configure:

```bash
# Server & App Environment
APP_ENV=production
DEBUG=false
SECRET_KEY=generate_with_openssl_rand_hex_32
API_BASE_URL=https://api.juhi.app
ALLOWED_ORIGINS=https://juhi.app,https://chat.juhi.app

# Database
POSTGRES_USER=juhi_admin
POSTGRES_PASSWORD=strong_random_db_password_here
POSTGRES_DB=juhi_prod
DATABASE_URL=postgresql+asyncpg://juhi_admin:strong_random_db_password_here@postgres:5432/juhi_prod

# Firebase Authentication (Verification only)
FIREBASE_PROJECT_ID=juhi-companion
FIREBASE_CREDENTIALS_JSON=

# AI Model Provider Credentials
AI_PROVIDER=mock # or anthropic / openai / venice
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
DEFAULT_MODEL=claude-3-5-sonnet-20241022

# Security & Rate Limiting
RATE_LIMIT_PER_MINUTE=60
```

---

## 5. Reverse Proxy Configuration (`Caddyfile`)

Caddy automatically handles HTTPS certificates through Let's Encrypt without manual certbot renewals:

```caddy
api.juhi.app {
    encode gzip zstd
    
    # Security Headers
    header {
        Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
        X-Content-Type-Options "nosniff"
        X-Frame-Options "DENY"
        Referrer-Policy "strict-origin-when-cross-origin"
    }

    # Proxy to FastAPI container
    reverse_proxy api:8000 {
        header_up Host {host}
        header_up X-Real-IP {remote_host}
        header_up X-Forwarded-For {remote_host}
        header_up X-Forwarded-Proto {scheme}
    }
}
```

---

## 6. Automated CI/CD Pipeline (GitHub Actions)

The deployment pipeline is triggered on release tag or push to the `main` branch:

1. **Continuous Integration (`ci.yml`)**:
   - Lints Python code with `ruff` and checks types with `mypy`.
   - Runs unit and integration test suite via `pytest`.
   - Analyzes Flutter code with `flutter analyze` and runs `flutter test`.
   - Builds Docker container images to verify buildability.

2. **Continuous Deployment (`deploy.yml`)**:
   - Triggers on push to `main` or tagged release.
   - Builds and tags the Docker image, pushing to GitHub Container Registry (GHCR) or Docker Hub.
   - Connects to the production VPS via SSH (using GitHub Secrets: `VPS_HOST`, `VPS_USER`, `VPS_SSH_KEY`).
   - Pulls the latest images and executes zero-downtime rolling restart:
     ```bash
     cd /opt/juhi
     docker compose -f docker-compose.prod.yml pull
     docker compose -f docker-compose.prod.yml up -d --remove-orphans
     docker compose -f docker-compose.prod.yml exec -T api alembic upgrade head
     ```

---

## 7. Database Migrations & Backups

### 7.1 Running Migrations
Alembic migrations run automatically on container startup or manually via:
```bash
docker compose -f docker-compose.prod.yml exec api alembic upgrade head
```

### 7.2 Automated Daily Backups
Add a cron job on the VPS (`crontab -e`):
```cron
0 2 * * * docker compose -f /opt/juhi/docker-compose.prod.yml exec -T postgres pg_dump -U juhi_admin juhi_prod | gzip > /opt/juhi/backups/juhi_prod_$(date +\%F_\%H\%M).sql.gz
30 2 * * * find /opt/juhi/backups -name "*.sql.gz" -mtime +14 -delete
```

---

## 8. Health Checks & Monitoring

- Health check endpoint: `GET https://api.juhi.app/api/v1/health`
  - Returns `{"status": "healthy", "database": "connected", "version": "1.0.0"}`
- Docker container health checks ensure automatic restart on process failure.
