# Contributing to Django Keel

Thank you for your interest in contributing to Django Keel!

## Development Setup

### Prerequisites

- Python 3.12+
- [Copier](https://copier.readthedocs.io/)
- Git

### Setup

```bash
# Clone the repository
git clone https://github.com/CuriousLearner/django-keel.git
cd django-keel

# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks (optional but recommended)
pip install pre-commit
pre-commit install
```

## Code Quality Standards

We maintain high code quality with automated tools:

### Linting and Formatting

```bash
# Check code with ruff
ruff check .

# Auto-fix linting issues
ruff check . --fix

# Format code
ruff format .
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov

# Run specific test
pytest tests/test_generation.py::test_basic_project_generates
```

All tests must pass before merging. We currently have 49 tests with 100% pass rate.

## Making Changes

### Workflow

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** in the `template/` directory

3. **Test your changes:**
   ```bash
   # Run the test suite
   pytest

   # Generate a test project manually
   copier copy . /tmp/test-project
   cd /tmp/test-project
   cat .env.example > .env
   docker compose up -d
   just test
   ```

4. **Lint and format:**
   ```bash
   ruff check . --fix
   ruff format .
   ```

5. **Commit using conventional commits:**
   ```bash
   git commit -m "feat: add awesome feature"
   ```

6. **Push and create a pull request**

### Commit Message Format

We use [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `test:` - Test additions or changes
- `refactor:` - Code refactoring
- `chore:` - Maintenance tasks

Examples:
```bash
git commit -m "feat: add GitLab CI support"
git commit -m "fix: resolve YAML indentation in docker-compose"
git commit -m "docs: update installation guide"
```

## Project Structure

```
django-keel/
├── tests/              # Test suite (49 tests)
│   ├── test_django_integration.py
│   ├── test_features.py
│   └── test_generation.py
├── template/           # Copier template files (80+ files)
├── CHANGELOG.md        # Version history
├── pyproject.toml      # Ruff & pytest config
├── requirements-dev.txt # Development dependencies
└── copier.yml         # Template configuration
```

## Testing Guidelines

### Writing Tests

- All tests must be function-based (not class-based)
- Use descriptive test names: `test_<what>_<condition>`
- Add docstrings to explain what the test verifies
- Use fixtures from `conftest.py`

Example:
```python
def test_postgresql_database_configured(generate):
    """Test PostgreSQL database configuration."""
    project = generate(database="postgresql")

    settings = project / "config/settings/base.py"
    content = settings.read_text()

    assert "DATABASES" in content
    assert 'env.db("DATABASE_URL")' in content
```

### Testing Generated Projects

To test generated projects manually:

```bash
# Basic project
copier copy . /tmp/test-basic

# With specific features
copier copy . /tmp/test-full \
  --data api_style=both \
  --data background_tasks=both \
  --data deployment_targets=kubernetes,ecs,flyio

# Test the generated project
cd /tmp/test-full
cat .env.example > .env
docker compose up -d
# Verify files, run tests, etc.
```

## Pull Request Process

### Before Submitting

- ✅ All tests pass (`pytest`)
- ✅ Code is linted (`ruff check .`)
- ✅ Code is formatted (`ruff format .`)
- ✅ CHANGELOG.md is updated
- ✅ Documentation is updated if needed
- ✅ Commit messages follow conventional commits

### PR Description

Include:
- What changes were made
- Why the changes were needed
- How to test the changes
- Any breaking changes

### Review Process

1. Maintainers review your PR
2. Address feedback if any
3. Once approved, maintainer merges
4. Your contribution is included in next release!

## Code Style Guidelines

- **Line length:** 100 characters
- **Imports:** Sorted with isort (handled by ruff)
- **Type hints:** Use where appropriate
- **Docstrings:** Required for all functions
- **Django conventions:** Follow Django coding style

## Questions or Need Help?

- 📝 Open an issue for bugs or feature requests
- 💬 Start a discussion for questions
- 📚 Check existing issues and discussions first

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
