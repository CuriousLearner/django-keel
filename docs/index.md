# 🚢 Django Keel

**A versatile, production-ready Django project template for any use case**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Django 5.2](https://img.shields.io/badge/django-5.2-green.svg)](https://www.djangoproject.com/)
[![Documentation Status](https://readthedocs.org/projects/django-keel/badge/?version=latest)](https://django-keel.readthedocs.io/en/latest/?badge=latest)

Build **SaaS applications**, **API backends**, **web apps**, or **internal tools** with one comprehensive template.

Django Keel is a modern Copier template that adapts to your needs—whether you're building a multi-tenant SaaS with billing, a simple API backend, a traditional web app, or an internal corporate tool. **One template, infinite possibilities.**

## 🎯 Why Django Keel?

### Choose Your Project Type, Get Smart Defaults

Django Keel asks you what type of project you're building and configures everything accordingly:

- **🚀 SaaS Application** - Multi-tenant SaaS with teams, Stripe billing, and feature gating
- **🔌 API Backend** - Clean REST/GraphQL API for mobile apps or microservices
- **🌐 Web Application** - Traditional Django web app with HTMX + Tailwind
- **🏢 Internal Tool** - Corporate dashboard with teams and permissions
- **⚙️ Custom** - Full control to configure everything yourself

[Learn more about Project Types →](getting-started/project-types.md)

### Production-Ready from Day One

- **Battle-tested architecture** from 10+ years of Django best practices
- **Security hardening** built-in (HSTS, CSP, rate limiting, 2FA)
- **6 deployment options** (Kubernetes, AWS ECS, Fly.io, Render, EC2, Docker)
- **Comprehensive observability** (logging, Sentry, OpenTelemetry, Prometheus)
- **127 template files** generating complete, working projects

### Modern Development Experience

- **⚡ uv** - 10-100x faster dependency management (or Poetry)
- **🧪 pytest** - Comprehensive test suite (80% coverage minimum)
- **✨ ruff** - Lightning-fast linting and formatting
- **🔍 mypy** - Type safety with django-stubs
- **🪝 pre-commit** - Automated quality checks
- **📦 Just** - 50+ task runner commands
- **🐳 Docker** - Complete local development environment

### Flexible & Adaptable

Choose exactly what you need:

=== "API Options"
    - Django REST Framework
    - Strawberry GraphQL
    - Both DRF + GraphQL
    - None (traditional views)

=== "Frontend Options"
    - None (API-only)
    - HTMX + Tailwind CSS + Alpine.js
    - Next.js (full-stack)

=== "Background Tasks"
    - Celery (traditional async tasks)
    - Temporal (durable workflows)
    - Both Celery + Temporal
    - None

=== "SaaS Features"
    - Teams/Organizations (multi-tenancy)
    - Stripe integration (basic or advanced)
    - Feature gating decorators
    - User impersonation
    - Feature flags (A/B testing)

=== "Deployment"
    - Kubernetes (Helm + Kustomize)
    - AWS ECS Fargate (Terraform)
    - Fly.io (global edge)
    - Render (PaaS)
    - AWS EC2 (Ansible)
    - Docker (universal)

## 🚀 Quick Start

```bash
# Install Copier
pipx install copier

# Create your project
copier copy gh:CuriousLearner/django-keel your-project-name

# Answer a few questions about your project type
# Django Keel configures everything automatically!

# Start developing
cd your-project-name
uv sync
docker compose up -d
just migrate
just createsuperuser
just dev
```

Visit:
- **Application**: http://localhost:8000
- **Admin**: http://localhost:8000/admin/
- **API Docs**: http://localhost:8000/api/schema/swagger/
- **Mailpit**: http://localhost:8025

[Detailed Quick Start Guide →](getting-started/quickstart.md)

## ✨ Features at a Glance

### 🎯 Core Foundation

- **Django 5.2** with Python 3.12/3.13
- **Custom User Model** from day one
- **Split Settings** (base/dev/test/prod)
- **12-Factor App** configuration with django-environ
- **uv or Poetry** for dependency management

### 🔐 Authentication & Security

- **django-allauth** with email verification
- **JWT authentication** (SimpleJWT)
- **2FA support** (TOTP with QR codes)
- **Security hardening** (HSTS, CSP, rate limiting)
- **SOPS** for encrypted secrets management

### 🌐 API Development

- **Django REST Framework** with drf-spectacular (OpenAPI 3.0)
- **Strawberry GraphQL** (modern, type-safe)
- **CORS** configuration
- **API versioning** ready
- **Automatic schema generation**

### 🎨 Frontend Options

- **None** - API-only backend
- **HTMX + Tailwind CSS + Alpine.js** - Modern, minimal JavaScript
- **Next.js** - Full-stack with React

### ⚡ Background Tasks & Async

- **Celery** - Traditional async tasks (emails, reports, high-volume jobs)
- **Temporal** - Durable workflows (onboarding, payment flows, sagas)
- **Django Channels** - WebSockets for real-time features
- **Celery Beat** - Periodic task scheduling
- **Flower** - Task monitoring UI

### 💼 SaaS Features (Optional)

- **Teams/Organizations** - Full multi-tenancy with RBAC
  - Owner/Admin/Member roles
  - Team invitations with email tokens
  - Per-seat billing integration

- **Advanced Stripe Integration** - Production-ready billing
  - Basic mode (stripe API) or Advanced mode (dj-stripe)
  - Subscription management with metadata
  - Per-seat and usage-based billing
  - Webhook handlers for all events
  - Customer portal integration

- **Feature Gating** - Subscription-based access control
  - `@subscription_required`, `@feature_required`, `@plan_required` decorators
  - Usage limit checking
  - Class-based view mixins

- **User Impersonation** - Admin support tools
  - Staff can impersonate users for debugging
  - Full audit logging
  - Security checks built-in

- **Feature Flags** - A/B testing with django-waffle
  - Flags, switches, and samples
  - User/group-based targeting
  - Gradual rollouts

[Learn more about SaaS Features →](saas/overview.md)

### 🚀 Deployment Options

**6 deployment targets to choose from:**

=== "Kubernetes"
    Enterprise-scale with Helm charts, Kustomize overlays, CloudNativePG, Traefik, HPA, ArgoCD ready

    [Kubernetes Guide →](deployment/kubernetes.md)

=== "AWS ECS Fargate"
    Serverless containers with no EC2 management, Application Load Balancer, Multi-AZ HA, Terraform IaC

    [ECS Guide →](deployment/ecs.md)

=== "Fly.io"
    Global edge deployment, automatic HTTPS, PostgreSQL + Redis included, free tier available

    [Fly.io Guide →](deployment/flyio.md)

=== "Render"
    One-click PaaS deployment from GitHub, auto-deploy on push, free tier available

    [Render Guide →](deployment/render.md)

=== "AWS EC2"
    Full control with Ansible, Ubuntu 24.04, Caddy reverse proxy, systemd services

    [EC2 Guide →](deployment/aws-ec2.md)

=== "Docker"
    Universal deployment anywhere, multi-stage optimized builds, docker-compose for dev

    [Docker Guide →](deployment/docker.md)

### 📊 Observability (3 Levels)

=== "Minimal"
    Basic logging for hobby projects

=== "Standard"
    Structured JSON logging + Sentry error tracking

=== "Full"
    OpenTelemetry + Prometheus + distributed tracing + custom metrics

[Learn more about Observability →](features/observability.md)

### 🧪 Developer Experience

- **ruff** - 10-100x faster linting (13+ rule categories)
- **mypy + django-stubs** - Type checking
- **pytest** - 80% coverage requirement
- **pre-commit** - Automated quality checks
- **Just** - 50+ task runner commands
- **Docker Compose** - Complete dev environment
- **MkDocs Material** - Beautiful documentation
- **Infrastructure validation** - YAML, Docker, Helm, Ansible

### 📦 Additional Features

- **Search** - PostgreSQL Full-Text Search or OpenSearch
- **Storage** - Local, AWS S3, GCP GCS, Azure Storage
- **Email** - Professional email template system
- **i18n** - Internationalization support
- **CI/CD** - GitHub Actions or GitLab CI

## 📚 Documentation

### Getting Started
- [Quick Start](getting-started/quickstart.md) - Get started in 5 minutes
- [Installation](getting-started/installation.md) - Detailed setup instructions
- [First Project](getting-started/first-project.md) - Build your first Django Keel project
- [Project Types](getting-started/project-types.md) - Choose the right project type

### Features
- [Features Overview](features/overview.md) - Complete feature list
- [API Options](features/api-options.md) - DRF, GraphQL, or both
- [Authentication](features/authentication.md) - Auth backends and 2FA
- [Background Tasks](features/background-tasks.md) - Celery vs Temporal
- [Frontend Options](features/frontend-options.md) - HTMX vs Next.js
- [Observability](features/observability.md) - Logging, metrics, tracing

### SaaS Features
- [SaaS Overview](saas/overview.md) - Build a complete SaaS
- [Teams & Organizations](saas/teams.md) - Multi-tenancy with RBAC
- [Stripe Integration](saas/stripe.md) - Subscription billing
- [Feature Gating](saas/feature-gating.md) - Access control by plan
- [User Impersonation](saas/impersonation.md) - Debug user issues
- [Feature Flags](saas/feature-flags.md) - A/B testing

### Deployment
- [Deployment Overview](deployment/overview.md) - Choose your platform
- [Kubernetes](deployment/kubernetes.md) - Enterprise-scale
- [AWS ECS Fargate](deployment/ecs.md) - Serverless containers
- [Fly.io](deployment/flyio.md) - Global edge
- [Render](deployment/render.md) - Simple PaaS
- [AWS EC2 (Ansible)](deployment/aws-ec2.md) - Full control
- [Docker](deployment/docker.md) - Universal

## 🎨 Example Configurations

### SaaS Application

```yaml
project_type: saas

# Smart defaults applied:
# - API: DRF for backend
# - Frontend: Next.js for modern SPA
# - Teams: Enabled (multi-tenancy)
# - Stripe: Advanced mode with dj-stripe
# - Background: Celery for emails/async tasks
# - Deployment: Kubernetes for scale
```

### API Backend

```yaml
project_type: api

# Smart defaults applied:
# - API: DRF only
# - Frontend: None
# - Teams: Disabled
# - Stripe: Disabled
# - Background: Celery for async processing
# - Deployment: Render for easy hosting
```

### Web Application

```yaml
project_type: web-app

# Smart defaults applied:
# - API: None (traditional Django views)
# - Frontend: HTMX + Tailwind CSS
# - Teams: Disabled
# - Stripe: Disabled
# - Background: Celery for emails
# - Deployment: Fly.io for global edge
```

### Internal Tool

```yaml
project_type: internal-tool

# Smart defaults applied:
# - API: DRF for flexibility
# - Frontend: HTMX + Tailwind CSS
# - Teams: Enabled (departments/groups)
# - Stripe: Disabled (no billing)
# - Background: Celery for reports
# - Deployment: AWS EC2 (on-premise friendly)
```

[More examples →](getting-started/project-types.md)

## 🔄 Template Updates

Built-in Copier update mechanism allows you to pull in template improvements:

```bash
cd your-project
copier update
```

Copier intelligently merges changes while preserving your customizations.

## 🤝 Contributing

Contributions are welcome! See our [Contributing Guide](contributing/development.md).

## 📜 License

MIT License - see [LICENSE](https://github.com/CuriousLearner/django-keel/blob/main/LICENSE)

## 🙏 Credits

Django Keel is inspired by:

- [django-init](https://github.com/fueled/django-init) - 10+ years of Django best practices
- [scaf](https://github.com/sixfeetup/scaf) - Copier-based approach and K8s patterns
- [cookiecutter-django](https://github.com/cookiecutter/cookiecutter-django) - Production-ready defaults
- [wemake-django-template](https://github.com/wemake-services/wemake-django-template) - Code quality focus

## 📞 Community & Support

- **Issues**: [GitHub Issues](https://github.com/CuriousLearner/django-keel/issues)
- **Discussions**: [GitHub Discussions](https://github.com/CuriousLearner/django-keel/discussions)
- **Changelog**: [CHANGELOG](CHANGELOG.md)

---

**Built with ❤️ by the Django community**
