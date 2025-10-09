# Kubernetes Deployment

Deploy Django Keel projects to Kubernetes with Helm or Kustomize.

## Prerequisites

- Kubernetes cluster (1.28+)
- kubectl configured
- Helm 3+ (for Helm deployments)

## Helm Deployment

### 1. Build and Push Image

```bash
docker build -t your-registry/your-project:v1.0.0 .
docker push your-registry/your-project:v1.0.0
```

### 2. Configure Values

```bash
cd deploy/k8s/helm/your_project
cp values.yaml values-prod.yaml
# Edit values-prod.yaml with your configuration
```

### 3. Install Chart

```bash
helm install your-project . -f values-prod.yaml
```

### 4. Upgrade

```bash
helm upgrade your-project . -f values-prod.yaml
```

## Kustomize Deployment

### 1. Configure Overlays

```bash
cd deploy/k8s/kustomize/overlays/prod
# Edit kustomization.yaml and patches
```

### 2. Deploy

```bash
kubectl apply -k deploy/k8s/kustomize/overlays/prod
```

## Features

- **CloudNativePG** for PostgreSQL
- **Horizontal Pod Autoscaling**
- **Ingress** with TLS via cert-manager
- **ConfigMaps** and **Secrets** management
- **Health checks** (liveness, readiness)
- **Resource limits** and requests

## Monitoring

Kubernetes deployments include Prometheus metrics and health endpoints.

For full monitoring setup, see the observability documentation.
