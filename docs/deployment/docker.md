# Docker Deployment

All Django Keel projects include production-ready Dockerfiles.

## Building the Image

```bash
docker build -t your-project:latest .
```

## Running the Container

```bash
docker run -d \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql://user:password@db:5432/dbname \
  -e DJANGO_SECRET_KEY=your-secret-key \
  -e DJANGO_DEBUG=False \
  -e DJANGO_ALLOWED_HOSTS=yourdomain.com \
  your-project:latest
```

## Docker Compose (Production)

```yaml
version: '3.8'

services:
  web:
    image: your-project:latest
    ports:
      - "8000:8000"
    env_file:
      - .env.prod
    depends_on:
      - db
      - redis

  db:
    image: postgres:16
    volumes:
      - postgres_data:/var/lib/postgresql/data
    env_file:
      - .env.prod

  redis:
    image: redis:7-alpine

volumes:
  postgres_data:
```

## Multi-Stage Build

The generated Dockerfile uses multi-stage builds for smaller images:

```dockerfile
# Build stage
FROM python:3.12-slim as builder
# Install dependencies

# Runtime stage
FROM python:3.12-slim
# Copy only necessary files
```

## Security

- Runs as non-root user
- Minimal base image
- Security updates applied
- Secrets via environment variables
