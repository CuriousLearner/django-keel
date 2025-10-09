# 🚩 Feature Flags

Enable A/B testing, gradual rollouts, and feature toggles with django-waffle.

## Overview

Feature flags allow you to:

- **A/B test** new features with a subset of users
- **Gradually roll out** features to minimize risk
- **Toggle features** on/off without deploying code
- **Test in production** safely with specific users/groups
- **Emergency rollback** by disabling a flag

Django Keel integrates [django-waffle](https://waffle.readthedocs.io/) for production-ready feature flagging.

## Types of Flags

### 1. Flags (User-based)

Enable features for specific users:

```python
from waffle import flag_is_active

if flag_is_active(request, 'new_dashboard'):
    # Show new dashboard
    return render(request, 'dashboard_v2.html')
else:
    # Show old dashboard
    return render(request, 'dashboard_v1.html')
```

### 2. Switches (Global)

Enable features globally for everyone:

```python
from waffle import switch_is_active

if switch_is_active('maintenance_mode'):
    return render(request, 'maintenance.html')
```

### 3. Samples (Percentage-based)

Enable features for a percentage of users:

```python
from waffle import sample_is_active

if sample_is_active('beta_features'):
    # 10% of users see beta features
    show_beta_features()
```

## Setup

### 1. Enable Feature Flags

When generating your project, feature flags are included by default in Django Keel projects.

Check `config/settings/base.py`:

```python
INSTALLED_APPS = [
    # ...
    'waffle',
    # ...
]

MIDDLEWARE = [
    # ...
    'waffle.middleware.WaffleMiddleware',
    # ...
]
```

### 2. Run Migrations

```bash
python manage.py migrate waffle
```

### 3. Access Admin Interface

Visit `/admin/waffle/` to manage flags, switches, and samples.

## Creating Flags

### Via Admin Interface

1. Go to `/admin/waffle/flag/`
2. Click "Add Flag"
3. Configure:
   - **Name**: `new_dashboard`
   - **Everyone**: Off (default)
   - **Percent**: 0 (or 10 for 10% rollout)
   - **Superusers**: On (enable for staff testing)
   - **Groups**: Select specific groups
   - **Users**: Add specific users

### Via Django Shell

```python
from waffle.models import Flag

# Create a flag
flag = Flag.objects.create(
    name='new_dashboard',
    everyone=False,
    percent=10.0,  # 10% of users
    superusers=True
)

# Enable for specific users
from django.contrib.auth import get_user_model
User = get_user_model()
user = User.objects.get(email='beta@example.com')
flag.users.add(user)
```

### Via Management Command

Django Keel provides helper commands:

```bash
# Create a flag
python manage.py waffle_flag new_dashboard --create

# Enable for everyone
python manage.py waffle_flag new_dashboard --everyone

# Enable for 25% of users
python manage.py waffle_flag new_dashboard --percent 25

# Disable
python manage.py waffle_flag new_dashboard --deactivate
```

## Usage in Views

### Function-Based Views

```python
from waffle.decorators import waffle_flag

@waffle_flag('new_dashboard')
def dashboard_view(request):
    """Only accessible when flag is active."""
    return render(request, 'dashboard_v2.html')
```

### Class-Based Views

```python
from waffle.mixins import WaffleFlagMixin

class DashboardView(WaffleFlagMixin, TemplateView):
    waffle_flag = 'new_dashboard'
    template_name = 'dashboard_v2.html'
```

### Conditional Logic

```python
from waffle import flag_is_active

def dashboard_view(request):
    if flag_is_active(request, 'new_dashboard'):
        context = get_new_dashboard_context()
        template = 'dashboard_v2.html'
    else:
        context = get_old_dashboard_context()
        template = 'dashboard_v1.html'

    return render(request, template, context)
```

## Usage in Templates

### Check Flag Status

```django
{% load waffle_tags %}

{% flag "new_dashboard" %}
  <div class="new-dashboard">
    <!-- New dashboard content -->
  </div>
{% else %}
  <div class="old-dashboard">
    <!-- Old dashboard content -->
  </div>
{% endflag %}
```

### Check Switch Status

```django
{% load waffle_tags %}

{% switch "maintenance_mode" %}
  <div class="alert alert-warning">
    Site is under maintenance. Some features may be unavailable.
  </div>
{% endswitch %}
```

## Usage in API (DRF)

### Conditional Endpoints

```python
from rest_framework.decorators import api_view
from waffle import flag_is_active

@api_view(['GET'])
def api_dashboard(request):
    if flag_is_active(request, 'new_dashboard_api'):
        serializer = DashboardV2Serializer
    else:
        serializer = DashboardV1Serializer

    data = get_dashboard_data()
    return Response(serializer(data).data)
```

### Feature Availability in Response

```python
from waffle import flag_is_active

class FeatureListView(APIView):
    def get(self, request):
        return Response({
            'features': {
                'new_dashboard': flag_is_active(request, 'new_dashboard'),
                'dark_mode': flag_is_active(request, 'dark_mode'),
                'ai_assistant': flag_is_active(request, 'ai_assistant'),
            }
        })
```

## Common Patterns

### Gradual Rollout

Start with 1% and increase gradually:

```python
# Day 1: 1% of users
flag.percent = 1.0
flag.save()

# Day 3: 10% of users (monitor metrics)
flag.percent = 10.0
flag.save()

# Day 7: 50% of users
flag.percent = 50.0
flag.save()

# Day 14: 100% of users
flag.everyone = True
flag.save()
```

### Canary Releases

Enable for internal users first:

```python
# Enable for superusers only
flag.superusers = True
flag.everyone = False

# Then enable for beta testers group
beta_group = Group.objects.get(name='Beta Testers')
flag.groups.add(beta_group)

# Finally, gradual rollout to all users
flag.percent = 10.0
flag.save()
```

### A/B Testing

Split users into control and treatment groups:

```python
# Create two flags for A/B test
flag_a = Flag.objects.create(name='checkout_v1', percent=50.0)
flag_b = Flag.objects.create(name='checkout_v2', percent=50.0)

# In view
if flag_is_active(request, 'checkout_v2'):
    return checkout_v2(request)
else:
    return checkout_v1(request)

# Track conversions
if flag_is_active(request, 'checkout_v2'):
    analytics.track('purchase', {'variant': 'v2'})
```

### Emergency Kill Switch

Quickly disable problematic features:

```python
from waffle.models import Switch

# Create kill switch
Switch.objects.create(name='new_payment_processor', active=True)

# In code
from waffle import switch_is_active

if switch_is_active('new_payment_processor'):
    process_payment_v2()
else:
    process_payment_v1()  # Fallback to old processor

# Emergency disable (via admin or shell)
switch = Switch.objects.get(name='new_payment_processor')
switch.active = False
switch.save()
```

## Testing with Feature Flags

### Override Flags in Tests

```python
from waffle.testutils import override_flag

class DashboardTestCase(TestCase):
    @override_flag('new_dashboard', active=True)
    def test_new_dashboard(self):
        response = self.client.get('/dashboard/')
        self.assertContains(response, 'New Dashboard')

    @override_flag('new_dashboard', active=False)
    def test_old_dashboard(self):
        response = self.client.get('/dashboard/')
        self.assertContains(response, 'Old Dashboard')
```

### Test Both Variants

```python
from waffle.testutils import override_flag

class CheckoutTestCase(TestCase):
    def test_checkout_variants(self):
        # Test new checkout
        with override_flag('checkout_v2', active=True):
            response = self.client.post('/checkout/', data)
            self.assertEqual(response.status_code, 200)

        # Test old checkout
        with override_flag('checkout_v2', active=False):
            response = self.client.post('/checkout/', data)
            self.assertEqual(response.status_code, 200)
```

## Monitoring & Analytics

### Track Flag Usage

```python
import logging
from waffle import flag_is_active

logger = logging.getLogger(__name__)

def my_view(request):
    flag_active = flag_is_active(request, 'new_feature')

    # Log flag usage
    logger.info(
        'feature_flag_check',
        extra={
            'flag_name': 'new_feature',
            'user_id': request.user.id,
            'is_active': flag_active,
        }
    )

    if flag_active:
        return new_feature_view(request)
    return old_feature_view(request)
```

### Integration with Analytics

```python
from waffle import flag_is_active

def checkout_view(request):
    variant = 'v2' if flag_is_active(request, 'checkout_v2') else 'v1'

    # Track with your analytics service
    analytics.track(request.user.id, 'checkout_started', {
        'variant': variant,
    })

    return render(request, f'checkout_{variant}.html')
```

## Best Practices

1. **Use descriptive names** - `new_dashboard_redesign` not `flag_123`
2. **Document flags** - Add notes in admin about what each flag does
3. **Clean up old flags** - Remove flags after full rollout
4. **Monitor metrics** - Track conversion rates for each variant
5. **Test both paths** - Write tests for flag on AND off
6. **Use switches for kill switches** - Faster than flags
7. **Avoid flag sprawl** - Consolidate related flags
8. **Set expiration dates** - Remove temporary flags after rollout

## Troubleshooting

### Flag Not Working

**Check middleware is installed:**
```python
# config/settings/base.py
MIDDLEWARE = [
    # ...
    'waffle.middleware.WaffleMiddleware',  # Must be here
    # ...
]
```

**Check flag configuration:**
```python
from waffle.models import Flag
flag = Flag.objects.get(name='my_flag')
print(f"Everyone: {flag.everyone}")
print(f"Percent: {flag.percent}")
print(f"Active: {flag.is_active_for_user(user)}")
```

### Flag Always Returns False

**Check user authentication:**
```python
# Flags require authenticated users for user-based checks
if not request.user.is_authenticated:
    # Flag will be False unless everyone=True
    pass
```

**Use switches for anonymous users:**
```python
from waffle import switch_is_active

# Works for all users (anonymous or authenticated)
if switch_is_active('new_feature'):
    show_feature()
```

### Performance Issues

**Cache flag lookups:**
```python
from django.core.cache import cache
from waffle import flag_is_active

def get_flag_status(request, flag_name):
    cache_key = f'flag_{flag_name}_{request.user.id}'
    status = cache.get(cache_key)

    if status is None:
        status = flag_is_active(request, flag_name)
        cache.set(cache_key, status, 60)  # Cache for 1 minute

    return status
```

## API Reference

### Helper Functions

Django Keel provides helper functions in `apps/core/feature_flags.py`:

```python
from apps.core.feature_flags import (
    is_feature_enabled,
    get_active_features,
    enable_feature_for_user,
)

# Check if feature is enabled
if is_feature_enabled('new_dashboard', user=request.user):
    show_new_dashboard()

# Get all active features for user
features = get_active_features(request.user)
# Returns: {'new_dashboard': True, 'dark_mode': False, ...}

# Enable feature for specific user
enable_feature_for_user('beta_access', user)
```

## Further Reading

- [django-waffle Documentation](https://waffle.readthedocs.io/)
- [Feature Flag Best Practices](https://www.optimizely.com/optimization-glossary/feature-flags/)
- [A/B Testing Guide](https://vwo.com/ab-testing/)

## Related Documentation

- [Feature Gating](feature-gating.md) - Subscription-based access control
- [Stripe Integration](stripe.md) - Payment and subscription management
- [Teams & Organizations](teams.md) - Multi-tenant team management
