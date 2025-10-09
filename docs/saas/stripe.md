# 💳 Stripe Integration

Production-ready subscription billing and payment processing for Django Keel SaaS projects.

## Overview

Django Keel provides two Stripe integration modes:

- **Basic Mode** - Simple Stripe API integration for checkout and subscriptions
- **Advanced Mode** - Full-featured integration with [dj-stripe](https://dj-stripe.dev/) for subscription lifecycle management

**Choose Basic Mode when:**
- You need simple one-time payments or basic subscriptions
- You want minimal dependencies and lighter codebase
- You prefer more control over Stripe API interactions

**Choose Advanced Mode when:**
- You need full subscription management with models and admin
- You want automatic webhook handling and database sync
- You're building a complex SaaS with usage-based billing
- You need customer portal, invoices, and payment methods management

## Quick Comparison

| Feature | Basic Mode | Advanced Mode |
|---------|------------|---------------|
| **Checkout** | ✅ Stripe Checkout API | ✅ Stripe Checkout API |
| **Subscriptions** | ✅ Basic tracking | ✅ Full lifecycle management |
| **Webhooks** | ✅ Manual handlers | ✅ Automatic sync with dj-stripe |
| **Database Models** | Simple (Customer, Subscription) | Full Stripe objects mirrored |
| **Admin Interface** | Basic | Full Stripe data management |
| **Customer Portal** | ✅ Redirect to Stripe | ✅ Integrated portal |
| **Usage-Based Billing** | Manual implementation | ✅ Built-in support |
| **Payment Methods** | Via Stripe Dashboard | ✅ Manage in Django |
| **Invoice Management** | Via Stripe Dashboard | ✅ Full invoice tracking |
| **Dependencies** | `stripe` only | `stripe` + `dj-stripe` |
| **Complexity** | Lower | Higher |

## Basic Mode

### Setup

#### 1. Get Stripe Keys

1. Create a Stripe account at [stripe.com](https://stripe.com)
2. Get your API keys from [Dashboard → Developers → API Keys](https://dashboard.stripe.com/test/apikeys)
3. Get webhook secret from [Dashboard → Developers → Webhooks](https://dashboard.stripe.com/test/webhooks)

#### 2. Configure Environment

```bash
# .env
STRIPE_PUBLIC_KEY=pk_test_51...
STRIPE_SECRET_KEY=sk_test_51...
STRIPE_WEBHOOK_SECRET=whsec_...
```

#### 3. Create Products in Stripe Dashboard

1. Go to [Products](https://dashboard.stripe.com/test/products)
2. Create product (e.g., "Pro Plan")
3. Add pricing (e.g., $29/month)
4. Copy the Price ID (starts with `price_...`)

### Implementation

#### Models (Basic Mode)

Generated models in `apps/billing/models.py`:

```python
class StripeCustomer(models.Model):
    """Links Django user to Stripe customer."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Subscription(models.Model):
    """Tracks user subscriptions."""
    customer = models.ForeignKey(StripeCustomer, on_delete=models.CASCADE)
    stripe_subscription_id = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=20)  # active, canceled, past_due, trialing
    plan_name = models.CharField(max_length=100)
    current_period_start = models.DateTimeField()
    current_period_end = models.DateTimeField()
```

#### Create Checkout Session

```python
from apps.billing.utils import create_checkout_session

def checkout_view(request):
    # Your Stripe Price ID
    price_id = 'price_1234567890'

    session = create_checkout_session(
        user=request.user,
        price_id=price_id,
        success_url=request.build_absolute_uri('/billing/success/'),
        cancel_url=request.build_absolute_uri('/pricing/'),
    )

    # Redirect to Stripe Checkout
    return redirect(session.url)
```

#### Handle Webhooks

Webhooks automatically update subscriptions in `apps/billing/webhooks.py`:

```python
# Handled events:
# - customer.subscription.created
# - customer.subscription.updated
# - customer.subscription.deleted
# - invoice.payment_succeeded
# - invoice.payment_failed
```

Configure webhook endpoint in Stripe Dashboard:
```
https://yourdomain.com/billing/webhook/
```

Select events to listen to:
- `customer.subscription.created`
- `customer.subscription.updated`
- `customer.subscription.deleted`
- `invoice.payment_succeeded`
- `invoice.payment_failed`

#### Customer Portal

Redirect users to Stripe Customer Portal to manage subscriptions:

```python
from apps.billing.utils import get_customer_portal_url

def portal_view(request):
    stripe_customer = request.user.stripe_customer
    return_url = request.build_absolute_uri('/billing/subscription/')

    portal_url = get_customer_portal_url(
        stripe_customer.stripe_customer_id,
        return_url
    )

    return redirect(portal_url)
```

### Basic Mode Example Flow

1. **User visits pricing page:**
   ```python
   # views.py
   def pricing(request):
       plans = [
           {'name': 'Pro', 'price': 29, 'price_id': 'price_...'},
           {'name': 'Enterprise', 'price': 99, 'price_id': 'price_...'},
       ]
       return render(request, 'billing/pricing.html', {'plans': plans})
   ```

2. **User clicks "Subscribe":**
   ```python
   def checkout(request):
       price_id = request.POST.get('price_id')

       session = create_checkout_session(
           user=request.user,
           price_id=price_id,
           success_url=request.build_absolute_uri('/billing/success/'),
           cancel_url=request.build_absolute_uri('/pricing/'),
       )

       return redirect(session.url)
   ```

3. **Stripe processes payment and creates subscription**

4. **Webhook updates database:**
   ```python
   # Webhook handler creates Subscription record
   # with status='active', plan details, etc.
   ```

5. **User redirected to success page:**
   ```python
   def success(request):
       return render(request, 'billing/success.html')
   ```

## Advanced Mode (dj-stripe)

### Setup

#### 1. Install dj-stripe

Already included when you select `stripe_mode: advanced` during project generation.

#### 2. Configure Settings

```python
# config/settings/base.py
INSTALLED_APPS = [
    # ...
    'djstripe',
]

# Stripe Configuration
STRIPE_LIVE_PUBLIC_KEY = env('STRIPE_PUBLIC_KEY')
STRIPE_LIVE_SECRET_KEY = env('STRIPE_SECRET_KEY')
STRIPE_TEST_PUBLIC_KEY = env('STRIPE_PUBLIC_KEY')
STRIPE_TEST_SECRET_KEY = env('STRIPE_SECRET_KEY')
STRIPE_LIVE_MODE = False  # Set to True in production

DJSTRIPE_WEBHOOK_SECRET = env('STRIPE_WEBHOOK_SECRET')
DJSTRIPE_FOREIGN_KEY_TO_FIELD = 'id'
DJSTRIPE_USE_NATIVE_JSONFIELD = True
```

#### 3. Run Migrations

```bash
python manage.py migrate djstripe
```

#### 4. Sync Stripe Data

```bash
# Sync products and prices from Stripe
python manage.py djstripe_sync_models Product Price

# Sync customers (if you have existing ones)
python manage.py djstripe_sync_models Customer
```

### Models (Advanced Mode)

dj-stripe provides models that mirror all Stripe objects:

```python
from djstripe.models import Customer, Subscription, Price, Product, Invoice

# Your custom models
class SubscriptionMetadata(models.Model):
    """Extended subscription data."""
    subscription = models.OneToOneField(
        Subscription,
        on_delete=models.CASCADE,
        related_name='metadata'
    )
    features = models.JSONField(default=dict)
    usage_limits = models.JSONField(default=dict)
    current_usage = models.JSONField(default=dict)


class PlanConfiguration(models.Model):
    """Configure subscription plans."""
    stripe_product = models.OneToOneField(Product, on_delete=models.CASCADE)
    stripe_price = models.ForeignKey(Price, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    features = models.JSONField(default=dict)
    limits = models.JSONField(default=dict)
    is_popular = models.BooleanField(default=False)


class UsageRecord(models.Model):
    """Track metered usage."""
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    metric = models.CharField(max_length=100)  # e.g., 'api_calls'
    quantity = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
```

### Implementation

#### Configure Plans

Create plan configurations in Django admin:

```python
# In Django admin
plan = PlanConfiguration.objects.create(
    stripe_product=Product.objects.get(id='prod_...'),
    stripe_price=Price.objects.get(id='price_...'),
    name='Pro Plan',
    slug='pro',
    features={
        'api_access': True,
        'advanced_analytics': True,
        'priority_support': True,
    },
    limits={
        'api_calls': 10000,
        'team_members': 10,
        'storage_gb': 100,
    },
    is_popular=True,
)
```

#### Create Checkout Session

```python
from apps.billing.utils import create_checkout_session

def checkout_view(request):
    price_id = request.POST.get('price_id')

    session = create_checkout_session(
        user=request.user,
        price_id=price_id,
        success_url=request.build_absolute_uri('/billing/success/?session_id={CHECKOUT_SESSION_ID}'),
        cancel_url=request.build_absolute_uri('/pricing/'),
        metadata={'plan_slug': 'pro'},  # Custom metadata
    )

    return redirect(session.url)
```

#### Get User's Subscription

```python
from apps.billing.utils import get_active_subscription

def dashboard_view(request):
    subscription = get_active_subscription(request.user)

    if subscription:
        # User has active subscription
        plan_config = PlanConfiguration.objects.get(
            stripe_product=subscription.plan.product
        )

        context = {
            'subscription': subscription,
            'plan': plan_config,
            'features': plan_config.features,
            'limits': plan_config.limits,
        }
    else:
        # No subscription
        context = {'subscription': None}

    return render(request, 'dashboard.html', context)
```

#### Track Usage

```python
from apps.billing.utils import record_usage, check_usage_limit

def api_endpoint(request):
    subscription = get_active_subscription(request.user)

    # Check if user is within limits
    can_use, remaining = check_usage_limit(
        subscription,
        metric='api_calls',
        limit=10000
    )

    if not can_use:
        return JsonResponse({'error': 'API limit exceeded'}, status=429)

    # Process API request
    result = process_request(request)

    # Record usage
    record_usage(subscription, metric='api_calls', quantity=1)

    return JsonResponse(result)
```

#### Webhooks (Advanced)

dj-stripe automatically handles webhooks and syncs data:

```python
# apps/billing/webhooks.py
from django.dispatch import receiver
from djstripe import webhooks

@receiver(webhooks.WEBHOOK_SIGNALS['customer.subscription.created'])
def handle_subscription_created(sender, event, **kwargs):
    """Handle new subscription."""
    subscription = event.data['object']

    # Create metadata
    from .models import SubscriptionMetadata
    SubscriptionMetadata.objects.create(
        subscription_id=subscription['id']
    )


@receiver(webhooks.WEBHOOK_SIGNALS['invoice.payment_succeeded'])
def handle_payment_succeeded(sender, event, **kwargs):
    """Handle successful payment."""
    invoice = event.data['object']

    # Reset usage counters for the billing period
    subscription = Subscription.objects.get(
        id=invoice['subscription']
    )
    if hasattr(subscription, 'metadata'):
        subscription.metadata.current_usage = {}
        subscription.metadata.save()


@receiver(webhooks.WEBHOOK_SIGNALS['customer.subscription.deleted'])
def handle_subscription_deleted(sender, event, **kwargs):
    """Handle canceled subscription."""
    subscription = event.data['object']

    # Revoke access, send email, etc.
    logger.info(f"Subscription canceled: {subscription['id']}")
```

Configure webhook endpoint in Stripe Dashboard:
```
https://yourdomain.com/djstripe/webhook/
```

### Customer Portal

```python
from apps.billing.utils import get_customer_portal_url

def customer_portal(request):
    return_url = request.build_absolute_uri('/billing/subscription/')
    portal_url = get_customer_portal_url(request.user, return_url)

    return redirect(portal_url)
```

## Feature Gating with Stripe

### Check Subscription Status

```python
from apps.billing.decorators import subscription_required

@subscription_required
def premium_feature(request):
    """Requires active subscription."""
    return render(request, 'premium.html')
```

### Check Specific Plan

```python
from apps.billing.decorators import plan_required

@plan_required('pro')
def pro_only_feature(request):
    """Only for Pro subscribers."""
    return render(request, 'pro_feature.html')

@plan_required(['pro', 'enterprise'])
def premium_feature(request):
    """For Pro or Enterprise subscribers."""
    return render(request, 'premium.html')
```

### Check Feature Access

```python
from apps.billing.decorators import feature_required

@feature_required('advanced_analytics')
def analytics_view(request):
    """Requires subscription with analytics feature."""
    return render(request, 'analytics.html')
```

### Usage Limits

```python
from apps.billing.decorators import usage_limit

@usage_limit('api_calls', limit=10000, period='month')
def api_endpoint(request):
    """Limited to 10,000 API calls per month."""
    # Usage tracked automatically
    return JsonResponse({'data': 'response'})
```

## Templates

### Display Pricing Plans

```django
{% load billing_tags %}

<div class="pricing-plans">
  {% for plan in plans %}
  <div class="plan {% if plan.is_popular %}popular{% endif %}">
    <h3>{{ plan.name }}</h3>
    <p class="price">${{ plan.stripe_price.unit_amount|divide:100 }}/mo</p>

    <ul class="features">
      {% for feature, enabled in plan.features.items %}
        {% if enabled %}
        <li>✓ {{ feature|title }}</li>
        {% endif %}
      {% endfor %}
    </ul>

    <ul class="limits">
      {% for limit, value in plan.limits.items %}
      <li>{{ value }} {{ limit|title }}</li>
      {% endfor %}
    </ul>

    {% if user.is_authenticated %}
      <form method="post" action="{% url 'billing:checkout' %}">
        {% csrf_token %}
        <input type="hidden" name="price_id" value="{{ plan.stripe_price.id }}">
        <button type="submit" class="btn btn-primary">Subscribe</button>
      </form>
    {% else %}
      <a href="{% url 'account_signup' %}" class="btn btn-primary">Get Started</a>
    {% endif %}
  </div>
  {% endfor %}
</div>
```

### Subscription Status

```django
{% load billing_tags %}

{% if user.has_active_subscription %}
<div class="subscription-status">
  <h3>Your Subscription</h3>
  <p>Plan: {{ subscription.plan.product.name }}</p>
  <p>Status: {{ subscription.status }}</p>
  <p>Renews: {{ subscription.current_period_end|date:"F j, Y" }}</p>

  <a href="{% url 'billing:customer_portal' %}" class="btn">
    Manage Subscription
  </a>
</div>
{% else %}
<div class="no-subscription">
  <p>You don't have an active subscription.</p>
  <a href="{% url 'billing:pricing' %}" class="btn">View Plans</a>
</div>
{% endif %}
```

### Usage Meters

```django
{% load billing_tags %}

{% get_usage user 'api_calls' as api_usage %}

<div class="usage-meter">
  <h4>API Calls</h4>
  <p>{{ api_usage.current }} / {{ api_usage.limit }}</p>

  <div class="progress-bar">
    <div class="progress" style="width: {{ api_usage.percentage }}%"></div>
  </div>

  {% if api_usage.is_near_limit %}
  <p class="warning">⚠️ Approaching limit. Consider upgrading.</p>
  {% endif %}

  {% if api_usage.is_over_limit %}
  <p class="error">❌ Limit exceeded. Please upgrade to continue.</p>
  {% endif %}
</div>
```

## Testing

### Test Mode

Stripe provides test mode with test cards:

```python
# Test cards
# Success: 4242 4242 4242 4242
# Decline: 4000 0000 0000 0002
# Require authentication: 4000 0025 0000 3155
```

### Unit Tests (Basic Mode)

```python
import pytest
from unittest.mock import patch, MagicMock
from apps.billing.utils import create_checkout_session


@pytest.mark.django_db
def test_create_checkout_session(user):
    """Test creating a checkout session."""
    with patch('stripe.checkout.Session.create') as mock_create:
        mock_create.return_value = MagicMock(
            id='cs_test_123',
            url='https://checkout.stripe.com/c/pay/cs_test_123'
        )

        session = create_checkout_session(
            user=user,
            price_id='price_123',
            success_url='https://example.com/success/',
            cancel_url='https://example.com/cancel/',
        )

        assert session.id == 'cs_test_123'
        assert 'checkout.stripe.com' in session.url
```

### Webhook Tests (Advanced Mode)

```python
import pytest
import json
from django.test import Client
from djstripe.models import Event


@pytest.mark.django_db
def test_subscription_created_webhook():
    """Test subscription.created webhook."""
    client = Client()

    payload = {
        'type': 'customer.subscription.created',
        'data': {
            'object': {
                'id': 'sub_123',
                'customer': 'cus_123',
                'status': 'active',
            }
        }
    }

    # Mock Stripe signature verification
    with patch('stripe.Webhook.construct_event') as mock_verify:
        mock_verify.return_value = payload

        response = client.post(
            '/djstripe/webhook/',
            data=json.dumps(payload),
            content_type='application/json',
            HTTP_STRIPE_SIGNATURE='test_signature'
        )

        assert response.status_code == 200

        # Verify event was created
        assert Event.objects.filter(type='customer.subscription.created').exists()
```

### Integration Tests

```python
@pytest.mark.django_db
class TestStripeIntegration:
    def test_full_subscription_flow(self, client, user):
        """Test complete subscription flow."""
        client.force_login(user)

        # 1. Visit pricing page
        response = client.get('/billing/pricing/')
        assert response.status_code == 200

        # 2. Create checkout session
        response = client.post('/billing/checkout/', {
            'price_id': 'price_test_123'
        })
        assert response.status_code == 302  # Redirect to Stripe

        # 3. Simulate webhook (subscription created)
        # ... webhook handling ...

        # 4. Check subscription is active
        from apps.billing.utils import get_active_subscription
        subscription = get_active_subscription(user)
        assert subscription is not None
        assert subscription.status == 'active'
```

## Deployment

### Environment Variables

```bash
# Production .env
STRIPE_PUBLIC_KEY=pk_live_...
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...

# For dj-stripe
DJSTRIPE_WEBHOOK_SECRET=whsec_...
```

### Webhook Configuration

1. Go to [Stripe Dashboard → Developers → Webhooks](https://dashboard.stripe.com/webhooks)
2. Click "Add endpoint"
3. Enter URL:
   - Basic mode: `https://yourdomain.com/billing/webhook/`
   - Advanced mode: `https://yourdomain.com/djstripe/webhook/`
4. Select events to listen to
5. Copy webhook signing secret to `.env`

### Production Checklist

- [ ] Switch to live API keys (`pk_live_...`, `sk_live_...`)
- [ ] Configure production webhook endpoint
- [ ] Test webhooks with Stripe CLI: `stripe listen --forward-to localhost:8000/djstripe/webhook/`
- [ ] Enable Stripe Radar for fraud protection
- [ ] Set up billing email notifications
- [ ] Configure customer portal settings
- [ ] Test with production Stripe account
- [ ] Set up monitoring for failed payments
- [ ] Document subscription cancellation policy
- [ ] Configure tax collection (Stripe Tax)

## Troubleshooting

### Webhook Not Received

**Symptoms:** Subscriptions not updating after payment

**Solutions:**

1. Verify webhook endpoint is accessible:
   ```bash
   curl https://yourdomain.com/djstripe/webhook/
   ```

2. Check webhook signing secret matches `.env`

3. Test with Stripe CLI:
   ```bash
   stripe listen --forward-to localhost:8000/djstripe/webhook/
   stripe trigger customer.subscription.created
   ```

4. Check webhook logs in Stripe Dashboard

### Checkout Session Expired

**Symptoms:** Users get "expired session" error

**Solution:** Checkout sessions expire after 24 hours. Create a new session if needed:

```python
# Check if session is recent
from datetime import timedelta
from django.utils import timezone

if session.created < timezone.now() - timedelta(hours=23):
    # Create new session
    session = create_checkout_session(...)
```

### Subscription Not Found

**Symptoms:** `get_active_subscription()` returns None

**Solutions:**

1. Sync from Stripe:
   ```bash
   python manage.py djstripe_sync_models Subscription Customer
   ```

2. Check subscription status in Stripe Dashboard

3. Verify webhook was received and processed

### Invoice Payment Failed

**Symptoms:** Subscription shows `past_due`

**Solution:** Stripe automatically retries failed payments. Configure retry logic in [Billing settings](https://dashboard.stripe.com/settings/billing/automatic).

Send email notification to customer:

```python
@receiver(webhooks.WEBHOOK_SIGNALS['invoice.payment_failed'])
def handle_payment_failed(sender, event, **kwargs):
    invoice = event.data['object']
    customer_email = invoice['customer_email']

    send_mail(
        subject='Payment Failed',
        message='Your recent payment failed. Please update your payment method.',
        from_email='billing@yourdomain.com',
        recipient_list=[customer_email],
    )
```

## Best Practices

1. **Use Test Mode** - Always test with test keys first
2. **Implement Webhooks** - Never rely solely on redirect callbacks
3. **Handle Idempotency** - Stripe may send duplicate webhooks
4. **Sync Regularly** - Use `djstripe_sync_models` to catch any missed updates
5. **Monitor Failed Payments** - Set up alerts for `invoice.payment_failed`
6. **Validate on Backend** - Never trust client-side data
7. **Use Customer Portal** - Let Stripe handle payment method updates
8. **Test Edge Cases** - Failed payments, cancellations, upgrades/downgrades
9. **Log Everything** - Track all subscription events for debugging
10. **Keep Stripe Updated** - Regularly update `stripe` and `dj-stripe` packages

## Common Patterns

### Free Trial

```python
# Create subscription with trial
session = stripe.checkout.Session.create(
    customer_email=user.email,
    payment_method_types=['card'],
    line_items=[{
        'price': price_id,
        'quantity': 1,
    }],
    mode='subscription',
    subscription_data={
        'trial_period_days': 14,  # 14-day free trial
    },
    success_url=success_url,
    cancel_url=cancel_url,
)
```

### Usage-Based Pricing

```python
# Metered billing
from apps.billing.utils import record_usage

def api_call(request):
    # Process request
    result = process_request(request)

    # Record usage (will be billed at end of period)
    subscription = get_active_subscription(request.user)
    record_usage(subscription, metric='api_calls', quantity=1)

    return JsonResponse(result)
```

### Per-Seat Pricing

```python
# Update subscription quantity when team size changes
import stripe

def add_team_member(request):
    team = request.user.team
    team.members.add(new_member)

    # Update Stripe subscription quantity
    subscription = team.stripe_subscription
    stripe.Subscription.modify(
        subscription.id,
        items=[{
            'id': subscription['items']['data'][0].id,
            'quantity': team.members.count(),
        }]
    )
```

### Proration

```python
# Upgrade/downgrade with proration
stripe.Subscription.modify(
    subscription.id,
    items=[{
        'id': subscription['items']['data'][0].id,
        'price': new_price_id,
    }],
    proration_behavior='create_prorations',  # or 'always_invoice', 'none'
)
```

## Further Reading

- [Stripe Documentation](https://stripe.com/docs)
- [dj-stripe Documentation](https://dj-stripe.dev/)
- [Stripe API Reference](https://stripe.com/docs/api)
- [Stripe Testing Guide](https://stripe.com/docs/testing)
- [Stripe Webhooks Best Practices](https://stripe.com/docs/webhooks/best-practices)

## Related Documentation

- [Feature Gating](feature-gating.md) - Control access by subscription tier
- [Feature Flags](feature-flags.md) - Gradual feature rollouts
- [Teams](teams.md) - Team subscriptions and per-seat billing
