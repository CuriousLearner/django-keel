# 🚢 Django Keel

**A versatile, production-ready Django project template for any use case**

Build **SaaS applications**, **API backends**, **web apps**, or **internal tools** with one template.

[![CI](https://github.com/CuriousLearner/django-keel/actions/workflows/ci.yml/badge.svg)](https://github.com/CuriousLearner/django-keel/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Django 5.2](https://img.shields.io/badge/django-5.2-green.svg)](https://www.djangoproject.com/)
[![Documentation](https://readthedocs.org/projects/django-keel/badge/?version=latest)](https://django-keel.readthedocs.io/en/latest/?badge=latest)

Django Keel is a comprehensive Copier template that adapts to your needs—whether you're building a multi-tenant SaaS with billing, a simple API backend, a traditional web app, or an internal corporate tool. One template, infinite possibilities.

**Choose your project type and get smart defaults. Or customize everything yourself.**

## 📋 Feature Availability

Before diving in, here's what's **included by default**, **optional**, or **planned** (grouped by category):

### Core (Always Included)
| Feature | Status | Notes |
|---------|--------|-------|
| **Django 5.2 + Python 3.12/3.13** | ✅ Included | Always enabled |
| **Custom User Model** | ✅ Included | Email-based authentication |
| **Split Settings (dev/test/prod)** | ✅ Included | 12-Factor App ready |
| **Docker + Compose** | ✅ Included | Local development |
| **pytest + coverage** | ✅ Included | Coverage gate configurable (default 80%) |
| **ruff + mypy** | ✅ Included | Code quality enforced |
| **Health/readiness endpoints** | ✅ Included | `/health/` and `/ready/` |

### API & Frontend
| Feature | Status | Notes |
|---------|--------|-------|
| **Django REST Framework** | 📦 Optional | Enable with `api: drf` |
| **Strawberry GraphQL** | 📦 Optional | Enable with `api: graphql` |
| **HTMX + Tailwind CSS** | 📦 Optional | Enable with `frontend: htmx-tailwind` |
| **Next.js** | 📦 Optional | Enable with `frontend: nextjs` |

### Background Tasks & Async
| Feature | Status | Notes |
|---------|--------|-------|
| **Celery (Beat/Flower)** | 📦 Optional | Enable with `background_tasks: celery` (enabled by default) |
| **Temporal** | 📦 Optional | Enable with `background_tasks: temporal` |
| **Django Channels (WebSockets)** | 📦 Optional | Enable with `use_channels: true` |

**Note on Temporal**: Requires Temporal Cloud or a self-hosted Temporal cluster. Keel wires the **client SDK + example worker** with sample workflows/activities; **the Temporal server/Cloud is not provisioned**.

### Observability
| Feature | Status | Notes |
|---------|--------|-------|
| **Structured JSON Logging** | ✅ Included | Always enabled |
| **Sentry** | 📦 Optional | `observability: standard` or `full` (enabled by default) |
| **OpenTelemetry** | 📦 Optional | `observability: full` only |
| **Prometheus metrics** | 📦 Optional | `observability: full` only |

### SaaS Features
| Feature | Status | Notes |
|---------|--------|-------|
| **Multi-tenant teams (RBAC)** | 📦 Optional | Enable with `use_teams: true` |
| **Stripe (basic)** | 📦 Optional | Enable with `use_stripe: basic` |
| **Stripe (dj-stripe)** | 📦 Optional | Enable with `use_stripe: advanced` |
| **2FA (TOTP)** | 📦 Optional | Enable with `use_2fa: true` |

### Additional Features
| Feature | Status | Notes |
|---------|--------|-------|
| **SOPS (encrypted secrets)** | 📦 Optional | Enable with `use_sops: true` |
| **PostgreSQL FTS** | 📦 Optional | Enable with `use_search: postgres-fts` |
| **OpenSearch** | 📦 Optional | Enable with `use_search: opensearch` |
| **i18n/l10n** | 📦 Optional | Enable with `use_i18n: true` |

### Deployment Targets
| Feature | Status | Notes |
|---------|--------|-------|
| **Kubernetes (Helm + Kustomize)** | 📦 Optional | Enable with `deployment_targets: [kubernetes]` |
| **AWS ECS Fargate (Terraform)** | 📦 Optional | Enable with `deployment_targets: [ecs]` |
| **Fly.io** | 📦 Optional | Enable with `deployment_targets: [flyio]` |
| **Render** | 📦 Optional | Enable with `deployment_targets: [render]` |
| **AWS EC2 (Ansible)** | 📦 Optional | Enable with `deployment_targets: [aws-ec2-ansible]` |

**Legend:**
- ✅ **Included** - Always generated, core to every project
- 📦 **Optional** - Choose during project generation (some enabled by default)
- 🔮 **Planned** - Coming in future releases

### Project Type Defaults (What Changes Automatically)

| Type | API | Frontend | Teams | Stripe | Background | Deploy |
|------|-----|----------|-------|--------|-----------|---------|
| **saas** | drf | nextjs | ✅ on | advanced | celery | kubernetes |
| **api** | drf | none | ❌ off | ❌ off | celery | render |
| **web-app** | none | htmx-tailwind | ❌ off | ❌ off | celery | flyio |
| **internal-tool** | drf | htmx-tailwind | ✅ on | ❌ off | celery | aws-ec2-ansible |
| **custom** | *pick* | *pick* | *pick* | *pick* | *pick* | *pick* |

## ⚙️ Default Configuration

When you press Enter on every prompt (choosing defaults for `project_type: custom`):

```yaml
# Project Type
project_type: custom                # Or: saas, api, web-app, internal-tool

# Dependency Management
dependency_manager: uv              # Or: poetry
python_version: "3.13"              # Or: "3.12"

# Database & Cache
database: postgresql                # Production-ready database
db_managed: true                    # Use managed DB (RDS/Cloud SQL recommended)
cache: redis                        # Or: none

# API & Frontend
api: drf                            # Or: graphql, both, none
frontend: none                      # Or: htmx-tailwind, nextjs

# Authentication
auth: allauth                       # Or: jwt, both
use_2fa: false                      # Two-factor authentication disabled

# Background Tasks
background_tasks: celery            # Or: temporal, both, none (optional, **enabled by default**)
use_channels: false                 # WebSockets disabled

# Observability
observability: standard             # Or: minimal, full
                                    # minimal = JSON logs + health
                                    # standard = minimal + Sentry
                                    # full = standard + Prometheus + OTel

# SaaS Features
use_teams: false                    # Multi-tenancy disabled
use_stripe: false                   # Or: basic, advanced

# Additional Features
use_search: none                    # Or: postgres-fts, opensearch
use_i18n: false                     # Internationalization disabled
use_sops: false                     # Encrypted secrets disabled

# Security
security_profile: standard          # Or: strict (see docs for differences)

# Storage
media_storage: aws-s3               # Or: gcs, azure, whitenoise-only

# Deployment
deployment_targets: [kubernetes]    # Or: [aws-ec2-ansible, ecs, flyio, render]

# CI/CD
ci_provider: github-actions         # Or: gitlab-ci, both
```

**💡 Tip:** Select a [project type](https://django-keel.readthedocs.io/en/latest/getting-started/project-types/) (saas, api, web-app, internal-tool) for smarter defaults!

**Note:** Some "optional" features are enabled by default for production-ready projects (e.g., Celery, Sentry via `observability: standard`). You can disable them during generation.

## 🔒 Security Baseline

Django Keel enforces production security out of the box:

### Included Security Features

- ✅ **`python manage.py check --deploy`** runs in CI
- ✅ **HSTS** (HTTP Strict Transport Security) enabled in production
- ✅ **Secure cookies** (`SECURE_*` flags) in production
- ✅ **SSL redirect** enforced in production
- ✅ **CSP headers** (Content Security Policy) with sane defaults
- ✅ **Admin hardening** - Custom admin URL, staff-only access
- ✅ **Rate limiting** - Optional with django-ratelimit
- ✅ **Brute-force protection** - Optional with django-axes
- ✅ **SOPS (age)** - Encrypted secrets management (optional)
- ✅ **`.env.example`** - Template for environment variables
- ✅ **No secrets in repo** - Environment-based configuration

### GitHub Security (when using GitHub Actions)

- OIDC to cloud providers (no long-lived keys)
- Dependabot enabled for dependency updates
- Secret scanning enabled
- Branch protection recommended

### security_profile: strict

When you enable `security_profile: strict`, additional hardening is applied:

- **CSP locked to 'self'** - Content Security Policy blocks all external resources
- **Admin path randomized** - Admin URL is generated randomly (not `/admin/`)
- **Session age shortened** - Sessions expire faster (15 min vs 2 weeks)
- **HTTPS-only cookies** - All cookies require HTTPS, no fallback
- **SECURE_HSTS_PRELOAD** - Enabled for HSTS preload list submission
- **Stricter CORS** - No wildcards, explicit origins only
- **Additional headers** - X-Frame-Options, X-Content-Type-Options, Referrer-Policy
- **Permissions-Policy** - Restrictive policy (e.g., `camera=(), geolocation=(), microphone=()`)

### Production Checks

Every generated project includes:

```bash
# Security audit
just security-check

# This runs:
# - python manage.py check --deploy
# - pip-audit (dependency vulnerabilities)
# - safety check (known security issues)
```

**🔐 Security Policy**: We follow Django's security best practices and respond to vulnerabilities within 24 hours. Report issues to security@django-keel (coming soon).

## 🔄 Template Updates & Versioning

### How Updates Work

Django Keel uses **semantic versioning** (SemVer):

- **MAJOR** (2.0.0) - Breaking changes requiring manual intervention
- **MINOR** (1.1.0) - New features, backward compatible
- **PATCH** (1.0.1) - Bug fixes, backward compatible

Your project tracks the template version in `.copier-answers.yml`:

```yaml
_commit: a1b2c3d
_src_path: gh:CuriousLearner/django-keel
```

### Updating Your Project

```bash
cd your-project

# Create a backup branch before updating
git switch -c pre-update

# Run update
copier update

# If issues arise, you can rollback
git reset --hard
```

Copier will:
1. Show you a diff of changes
2. Let you selectively accept/reject changes
3. Preserve your customizations
4. Handle merge conflicts intelligently

### Breaking Changes

We mark breaking changes in the **CHANGELOG** with a `⚠️ BREAKING` label and provide migration guides.

**Policy**: We aim for **no more than 2 major versions per year** to minimize disruption.

## 🧪 Compatibility & Support

### Tested Combinations

We test Django Keel against:

| Python | Django | Status |
|--------|--------|--------|
| 3.12 | 5.1 | ✅ Tested |
| 3.12 | 5.2 | ✅ Tested |
| 3.13 | 5.1 | ✅ Tested |
| 3.13 | 5.2 | ✅ Tested |

### Support Policy

- **Python**: Last 2 minor versions (currently 3.12, 3.13)
- **Django**: Last 2 minor versions (currently 5.1, 5.2)
- **LTS versions** get priority bug fixes
- **Security patches** backported for 1 year

### CI Testing

Every commit is tested against:
- ✅ All Python + Django combinations
- ✅ Template generation with all project types
- ✅ Docker builds
- ✅ Code quality (ruff, mypy)
- ✅ Security checks (pip-audit, safety)
- ✅ SBOM generation (Syft)
- ✅ Container image scanning (Trivy)

## ✨ Features

### 🎯 Core
- **Django 5.2** with Python 3.12/3.13
- **uv** or **Poetry** for blazing-fast dependency management
- **[12-Factor App](https://12factor.net/) compliant** - Fully adheres to all 12 factors ([docs](docs/12-factor.md))
  - Single codebase with multiple deploys
  - Explicit dependencies with lock files
  - Config in environment variables
  - Backing services as attached resources
  - Separate build/release/run stages (`Procfile`, `release.sh`)
  - Stateless processes
  - Port binding export
  - Horizontal scalability via process model
  - Fast startup, graceful shutdown
  - Dev/prod parity
  - Logs as event streams
  - Admin processes as one-off tasks
- **Custom User Model** from day one
- **Split Settings** (base/dev/test/prod)
- **Docker + Compose** for local development - Postgres, Redis, and Mailpit included out-of-the-box

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
- **HTMX + Tailwind CSS** (modern, minimal JS) - *Alpine.js available as optional addition*
- **Next.js** (full-stack React)

### ⚡ Async & Background Tasks
- **Celery** - Traditional async tasks (emails, reports, high-volume processing)
- **Temporal** - Durable workflows (onboarding, payment flows, long-running processes)
- **Both** - Use Celery AND Temporal together
- Celery Beat for periodic tasks
- Flower for monitoring
- **Django Channels** for WebSockets (optional)

### 📊 Observability
- **Structured JSON Logging** (always included)
- **Sentry** error tracking (optional)
- **OpenTelemetry** distributed tracing (optional, `observability: full`)
- **Prometheus** metrics (optional, `observability: full`)
- **Health and readiness endpoints** (always included)

**Note:** OpenTelemetry and Prometheus add overhead and cost. Enable only when needed and configure exporters appropriately.

### 🚀 Deployment
- **Kubernetes** (Enterprise-scale):
  - Helm charts
  - Kustomize overlays (dev/staging/prod)
  - PostgreSQL options: **Managed (RDS recommended)** or CloudNativePG operator
  - Traefik + cert-manager for ingress
  - Horizontal Pod Autoscaling
  - ArgoCD ready

**💡 K8s DB Guidance:** Start with managed Postgres (RDS/Cloud SQL/Azure Database) unless you have strong operational reasons for CloudNativePG. Both paths included.

- **AWS ECS Fargate** (Serverless containers):
  - No EC2 instance management
  - Application Load Balancer with auto-scaling
  - Multi-AZ high availability
  - Terraform infrastructure-as-code

- **Fly.io** (Global edge):
  - Deploy close to users worldwide
  - Automatic HTTPS & SSL
  - PostgreSQL & Redis included
  - Free tier available
  - Multi-region deployment

- **Render** (Platform-as-a-Service, PaaS):
  - One-click deployment from GitHub
  - Auto-deploy on git push
  - PostgreSQL & Redis included
  - Free and paid tiers
  - Zero configuration

- **AWS EC2 (Ansible)** (Full control):
  - Ubuntu 24.04 playbooks
  - Caddy reverse proxy with auto-HTTPS
  - Systemd services
  - Zero-downtime deploys (socket activation/rolling restart)

- **Docker** (Universal):
  - Multi-stage optimized builds
  - docker-compose for development
  - Deploy anywhere

### 🧪 Developer Experience
- **ruff** for linting and formatting (10-100x faster)
  - Comprehensive rule set (13+ categories)
  - 100-character line length
  - Modern Python 3.12+ type hints
- **mypy + django-stubs** for type checking
- **pytest** with coverage reporting (coverage gate configurable, default 80%)
- **pre-commit** hooks for automated quality checks
- **Just** task runner with essential commands:
  ```bash
  just dev            # Start development server
  just test           # Run test suite
  just lint           # Lint and format code
  just migrate        # Run migrations
  just createsuperuser # Create admin user
  ```
  *A focused set of commands (extendable) for all common workflows.*
- **Docker Compose** for local development
- **VS Code Devcontainer** support
- **MkDocs Material** documentation
- **Infrastructure validation** (YAML, Docker Compose, Helm, Ansible)

### 💼 SaaS Features (Optional)
- **Multi-tenant teams (RBAC)** - Full team management system
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

> **Next.js option?** Install Node.js **20 LTS** (or later) and pnpm/npm/yarn.

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
- API Docs: http://localhost:8000/api/schema/swagger/ *(only when `api != none`)*
- Mailpit: http://localhost:8025 (email testing)

## 🧪 Testing

The template includes comprehensive test suites for both the template itself and generated projects.

### Template Tests

```bash
# Run all template tests
pytest

# Run with coverage
pytest --cov

# Comprehensive test suite covering:
# - Django integration and compatibility
# - Feature generation for all project types
# - Project structure validation
# - Conditional file generation based on selections
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
use_stripe: advanced          # Combines use_stripe + stripe_mode
use_teams: true
frontend: nextjs
deployment_targets: [kubernetes]
```

**Mobile App Backend:**
```yaml
project_type: api
auth: jwt
use_channels: true            # WebSockets for real-time features
deployment_targets: [render]
```

**Company Blog:**
```yaml
project_type: web-app
frontend: htmx-tailwind
use_search: postgres-fts
deployment_targets: [flyio]
```

**Enterprise Dashboard:**
```yaml
project_type: internal-tool
use_teams: true               # Departments/groups
security_profile: strict
deployment_targets: [aws-ec2-ansible]
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
