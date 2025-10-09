# Testing Django Keel

This guide covers testing the Django Keel template itself.

## Running Template Tests

Django Keel has a comprehensive test suite with 49 tests.

### Run All Tests

```bash
pytest
```

### Run with Coverage

```bash
pytest --cov
```

### Run Specific Test

```bash
pytest tests/test_generation.py::test_basic_project_generates
```

## Test Categories

### Django Integration Tests (16 tests)

Tests that verify Django configuration in generated projects:

- Settings import correctly
- Database configuration
- Middleware setup
- URL routing
- Templates configuration

### Feature Tests (17 tests)

Tests for optional features:

- Background tasks (Celery, Temporal, both)
- Channels/WebSockets
- Stripe integration
- 2FA setup
- i18n configuration
- Caching options
- Deployment targets (Kubernetes, ECS, Fly.io, Render, EC2)

### Generation Tests (16 tests)

Tests for project generation:

- Valid Python syntax
- Valid YAML files
- Correct project structure
- Package manager configuration
- API framework setup
- Frontend options
- Authentication backends

## Writing Tests

All tests must be function-based (not class-based):

```python
def test_feature_enabled(generate):
    """Test that feature is configured when enabled."""
    project = generate(use_feature=True)

    settings = project / "config/settings/base.py"
    content = settings.read_text()

    assert "FEATURE_CONFIG" in content
```

### Using Fixtures

```python
def test_with_config(project_with_config):
    """Test using project_with_config fixture."""
    project, config = project_with_config(
        api_style="drf",
        background_tasks="celery"
    )

    assert (project / "config/celery.py").exists()
```

## Test Requirements

- All tests must pass
- Use descriptive test names
- Add docstrings
- No class-based tests
- Use existing fixtures from `conftest.py`

## Continuous Integration

Tests run automatically on:

- Pull requests
- Pushes to main branch
- Using GitHub Actions

See `.github/workflows/test.yml` for CI configuration.
