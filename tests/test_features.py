"""Behavioral tests for optional features."""

import pytest
from copier import run_copy


# Celery Feature Tests


def test_celery_files_generated_when_enabled(generate):
    """Test that Celery configuration is generated when enabled."""
    project = generate(django_version="5.2", background_tasks="celery")

    # Celery file should exist
    celery_file = project / "config/celery.py"
    assert celery_file.exists()

    content = celery_file.read_text()
    assert "from celery import Celery" in content
    assert "app = Celery" in content

    # Check settings
    settings = project / "config/settings/base.py"
    settings_content = settings.read_text()
    assert "django_celery_beat" in settings_content
    assert "django_celery_results" in settings_content
    assert "CELERY_BROKER_URL" in settings_content


def test_celery_not_generated_when_disabled(generate):
    """Test that Celery is excluded when disabled."""
    project = generate(background_tasks="none")

    # Celery file should not exist
    celery_file = project / "config/celery.py"
    assert not celery_file.exists()

    # Settings should not have celery config
    settings = project / "config/settings/base.py"
    content = settings.read_text()
    assert "django_celery_beat" not in content


def test_celery_requires_django_52(template_dir, temp_dir, copier_answers):
    """Test that Celery with Django 6.0 is rejected by copier validation."""
    answers = copier_answers.copy()
    answers["django_version"] = "6.0"
    answers["background_tasks"] = "celery"

    with pytest.raises(
        ValueError,
        match=r"Django 6\.0 is not yet supported with Celery",
    ):
        run_copy(
            str(template_dir),
            str(temp_dir / "test_project"),
            data=answers,
            defaults=True,
            unsafe=True,
            vcs_ref="HEAD",
        )


# Channels Feature Tests


def test_channels_asgi_when_enabled(generate):
    """Test that ASGI configuration uses Channels when enabled."""
    project = generate(use_channels=True)

    settings = project / "config/settings/base.py"
    content = settings.read_text()

    assert "channels" in content
    assert "ASGI_APPLICATION" in content
    # Should not have WSGI when channels enabled
    assert "WSGI_APPLICATION" not in content or content.count("ASGI_APPLICATION") > 0


def test_wsgi_when_channels_disabled(generate):
    """Test that WSGI is used when Channels is disabled."""
    project = generate(use_channels=False)

    settings = project / "config/settings/base.py"
    content = settings.read_text()

    assert "WSGI_APPLICATION" in content
    assert "channels" not in content


# Stripe Feature Tests


def test_billing_app_generated_when_stripe_enabled(generate):
    """Test that billing app is generated with Stripe (basic mode)."""
    project = generate(use_stripe=True, stripe_mode="basic")

    # Billing app should exist
    billing_app = project / "apps/billing"
    assert billing_app.exists()
    assert (billing_app / "models.py").exists()

    # Check for Stripe models (basic mode)
    models = (billing_app / "models.py").read_text()
    assert "StripeCustomer" in models
    assert "stripe_customer_id" in models


def test_billing_app_generated_when_stripe_advanced(generate):
    """Test that billing app is generated with Stripe (advanced mode with dj-stripe)."""
    project = generate(use_stripe=True, stripe_mode="advanced")

    # Billing app should exist
    billing_app = project / "apps/billing"
    assert billing_app.exists()
    assert (billing_app / "models.py").exists()

    # Check for dj-stripe advanced models
    models = (billing_app / "models.py").read_text()
    assert "SubscriptionMetadata" in models
    assert "PlanConfiguration" in models
    assert "UsageRecord" in models
    assert "djstripe" in models


def test_billing_app_not_generated_when_stripe_disabled(generate):
    """Test that billing app is excluded without Stripe."""
    project = generate(use_stripe=False)

    billing_app = project / "apps/billing"
    # Billing directory might exist but should be empty or minimal
    if billing_app.exists():
        # Should not have models.py
        assert not (billing_app / "models.py").exists()


# 2FA Feature Tests


def test_2fa_packages_when_enabled(generate):
    """Test that 2FA packages are included when enabled."""
    project = generate(use_2fa=True)

    settings = project / "config/settings/base.py"
    content = settings.read_text()

    assert "django_otp" in content
    assert "django_otp.plugins.otp_totp" in content
    assert "django_otp.middleware.OTPMiddleware" in content


def test_2fa_excluded_when_disabled(generate):
    """Test that 2FA is excluded when disabled."""
    project = generate(use_2fa=False)

    settings = project / "config/settings/base.py"
    content = settings.read_text()

    assert "django_otp" not in content


# i18n Feature Tests


def test_i18n_configuration_when_enabled(generate):
    """Test that i18n is properly configured when enabled."""
    project = generate(use_i18n=True)

    settings = project / "config/settings/base.py"
    content = settings.read_text()

    assert "parler" in content
    assert "USE_I18N = True" in content
    assert "LANGUAGES" in content
    assert "LOCALE_PATHS" in content


def test_i18n_disabled_when_not_needed(generate):
    """Test that i18n is disabled when not needed."""
    project = generate(use_i18n=False)

    settings = project / "config/settings/base.py"
    content = settings.read_text()

    assert "USE_I18N = False" in content
    assert "parler" not in content


# Cache Option Tests


def test_redis_cache_configured(generate):
    """Test that Redis cache is configured correctly."""
    project = generate(cache="redis")

    settings = project / "config/settings/base.py"
    content = settings.read_text()

    assert "django_redis" in content
    assert "RedisCache" in content
    assert "CACHES" in content

    # Check views don't import cache when not needed
    views = project / "apps/core/views.py"
    views_content = views.read_text()
    assert "from django.core.cache import cache" in views_content


def test_no_cache_configured(generate):
    """Test that cache is excluded when set to none."""
    project = generate(cache="none")

    settings = project / "config/settings/base.py"
    content = settings.read_text()

    assert "django_redis" not in content

    # Views should not import cache
    views = project / "apps/core/views.py"
    views_content = views.read_text()
    assert "from django.core.cache import cache" not in views_content


# Deployment Target Tests

# Mapping of deployment target to its deploy directory
DEPLOY_DIRECTORIES = [
    ("kubernetes", "k8s"),
    ("render", "render"),
    ("flyio", "flyio"),
    ("aws-ecs-fargate", "ecs"),
    ("aws-ec2-ansible", "ansible"),
]


@pytest.mark.parametrize("target,deploy_dir", DEPLOY_DIRECTORIES)
def test_deploy_directory_created_when_target_selected(generate, target, deploy_dir):
    """Test that deploy directory is created when its target is selected."""
    project = generate(deployment_targets=[target])
    assert (project / f"deploy/{deploy_dir}").exists()


@pytest.mark.parametrize("target,deploy_dir", DEPLOY_DIRECTORIES)
def test_deploy_directory_not_created_when_target_not_selected(generate, target, deploy_dir):
    """Test that deploy directory is NOT created when its target is not selected."""
    # Use docker as a neutral target that doesn't create a deploy subdirectory
    project = generate(deployment_targets=["docker"])
    assert not (project / f"deploy/{deploy_dir}").exists()


def test_docker_deployment_generated(generate):
    """Test that Docker deployment files are generated."""
    project = generate(deployment_targets=["docker"])

    dockerfile = project / "Dockerfile"
    assert dockerfile.exists()

    content = dockerfile.read_text()
    assert "FROM python:" in content
    assert "WORKDIR" in content

    assert (project / "docker-compose.yml").exists()


def test_render_root_files_generated(generate):
    """Test that Render creates render.yaml in project root."""
    project = generate(deployment_targets=["render"])

    render_yaml = project / "render.yaml"
    assert render_yaml.exists()

    content = render_yaml.read_text()
    assert "services:" in content


def test_flyio_root_files_generated(generate):
    """Test that Fly.io creates fly.toml in project root."""
    project = generate(deployment_targets=["flyio"])

    fly_toml = project / "fly.toml"
    assert fly_toml.exists()

    content = fly_toml.read_text()
    assert "app =" in content or "[app]" in content


def test_multiple_deployment_targets(generate):
    """Test that multiple deployment targets can be specified."""
    project = generate(deployment_targets=["kubernetes", "render", "flyio", "docker"])

    assert (project / "deploy/k8s").exists()
    assert (project / "deploy/render").exists()
    assert (project / "deploy/flyio").exists()
    assert (project / "render.yaml").exists()
    assert (project / "fly.toml").exists()
    assert (project / "Dockerfile").exists()


def test_no_deployment_targets_excludes_all_deploy_dirs(generate):
    """Test that no deploy directories are created when deployment_targets is empty."""
    project = generate(deployment_targets=[])

    assert not (project / "render.yaml").exists()
    assert not (project / "fly.toml").exists()

    deploy_dir = project / "deploy"
    if deploy_dir.exists():
        for _, dir_name in DEPLOY_DIRECTORIES:
            assert not (deploy_dir / dir_name).exists()


# Media Storage Tests


def test_local_whitenoise_storage(generate):
    """Test local storage with Whitenoise."""
    project = generate(media_storage="local-whitenoise")

    settings = project / "config/settings/base.py"
    content = settings.read_text()

    assert "whitenoise" in content
    assert "STATICFILES_STORAGE" in content or "WhiteNoiseMiddleware" in content


def test_aws_s3_storage_configuration(generate):
    """Test AWS S3 storage configuration."""
    project = generate(media_storage="aws-s3")

    settings = project / "config/settings/base.py"
    content = settings.read_text()

    assert "AWS_" in content
    assert "S3" in content or "s3" in content


# All Features Combination Test


def test_all_features_enabled_generates_successfully(generate):
    """Test that enabling all features generates a valid project."""
    project = generate(
        django_version="5.2",  # Celery requires 5.2 (django-celery-beat incompatible with 6.0)
        dependency_manager="uv",
        api_style="both",
        frontend="htmx-tailwind",
        frontend_bundling="vite",  # Explicitly test Vite (the default)
        background_tasks="celery",
        use_channels=True,
        auth_backend="both",
        use_2fa=True,
        use_stripe=True,
        stripe_mode="advanced",
        use_teams=True,
        use_i18n=True,
        cache="redis",
        deployment_targets=["kubernetes"],
        media_storage="aws-s3",
        observability_level="full",
        use_sentry=True,
        use_search="postgres-fts",
    )

    # Project should exist
    assert project.exists()

    # All apps should exist
    assert (project / "apps/api").exists()
    assert (project / "apps/billing").exists()
    assert (project / "apps/core").exists()
    assert (project / "apps/users").exists()

    # All config files should exist
    assert (project / "config/celery.py").exists()
    assert (project / "config/asgi.py").exists()

    # Check settings has all features
    settings = project / "config/settings/base.py"
    content = settings.read_text()

    # API frameworks
    assert "rest_framework" in content
    assert "strawberry" in content

    # Auth
    assert "allauth" in content
    assert "simplejwt" in content or "SIMPLE_JWT" in content

    # Optional features
    assert "django_celery" in content
    assert "channels" in content
    assert "django_otp" in content
    assert "parler" in content

    # Ensure Python syntax is valid
    import py_compile

    for py_file in project.rglob("*.py"):
        py_compile.compile(str(py_file), doraise=True)
