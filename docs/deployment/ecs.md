# AWS ECS Fargate Deployment

Deploy Django Keel with serverless containers using AWS ECS Fargate and Terraform.

## Overview

AWS ECS Fargate provides serverless container deployment with:

- **No server management** - AWS manages infrastructure
- **Auto-scaling** - Scale based on CPU/memory/requests
- **High availability** - Multi-AZ deployment
- **AWS integration** - RDS, S3, CloudWatch, Secrets Manager
- **Terraform IaC** - Infrastructure as code
- **Load balancing** - Application Load Balancer included

## Prerequisites

- AWS account with appropriate permissions
- AWS CLI configured (`aws configure`)
- Terraform installed (v1.5+)
- `deployment_targets: [ecs]` selected during generation

## Quick Start

### 1. Configure Terraform Variables

```bash
cd deploy/ecs
cp terraform.tfvars.example terraform.tfvars
```

Edit `terraform.tfvars`:

```hcl
# Project Configuration
project_name = "your-project"
environment  = "production"
aws_region   = "us-west-2"

# Application Configuration
app_port          = 8000
container_cpu     = 512   # 0.5 vCPU
container_memory  = 1024  # 1 GB

# Database Configuration
db_instance_class = "db.t4g.micro"  # Free tier eligible
db_name          = "your_project_db"
db_username      = "admin"

# Domain Configuration (optional)
domain_name      = "yourdomain.com"
certificate_arn  = "arn:aws:acm:us-west-2:123456789:certificate/abc123"
```

### 2. Initialize Terraform

```bash
terraform init
```

### 3. Plan Deployment

```bash
terraform plan
```

Review the resources that will be created:
- VPC with public/private subnets
- RDS PostgreSQL database
- ElastiCache Redis cluster
- ECS cluster and service
- Application Load Balancer
- CloudWatch log groups
- IAM roles and policies

### 4. Deploy

```bash
terraform apply
```

Type `yes` to confirm. Deployment takes ~10 minutes.

Your app will be available at the ALB DNS name (output after apply).

## Architecture

```
Internet
    ↓
Application Load Balancer (ALB)
    ↓
ECS Service (Fargate)
    ├── Task 1 (Private Subnet AZ-A)
    ├── Task 2 (Private Subnet AZ-B)
    └── Task 3 (Auto-scaled)
         ↓
    RDS PostgreSQL (Multi-AZ)
    ElastiCache Redis
    S3 (Media/Static files)
```

## Project Structure

Generated with `deployment_targets: [ecs]`:

```
deploy/ecs/
├── main.tf                 # Main configuration
├── variables.tf            # Input variables
├── outputs.tf              # Output values
├── terraform.tfvars        # Your values (gitignored)
├── modules/
│   ├── vpc/               # VPC, subnets, NAT gateways
│   ├── rds/               # PostgreSQL database
│   ├── redis/             # ElastiCache Redis
│   ├── ecs/               # ECS cluster & service
│   ├── alb/               # Application Load Balancer
│   └── ecr/               # Container registry
└── README.md
```

## Terraform Modules

### VPC Module

Creates networking infrastructure:
- VPC with CIDR block
- Public subnets (ALB)
- Private subnets (ECS tasks, RDS)
- Internet Gateway
- NAT Gateways (high availability)
- Route tables

### RDS Module

PostgreSQL database:
- Multi-AZ deployment
- Automated backups (7 days retention)
- Encryption at rest
- Security group (private subnets only)

### ECS Module

Container orchestration:
- ECS cluster
- Task definition (Django app)
- Service with desired count
- Auto-scaling policies
- CloudWatch logs

### ALB Module

Load balancing:
- Application Load Balancer
- Target group (ECS tasks)
- Health checks (`/health/`)
- HTTPS listener (optional)
- HTTP → HTTPS redirect

## Environment Variables

Set via AWS Secrets Manager:

```bash
# Create secret
aws secretsmanager create-secret \
  --name /your-project/prod/django \
  --secret-string '{
    "DJANGO_SECRET_KEY": "your-secret-key",
    "DEBUG": "False",
    "ALLOWED_HOSTS": "yourdomain.com",
    "AWS_STORAGE_BUCKET_NAME": "your-bucket",
    "SENTRY_DSN": "your-sentry-dsn",
    "STRIPE_SECRET_KEY": "your-stripe-key"
  }'
```

Terraform automatically injects secrets into ECS tasks.

## Deploying Updates

### 1. Build and Push Image

```bash
# Login to ECR
aws ecr get-login-password --region us-west-2 | \
  docker login --username AWS --password-stdin \
  123456789.dkr.ecr.us-west-2.amazonaws.com

# Build image
docker build -t your-project:latest .

# Tag for ECR
docker tag your-project:latest \
  123456789.dkr.ecr.us-west-2.amazonaws.com/your-project:latest

# Push
docker push 123456789.dkr.ecr.us-west-2.amazonaws.com/your-project:latest
```

### 2. Update ECS Service

```bash
# ECS automatically detects new image
aws ecs update-service \
  --cluster your-project-cluster \
  --service your-project-service \
  --force-new-deployment
```

Or use Terraform:

```bash
terraform apply -target=module.ecs
```

## Auto-Scaling

Configure in `terraform.tfvars`:

```hcl
# Auto-scaling configuration
autoscaling_min_capacity = 2
autoscaling_max_capacity = 10

# Scale on CPU
cpu_target_value = 70  # Target 70% CPU

# Scale on memory
memory_target_value = 80  # Target 80% memory

# Scale on ALB requests
alb_request_count_target = 1000  # Requests per target
```

ECS auto-scales based on these metrics.

## Database Migrations

Run migrations before deploying new tasks:

```bash
# Option 1: ECS Exec into running task
aws ecs execute-command \
  --cluster your-project-cluster \
  --task <task-id> \
  --container django \
  --command "python manage.py migrate" \
  --interactive

# Option 2: Run one-off task
aws ecs run-task \
  --cluster your-project-cluster \
  --task-definition your-project-task \
  --launch-type FARGATE \
  --network-configuration '{
    "awsvpcConfiguration": {
      "subnets": ["subnet-abc123"],
      "securityGroups": ["sg-abc123"]
    }
  }' \
  --overrides '{
    "containerOverrides": [{
      "name": "django",
      "command": ["python", "manage.py", "migrate"]
    }]
  }'
```

## Background Workers (Celery)

Add Celery service to Terraform:

```hcl
# modules/ecs/celery.tf
resource "aws_ecs_task_definition" "celery_worker" {
  family = "${var.project_name}-celery-worker"

  container_definitions = jsonencode([{
    name  = "celery-worker"
    image = "${var.ecr_repository_url}:latest"
    command = ["celery", "-A", "config", "worker", "-l", "info"]

    environment = [
      { name = "DJANGO_SETTINGS_MODULE", value = "config.settings.prod" }
    ]

    secrets = [
      { name = "DATABASE_URL", valueFrom = aws_secretsmanager_secret.django.arn }
    ]
  }])
}

resource "aws_ecs_service" "celery_worker" {
  name            = "${var.project_name}-celery-worker"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.celery_worker.arn
  desired_count   = 2
  launch_type     = "FARGATE"
}
```

## Monitoring

### CloudWatch Logs

View logs:

```bash
# Web application logs
aws logs tail /ecs/your-project --follow

# Celery worker logs
aws logs tail /ecs/your-project-celery --follow
```

### CloudWatch Metrics

Monitor in AWS Console:
- ECS → Clusters → your-project → Metrics
- Key metrics: CPU, Memory, Request count

### Alarms

Terraform creates alarms for:
- High CPU utilization (> 80%)
- High memory utilization (> 80%)
- ECS service unhealthy tasks
- RDS high connections

## Custom Domain

### 1. Request SSL Certificate

```bash
aws acm request-certificate \
  --domain-name yourdomain.com \
  --validation-method DNS \
  --region us-west-2
```

### 2. Validate Certificate

Add DNS records shown in ACM console.

### 3. Update Terraform

```hcl
# terraform.tfvars
domain_name     = "yourdomain.com"
certificate_arn = "arn:aws:acm:us-west-2:123:certificate/abc"
```

```bash
terraform apply
```

### 4. Update DNS

Point your domain to the ALB:

```
CNAME yourdomain.com your-alb-123.us-west-2.elb.amazonaws.com
```

## Disaster Recovery

### Database Backups

RDS automatic backups:
- Retention: 7 days (configurable)
- Automated snapshots daily
- Point-in-time recovery available

Manual snapshot:

```bash
aws rds create-db-snapshot \
  --db-instance-identifier your-project-db \
  --db-snapshot-identifier manual-backup-$(date +%Y%m%d)
```

### Restore from Backup

```bash
aws rds restore-db-instance-from-db-snapshot \
  --db-instance-identifier your-project-db-restored \
  --db-snapshot-identifier manual-backup-20250109
```

Update Terraform to point to restored database.

## Cost Optimization

### Estimated Monthly Costs

**Minimal setup** (1 task, db.t4g.micro, 1GB traffic):
- ECS Fargate: ~$15
- RDS db.t4g.micro: ~$15
- ALB: ~$20
- NAT Gateway: ~$35
- ElastiCache (cache.t4g.micro): ~$12
- **Total**: ~$97/month

### Optimization Tips

1. **Use Spot instances** for non-production
2. **Scheduled scaling** - Scale down at night
3. **Use S3 for static files** - Cheaper than EFS
4. **Single NAT Gateway** for non-prod (not HA)
5. **RDS reserved instances** - Up to 60% savings
6. **CloudFront CDN** - Reduce ALB data transfer costs

## Troubleshooting

### Task Keeps Restarting

```bash
# Check task stopped reason
aws ecs describe-tasks \
  --cluster your-project-cluster \
  --tasks <task-id>

# Check logs
aws logs tail /ecs/your-project --since 1h
```

Common causes:
- Health check failing (`/health/` endpoint)
- Database connection issues
- Missing environment variables
- Out of memory (increase `container_memory`)

### Database Connection Timeout

```bash
# Check security group rules
aws ec2 describe-security-groups \
  --group-ids sg-abc123

# Verify RDS is in same VPC
aws rds describe-db-instances \
  --db-instance-identifier your-project-db
```

### High Costs

```bash
# Analyze costs
aws ce get-cost-and-usage \
  --time-period Start=2025-01-01,End=2025-01-31 \
  --granularity MONTHLY \
  --metrics BlendedCost \
  --group-by Type=SERVICE
```

Check:
- NAT Gateway data transfer
- ALB idle time
- Underutilized RDS instances

## Production Checklist

- [ ] Enable RDS Multi-AZ
- [ ] Configure automated backups
- [ ] Set up CloudWatch alarms
- [ ] Enable ECS Container Insights
- [ ] Configure WAF rules on ALB
- [ ] Set up VPC Flow Logs
- [ ] Enable AWS Config for compliance
- [ ] Use Secrets Manager for sensitive data
- [ ] Configure auto-scaling policies
- [ ] Set up CI/CD pipeline (GitHub Actions/GitLab CI)
- [ ] Document runbooks for common issues
- [ ] Test disaster recovery procedures

## Best Practices

1. **Use Terraform workspaces** for multiple environments
2. **Store state in S3** with DynamoDB locking
3. **Tag all resources** for cost tracking
4. **Use IAM roles** (not access keys) for ECS tasks
5. **Enable encryption** for RDS, S3, secrets
6. **Implement blue/green deployments** for zero downtime
7. **Use VPC endpoints** to reduce NAT costs
8. **Regular security audits** with AWS Trusted Advisor

## Further Reading

- [AWS ECS Documentation](https://docs.aws.amazon.com/ecs/)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [ECS Best Practices](https://docs.aws.amazon.com/AmazonECS/latest/bestpracticesguide/)

## Support

- **AWS Support**: Available in AWS Console
- **Terraform Community**: [discuss.hashicorp.com](https://discuss.hashicorp.com/)
- **Stack Overflow**: [aws-ecs](https://stackoverflow.com/questions/tagged/amazon-ecs)
