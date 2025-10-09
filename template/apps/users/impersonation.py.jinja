"""User impersonation for admin support."""
import logging
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import View

User = get_user_model()
logger = logging.getLogger(__name__)


class ImpersonationMiddleware:
    """
    Middleware to allow staff users to impersonate other users.

    Stores the impersonated user ID in the session and swaps request.user.
    The original user is preserved for permission checks.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if impersonating
        impersonate_id = request.session.get("impersonate_id")

        if impersonate_id:
            try:
                # Get the impersonated user
                impersonated_user = User.objects.get(pk=impersonate_id)

                # Store the real user for permission checks
                request.real_user = request.user

                # Replace request.user with impersonated user
                request.user = impersonated_user

                # Mark that we're impersonating
                request.is_impersonating = True

                logger.info(
                    f"User {request.real_user.email} is impersonating {impersonated_user.email}"
                )

            except User.DoesNotExist:
                # Invalid user ID, clear impersonation
                logger.warning(f"Invalid impersonate_id: {impersonate_id}")
                del request.session["impersonate_id"]
                request.is_impersonating = False
        else:
            request.is_impersonating = False

        response = self.get_response(request)
        return response


class ImpersonateView(View):
    """Start impersonating a user."""

    def get(self, request, user_id):
        # Only staff can impersonate
        if not request.user.is_staff:
            messages.error(request, _("Permission denied."))
            return redirect("/")

        # Get the user to impersonate
        user_to_impersonate = get_object_or_404(User, pk=user_id)

        # Prevent impersonating superusers (unless you're a superuser)
        if user_to_impersonate.is_superuser and not request.user.is_superuser:
            messages.error(request, _("Cannot impersonate superusers."))
            return redirect("admin:index")

        # Prevent impersonating yourself
        if user_to_impersonate.pk == request.user.pk:
            messages.warning(request, _("Cannot impersonate yourself."))
            return redirect("admin:index")

        # Store impersonation in session
        request.session["impersonate_id"] = user_id

        # Log the impersonation
        logger.warning(
            f"IMPERSONATION: {request.user.email} (ID: {request.user.pk}) "
            f"started impersonating {user_to_impersonate.email} (ID: {user_to_impersonate.pk})"
        )

        messages.success(
            request,
            _("You are now impersonating {user}").format(user=user_to_impersonate.email)
        )

        # Redirect to homepage or specified URL
        next_url = request.GET.get("next", "/")
        return redirect(next_url)


class StopImpersonateView(View):
    """Stop impersonating and return to original user."""

    def get(self, request):
        if not request.is_impersonating:
            messages.info(request, _("You are not impersonating anyone."))
            return redirect("/")

        # Get the impersonated user for logging
        impersonated_user = request.user

        # Clear impersonation
        del request.session["impersonate_id"]

        # Log the end of impersonation
        logger.info(
            f"IMPERSONATION ENDED: {request.real_user.email} "
            f"stopped impersonating {impersonated_user.email}"
        )

        messages.success(request, _("You have stopped impersonating."))

        # Redirect to admin or specified URL
        next_url = request.GET.get("next", reverse("admin:index"))
        return redirect(next_url)


# Template context processor to add impersonation info
def impersonation_context(request):
    """Add impersonation info to template context."""
    return {
        "is_impersonating": getattr(request, "is_impersonating", False),
        "real_user": getattr(request, "real_user", None),
    }


# Admin action to impersonate from user list
def impersonate_user_admin_action(modeladmin, request, queryset):
    """Admin action to impersonate a user."""
    if queryset.count() != 1:
        messages.error(request, _("Please select exactly one user to impersonate."))
        return

    user = queryset.first()

    # Check permissions
    if not request.user.is_staff:
        messages.error(request, _("Permission denied."))
        return

    if user.is_superuser and not request.user.is_superuser:
        messages.error(request, _("Cannot impersonate superusers."))
        return

    if user.pk == request.user.pk:
        messages.warning(request, _("Cannot impersonate yourself."))
        return

    # Start impersonation
    request.session["impersonate_id"] = user.pk

    logger.warning(
        f"IMPERSONATION: {request.user.email} (ID: {request.user.pk}) "
        f"started impersonating {user.email} (ID: {user.pk}) via admin action"
    )

    messages.success(
        request,
        _("You are now impersonating {user}. Click here to stop: {url}").format(
            user=user.email,
            url=reverse("users:stop_impersonate")
        )
    )


impersonate_user_admin_action.short_description = _("Impersonate selected user")


# Decorator to prevent actions while impersonating
def prevent_while_impersonating(view_func):
    """
    Decorator to prevent certain actions while impersonating.

    Usage:
        @prevent_while_impersonating
        def sensitive_view(request):
            ...
    """
    from functools import wraps

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if getattr(request, "is_impersonating", False):
            messages.error(
                request,
                _("This action cannot be performed while impersonating.")
            )
            return redirect("/")

        return view_func(request, *args, **kwargs)

    return wrapper


# Class-based view mixin
class PreventWhileImpersonatingMixin:
    """Mixin to prevent access while impersonating."""

    def dispatch(self, request, *args, **kwargs):
        if getattr(request, "is_impersonating", False):
            messages.error(
                request,
                _("This action cannot be performed while impersonating.")
            )
            return redirect("/")

        return super().dispatch(request, *args, **kwargs)
