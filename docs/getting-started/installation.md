# 🚢 Django Keel

**A modern, production-ready Django project template with Copier**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Django 6.0](https://img.shields.io/badge/django-6.0-green.svg)](https://www.djangoproject.com/)

Django Keel is a comprehensive Copier template for Django projects that combines the best practices from over a decade of production Django development with modern tooling and deployment strategies.

## ✨ Features

### 🎯 Core
- **Django 5.2/6.0** with Python 3.12/3.13/3.14 support
- **uv** or **Poetry** for blazing-fast dependency management
- **12-Factor App** configuration with django-environ
- **Custom User Model** from day one
- **Split Settings** (base/dev/test/prod)

### 🔐 Authentication & Security
- django-allauth with email verification
- JWT authentication (SimpleJWT)
- 2FA support (TOTP)
- Security hardening (HSTS, CSP, etc.)
- SOPS for encrypted secrets
- Rate limiting and brute-force protection

### 🌐 API Options
- **Django REST Framework** with drf-spectacular (OpenAPI 3.0)
- **Strawberry GraphQL** (modern, type-safe)
- CORS configuration
- API versioning ready
- Automatic schema generation

### 🎨 Frontend Options
- **None** (API-only)
- **HTMX + Tailwind CSS + Alpine.js** (modern, minimal JS)
- **Next.js** (full-stack)

### ⚡ Async & Background Tasks
- **Celery** - Traditional async tasks (emails, reports, high-volume processing)
- **Temporal** - Durable workflows (onboarding, payment flows, long-running processes)
- **Both** - Use Celery AND Temporal together
- Celery Beat for periodic tasks
- Flower for monitoring
- **Django Channels** for WebSockets (optional)

### 📊 Observability
- **Structured JSON Logging**
- **Sentry** error tracking
- **OpenTelemetry** distributed tracing
- **Prometheus** metrics with django-prometheus
- Health and readiness endpoints

### 🚀 Deployment
- **Kubernetes** (Enterprise-scale):
  - Helm charts
  - Kustomize overlays (dev/staging/prod)
  - CloudNativePG operator for PostgreSQL
  - Traefik + cert-manager for ingress
  - Horizontal Pod Autoscaling
  - ArgoCD ready

- **AWS ECS Fargate** (Serverless containers):
  - No EC2 instance management
  - Application Load Balancer with auto-scaling
  - Multi-AZ high availability
  - Terraform infrastructure-as-code

- **Fly.io** (Global edge):
  - Deploy close to users worldwide
  - Automatic HTTPS and SSL
  - PostgreSQL and Redis included
  - Free tier available

- **Render** (Platform-as-Service):
  - One-click deployment from GitHub
  - Auto-deploy on git push
  - PostgreSQL and Redis included
  - Free tier available

- **AWS EC2 (Ansible)** (Full control):
  - Ubuntu 24.04 playbooks
  - Caddy reverse proxy with auto-HTTPS
  - Systemd services
  - Zero-downtime deployments

- **Docker** (Universal):
  - Multi-stage optimized builds
  - Deploy to any container platform

### 🧪 Developer Experience
- **ruff** for linting and formatting (10-100x faster)
  - Comprehensive rule set (Pyflakes, pycodestyle, isort, pep8-naming, pyupgrade, flake8-bugbear, and more)
  - 100-character line length
  - Modern Python 3.12+ type hints
- **mypy + django-stubs** for type checking
- **pytest** with coverage reporting
  - Function-based tests following best practices
  - Comprehensive fixtures
  - Conditional test generation based on features
- **pre-commit** hooks for automated quality checks
  - Trailing whitespace removal
  - YAML/JSON/TOML validation
  - Automatic linting and formatting
  - Type checking
- **Just** for task running (50+ commands)
- **Docker Compose** for local development
- **VS Code Devcontainer** support
- **MkDocs Material** documentation
- **Infrastructure validation** (YAML, Docker Compose, Helm, Ansible)

### 📦 Optional Features
- Stripe payment integration
- PostgreSQL Full-Text Search or OpenSearch
- Internationalization (i18n/l10n)
- Multi-tenancy (planned)
- Feature flags with django-waffle

### 🔄 Template Updates
- Built-in **Copier update mechanism**
- Track template version
- Merge upstream changes easily

## 🚀 Quick Start

### Prerequisites
- [Python 3.12+](https://www.python.org/downloads/)
- [Copier](https://copier.readthedocs.io/) (`pipx install copier`)
- [Docker & Docker Compose](https://docs.docker.com/get-docker/)

### Create a New Project

```bash
# Using copier
copier copy gh:CuriousLearner/django-keel your-project-name

# Follow the interactive prompts
```

### What Gets Generated

```
your-project/
├── apps/                      # Django applications
│   ├── core/                 # Core functionality (health checks, etc.)
│   ├── users/                # Custom user model
│   └── api/                  # API endpoints (if selected)
├── config/                    # Django configuration
│   ├── settings/             # Split settings
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── deploy/                    # Deployment configs
│   ├── k8s/                  # Kubernetes (Helm + Kustomize)
│   ├── ecs/                  # AWS ECS Fargate (Terraform)
│   ├── flyio/                # Fly.io configuration
│   ├── render/               # Render blueprints
│   └── ansible/              # EC2/Ansible playbooks
├── fly.toml                   # Fly.io config (if selected)
├── render.yaml                # Render blueprint (if selected)
├── docs/                      # MkDocs documentation
├── tests/                     # Test suite
├── Dockerfile                 # Production image
├── docker-compose.yml         # Development environment
├── Justfile                   # Task runner
├── pyproject.toml            # Dependencies & config
└── README.md
```

### Start Developing

```bash
cd your-project

# Install dependencies (uv)
uv sync

# Start services
docker compose up -d

# Run migrations
just migrate

# Create superuser
just createsuperuser

# Start development server
just dev
```

Visit:
- Application: http://localhost:8000
- Admin: http://localhost:8000/admin/
- API Docs: http://localhost:8000/api/schema/swagger/
- Mailpit: http://localhost:8025

## 🧪 Testing

The template includes comprehensive test suites for both the template itself and generated projects.

### Template Tests

```bash
# Run all template tests
pytest

# Run with coverage
pytest --cov

# 49 tests covering:
# - Django integration
# - Feature generation
# - Project structure validation
# - Conditional file generation
```

### Generated Project Tests

Each generated project includes a complete test suite with conditional test files:

```bash
cd your-project
just test

# Tests include:
# - Core functionality (health checks, settings, middleware)
# - User authentication and permissions
# - API endpoints (when enabled)
# - Celery tasks (when enabled)
# - Stripe integration (when enabled)
# - WebSocket functionality (when enabled)
# - 2FA authentication (when enabled)
```

## 📖 Documentation

Full documentation is available in the generated project's `docs/` directory.

Key topics:
- Getting Started
- Configuration
- API Development
- Deployment (Kubernetes, EC2)
- Monitoring & Observability
- Architecture Decision Records

## 🎨 Example Configurations

### Minimal API Project
```yaml
# Example answers
api_style: drf
frontend: none
background_tasks: none
observability_level: minimal
deployment_targets: render
```

### Full-Stack SaaS
```yaml
api_style: both  # DRF + GraphQL
frontend: nextjs
background_tasks: both  # Celery + Temporal
use_stripe: true
observability_level: full
deployment_targets: kubernetes,ecs
```

### HTMX Monolith
```yaml
api_style: drf
frontend: htmx-tailwind
background_tasks: celery
observability_level: standard
deployment_targets: flyio
```

### Hobby Project
```yaml
api_style: drf
frontend: htmx-tailwind
background_tasks: celery
observability_level: minimal
deployment_targets: render
```

## 🔄 Updating Your Project

When the template is updated, you can pull in changes:

```bash
cd your-project
copier update
```

Copier will intelligently merge changes, respecting your modifications.

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](https://github.com/CuriousLearner/django-keel/blob/main/CONTRIBUTING.md) for details.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/CuriousLearner/django-keel/blob/main/LICENSE) file for details.

## 🙏 Credits

Django Keel is inspired by:
- [django-init](https://github.com/fueled/django-init) - 10+ years of Django best practices
- [scaf](https://github.com/sixfeetup/scaf) - Copier-based approach and K8s patterns
- [cookiecutter-django](https://github.com/cookiecutter/cookiecutter-django) - Production-ready defaults
- [wemake-django-template](https://github.com/wemake-services/wemake-django-template) - Code quality focus

## 🌟 Star History

If you find Django Keel useful, please consider starring the repository!

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/CuriousLearner/django-keel/issues)
- **Discussions**: [GitHub Discussions](https://github.com/CuriousLearner/django-keel/discussions)
- **Docs**: Generated in your project's `docs/` directory

---

**Built with ❤️ by the Django community**
