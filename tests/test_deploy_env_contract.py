"""Deploy targets must pass Django its config using the env var names that
``config/settings`` actually reads.

Regression guard for the ECS mismatch where the Terraform injected ``SECRET_KEY``
and ``ALLOWED_HOSTS`` while Django reads ``DJANGO_SECRET_KEY`` /
``DJANGO_ALLOWED_HOSTS``. The injected values were silently ignored, so a prod
deploy came up with an empty ``ALLOWED_HOSTS`` (400 DisallowedHost on every
request, including the load balancer health probe) and the insecure fallback
secret key. Every other target already used the ``DJANGO_``-prefixed names.
"""

import pytest


# Names config/settings reads from the environment for core prod config.
REQUIRED_ENV_NAMES = ["DJANGO_SECRET_KEY", "DJANGO_ALLOWED_HOSTS"]


def _deploy_text(project, target_dir, extra_files):
    """Concatenate the artifacts a target uses to hand env vars to Django."""
    parts = []
    directory = project / target_dir
    if directory.exists():
        parts += [p.read_text() for p in sorted(directory.rglob("*")) if p.is_file()]
    for name in extra_files:
        path = project / name
        if path.exists():
            parts.append(path.read_text())
    return "\n".join(parts)


@pytest.mark.parametrize(
    "target,target_dir,extra_files",
    [
        ("aws-ecs-fargate", "deploy/ecs", []),
        ("render", "deploy/render", ["render.yaml"]),
        ("flyio", "deploy/flyio", ["fly.toml"]),
    ],
)
def test_deploy_target_uses_settings_env_names(generate, target, target_dir, extra_files):
    """Each target that injects app env vars must use the names settings read."""
    project = generate(deployment_targets=[target])
    text = _deploy_text(project, target_dir, extra_files)
    assert text, f"no deploy artifacts found for {target}"
    for name in REQUIRED_ENV_NAMES:
        assert name in text, f"{target} never references {name}, which config/settings reads"


def test_ecs_env_names_match_settings(generate):
    """ECS Terraform must not inject the bare names Django never reads."""
    project = generate(deployment_targets=["aws-ecs-fargate"], media_storage="aws-s3")
    ecs_tf = (project / "deploy/ecs/terraform/ecs.tf").read_text()

    # Correct, settings-read names are injected.
    assert '"DJANGO_SECRET_KEY"' in ecs_tf
    assert '"DJANGO_ALLOWED_HOSTS"' in ecs_tf
    # Django uses one storage bucket; the two-bucket names are never read.
    assert '"AWS_STORAGE_BUCKET_NAME"' in ecs_tf
    assert "AWS_STORAGE_BUCKET_NAME_STATIC" not in ecs_tf
    assert "AWS_STORAGE_BUCKET_NAME_MEDIA" not in ecs_tf
    # The bare names Django does not read must not be injected as env vars.
    assert '"SECRET_KEY"' not in ecs_tf
    assert '"ALLOWED_HOSTS"' not in ecs_tf
