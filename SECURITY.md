# Security Policy

## Supported Versions

We provide security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 0.x     | :white_check_mark: |

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them via email to:
- **Email**: security@django-keel.dev (monitored by maintainers)

Include the following information:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### What to expect

- **Initial response**: Within 48 hours
- **Status updates**: Every 72 hours until resolved
- **Fix timeline**: Critical issues within 7 days, others within 30 days
- **Credit**: Security researchers will be credited in release notes (unless you prefer to remain anonymous)

## Security Best Practices

Django Keel generates projects with security best practices by default:

- ✅ Django's `check --deploy` runs in CI
- ✅ HSTS, secure cookies, CSP headers enabled in production
- ✅ Dependencies scanned with `pip-audit` and `safety`
- ✅ Container images scanned with Trivy
- ✅ No secrets in repository (environment-based config)
- ✅ SOPS for encrypted secrets (optional)

For enhanced security, use `security_profile: strict` when generating your project.

## Disclosure Policy

When we receive a security report:

1. We confirm the vulnerability and determine severity
2. We develop and test a fix
3. We release a patch version
4. We publicly disclose the vulnerability 7 days after the patch release

## Security Hall of Fame

We recognize and thank security researchers who help keep Django Keel secure.

*No security reports yet - be the first!*

---

Thank you for helping keep Django Keel and our community safe! 🛡️
