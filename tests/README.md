# Django Keel Tests

Comprehensive functional and behavioral test suite for the django-keel template using pytest.

## Overview

This test suite ensures that the django-keel template generates valid, working Django projects across all configuration combinations. All tests are **function-based** (no classes) following pytest best practices for functional and behavioral testing.

Tests are organized into three main categories:

1. **Functional Tests** (`test_generation.py`) - Verify project generation and structure
2. **Behavioral Tests** (`test_features.py`) - Verify feature-specific behavior
3. **Integration Tests** (`test_django_integration.py`) - Verify Django functionality

## Test Structure

```
tests/
├── conftest.py                    # Pytest fixtures and configuration
├── test_generation.py             # Functional tests for project generation
├── test_features.py               # Behavioral tests for features
├── test_django_integration.py     # Django integration tests
└── README.md                      # This file
```

## Running Tests

### Install Dependencies

```bash
pip install -e ".[dev]"
```

### Run All Tests

```bash
pytest
```

### Run Specific Test Categories

```bash
# Run only generation tests
pytest tests/test_generation.py

# Run only feature tests
pytest tests/test_features.py

# Run only integration tests
pytest tests/test_django_integration.py
```

### Run with Coverage

```bash
pytest --cov=. --cov-report=html --cov-report=term-missing
```

### Run in Parallel

```bash
pytest -n auto
```

### Run Specific Tests

```bash
# Run a specific test class
pytest tests/test_features.py::TestCeleryFeature

# Run a specific test method
pytest tests/test_features.py::TestCeleryFeature::test_celery_files_generated_when_enabled
```

## Test Categories

### Functional Tests (test_generation.py)

Tests that verify the basic project generation functionality - all function-based:

- Basic project structure and files
- UV and Poetry configuration
- DRF, GraphQL, both, and none API styles
- None, HTMX, and Next.js frontend options
- Allauth, JWT, and both auth backends

**Example:**
```python
def test_basic_project_generates(generate):
    """Test that a basic project can be generated."""
    project = generate()
    assert project.exists()
    assert (project / "manage.py").exists()
```

### Behavioral Tests (test_features.py)

Tests that verify feature-specific behavior and conditional logic - all function-based:

- Celery task queue configuration
- WebSocket support with Channels
- Stripe payment integration
- Two-factor authentication
- Internationalization
- Redis and no-cache configurations
- Kubernetes and other deployment options
- Local, S3, and other storage backends
- All features enabled together

**Example:**
```python
def test_celery_files_generated_when_enabled(generate):
    """Test that Celery configuration is generated when enabled."""
    project = generate(use_celery=True)
    assert (project / "config/celery.py").exists()
```

### Integration Tests (test_django_integration.py)

Tests that verify Django-specific functionality - all function-based:

- Django management commands
- Database setup
- Static file handling
- URL routing
- Middleware stack
- Custom user model
- Template engine setup

**Example:**
```python
def test_django_check_passes(generate, copier_answers):
    """Test that Django system check passes on generated project."""
    project = generate()
    # ... run manage.py check
    assert result.returncode == 0
```

## Fixtures

### Core Fixtures

- **`template_dir`**: Path to the django-keel template
- **`temp_dir`**: Temporary directory for test outputs
- **`copier_answers`**: Default configuration answers
- **`generate`**: Function to generate projects with custom config
- **`project_with_config`**: Generate project and return path + config

### Usage Example

```python
def test_custom_configuration(generate):
    # Generate project with custom options
    project = generate(
        api_style="drf",
        frontend="htmx-tailwind",
        use_celery=True
    )

    # Verify generated files
    assert (project / "config/celery.py").exists()
```

## Writing New Tests

### Test Naming Conventions

- Test files: `test_*.py`
- Test functions: `test_*`
- **No classes** - all tests are function-based

### Example Test

```python
def test_feature_enabled(generate):
    """Test that feature works when enabled."""
    project = generate(my_feature=True)

    # Verify behavior
    assert (project / "my_feature_file.py").exists()

    settings = project / "config/settings/base.py"
    content = settings.read_text()
    assert "my_feature" in content


def test_feature_disabled(generate):
    """Test that feature is excluded when disabled."""
    project = generate(my_feature=False)

    assert not (project / "my_feature_file.py").exists()
```

## Testing Best Practices

### 1. Use Behavioral Testing

Focus on **what** the feature does, not **how** it's implemented:

```python
# Good: Behavioral
def test_celery_tasks_can_be_defined(self, generate):
    """Test that projects can define Celery tasks."""

# Avoid: Implementation-focused
def test_celery_imports_specific_module(self, generate):
    """Test that celery.py imports X from Y."""
```

### 2. Test Each Feature Independently

```python
def test_stripe_without_celery(self, generate):
    """Test Stripe works independently."""
    project = generate(use_stripe=True, use_celery=False)
    # ...
```

### 3. Test Feature Combinations

```python
def test_stripe_with_celery(self, generate):
    """Test Stripe and Celery work together."""
    project = generate(use_stripe=True, use_celery=True)
    # ...
```

### 4. Verify Both Positive and Negative Cases

```python
def test_feature_enabled(self, generate):
    """Test feature when enabled."""
    # ...

def test_feature_disabled(self, generate):
    """Test feature when disabled."""
    # ...
```

## Continuous Integration

These tests are designed to run in CI/CD pipelines. Example GitHub Actions workflow:

```yaml
- name: Run tests
  run: |
    pip install -e ".[dev]"
    pytest -v --cov=. --cov-report=xml

- name: Upload coverage
  uses: codecov/codecov-action@v3
```

## Troubleshooting

### Tests are slow

Use parallel execution:
```bash
pytest -n auto
```

### Import errors in tests

Ensure dependencies are installed:
```bash
pip install -e ".[dev]"
```

### Generated projects have errors

Check the template files for syntax errors or missing conditionals.

## Contributing

When adding new features to django-keel:

1. Write tests for the new feature
2. Test both enabled and disabled states
3. Test interactions with other features
4. Ensure all tests pass before submitting PR

## License

Same as django-keel template (MIT)
