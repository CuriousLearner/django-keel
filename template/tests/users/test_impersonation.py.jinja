"""Tests for user impersonation."""
import pytest
from django.contrib.auth import get_user_model
from django.test import RequestFactory
from django.urls import reverse

from apps.users.impersonation import (
    ImpersonationMiddleware,
    prevent_while_impersonating,
)

User = get_user_model()


@pytest.fixture
def staff_user(db):
    """Create a staff user."""
    return User.objects.create_user(
        email="staff@example.com",
        password="testpass123",
        is_staff=True
    )


@pytest.fixture
def superuser(db):
    """Create a superuser."""
    return User.objects.create_superuser(
        email="admin@example.com",
        password="testpass123"
    )


@pytest.fixture
def regular_user(db):
    """Create a regular user."""
    return User.objects.create_user(
        email="user@example.com",
        password="testpass123"
    )


@pytest.fixture
def rf():
    """Request factory."""
    return RequestFactory()


@pytest.mark.django_db
class TestImpersonationMiddleware:
    """Test ImpersonationMiddleware."""

    def test_middleware_without_impersonation(self, rf, regular_user):
        """Test middleware does nothing without impersonation."""
        def get_response(request):
            return None

        middleware = ImpersonationMiddleware(get_response)

        request = rf.get("/")
        request.user = regular_user
        request.session = {}

        middleware(request)

        assert request.user == regular_user
        assert not hasattr(request, "is_impersonating")

    def test_middleware_with_impersonation(self, rf, staff_user, regular_user):
        """Test middleware swaps user when impersonating."""
        def get_response(request):
            return None

        middleware = ImpersonationMiddleware(get_response)

        request = rf.get("/")
        request.user = staff_user
        request.session = {"impersonate_id": regular_user.id}

        middleware(request)

        assert request.user == regular_user
        assert request.real_user == staff_user
        assert request.is_impersonating is True

    def test_middleware_with_invalid_user_id(self, rf, staff_user):
        """Test middleware clears invalid impersonate_id."""
        def get_response(request):
            return None

        middleware = ImpersonationMiddleware(get_response)

        request = rf.get("/")
        request.user = staff_user
        request.session = {"impersonate_id": 99999}  # Non-existent

        middleware(request)

        assert request.user == staff_user
        assert "impersonate_id" not in request.session


@pytest.mark.django_db
class TestImpersonationViews:
    """Test impersonation views."""

    def test_impersonate_as_staff(self, client, staff_user, regular_user):
        """Test staff can impersonate users."""
        client.force_login(staff_user)

        response = client.get(
            reverse("users:impersonate", kwargs={"user_id": regular_user.id})
        )

        assert response.status_code == 302
        assert client.session.get("impersonate_id") == regular_user.id

    def test_impersonate_as_non_staff(self, client, regular_user):
        """Test non-staff cannot impersonate."""
        another_user = User.objects.create_user(
            email="another@example.com",
            password="testpass123"
        )

        client.force_login(regular_user)

        response = client.get(
            reverse("users:impersonate", kwargs={"user_id": another_user.id})
        )

        assert response.status_code == 302  # Redirect
        assert "impersonate_id" not in client.session

    def test_cannot_impersonate_superuser_as_staff(self, client, staff_user, superuser):
        """Test staff cannot impersonate superusers."""
        client.force_login(staff_user)

        response = client.get(
            reverse("users:impersonate", kwargs={"user_id": superuser.id})
        )

        assert response.status_code == 302
        assert "impersonate_id" not in client.session

    def test_can_impersonate_superuser_as_superuser(self, client, superuser):
        """Test superuser can impersonate other superusers."""
        another_super = User.objects.create_superuser(
            email="another_admin@example.com",
            password="testpass123"
        )

        client.force_login(superuser)

        response = client.get(
            reverse("users:impersonate", kwargs={"user_id": another_super.id})
        )

        assert response.status_code == 302
        assert client.session.get("impersonate_id") == another_super.id

    def test_cannot_impersonate_self(self, client, staff_user):
        """Test cannot impersonate yourself."""
        client.force_login(staff_user)

        response = client.get(
            reverse("users:impersonate", kwargs={"user_id": staff_user.id})
        )

        assert response.status_code == 302
        assert "impersonate_id" not in client.session

    def test_stop_impersonating(self, client, staff_user, regular_user):
        """Test stopping impersonation."""
        client.force_login(staff_user)

        # Start impersonating
        client.get(
            reverse("users:impersonate", kwargs={"user_id": regular_user.id})
        )

        assert "impersonate_id" in client.session

        # Stop impersonating
        response = client.get(reverse("users:stop_impersonate"))

        assert response.status_code == 302
        assert "impersonate_id" not in client.session


@pytest.mark.django_db
class TestPreventWhileImpersonatingDecorator:
    """Test prevent_while_impersonating decorator."""

    def test_allows_when_not_impersonating(self, rf, regular_user):
        """Test decorator allows access when not impersonating."""
        from django.http import HttpResponse

        @prevent_while_impersonating
        def view(request):
            return HttpResponse("Success")

        request = rf.get("/")
        request.user = regular_user
        request.is_impersonating = False

        response = view(request)

        assert response.status_code == 200

    def test_blocks_when_impersonating(self, rf, staff_user):
        """Test decorator blocks access when impersonating."""
        @prevent_while_impersonating
        def view(request):
            from django.http import HttpResponse
            return HttpResponse("Success")

        request = rf.get("/")
        request.user = staff_user
        request.is_impersonating = True

        response = view(request)

        assert response.status_code == 302  # Redirect
