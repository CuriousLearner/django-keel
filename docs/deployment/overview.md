# 🚀 Deployment Overview

Django Keel supports 6 deployment targets. Choose based on your needs:

## Quick Comparison

| Platform | Best For | Complexity | Cost | Scale |
|----------|----------|------------|------|-------|
| **Render** | Hobby projects, MVPs | ⭐ Easy | $ Low | Small |
| **Fly.io** | Global apps, startups | ⭐⭐ Medium | $$ Medium | Medium |
| **Docker** | Any platform | ⭐⭐ Medium | Varies | Any |
| **AWS EC2** | Full control | ⭐⭐⭐ Advanced | $$ Medium | Large |
| **AWS ECS** | Serverless containers | ⭐⭐⭐⭐ Complex | $$$ High | Large |
| **Kubernetes** | Enterprise | ⭐⭐⭐⭐⭐ Expert | $$$$ Very High | Massive |

## Platform Guides

- [Render](render.md) - One-click PaaS deployment
- [Fly.io](flyio.md) - Global edge deployment
- [Docker](docker.md) - Universal containers
- [AWS EC2 (Ansible)](aws-ec2.md) - Full control with automation
- [AWS ECS Fargate](ecs.md) - Serverless containers
- [Kubernetes](kubernetes.md) - Enterprise-scale

## Decision Guide

### Choose Render if:
- You want one-click deployment
- You're building an MVP or hobby project
- You don't want to manage infrastructure

### Choose Fly.io if:
- You need global edge deployment
- You want low latency worldwide
- You're a startup with growth plans

### Choose Docker if:
- You want portability
- You'll deploy to multiple platforms
- You need local dev/prod parity

### Choose AWS EC2 if:
- You need full server control
- You want on-premise-style deployment
- You have DevOps experience

### Choose AWS ECS if:
- You want serverless containers
- You're already on AWS
- You need high availability

### Choose Kubernetes if:
- You're enterprise-scale
- You need advanced orchestration
- You have Kubernetes expertise
