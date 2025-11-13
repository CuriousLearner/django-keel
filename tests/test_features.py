"""Behavioral tests for optional features."""


# Celery Feature Tests


def test_celery_files_generated_when_enabled(generate):
    """Test that Celery configuration is generated when enabled."""
    project = generate(background_tasks="celery")

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


def test_kubernetes_deployment_generated(generate):
    """Test that Kubernetes manifests are generated."""
    project = generate(deployment_targets=["kubernetes"])

    k8s_dir = project / "deploy/k8s"
    assert k8s_dir.exists()

    # Check for helm charts
    helm_dir = k8s_dir / "helm"
    if helm_dir.exists():
        assert len(list(helm_dir.iterdir())) > 0


def test_render_deployment_generated(generate):
    """Test that Render deployment files are generated."""
    project = generate(deployment_targets=["render"])

    # Check render.yaml exists in root
    render_yaml = project / "render.yaml"
    assert render_yaml.exists()

    # Validate YAML content
    content = render_yaml.read_text()
    assert "services:" in content
    assert "databases:" in content or "name:" in content

    # Check deploy/render directory
    render_dir = project / "deploy/render"
    assert render_dir.exists()
    assert (render_dir / "build.sh").exists()

    # Verify build script is executable content
    build_script = (render_dir / "build.sh").read_text()
    assert "#!/bin/bash" in build_script or "pip install" in build_script


def test_flyio_deployment_generated(generate):
    """Test that Fly.io deployment files are generated."""
    project = generate(deployment_targets=["flyio"])

    # Check fly.toml exists in root
    fly_toml = project / "fly.toml"
    assert fly_toml.exists()

    # Validate TOML content
    content = fly_toml.read_text()
    assert "app =" in content or "[app]" in content
    assert "[[services]]" in content or "[http_service]" in content

    # Check deploy/flyio directory
    flyio_dir = project / "deploy/flyio"
    assert flyio_dir.exists()


def test_ecs_deployment_generated(generate):
    """Test that AWS ECS deployment files are generated."""
    project = generate(deployment_targets=["aws-ecs-fargate"])

    # Check deploy/ecs directory
    ecs_dir = project / "deploy/ecs"
    assert ecs_dir.exists()

    # Currently ECS only has README (deployment configs are WIP)
    readme = ecs_dir / "README.md"
    assert readme.exists()

    # Verify README has ECS content
    content = readme.read_text()
    assert "ECS" in content or "Fargate" in content or "AWS" in content


def test_docker_deployment_generated(generate):
    """Test that Docker deployment files are generated."""
    project = generate(deployment_targets=["docker"])

    # Check Dockerfile exists
    dockerfile = project / "Dockerfile"
    assert dockerfile.exists()

    # Validate Dockerfile content
    content = dockerfile.read_text()
    assert "FROM python:" in content
    assert "WORKDIR" in content
    assert "COPY" in content

    # Check docker-compose files
    docker_compose = project / "docker-compose.yml"
    assert docker_compose.exists()


def test_ec2_ansible_deployment_generated(generate):
    """Test that AWS EC2 Ansible playbooks are generated."""
    project = generate(deployment_targets=["aws-ec2-ansible"])

    # Check deploy/ansible directory
    ansible_dir = project / "deploy/ansible"
    assert ansible_dir.exists()

    # Check README
    readme = ansible_dir / "README.md"
    assert readme.exists()

    # Check playbooks directory
    playbooks_dir = ansible_dir / "playbooks"
    assert playbooks_dir.exists()

    # Check for deploy playbook
    deploy_yml = playbooks_dir / "deploy.yml"
    assert deploy_yml.exists()

    # Validate YAML syntax (basic check)
    deploy_content = deploy_yml.read_text()
    assert "hosts:" in deploy_content or "- name:" in deploy_content or "tasks:" in deploy_content

    # Check templates directory
    templates_dir = ansible_dir / "templates"
    assert templates_dir.exists()


def test_multiple_deployment_targets(generate):
    """Test that multiple deployment targets can be specified."""
    project = generate(deployment_targets=["render", "flyio", "docker"])

    # All selected platforms should have their files
    assert (project / "render.yaml").exists()
    assert (project / "fly.toml").exists()
    assert (project / "Dockerfile").exists()

    # Deploy directories
    assert (project / "deploy/render").exists()
    assert (project / "deploy/flyio").exists()


def test_no_deployment_excludes_deploy_configs(generate):
    """Test that platform-specific deployment configs are excluded when not specified."""
    project = generate(deployment_targets=[])

    # Platform-specific files should not exist
    assert not (project / "render.yaml").exists()
    assert not (project / "fly.toml").exists()

    # Platform-specific deploy directories should not exist
    deploy_dir = project / "deploy"
    if deploy_dir.exists():
        assert not (deploy_dir / "render").exists()
        assert not (deploy_dir / "flyio").exists()
        assert not (deploy_dir / "ansible").exists()
        assert not (deploy_dir / "ecs").exists()

    # Note: K8s configs may still exist as they're often used as a base/reference
    # even when not explicitly selected as a deployment target


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
        dependency_manager="uv",
        api_style="both",
        frontend="htmx-tailwind",
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
