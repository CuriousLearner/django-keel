# 🎯 Project Types

Django Keel adapts to your needs with **smart defaults** based on your project type. You still see every question, but choosing what you're building pre-fills sensible answers - just press Enter to accept them.

## Overview

When you run `copier copy gh:CuriousLearner/django-keel`, the first question is:

```
What type of project are you building?
1. saas - Multi-tenant SaaS with billing
2. api - API-only backend
3. web-app - Traditional web application
4. internal-tool - Corporate internal tool
5. custom - I'll choose everything myself
```

Each project type automatically configures:

- API framework (DRF, GraphQL, both, or none)
- Frontend approach (Next.js, HTMX+Tailwind, or API-only)
- Background tasks (Celery, Temporal, both, or none)
- Optional features (Teams, Stripe billing, etc.)
- Deployment target (Kubernetes, Fly.io, Render, etc.)

**You can always override any default!**

---

## 🚀 SaaS Application

**Perfect for:** Multi-tenant SaaS products with subscriptions, billing, and teams

### What You Get

```yaml
project_type: saas

# Smart defaults:
api_style: drf                    # RESTful API with Django REST Framework
frontend: nextjs                  # Modern React frontend
use_teams: true                   # Multi-tenancy with RBAC
use_stripe: true                  # Advanced Stripe integration (dj-stripe)
stripe_mode: advanced             # Full subscription management
background_tasks: celery          # Async tasks for emails, reports
deployment_targets: kubernetes    # Enterprise-scale deployment
```

### Features Included

- ✅ **Teams/Organizations** - Owner/Admin/Member roles
- ✅ **Stripe Billing** - Subscriptions, webhooks, customer portal
- ✅ **Feature Gating** - `@subscription_required()`, `@feature_required()`
- ✅ **User Impersonation** - Admin can debug user issues
- ✅ **Feature Flags** - A/B testing with django-waffle
- ✅ **Professional Emails** - Transactional email templates
- ✅ **API Documentation** - Auto-generated OpenAPI/Swagger docs
- ✅ **WebSocket Support** - Optional real-time features

### Use Cases

- B2B SaaS platforms
- Project management tools
- Analytics dashboards
- CRM systems
- Collaborative tools

### Example: Startup SaaS

```yaml
project_type: saas
use_stripe: true
stripe_mode: advanced
use_teams: true
frontend: nextjs
use_channels: true          # Add WebSockets
observability_level: full   # Full monitoring stack
deployment_targets: kubernetes
```

---

## 🔌 API Backend

**Perfect for:** Mobile apps, microservices, headless backends

### What You Get

```yaml
project_type: api

# Smart defaults:
api_style: drf                 # RESTful API
frontend: none                 # No frontend
use_teams: false               # Single-tenant
use_stripe: false              # No billing
background_tasks: celery       # Async processing
deployment_targets: render     # Easy PaaS hosting
```

### Features Included

- ✅ **Django REST Framework** - Serializers, viewsets, permissions
- ✅ **drf-spectacular** - Auto-generated OpenAPI 3.0 docs
- ✅ **JWT Authentication** - Token-based auth for mobile
- ✅ **CORS** - Cross-origin requests configured
- ✅ **Rate Limiting** - API throttling
- ✅ **Celery** - Background task processing
- ✅ **Health Checks** - `/health/` and `/ready/` endpoints

### Use Cases

- Mobile app backends
- Microservices
- API gateways
- Third-party integrations
- Headless CMS

### Example: Mobile App Backend

```yaml
project_type: api
auth_backend: jwt
use_channels: true          # WebSockets for real-time chat
use_2fa: true               # TOTP for sensitive operations
observability_level: standard
deployment_targets: render
```

### Example: GraphQL API

```yaml
project_type: api
api_style: graphql-strawberry  # Override to use GraphQL
auth_backend: jwt
background_tasks: celery
deployment_targets: flyio
```

---

## 🌐 Web Application

**Perfect for:** Traditional Django web apps, MVPs, content sites

### What You Get

```yaml
project_type: web-app

# Smart defaults:
api_style: none                # Traditional Django views
frontend: htmx-tailwind        # Modern, minimal JavaScript
use_teams: false               # Single-tenant
use_stripe: false              # No billing
background_tasks: celery       # Email sending
deployment_targets: flyio      # Global edge deployment
```

### Features Included

- ✅ **HTMX** - Dynamic HTML without writing JavaScript
- ✅ **Tailwind CSS** - Utility-first styling
- ✅ **Alpine.js** - Minimal JavaScript for interactions
- ✅ **django-allauth** - Social auth, email verification
- ✅ **Form Handling** - Django forms with CSRF protection
- ✅ **Template System** - Django templates with partials
- ✅ **Celery** - Send emails in background

### Use Cases

- Company websites
- Blogs and content sites
- E-commerce stores
- Landing pages
- MVPs and prototypes

### Example: Company Blog

```yaml
project_type: web-app
frontend: htmx-tailwind
use_search: postgres-fts    # Full-text search
use_i18n: true              # Multi-language support
background_tasks: celery
deployment_targets: flyio
```

### Example: E-commerce Site

```yaml
project_type: web-app
frontend: htmx-tailwind
use_stripe: true            # Add payment processing
stripe_mode: basic          # Simple checkout flows
use_search: opensearch      # Advanced product search
deployment_targets: kubernetes
```

---

## 🏢 Internal Tool

**Perfect for:** Corporate dashboards, admin panels, internal systems

### What You Get

```yaml
project_type: internal-tool

# Smart defaults:
api_style: drf                     # API for flexibility
frontend: htmx-tailwind            # Fast UI development
use_teams: true                    # Departments/groups
use_stripe: false                  # No billing
background_tasks: celery           # Reports, exports
deployment_targets: aws-ec2-ansible # On-premise friendly
```

### Features Included

- ✅ **Teams/Organizations** - Department-based access
- ✅ **RBAC** - Owner/Admin/Member roles
- ✅ **User Impersonation** - IT can help users debug
- ✅ **Django Admin** - Powerful admin interface
- ✅ **Celery** - Generate reports, export data

### Use Cases

- Corporate dashboards
- Admin panels
- Inventory systems
- HR tools
- Internal APIs

### Example: Enterprise Dashboard

```yaml
project_type: internal-tool
use_teams: true             # Departments
security_profile: strict    # Enhanced security
auth_backend: both          # allauth + JWT
observability_level: full   # Complete monitoring
deployment_targets: aws-ec2-ansible
```

### Example: Data Analysis Tool

```yaml
project_type: internal-tool
frontend: htmx-tailwind
background_tasks: temporal  # Long-running data processing
use_channels: true          # Real-time progress updates
deployment_targets: kubernetes
```

---

## ⚙️ Custom Configuration

**Perfect for:** Unique requirements, maximum control

### What You Get

```yaml
project_type: custom

# Generic defaults - nothing pre-decided for you
```

Every project type asks the same full set of questions; `project_type` only changes the pre-filled defaults. With "custom" you get generic defaults instead of opinionated ones:

1. **API Framework** - DRF, GraphQL, both, or none
2. **Frontend** - Next.js, HTMX+Tailwind, or none
3. **Background Tasks** - Celery, Temporal, both, or none
4. **Authentication** - django-allauth, JWT, or both
5. **2FA** - Enable TOTP two-factor auth?
6. **Teams** - Include multi-tenancy?
7. **Stripe** - Payment integration? (basic or advanced)
8. **Search** - PostgreSQL FTS, OpenSearch, or none
9. **Observability** - Minimal, standard, or full
10. **Deployment** - Kubernetes, Render, Fly.io, AWS ECS Fargate, AWS EC2, Docker
11. **And more...**

### Use Cases

- Hybrid applications
- Complex requirements
- Learning/experimentation
- Unique tech stack needs

---

## 🔄 Changing Your Mind

**You can always change any default!**

After selecting a project type, you'll see the smart defaults and can override any of them:

```
API framework? [drf]
> graphql-strawberry    # Override the default

Frontend approach? [nextjs]
> htmx-tailwind         # Override the default
```

---

## 📊 Comparison Matrix

| Feature | SaaS | API | Web App | Internal Tool | Custom |
|---------|------|-----|---------|---------------|--------|
| **API Framework** | DRF | DRF | None | DRF | Your choice |
| **Frontend** | Next.js | None | HTMX | HTMX | Your choice |
| **Teams** | ✅ Yes | ❌ No | ❌ No | ✅ Yes | Your choice |
| **Stripe** | ✅ Advanced | ❌ No | ❌ No | ❌ No | Your choice |
| **Background Tasks** | Celery | Celery | Celery | Celery | Your choice |
| **Deployment** | Kubernetes | Render | Fly.io | AWS EC2 | Your choice |

---

## 🎯 Decision Guide

### Choose **SaaS** if you're building:
- A product with monthly/yearly subscriptions
- Multi-tenant application (many customers, isolated data)
- Need team collaboration features
- Want per-seat or usage-based billing

### Choose **API** if you're building:
- Mobile app backend
- Microservice
- Headless CMS
- Third-party API

### Choose **Web App** if you're building:
- Traditional website
- Blog or content site
- MVP or prototype
- E-commerce site

### Choose **Internal Tool** if you're building:
- Company dashboard
- Admin panel
- Employee-facing tool
- On-premise system

### Choose **Custom** if:
- None of the above fit
- You want full control
- You're experimenting
- You have unique requirements

---

## 🚀 Next Steps

1. [Quick Start](quickstart.md) - Create your first project
2. [Features Overview](../features/overview.md) - Explore all features
3. [SaaS Features](../saas/overview.md) - Deep dive into SaaS capabilities
4. [Deployment Options](../deployment/overview.md) - Choose your hosting
