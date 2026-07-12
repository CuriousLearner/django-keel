# 🔒 Feature Gating

!!! note
    Feature gating requires `stripe_mode: advanced` — the decorators, mixins, and
    usage utilities are built on the dj-stripe models (`PlanConfiguration`,
    `UsageRecord`) that only generate in advanced mode.

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

Generate your project with `use_stripe: true` and `stripe_mode: advanced`. Feature gating lives in `apps/billing/decorators.py` (decorators and mixins) and `apps/billing/utils.py` (helper functions).

### Basic Usage

```python
from apps.billing.decorators import subscription_required, feature_required

@subscription_required()
@feature_required('advanced_analytics')
def analytics_view(request):
    """Only accessible to users with active subscription and feature."""
    return render(request, 'analytics.html')
```

All decorators are factories - always call them with parentheses, even without arguments.

## Decorators

### @subscription_required()

Ensures the user has an active subscription:

```python
from apps.billing.decorators import subscription_required

@subscription_required()
def premium_feature(request):
    """Requires any active subscription."""
    return render(request, 'premium.html')

@subscription_required(redirect_url="/pricing/")
def another_view(request):
    ...
```

**Parameters:** `redirect_url` (default `/billing/subscribe/`), `message`, `ajax_response` (return a JSON 403 instead of redirecting).

**Behavior:**

- ✅ User with active (or trialing) subscription → Access granted
- ❌ Not authenticated → Redirect to login (or JSON 401 with `ajax_response=True`)
- ❌ No active subscription → Warning message and redirect (or JSON 403)

### @feature_required(feature_key)

Checks if the subscription's plan includes a specific feature:

```python
from apps.billing.decorators import feature_required

@feature_required('api_access')
def api_dashboard(request):
    """Requires subscription with API access feature."""
    return render(request, 'api_dashboard.html')

@feature_required('advanced_analytics', redirect_url='/pricing/')
def analytics_view(request):
    ...
```

**Parameters:** `feature_key`, `redirect_url` (default `/billing/upgrade/`), `message`, `ajax_response`.

### @plan_required(*plan_slugs)

Requires one of the given plan slugs. Pass slugs as positional arguments, not a list:

```python
from apps.billing.decorators import plan_required

@plan_required('pro')
def pro_only_feature(request):
    """Only for Pro tier subscribers."""
    return render(request, 'pro_feature.html')

@plan_required('pro', 'enterprise')
def premium_feature(request):
    """For Pro or Enterprise subscribers."""
    return render(request, 'premium.html')
```

Plan slugs are matched against `PlanConfiguration` rows (see [Plan Configuration](#plan-configuration) below).

### @usage_limit_check(metric)

Blocks the view when the user is already over the limit for a metric:

```python
from apps.billing.decorators import usage_limit_check

@usage_limit_check('api_calls')
def api_endpoint(request):
    """Blocked with a 429/redirect once the user is over their limit."""
    return JsonResponse({'data': 'response'})
```

**Parameters:** `metric`, `redirect_url` (default `/billing/upgrade/`), `message`, `ajax_response` (returns JSON with status 429 when over limit).

Limits come from the subscription's `SubscriptionMetadata.usage_limits` JSON. The decorator only checks the limit - it does not record usage. Call `record_usage()` yourself (see [Usage Tracking](#usage-tracking)).

## Class-Based Views

The mixins live in `apps/billing/decorators.py` alongside the decorators.

### SubscriptionRequiredMixin

```python
from apps.billing.decorators import SubscriptionRequiredMixin
from django.views.generic import TemplateView

class PremiumDashboard(SubscriptionRequiredMixin, TemplateView):
    template_name = 'dashboard.html'
    # Optional overrides:
    # subscription_redirect_url = "/billing/subscribe/"
    # subscription_message = "..."
```

### FeatureRequiredMixin

```python
from apps.billing.decorators import FeatureRequiredMixin

class AnalyticsView(FeatureRequiredMixin, TemplateView):
    template_name = 'analytics.html'
    required_feature = 'advanced_analytics'
    # Optional: feature_redirect_url, feature_message
```

### PlanRequiredMixin

```python
from apps.billing.decorators import PlanRequiredMixin

class EnterpriseView(PlanRequiredMixin, TemplateView):
    template_name = 'enterprise.html'
    required_plans = ['enterprise']
    # Optional: plan_redirect_url, plan_message
```

There is no usage-limit mixin; use the `usage_limit_check()` decorator (e.g. via `method_decorator`) for class-based views.

## Programmatic Checks

All helpers are in `apps/billing/utils.py`.

### Check Subscription

```python
from apps.billing.utils import has_active_subscription, get_active_subscription

if has_active_subscription(request.user):
    # User can access premium features
    ...

subscription = get_active_subscription(request.user)  # dj-stripe Subscription or None
```

### Check Feature

```python
from apps.billing.utils import check_feature_access

if check_feature_access(request.user, 'api_access'):
    # User has API access feature
    api_key = generate_api_key(request.user)
```

### Check Usage Limit

```python
from apps.billing.utils import check_usage_limit

# Returns True when the user is OVER the limit (or has no subscription)
if check_usage_limit(request.user, 'api_calls'):
    return JsonResponse({'error': 'Usage limit exceeded'}, status=429)

result = make_api_call()
```

Note the semantics: `check_usage_limit(user, metric)` returns `True` when the user is over the limit, and also when they have no active subscription.

### Get Plan Features

```python
from apps.billing.utils import get_active_subscription, get_subscription_features

subscription = get_active_subscription(request.user)
features = get_subscription_features(subscription)  # dict from PlanConfiguration.features
```

## API (DRF) Integration

### Subscription Required

```python
from rest_framework.decorators import api_view
from apps.billing.decorators import subscription_required

@api_view(['GET'])
@subscription_required(ajax_response=True)
def premium_api(request):
    """API endpoint requires active subscription."""
    return Response({'data': 'premium data'})
```

### Feature-Based Permissions

```python
from rest_framework.permissions import BasePermission
from apps.billing.utils import check_feature_access

class HasAPIAccess(BasePermission):
    """Custom permission for API access feature."""

    def has_permission(self, request, view):
        return check_feature_access(request.user, 'api_access')

class MyAPIView(APIView):
    permission_classes = [HasAPIAccess]

    def get(self, request):
        return Response({'data': 'api response'})
```

## Plan Configuration

Plans are database rows, not settings. The `PlanConfiguration` model (`apps/billing/models.py`) links a Stripe product to a plan slug, features, and limits:

```python
from apps.billing.models import PlanConfiguration
from djstripe.models import Product, Price

product = Product.objects.get(name="Pro")
PlanConfiguration.objects.create(
    stripe_product=product,
    stripe_price=Price.objects.get(product=product, active=True),
    name="Pro Plan",
    slug="pro",
    features={
        "advanced_analytics": True,
        "custom_domains": True,
        "priority_support": True,
    },
    limits={
        "api_calls": 10000,
        "storage_gb": 50,
        "team_members": 10,
    },
)
```

Create one `PlanConfiguration` per Stripe product - via the Django admin, a data migration, or a setup script. `@plan_required()` matches against `slug`, and `check_feature_access()` / `get_subscription_features()` read `features`.

Per-subscription overrides live in `SubscriptionMetadata` (`features`, `usage_limits`, `current_usage` JSON fields), which `check_feature_access()` and `check_usage_limit()` consult first when present.

## Usage Tracking

### Recording Usage

Usage is not recorded automatically - record it where the work happens:

```python
from apps.billing.utils import get_active_subscription, record_usage

subscription = get_active_subscription(request.user)
record_usage(subscription, metric='api_calls', quantity=1)
```

`record_usage(subscription, metric, quantity)` creates a `UsageRecord` row.

### Usage Model

`UsageRecord` (`apps/billing/models.py`) has five fields: `subscription` (FK to dj-stripe `Subscription`), `metric`, `quantity`, an auto-set `timestamp`, and a `metadata` JSONField for arbitrary extra context.

```python
from apps.billing.models import UsageRecord

# All API call records for a subscription
records = UsageRecord.objects.filter(
    subscription=subscription,
    metric='api_calls',
)
```

## Best Practices

1. **Clear upgrade paths** - Always show what plan includes the feature
2. **Graceful degradation** - Disable features, don't break the app
3. **Usage warnings** - Alert users when approaching limits (80%, 90%)
4. **Feature discoverability** - Show locked features with upgrade CTA
5. **Track metrics** - Monitor which features drive upgrades
6. **Testing** - Test all subscription tiers
7. **Documentation** - Document all gated features clearly

## Common Patterns

### Tiered Feature Access

```python
from apps.billing.utils import get_active_subscription, get_subscription_features

def can_create_project(user):
    """Check if user can create more projects."""
    subscription = get_active_subscription(user)
    if not subscription:
        return user.projects.count() < 3  # free tier

    features = get_subscription_features(subscription)
    limit = features.get('projects')
    if limit is None:  # Unlimited
        return True

    return user.projects.count() < limit
```

### Feature Flags + Gating

Combine feature flags with gating:

```python
from waffle import flag_is_active
from apps.billing.utils import check_feature_access

def advanced_feature_view(request):
    # Check feature flag (gradual rollout)
    if not flag_is_active(request, 'new_analytics'):
        return redirect('dashboard')

    # Check subscription (monetization)
    if not check_feature_access(request.user, 'advanced_analytics'):
        return render(request, 'upgrade_required.html')

    # Both checks passed
    return render(request, 'analytics.html')
```

## Troubleshooting

### User Can't Access Feature

**Check subscription status:**
```python
from apps.billing.utils import get_active_subscription

subscription = get_active_subscription(user)
print(subscription)  # None means no active/trialing subscription
```

**Check plan configuration:**
```python
from apps.billing.models import PlanConfiguration

plan = PlanConfiguration.objects.get(slug='pro')
print(plan.features)
print(plan.limits)
```

### Usage Not Tracking

Make sure your code calls `record_usage()` - nothing records usage automatically:

```python
from apps.billing.models import UsageRecord

records = UsageRecord.objects.filter(subscription=subscription, metric='api_calls')
for r in records:
    print(f"{r.timestamp}: {r.quantity}")
```

## Further Reading

- [Stripe Integration](stripe.md) - Set up subscription billing
- [Teams & Organizations](teams.md) - Team-based subscriptions
- [Feature Flags](feature-flags.md) - Gradual feature rollouts

## Related

- **Basic Stripe Mode**: Simple checkout without feature gating
- **Advanced Stripe Mode**: Full subscription management with feature gating
- **Teams**: Per-seat billing with team-based limits
