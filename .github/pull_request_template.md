## Summary
<!-- Provide a clear and concise description of what this PR does -->

## Related Issues
<!-- Link to related issues using #issue_number -->
Fixes #
Related to #

## Type of Change
<!-- Check all that apply -->
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to change)
- [ ] Documentation update
- [ ] Template configuration change
- [ ] CI/CD update
- [ ] Dependency update
- [ ] Refactoring (no functional changes)

## What Changed
<!-- Provide a detailed description of the changes -->

### Template Changes
<!-- If this affects the generated project template -->
- [ ] Added new Copier prompts
- [ ] Modified existing prompts
- [ ] Added conditional file generation
- [ ] Modified project structure
- [ ] Updated default values

### Components Affected
<!-- Check all that apply -->
- [ ] Core template structure
- [ ] Django settings
- [ ] Authentication/Authorization
- [ ] API (DRF/GraphQL)
- [ ] Frontend (HTMX/Next.js)
- [ ] Background tasks (Celery/Temporal)
- [ ] Deployment configs (K8s/ECS/Fly.io/Render/EC2)
- [ ] Observability (Sentry/OpenTelemetry/Prometheus)
- [ ] SaaS features (Teams/Stripe/Feature flags)
- [ ] Security configuration
- [ ] Database/Cache configuration
- [ ] Docker/Compose setup
- [ ] CI/CD pipelines

## Testing Checklist
<!-- Confirm that you've tested the changes -->
- [ ] Template generation succeeds without errors
- [ ] Generated project structure is valid
- [ ] All template tests pass (`pytest`)
- [ ] Generated project tests pass (`just test` in generated project)
- [ ] Docker builds successfully
- [ ] Pre-commit hooks pass
- [ ] Tested with multiple project types (if applicable)
- [ ] Tested with different configuration combinations
- [ ] Manual testing completed

### Test Coverage
<!-- If applicable, describe test coverage changes -->
- Current coverage: __%
- Coverage change: __% (increase/decrease)

## Breaking Changes
<!-- If this introduces breaking changes, describe them in detail -->
- [ ] No breaking changes
- [ ] Yes, breaking changes (documented below and in CHANGELOG with ⚠️)

<!-- If breaking changes, describe migration path -->
**Migration Guide:**
<!-- How should users update their existing projects? -->

## Backward Compatibility
<!-- How does this affect existing generated projects? -->
- [ ] Fully backward compatible
- [ ] Requires `copier update` with user action
- [ ] Only affects new project generation
- [ ] Requires manual intervention (describe below)

## Security Considerations
<!-- Any security implications of this change? -->
- [ ] No security impact
- [ ] Security improvement
- [ ] Potential security concern (describe below)

<!-- If security-related, explain the impact and mitigation -->

## Documentation
<!-- Check all that apply -->
- [ ] README updated
- [ ] ReadTheDocs documentation updated
- [ ] Inline code comments added/updated
- [ ] CHANGELOG.md updated
- [ ] Generated project docs updated
- [ ] Copier prompt help text updated
- [ ] No documentation needed

## Deployment Impact
<!-- Does this affect any deployment targets? -->
- [ ] No deployment impact
- [ ] Kubernetes manifests updated
- [ ] Helm charts modified
- [ ] Terraform configs changed
- [ ] Ansible playbooks updated
- [ ] Fly.io/Render configs modified
- [ ] Docker/Compose files changed

## Screenshots / Logs
<!-- If applicable, add screenshots of UI changes or command output -->

## Checklist
<!-- Final pre-merge checklist -->
- [ ] Code follows the project's style guidelines (ruff, mypy)
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] No unnecessary debug code or comments
- [ ] Conventional commit message format will be used
- [ ] PR title clearly describes the change

## Additional Notes
<!-- Any additional context, concerns, or information for reviewers -->

---

**Reviewer Notes:**
<!-- Area that needs special attention during review -->
