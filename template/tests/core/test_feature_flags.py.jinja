"""Tests for feature flags."""
import pytest
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.test import RequestFactory
from waffle.models import Flag, Switch, Sample

from apps.core.feature_flags import (
    is_feature_enabled,
    is_switch_enabled,
    feature_flag,
    feature_switch,
    create_default_flags,
    create_default_switches,
)

User = get_user_model()


@pytest.fixture
def user(db):
    """Create a test user."""
    return User.objects.create_user(
        email="user@example.com",
        password="testpass123"
    )


@pytest.fixture
def rf():
    """Request factory."""
    return RequestFactory()


@pytest.mark.django_db
class TestFeatureFlagUtilities:
    """Test feature flag utility functions."""

    def test_is_feature_enabled_with_flag(self, user, rf):
        """Test is_feature_enabled with active flag."""
        Flag.objects.create(name="test_feature", everyone=True)

        request = rf.get("/")
        request.user = user

        assert is_feature_enabled("test_feature", request=request) is True

    def test_is_feature_enabled_disabled(self, user, rf):
        """Test is_feature_enabled with inactive flag."""
        Flag.objects.create(name="test_feature", everyone=False)

        request = rf.get("/")
        request.user = user

        assert is_feature_enabled("test_feature", request=request) is False

    def test_is_feature_enabled_with_user(self, user):
        """Test is_feature_enabled with just user."""
        Flag.objects.create(name="test_feature", everyone=True)

        assert is_feature_enabled("test_feature", user=user) is True

    def test_is_switch_enabled(self):
        """Test is_switch_enabled."""
        Switch.objects.create(name="test_switch", active=True)

        assert is_switch_enabled("test_switch") is True

        Switch.objects.filter(name="test_switch").update(active=False)

        assert is_switch_enabled("test_switch") is False


@pytest.mark.django_db
class TestFeatureFlagDecorator:
    """Test feature_flag decorator."""

    def test_with_enabled_flag(self, user, rf):
        """Test decorator allows access when flag is enabled."""
        Flag.objects.create(name="beta_feature", everyone=True)

        @feature_flag("beta_feature")
        def view(request):
            return HttpResponse("Success")

        request = rf.get("/")
        request.user = user

        response = view(request)

        assert response.status_code == 200
        assert response.content == b"Success"

    def test_with_disabled_flag(self, user, rf):
        """Test decorator blocks access when flag is disabled."""
        Flag.objects.create(name="beta_feature", everyone=False)

        @feature_flag("beta_feature")
        def view(request):
            return HttpResponse("Success")

        request = rf.get("/")
        request.user = user

        response = view(request)

        assert response.status_code == 302  # Redirect

    def test_custom_redirect(self, user, rf):
        """Test decorator with custom redirect URL."""
        Flag.objects.create(name="beta_feature", everyone=False)

        @feature_flag("beta_feature", redirect_to="/pricing/")
        def view(request):
            return HttpResponse("Success")

        request = rf.get("/")
        request.user = user

        response = view(request)

        assert response.status_code == 302
        assert response.url == "/pricing/"

    def test_ajax_response(self, user, rf):
        """Test decorator returns JSON for AJAX."""
        Flag.objects.create(name="beta_feature", everyone=False)

        @feature_flag("beta_feature", ajax_response=True)
        def view(request):
            return HttpResponse("Success")

        request = rf.get("/")
        request.user = user

        response = view(request)

        assert response.status_code == 403
        assert response["Content-Type"] == "application/json"


@pytest.mark.django_db
class TestFeatureSwitchDecorator:
    """Test feature_switch decorator."""

    def test_with_active_switch(self, user, rf):
        """Test decorator allows access when switch is active."""
        Switch.objects.create(name="api_enabled", active=True)

        @feature_switch("api_enabled")
        def view(request):
            return HttpResponse("Success")

        request = rf.get("/")
        request.user = user

        response = view(request)

        assert response.status_code == 200

    def test_with_inactive_switch(self, user, rf):
        """Test decorator blocks access when switch is inactive."""
        Switch.objects.create(name="api_enabled", active=False)

        @feature_switch("api_enabled")
        def view(request):
            return HttpResponse("Success")

        request = rf.get("/")
        request.user = user

        response = view(request)

        assert response.status_code == 302


@pytest.mark.django_db
class TestDefaultFlagsAndSwitches:
    """Test default flags and switches creation."""

    def test_create_default_flags(self):
        """Test creating default flags."""
        create_default_flags()

        assert Flag.objects.filter(name="beta_features").exists()
        assert Flag.objects.filter(name="api_v2").exists()

    def test_create_default_switches(self):
        """Test creating default switches."""
        create_default_switches()

        assert Switch.objects.filter(name="maintenance_mode").exists()
        assert Switch.objects.filter(name="read_only_mode").exists()

        # Check default values
        maintenance = Switch.objects.get(name="maintenance_mode")
        assert maintenance.active is False

    def test_idempotent_creation(self):
        """Test that creating defaults multiple times is idempotent."""
        create_default_flags()
        count_first = Flag.objects.count()

        create_default_flags()
        count_second = Flag.objects.count()

        assert count_first == count_second
