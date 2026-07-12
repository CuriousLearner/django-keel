# Docker Deployment

All Django Keel projects include a `Dockerfile` and a `docker-compose.yml` at the project root - they are always generated, regardless of your `deployment_targets` selection.

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
  -e DEBUG=False \
  -e DJANGO_ALLOWED_HOSTS=yourdomain.com \
  your-project:latest
```

## Docker Compose (Production)

The generated `docker-compose.yml` is a development stack (with Mailpit, mounted source, etc.). For production, write your own compose file along these lines:

```yaml
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

## Image Layout

The generated Dockerfile uses a single Python stage based on `python:<version>-slim`, installing dependencies with your chosen package manager (uv or Poetry) and running as a non-root user. When you choose the HTMX + Tailwind frontend with Vite bundling, a Node `frontend-builder` stage builds the assets first and copies `static/dist` into the final image:

```dockerfile
# Only with frontend_bundling: vite
FROM node:26-slim AS frontend-builder
# npm ci && npm run build

FROM python:3.14-slim as base
# Install dependencies, copy app, run gunicorn (or daphne with Channels)
```

## Security

- Runs as non-root user
- Minimal base image
- Security updates applied
- Secrets via environment variables
