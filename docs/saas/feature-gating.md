# 🔒 Feature Gating

Control access to features based on subscription plans and usage limits.

## Overview

Feature gating allows you to:

- **Restrict features** by subscription tier (Free, Pro, Enterprise)
- **Enforce usage limits** (API calls, storage, users per team)
- **Monetize features** with clear upgrade paths
- **Prevent feature creep** in lower tiers
- **Encourage upgrades** with locked premium features

Django Keel provides decorators, mixins, and utilities for subscription-based access control.

## Quick Start

### Enable Feature Gating

When generating your project with `use_stripe: advanced`, feature gating is automatically included.

Check `apps/billing/decorators.py` exists in your generated project.

### Basic Usage

```python
from apps.billing.decorators import subscription_required, feature_required

@subscription_required
@feature_required('advanced_analytics')
def analytics_view(request):
    """Only accessible to users with active subscription and feature."""
    return render(request, 'analytics.html')
```

## Decorators

### @subscription_required

Ensures user has an active subscription:

```python
from apps.billing.decorators import subscription_required

@subscription_required
def premium_feature(request):
    """Requires any active subscription."""
    return render(request, 'premium.html')
```

**Behavior:**
- ✅ User with active subscription → Access granted
- ❌ No subscription → Redirect to pricing page
- ❌ Expired subscription → Show renewal prompt

### @feature_required

Checks if subscription includes specific feature:

```python
from apps.billing.decorators import feature_required

@feature_required('api_access')
def api_dashboard(request):
    """Requires subscription with API access feature."""
    return render(request, 'api_dashboard.html')
```

**Behavior:**
- ✅ Feature included in plan → Access granted
- ❌ Feature not included → Show upgrade prompt
- ❌ No subscription → Redirect to pricing

### @plan_required

Requires specific subscription tier:

```python
from apps.billing.decorators import plan_required

@plan_required('pro')
def pro_only_feature(request):
    """Only for Pro tier subscribers."""
    return render(request, 'pro_feature.html')

@plan_required(['pro', 'enterprise'])
def premium_feature(request):
    """For Pro or Enterprise subscribers."""
    return render(request, 'premium.html')
```

### @usage_limit

Enforces usage limits:

```python
from apps.billing.decorators import usage_limit

@usage_limit('api_calls', limit=1000, period='month')
def api_endpoint(request):
    """Limited to 1000 calls per month."""
    # Usage is tracked automatically
    return JsonResponse({'data': 'response'})
```

**Parameters:**
- `limit`: Maximum allowed (integer)
- `period`: `'day'`, `'month'`, `'year'`, or `'lifetime'`
- `resource`: Name of the resource being limited

## Class-Based Views

### SubscriptionRequiredMixin

```python
from apps.billing.mixins import SubscriptionRequiredMixin
from django.views.generic import TemplateView

class PremiumDashboard(SubscriptionRequiredMixin, TemplateView):
    template_name = 'dashboard.html'
```

### FeatureRequiredMixin

```python
from apps.billing.mixins import FeatureRequiredMixin

class AnalyticsView(FeatureRequiredMixin, TemplateView):
    template_name = 'analytics.html'
    required_feature = 'advanced_analytics'
```

### PlanRequiredMixin

```python
from apps.billing.mixins import PlanRequiredMixin

class EnterpriseView(PlanRequiredMixin, TemplateView):
    template_name = 'enterprise.html'
    required_plans = ['enterprise']
```

### UsageLimitMixin

```python
from apps.billing.mixins import UsageLimitMixin

class APIView(UsageLimitMixin, View):
    usage_resource = 'api_calls'
    usage_limit = 1000
    usage_period = 'month'

    def get(self, request):
        # Usage tracked automatically
        return JsonResponse({'data': 'response'})
```

## Template Usage

### Check Subscription Status

```django
{% load billing_tags %}

{% if user.has_active_subscription %}
  <a href="{% url 'premium_feature' %}">Access Premium Feature</a>
{% else %}
  <a href="{% url 'pricing' %}" class="btn-upgrade">Upgrade to Access</a>
{% endif %}
```

### Check Feature Availability

```django
{% load billing_tags %}

{% if user|has_feature:'advanced_analytics' %}
  <a href="{% url 'analytics' %}">View Analytics</a>
{% else %}
  <div class="feature-locked">
    <span class="lock-icon">🔒</span>
    <p>Analytics requires Pro plan</p>
    <a href="{% url 'upgrade' %}">Upgrade Now</a>
  </div>
{% endif %}
```

### Check Plan

```django
{% load billing_tags %}

{% if user.subscription.plan == 'enterprise' %}
  <div class="enterprise-badge">Enterprise Account</div>
{% endif %}
```

### Show Usage Limits

```django
{% load billing_tags %}

{% get_usage user 'api_calls' as api_usage %}
<div class="usage-meter">
  <p>API Calls: {{ api_usage.current }} / {{ api_usage.limit }}</p>
  <div class="progress-bar">
    <div style="width: {{ api_usage.percentage }}%"></div>
  </div>
  {% if api_usage.is_near_limit %}
    <p class="warning">⚠️ Approaching limit. Consider upgrading.</p>
  {% endif %}
</div>
```

## Programmatic Checks

### Check Subscription

```python
from apps.billing.utils import has_active_subscription

if has_active_subscription(request.user):
    # User can access premium features
    pass
```

### Check Feature

```python
from apps.billing.utils import user_has_feature

if user_has_feature(request.user, 'api_access'):
    # User has API access feature
    api_key = generate_api_key(request.user)
```

### Check Plan

```python
from apps.billing.utils import user_has_plan

if user_has_plan(request.user, 'enterprise'):
    # Enterprise-specific functionality
    enable_white_label()
```

### Check Usage Limit

```python
from apps.billing.utils import check_usage_limit, increment_usage

# Check if user can perform action
can_use, remaining = check_usage_limit(
    request.user,
    resource='api_calls',
    limit=1000
)

if can_use:
    # Perform action
    result = make_api_call()

    # Increment usage counter
    increment_usage(request.user, resource='api_calls')

    return result
else:
    return JsonResponse({
        'error': 'Usage limit exceeded',
        'limit': 1000,
        'remaining': 0
    }, status=429)
```

## API (DRF) Integration

### Subscription Required

```python
from rest_framework.decorators import api_view
from apps.billing.decorators import subscription_required

@api_view(['GET'])
@subscription_required
def premium_api(request):
    """API endpoint requires active subscription."""
    return Response({'data': 'premium data'})
```

### Feature-Based Permissions

```python
from rest_framework.permissions import BasePermission
from apps.billing.utils import user_has_feature

class HasAPIAccess(BasePermission):
    """Custom permission for API access feature."""

    def has_permission(self, request, view):
        return user_has_feature(request.user, 'api_access')

class APIView(APIView):
    permission_classes = [HasAPIAccess]

    def get(self, request):
        return Response({'data': 'api response'})
```

### Rate Limiting by Plan

```python
from rest_framework.throttling import UserRateThrottle
from apps.billing.utils import get_user_plan

class PlanBasedRateThrottle(UserRateThrottle):
    """Different rate limits per plan."""

    def get_rate(self):
        user = self.request.user
        plan = get_user_plan(user)

        rates = {
            'free': '100/day',
            'pro': '1000/day',
            'enterprise': '10000/day',
        }

        return rates.get(plan, '100/day')

class APIView(APIView):
    throttle_classes = [PlanBasedRateThrottle]

    def get(self, request):
        return Response({'data': 'response'})
```

## Plan Configuration

Define plans in `config/settings/base.py`:

```python
SUBSCRIPTION_PLANS = {
    'free': {
        'name': 'Free',
        'price': 0,
        'features': {
            'projects': 3,
            'storage_gb': 1,
            'team_members': 1,
            'api_calls_per_month': 100,
        },
        'includes': ['basic_support'],
    },
    'pro': {
        'name': 'Pro',
        'price': 29,
        'features': {
            'projects': 50,
            'storage_gb': 50,
            'team_members': 10,
            'api_calls_per_month': 10000,
        },
        'includes': [
            'basic_support',
            'advanced_analytics',
            'custom_domains',
            'priority_support',
        ],
    },
    'enterprise': {
        'name': 'Enterprise',
        'price': 99,
        'features': {
            'projects': 'unlimited',
            'storage_gb': 500,
            'team_members': 'unlimited',
            'api_calls_per_month': 100000,
        },
        'includes': [
            'basic_support',
            'advanced_analytics',
            'custom_domains',
            'priority_support',
            'sso',
            'white_label',
            'dedicated_support',
        ],
    },
}
```

## Usage Tracking

### Automatic Tracking

Usage is tracked automatically when using decorators:

```python
@usage_limit('api_calls', limit=1000)
def api_endpoint(request):
    # Usage incremented automatically on successful response
    return JsonResponse({'data': 'response'})
```

### Manual Tracking

For custom scenarios:

```python
from apps.billing.utils import increment_usage, get_usage

# Increment usage
increment_usage(user, resource='api_calls', amount=1)

# Batch increment
increment_usage(user, resource='storage_gb', amount=5.2)

# Get current usage
usage = get_usage(user, resource='api_calls', period='month')
print(f"Used: {usage.current} / {usage.limit}")
```

### Usage Models

```python
from apps.billing.models import Usage

# Get all usage for user this month
usage_records = Usage.objects.filter(
    user=user,
    period_start__month=current_month
)

# Reset usage (e.g., at month start)
Usage.objects.filter(
    user=user,
    resource='api_calls'
).update(current=0)
```

## Upgrade Prompts

### Custom Upgrade Messages

```python
from apps.billing.decorators import feature_required

@feature_required(
    'advanced_analytics',
    upgrade_message="Unlock advanced analytics with Pro plan",
    upgrade_url='/pricing/'
)
def analytics_view(request):
    return render(request, 'analytics.html')
```

### Contextual Upgrade CTAs

```python
from apps.billing.utils import get_upgrade_message

def feature_view(request):
    if not user_has_feature(request.user, 'export_data'):
        upgrade_msg = get_upgrade_message(
            feature='export_data',
            user=request.user
        )
        # upgrade_msg: "Upgrade to Pro to export data"

    context = {'upgrade_message': upgrade_msg}
    return render(request, 'feature.html', context)
```

## Testing

### Mock Subscriptions

```python
from apps.billing.models import Subscription

class FeatureGatingTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test@example.com')

        # Create Pro subscription
        self.subscription = Subscription.objects.create(
            user=self.user,
            plan='pro',
            status='active'
        )

    def test_feature_access(self):
        """Test Pro users can access pro features."""
        self.client.login(email='test@example.com')
        response = self.client.get('/analytics/')
        self.assertEqual(response.status_code, 200)
```

### Test Usage Limits

```python
from apps.billing.utils import increment_usage, check_usage_limit

class UsageLimitTestCase(TestCase):
    def test_usage_enforcement(self):
        """Test usage limits are enforced."""
        user = User.objects.create_user('test@example.com')

        # Use 999 times (just under limit)
        for _ in range(999):
            increment_usage(user, resource='api_calls')

        # Should still have access
        can_use, remaining = check_usage_limit(
            user, resource='api_calls', limit=1000
        )
        self.assertTrue(can_use)
        self.assertEqual(remaining, 1)

        # Use once more (hit limit)
        increment_usage(user, resource='api_calls')

        # Should be blocked
        can_use, remaining = check_usage_limit(
            user, resource='api_calls', limit=1000
        )
        self.assertFalse(can_use)
        self.assertEqual(remaining, 0)
```

## Best Practices

1. **Clear upgrade paths** - Always show what plan includes the feature
2. **Graceful degradation** - Disable features, don't break the app
3. **Usage warnings** - Alert users when approaching limits (80%, 90%)
4. **Feature discoverability** - Show locked features with upgrade CTA
5. **Track metrics** - Monitor which features drive upgrades
6. **Testing** - Test all subscription tiers
7. **Documentation** - Document all gated features clearly
8. **Usage resets** - Reset monthly limits reliably

## Common Patterns

### Tiered Feature Access

```python
def get_project_limit(user):
    """Return project limit based on plan."""
    plan_limits = {
        'free': 3,
        'pro': 50,
        'enterprise': None,  # Unlimited
    }

    plan = get_user_plan(user)
    return plan_limits.get(plan, 3)

def can_create_project(user):
    """Check if user can create more projects."""
    current_count = user.projects.count()
    limit = get_project_limit(user)

    if limit is None:  # Unlimited
        return True

    return current_count < limit
```

### Soft Limits vs Hard Limits

```python
# Soft limit: Allow with warning
if usage > soft_limit:
    messages.warning(
        request,
        f"You're approaching your limit. Consider upgrading."
    )

# Hard limit: Block action
if usage >= hard_limit:
    messages.error(
        request,
        f"Usage limit reached. Please upgrade to continue."
    )
    return redirect('upgrade')
```

### Feature Flags + Gating

Combine feature flags with gating:

```python
from waffle import flag_is_active
from apps.billing.utils import user_has_feature

def advanced_feature_view(request):
    # Check feature flag (gradual rollout)
    if not flag_is_active(request, 'new_analytics'):
        return redirect('dashboard')

    # Check subscription (monetization)
    if not user_has_feature(request.user, 'advanced_analytics'):
        return render(request, 'upgrade_required.html')

    # Both checks passed
    return render(request, 'analytics.html')
```

## Troubleshooting

### User Can't Access Feature

**Check subscription status:**
```python
from apps.billing.models import Subscription

subscription = Subscription.objects.get(user=user)
print(f"Plan: {subscription.plan}")
print(f"Status: {subscription.status}")
print(f"Expired: {subscription.is_expired}")
```

**Check feature configuration:**
```python
from django.conf import settings

plan_features = settings.SUBSCRIPTION_PLANS['pro']['includes']
print(f"Pro features: {plan_features}")
```

### Usage Not Tracking

**Check usage records:**
```python
from apps.billing.models import Usage

usage = Usage.objects.filter(user=user, resource='api_calls')
for u in usage:
    print(f"Period: {u.period_start} - Current: {u.current}")
```

**Manual reset if needed:**
```python
Usage.objects.filter(user=user, resource='api_calls').delete()
```

## Further Reading

- [Stripe Integration](stripe.md) - Set up subscription billing
- [Teams & Organizations](teams.md) - Team-based subscriptions
- [Feature Flags](feature-flags.md) - Gradual feature rollouts

## Related

- **Basic Stripe Mode**: Simple checkout without feature gating
- **Advanced Stripe Mode**: Full subscription management with feature gating
- **Teams**: Per-seat billing with team-based limits
