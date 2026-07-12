# Kubernetes Deployment

Deploy Django Keel projects to Kubernetes with Helm or Kustomize.

## Prerequisites

- Kubernetes cluster (1.28+)
- kubectl configured
- Helm 3+ (for Helm deployments)

## Helm Deployment

The generated chart lives at `deploy/k8s/helm/<project_slug>/` with the standard layout: `Chart.yaml`, `values.yaml`, and `templates/` (deployment, service, ingress, plus Celery worker/beat when Celery is enabled).

### 1. Build and Push Image

```bash
docker build -t your-registry/your-project:v1.0.0 .
docker push your-registry/your-project:v1.0.0
```

### 2. Configure Values

```bash
cd deploy/k8s/helm/your_project
cp values.yaml values-prod.yaml
# Edit values-prod.yaml: image repository/tag, replica count,
# ingress host, resources, environment
```

### 3. Install Chart

```bash
helm install your-project deploy/k8s/helm/your_project -f values-prod.yaml
```

### 4. Upgrade

```bash
helm upgrade your-project deploy/k8s/helm/your_project -f values-prod.yaml
```

## Kustomize Deployment

Kustomize manifests live in `deploy/k8s/kustomize/` with a `base/` and two overlays: `overlays/dev` and `overlays/prod`.

### 1. Configure Overlays

```bash
cd deploy/k8s/kustomize/overlays/prod
# Edit kustomization.yaml and patches
```

### 2. Deploy

```bash
# Development
kubectl apply -k deploy/k8s/kustomize/overlays/dev

# Production
kubectl apply -k deploy/k8s/kustomize/overlays/prod
```

## PostgreSQL with CloudNativePG

The template ships a CloudNativePG cluster manifest at `deploy/k8s/operators/postgresql-cluster.yaml`. Install the operator first:

```bash
kubectl apply -f https://raw.githubusercontent.com/cloudnative-pg/cloudnative-pg/release-1.25/releases/cnpg-1.25.0.yaml
```

See `deploy/k8s/README.md` in your generated project for the full walkthrough, including local development with Minikube.

## Features

- **CloudNativePG** for PostgreSQL
- **Ingress** configured via chart values (host, TLS secret, annotations)
- **Celery worker and beat** deployments when Celery is enabled
- **ConfigMaps** and **Secrets** management
- **Health checks** (liveness, readiness)
- **Resource limits** and requests

## Monitoring

With `observability_level: full`, the template also generates a Prometheus ServiceMonitor and a Grafana dashboard under `deploy/k8s/monitoring/`.

For full monitoring setup, see the observability documentation.
