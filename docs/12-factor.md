# 12-Factor App Compliance

Django Keel strictly adheres to the [12-Factor App](https://12factor.net/) methodology. This document details how each factor is implemented.

## I. Codebase

**One codebase tracked in revision control, many deploys**

✅ **Implementation:**
- Single Git repository
- Multiple deployment environments (dev, staging, production) from same codebase
- Environment-specific configuration via environment variables

## II. Dependencies

**Explicitly declare and isolate dependencies**

✅ **Implementation:**
- All dependencies declared in `pyproject.toml`
- Version pinning with `>=` for security updates
- Isolated virtual environments (uv/poetry)
- No system-wide packages assumed
- Lock files (`uv.lock` or `poetry.lock`) for reproducibility

**Example:**
```toml
dependencies = [
    "django>=5.2,<5.3",
    "psycopg[binary]>=3.2.0",
    "gunicorn>=22.0.0",
]
```

## III. Config

**Store config in the environment**

✅ **Implementation:**
- All configuration via environment variables
- No secrets in code
- `django-environ` for structured config
- `.env.example` for documentation
- Different configs per environment without code changes

**Example:**
```python
import environ

env = environ.Env()
SECRET_KEY = env("DJANGO_SECRET_KEY")
DATABASE_URL = env.db("DATABASE_URL")
DEBUG = env.bool("DEBUG", default=False)
```

## IV. Backing Services

**Treat backing services as attached resources**

✅ **Implementation:**
- All backing services accessed via URLs
- Database: `DATABASE_URL`
- Redis: `REDIS_URL`
- Celery: `CELERY_BROKER_URL`
- Object Storage: AWS/GCS/Azure URLs
- Services swappable without code changes
- Local and remote services treated identically

**Example:**
```bash
DATABASE_URL=postgres://localhost/mydb        # Local
DATABASE_URL=postgres://prod.db.com/mydb      # Remote
# Same connection code, different environment
```

## V. Build, Release, Run

**Strictly separate build and run stages**

✅ **Implementation:**

### Build Stage
- Creates deployment artifact
- Installs dependencies
- Compiles assets
- Creates Docker image

### Release Stage
- Combines build with config
- Runs database migrations
- Collects static files
- Executed via `release.sh`

### Run Stage
- Executes the application
- Uses `Procfile` for process types
- No code/config changes at runtime

**Build command:**
```bash
docker build -t myapp:v123 .
```

**Release command:**
```bash
./release.sh  # Migrations, collectstatic
```

**Run command:**
```bash
gunicorn config.wsgi:application
```

## VI. Processes

**Execute the app as stateless processes**

✅ **Implementation:**
- All processes are stateless
- No sticky sessions
- Session data in Redis/database, not memory
- File uploads go to object storage
- Ephemeral filesystem
- Process memory is transient

**Stateless process example:**
```python
# ❌ BAD: In-memory session
sessions = {}

# ✅ GOOD: Database/Redis session
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
```

## VII. Port Binding

**Export services via port binding**

✅ **Implementation:**
- Self-contained web server (Gunicorn/Daphne)
- No external web server in container
- Port configurable via `$PORT` environment variable
- Standalone HTTP services

**Example:**
```python
# Procfile
web: gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
```

## VIII. Concurrency

**Scale out via the process model**

✅ **Implementation:**
- Horizontal scaling via process replication
- Different process types in `Procfile`:
  - `web`: HTTP requests
  - `worker`: Background jobs (Celery)
  - `beat`: Scheduled tasks
- Each process type scales independently
- Process manager handles concurrency (Docker, K8s, Systemd)

**Procfile:**
```
web: gunicorn config.wsgi --workers 4
worker: celery -A config worker --concurrency=2
beat: celery -A config beat
```

**Scaling:**
```bash
# Scale web processes
docker-compose up --scale web=5

# Scale worker processes
docker-compose up --scale worker=10
```

## IX. Disposability

**Maximize robustness with fast startup and graceful shutdown**

✅ **Implementation:**

### Fast Startup
- Minimal initialization time
- Lazy loading where possible
- Connection pooling with timeouts

### Graceful Shutdown
- SIGTERM handler registered
- Closes database connections
- Finishes current requests
- No orphaned transactions
- Celery workers finish current tasks

**Signal handler:**
```python
def graceful_shutdown(signum, frame):
    logger.info("Shutting down gracefully...")
    # Close connections
    for conn in connections.all():
        conn.close()
    sys.exit(0)

signal.signal(signal.SIGTERM, graceful_shutdown)
```

### Crash Resilience
- Process supervisor restarts crashed processes
- Database transactions use `ATOMIC_REQUESTS`
- Idempotent migrations

## X. Dev/Prod Parity

**Keep development, staging, and production as similar as possible**

✅ **Implementation:**

### Time Gap: Minimized
- Continuous deployment
- Same-day code → production

### Personnel Gap: Eliminated
- Developers deploy their code
- Infrastructure as code

### Tools Gap: Identical
- Same services in dev and prod:
  - PostgreSQL (not SQLite)
  - Redis
  - Same Python version
- Docker ensures consistency
- `docker-compose.yml` mirrors production

**Example:**
```yaml
# Same services dev and prod
services:
  db:
    image: postgres:16
  redis:
    image: redis:7
  web:
    build: .
```

## XI. Logs

**Treat logs as event streams**

✅ **Implementation:**
- All logs to `stdout`/`stderr`
- No log files in application
- Structured JSON logging in production
- Log aggregation by execution environment
- Stream-based log processing

**Logging config:**
```python
LOGGING = {
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json",  # Structured logs
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}
```

**Log aggregation:**
```bash
# Logs captured by platform
# Render: Dashboard logs
# Kubernetes: kubectl logs
# Docker: docker logs
# Systemd: journalctl
```

## XII. Admin Processes

**Run admin/management tasks as one-off processes**

✅ **Implementation:**
- Django management commands
- Same environment as web processes
- One-off process execution
- No special admin servers

**Examples:**
```bash
# Database migration
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Custom data import
python manage.py import_data

# Django shell
python manage.py shell

# Run in production
heroku run python manage.py migrate
kubectl exec -it pod -- python manage.py shell
docker-compose run web python manage.py createsuperuser
```

**Management command structure:**
```python
# apps/core/management/commands/import_data.py
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Admin task logic
        pass
```

---

## Verification Checklist

Use this checklist to verify 12-factor compliance:

- [x] **I. Codebase**: Git repo? Multiple environments?
- [x] **II. Dependencies**: `pyproject.toml`? Lock file?
- [x] **III. Config**: Environment variables? No secrets in code?
- [x] **IV. Backing Services**: URLs? Swappable?
- [x] **V. Build/Release/Run**: Separate stages? Release script?
- [x] **VI. Processes**: Stateless? No sticky sessions?
- [x] **VII. Port Binding**: Self-contained? Configurable port?
- [x] **VIII. Concurrency**: Procfile? Horizontal scaling?
- [x] **IX. Disposability**: Fast startup? Graceful shutdown?
- [x] **X. Dev/Prod Parity**: Same services? Docker?
- [x] **XI. Logs**: stdout/stderr? Structured?
- [x] **XII. Admin**: Management commands? One-off processes?

## References

- [The Twelve-Factor App](https://12factor.net/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [Django Environ Documentation](https://django-environ.readthedocs.io/)
