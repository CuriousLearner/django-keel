# Django Keel

**A modern, production-ready Django project template with Copier**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Django 5.2](https://img.shields.io/badge/django-5.2-green.svg)](https://www.djangoproject.com/)
[![Documentation Status](https://readthedocs.org/projects/django-keel/badge/?version=latest)](https://django-keel.readthedocs.io/en/latest/?badge=latest)

Django Keel is a comprehensive Copier template for Django projects that combines the best practices from over a decade of production Django development with modern tooling and deployment strategies.

## Why Django Keel?

### 🚀 Production-Ready from Day One

- **Battle-tested architecture** from years of real-world Django projects
- **Security hardening** built-in (HSTS, CSP, rate limiting)
- **Multiple deployment options** (Kubernetes, AWS EC2, more coming)
- **Comprehensive observability** (logging, metrics, tracing)

### ⚡ Modern Development Experience

- **Blazing-fast dependency management** with uv or Poetry
- **Comprehensive testing** with pytest (49 tests for template, full suite for generated projects)
- **Code quality tooling** (ruff, mypy, pre-commit hooks)
- **Infrastructure validation** (YAML, Docker, Helm, Ansible)

### 🎯 Flexible & Customizable

Choose exactly what you need:

- **API**: Django REST Framework, GraphQL (Strawberry), both, or none
- **Frontend**: HTMX + Tailwind, Next.js, or API-only
- **Background Tasks**: Celery with Redis
- **WebSockets**: Django Channels
- **Payments**: Stripe integration
- **Search**: PostgreSQL FTS or OpenSearch
- **Deployment**: Kubernetes (Helm + Kustomize), AWS EC2 (Ansible)
- **Observability**: Minimal, standard, or full stack
- **And much more...**

### 🔄 Template Updates

Built-in Copier update mechanism allows you to pull in template improvements while preserving your customizations.

## Quick Start

```bash
# Install Copier
pipx install copier

# Create your project
copier copy gh:CuriousLearner/django-keel your-project-name

# Start developing
cd your-project-name
uv sync
docker compose up -d
just migrate
just dev
```

Visit [Quick Start](getting-started/quickstart.md) for detailed instructions.

## Features Overview

### Core

- Django 5.2 with Python 3.12/3.13
- uv or Poetry for dependency management
- 12-Factor App configuration
- Custom User Model from day one
- Split settings (dev/test/prod)

### Authentication & Security

- django-allauth with email verification
- JWT authentication (SimpleJWT)
- 2FA support (TOTP)
- Security hardening (HSTS, CSP, etc.)
- SOPS for encrypted secrets
- Rate limiting

### APIs

- Django REST Framework with drf-spectacular
- Strawberry GraphQL (modern, type-safe)
- CORS configuration
- API versioning ready
- Automatic schema generation

### Frontend

- None (API-only)
- HTMX + Tailwind CSS + Alpine.js
- Next.js (full-stack)

### Background Tasks

- Celery with Redis broker
- Celery Beat for periodic tasks
- Flower for monitoring

### Deployment

**Kubernetes**:

- Helm charts
- Kustomize overlays (dev/staging/prod)
- CloudNativePG operator for PostgreSQL
- Traefik + cert-manager for ingress
- Horizontal Pod Autoscaling
- ArgoCD ready

**AWS EC2**:

- Ubuntu 24.04 Ansible playbooks
- Caddy reverse proxy with auto-HTTPS
- Systemd services
- Zero-downtime deployments

### Observability

- Structured JSON logging
- Sentry error tracking
- OpenTelemetry distributed tracing
- Prometheus metrics
- Health and readiness endpoints

### Developer Experience

- ruff for linting and formatting (10-100x faster)
  - Comprehensive rule set (13+ categories)
  - Modern Python 3.12+ type hints
- mypy + django-stubs for type checking
- pytest with coverage reporting
  - 49 tests for template validation
  - Comprehensive test suite for generated projects
- pre-commit hooks for automated quality checks
- Just task runner (50+ commands)
- Docker Compose for local development
- MkDocs Material documentation
- Infrastructure validation

## Example Configurations

### Minimal API Project

```yaml
api_style: drf
frontend: none
use_celery: false
observability_level: minimal
deployment_targets: kubernetes
```

### Full-Stack SaaS

```yaml
api_style: both  # DRF + GraphQL
frontend: nextjs
use_celery: true
use_stripe: true
observability_level: full
deployment_targets: kubernetes,aws-ec2-ansible
```

### HTMX Monolith

```yaml
api_style: drf
frontend: htmx-tailwind
use_celery: true
observability_level: standard
deployment_targets: aws-ec2-ansible
```

## What You Get

When you generate a project with Django Keel:

- **Complete project structure** with Django apps, configuration, and deployment configs
- **Working CI/CD** with GitHub Actions or GitLab CI
- **Docker setup** for development and production
- **Comprehensive tests** (conditional based on your selections)
- **Full documentation** with MkDocs
- **Infrastructure as code** (Kubernetes manifests, Ansible playbooks)
- **Quality tooling** (linting, formatting, type checking)

## Documentation

- [Quick Start](getting-started/quickstart.md) - Get up and running in 5 minutes
- [Installation](getting-started/installation.md) - Detailed installation guide
- [Features](features/overview.md) - Deep dive into all features
- [Deployment](deployment/kubernetes.md) - Deploy to production
- [Contributing](contributing/development.md) - Contribute to Django Keel

## Community & Support

- **Issues**: [GitHub Issues](https://github.com/CuriousLearner/django-keel/issues)
- **Discussions**: [GitHub Discussions](https://github.com/CuriousLearner/django-keel/discussions)
- **Changelog**: [CHANGELOG.md](CHANGELOG.md)

## Credits

Django Keel is inspired by:

- [django-init](https://github.com/fueled/django-init) - 10+ years of Django best practices
- [scaf](https://github.com/sixfeetup/scaf) - Copier-based approach and K8s patterns
- [cookiecutter-django](https://github.com/cookiecutter/cookiecutter-django) - Production-ready defaults
- [wemake-django-template](https://github.com/wemake-services/wemake-django-template) - Code quality focus

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/CuriousLearner/django-keel/blob/main/LICENSE) file for details.

---

**Built with ❤️ by the Django community**
