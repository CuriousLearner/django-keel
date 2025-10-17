# Django Keel Usage Guide

Complete guide to using the django-keel template.

## Table of Contents

- [Quick Start](#quick-start)
- [Template Options](#template-options)
- [Development Workflow](#development-workflow)
- [Testing](#testing)
- [Deployment](#deployment)
- [Updating from Template](#updating-from-template)
- [Common Tasks](#common-tasks)

## Quick Start

### 1. Install Copier

```bash
pipx install copier
```

### 2. Generate Your Project

```bash
copier copy gh:CuriousLearner/django-keel my-awesome-project
```

You'll be asked a series of questions. Here's an example session:

```
🎤 What is your project name? My Awesome Project
🎤 Python package name (slug)? my_awesome_project
🎤 Brief project description? An awesome Django application
🎤 Your name? John Doe
🎤 Your email? john@example.com
🎤 Python version? 3.13
🎤 Package manager? uv
🎤 Database? postgresql
🎤 Cache backend? redis
🎤 API framework? drf
🎤 Frontend approach? htmx-tailwind
🎤 Include Celery for background tasks? Yes
🎤 Include Django Channels for WebSockets? No
🎤 Authentication? allauth
🎤 Include 2FA (TOTP)? No
🎤 Observability features? standard
🎤 Include Sentry error tracking? Yes
🎤 Deployment targets? kubernetes
🎤 Media file storage? aws-s3
🎤 Security level? standard
🎤 Use SOPS for encrypted secrets? No
🎤 Include Stripe payment integration? No
🎤 Search backend? none
🎤 Enable internationalization? No
🎤 CI/CD provider? github-actions
🎤 Project license? MIT
```

### 3. Start Development

```bash
cd my-awesome-project

# Install dependencies
uv sync

# Start services
docker compose up -d

# Run migrations
just migrate

# Create superuser
just createsuperuser

# Start dev server
just dev
```

## Template Options

### API Styles

- **`drf`**: Django REST Framework with OpenAPI docs
- **`graphql-strawberry`**: Strawberry GraphQL (type-safe, modern)
- **`both`**: DRF + GraphQL
- **`none`**: No API (traditional Django views)

### Frontend Options

- **`none`**: API-only backend
- **`htmx-tailwind`**: HTMX + Tailwind CSS + Alpine.js (recommended for Django developers)
- **`nextjs`**: Full Next.js frontend (separate project)

### Observability Levels

- **`minimal`**: Basic structured logging
- **`standard`**: Logging + Sentry
- **`full`**: OpenTelemetry + Prometheus + Grafana + Sentry

### Deployment Targets

- **`render`**: Zero-config PaaS deployment with render.yaml
- **`flyio`**: Global edge deployment with fly.toml
- **`aws-ecs-fargate`**: Serverless containers with Terraform
- **`docker`**: Universal containerization
- **`aws-ec2-ansible`**: EC2 deployment via Ansible
- **`kubernetes`**: Full K8s setup with Helm + Kustomize

You can specify multiple targets separated by commas: `render,flyio,docker`

See [Deployment Overview](../deployment/overview.md) for detailed comparison and guides.

## Development Workflow

### Using Just (Task Runner)

All common tasks are available via `just`:

```bash
just --list                # Show all commands
just dev                   # Start dev server
just test                  # Run tests
just test-cov              # Run tests with coverage
just lint                  # Lint code
just format                # Format code
just typecheck             # Type check with mypy
just shell                 # Django shell
just makemigrations        # Create migrations
just migrate               # Run migrations
just createsuperuser       # Create admin user
```

### Docker Compose Services

```bash
just up                    # Start all services
just down                  # Stop all services
just logs                  # View logs
```

Services include:
- **PostgreSQL** (port 5432)
- **Redis** (port 6379, if enabled)
- **Mailpit** (SMTP: 1025, Web UI: 8025)

### Celery Tasks

If you enabled Celery:

```bash
just celery-worker         # Start worker
just celery-beat           # Start beat (periodic tasks)
just celery-flower         # Start Flower (monitoring)
```

## Testing

### Run Tests

```bash
# All tests
just test

# With coverage
just test-cov

# Specific test file
uv run pytest tests/test_users.py

# Specific test
uv run pytest tests/test_users.py::TestUserModel::test_create_user

# With verbose output
uv run pytest -v

# Stop on first failure
uv run pytest -x
```

### Code Quality

```bash
# Lint
just lint                  # or: uv run ruff check .

# Format
just format                # or: uv run ruff format .

# Type check
just typecheck             # or: uv run mypy .

# Run all checks
just check                 # lint + typecheck + test
```

### Pre-commit Hooks

Install pre-commit hooks to run checks automatically:

```bash
uv run pre-commit install

# Run manually
uv run pre-commit run --all-files
```

## Deployment

### Kubernetes

1. **Build and push image**:

```bash
docker build -t your-registry/my-project:v1.0.0 .
docker push your-registry/my-project:v1.0.0
```

2. **Deploy with Helm**:

```bash
cd deploy/k8s/helm/my_project

# Install
helm install my-project . -f values.yaml

# Upgrade
helm upgrade my-project . -f values.yaml
```

3. **Deploy with Kustomize**:

```bash
# Development
kubectl apply -k deploy/k8s/kustomize/overlays/dev

# Production
kubectl apply -k deploy/k8s/kustomize/overlays/prod
```

See `deploy/k8s/README.md` for detailed instructions.

### AWS EC2 (Ansible)

1. **Configure inventory**:

```bash
cd deploy/ansible
cp inventory/hosts.example inventory/hosts
# Edit with your EC2 details
```

2. **Configure variables**:

```bash
cp group_vars/all.yml.example group_vars/all.yml
# Update with your settings
```

3. **Deploy**:

```bash
# Initial setup
ansible-playbook -i inventory/hosts playbooks/setup.yml

# Deploy application
ansible-playbook -i inventory/hosts playbooks/deploy.yml
```

See `deploy/ansible/README.md` for detailed instructions.

## Updating from Template

When the django-keel template is updated, you can merge changes:

```bash
# Check for updates
copier update --pretend

# Apply updates
copier update

# Update to specific version
copier update --vcs-ref=v1.2.0
```

Copier will:
1. Show you what will change
2. Ask for confirmation
3. Intelligently merge changes
4. Respect your custom modifications

### Handling Conflicts

If there are conflicts:
1. Copier will mark them with conflict markers
2. Resolve manually
3. Test thoroughly
4. Commit

## Common Tasks

### Add a New Django App

```bash
uv run python manage.py startapp my_app apps/my_app

# Register in config/settings/base.py
# Add to INSTALLED_APPS
```

### Add Dependencies

```bash
# Using uv
uv add django-package-name

# Dev dependency
uv add --dev pytest-package-name

# Using Poetry
poetry add django-package-name
poetry add --group dev pytest-package-name
```

### Database Operations

```bash
# Create migration
just makemigrations

# Apply migrations
just migrate

# Show migrations
uv run python manage.py showmigrations

# Rollback migration
uv run python manage.py migrate app_name 0001

# Reset database (CAUTION!)
docker compose down -v  # Destroys data!
docker compose up -d
just migrate
```

### Create API Endpoint (DRF)

1. Create serializer in `apps/api/serializers.py`
2. Create viewset in `apps/api/views.py`
3. Register in router in `apps/api/urls.py`
4. View auto-generated docs at `/api/schema/swagger/`

### Background Task (Celery)

```python
# apps/my_app/tasks.py
from celery import shared_task

@shared_task
def my_background_task(arg1, arg2):
    # Do work
    return result

# Call it
from apps.my_app.tasks import my_background_task
my_background_task.delay(arg1, arg2)
```

### Environment Variables

Always add new variables to:
1. `.env.example` (with placeholder)
2. `config/settings/base.py` (read with `env()`)
3. Deployment configs (K8s ConfigMap/Secret, Ansible vars)

### Static Files

```bash
# Collect static
just collectstatic

# Or manually
uv run python manage.py collectstatic --noinput
```

### Documentation

```bash
# Serve locally
just docs-serve

# Build
just docs-build

# Add ADR (Architecture Decision Record)
# Create file in docs/adr/NNNN-my-decision.md
```

## Troubleshooting

### Database Connection Issues

```bash
# Check if PostgreSQL is running
docker compose ps

# View logs
docker compose logs db

# Restart
docker compose restart db
```

### Redis Connection Issues

```bash
# Check Redis
docker compose ps redis
docker compose logs redis

# Test connection
docker compose exec redis redis-cli ping
# Should return: PONG
```

### Import Errors

```bash
# Reinstall dependencies
rm -rf .venv
uv sync
```

### Migration Conflicts

```bash
# Show current state
uv run python manage.py showmigrations

# If needed, fake a migration
uv run python manage.py migrate --fake app_name migration_name
```

## Best Practices

1. **Always use `just` commands** for common tasks
2. **Run tests before committing**: `just check`
3. **Keep `.env.example` updated** when adding new variables
4. **Write tests** for new features
5. **Document in `docs/`** for complex features
6. **Use ADRs** for architectural decisions
7. **Tag releases** when deploying
8. **Monitor** your application in production

## Next Steps

- Explore the [API Options](api-options.md) in detail
- Learn about [Background Tasks](background-tasks.md)
- Review [Deployment Options](../deployment/overview.md)
- Check out [Authentication](authentication.md) setup

---

**Questions?** Open an issue or check the [Discussions](https://github.com/CuriousLearner/django-keel/discussions)
