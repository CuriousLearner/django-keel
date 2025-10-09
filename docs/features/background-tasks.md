# Background Tasks

Django Keel provides two powerful options for background task processing: **Celery** and **Temporal**. Each has its strengths and is suited for different use cases.

## Overview

| Feature | Celery | Temporal |
|---------|--------|----------|
| **Use Case** | Traditional async tasks | Durable workflows & orchestration |
| **Learning Curve** | Low-Medium | Medium-High |
| **Task Duration** | Minutes-Hours | Minutes-Days-Months |
| **Retries** | Manual configuration | Automatic with backoff |
| **Observability** | Flower + monitoring | Built-in UI & history |
| **Versioning** | Manual | Built-in workflow versioning |
| **State Management** | External (database/cache) | Built-in (durable execution) |
| **Community** | Mature Python ecosystem | Growing, popular in 2025 |

## When to Use Celery

Choose Celery for:
- Simple async tasks (emails, image processing, reports)
- Periodic tasks (cron-like scheduled jobs)
- High throughput (millions of simple tasks)
- Existing Celery expertise
- Lightweight needs without complex orchestration

## When to Use Temporal

Choose Temporal for:
- Complex multi-step workflows with dependencies
- Long-running workflows (days/weeks/months)
- Reliability-critical processes (automatic retries, no lost work)
- Workflows requiring state management
- Saga patterns (distributed transactions with compensation)
- Human-in-the-loop workflows

## Using Both

You can use **both** Celery and Temporal in the same project:
- **Celery**: Simple, high-volume tasks (emails, notifications)
- **Temporal**: Complex workflows (onboarding, payment processing)

When you select `both` during template generation, django-keel sets up both systems independently.

## Configuration

### Celery Setup

- **Docker Compose**: Redis automatically configured
- **Worker**: `celery -A config worker -l info`
- **Beat**: `celery -A config beat -l info`
- **Flower**: Available at `http://localhost:5555`

Environment variables:
```bash
CELERY_BROKER_URL=redis://localhost:6379/1
```

### Temporal Setup

- **Docker Compose**: Temporal server and UI configured
- **Worker**: `python manage.py run_temporal_worker`
- **UI**: Available at `http://localhost:8080`

Environment variables:
```bash
TEMPORAL_ADDRESS=localhost:7233
TEMPORAL_NAMESPACE=default
TEMPORAL_TASK_QUEUE=myproject-tasks
```

## Examples

### Celery Task Example

```python
from celery import shared_task

@shared_task
def send_welcome_email(user_id):
    user = User.objects.get(pk=user_id)
    send_mail(
        subject="Welcome!",
        message=f"Hi {user.name}",
        from_email="noreply@example.com",
        recipient_list=[user.email],
    )
```

### Temporal Workflow Example

```python
from temporalio import workflow
from datetime import timedelta

@workflow.defn
class UserOnboardingWorkflow:
    @workflow.run
    async def run(self, input: OnboardingInput):
        # Step 1: Process user
        await workflow.execute_activity(
            process_user,
            input.user_id,
            start_to_close_timeout=timedelta(seconds=30),
        )

        # Step 2: Send welcome email
        await workflow.execute_activity(
            send_email,
            EmailPayload(to=input.email, subject="Welcome!"),
            start_to_close_timeout=timedelta(seconds=30),
        )

        # Step 3: Wait 24 hours
        await workflow.sleep(timedelta(hours=24))

        # Step 4: Send follow-up
        await workflow.execute_activity(
            send_email,
            EmailPayload(to=input.email, subject="How's it going?"),
            start_to_close_timeout=timedelta(seconds=30),
        )
```

## Resources

### Celery
- [Celery Documentation](https://docs.celeryq.dev/)
- [Django-Celery-Beat](https://django-celery-beat.readthedocs.io/)
- [Flower Monitoring](https://flower.readthedocs.io/)

### Temporal
- [Temporal Documentation](https://docs.temporal.io/)
- [Python SDK Guide](https://docs.temporal.io/develop/python)
- [Temporal Samples](https://github.com/temporalio/samples-python)
- [django-temporalio](https://github.com/RegioHelden/django-temporalio)

## Decision Guide

**Choose Celery if**:
- Simple task queue needs
- Team already familiar with Celery
- High-volume, short-duration tasks
- Minimal learning curve needed

**Choose Temporal if**:
- Complex multi-step workflows
- Long-running processes (hours/days/months)
- Need built-in retry and state management
- Willing to invest in learning curve
- Building saga patterns or distributed transactions

**Choose Both if**:
- Large project with diverse needs
- Want best tool for each job
- Can manage two systems
