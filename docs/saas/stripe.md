# 💳 Stripe Integration

Production-ready subscription billing for Django Keel SaaS projects.

## Two Modes

### Basic Mode
Simple Stripe API integration for checkout flows.

### Advanced Mode (dj-stripe)
Full subscription lifecycle management with models, webhooks, and customer portal.

[Full documentation coming soon]

## Quick Setup

```bash
# .env
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

## Next Steps

- [Feature Gating](feature-gating.md) - Control access by plan
- [Teams](teams.md) - Per-seat billing
