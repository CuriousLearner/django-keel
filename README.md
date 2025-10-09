# 🚢 Django Keel

**A versatile, production-ready Django project template for any use case**

Build **SaaS applications**, **API backends**, **web apps**, or **internal tools** with one template.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Django 5.2](https://img.shields.io/badge/django-5.2-green.svg)](https://www.djangoproject.com/)
[![Documentation](https://readthedocs.org/projects/django-keel/badge/?version=latest)](https://django-keel.readthedocs.io/en/latest/?badge=latest)

Django Keel is a comprehensive Copier template that adapts to your needs—whether you're building a multi-tenant SaaS with billing, a simple API backend, a traditional web app, or an internal corporate tool. One template, infinite possibilities.

**Choose your project type and get smart defaults. Or customize everything yourself.**

## ✨ Features

### 🎯 Core
- **Django 5.2** with Python 3.12/3.13
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
  - Automatic HTTPS & SSL
  - PostgreSQL & Redis included
  - Free tier: 3 VMs, 3GB DB, 160GB bandwidth
  - Multi-region deployment

- **Render** (Platform-as-Service):
  - One-click deployment from GitHub
  - Auto-deploy on git push
  - PostgreSQL & Redis included
  - Free tier available
  - Zero configuration

- **AWS EC2 (Ansible)** (Full control):
  - Ubuntu 24.04 playbooks
  - Caddy reverse proxy with auto-HTTPS
  - Systemd services
  - Zero-downtime deployments

- **Docker** (Universal):
  - Multi-stage optimized builds
  - docker-compose for development
  - Deploy anywhere

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

### 📦 Additional Features
- PostgreSQL Full-Text Search or OpenSearch
- Internationalization (i18n/l10n)
- Professional email template system

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

**Full documentation**: [https://django-keel.readthedocs.io/](https://django-keel.readthedocs.io/)

### Template Documentation

- [Quick Start](https://django-keel.readthedocs.io/en/latest/getting-started/quickstart/) - Get started in 5 minutes
- [Installation Guide](https://django-keel.readthedocs.io/en/latest/getting-started/installation/) - Detailed setup instructions
- [Features Overview](https://django-keel.readthedocs.io/en/latest/features/overview/) - All available features
- [API Options](https://django-keel.readthedocs.io/en/latest/features/api-options/) - DRF, GraphQL, or both
- [Deployment Guides](https://django-keel.readthedocs.io/en/latest/deployment/kubernetes/) - Kubernetes, AWS EC2, Docker
- [Contributing](https://django-keel.readthedocs.io/en/latest/contributing/development/) - How to contribute

### Generated Project Documentation

Each generated project includes its own comprehensive documentation in the `docs/` directory:

- Getting Started & Installation
- Configuration
- API Development
- Testing Guide
- Deployment (Kubernetes, EC2)
- Architecture Overview
- Monitoring & Observability

## 🎨 Project Types & Examples

Django Keel adapts to your project needs with smart defaults based on project type:

### 🚀 SaaS Application
**Perfect for:** Multi-tenant SaaS products with billing
```yaml
project_type: saas

# Smart defaults:
# - API: DRF for backend
# - Frontend: Next.js for modern SPA
# - Teams: Enabled (multi-tenancy)
# - Stripe: Advanced mode with dj-stripe
# - Background: Celery for emails/async tasks
# - Deployment: Kubernetes for scale
```

### 🔌 API Backend
**Perfect for:** Mobile apps, microservices, headless backends
```yaml
project_type: api

# Smart defaults:
# - API: DRF only
# - Frontend: None
# - Teams: Disabled
# - Stripe: Disabled
# - Background: Celery for async processing
# - Deployment: Render for easy hosting
```

### 🌐 Web Application
**Perfect for:** Traditional Django web apps, MVPs, content sites
```yaml
project_type: web-app

# Smart defaults:
# - API: None (traditional Django views)
# - Frontend: HTMX + Tailwind CSS
# - Teams: Disabled
# - Stripe: Disabled
# - Background: Celery for emails
# - Deployment: Fly.io for global edge
```

### 🏢 Internal Tool
**Perfect for:** Corporate dashboards, admin panels, internal systems
```yaml
project_type: internal-tool

# Smart defaults:
# - API: DRF for flexibility
# - Frontend: HTMX + Tailwind CSS
# - Teams: Enabled (departments/groups)
# - Stripe: Disabled (no billing)
# - Background: Celery for reports
# - Deployment: AWS EC2 (on-premise friendly)
```

### ⚙️ Custom Configuration
**Perfect for:** Unique requirements, maximum control
```yaml
project_type: custom

# You choose everything yourself!
# All options will be presented with sensible defaults
```

### 📝 Real-World Examples

**Startup SaaS:**
```yaml
project_type: saas
use_stripe: true
stripe_mode: advanced
use_teams: true
frontend: nextjs
deployment_targets: kubernetes
```

**Mobile App Backend:**
```yaml
project_type: api
auth_backend: jwt
use_channels: true  # WebSockets
deployment_targets: render
```

**Company Blog:**
```yaml
project_type: web-app
frontend: htmx-tailwind
use_search: postgres-fts
deployment_targets: flyio
```

**Enterprise Dashboard:**
```yaml
project_type: internal-tool
use_teams: true  # Departments
security_profile: strict
deployment_targets: aws-ec2-ansible
```

## 🔄 Updating Your Project

When the template is updated, you can pull in changes:

```bash
cd your-project
copier update
```

Copier will intelligently merge changes, respecting your modifications.

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

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
