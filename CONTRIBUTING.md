# Contributing to Django Keel

Thank you for your interest in contributing to Django Keel!

## Development Setup

1. Fork and clone the repository:
```bash
git clone https://github.com/CuriousLearner/django-keel.git
cd django-keel
```

2. Install Copier:
```bash
pipx install copier
```

3. Test the template locally:
```bash
copier copy . ../test-project
cd ../test-project
# Test the generated project
```

## Making Changes

1. Create a feature branch:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes in the `template/` directory

3. Test your changes:
```bash
# Generate a test project
copier copy . ../test-project --force

# Test the generated project
cd ../test-project
uv sync
docker compose up -d
just migrate
just test
```

4. Update documentation if needed

5. Commit your changes:
```bash
git add .
git commit -m "feat: add awesome feature"
```

6. Push and create a pull request

## Code Style

- Follow Django best practices
- Use type hints where appropriate
- Write tests for new features
- Update documentation

## Pull Request Process

1. Ensure all tests pass
2. Update the README.md if needed
3. Update CHANGELOG.md
4. Request review from maintainers

## Questions?

Open an issue or start a discussion!
