# Changelog

All notable changes to django-keel will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

#### Core Template Features
- Copier-based template for modern Django projects
- Django 5.2 with Python 3.12/3.13 support
- Multiple package managers (uv, Poetry)
- Multiple API frameworks (DRF, Strawberry GraphQL, both, or none)
- Multiple frontend options (HTMX + Tailwind, Next.js, or none)
- Multiple authentication backends (django-allauth, JWT, or both)
- Split settings structure (base, dev, test, prod)

#### Optional Features
- Background task processing with multiple options:
  - Celery for traditional async tasks with Redis broker
  - Temporal for durable workflows and complex orchestration
  - Support for using both Celery and Temporal together
- Django Channels for WebSockets
- Stripe payment integration
- Two-factor authentication (TOTP)
- Internationalization (i18n) with django-parler
- Search (PostgreSQL FTS, OpenSearch)

#### Deployment
- Kubernetes deployment with Helm charts and Kustomize
- AWS ECS Fargate deployment with Terraform
- Fly.io deployment with automatic global edge distribution
- Render deployment with one-click GitHub integration
- AWS EC2 deployment with Ansible playbooks
- Docker and Docker Compose setup
- Multiple storage backends (local + Whitenoise, AWS S3, GCP GCS, Azure)

#### Observability
- Three observability levels (minimal, standard, full)
- Structured logging with python-json-logger
- Sentry error tracking integration
- OpenTelemetry instrumentation
- Prometheus metrics
- django-alive for standardized health check endpoints (GET /health/)

#### Security
- SOPS for encrypted secrets
- Security profiles (standard, strict)
- django-csp for Content Security Policy
- Rate limiting and brute-force protection

#### Testing
- Comprehensive pytest test suite for template (49 tests)
  - Django integration tests
  - Feature generation tests
  - Project structure validation tests
- Complete pytest test suite for generated projects
  - Core functionality tests
  - User authentication and permission tests
  - API endpoint tests (when DRF enabled)
  - Conditional feature tests (Celery, Stripe, Channels, 2FA)
- Conditional test file generation based on project configuration
- pytest-asyncio for Channels WebSocket testing
- Enhanced conftest.py with comprehensive fixtures
- pytest.ini configuration

#### Development Tools
- Ruff for linting and formatting with comprehensive rule set
- mypy for type checking with django-stubs
- pre-commit hooks for automated quality checks
- pyproject.toml with extensive configuration
- Justfile for common tasks (50+ commands)
- Infrastructure validation commands (YAML, Docker, Helm, Ansible)

#### CI/CD
- GitHub Actions workflow template
- GitLab CI workflow template
- Support for both or either CI provider

#### Documentation
- ReadTheDocs integration with .readthedocs.yaml
- Complete MkDocs documentation structure
- Getting Started guides (Quick Start, Installation, First Project)
- Features documentation (API options, Authentication, Background Tasks, Frontend, Deployment, Observability)
- Deployment guides (Kubernetes, AWS EC2, Docker)
- Contributing guides (Development, Testing, Documentation)
- CONTRIBUTING.md for template contributors
- CONTRIBUTING.md template for generated projects
- CHANGELOG.md template for generated projects
- Testing guide in generated project docs

### Fixed
- Jinja2 whitespace control in GitHub Actions CI workflow
- Jinja2 whitespace control in docker-compose.yml breaking YAML indentation
- Jinja2 whitespace control in mkdocs.yml breaking YAML structure
- Allauth middleware configuration for Django 5.2
- YAML indentation in CI workflow templates
- Settings import tests with proper .env file setup
- Justfile syntax for install/update commands
- All linting issues in test files (14 issues):
  - Removed unused imports
  - Fixed import ordering with isort
  - Fixed type hints to use modern Python 3.12 syntax
  - Removed unused variables

### Changed
- Converted all tests from class-based to function-based
- Updated test organization with comment headers instead of classes

[Unreleased]: https://github.com/CuriousLearner/django-keel/compare/HEAD...HEAD
