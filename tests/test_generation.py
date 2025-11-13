"""Functional tests for template project generation."""

import py_compile

import pytest
import yaml


# Basic Project Generation Tests


def test_basic_project_generates(generate):
    """Test that a basic project can be generated."""
    project = generate()
    assert project.exists()
    assert (project / "manage.py").exists()
    assert (project / "config").exists()
    assert (project / "apps").exists()


def test_project_has_valid_python_syntax(generate):
    """Test that all generated Python files have valid syntax."""
    project = generate()

    python_files = list(project.rglob("*.py"))
    assert len(python_files) > 0, "No Python files found"

    for py_file in python_files:
        try:
            py_compile.compile(str(py_file), doraise=True)
        except py_compile.PyCompileError as e:
            pytest.fail(f"Syntax error in {py_file}: {e}")


def test_project_has_valid_yaml_files(generate):
    """Test that all generated YAML files are valid."""
    project = generate()

    yaml_files = [
        project / ".pre-commit-config.yaml",
        project / ".github" / "workflows" / "ci.yml",
    ]

    for yaml_file in yaml_files:
        if yaml_file.exists():
            with open(yaml_file) as f:
                try:
                    yaml.safe_load(f)
                except yaml.YAMLError as e:
                    # Show file content for debugging
                    content = yaml_file.read_text()
                    pytest.fail(
                        f"Invalid YAML in {yaml_file}:\n"
                        f"Error: {e}\n"
                        f"Content preview:\n{content[:500]}"
                    )


def test_project_structure_is_correct(generate):
    """Test that the generated project has the expected structure."""
    project = generate()

    expected_dirs = [
        "config",
        "config/settings",
        "apps",
        "apps/core",
        "apps/users",
        "static",
        "media",
        "templates",
    ]

    for dir_path in expected_dirs:
        assert (project / dir_path).exists(), f"Missing directory: {dir_path}"

    expected_files = [
        "manage.py",
        "config/__init__.py",
        "config/settings/__init__.py",
        "config/settings/base.py",
        "config/settings/dev.py",
        "config/settings/prod.py",
        "config/settings/test.py",
        "config/urls.py",
        "config/wsgi.py",
        "apps/core/views.py",
        "apps/users/models.py",
        ".gitignore",
        "README.md",
        "pyproject.toml",
    ]

    for file_path in expected_files:
        assert (project / file_path).exists(), f"Missing file: {file_path}"


def test_project_name_has_validator(template_dir):
    """Test that project_name field has a non-empty validator."""
    copier_yml = template_dir / "copier.yml"

    with open(copier_yml) as f:
        config = yaml.safe_load(f)

    assert "project_name" in config
    assert "validator" in config["project_name"]
    validator = config["project_name"]["validator"]
    assert "project_name" in validator
    assert "empty" in validator.lower() or "not project_name" in validator


def test_project_description_has_validator(template_dir):
    """Test that project_description field has a non-empty validator."""
    copier_yml = template_dir / "copier.yml"

    with open(copier_yml) as f:
        config = yaml.safe_load(f)

    assert "project_description" in config
    assert "validator" in config["project_description"]
    validator = config["project_description"]["validator"]
    assert "project_description" in validator
    assert "empty" in validator.lower() or "not project_description" in validator


# Dependency Manager Tests


def test_uv_pyproject_generated(generate):
    """Test that UV pyproject.toml is generated correctly."""
    project = generate(dependency_manager="uv")
    pyproject = project / "pyproject.toml"

    assert pyproject.exists()
    content = pyproject.read_text()
    assert "[project]" in content
    assert "dependencies" in content
    assert "django>=" in content


def test_poetry_pyproject_generated(generate):
    """Test that Poetry pyproject.toml is generated correctly."""
    project = generate(dependency_manager="poetry")
    pyproject = project / "pyproject.toml"

    assert pyproject.exists()
    content = pyproject.read_text()
    assert "[tool.poetry]" in content
    assert "[tool.poetry.dependencies]" in content
    assert "django" in content


# API Style Tests


def test_drf_api_generated(generate):
    """Test that DRF API configuration is correct."""
    project = generate(api_style="drf")

    # Check settings
    settings = project / "config/settings/base.py"
    content = settings.read_text()
    assert "rest_framework" in content
    assert "drf_spectacular" in content
    assert "django_filters" in content
    assert "corsheaders" in content

    # Check API app exists
    assert (project / "apps/api").exists()
    assert (project / "apps/api/urls.py").exists()
    assert (project / "apps/api/views.py").exists()


def test_graphql_api_generated(generate):
    """Test that GraphQL API configuration is correct."""
    project = generate(api_style="graphql-strawberry")

    settings = project / "config/settings/base.py"
    content = settings.read_text()
    assert "strawberry" in content


def test_both_apis_generated(generate):
    """Test that both DRF and GraphQL can coexist."""
    project = generate(api_style="both")

    settings = project / "config/settings/base.py"
    content = settings.read_text()
    assert "rest_framework" in content
    assert "strawberry" in content


def test_no_api_excludes_frameworks(generate):
    """Test that no API style excludes API frameworks."""
    project = generate(api_style="none")

    settings = project / "config/settings/base.py"
    content = settings.read_text()
    assert "rest_framework" not in content
    assert "strawberry" not in content


# Frontend Option Tests


def test_htmx_frontend_templates_generated(generate):
    """Test that HTMX frontend generates templates."""
    project = generate(frontend="htmx-tailwind")

    templates_dir = project / "templates"
    assert (templates_dir / "base.html").exists()

    base_html = (templates_dir / "base.html").read_text()
    assert "{% block" in base_html
    assert "tailwindcss" in base_html
    assert "htmx" in base_html


def test_nextjs_frontend_generated(generate):
    """Test that Next.js frontend is generated."""
    project = generate(frontend="nextjs")

    frontend_dir = project / "frontend"
    assert frontend_dir.exists()
    assert (frontend_dir / "package.json").exists()

    package_json = (frontend_dir / "package.json").read_text()
    assert "next" in package_json


def test_no_frontend_has_minimal_templates(generate):
    """Test that no frontend option has minimal templates."""
    project = generate(frontend="none")

    templates_dir = project / "templates"
    # Should have directory but minimal content
    assert templates_dir.exists()
    # base.html should not exist
    assert not (templates_dir / "base.html").exists()


# Auth Backend Tests


def test_allauth_configuration(generate):
    """Test that allauth is configured correctly."""
    project = generate(auth_backend="allauth")

    settings = project / "config/settings/base.py"
    content = settings.read_text()

    # Check allauth packages
    assert "allauth" in content
    assert "allauth.account" in content
    assert "allauth.socialaccount" in content

    # Check middleware
    assert "allauth.account.middleware.AccountMiddleware" in content

    # Check sites framework
    assert "django.contrib.sites" in content

    # Check new settings format
    assert "ACCOUNT_LOGIN_METHODS" in content


def test_jwt_configuration(generate):
    """Test that JWT is configured correctly."""
    project = generate(auth_backend="jwt")

    settings = project / "config/settings/base.py"
    content = settings.read_text()
    assert "simplejwt" in content or "SIMPLE_JWT" in content


def test_both_auth_backends(generate):
    """Test that both auth backends can coexist."""
    project = generate(auth_backend="both")

    settings = project / "config/settings/base.py"
    content = settings.read_text()
    assert "allauth" in content
    assert "simplejwt" in content or "SIMPLE_JWT" in content
