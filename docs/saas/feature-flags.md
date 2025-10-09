# 🚩 Feature Flags

A/B testing and gradual rollouts with django-waffle.

## Usage

```python
from apps.core.feature_flags import is_feature_enabled

if is_feature_enabled('new_dashboard', user=request.user):
    return render(request, 'dashboard_v2.html')
```

[Full documentation coming soon]
