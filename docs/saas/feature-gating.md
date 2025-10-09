# 🔒 Feature Gating

Control access to features based on subscription plans.

## Decorators

```python
from apps.billing.decorators import subscription_required, feature_required

@subscription_required
@feature_required('advanced_analytics')
def advanced_report(request):
    # Only accessible with active subscription
    # and 'advanced_analytics' feature
    pass
```

[Full documentation coming soon]
