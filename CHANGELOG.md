# Changelog

All notable changes to django-keel will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

#### Core Features
- Copier-based Django project template with flexible configuration options
- Django 5.2/6.0 with Python 3.12/3.13/3.14 support
- Multiple package managers: uv, Poetry
- Split settings structure: base, dev, test, prod
- 12-Factor App compliance with environment-based configuration

#### API & Frontend Options
- API frameworks: Django REST Framework, Strawberry GraphQL, both, or none
- Frontend: HTMX + Tailwind CSS, Next.js, or headless
- Frontend bundling for HTMX+Tailwind: Vite (production-ready) or CDN (simple)
- Authentication: django-allauth, JWT, or both

#### Background Task Processing
- **Celery**: Traditional async tasks with Redis broker and Celery Beat
- **Temporal**: Durable workflow orchestration for complex multi-step processes
- **Both**: Use Celery and Temporal together for different use cases
- **None**: Skip background task setup entirely

#### Deployment Platforms
- **Kubernetes**: Enterprise-scale with Helm charts and Kustomize overlays
- **AWS ECS Fargate**: Serverless containers with Terraform
- **Fly.io**: Global edge deployment with automatic SSL
- **Render**: One-click PaaS deployment from GitHub
- **AWS EC2**: Full control VMs with Ansible provisioning
- **Docker**: Universal container deployment with docker-compose

#### Optional Features
- Django Channels for WebSockets
- Stripe payment integration with billing app
- Two-factor authentication with django-otp
- Internationalization with django-parler
- Search: PostgreSQL Full-Text or OpenSearch
- Storage: Local (Whitenoise), AWS S3, GCS, or Azure

#### Observability
- Three levels: minimal, standard, full
- Structured JSON logging
- Sentry error tracking
- OpenTelemetry instrumentation
- Prometheus metrics
- Health check endpoints with django-alive

#### Security
- SOPS for encrypted secrets management
- Security profiles: standard or strict
- Content Security Policy with django-csp
- Rate limiting and brute-force protection

#### Development Tools
- Ruff for linting and formatting
- mypy for type checking
- pre-commit hooks
- pytest test suite
- Justfile with 50+ common tasks
- Infrastructure validation commands

#### CI/CD
- GitHub Actions workflow template
- GitLab CI workflow template
- Python + Django version matrix testing to verify all supported combinations

#### Version Support
- Django 5.2 and 6.0 support
- Python 3.12, 3.13, and 3.14 support

#### Documentation
- ReadTheDocs integration with MkDocs Material theme
- Getting started guides
- Feature comparison tables
- Deployment guides for all platforms
- Background tasks decision guide
- Contributing guidelines

### Changed
- Background tasks configuration: `background_tasks` parameter with options: "celery", "temporal", "both", or "none"
- `copier.yml` UX enhancements:
  - Choice fields now display user-friendly labels instead of raw values
  - `project_name` and `project_description` use placeholders with non-empty validators
  - `deployment_targets` converted to multiselect field

### Fixed
- Docker development on Linux: Added named volume for `.venv` to prevent permission errors due to UID mismatch between host and container
- Clarified development workflow documentation to distinguish Docker vs local development approaches

[Unreleased]: https://github.com/CuriousLearner/django-keel/compare/HEAD...HEAD
