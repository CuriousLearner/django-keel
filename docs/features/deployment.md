# Deployment Options

Django Keel supports multiple deployment targets.

## Kubernetes

- Helm charts for package management
- Kustomize overlays for environment-specific configs
- CloudNativePG for PostgreSQL
- Traefik + cert-manager for ingress
- Horizontal Pod Autoscaling

See [Kubernetes Deployment](../deployment/kubernetes.md) for details.

## AWS EC2 (Ansible)

- Automated provisioning with Ansible
- Caddy reverse proxy with auto-HTTPS
- Systemd service management
- Zero-downtime deployments

See [AWS EC2 Deployment](../deployment/aws-ec2.md) for details.

## Docker

All projects include Dockerfile for containerized deployments.

See [Docker Deployment](../deployment/docker.md) for details.
