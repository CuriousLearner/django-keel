# Observability

Monitor and debug your application in production.

## Levels

The observability level controls logging and metrics. It is independent of error
tracking, which is enabled separately by the "Include Sentry error tracking?" prompt.

### Minimal

- Structured JSON logging
- Health and readiness endpoints (`/health/`, `/ready/`)

### Standard

- Everything in Minimal
- Production request logging with enriched fields (per-request and Celery task logs)

### Full

- Everything in Standard
- **Prometheus** metrics (`django-prometheus`)
- **OpenTelemetry** distributed tracing

With the Kubernetes deployment target, the Full level also generates a Prometheus
`ServiceMonitor` and a Grafana dashboard under `deploy/k8s/monitoring/`.

## Error tracking (Sentry)

Sentry is controlled by its own prompt, not the observability level, so it works at
any level. When enabled it is wired in `config/settings/prod.py` and reads
`SENTRY_DSN` from the environment; at the Full level the Redis integration is added
as well.

See the [Features Overview](overview.md) for the full option list.
