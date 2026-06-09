# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.x     | ✅ Active development |
| < 1.0   | ❌ Pre-release |

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, report via email to: **iamprbkr@users.noreply.github.com**

You should receive a response within 48 hours. If not, follow up to ensure receipt.

### What to include

- Type of vulnerability
- Full reproduction steps
- Affected versions
- Any proof-of-concept code (if available)
- Impact assessment

## Security Practices

This project follows these security practices:

1. **No hardcoded secrets** — All credentials via environment variables or secrets manager
2. **Input validation** — All external input sanitized before processing
3. **Least privilege** — RBAC enforced at every service boundary
4. **Audit logging** — All security-relevant actions logged immutably
5. **Dependency scanning** — Automated via Dependabot and `pip-audit`
6. **SAST scanning** — Bandit and CodeQL in CI pipeline
7. **Pre-commit hooks** — Detect secrets, validate code before commit

## Supply Chain Security

- All dependencies pinned with exact versions in `requirements/`
- SBOM generation recommended before production deployment
- Dependabot configured for automated dependency updates
