# Creating Your First Project

This guide walks you through creating your first Django Keel project and understanding what gets generated.

## Prerequisites

Before you begin, ensure you have:

- Python 3.12 or higher installed
- [Copier](https://copier.readthedocs.io/) installed (`pipx install copier`)
- Docker and Docker Compose installed
- Basic familiarity with Django

## Generate Your Project

### 1. Run Copier

```bash
copier copy gh:CuriousLearner/django-keel my-awesome-project
```

### 2. Answer the Prompts

Copier will ask you a series of questions. Here's a recommended configuration for your first project:

```
🎤 What is your project name? My Awesome Project
🎤 Python package name (slug)? my_awesome_project
🎤 Brief project description? My first Django Keel project
🎤 Your name? Your Name
🎤 Your email? your.email@example.com
🎤 Python version? 3.12
🎤 Package manager? uv
🎤 Database? postgresql
🎤 Cache backend? redis
🎤 API framework? drf
🎤 Frontend approach? none
🎤 Include Celery for background tasks? No
🎤 Include Django Channels for WebSockets? No
🎤 Authentication? allauth
🎤 Include 2FA (TOTP)? No
🎤 Observability features? minimal
🎤 Include Sentry error tracking? No
🎤 Deployment targets? none
🎤 Media file storage? local-whitenoise
🎤 Security level? standard
🎤 Use SOPS for encrypted secrets? No
🎤 Include Stripe payment integration? No
🎤 Search backend? none
🎤 Enable internationalization? No
🎤 CI/CD provider? github-actions
🎤 Project license? MIT
```

### 3. Navigate to Your Project

```bash
cd my-awesome-project
```

## Understanding the Project Structure

Your generated project will have the following structure:

```
my-awesome-project/
├── apps/                      # Django applications
│   ├── core/                 # Core app (health checks, utils)
│   ├── users/                # Custom user model
│   └── api/                  # API endpoints (DRF)
├── config/                    # Django configuration
│   ├── settings/             # Split settings
│   │   ├── base.py          # Shared settings
│   │   ├── dev.py           # Development settings
│   │   ├── test.py          # Test settings
│   │   └── prod.py          # Production settings
│   ├── urls.py              # URL configuration
│   ├── wsgi.py              # WSGI application
│   └── asgi.py              # ASGI application
├── docs/                      # MkDocs documentation
│   ├── index.md
│   ├── getting-started/
│   ├── architecture/
│   └── development/
├── tests/                     # Test suite
│   ├── conftest.py          # Pytest fixtures
│   ├── test_core.py         # Core tests
│   ├── test_users.py        # User tests
│   └── test_api.py          # API tests
├── static/                    # Static files
├── media/                     # User uploads
├── templates/                 # Django templates
├── .github/                   # GitHub Actions workflows
│   └── workflows/
│       └── ci.yml
├── docker-compose.yml         # Development environment
├── Dockerfile                 # Production Docker image
├── Justfile                   # Task runner
├── pyproject.toml            # Python dependencies
├── pytest.ini                # Pytest configuration
├── .pre-commit-config.yaml   # Pre-commit hooks
├── .env.example              # Environment variables template
├── README.md                 # Project README
├── CONTRIBUTING.md           # Contributing guide
└── CHANGELOG.md              # Changelog
```

## Set Up the Development Environment

### 1. Install Dependencies

```bash
uv sync
```

This installs all Python dependencies defined in `pyproject.toml`.

### 2. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and customize the values. For local development, the defaults usually work fine.

### 3. Start Services

```bash
docker compose up -d
```

This starts:

- PostgreSQL (port 5432)
- Redis (port 6379)
- Mailpit for email testing (port 8025)

### 4. Run Migrations

```bash
just migrate
```

Or manually:

```bash
uv run python manage.py migrate
```

### 5. Create a Superuser

```bash
just createsuperuser
```

Or manually:

```bash
uv run python manage.py createsuperuser
```

### 6. Start the Development Server

```bash
just dev
```

Or manually:

```bash
uv run python manage.py runserver
```

## Verify Everything Works

Visit the following URLs to verify your setup:

- **Application**: [http://localhost:8000](http://localhost:8000)
- **Admin Panel**: [http://localhost:8000/admin/](http://localhost:8000/admin/)
- **API Documentation**: [http://localhost:8000/api/schema/swagger/](http://localhost:8000/api/schema/swagger/)
- **Mailpit** (email testing): [http://localhost:8025](http://localhost:8025)

## Run the Tests

Your project comes with a comprehensive test suite:

```bash
just test
```

Or manually:

```bash
uv run pytest
```

All tests should pass! ✅

## Code Quality Checks

Run code quality checks:

```bash
# Format code
just format

# Lint code
just lint

# Type check
just typecheck

# Run all checks
just check
```

## Next Steps

Now that you have a working project:

1. **Explore the code**: Start with `apps/core/views.py` and `apps/api/views.py`
2. **Read the documentation**: Check out `docs/` directory
3. **Create your first app**: `uv run python manage.py startapp my_app apps/my_app`
4. **Add features**: Enable Celery, Channels, or Stripe in a new generation
5. **Deploy**: See [Deployment guides](../deployment/kubernetes.md)

## Common Issues

### Port Already in Use

If port 8000 is already in use:

```bash
# Run on a different port
uv run python manage.py runserver 8001
```

### Database Connection Error

If you can't connect to PostgreSQL:

```bash
# Check if PostgreSQL is running
docker compose ps

# Restart services
docker compose down
docker compose up -d
```

### Import Errors

If you get import errors:

```bash
# Reinstall dependencies
rm -rf .venv
uv sync
```

## Get Help

- Check the [documentation](https://django-keel.readthedocs.io/)
- Open an [issue](https://github.com/CuriousLearner/django-keel/issues)
- Start a [discussion](https://github.com/CuriousLearner/django-keel/discussions)

---

Congratulations! You've created your first Django Keel project! 🎉
