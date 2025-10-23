# 🚀 Deployment Overview

Django Keel provides production-ready deployment configurations for 6 platforms. Choose based on your needs, budget, and expertise.

## Quick Comparison

| Platform | Best For | Complexity | Monthly Cost* | Auto-Scale | Documentation |
|----------|----------|------------|---------------|------------|---------------|
| **Render** | MVPs, hobby projects | ⭐ Easy | $7-50 | ✅ Yes | [Guide](render.md) |
| **Fly.io** | Global apps, startups | ⭐⭐ Medium | $10-100 | ✅ Yes | [Guide](flyio.md) |
| **Docker** | Any platform | ⭐⭐ Medium | Varies | Platform-dependent | [Guide](docker.md) |
| **AWS EC2** | Full control, on-premise style | ⭐⭐⭐ Advanced | $50-200 | Manual setup | [Guide](aws-ec2.md) |
| **AWS ECS** | Serverless containers | ⭐⭐⭐⭐ Complex | $97-500+ | ✅ Yes | [Guide](ecs.md) |
| **Kubernetes** | Enterprise, multi-cloud | ⭐⭐⭐⭐⭐ Expert | $200-2000+ | ✅ Yes | [Guide](kubernetes.md) |

*Estimated costs for small-medium apps with PostgreSQL, Redis, and basic scaling.

## Platform Guides

### 🟢 Ready for Production

All platforms below have comprehensive documentation and tested deployment configurations:

- **[Render](render.md)** - Zero-config PaaS deployment with `render.yaml`
- **[Fly.io](flyio.md)** - Global edge network deployment with `fly.toml`
- **[AWS ECS Fargate](ecs.md)** - Serverless containers with Terraform IaC
- **[Docker](docker.md)** - Universal containerization for any platform
- **[AWS EC2 (Ansible)](aws-ec2.md)** - Traditional VMs with automation
- **[Kubernetes](kubernetes.md)** - Enterprise orchestration with Helm/Kustomize

## Decision Guide

### Choose Render if:
✅ You want **one-click deployment** from GitHub
✅ You're building an **MVP or hobby project**
✅ You don't want to **manage infrastructure**
✅ You need **$7/month pricing** for small apps
✅ You prefer **PaaS simplicity**

**Free tier:** 750 hours/month web service, 90-day free database
**Scaling:** Automatic horizontal + vertical scaling
**Database:** Managed PostgreSQL + Redis included

### Choose Fly.io if:
✅ You need **global edge deployment** (30+ regions)
✅ You want **low latency worldwide**
✅ You're a **startup with growth plans**
✅ You need **multi-region** by default
✅ You want **generous free tier**

**Free tier:** 3 VMs (256MB each), 3GB PostgreSQL, 160GB bandwidth
**Scaling:** Auto-scale across 30+ regions
**Special:** Anycast routing, WebSocket support

### Choose Docker if:
✅ You want **maximum portability**
✅ You'll **deploy to multiple platforms**
✅ You need **local dev/prod parity**
✅ You're **platform-agnostic**
✅ You have **specific hosting requirements**

**Flexibility:** Deploy anywhere that runs Docker
**Dev Experience:** Identical local and production environments
**Options:** DigitalOcean, Linode, self-hosted, etc.

### Choose AWS EC2 if:
✅ You need **full server control**
✅ You want **on-premise-style deployment**
✅ You have **DevOps experience**
✅ You need **specific OS configurations**
✅ You prefer **traditional VMs**

**Control:** Full root access, custom kernels
**Automation:** Ansible playbooks included
**Cost:** Reserved instances up to 60% savings

### Choose AWS ECS if:
✅ You want **serverless containers**
✅ You're **already on AWS ecosystem**
✅ You need **high availability** (Multi-AZ)
✅ You want **AWS service integrations**
✅ You prefer **managed infrastructure**

**Management:** No servers to manage
**Integration:** Native RDS, ElastiCache, S3, CloudWatch
**HA:** Multi-AZ deployment with auto-failover
**Cost:** ~$97/month minimal setup (see [ECS guide](ecs.md))

### Choose Kubernetes if:
✅ You're at **enterprise scale**
✅ You need **advanced orchestration**
✅ You have **Kubernetes expertise**
✅ You require **multi-cloud deployment**
✅ You need **advanced traffic management**

**Deployment:** Helm charts + Kustomize overlays
**Scale:** Handle massive traffic with ease
**Ecosystem:** Largest cloud-native ecosystem

## Feature Matrix

| Feature | Render | Fly.io | Docker | EC2 | ECS | K8s |
|---------|--------|--------|--------|-----|-----|-----|
| **Setup Time** | 10 min | 15 min | 20 min | 1 hour | 2 hours | 4+ hours |
| **Free Tier** | ✅ Yes | ✅ Yes | N/A | ⚠️ Limited | ❌ No | ❌ No |
| **Managed DB** | ✅ Yes | ✅ Yes | ❌ DIY | ❌ DIY | ✅ RDS | ⚠️ Operator |
| **Auto SSL** | ✅ Free | ✅ Free | ⚠️ Manual | ⚠️ ACM | ✅ ACM | ⚠️ Cert Manager |
| **Auto Scaling** | ✅ Yes | ✅ Yes | ❌ No | ⚠️ Manual | ✅ Yes | ✅ Yes |
| **Multi-Region** | ❌ No | ✅ Yes | Manual | Manual | Manual | ✅ Yes |
| **Logs/Metrics** | Built-in | Built-in | 3rd party | CloudWatch | CloudWatch | Prometheus |
| **Blue/Green Deploy** | ❌ No | ⚠️ Via config | Manual | Manual | ✅ Yes | ✅ Yes |
| **Rollback** | Manual | ✅ Yes | Manual | Manual | ✅ Yes | ✅ Yes |
| **Cost Control** | Good | Good | Varies | Good | Fair | Complex |

## Deployment Files Generated

When you select deployment targets during project generation, Django Keel creates:

### Render
```
deploy/render/
├── build.sh              # Build script
└── README.md
render.yaml               # Blueprint config (root)
```

### Fly.io
```
deploy/flyio/
├── README.md
└── scripts/
fly.toml                  # App config (root)
```

### Docker
```
Dockerfile                # Multi-stage build
docker-compose.yml        # Local development
docker-compose.prod.yml   # Production setup
deploy/docker/
└── README.md
```

### AWS EC2 (Ansible)
```
deploy/ansible/
├── playbooks/
│   ├── setup.yml         # Initial server setup
│   └── deploy.yml        # App deployment
├── roles/
├── inventory/
│   └── hosts.example
└── README.md
```

### AWS ECS (Terraform)
```
deploy/ecs/
├── main.tf               # Main config
├── variables.tf          # Input variables
├── outputs.tf            # Outputs
├── terraform.tfvars.example
├── modules/
│   ├── vpc/
│   ├── rds/
│   ├── redis/
│   ├── ecs/
│   ├── alb/
│   └── ecr/
└── README.md
```

### Kubernetes
```
deploy/k8s/
├── helm/
│   └── my_project/
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/
├── kustomize/
│   ├── base/
│   └── overlays/
│       ├── dev/
│       ├── staging/
│       └── prod/
└── README.md
```

## Getting Started

### 1. During Project Generation

Select your deployment targets when prompted:

```bash
copier copy gh:CuriousLearner/django-keel my-project
```

```
🎤 Deployment targets (comma-separated)?
   [render, flyio, docker, aws-ec2-ansible, aws-ecs-fargate, kubernetes]
   Choose: render,docker
```

You can select multiple targets separated by commas.

### 2. After Generation

Deployment files are created in `deploy/` directory and root:

```bash
cd my-project
ls deploy/
# Output: render/ docker/ (based on your selection)
```

### 3. Follow Platform Guide

Each platform has a detailed README:

```bash
# Example: Render deployment
cat deploy/render/README.md

# Or read online
# https://django-keel.readthedocs.io/deployment/render/
```

## Common Deployment Patterns

### Staging + Production

Most platforms support multiple environments:

**Render:**
```yaml
# render.yaml - separate services
services:
  - name: myapp-staging
    branch: staging
  - name: myapp-production
    branch: main
```

**Fly.io:**
```bash
# Separate apps
fly apps create myapp-staging
fly apps create myapp-production
```

**Kubernetes:**
```bash
# Kustomize overlays
kubectl apply -k deploy/k8s/kustomize/overlays/staging
kubectl apply -k deploy/k8s/kustomize/overlays/prod
```

### Multi-Region Deployment

**Fly.io** (easiest):
```bash
fly regions add ams gru syd  # Amsterdam, São Paulo, Sydney
fly scale count 2
```

**Kubernetes** (most control):
```yaml
# Multi-cluster with Kustomize
clusters:
  - us-west-2
  - eu-central-1
  - ap-southeast-1
```

### Hybrid Approach

You can mix platforms:

- **Primary:** AWS ECS (us-east-1) for main traffic
- **Edge:** Fly.io for global CDN/API edge
- **Development:** Docker Compose locally
- **Staging:** Render for cost efficiency

## Cost Optimization Tips

### All Platforms
1. **Use spot instances** for non-production (EC2, ECS)
2. **Scale down** at night/weekends (automation)
3. **Use reserved instances** for production (AWS)
4. **Monitor costs** with alerts (AWS Cost Explorer, Datadog)

### Platform-Specific

**Render:**
- Use starter plan for staging ($7/month)
- Suspend staging when not in use
- Combine services where possible

**Fly.io:**
- Stay in free tier (3 VMs) for small apps
- Use shared-cpu-1x for dev/staging
- Scale to 0 for inactive apps

**AWS ECS:**
- Use Fargate Spot (70% discount)
- Right-size task definitions
- Use S3 for static files (cheaper than EFS)
- Single NAT gateway for non-prod (~$35/month savings)

**Kubernetes:**
- Use cluster autoscaler
- Implement pod resource requests/limits
- Use spot/preemptible instances
- Consider managed K8s (EKS, GKE) vs self-hosted

## Production Checklist

Before deploying to production, ensure:

### Security
- [ ] Environment variables stored securely (not in code)
- [ ] `DEBUG=False` in production
- [ ] `ALLOWED_HOSTS` configured correctly
- [ ] Strong `DJANGO_SECRET_KEY` set
- [ ] HTTPS enabled (SSL certificates)
- [ ] Database passwords rotated regularly
- [ ] WAF enabled (if using AWS)
- [ ] Security headers configured

### Database
- [ ] Automated backups enabled
- [ ] Backup retention policy set (7-30 days)
- [ ] Database replication configured (if critical)
- [ ] Connection pooling enabled (PgBouncer)
- [ ] Slow query monitoring enabled

### Monitoring
- [ ] Error tracking (Sentry) configured
- [ ] Logging aggregation set up
- [ ] Uptime monitoring (Pingdom, UptimeRobot)
- [ ] Alerts for critical errors
- [ ] Metrics dashboards created
- [ ] APM enabled (New Relic, Datadog)

### Performance
- [ ] Static files served via CDN (CloudFront, Cloudflare)
- [ ] Redis caching configured
- [ ] Database indexes optimized
- [ ] Django DEBUG toolbar disabled
- [ ] Gzip compression enabled
- [ ] Load testing completed

### Deployment
- [ ] CI/CD pipeline configured
- [ ] Automated tests passing
- [ ] Rollback procedure documented
- [ ] Zero-downtime deployment tested
- [ ] Database migration strategy defined
- [ ] Health check endpoint working (`/health/`)

### Documentation
- [ ] Deployment runbook created
- [ ] Incident response plan documented
- [ ] Architecture diagram updated
- [ ] DNS records documented
- [ ] Secrets/credentials inventory maintained

## Troubleshooting

### Build Failures

**Symptoms:** Docker build fails, image too large

**Solutions:**
1. Use multi-stage builds (already in Django Keel)
2. Check `.dockerignore` includes `node_modules`, `.git`, `*.pyc`
3. Verify base image is available
4. Check Python version matches

### Database Connection Issues

**Symptoms:** `OperationalError: could not connect to server`

**Solutions:**
1. Check `DATABASE_URL` environment variable
2. Verify database host is accessible (security groups, VPC)
3. Test connection: `psql $DATABASE_URL`
4. Check database is running: `docker ps` or cloud dashboard

### Static Files Not Loading

**Symptoms:** 404 errors for CSS/JS files

**Solutions:**
1. Run `python manage.py collectstatic --noinput`
2. Check `STATIC_ROOT` and `STATIC_URL` settings
3. Verify storage backend (S3, WhiteNoise) configured
4. Ensure CDN is not caching old files

### Health Check Failures

**Symptoms:** App marked unhealthy, keeps restarting

**Solutions:**
1. Check `/health/` endpoint returns 200
2. Verify database migrations ran
3. Check container logs for startup errors
4. Increase health check grace period

## Migration Between Platforms

### From Render → AWS ECS

1. **Export data:**
   ```bash
   render db dump my-app-db > backup.sql
   ```

2. **Restore to RDS:**
   ```bash
   psql $RDS_DATABASE_URL < backup.sql
   ```

3. **Update DNS:**
   - Point domain to ALB DNS name

### From Docker → Kubernetes

1. **Same Docker image** - No rebuild needed
2. **Create K8s manifests** or use Helm
3. **Migrate data** to managed database
4. **Deploy** with kubectl or Helm

### From Any Platform → Fly.io

1. **Launch app:**
   ```bash
   fly launch
   ```

2. **Create Postgres:**
   ```bash
   fly postgres create
   fly postgres attach
   ```

3. **Migrate data:**
   ```bash
   fly postgres connect -a old-db
   pg_dump | fly postgres connect -a new-db
   ```

## Support & Resources

### Platform Documentation
- [Render Docs](https://render.com/docs)
- [Fly.io Docs](https://fly.io/docs)
- [Docker Docs](https://docs.docker.com/)
- [AWS ECS Docs](https://docs.aws.amazon.com/ecs/)
- [Kubernetes Docs](https://kubernetes.io/docs/)

### Community
- [Django Keel Discussions](https://github.com/CuriousLearner/django-keel/discussions)
- [Django Forum](https://forum.djangoproject.com/)
- Platform-specific forums (see individual guides)

### Professional Support
- Managed Kubernetes: EKS, GKE, AKS
- Deployment consulting: Contact Django Keel maintainers
- Training: See individual platform training resources

## Next Steps

1. **Choose your platform** using the decision guide above
2. **Read the detailed guide** for your chosen platform(s)
3. **Follow the deployment checklist** before going live
4. **Set up monitoring** from day one
5. **Document your setup** for your team

---

**Questions?** Check the [Troubleshooting](#troubleshooting) section or open a [Discussion](https://github.com/CuriousLearner/django-keel/discussions).
