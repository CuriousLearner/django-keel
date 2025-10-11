# Kubernetes Deployment Guide

This guide covers deploying your Django application to Kubernetes, including local testing with minikube.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Local Development (minikube)](#local-development-minikube)
- [Production Deployment](#production-deployment)
- [Configuration](#configuration)
- [Monitoring and Troubleshooting](#monitoring-and-troubleshooting)
- [Scaling](#scaling)
- [Updates and Rollbacks](#updates-and-rollbacks)

## Prerequisites

### Required Tools

- **kubectl** (v1.26+) - Kubernetes command-line tool
- **Docker** - For building container images
- **minikube** (for local testing) - Local Kubernetes cluster
- **kustomize** - Built into kubectl (v1.14+)

### Optional Tools

- **k9s** - Terminal UI for Kubernetes
- **helm** - Package manager for Kubernetes
- **stern** - Multi-pod log tailing

Install kubectl and minikube:
```bash
# macOS
brew install kubectl minikube

# Linux
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
```

## Local Development (minikube)

### Step 1: Start minikube

```bash
# Start minikube with appropriate resources
minikube start --cpus=4 --memory=8192 --disk-size=20g

# Verify minikube is running
minikube status

# Enable metrics (optional)
minikube addons enable metrics-server
```

### Step 2: Build Docker Image

```bash
# Use minikube's Docker daemon to build directly in minikube
eval $(minikube docker-env)

# Build the image (from your project root)
docker build -t {{ project_slug | replace("_", "-") }}:latest .

# Verify the image
docker images | grep {{ project_slug | replace("_", "-") }}
```

### Step 3: Configure for Local Testing

The deployment includes a simple PostgreSQL StatefulSet for local testing. For production, consider using CloudNativePG or a managed database service.

Update the configmap for local testing:
```bash
cd deploy/k8s/kustomize/base
```

Edit `configmap.yaml` and ensure `SECURE_SSL_REDIRECT` is set to `"False"` for local HTTP testing:
```yaml
data:
  SECURE_SSL_REDIRECT: "False"  # Important for local testing
  DEBUG: "False"
  DJANGO_ALLOWED_HOSTS: "*"  # For local testing only
```

### Step 4: Deploy to minikube

```bash
# Apply all resources using kustomize
kubectl apply -k deploy/k8s/kustomize/base

# Watch resources come up
kubectl get pods -w

# Wait for all pods to be ready (this may take 2-3 minutes)
kubectl wait --for=condition=Ready pod -l app={{ project_slug | replace("_", "-") }} --timeout=300s
```

### Step 5: Access the Application

The simplest way to access your application locally is via port-forward:

```bash
# Forward local port 8000 to the service
kubectl port-forward service/{{ project_slug | replace("_", "-") }}-web 8000:80

# In another terminal, test the connection
curl http://localhost:8000/

# Access in browser
open http://localhost:8000
```

Admin interface will be available at: http://localhost:8000/admin/

### Step 6: Create Superuser

```bash
# Create Django superuser
kubectl exec -it deployment/{{ project_slug | replace("_", "-") }}-web -- \
  {% if dependency_manager == 'uv' -%}uv run {% endif %}python manage.py createsuperuser
```

### Verifying the Deployment

Check all components are running:

```bash
# View all resources
kubectl get all -l app={{ project_slug | replace("_", "-") }}

# Check pod status
kubectl get pods

# View logs from web pods
kubectl logs -f deployment/{{ project_slug | replace("_", "-") }}-web

# Check celery workers
kubectl logs -f deployment/{{ project_slug | replace("_", "-") }}-celery-worker

# Check celery beat scheduler
kubectl logs -f deployment/{{ project_slug | replace("_", "-") }}-celery-beat

# View PostgreSQL logs
kubectl logs {{ project_slug | replace("_", "-") }}-pg-0

# View Redis logs
kubectl logs deployment/{{ project_slug | replace("_", "-") }}-redis
```

### Accessing minikube Services

Alternative access methods:

```bash
# Get minikube IP
minikube ip

# Use minikube service command (creates automatic port-forward)
minikube service {{ project_slug | replace("_", "-") }}-web --url

# Access minikube dashboard
minikube dashboard
```

### Stop and Clean Up

```bash
# Delete all resources
kubectl delete -k deploy/k8s/kustomize/base

# Stop minikube
minikube stop

# Delete minikube cluster (removes all data)
minikube delete
```

## Production Deployment

### Architecture Overview

The Kubernetes deployment includes:

- **Web Pods**: Django application with Gunicorn (2 replicas)
- **Celery Workers**: Background task processors (2 replicas)
- **Celery Beat**: Periodic task scheduler (1 replica)
- **PostgreSQL**: Database (StatefulSet with persistent volume)
- **Redis**: Cache and Celery broker (1 replica)

### Step 1: Prepare Container Registry

```bash
# Build and tag image
docker build -t {{ project_slug | replace("_", "-") }}:v1.0.0 .

# Tag for your registry
docker tag {{ project_slug | replace("_", "-") }}:v1.0.0 \
  <your-registry>/{{ project_slug | replace("_", "-") }}:v1.0.0

# Push to registry
docker push <your-registry>/{{ project_slug | replace("_", "-") }}:v1.0.0
```

### Step 2: Configure Secrets

**IMPORTANT**: Never commit secrets to version control!

Generate a secure Django secret key:
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

Edit `deploy/k8s/kustomize/base/secret.yaml` and update all secret values:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: {{ project_slug | replace("_", "-") }}-secrets
stringData:
  DJANGO_SECRET_KEY: "<your-generated-secret-key>"
  AWS_ACCESS_KEY_ID: "<your-aws-key>"
  AWS_SECRET_ACCESS_KEY: "<your-aws-secret>"
  AWS_STORAGE_BUCKET_NAME: "<your-s3-bucket>"
  EMAIL_HOST_USER: "<smtp-username>"
  EMAIL_HOST_PASSWORD: "<smtp-password>"
  SENTRY_DSN: "<your-sentry-dsn>"
```

For PostgreSQL credentials, edit `secret.yaml`:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: {{ project_slug | replace("_", "-") }}-pg-credentials
stringData:
  username: {{ project_slug }}_user
  password: "<strong-database-password>"  # Change this!
```

### Step 3: Configure Application Settings

Edit `deploy/k8s/kustomize/base/configmap.yaml`:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ project_slug | replace("_", "-") }}-config
data:
  DEBUG: "False"
  DJANGO_SETTINGS_MODULE: "config.settings.prod"
  DJANGO_ALLOWED_HOSTS: "your-domain.com,{{ project_slug | replace("_", "-") }}-web"
  SECURE_SSL_REDIRECT: "True"  # Enable for production with HTTPS
  EMAIL_HOST: "smtp.your-email-provider.com"
  EMAIL_PORT: "587"
  EMAIL_USE_TLS: "True"
```

### Step 4: Update Image References

Edit `deploy/k8s/kustomize/base/kustomization.yaml`:

```yaml
images:
  - name: {{ project_slug | replace("_", "-") }}
    newName: <your-registry>/{{ project_slug | replace("_", "-") }}
    newTag: v1.0.0
```

### Step 5: Choose Database Option

#### Option A: Simple PostgreSQL (Development/Testing)

Uses the included `postgresql-simple.yaml` (default in kustomization).

#### Option B: CloudNativePG Operator (Production)

For production, use the CloudNativePG operator for managed PostgreSQL:

```bash
# Install CloudNativePG operator
kubectl apply -f https://raw.githubusercontent.com/cloudnative-pg/cloudnative-pg/release-1.22/releases/cnpg-1.22.0.yaml

# Wait for operator
kubectl wait --for=condition=Available --timeout=300s \
  deployment/cnpg-controller-manager -n cnpg-system

# Update kustomization.yaml to use postgresql-cluster.yaml instead of postgresql-simple.yaml
```

Edit `kustomization.yaml`:
```yaml
resources:
  - postgresql-cluster.yaml  # Use this instead of postgresql-simple.yaml
  - redis.yaml
  - deployment.yaml
  - celery-worker.yaml
  - service.yaml
  - configmap.yaml
  - secret.yaml
```

### Step 6: Deploy Using Overlays

Use overlays for environment-specific configurations:

```bash
# Deploy to development
kubectl apply -k deploy/k8s/kustomize/overlays/dev

# Deploy to production
kubectl apply -k deploy/k8s/kustomize/overlays/prod
```

Or deploy base configuration:
```bash
kubectl apply -k deploy/k8s/kustomize/base
```

### Step 7: Verify Deployment

```bash
# Check rollout status
kubectl rollout status deployment/{{ project_slug | replace("_", "-") }}-web
kubectl rollout status deployment/{{ project_slug | replace("_", "-") }}-celery-worker
kubectl rollout status deployment/{{ project_slug | replace("_", "-") }}-celery-beat

# Verify all pods are running
kubectl get pods -l app={{ project_slug | replace("_", "-") }}

# Check services and endpoints
kubectl get svc,endpoints
```

### Step 8: Set Up Ingress

Install an ingress controller:

```bash
# For NGINX Ingress Controller
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml

# For Traefik
helm repo add traefik https://traefik.github.io/charts
helm install traefik traefik/traefik
```

Create Ingress resource:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {{ project_slug | replace("_", "-") }}-ingress
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - your-domain.com
      secretName: {{ project_slug | replace("_", "-") }}-tls
  rules:
    - host: your-domain.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: {{ project_slug | replace("_", "-") }}-web
                port:
                  number: 80
```

Apply:
```bash
kubectl apply -f ingress.yaml
```

### Step 9: Set Up TLS Certificates

Install cert-manager:
```bash
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml
```

Create ClusterIssuer:
```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: your-email@example.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
      - http01:
          ingress:
            class: nginx
```

## Configuration

### Environment Variables

Key environment variables (set in ConfigMap):

| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Enable debug mode | `False` |
| `DJANGO_SETTINGS_MODULE` | Settings module | `config.settings.prod` |
| `DJANGO_ALLOWED_HOSTS` | Allowed hosts | Required |
| `SECURE_SSL_REDIRECT` | Redirect HTTP to HTTPS | `True` |
| `DATABASE_URL` | PostgreSQL connection | Auto-configured |
| `REDIS_URL` | Redis connection | Auto-configured |
| `CELERY_BROKER_URL` | Celery broker | Auto-configured |

### Resource Limits

Default resource allocations:

**Web Pods:**
- Requests: 500m CPU, 512Mi memory
- Limits: 2000m CPU, 1Gi memory

**Celery Worker:**
- Requests: 250m CPU, 512Mi memory
- Limits: 1000m CPU, 1Gi memory

**Celery Beat:**
- Requests: 100m CPU, 256Mi memory
- Limits: 500m CPU, 512Mi memory

**PostgreSQL:**
- Requests: 250m CPU, 256Mi memory
- Limits: 500m CPU, 512Mi memory
- Storage: 1Gi (increase for production)

Adjust in deployment YAML files as needed.

### Health Checks

The deployment uses TCP socket probes to verify application availability:

```yaml
livenessProbe:
  tcpSocket:
    port: http
  initialDelaySeconds: 60
  periodSeconds: 10

readinessProbe:
  tcpSocket:
    port: http
  initialDelaySeconds: 15
  periodSeconds: 10
```

## Monitoring and Troubleshooting

### View Logs

```bash
# Tail logs from web pods
kubectl logs -f deployment/{{ project_slug | replace("_", "-") }}-web

# View logs from specific pod
kubectl logs <pod-name>

# View logs from init container (migrations)
kubectl logs <pod-name> -c migrate

# View logs from all celery workers
kubectl logs -f deployment/{{ project_slug | replace("_", "-") }}-celery-worker --all-containers=true

# Use stern for multi-pod log tailing
stern {{ project_slug | replace("_", "-") }}-web
```

### Debug Pod Issues

```bash
# Describe pod to see events
kubectl describe pod <pod-name>

# Check resource usage
kubectl top pods

# Execute commands in pod
kubectl exec -it <pod-name> -- /bin/sh

# Test database connectivity
kubectl exec -it deployment/{{ project_slug | replace("_", "-") }}-web -- \
  {% if dependency_manager == 'uv' -%}uv run {% endif %}python manage.py dbshell

# Run Django shell
kubectl exec -it deployment/{{ project_slug | replace("_", "-") }}-web -- \
  {% if dependency_manager == 'uv' -%}uv run {% endif %}python manage.py shell
```

### Common Issues

#### Pods Not Starting

```bash
# Check events
kubectl get events --sort-by='.lastTimestamp'

# Check pod events
kubectl describe pod <pod-name>

# Common causes:
# - Image pull errors: Check image name and registry credentials
# - Resource limits: Check cluster capacity
# - Configuration errors: Check environment variables and secrets
```

#### Database Connection Issues

```bash
# Check PostgreSQL status
kubectl get pods -l component=postgresql

# View PostgreSQL logs
kubectl logs {{ project_slug | replace("_", "-") }}-pg-0

# Test connectivity from web pod
kubectl exec -it deployment/{{ project_slug | replace("_", "-") }}-web -- \
  nc -zv {{ project_slug | replace("_", "-") }}-pg 5432
```

#### Celery Tasks Not Running

```bash
# Check celery worker logs
kubectl logs -f deployment/{{ project_slug | replace("_", "-") }}-celery-worker

# Check celery beat logs
kubectl logs -f deployment/{{ project_slug | replace("_", "-") }}-celery-beat

# Verify Redis connectivity
kubectl exec -it deployment/{{ project_slug | replace("_", "-") }}-web -- \
  nc -zv {{ project_slug | replace("_", "-") }}-redis-master 6379
```

## Scaling

### Manual Scaling

```bash
# Scale web pods
kubectl scale deployment/{{ project_slug | replace("_", "-") }}-web --replicas=5

# Scale celery workers
kubectl scale deployment/{{ project_slug | replace("_", "-") }}-celery-worker --replicas=4
```

### Horizontal Pod Autoscaling

Create HPA for web pods:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: {{ project_slug | replace("_", "-") }}-web-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: {{ project_slug | replace("_", "-") }}-web
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
```

Apply:
```bash
kubectl apply -f hpa.yaml
```

## Updates and Rollbacks

### Rolling Updates

```bash
# Build new version
docker build -t {{ project_slug | replace("_", "-") }}:v1.1.0 .
docker tag {{ project_slug | replace("_", "-") }}:v1.1.0 <your-registry>/{{ project_slug | replace("_", "-") }}:v1.1.0
docker push <your-registry>/{{ project_slug | replace("_", "-") }}:v1.1.0

# Update image using kubectl
kubectl set image deployment/{{ project_slug | replace("_", "-") }}-web \
  web=<your-registry>/{{ project_slug | replace("_", "-") }}:v1.1.0

# Watch rollout
kubectl rollout status deployment/{{ project_slug | replace("_", "-") }}-web

# Check rollout history
kubectl rollout history deployment/{{ project_slug | replace("_", "-") }}-web
```

### Rollback

```bash
# Rollback to previous version
kubectl rollout undo deployment/{{ project_slug | replace("_", "-") }}-web

# Rollback to specific revision
kubectl rollout undo deployment/{{ project_slug | replace("_", "-") }}-web --to-revision=2

# Pause rollout (for issues)
kubectl rollout pause deployment/{{ project_slug | replace("_", "-") }}-web

# Resume rollout
kubectl rollout resume deployment/{{ project_slug | replace("_", "-") }}-web
```

## Production Checklist

Before deploying to production:

### Security
- [ ] Change all default passwords in secrets
- [ ] Generate strong `DJANGO_SECRET_KEY`
- [ ] Configure proper `ALLOWED_HOSTS`
- [ ] Enable `SECURE_SSL_REDIRECT=True`
- [ ] Set up TLS/SSL certificates with cert-manager
- [ ] Enable network policies
- [ ] Set up pod security standards
- [ ] Configure RBAC properly
- [ ] Use private container registry

### Database
- [ ] Use CloudNativePG or managed database service
- [ ] Configure automated backups
- [ ] Set up point-in-time recovery
- [ ] Configure connection pooling
- [ ] Increase storage size from default 1Gi
- [ ] Set up database monitoring

### Reliability
- [ ] Configure resource requests and limits
- [ ] Set up horizontal pod autoscaling
- [ ] Configure pod disruption budgets
- [ ] Set up liveness and readiness probes
- [ ] Configure persistent volumes for media files
- [ ] Test disaster recovery procedures

### Observability
- [ ] Set up Prometheus monitoring
- [ ] Configure Grafana dashboards
- [ ] Set up log aggregation (ELK/Loki)
- [ ] Configure Sentry for error tracking
- [ ] Set up alerts for critical issues
- [ ] Enable tracing (optional)

### Performance
- [ ] Enable Redis for caching
- [ ] Configure CDN for static files
- [ ] Optimize database queries
- [ ] Set up connection pooling
- [ ] Configure appropriate worker counts
- [ ] Enable compression

### Compliance
- [ ] Review data residency requirements
- [ ] Configure audit logging
- [ ] Set up backup retention policies
- [ ] Document security procedures
- [ ] Set up access controls

## Additional Resources

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [CloudNativePG Documentation](https://cloudnative-pg.io/documentation/)
- [Kustomize Documentation](https://kustomize.io/)
- [Helm Documentation](https://helm.sh/docs/)

## Getting Help

If you encounter issues:

1. Check pod logs: `kubectl logs <pod-name>`
2. Check events: `kubectl get events`
3. Describe resources: `kubectl describe <resource-type> <resource-name>`
4. Check resource status: `kubectl get all`
5. Review this documentation
6. Check Kubernetes troubleshooting guides
