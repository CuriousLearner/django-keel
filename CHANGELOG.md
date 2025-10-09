# Changelog

All notable changes to django-keel will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive pytest test suite for template generation
  - 49 functional and behavioral tests covering all features
  - Tests for Django integration, features, and project generation
  - All tests are function-based following pytest best practices
- Complete pytest test suite for generated projects
  - Core functionality tests (health checks, URLs, settings, middleware)
  - User authentication and permission tests
  - API endpoint tests (DRF support)
  - Conditional feature tests (Celery, Stripe, Channels, 2FA)
  - All tests are function-based with proper fixtures
- Conditional test file generation based on project configuration
  - test_api.py only when API framework enabled
  - test_tasks.py only when Celery enabled
  - test_billing.py only when Stripe enabled
  - test_websockets.py only when Channels enabled
  - test_2fa.py only when 2FA enabled
- pytest-asyncio conditionally added for Channels WebSocket testing
- Enhanced conftest.py with comprehensive fixtures
- pytest.ini configuration for generated projects
- GitLab CI workflow template (.gitlab-ci.yml)
- Infrastructure validation commands in Justfile
  - validate-yaml: Validate all YAML files
  - validate-compose: Validate docker-compose.yml
  - lint-docker: Lint Dockerfile with hadolint
  - validate-k8s: Validate Kubernetes manifests (when enabled)
  - lint-helm: Lint Helm charts (when enabled)
  - validate-ansible: Validate Ansible playbooks (when enabled)
  - validate-infra: Run all infrastructure validations
- Comprehensive documentation for generated projects
  - CONTRIBUTING.md with development workflow
  - CHANGELOG.md template
  - Testing guide in docs/development/testing.md

### Fixed
- Template rendering issues with Django template tags
- Jinja2 whitespace control in GitHub Actions CI workflow
- Jinja2 whitespace control in docker-compose.yml breaking YAML indentation
- Jinja2 whitespace control in mkdocs.yml breaking YAML structure
- Allauth middleware configuration for Django 5.2
- YAML indentation in CI workflow templates
- Settings import tests with proper .env file setup
- Justfile syntax for install/update commands

### Changed
- Converted all tests from class-based to function-based
- Updated test organization with comment headers instead of classes
- Improved test documentation in tests/README.md

## [0.1.0] - 2025-01-XX

### Added
- Initial release of Django Keel template
- Copier-based template for modern Django projects
- Django 5.2 with Python 3.12/3.13 support
- Multiple package managers (uv, Poetry)
- Multiple API frameworks (DRF, Strawberry GraphQL, both, or none)
- Multiple frontend options (HTMX + Tailwind, Next.js, or none)
- Multiple authentication backends (django-allauth, JWT, or both)
- Optional features:
  - Celery for background tasks
  - Django Channels for WebSockets
  - Stripe payment integration
  - Two-factor authentication (TOTP)
  - Internationalization (i18n)
  - Search (PostgreSQL FTS, OpenSearch)
- Multiple deployment targets:
  - Kubernetes with Helm charts and Kustomize
  - AWS EC2 with Ansible playbooks
- Observability options (minimal, standard, full)
  - Structured logging
  - Sentry error tracking
  - OpenTelemetry instrumentation
  - Prometheus metrics
- Multiple storage backends (local + Whitenoise, AWS S3, GCP GCS, Azure)
- Modern development tooling:
  - Ruff for linting and formatting
  - mypy for type checking
  - pre-commit hooks
  - GitHub Actions / GitLab CI workflows
- Security features:
  - SOPS for encrypted secrets
  - Security profiles (standard, strict)
  - Vulnerability scanning with Trivy
- Comprehensive documentation:
  - MkDocs-based documentation
  - Architecture Decision Records (ADRs)
  - Getting started guides
- Developer experience:
  - Justfile for common tasks
  - Docker Compose for development
  - Split settings (dev, test, prod)
  - .env.example template

[Unreleased]: https://github.com/CuriousLearner/django-keel/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/CuriousLearner/django-keel/releases/tag/v0.1.0
