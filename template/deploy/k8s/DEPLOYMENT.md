# Deploying Test Keel to Kubernetes

This guide shows you how to deploy the Test Keel Django application to Kubernetes.

## Prerequisites

- **kubectl** configured for your cluster
- **Docker** installed
- Access to a container registry (Docker Hub, GCR, ECR, etc.)
- A Kubernetes cluster (minikube, kind, GKE, EKS, AKS, etc.)

## Step 1: Build and Push Docker Image

```bash
cd /path/to/keel-demo

# Build the Docker image
docker build -t test-keel:latest .

# Tag for your registry (replace with your registry)
docker tag test-keel:latest <your-registry>/test-keel:latest

# Push to registry
docker push <your-registry>/test-keel:latest
```

### For local development (minikube/kind):
```bash
# For minikube:
eval $(minikube docker-env)
docker build -t test-keel:latest .

# For kind:
docker build -t test-keel:latest .
kind load docker-image test-keel:latest
```

## Step 2: Install CloudNativePG Operator

```bash
# Install CloudNativePG operator for PostgreSQL management
kubectl apply -f https://raw.githubusercontent.com/cloudnative-pg/cloudnative-pg/release-1.22/releases/cnpg-1.22.0.yaml

# Wait for operator to be ready
kubectl wait --for=condition=Available --timeout=300s \
  deployment/cnpg-controller-manager -n cnpg-system
```

## Step 3: Configure Secrets and ConfigMap

### Update the image reference in kustomization.yaml:
```bash
cd deploy/k8s/kustomize/base
```

Edit `kustomization.yaml` and update the image:
```yaml
images:
  - name: test_keel
    newName: <your-registry>/test-keel  # Change this!
    newTag: latest
```

### Update secrets:
Edit `secret.yaml` and set your actual secrets:
- `DJANGO_SECRET_KEY` - Generate with: `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`
- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_STORAGE_BUCKET_NAME` - For S3 storage
- `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` - For email sending
- `SENTRY_DSN` - For error tracking (optional)

### Update ConfigMap:
Edit `configmap.yaml` and set:
- `DJANGO_ALLOWED_HOSTS` - Your domain name
- `EMAIL_HOST` - Your SMTP server

### Update PostgreSQL password:
Edit `postgresql-cluster.yaml` and change the password in the Secret.

## Step 4: Deploy to Kubernetes

```bash
# From the keel-demo directory
cd deploy/k8s/kustomize/base

# Preview what will be deployed
kubectl kustomize . | less

# Apply the resources
kubectl apply -k .
```

## Step 5: Wait for Resources to be Ready

```bash
# Watch all resources
kubectl get all -w

# Check PostgreSQL cluster status
kubectl get cluster test-keel-pg

# Wait for PostgreSQL to be ready (this may take 2-5 minutes)
kubectl wait --for=condition=Ready cluster/test-keel-pg --timeout=600s

# Check pod status
kubectl get pods

# Watch logs
kubectl logs -f deployment/test-keel-web
```

## Step 6: Run Initial Setup

```bash
# The migrations run automatically via initContainer, but you can verify:
kubectl logs deployment/test-keel-web -c migrate

# Collect static files (one-time)
kubectl exec deployment/test-keel-web -- uv run python manage.py collectstatic --noinput

# Create a superuser
kubectl exec -it deployment/test-keel-web -- uv run python manage.py createsuperuser
```

## Step 7: Access the Application

### Port Forward (for testing):
```bash
kubectl port-forward service/test-keel-web 8000:80
```
Then visit: http://localhost:8000

### Set up Ingress (for production):

Install an ingress controller if you don't have one:
```bash
# For Traefik
helm repo add traefik https://traefik.github.io/charts
helm install traefik traefik/traefik

# For Nginx
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml
```

Create an Ingress:
```bash
cat <<EOF | kubectl apply -f -
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: test-keel-ingress
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  ingressClassName: traefik  # or nginx
  tls:
    - hosts:
        - test-keel.example.com
      secretName: test-keel-tls
  rules:
    - host: test-keel.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: test-keel-web
                port:
                  number: 80
EOF
```

## Monitoring and Troubleshooting

### Check pod status:
```bash
kubectl get pods
kubectl describe pod <pod-name>
```

### View logs:
```bash
# Web pods
kubectl logs -f deployment/test-keel-web

# Celery worker
kubectl logs -f deployment/test-keel-celery-worker

# Celery beat
kubectl logs -f deployment/test-keel-celery-beat

# PostgreSQL
kubectl logs test-keel-pg-1
```

### Check services:
```bash
kubectl get svc
kubectl get endpoints
```

### Debug connectivity:
```bash
# Test from within cluster
kubectl run -it --rm debug --image=busybox --restart=Never -- sh
wget -qO- http://test-keel-web
```

## Scaling

### Scale web pods:
```bash
kubectl scale deployment/test-keel-web --replicas=5
```

### Scale Celery workers:
```bash
kubectl scale deployment/test-keel-celery-worker --replicas=4
```

## Updating the Application

```bash
# Build new image
docker build -t test-keel:v2 .
docker tag test-keel:v2 <your-registry>/test-keel:v2
docker push <your-registry>/test-keel:v2

# Update kustomization.yaml with new tag
# Then apply
kubectl apply -k deploy/k8s/kustomize/base

# Or use kubectl set image
kubectl set image deployment/test-keel-web web=<your-registry>/test-keel:v2
kubectl set image deployment/test-keel-celery-worker celery-worker=<your-registry>/test-keel:v2
kubectl set image deployment/test-keel-celery-beat celery-beat=<your-registry>/test-keel:v2
```

## Clean Up

```bash
# Delete all resources
kubectl delete -k deploy/k8s/kustomize/base

# Delete CloudNativePG operator (optional)
kubectl delete -f https://raw.githubusercontent.com/cloudnative-pg/cloudnative-pg/release-1.22/releases/cnpg-1.22.0.yaml
```

## Production Checklist

- [ ] Change all default passwords
- [ ] Set proper DJANGO_SECRET_KEY
- [ ] Configure proper ALLOWED_HOSTS
- [ ] Set up SSL/TLS certificates
- [ ] Configure proper resource limits and requests
- [ ] Set up monitoring (Prometheus, Grafana)
- [ ] Configure log aggregation
- [ ] Set up automated backups for PostgreSQL
- [ ] Configure horizontal pod autoscaling
- [ ] Set up persistent volumes for media files
- [ ] Configure network policies
- [ ] Set up pod disruption budgets
- [ ] Enable pod security policies
