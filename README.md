# 🚢 Django Keel

**A versatile, production-ready Django project template for any use case**

Build **SaaS applications**, **API backends**, **web apps**, or **internal tools** with one template.

[![CI](https://github.com/CuriousLearner/django-keel/actions/workflows/ci.yml/badge.svg)](https://github.com/CuriousLearner/django-keel/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Django 6.0](https://img.shields.io/badge/django-6.0-green.svg)](https://www.djangoproject.com/)
[![Documentation](https://readthedocs.org/projects/django-keel/badge/?version=latest)](https://django-keel.readthedocs.io/en/latest/?badge=latest)

> [!NOTE]
> **💼 Available for Hire** — Need help with **Backend Development** or **DevOps**? I specialize in Django, Python, Kubernetes, CI/CD, and cloud infrastructure.
> 📧 Contact: [sanyam@sanyamkhurana.com](mailto:sanyam@sanyamkhurana.com)

Django Keel is a comprehensive Copier template that adapts to your needs—whether you're building a multi-tenant SaaS with billing, a simple API backend, a traditional web app, or an internal corporate tool. One template, infinite possibilities.

**Choose your project type and get smart defaults. Or customize everything yourself.**

## 🚢 What is a "Keel"?

In nautical terms, the **keel** is the structural backbone of a ship—running along the bottom from bow to stern. It provides:

- **Stability** - Prevents the ship from capsizing in rough waters
- **Direction** - Keeps the vessel on course, resisting sideways drift
- **Foundation** - The first part built, upon which the entire ship is constructed

Similarly, **Django Keel** provides the structural foundation for your Django projects:

- **Stability** - Production-ready defaults and battle-tested patterns
- **Direction** - Clear project structure and 12-Factor App compliance
- **Foundation** - A solid base to build upon, whether you're sailing smooth seas or navigating stormy deployments

Just as a ship's keel allows it to sail anywhere, Django Keel enables you to deploy your application to any platform—Kubernetes, AWS, Fly.io, Render, or traditional servers.

<details><summary><strong>Table of Contents</strong></summary>

- [📋 Feature Availability](#-feature-availability)
- [⚙️ Default Configuration](#️-default-configuration)
- [🔒 Security Baseline](#-security-baseline)
- [🔄 Template Updates & Versioning](#-template-updates--versioning)
- [🧪 Compatibility & Support](#-compatibility--support)
- [✨ Features](#-features)
- [🚀 Quick Start](#-quick-start)
- [🧪 Testing](#-testing)
- [📖 Documentation](#-documentation)
- [🎨 Project Types & Examples](#-project-types--examples)
- [🔄 Updating Your Project](#-updating-your-project)
- [🤝 Contributing](#-contributing)
- [📜 License](#-license)
- [🙏 Credits](#-credits)
- [📞 Support](#-support)
</details>

## 📋 Feature Availability

Before diving in, here's what's **included by default**, **optional**, or **planned** (grouped by category):

### Core (Always Included)

| Feature                                | Status      | Notes                                    |
| -------------------------------------- | ----------- | ---------------------------------------- |
| **Django 6.0/5.2 + Python 3.12/3.13/3.14** | ✅ Included | Django 6.0 by default (`django_version`) |
| **Custom User Model**                  | ✅ Included | Email-based authentication               |
| **Split Settings (dev/test/prod)**     | ✅ Included | 12-Factor App ready                      |
| **Docker + Compose**                   | ✅ Included | Local development                        |
| **pytest + coverage**                  | ✅ Included | Coverage gate configurable (default 80%) |
| **ruff + mypy**                        | ✅ Included | Code quality enforced                    |
| **Health/readiness endpoints**         | ✅ Included | `/health/` and `/ready/`                 |

### API & Frontend

| Feature                   | Status      | Notes                                                                                     |
| ------------------------- | ----------- | ----------------------------------------------------------------------------------------- |
| **Django REST Framework** | 📦 Optional | Enable with `api_style: drf` (or `api_style: both` for DRF + GraphQL)                     |
| **Strawberry GraphQL**    | 📦 Optional | Enable with `api_style: graphql-strawberry` (or `api_style: both` for DRF + GraphQL)      |
| **HTMX + Tailwind CSS**   | 📦 Optional | Enable with `frontend: htmx-tailwind`; assets via `frontend_bundling: vite` (default) or `cdn` |
| **Next.js**               | 📦 Optional | `frontend: nextjs` generates a `frontend/README.md` with `npx create-next-app` instructions — you scaffold Next.js yourself |

### Background Tasks & Async

| Feature                          | Status      | Notes                                                       |
| -------------------------------- | ----------- | ----------------------------------------------------------- |
| **Celery (Beat/Flower)**         | 📦 Optional | Enable with `background_tasks: celery` (enabled by default) |
| **Temporal**                     | 📦 Optional | Enable with `background_tasks: temporal`                    |
| **Django Channels (WebSockets)** | 📦 Optional | Enable with `use_channels: true`                            |

**Note on Temporal**: For production, you need Temporal Cloud or a self-hosted Temporal cluster. Keel wires the **client SDK + example worker** with sample workflows/activities, and `docker-compose.yml` includes a local Temporal dev server + UI; **the production Temporal server/Cloud is not provisioned**.

### Observability

| Feature                     | Status      | Notes                                                            |
| --------------------------- | ----------- | ---------------------------------------------------------------- |
| **Structured JSON Logging** | ✅ Included | Always enabled                                                   |
| **Sentry**                  | 📦 Optional | Independent toggle: `use_sentry: true` (enabled by default)      |
| **OpenTelemetry**           | 📦 Optional | `observability_level: full` only                                 |
| **Prometheus metrics**      | 📦 Optional | `observability_level: full` only                                 |

### SaaS Features

| Feature                       | Status      | Notes                              |
| ----------------------------- | ----------- | ---------------------------------- |
| **Multi-tenant teams (RBAC)** | 📦 Optional | Enable with `use_teams: true`                       |
| **Stripe (basic)**            | 📦 Optional | `use_stripe: true` + `stripe_mode: basic`           |
| **Stripe (dj-stripe)**        | 📦 Optional | `use_stripe: true` + `stripe_mode: advanced`        |
| **2FA (TOTP)**                | 📦 Optional | Enable with `use_2fa: true`                         |

### Additional Features

| Feature                      | Status      | Notes                                  |
| ---------------------------- | ----------- | -------------------------------------- |
| **SOPS config scaffold**     | 📦 Optional | `use_sops: true` generates a minimal `.sops.yaml` (bring your own age keys/tooling) |
| **PostgreSQL FTS**           | 📦 Optional | Enable with `use_search: postgres-fts` |
| **OpenSearch**               | 📦 Optional | Enable with `use_search: opensearch`   |
| **i18n/l10n**                | 📦 Optional | Enable with `use_i18n: true`           |

### Deployment Targets

| Feature                           | Status      | Notes                                               |
| --------------------------------- | ----------- | --------------------------------------------------- |
| **Kubernetes (Helm + Kustomize)** | 📦 Optional | Enable with `deployment_targets: [kubernetes]`      |
| **AWS ECS Fargate (Terraform)**   | 📦 Optional | Enable with `deployment_targets: [aws-ecs-fargate]` |
| **Fly.io**                        | 📦 Optional | Enable with `deployment_targets: [flyio]`           |
| **Render**                        | 📦 Optional | Enable with `deployment_targets: [render]`          |
| **AWS EC2 (Ansible)**             | 📦 Optional | Enable with `deployment_targets: [aws-ec2-ansible]` |
| **Docker Compose**                | 📦 Optional | Enable with `deployment_targets: [docker]`          |

`deployment_targets` is a multiselect — pick any combination of the above.

**Legend:**

- ✅ **Included** - Always generated, core to every project
- 📦 **Optional** - Choose during project generation (some enabled by default)
- 🔮 **Planned** - Coming in future releases

### Project Type Defaults (What Changes Automatically)

| Type              | API    | Frontend      | Teams  | Stripe   | Background | Deploy          |
| ----------------- | ------ | ------------- | ------ | -------- | ---------- | --------------- |
| **saas**          | drf    | nextjs        | ✅ on  | advanced | celery     | kubernetes      |
| **api**           | drf    | none          | ❌ off | ❌ off   | celery     | render          |
| **web-app**       | none   | htmx-tailwind | ❌ off | ❌ off   | celery     | flyio           |
| **internal-tool** | drf    | htmx-tailwind | ✅ on  | ❌ off   | celery     | aws-ec2-ansible |
| **custom**        | _pick_ | _pick_        | _pick_ | _pick_   | _pick_     | _pick_          |

## ⚙️ Default Configuration

When you press Enter on every prompt (choosing defaults for `project_type: custom`):

```yaml
# Project Type
project_type: custom # Or: saas, api, web-app, internal-tool

# Tech Stack
python_version: "3.14" # Or: "3.13", "3.12"
django_version: "6.0" # Or: "5.2"
dependency_manager: uv # Or: poetry

# Database & Cache
database: postgresql # Or: sqlite-dev-postgres-prod (SQLite in dev, PostgreSQL in prod)
cache: redis # Or: none

# API & Frontend
api_style: drf # Or: graphql-strawberry, both, none
frontend: none # Or: htmx-tailwind, nextjs
frontend_bundling: vite # Or: cdn (asked only when frontend is htmx-tailwind)

# Background Tasks
background_tasks: celery # Or: temporal, both, none (**celery by default**)
use_channels: false # WebSockets disabled

# Authentication
auth_backend: allauth # Or: jwt, both
use_2fa: false # Two-factor authentication disabled

# Observability
observability_level:
  standard # Or: minimal, full
  # minimal = JSON logs + health endpoints
  # standard = minimal + production JSON logging config
  # full = standard + Prometheus + OTel
use_sentry: true # Sentry error tracking (independent of observability_level)

# Deployment (multiselect — pick any combination)
deployment_targets: [kubernetes] # Or: render, flyio, aws-ecs-fargate, aws-ec2-ansible, docker

# Storage
media_storage: aws-s3 # Or: local-whitenoise, gcp-gcs, azure-storage

# Security
security_profile: standard # Or: strict (adds Content Security Policy via django-csp)
use_sops: false # SOPS config scaffold disabled

# SaaS Features
use_teams: false # Multi-tenancy disabled
use_stripe: false # Stripe disabled
stripe_mode: advanced # Or: basic (asked only when use_stripe is true)

# Additional Features
use_search: none # Or: postgres-fts, opensearch
use_i18n: false # Internationalization disabled

# CI/CD
ci_provider: github-actions # Or: gitlab-ci, both

# License
license: MIT # Or: Apache-2.0, GPL-3.0, BSD-3-Clause, Proprietary
```

**💡 Tip:** Select a [project type](https://django-keel.readthedocs.io/en/latest/getting-started/project-types/) (saas, api, web-app, internal-tool) for smarter defaults!

**Note:** Some "optional" features are enabled by default for production-ready projects (e.g., Celery via `background_tasks: celery`, Sentry via `use_sentry: true`). You can disable them during generation.

## 🔒 Security Baseline

Generated projects ship with production security defaults:

### Included Security Features

- ✅ **HSTS** (HTTP Strict Transport Security) enabled in production, including `SECURE_HSTS_PRELOAD`
- ✅ **SSL redirect** enforced in production
- ✅ **Secure cookies** - Session and CSRF cookies are `Secure`, `HttpOnly`, `SameSite=Lax` in production
- ✅ **Hardening headers** - `X-Frame-Options: DENY`, `SECURE_CONTENT_TYPE_NOSNIFF`
- ✅ **Dependency audit tooling** - `pip-audit` and `safety` installed as dev dependencies
- ✅ **`.env.example`** - Template for environment variables
- ✅ **No secrets in repo** - Environment-based configuration

### security_profile: strict

`security_profile: strict` adds a Content Security Policy via **django-csp** (dependency + middleware), with directives locked down to `'self'` plus minimal allowances for inline styles, data URIs, and HTTPS images.

### Optional: SOPS

`use_sops: true` generates a minimal `.sops.yaml` config scaffold for encrypted secrets. You bring your own age keys and SOPS tooling — no key generation or CI wiring is included.

**🔐 Security Policy**: We follow Django's security best practices. Report issues via [GitHub Issues](https://github.com/CuriousLearner/django-keel/issues).

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

The template's CI generates a project for every combination of Python 3.12/3.13/3.14 and Django 5.2/6.0 and verifies the versions are correctly pinned in the generated `pyproject.toml`.

### Support Policy

- **Python**: Last 2-3 minor versions (currently 3.12, 3.13, 3.14)
- **Django**: Last 2-3 minor versions (currently 5.2, 6.0)

### CI Testing

On every commit, the template repo's CI runs:

- ✅ Template test suite (pytest) on Python 3.12/3.13/3.14
- ✅ Project generation for all project types (saas, api, web-app, internal-tool) with structure checks and a scan for unrendered Jinja syntax
- ✅ Project generation for every Python + Django version combination with version pin checks
- ✅ Code quality on the template repo (ruff, mypy)
- ✅ YAML validation (yamllint) and secret scanning (TruffleHog)
- ✅ Documentation build with link checking

The repo CI does not build Docker images or run the generated project's test suite. Generated projects get their own CI workflow that lints, tests, builds the Docker image, generates an SBOM (Syft), and scans the image with Trivy.

## ✨ Features

### 🎯 Core

- **Django 5.2/6.0** with Python 3.12/3.13/3.14 support
- **uv** or **Poetry** for blazing-fast dependency management
- **[12-Factor App](https://12factor.net/) aligned** - Implements all 12 factors in practice ([docs](docs/12-factor.md))
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
- **Docker + Compose** for local development - Postgres, Redis, and Mailpit out-of-the-box, plus Celery worker/beat, Vite, Temporal dev server, Daphne, or Jaeger depending on your selections

### 🔐 Authentication & Security

- django-allauth with email verification
- JWT authentication (SimpleJWT)
- 2FA support (TOTP)
- Security hardening (HSTS, SSL redirect, secure cookies; CSP via django-csp with `security_profile: strict`)
- SOPS config scaffold for encrypted secrets (optional)

### 🌐 API Options

- **Django REST Framework** with drf-spectacular (OpenAPI 3.0)
- **Strawberry GraphQL** (modern, type-safe)
- CORS configuration
- API versioning ready
- Automatic schema generation

### 🎨 Frontend Options

- **None** (API-only)
- **HTMX + Tailwind CSS** (modern, minimal JS) - _Alpine.js available as optional addition_
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
- **OpenTelemetry** distributed tracing (optional, `observability_level: full`)
- **Prometheus** metrics (optional, `observability_level: full`)
- **Health and readiness endpoints** (always included)

**Note:** OpenTelemetry and Prometheus add overhead and cost. Enable only when needed and configure exporters appropriately.

### 🚀 Deployment

- **Kubernetes** (Enterprise-scale):
  - Minimal Helm chart (`deploy/k8s/helm/<project_slug>/` with deployment, service, ingress, and optional Celery worker templates)
  - Kustomize overlays (dev/prod)
  - PostgreSQL options: **Managed (RDS recommended)** or CloudNativePG operator

**💡 K8s DB Guidance:** Start with managed Postgres (RDS/Cloud SQL/Azure Database) unless you have strong operational reasons for CloudNativePG. Both paths included.

- **AWS ECS Fargate** (Serverless containers):

  - No EC2 instance management
  - Application Load Balancer with auto-scaling
  - Multi-AZ high availability
  - Terraform infrastructure-as-code
  - `deploy.sh` helper script and a GitHub Actions deploy workflow (`deploy-ecs.yml`) using OIDC — no long-lived AWS keys

- **Fly.io** (Global edge):

  - Deploy close to users worldwide
  - Automatic HTTPS & SSL
  - PostgreSQL & Redis included
  - Multi-region deployment
  - Helper scripts (`deploy.sh`, `setup_env.sh`, `manage_db.sh`) and a GitHub Actions deploy workflow (`deploy-flyio.yml`)

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
  - Curated rule set (pycodestyle, pyflakes, isort, bugbear, pyupgrade, flake8-django, and more)
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
  _A focused set of commands (extendable) for all common workflows._
- **Docker Compose** for local development
- **VS Code Devcontainer** support
- **MkDocs Material** documentation
- **Infrastructure validation** just recipes: `validate-yaml`, `lint-docker`, `validate-compose`, `validate-k8s`, `lint-helm`, `validate-ansible`, or all at once with `just validate-infra`

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
  - `python manage.py init_feature_flags` seeds default flags/switches/samples

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
│   ├── core/                 # Core functionality (health checks, feature flags, etc.)
│   ├── users/                # Custom user model
│   ├── api/                  # API endpoints (if selected)
│   ├── teams/                # Multi-tenant teams (if selected)
│   └── billing/              # Stripe billing (if selected)
├── config/                    # Django configuration
│   ├── settings/             # Split settings
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── temporal_app/              # Temporal workflows/activities (if selected)
├── frontend/                  # Frontend assets (if selected)
├── templates/                 # Django templates
├── static/                    # Static files
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
├── .env.example               # Environment variable template
├── Dockerfile                 # Production image
├── docker-compose.yml         # Development environment
├── Justfile                   # Task runner
├── Procfile                   # Process types (12-factor)
├── release.sh                 # Release-phase script (migrations, etc.)
├── pytest.ini                 # Test configuration
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

# Create and run migrations (first run generates migrations for optional apps like teams/billing)
just makemigrations
just migrate

# Create superuser
just createsuperuser

# Start development server
just dev
```

Visit:

- Application: http://localhost:8000
- Admin: http://localhost:8000/admin/
- API Docs: http://localhost:8000/api/schema/swagger/ _(only when `api_style` is `drf` or `both`)_
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

Each generated project includes starter documentation in the `docs/` directory (MkDocs):

- Home (`index.md`)
- Installation (`getting-started/installation.md`)
- Testing (`development/testing.md`)
- Architecture Overview (`architecture/overview.md`)

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
deployment_targets: [kubernetes]
```

**Mobile App Backend:**

```yaml
project_type: api
auth_backend: jwt
use_channels: true # WebSockets for real-time features
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
use_teams: true # Departments/groups
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
