"""Functional tests for template project generation."""

import json
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


def test_poetry_whitenoise_unconditional(generate):
    """whitenoise is required by base settings regardless of media storage."""
    project = generate(dependency_manager="poetry", media_storage="aws-s3")
    content = (project / "pyproject.toml").read_text()
    assert "whitenoise" in content
    assert "package-mode = false" in content


def test_poetry_justfile_uses_poetry_run(generate):
    """Justfile recipes must run tools through the poetry venv."""
    project = generate(dependency_manager="poetry")
    content = (project / "Justfile").read_text()
    assert "poetry run pytest" in content
    assert "poetry run python manage.py migrate" in content


def test_uv_ci_installs_dev_extras(generate):
    """CI needs --all-extras so ruff/mypy/pytest from the dev extra are installed."""
    project = generate(dependency_manager="uv", ci_provider="github-actions")
    content = (project / ".github/workflows/ci.yml").read_text()
    assert "uv sync --all-extras" in content


@pytest.mark.parametrize("dep_manager", ["uv", "poetry"])
def test_coverage_targets_apps_and_config(generate, dep_manager):
    """Coverage must measure apps/config (where code lives), from one config location."""
    project = generate(dependency_manager=dep_manager)
    pyproject = (project / "pyproject.toml").read_text()
    assert 'source = ["apps", "config"]' in pyproject
    # pytest.ini is the single canonical pytest config
    assert "[tool.pytest.ini_options]" not in pyproject
    assert (project / "pytest.ini").exists()


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

    # config/urls.py includes apps.api.urls, so it must exist for graphql-only
    assert (project / "apps/api/urls.py").exists()

    # Schema must use the modern strawberry-graphql-django API (issue #73)
    schema = (project / "apps/api/schema.py").read_text()
    assert "from strawberry.django import auto" not in schema
    assert "import strawberry_django" in schema


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
    """Test that HTMX frontend generates templates with Vite (default)."""
    project = generate(frontend="htmx-tailwind")

    templates_dir = project / "templates"
    assert (templates_dir / "base.html").exists()

    base_html = (templates_dir / "base.html").read_text()
    assert "{% block" in base_html
    # Vite is the default, so check for vite tags
    assert "django_vite" in base_html
    assert "vite_asset" in base_html

    # Vite frontend files should exist
    frontend_dir = project / "frontend"
    assert (frontend_dir / "package.json").exists()
    assert (frontend_dir / "vite.config.js").exists()
    assert (frontend_dir / "tailwind.config.js").exists()

    # Check Django settings include django_vite
    settings = project / "config" / "settings" / "base.py"
    settings_content = settings.read_text()
    assert "django_vite" in settings_content
    assert "DJANGO_VITE" in settings_content


def test_htmx_frontend_cdn_mode(generate):
    """Test that HTMX frontend with CDN mode uses CDN links."""
    project = generate(frontend="htmx-tailwind", frontend_bundling="cdn")

    templates_dir = project / "templates"
    base_html = (templates_dir / "base.html").read_text()
    assert "{% block" in base_html
    assert "tailwindcss" in base_html
    assert "htmx" in base_html
    # Should not have vite tags
    assert "django_vite" not in base_html

    # CDN mode should NOT create frontend build files
    frontend_dir = project / "frontend"
    assert not (frontend_dir / "package.json").exists()
    assert not (frontend_dir / "vite.config.js").exists()
    assert not (frontend_dir / "tailwind.config.js").exists()


def test_nextjs_frontend_generated(generate):
    """Test that Next.js frontend generates a runnable minimal App Router app."""
    project = generate(frontend="nextjs")

    frontend_dir = project / "frontend"
    assert frontend_dir.exists()
    assert (frontend_dir / "README.md").exists()

    # A runnable app, not a bare README stub: package.json + app/ entrypoints.
    package_json = frontend_dir / "package.json"
    assert package_json.exists()
    pkg = json.loads(package_json.read_text())
    assert pkg["scripts"]["dev"] == "next dev"
    for dep in ("next", "react", "react-dom"):
        assert dep in pkg["dependencies"]
    assert (frontend_dir / "app/layout.js").exists()
    assert (frontend_dir / "app/page.js").exists()


def test_no_frontend_has_minimal_templates(generate):
    """Test that no frontend option has minimal templates."""
    project = generate(frontend="none")

    templates_dir = project / "templates"
    # Should have directory but minimal content
    assert templates_dir.exists()
    # base.html is always shipped (teams/billing templates extend it),
    # but without frontend-specific assets
    assert (templates_dir / "base.html").exists()
    assert "tailwindcss" not in (templates_dir / "base.html").read_text()
    # Frontend-specific pages should not exist
    assert not (templates_dir / "core/index.html").exists()


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


# Devcontainer Tests


def test_devcontainer_files_exist(generate):
    """Test that devcontainer files are always generated."""
    project = generate()
    assert (project / ".devcontainer/devcontainer.json").exists()
    assert (project / ".devcontainer/docker-compose.devcontainer.yml").exists()


def test_devcontainer_json_is_valid_minimal(generate):
    """Test that devcontainer.json is valid JSON with minimal options."""
    project = generate(
        cache="none",
        frontend="none",
        background_tasks="none",
        observability_level="minimal",
    )
    content = (project / ".devcontainer/devcontainer.json").read_text()
    config = json.loads(content)
    assert config["service"] == "web"
    assert 8000 in config["forwardPorts"]
    assert 6379 not in config["forwardPorts"]


def test_devcontainer_json_is_valid_all_options(generate):
    """Test that devcontainer.json is valid JSON with all conditional options enabled."""
    project = generate(
        cache="redis",
        frontend="htmx-tailwind",
        frontend_bundling="vite",
        background_tasks="temporal",
        observability_level="full",
    )
    content = (project / ".devcontainer/devcontainer.json").read_text()
    config = json.loads(content)
    assert 6379 in config["forwardPorts"]
    assert 5173 in config["forwardPorts"]
    assert 7233 in config["forwardPorts"]
    assert 16686 in config["forwardPorts"]


def test_devcontainer_compose_override_is_valid_yaml(generate):
    """Test that the devcontainer compose override is valid YAML."""
    project = generate()
    content = (project / ".devcontainer/docker-compose.devcontainer.yml").read_text()
    config = yaml.safe_load(content)
    assert config["services"]["web"]["command"] == "sleep infinity"


def test_compose_env_file_is_optional(generate):
    """A fresh project ships only .env.example, so the compose services must
    mark env_file: .env as required: false; otherwise the devcontainer (and a
    plain `docker compose up`) fails before anything can create .env."""
    project = generate(background_tasks="celery")
    compose = yaml.safe_load((project / "docker-compose.yml").read_text())
    web_env_file = compose["services"]["web"]["env_file"]
    assert web_env_file == [{"path": ".env", "required": False}]


def test_devcontainer_installs_dev_extras(generate):
    """The uv post-create step must install the dev extra (ruff, pytest, mypy),
    matching the repo's `uv sync --all-extras` convention; plain `uv sync` skips
    optional-dependencies and leaves the devcontainer without dev tooling."""
    project = generate(dependency_manager="uv")
    config = json.loads((project / ".devcontainer/devcontainer.json").read_text())
    assert "uv sync --all-extras" in config["postCreateCommand"]


@pytest.mark.parametrize("dependency_manager", ["uv", "poetry"])
def test_devcontainer_interpreter_path(generate, dependency_manager):
    """Both dependency managers resolve to the in-project venv interpreter."""
    project = generate(dependency_manager=dependency_manager)
    config = json.loads((project / ".devcontainer/devcontainer.json").read_text())
    interpreter = config["customizations"]["vscode"]["settings"]
    assert interpreter["python.defaultInterpreterPath"] == "/app/.venv/bin/python"


def test_devcontainer_project_name_with_special_chars(generate):
    """Test that project_name with quotes/special chars produces valid JSON."""
    project = generate(project_name='My "Awesome" Project')
    content = (project / ".devcontainer/devcontainer.json").read_text()
    config = json.loads(content)
    assert config["name"] == 'My "Awesome" Project'


# License Tests


@pytest.mark.parametrize(
    "license_choice,expected_phrase",
    [
        ("MIT", "MIT License"),
        ("Apache-2.0", "TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION"),
        ("GPL-3.0", "GNU GENERAL PUBLIC LICENSE"),
        ("BSD-3-Clause", "Redistribution and use in source and binary forms"),
        ("Proprietary", "Proprietary"),
    ],
)
def test_license_content(generate, license_choice, expected_phrase):
    """Test that each license choice generates the correct license text."""
    project = generate(license=license_choice)

    content = (project / "LICENSE").read_text()
    assert expected_phrase in content
    assert "would go here" not in content  # no placeholder bodies


# Ansible Deployment Tests


def test_ansible_playbook_preserves_runtime_variables(generate):
    """Test that ansible runtime variables are not consumed by copier."""
    project = generate(deployment_targets=["aws-ec2-ansible"])

    playbook = project / "deploy/ansible/playbooks/deploy.yml"
    content = playbook.read_text()
    assert yaml.safe_load(content)  # valid YAML after rendering
    assert '"{{ app_user }}"' in content
    assert "{{ app_dir }}" in content
    assert "{{ git_repo }}" in content
    assert "test_project" in content  # copier vars still rendered


# Migration Tests
#
# Guards two boot/CI-fatal regressions: teams/billing shipping no migrations
# (makemigrations --check fails, migrate creates no tables), and the users
# initial migration recording a stale manager (makemigrations wants a 0002).


def test_teams_migrations_shipped(generate):
    """Teams app ships an initial migration so `migrate` creates its tables."""
    project = generate(use_teams=True)

    migrations = project / "apps/teams/migrations"
    assert (migrations / "__init__.py").exists()
    assert (migrations / "0001_initial.py").exists()
    content = (migrations / "0001_initial.py").read_text()
    for model in ("Team", "TeamMember", "TeamInvitation"):
        assert f'name="{model}"' in content


@pytest.mark.parametrize(
    ("stripe_mode", "expected_models"),
    [
        ("advanced", ("PlanConfiguration", "UsageRecord", "SubscriptionMetadata")),
        ("basic", ("StripeCustomer", "Subscription")),
    ],
)
def test_billing_migrations_shipped(generate, stripe_mode, expected_models):
    """Billing ships the initial migration matching the selected stripe mode."""
    project = generate(use_teams=True, use_stripe=True, stripe_mode=stripe_mode)

    migrations = project / "apps/billing/migrations"
    assert (migrations / "__init__.py").exists()
    content = (migrations / "0001_initial.py").read_text()
    for model in expected_models:
        assert f'name="{model}"' in content


def test_disabled_feature_apps_are_absent(generate):
    """Teams/billing/api apps are gated at the directory level.

    With the feature off the whole app dir (and its migrations) must be absent,
    not shipped as dead files or an empty ``migrations/`` dir.
    """
    project = generate(use_teams=False, use_stripe=False, api_style="none")

    assert not (project / "apps/teams").exists()
    assert not (project / "apps/billing").exists()
    assert not (project / "apps/api").exists()
    # apps that always ship are unaffected
    assert (project / "apps/users").exists()
    assert (project / "apps/core").exists()


def test_users_initial_migration_has_no_stale_manager(generate):
    """Users 0001 must not record a manager, or makemigrations wants a 0002."""
    project = generate()

    content = (project / "apps/users/migrations/0001_initial.py").read_text()
    assert "managers=" not in content
    assert "django.contrib.auth.models" not in content
