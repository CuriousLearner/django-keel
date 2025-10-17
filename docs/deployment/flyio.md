# Fly.io Deployment

Deploy Django Keel projects globally with Fly.io's edge network.

## Overview

Fly.io runs your application close to users worldwide with:

- **Global edge deployment** - Deploy to 30+ regions
- **Automatic HTTPS** - Free SSL certificates
- **PostgreSQL included** - Managed Postgres clusters
- **Redis included** - Managed Redis
- **Free tier** - Generous free allowance
- **Near-instant deploys** - Deploy in seconds

## Prerequisites

- Fly.io account (free tier available)
- Fly CLI installed
- `deployment_targets: [flyio]` selected during generation

## Installation

### Install Fly CLI

```bash
# macOS
brew install flyctl

# Linux
curl -L https://fly.io/install.sh | sh

# Windows
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
```

### Authenticate

```bash
fly auth login
```

## Quick Start

### 1. Launch Application

From your project directory:

```bash
fly launch
```

Fly.io will:
1. Detect your Django app
2. Generate `fly.toml` configuration
3. Prompt for app name and region
4. Create PostgreSQL database (optional)
5. Create Redis instance (optional)

### 2. Configure fly.toml

Generated `fly.toml`:

```toml
app = "your-app-name"
primary_region = "sjc"  # San Jose

[build]
  builder = "paketobuildpacks/builder:base"

[env]
  PORT = "8000"
  DJANGO_SETTINGS_MODULE = "config.settings.prod"

[[services]]
  internal_port = 8000
  protocol = "tcp"

  [[services.ports]]
    port = 80
    handlers = ["http"]

  [[services.ports]]
    port = 443
    handlers = ["tls", "http"]

  [[services.http_checks]]
    interval = "10s"
    timeout = "2s"
    grace_period = "5s"
    method = "GET"
    path = "/health/"
```

### 3. Set Secrets

```bash
# Required
fly secrets set DJANGO_SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')

fly secrets set DEBUG=False
fly secrets set ALLOWED_HOSTS=your-app.fly.dev

# If using AWS S3
fly secrets set AWS_ACCESS_KEY_ID=your-key
fly secrets set AWS_SECRET_ACCESS_KEY=your-secret
fly secrets set AWS_STORAGE_BUCKET_NAME=your-bucket

# If using Sentry
fly secrets set SENTRY_DSN=your-sentry-dsn

# If using Stripe
fly secrets set STRIPE_PUBLIC_KEY=your-public-key
fly secrets set STRIPE_SECRET_KEY=your-secret-key
```

### 4. Deploy

```bash
fly deploy
```

Your app will be live at `https://your-app.fly.dev`

## Database Setup

### Create PostgreSQL

```bash
fly postgres create
```

Options:
- Name: `your-app-db`
- Region: Same as your app
- Configuration: Development (1GB RAM, 10GB disk)

### Attach Database

```bash
fly postgres attach your-app-db
```

This sets the `DATABASE_URL` secret automatically.

### Create Redis

```bash
fly redis create
```

Options:
- Plan: Free (256MB)
- Region: Same as your app

### Attach Redis

```bash
fly redis attach your-redis
```

This sets the `REDIS_URL` secret automatically.

## Multi-Region Deployment

Deploy to multiple regions for low latency worldwide:

```bash
# Add regions
fly regions add ams  # Amsterdam
fly regions add gru  # São Paulo
fly regions add syd  # Sydney

# Scale to 2 machines per region
fly scale count 2
```

Fly.io automatically routes users to the nearest region.

## Adding Background Workers

### Celery Worker

Create `fly.worker.toml`:

```toml
app = "your-app-worker"

[build]
  builder = "paketobuildpacks/builder:base"

[deploy]
  release_command = "python manage.py migrate"

[[services]]
  internal_port = 8080
  protocol = "tcp"
```

Add Procfile for worker:

```
worker: celery -A config worker -l info
```

Deploy worker:

```bash
fly deploy -c fly.worker.toml
```

### Celery Beat

Similar setup for scheduled tasks:

```
beat: celery -A config beat -l info
```

## Volumes for Persistent Storage

If not using S3:

```bash
# Create volume
fly volumes create data --size 10  # 10GB

# Update fly.toml
[[mounts]]
  source = "data"
  destination = "/data"
```

Update Django settings:

```python
MEDIA_ROOT = "/data/media"
```

## Custom Domains

### Add Domain

```bash
fly certs create yourdomain.com
fly certs create www.yourdomain.com
```

### Configure DNS

Add records to your DNS provider:

```
A     @     66.241.124.123  # Fly.io IP (check dashboard)
AAAA  @     2a09:8280:1::1  # IPv6
CNAME www   your-app.fly.dev
```

Fly.io automatically provisions SSL certificates.

## Monitoring

### View Logs

```bash
# Real-time logs
fly logs

# Last 100 lines
fly logs --lines 100
```

### Metrics

```bash
# Dashboard
fly dashboard

# CLI metrics
fly status
fly vm status
```

### Monitoring Dashboard

Access at: `https://fly.io/apps/your-app/monitoring`

- Request rate
- Response time
- Error rate
- CPU/Memory usage

## Scaling

### Vertical Scaling

```bash
# List available VM sizes
fly platform vm-sizes

# Scale to shared-cpu-2x (2 CPU, 4GB RAM)
fly scale vm shared-cpu-2x
```

VM Sizes:
- **shared-cpu-1x**: 1 CPU, 256MB RAM (free tier)
- **shared-cpu-2x**: 2 CPU, 4GB RAM
- **dedicated-cpu-1x**: 1 vCPU, 2GB RAM
- **dedicated-cpu-2x**: 2 vCPU, 4GB RAM

### Horizontal Scaling

```bash
# Scale to 3 instances
fly scale count 3

# Scale per region
fly scale count 2 --region sjc
fly scale count 2 --region ams
```

### Auto-scaling

```toml
# fly.toml
[[services]]
  internal_port = 8000

  [[services.autoscaling]]
    min_instances = 2
    max_instances = 10
```

## Health Checks

Fly.io uses your `/health/` endpoint:

```toml
[[services.http_checks]]
  interval = "10s"
  timeout = "2s"
  grace_period = "5s"
  method = "GET"
  path = "/health/"
```

Django Keel provides this endpoint by default.

## Zero-Downtime Deployments

Fly.io handles this automatically:

1. Deploys new version
2. Waits for health checks to pass
3. Routes traffic to new version
4. Terminates old version

## Troubleshooting

### Build Fails

**Error: "No Dockerfile found"**
```bash
# Fly.io expects Dockerfile
# Django Keel provides one
ls Dockerfile  # Verify it exists
```

**Error: "requirements.txt not found"**
```bash
# For uv projects, create requirements.txt
uv pip compile pyproject.toml -o requirements.txt
```

### Database Connection

**Error: "could not connect to database"**
```bash
# Check DATABASE_URL is set
fly secrets list | grep DATABASE

# Test connection
fly ssh console
python manage.py dbshell
```

### Memory Issues

**Error: "OOMKilled"**
```bash
# Check memory usage
fly vm status

# Scale up
fly scale vm shared-cpu-2x  # 4GB RAM
```

### SSL Certificate Issues

**Error: "certificate verification failed"**
```bash
# Check certificate status
fly certs show yourdomain.com

# Recreate certificate
fly certs remove yourdomain.com
fly certs create yourdomain.com
```

## Cost Optimization

### Free Tier Limits

- **3 shared-cpu-1x VMs** (256MB RAM each)
- **3GB PostgreSQL storage**
- **160GB outbound transfer**
- **Free HTTPS certificates**

### Tips

1. **Use shared-cpu** for dev/staging
2. **Auto-scale down** during low traffic
3. **Optimize images** - Reduce Docker image size
4. **Use volumes** instead of S3 for small files
5. **Monitor usage** - Set billing alerts

## Production Checklist

- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Set strong `DJANGO_SECRET_KEY`
- [ ] Enable Sentry for error tracking
- [ ] Set up database backups
- [ ] Configure custom domain with SSL
- [ ] Test Celery workers (if using)
- [ ] Configure auto-scaling
- [ ] Set up monitoring alerts
- [ ] Enable database replication for critical apps

## Comparison with Other Platforms

| Feature | Fly.io | Render | Heroku |
|---------|--------|--------|--------|
| **Regions** | 30+ | 7 | 2 (US/EU) |
| **Free Tier** | 3 VMs, 3GB DB | 750 hrs/month | No free tier |
| **Auto-scaling** | ✅ Yes | ✅ Yes | ✅ Yes |
| **SSL** | ✅ Free | ✅ Free | ✅ Free |
| **Pricing** | $1.94+/month | $7+/month | $5-$25+/month |

## Best Practices

1. **Deploy to multiple regions** - Low latency worldwide
2. **Use volumes** for persistent data (if not using S3)
3. **Monitor health checks** - Ensure endpoints respond
4. **Enable auto-scaling** - Handle traffic spikes
5. **Regular backups** - Snapshot PostgreSQL regularly
6. **Use Fly CLI** - Faster than web dashboard
7. **Keep fly.toml** in version control

## Further Reading

- [Fly.io Documentation](https://fly.io/docs/)
- [Fly.io Pricing](https://fly.io/docs/about/pricing/)
- [Fly.io CLI Reference](https://fly.io/docs/flyctl/)

## Support

- **Community Forum**: [community.fly.io](https://community.fly.io/)
- **Status**: [status.fly.io](https://status.fly.io/)
