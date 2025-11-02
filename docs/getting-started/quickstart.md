# Quick Start - Test Django Keel Template

This guide shows how to quickly test the django-keel template.

## Prerequisites

```bash
# Install Copier
pipx install copier

# Or with pip
pip install copier
```

## Test the Template Locally

### 1. Generate a Test Project

From the django-keel directory:

```bash
# Generate a project with default options
copier copy . ../test-project --force

# Or with specific options
copier copy . ../my-api-project \
  --data project_name="My API Project" \
  --data api_style=drf \
  --data frontend=none \
  --data background_tasks=none \
  --data deployment_targets=[kubernetes]
```

### 2. Quick Test (Minimal Config)

```bash
# Go to generated project
cd ../test-project

# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync

# Start services
docker compose up -d

# Wait for services to be ready (about 10 seconds)
sleep 10

# Run migrations
uv run python manage.py migrate

# Create superuser (non-interactive for testing)
uv run python manage.py createsuperuser \
  --email admin@example.com \
  --noinput || true

# Run tests
uv run pytest

# Check code quality
uv run ruff check .
uv run mypy .

# Start development server
uv run python manage.py runserver
```

Visit:
- http://localhost:8000 - Application
- http://localhost:8000/admin/ - Admin (login: admin@example.com)
- http://localhost:8000/api/schema/swagger/ - API Docs
- http://localhost:8025 - Mailpit (email testing)

### 3. Test with Justfile

```bash
# List all available commands
just --list

# Run common tasks
just test
just lint
just format
just typecheck

# Or run full check
just check
```

### 4. Test Docker Build

```bash
# Build production image
docker build -t test-project:latest .

# Run it
docker run -p 8000:8000 \
  -e DATABASE_URL=sqlite:///db.sqlite3 \
  -e DJANGO_SECRET_KEY=test-secret-key-change-in-production \
  -e DJANGO_DEBUG=False \
  test-project:latest
```

### 5. Test Template Update

```bash
# From the test project directory
cd ../test-project

# Preview what would change
copier update --pretend

# Apply updates
copier update
```

## Test Different Configurations

### API-Only Project

```bash
copier copy ../django-keel ../api-only \
  --data api_style=drf \
  --data frontend=none \
  --data background_tasks=none

cd ../api-only
uv sync
just test
```

### Full-Stack with HTMX

```bash
copier copy ../django-keel ../fullstack-htmx \
  --data api_style=both \
  --data frontend=htmx-tailwind \
  --data background_tasks=celery \
  --data observability_level=full

cd ../fullstack-htmx
uv sync
docker compose up -d
just migrate
just dev
```

### SaaS with All Features

```bash
copier copy ../django-keel ../saas-project \
  --data api_style=both \
  --data frontend=nextjs \
  --data background_tasks=both \
  --data use_stripe=true \
  --data use_search=postgres-fts \
  --data observability_level=full \
  --data security_profile=strict \
  --data deployment_targets=[kubernetes,aws-ecs-fargate,flyio]

cd ../saas-project
uv sync
docker compose up -d
just migrate
just test
```

## Verify Template Quality

### 1. Check Generated Files

```bash
cd ../test-project

# Count Python files
find . -name "*.py" | wc -l

# Check structure
tree -L 3 -I '__pycache__|*.pyc|.venv'

# Verify no Jinja syntax errors
grep -r "{{" . --include="*.py" --include="*.md"  # Should be empty
```

### 2. Run All Quality Checks

```bash
# Linting
uv run ruff check .

# Formatting check
uv run ruff format --check .

# Type checking
uv run mypy .

# Tests
uv run pytest -v

# Coverage
uv run pytest --cov --cov-report=term
```

### 3. Test CI/CD

```bash
# Simulate CI pipeline
docker compose up -d
uv run ruff check .
uv run mypy .
uv run pytest --cov
docker build -t test:latest .

# If you have act (GitHub Actions locally)
act -j test
```

### 4. Test Deployment Configs

```bash
# Kubernetes (if you have kubectl and kind)
cd deploy/k8s

# Validate manifests
kubectl apply --dry-run=client -f kustomize/base/

# Test Helm chart
helm lint helm/test_project/

# Ansible (syntax check)
cd ../ansible
ansible-playbook playbooks/deploy.yml --syntax-check
```

## Common Issues

### Database Connection

If migrations fail:

```bash
# Check if PostgreSQL is running
docker compose ps

# View logs
docker compose logs db

# Restart
docker compose down && docker compose up -d
sleep 10
just migrate
```

### Import Errors

If you get import errors:

```bash
# Reinstall
rm -rf .venv
uv sync
```

### Port Already in Use

If port 8000 is taken:

```bash
# Run on different port
uv run python manage.py runserver 8001
```

## Benchmark Template Generation

```bash
# Time template generation
time copier copy . ../benchmark-test --force

# Typical times:
# - Template generation: 2-5 seconds
# - uv sync: 10-30 seconds
# - docker compose up: 10-20 seconds
# - Migrations: 1-2 seconds
# - Tests: 5-10 seconds

# Total: ~1-2 minutes from zero to working project
```

## Cleanup

```bash
# Remove test projects
cd ..
rm -rf test-project api-only fullstack-htmx saas-project benchmark-test
```

## Next Steps

After testing locally:

1. **Publish to GitHub**:
```bash
cd django-keel
git init
git add .
git commit -m "Initial commit"
gh repo create CuriousLearner/django-keel --public
git push origin main
```

2. **Tag a Release**:
```bash
git tag -a v0.1.0 -m "Initial release"
git push origin v0.1.0
```

3. **Use from GitHub**:
```bash
copier copy gh:CuriousLearner/django-keel my-new-project
```

4. **Share with Community**:
- Post on Django forum
- Share on Twitter/X
- Submit to awesome-django lists
- Write blog post

---

## Testing Checklist

- [ ] Template generates without errors
- [ ] All tests pass
- [ ] Linting passes
- [ ] Type checking passes
- [ ] Docker Compose works
- [ ] Docker build succeeds
- [ ] Development server starts
- [ ] Admin panel accessible
- [ ] API docs load
- [ ] Database migrations work
- [ ] Celery tasks work (if enabled)
- [ ] GraphQL endpoint works (if enabled)
- [ ] HTMX pages render (if enabled)
- [ ] Template update works
- [ ] Documentation builds
- [ ] CI/CD validates (if pushed to GitHub)

---

**Ready to use django-keel!** 🚢
