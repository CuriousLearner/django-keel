# Deployment Options

Django Keel supports multiple deployment targets, from self-hosted Kubernetes to managed cloud platforms.

## Overview

| Platform | Type | Complexity | Cost | Best For |
|----------|------|------------|------|----------|
| **Kubernetes** | Self-hosted | High | Variable | Large-scale, enterprise |
| **AWS ECS Fargate** | Managed containers | Medium | Pay-per-use | AWS ecosystem, scalable apps |
| **Fly.io** | Global edge | Low | Free tier available | Global deployment, low latency |
| **Render** | Platform-as-Service | Very Low | Free tier available | Quick deployment, hobby projects |
| **AWS EC2 (Ansible)** | Self-hosted VMs | Medium | Variable | Full control, custom setup |
| **Docker** | Containerized | Low | N/A | Any container platform |

## Kubernetes

**Production-grade orchestration for large-scale applications**

- Helm charts for package management
- Kustomize overlays for environment-specific configs
- CloudNativePG for PostgreSQL
- Traefik + cert-manager for ingress
- Horizontal Pod Autoscaling
- Multi-region support

**When to use:**
- Large-scale applications (100+ users)
- Need auto-scaling and high availability
- Complex microservices architecture
- Team has Kubernetes expertise

See [Kubernetes Deployment](../deployment/kubernetes.md) for details.

## AWS ECS Fargate

**Serverless containers on AWS without managing EC2 instances**

- No server management (Fargate)
- Application Load Balancer included
- Auto-scaling based on CPU/memory
- Multi-AZ deployment for high availability
- Integration with AWS services (RDS, S3, CloudWatch)
- Terraform infrastructure-as-code

**When to use:**
- Already using AWS ecosystem
- Want containers without EC2 management
- Need auto-scaling and load balancing
- Prefer serverless approach

**Quick start:**
```bash
# Deploy directory included when deployment_targets includes 'ecs'
cd deploy/ecs/terraform
terraform init
terraform apply
```

See [ECS Fargate Deployment](../deployment/ecs.md) for details.

## Fly.io

**Global edge deployment with automatic scaling**

- Deploy close to users worldwide
- Automatic HTTPS and SSL
- PostgreSQL included
- Redis available
- Free tier (3 VMs, 3GB DB, 160GB bandwidth)
- Deploy with one command: `fly deploy`

**When to use:**
- Need global deployment
- Want low latency worldwide
- Quick deployment (minutes)
- Starting small with free tier
- Mobile app backend

**Quick start:**
```bash
# fly.toml included when deployment_targets includes 'flyio'
fly launch
fly deploy
```

See [Fly.io Deployment](../deployment/flyio.md) for details.

## Render

**Simple platform-as-service with automatic deploys**

- Deploy from GitHub with one click
- Automatic deploys on git push
- PostgreSQL and Redis included
- Automatic SSL certificates
- Free tier available (spins down after 15 min)
- Zero configuration required

**When to use:**
- Hobby projects and MVPs
- Want zero DevOps overhead
- Auto-deploy from GitHub
- Starting with free tier
- Learning Django deployment

**Quick start:**
```bash
# render.yaml included when deployment_targets includes 'render'
# 1. Push to GitHub
# 2. Connect repository in Render dashboard
# 3. Select render.yaml
# 4. Click "Apply"
```

See [Render Deployment](../deployment/render.md) for details.

## AWS EC2 (Ansible)

**Traditional VM deployment with full control**

- Automated provisioning with Ansible
- Caddy reverse proxy with auto-HTTPS
- Systemd service management
- Zero-downtime deployments
- Full control over infrastructure

**When to use:**
- Need full control of infrastructure
- Want traditional VM deployment
- Have Ansible expertise
- Specific compliance requirements

See [AWS EC2 Deployment](../deployment/aws-ec2.md) for details.

## Docker

**Containerized deployment for any platform**

All projects include:
- Optimized Dockerfile
- Multi-stage builds
- docker-compose.yml for local development
- Production-ready configuration

**When to use:**
- Deploying to any container platform
- Local development environment
- Custom deployment setup
- Building CI/CD pipelines

See [Docker Deployment](../deployment/docker.md) for details.

## Comparison

### By Use Case

**Hobby/Personal Project:**
- Best: Render (free tier, auto-deploy)
- Alternative: Fly.io (free tier, global edge)

**Startup/MVP:**
- Best: Fly.io (global, scalable)
- Alternative: Render (simple), ECS Fargate (AWS ecosystem)

**Production App (< 1000 users):**
- Best: Fly.io or ECS Fargate
- Alternative: Render (Standard plan)

**Production App (1000+ users):**
- Best: Kubernetes or ECS Fargate
- Alternative: Fly.io (with scaling)

**Enterprise:**
- Best: Kubernetes (self-hosted or managed)
- Alternative: ECS Fargate (AWS)

### By Developer Experience

**Easiest to Deploy:**
1. Render (one-click from GitHub)
2. Fly.io (`fly deploy`)
3. ECS Fargate (with Terraform)
4. AWS EC2 (with Ansible)
5. Kubernetes (most complex)

**Least DevOps Required:**
1. Render
2. Fly.io
3. ECS Fargate
4. AWS EC2
5. Kubernetes

### By Cost (Production)

**Free Tier Available:**
- Render (limited, spins down)
- Fly.io (3 VMs, 3GB DB)

**Low Cost ($10-50/month):**
- Render Starter ($7/month)
- Fly.io (small instance)
- AWS ECS Fargate (small tasks)

**Medium Cost ($50-200/month):**
- Fly.io (multiple regions)
- ECS Fargate (multiple tasks)
- AWS EC2 (small instances)

**High Cost ($200+/month):**
- Kubernetes (multiple nodes)
- ECS Fargate (large scale)
- AWS EC2 (large instances)

## Configuration

### Deployment Targets

When creating a project, specify deployment targets:

```bash
# Single platform
copier copy . myproject -d deployment_targets=render

# Multiple platforms (comma-separated)
copier copy . myproject -d deployment_targets=kubernetes,flyio,render
```

Available options:
- `kubernetes` - K8s with Helm
- `ecs` - AWS ECS Fargate
- `flyio` - Fly.io
- `render` - Render.com
- `aws-ec2-ansible` - EC2 with Ansible
- `none` - Docker only

### Generated Files

Each deployment target generates specific files:

**Kubernetes:**
- `deploy/k8s/helm/` - Helm charts
- `deploy/k8s/kustomize/` - Kustomize overlays

**ECS Fargate:**
- `deploy/ecs/terraform/` - Terraform configs
- `deploy/ecs/README.md` - Deployment guide

**Fly.io:**
- `fly.toml` - Fly.io configuration
- `deploy/flyio/README.md` - Deployment guide

**Render:**
- `render.yaml` - Render blueprint
- `deploy/render/build.sh` - Build script
- `deploy/render/README.md` - Deployment guide

**AWS EC2:**
- `deploy/ansible/` - Ansible playbooks

**Docker (always included):**
- `Dockerfile` - Multi-stage build
- `docker-compose.yml` - Local development

## Migration Between Platforms

### From Render to Fly.io

```bash
# Export database
render db dump {{ project_slug }}-db > dump.sql

# Import to Fly.io
fly postgres connect
psql < dump.sql
```

### From Fly.io to ECS

```bash
# Export from Fly.io
fly postgres connect -a {{ project_slug }}-db
pg_dump > dump.sql

# Import to RDS
psql -h <rds-endpoint> -U postgres < dump.sql
```

### From Any Platform to Kubernetes

Use standard PostgreSQL dump/restore and update configurations.

## Best Practices

### All Platforms

1. **Environment Variables**: Never commit secrets
2. **Database Backups**: Enable automated backups
3. **SSL/HTTPS**: Always use HTTPS in production
4. **Monitoring**: Set up error tracking (Sentry)
5. **Logging**: Use structured JSON logging

### Static/Media Files

- **Render/Fly.io**: Use S3 for media files
- **ECS**: S3 for both static and media
- **Kubernetes**: S3 or GCS

### Database

- **Development**: SQLite or Docker Postgres
- **Staging/Production**: Managed PostgreSQL (RDS, Render DB, Fly Postgres)

## Resources

- [Kubernetes Deployment Guide](../deployment/kubernetes.md)
- [ECS Fargate Deployment Guide](../deployment/ecs.md)
- [Fly.io Deployment Guide](../deployment/flyio.md)
- [Render Deployment Guide](../deployment/render.md)
- [AWS EC2 Deployment Guide](../deployment/aws-ec2.md)
- [Docker Guide](../deployment/docker.md)

## Support

Each deployment platform has comprehensive documentation in the `deploy/` directory of generated projects.
