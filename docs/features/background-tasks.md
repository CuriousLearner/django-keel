# Background Tasks

Execute long-running tasks asynchronously with Celery.

## When Enabled

Django Keel configures:

- **Celery** with Redis broker
- **Celery Beat** for periodic tasks
- **Flower** for task monitoring
- **django-celery-results** for result persistence
- **django-celery-beat** for database-backed schedules

See the [Usage Guide](overview.md) for detailed Celery configuration and task examples.
