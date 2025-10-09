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

#### Background Task Processing
- **Celery** - Traditional async tasks
  - Redis broker for task queue
  - Celery Beat for periodic tasks (cron-like scheduling)
  - Flower for monitoring and management
  - django-celery-beat for database-backed schedules
  - django-celery-results for result persistence
  - Best for: Simple async tasks, emails, image processing, high-volume jobs

- **Temporal** - Durable workflow orchestration (NEW)
  - Temporal Python SDK (temporalio>=1.6.0)
  - django-temporalio integration
  - Example workflows: UserOnboardingWorkflow, BatchProcessingWorkflow
  - Example activities: send_email, process_user (with Django ORM support)
  - Management command: run_temporal_worker
  - Docker Compose services: temporal, temporal-ui, temporal-worker
  - Temporal UI for workflow monitoring (port 8080)
  - Best practices: sync_to_async for Django ORM, single dataclass arguments
  - Best for: Complex multi-step workflows, long-running processes, saga patterns
  - Comprehensive README with usage examples (300+ lines)

- **Both** - Use Celery AND Temporal together
  - Celery for simple, high-volume tasks
  - Temporal for complex workflow orchestration
  - Independent configuration and scaling
  - Best for: Large applications with diverse background task needs

#### Other Optional Features
- Django Channels for WebSockets
- Stripe payment integration with billing app
- Two-factor authentication (TOTP) with django-otp
- Internationalization (i18n) with django-parler
- Search (PostgreSQL Full-Text Search, OpenSearch)

#### Deployment Options (6 platforms)
- **Kubernetes** - Enterprise-scale orchestration
  - Helm charts for package management
  - Kustomize overlays for environment-specific configs (dev/staging/prod)
  - CloudNativePG operator for PostgreSQL
  - Traefik + cert-manager for automatic HTTPS
  - Horizontal Pod Autoscaling
  - ArgoCD GitOps ready

- **AWS ECS Fargate** - Serverless containers
  - No EC2 instance management required
  - Application Load Balancer with auto-scaling
  - Multi-AZ high availability deployment
  - CloudWatch logging and monitoring
  - Terraform infrastructure-as-code
  - Comprehensive deployment guide (400+ lines)

- **Fly.io** - Global edge deployment
  - Deploy close to users worldwide for low latency
  - Automatic HTTPS and SSL certificates
  - PostgreSQL and Redis included
  - Free tier: 3 VMs, 3GB DB, 160GB bandwidth
  - Multi-region deployment support
  - fly.toml configuration file
  - Complete deployment guide (500+ lines)

- **Render** - Platform-as-Service
  - One-click deployment from GitHub
  - Automatic deploys on git push
  - PostgreSQL and Redis included
  - Automatic SSL certificates
  - Free tier available (spins down after 15 min)
  - render.yaml blueprint for infrastructure-as-code
  - Build script for automated setup
  - Comprehensive deployment guide (450+ lines)

- **AWS EC2 (Ansible)** - Full control VMs
  - Ubuntu 24.04 automated provisioning
  - Caddy reverse proxy with auto-HTTPS
  - Systemd service management
  - Zero-downtime deployments

- **Docker** - Universal containers
  - Multi-stage optimized Dockerfile
  - docker-compose.yml for local development
  - Deploy to any container platform

- **Storage Options**:
  - Local storage with Whitenoise (compressed, cached)
  - AWS S3 with boto3
  - Google Cloud Storage
  - Azure Blob Storage

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

#### Documentation (2,700+ lines)
- ReadTheDocs integration with .readthedocs.yaml
- Complete MkDocs documentation structure with Material theme
- Getting Started guides:
  - Quick Start (5-minute setup)
  - Installation (detailed)
  - First Project (step-by-step)
- Features documentation:
  - API Options (DRF vs GraphQL comparison with examples)
  - Authentication (django-allauth, JWT, or both)
  - Background Tasks (Celery vs Temporal decision guide)
  - Frontend Options (HTMX+Tailwind, Next.js)
  - Deployment (6 platforms with comparison tables)
  - Observability (logging, tracing, metrics)
- Deployment guides:
  - Kubernetes (Helm + Kustomize)
  - AWS ECS Fargate (Terraform, 400+ lines)
  - Fly.io (Global edge, 500+ lines)
  - Render (PaaS, 450+ lines)
  - AWS EC2 (Ansible)
  - Docker
  - Platform comparison by use case, cost, and complexity
  - Migration guides between platforms
- Background Tasks documentation:
  - Celery vs Temporal comparison table
  - When to use each platform
  - Django ORM async safety patterns
  - Testing workflows and activities
- Contributing guides:
  - Development workflow
  - Testing strategy
  - Documentation standards
- CONTRIBUTING.md for template contributors
- CONTRIBUTING.md template for generated projects
- CHANGELOG.md template for generated projects
- Testing guide in generated project docs
- Temporal app README with comprehensive examples

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

#### Breaking Changes
- **Background tasks configuration**: Replaced `use_celery: bool` with `background_tasks: str`
  - Old: `use_celery: true` or `use_celery: false`
  - New: `background_tasks: "celery" | "temporal" | "both" | "none"`
  - Migration: `use_celery: true` → `background_tasks: "celery"`
  - Migration: `use_celery: false` → `background_tasks: "none"`
  - All template files updated to use new variable
  - All tests updated to use new variable
  - Celery configuration files now conditionally generated

#### Other Changes
- Converted all tests from class-based to function-based
- Updated test organization with comment headers instead of classes
- Enhanced deployment documentation with platform comparisons
- Added decision guides for choosing deployment platforms
- Expanded example configurations for different project types

[Unreleased]: https://github.com/CuriousLearner/django-keel/compare/HEAD...HEAD
