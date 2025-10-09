# 👤 User Impersonation

Allow staff members to impersonate users for debugging, support, and testing purposes.

## Overview

User impersonation enables your support team to:

- **Debug user issues** - See exactly what users see
- **Provide support** - Help users with complex workflows
- **Test permissions** - Verify access controls work correctly
- **Reproduce bugs** - Experience issues from user's perspective
- **Maintain audit trail** - All impersonation is logged

Django Keel provides secure impersonation with middleware, views, and safety controls.

## How It Works

1. **Staff initiates** - Only staff/superuser can start impersonation
2. **Session storage** - User ID stored in session
3. **Request swapping** - `request.user` becomes impersonated user
4. **Original preserved** - `request.real_user` remains staff member
5. **Automatic logging** - All actions logged for security audit
6. **Easy exit** - Staff can stop impersonation anytime

## Setup

### 1. Enable Middleware

Ensure `ImpersonationMiddleware` is in your settings:

```python
# config/settings/base.py
MIDDLEWARE = [
    # ...
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'apps.users.impersonation.ImpersonationMiddleware',  # Add after auth
    # ...
]
```

**Important:** Place after `AuthenticationMiddleware`.

### 2. Add Context Processor

Enable template context for impersonation status:

```python
# config/settings/base.py
TEMPLATES = [
    {
        'OPTIONS': {
            'context_processors': [
                # ...
                'apps.users.impersonation.impersonation_context',
            ],
        },
    },
]
```

### 3. Include URLs

URLs are automatically included with `apps/users/urls.py`:

```python
# apps/users/urls.py
from django.urls import path
from .impersonation import ImpersonateView, StopImpersonateView

urlpatterns = [
    # ...
    path('impersonate/<int:user_id>/', ImpersonateView.as_view(), name='impersonate'),
    path('stop-impersonate/', StopImpersonateView.as_view(), name='stop_impersonate'),
]
```

## Usage

### Start Impersonation

#### Via URL

```python
# Visit directly
/users/impersonate/<user_id>/

# With redirect after impersonation
/users/impersonate/<user_id>/?next=/dashboard/
```

#### Via Admin Action

Django admin includes an action to impersonate from user list:

1. Go to Django admin → Users
2. Select user to impersonate (only one)
3. Choose "Impersonate selected user" action
4. You'll be redirected to the app as that user

#### Programmatically

```python
from django.shortcuts import redirect

def some_view(request):
    # Start impersonating user ID 42
    request.session['impersonate_id'] = 42
    return redirect('dashboard')
```

### Stop Impersonation

#### Via URL

```python
# Stop and return to admin
/users/stop-impersonate/

# Stop and redirect elsewhere
/users/stop-impersonate/?next=/custom/url/
```

#### Programmatically

```python
def stop_impersonating(request):
    if 'impersonate_id' in request.session:
        del request.session['impersonate_id']
    return redirect('admin:index')
```

## Permission Checks

### Who Can Impersonate

By default:

- **Staff** can impersonate regular users
- **Staff cannot** impersonate superusers
- **Superusers can** impersonate anyone (including other superusers)
- **Nobody can** impersonate themselves

### Security Rules

The `ImpersonateView` enforces:

```python
# Only staff can impersonate
if not request.user.is_staff:
    return redirect('/')  # Permission denied

# Staff cannot impersonate superusers
if user.is_superuser and not request.user.is_superuser:
    return redirect('admin:index')  # Cannot impersonate superusers

# Cannot impersonate yourself
if user.pk == request.user.pk:
    return redirect('admin:index')  # Cannot impersonate yourself
```

## Template Integration

### Display Impersonation Banner

Show a banner when staff is impersonating:

```django
{% if is_impersonating %}
<div class="impersonation-banner">
  <span class="warning-icon">⚠️</span>
  You are impersonating <strong>{{ user.email }}</strong>
  as <strong>{{ real_user.email }}</strong>

  <a href="{% url 'users:stop_impersonate' %}" class="btn btn-warning">
    Stop Impersonating
  </a>
</div>
{% endif %}
```

### Conditional Features

Show different UI when impersonating:

```django
{% if is_impersonating %}
  <div class="alert alert-info">
    <p>Viewing as {{ user.email }}</p>
    <p>Actual user: {{ real_user.email }}</p>
  </div>
{% endif %}
```

### Hide Sensitive Actions

```django
{% if not is_impersonating %}
  <a href="{% url 'billing:cancel_subscription' %}">Cancel Subscription</a>
{% else %}
  <span class="text-muted">
    (Action disabled during impersonation)
  </span>
{% endif %}
```

## Preventing Actions While Impersonating

### Decorator for Function-Based Views

Prevent sensitive actions while impersonating:

```python
from apps.users.impersonation import prevent_while_impersonating

@prevent_while_impersonating
def delete_account(request):
    """This cannot be done while impersonating."""
    request.user.delete()
    return redirect('goodbye')
```

**Behavior:** Returns error message and redirects to `/` if impersonating.

### Mixin for Class-Based Views

```python
from apps.users.impersonation import PreventWhileImpersonatingMixin

class DeleteAccountView(PreventWhileImpersonatingMixin, View):
    """Cannot delete account while impersonating."""

    def post(self, request):
        request.user.delete()
        return redirect('goodbye')
```

### Manual Check

```python
def sensitive_action(request):
    if request.is_impersonating:
        messages.error(request, "Cannot perform this action while impersonating.")
        return redirect('dashboard')

    # Proceed with sensitive action
    ...
```

## Accessing Real User

When impersonating, you have access to both users:

```python
def my_view(request):
    if request.is_impersonating:
        # request.user = The impersonated user
        # request.real_user = The staff member

        print(f"Viewing as: {request.user.email}")
        print(f"Actually: {request.real_user.email}")
    else:
        # request.user = The authenticated user
        # request.is_impersonating = False
        pass
```

**Use cases:**

- **Audit logging:** Record who performed action while impersonating
- **Permission checks:** Use `real_user` for staff-only operations
- **Analytics:** Track impersonation sessions

## Logging and Audit Trail

All impersonation is automatically logged:

### Start Impersonation

```python
# Logged at WARNING level
logger.warning(
    f"IMPERSONATION: {request.user.email} (ID: {request.user.pk}) "
    f"started impersonating {user_to_impersonate.email} (ID: {user_to_impersonate.pk})"
)
```

### During Impersonation

```python
# Logged at INFO level for each request
logger.info(
    f"User {request.real_user.email} is impersonating {request.user.email}"
)
```

### Stop Impersonation

```python
# Logged at INFO level
logger.info(
    f"IMPERSONATION ENDED: {request.real_user.email} "
    f"stopped impersonating {impersonated_user.email}"
)
```

### Viewing Logs

```bash
# Filter for impersonation events
grep "IMPERSONATION" logs/django.log

# Example output:
# 2025-01-09 10:30:15 WARNING IMPERSONATION: admin@example.com (ID: 1) started impersonating user@example.com (ID: 42)
# 2025-01-09 10:45:22 INFO IMPERSONATION ENDED: admin@example.com stopped impersonating user@example.com
```

## Testing

### Unit Tests

Test impersonation functionality:

```python
import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


@pytest.mark.django_db
class TestImpersonation:
    def test_staff_can_impersonate_user(self, client):
        """Test staff can impersonate regular users."""
        staff = User.objects.create_user(
            email='staff@example.com',
            password='testpass',
            is_staff=True
        )
        user = User.objects.create_user(
            email='user@example.com',
            password='testpass'
        )

        client.force_login(staff)
        response = client.get(
            reverse('users:impersonate', kwargs={'user_id': user.id})
        )

        assert response.status_code == 302
        assert client.session.get('impersonate_id') == user.id

    def test_staff_cannot_impersonate_superuser(self, client):
        """Test staff cannot impersonate superusers."""
        staff = User.objects.create_user(
            email='staff@example.com',
            password='testpass',
            is_staff=True
        )
        superuser = User.objects.create_superuser(
            email='admin@example.com',
            password='testpass'
        )

        client.force_login(staff)
        response = client.get(
            reverse('users:impersonate', kwargs={'user_id': superuser.id})
        )

        assert 'impersonate_id' not in client.session

    def test_stop_impersonation(self, client):
        """Test stopping impersonation."""
        staff = User.objects.create_user(
            email='staff@example.com',
            password='testpass',
            is_staff=True
        )
        user = User.objects.create_user(
            email='user@example.com',
            password='testpass'
        )

        client.force_login(staff)

        # Start impersonating
        client.get(reverse('users:impersonate', kwargs={'user_id': user.id}))
        assert 'impersonate_id' in client.session

        # Stop impersonating
        client.get(reverse('users:stop_impersonate'))
        assert 'impersonate_id' not in client.session
```

### Integration Tests

Test with middleware:

```python
@pytest.mark.django_db
def test_middleware_swaps_user(rf, staff_user, regular_user):
    """Test middleware swaps request.user during impersonation."""
    from apps.users.impersonation import ImpersonationMiddleware

    def get_response(request):
        return None

    middleware = ImpersonationMiddleware(get_response)

    request = rf.get('/')
    request.user = staff_user
    request.session = {'impersonate_id': regular_user.id}

    middleware(request)

    assert request.user == regular_user
    assert request.real_user == staff_user
    assert request.is_impersonating is True
```

## Common Patterns

### View User Dashboard As Them

```python
def impersonate_and_view_dashboard(request, user_id):
    """Quick helper to impersonate and view user's dashboard."""
    if not request.user.is_staff:
        return redirect('/')

    request.session['impersonate_id'] = user_id
    return redirect('user_dashboard')
```

### Impersonate from Support Ticket

```python
class SupportTicketView(StaffRequiredMixin, DetailView):
    model = SupportTicket

    def post(self, request, *args, **kwargs):
        ticket = self.get_object()

        # Start impersonating ticket creator
        request.session['impersonate_id'] = ticket.created_by.id

        messages.success(
            request,
            f"Now viewing as {ticket.created_by.email} to debug issue."
        )

        # Redirect to page where issue occurs
        return redirect(ticket.problem_url)
```

### Time-Limited Impersonation

```python
from django.utils import timezone
from datetime import timedelta

def start_timed_impersonation(request, user_id, minutes=30):
    """Start impersonation that expires after N minutes."""
    request.session['impersonate_id'] = user_id
    request.session['impersonate_expires'] = (
        timezone.now() + timedelta(minutes=minutes)
    ).isoformat()

    return redirect('/')


# In middleware or view
def check_impersonation_expiry(request):
    """Check if impersonation has expired."""
    if 'impersonate_expires' in request.session:
        expires = timezone.datetime.fromisoformat(
            request.session['impersonate_expires']
        )

        if timezone.now() > expires:
            # Expired, stop impersonation
            del request.session['impersonate_id']
            del request.session['impersonate_expires']
            messages.warning(request, "Impersonation session expired.")
```

## Security Best Practices

1. **Restrict to staff** - Only allow trusted team members
2. **Log everything** - Maintain audit trail of all impersonation
3. **Block sensitive actions** - Prevent deletion, payments while impersonating
4. **Time limits** - Consider expiring impersonation sessions
5. **Visual indicators** - Always show banner when impersonating
6. **Review logs regularly** - Monitor for abuse
7. **Don't store credentials** - Never ask staff for user passwords
8. **Document procedures** - Train support team on proper usage

## Troubleshooting

### Impersonation Not Working

**Symptoms:** Session not storing user ID, always redirected

**Solutions:**

1. Check middleware is installed:
   ```python
   # config/settings/base.py
   MIDDLEWARE = [
       # ...
       'apps.users.impersonation.ImpersonationMiddleware',
   ]
   ```

2. Ensure sessions are enabled:
   ```python
   MIDDLEWARE = [
       'django.contrib.sessions.middleware.SessionMiddleware',  # Required
       # ...
   ]
   ```

3. Check staff permissions:
   ```python
   user.is_staff  # Must be True
   ```

### Impersonation Doesn't Stop

**Symptoms:** Session persists after clicking "Stop"

**Solutions:**

1. Clear session manually:
   ```python
   # In Django shell
   from django.contrib.sessions.models import Session
   Session.objects.all().delete()
   ```

2. Check for middleware conflicts
3. Verify `StopImpersonateView` is being called

### Can't Impersonate Superusers

**Expected behavior:** Staff cannot impersonate superusers for security.

**Solution:** Login as superuser to impersonate other superusers.

### Template Context Not Available

**Symptoms:** `is_impersonating` undefined in templates

**Solution:** Add context processor:

```python
# config/settings/base.py
TEMPLATES = [
    {
        'OPTIONS': {
            'context_processors': [
                # ...
                'apps.users.impersonation.impersonation_context',
            ],
        },
    },
]
```

## Alternative Implementations

### Django Hijack

For more features, consider [django-hijack](https://github.com/django-hijack/django-hijack):

```bash
pip install django-hijack
```

**Features:**
- Admin integration
- Release notifications
- History tracking
- Toolbar integration

**Trade-off:** More dependencies, heavier implementation.

### Custom Requirements

Extend Django Keel's impersonation:

```python
# Custom middleware with extra checks
class CustomImpersonationMiddleware(ImpersonationMiddleware):
    def __call__(self, request):
        # Add IP whitelisting
        if request.is_impersonating:
            allowed_ips = ['192.168.1.1', '10.0.0.1']
            if request.META.get('REMOTE_ADDR') not in allowed_ips:
                del request.session['impersonate_id']
                messages.error(request, "Impersonation not allowed from this IP")

        return super().__call__(request)
```

## API Reference

### Middleware

**`ImpersonationMiddleware`**

- Swaps `request.user` with impersonated user
- Sets `request.real_user` to original staff user
- Sets `request.is_impersonating = True/False`

### Views

**`ImpersonateView(user_id)`**
- Start impersonating user
- GET parameter `next` for redirect after start

**`StopImpersonateView()`**
- Stop impersonating and restore original user
- GET parameter `next` for redirect after stop

### Decorators

**`@prevent_while_impersonating`**
- Blocks view execution if impersonating
- Returns redirect to `/` with error message

### Mixins

**`PreventWhileImpersonatingMixin`**
- Class-based view mixin
- Blocks dispatch if impersonating

### Context Processor

**`impersonation_context(request)`**
- Returns `{'is_impersonating': bool, 'real_user': User|None}`

### Admin Action

**`impersonate_user_admin_action`**
- Admin action to impersonate from user list
- Select exactly one user

## Further Reading

- [Django Sessions](https://docs.djangoproject.com/en/stable/topics/http/sessions/)
- [Django Middleware](https://docs.djangoproject.com/en/stable/topics/http/middleware/)
- [django-hijack](https://github.com/django-hijack/django-hijack) - Alternative package

## Related Documentation

- [Teams](teams.md) - Impersonate team members for support
- [Feature Gating](feature-gating.md) - Test subscription access as users
- [Feature Flags](feature-flags.md) - Test feature rollouts as different users
