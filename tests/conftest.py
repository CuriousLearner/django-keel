"""Pytest configuration and fixtures for django-keel template tests."""

import shutil
import tempfile
from pathlib import Path
from typing import Dict, Any

import pytest
import yaml
from plumbum import local


@pytest.fixture(scope="session")
def template_dir() -> Path:
    """Return the path to the django-keel template directory."""
    return Path(__file__).parent.parent


@pytest.fixture
def temp_dir(tmp_path_factory):
    """Create a temporary directory for test outputs."""
    return tmp_path_factory.mktemp("generated_projects")


@pytest.fixture
def copier_answers():
    """Default copier answers for testing."""
    return {
        "project_name": "Test Project",
        "project_slug": "test_project",
        "project_description": "A test Django project",
        "author_name": "Test Author",
        "author_email": "test@example.com",
        "python_version": "3.12",
        "dependency_manager": "uv",
        "database": "postgresql",
        "cache": "redis",
        "api_style": "drf",
        "frontend": "none",
        "use_celery": False,
        "use_channels": False,
        "auth_backend": "allauth",
        "use_2fa": False,
        "observability_level": "minimal",
        "use_sentry": False,
        "deployment_targets": "none",
        "media_storage": "local-whitenoise",
        "security_profile": "standard",
        "use_sops": False,
        "use_stripe": False,
        "use_search": "none",
        "use_i18n": False,
        "ci_provider": "github-actions",
        "license": "MIT",
    }


def generate_project(
    template_dir: Path,
    output_dir: Path,
    answers: Dict[str, Any],
) -> Path:
    """
    Generate a project from the template.

    Args:
        template_dir: Path to the template directory
        output_dir: Path where the project should be generated
        answers: Dictionary of copier answers

    Returns:
        Path to the generated project
    """
    from copier import run_copy

    # Create answers file
    answers_file = output_dir / "answers.yml"
    with open(answers_file, "w") as f:
        yaml.dump(answers, f)

    project_dir = output_dir / answers["project_slug"]

    # Generate project
    run_copy(
        str(template_dir),
        str(project_dir),
        data=answers,
        defaults=True,
        unsafe=True,
        vcs_ref="HEAD",
    )

    return project_dir


@pytest.fixture
def generate(template_dir, temp_dir, copier_answers):
    """Fixture that returns a function to generate projects."""
    def _generate(answers: Dict[str, Any] = None, **kwargs) -> Path:
        """
        Generate a project with custom answers.

        Args:
            answers: Base answers dict (defaults to copier_answers)
            **kwargs: Override specific answer values

        Returns:
            Path to generated project
        """
        final_answers = copier_answers.copy()
        if answers:
            final_answers.update(answers)
        final_answers.update(kwargs)

        return generate_project(template_dir, temp_dir, final_answers)

    return _generate


@pytest.fixture
def project_with_config(generate, copier_answers):
    """Generate a project and return both the path and config."""
    def _project_with_config(**kwargs):
        answers = copier_answers.copy()
        answers.update(kwargs)
        project_path = generate(answers)
        return project_path, answers

    return _project_with_config
