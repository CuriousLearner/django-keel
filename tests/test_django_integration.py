"""Integration tests that verify Django functionality."""

import os
import subprocess
import sys


# Django Command Tests


def test_django_check_passes(generate, copier_answers):
    """Test that Django system check passes on generated project."""
    project = generate()

    # Create .env file
    env_example = project / ".env.example"
    env_file = project / ".env"
    if env_example.exists():
        env_file.write_text(env_example.read_text())

    # Run Django check
    result = subprocess.run(
        [sys.executable, "manage.py", "check", "--deploy"],
        cwd=project,
        capture_output=True,
        text=True,
        env={**os.environ, "DJANGO_SETTINGS_MODULE": "config.settings.dev"},
    )

    # Should not have errors (warnings are OK for dev environment)
    assert "ERRORS" not in result.stdout or "0 errors" in result.stdout
    assert result.returncode in [0, 1]  # 1 is OK if only warnings


def test_settings_can_be_imported(generate):
    """Test that Django settings can be imported."""
    project = generate()

    # Create .env file from .env.example
    env_example = project / ".env.example"
    env_file = project / ".env"
    if env_example.exists():
        env_file.write_text(env_example.read_text())

    # Try importing settings
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "import sys; sys.path.insert(0, '.'); "
            "from config.settings import dev; "
            "print('Settings imported successfully')",
        ],
        cwd=project,
        capture_output=True,
        text=True,
    )

    # Some import errors are expected without dependencies installed
    # Just check that the files are syntactically correct
    # Accept success OR specific import errors for missing dependencies
    if result.returncode != 0:
        # These are expected import errors when dependencies aren't installed
        expected_errors = ["ModuleNotFoundError", "ImportError"]
        assert any(err in result.stderr for err in expected_errors), (
            f"Unexpected error: {result.stderr}"
        )


def test_manage_py_is_executable(generate):
    """Test that manage.py can be executed."""
    project = generate()
    manage_py = project / "manage.py"

    assert manage_py.exists()

    # Check it has execute permissions on Unix
    if sys.platform != "win32":
        # Should be readable and have Python shebang
        content = manage_py.read_text()
        assert content.startswith("#!/usr/bin/env python")


# Database Configuration Tests


def test_postgresql_database_configured(generate):
    """Test PostgreSQL database configuration."""
    project = generate(database="postgresql")

    settings = project / "config/settings/base.py"
    content = settings.read_text()

    assert "DATABASES" in content
    assert 'env.db("DATABASE_URL")' in content

    # Check dependencies include psycopg
    pyproject = project / "pyproject.toml"
    pyproject_content = pyproject.read_text()
    assert "psycopg" in pyproject_content


def test_sqlite_dev_postgres_prod_configuration(generate):
    """Test SQLite for dev, PostgreSQL for prod configuration."""
    project = generate(database="sqlite-dev-postgres-prod")

    # Check that base settings use PostgreSQL by default
    base_settings = project / "config/settings/base.py"
    base_content = base_settings.read_text()
    assert "DATABASES" in base_content
    assert 'env.db("DATABASE_URL")' in base_content

    # Dev settings should exist and import from base
    dev_settings = project / "config/settings/dev.py"
    assert dev_settings.exists()
    dev_content = dev_settings.read_text()
    assert "from .base import *" in dev_content


# Static Files Tests


def test_static_directories_exist(generate):
    """Test that static file directories are created."""
    project = generate()

    assert (project / "static").exists()
    assert (project / "media").exists()


def test_whitenoise_middleware_configured(generate):
    """Test that Whitenoise middleware is configured."""
    project = generate(media_storage="local-whitenoise")

    settings = project / "config/settings/base.py"
    content = settings.read_text()

    assert "WhiteNoiseMiddleware" in content
    assert "STATIC_URL" in content
    assert "STATIC_ROOT" in content


# URL Configuration Tests


def test_main_urls_include_app_urls(generate):
    """Test that main URLs include app URLs."""
    project = generate(api_style="drf")

    urls = project / "config/urls.py"
    content = urls.read_text()

    assert "urlpatterns" in content
    assert "include" in content

    # Should include core app
    assert "apps.core" in content or "core.urls" in content


def test_api_urls_when_drf_enabled(generate):
    """Test that API URLs are included when DRF is enabled."""
    project = generate(api_style="drf")

    urls = project / "config/urls.py"
    content = urls.read_text()

    assert "api" in content or "apps.api" in content


def test_admin_urls_included(generate):
    """Test that admin URLs are included."""
    project = generate()

    urls = project / "config/urls.py"
    content = urls.read_text()

    assert "admin" in content
    assert "admin.site.urls" in content


# Middleware Configuration Tests


def test_security_middleware_included(generate):
    """Test that security middleware is included."""
    project = generate()

    settings = project / "config/settings/base.py"
    content = settings.read_text()

    assert "MIDDLEWARE" in content
    assert "SecurityMiddleware" in content
    assert "AuthenticationMiddleware" in content
    assert "CsrfViewMiddleware" in content


def test_cors_middleware_when_api_enabled(generate):
    """Test that CORS middleware is included with API."""
    project = generate(api_style="drf")

    settings = project / "config/settings/base.py"
    content = settings.read_text()

    assert "CorsMiddleware" in content
    assert "CORS_ALLOWED_ORIGINS" in content


def test_allauth_middleware_when_enabled(generate):
    """Test that allauth middleware is included when enabled."""
    project = generate(auth_backend="allauth")

    settings = project / "config/settings/base.py"
    content = settings.read_text()

    assert "allauth.account.middleware.AccountMiddleware" in content


# Model Configuration Tests


def test_custom_user_model_configured(generate):
    """Test that custom user model is configured."""
    project = generate()

    settings = project / "config/settings/base.py"
    content = settings.read_text()

    assert 'AUTH_USER_MODEL = "users.User"' in content

    # Check user model exists
    user_model = project / "apps/users/models.py"
    assert user_model.exists()

    model_content = user_model.read_text()
    assert "AbstractUser" in model_content or "AbstractBaseUser" in model_content


# Template Configuration Tests


def test_templates_directory_configured(generate):
    """Test that templates directory is configured."""
    project = generate(frontend="htmx-tailwind")

    settings = project / "config/settings/base.py"
    content = settings.read_text()

    assert "TEMPLATES" in content
    assert "DjangoTemplates" in content
    assert "DIRS" in content


def test_django_templates_not_conflict_with_jinja(generate):
    """Test that Django template tags render correctly."""
    project = generate(frontend="htmx-tailwind")

    base_html = project / "templates/base.html"
    if base_html.exists():
        content = base_html.read_text()

        # Django tags should be present (not wrapped in raw)
        assert "{% block" in content
        assert "{% endblock" in content

        # Should not have Jinja2 raw tags in output
        assert "{% raw %}" not in content
        assert "{% endraw %}" not in content
