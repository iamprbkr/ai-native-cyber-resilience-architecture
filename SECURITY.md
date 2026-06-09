# Security Policy — AI-Native Cyber Resilience Architecture

**Repository**: `ai-native-cyber-resilience-architecture`  
**URL**: [https://github.com/iamprbkr/ai-native-cyber-resilience-architecture](https://github.com/iamprbkr/ai-native-cyber-resilience-architecture)  
**Version**: 1.x

This document outlines the security practices, vulnerability disclosure process, and supply chain controls for the AI-native cyber resilience platform — an autonomous SOC reference blueprint aligned to NIST CSF 2.0, ISO 27001:2022, Zero Trust (NIST SP 800-207), and MITRE ATT&CK.

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.x     | ✅ Active development |
| < 1.0   | ❌ Pre-release |

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, report via email to: **iamprbkr@users.noreply.github.com**

You should receive a response within **48 hours**. If not, follow up to ensure receipt.

### What to include

- Type of vulnerability (with CWE/CVE if known)
- Full reproduction steps or proof of concept
- Affected versions and components
- Impact assessment (CVSS score if calculated)
- Any suggested remediation

## Security Practices

All platform components implement defense-in-depth across the following controls:

| # | Practice | Implementation | Location |
|---|----------|---------------|----------|
| 1 | **Input Sanitization** | Strips SQLi (`';--`), XSS (`<script>`), path traversal (`../`), and shell metacharacters. Recursively sanitizes nested objects. | `src/security/sanitizer.py` |
| 2 | **RBAC — Least Privilege** | 4 roles (admin, analyst, viewer, automation) with 8 granular permissions. Every service call authorized. | `src/security/rbac.py` |
| 3 | **Audit Logging** | Structured audit entries with timestamp, actor, action, resource, and outcome for all security-relevant operations. | `src/security/audit.py` |
| 4 | **Secrets Management** | Fernet (AES) encryption via `cryptography`. No hardcoded credentials — all secrets via environment variables. | `src/security/secrets.py` |
| 5 | **Human-in-the-Loop** | Critical and high-priority alerts require human approval before playbook execution. Automated only for low/medium. | `src/response/engine.py`, `src/ai/decision_agent.py` |
| 6 | **Data Validation** | Pydantic frozen models with field-level validation, type coercion, and range checks (e.g., risk score 0–100). | `src/models.py`, `src/ingestion/validators.py` |
| 7 | **Data Classification** | 4-tier policy (public/internal/confidential/restricted) with encryption, retention, access control, and audit requirements. | `config/data-classification.yaml` |
| 8 | **Zero Trust Policy** | 4 Policy Enforcement Points (Ingestion, Scoring, Response, Reporting) with trust scoring and continuous validation. | `config/zero-trust-policy.yaml`, `architecture/zero-trust-architecture.md` |
| 9 | **Structured Exception Handling** | 11 typed exceptions. All failures logged, audited, and tracked in telemetry. | `src/exceptions.py` |
| 10 | **Telemetry & Monitoring** | Pipeline-wide latency tracking, success/failure counters, and metrics snapshot for observability. | `src/telemetry.py` |
| 11 | **CI Security Scanning** | GitHub Actions: Bandit SAST, CodeQL analysis, `pip-audit` dependency scanning on every push and weekly. | `.github/workflows/security-scan.yml`, `.github/workflows/ci.yml` |
| 12 | **Pre-commit Hooks** | Automated checks for secrets, private keys, merge conflicts, YAML/JSON validity, trailing whitespace, and mixed line endings. | `.pre-commit-config.yaml` |
| 13 | **Dependency Management** | Pinned versions in `requirements/`, automated updates via Dependabot (weekly pip, monthly GitHub Actions). | `.github/dependabot.yml` |
| 14 | **SAST Regression Tests** | Automated test suite scanning all source files for hardcoded secret patterns, private keys, and API keys. | `tests/security/test_sast.py` |

## Threat Model Coverage

A full STRIDE threat model per component is documented in `architecture/threat-model.md`:

| Component | Threats Addressed |
|-----------|------------------|
| **Ingestion API** | DoS, SQLi, alert replay, spoofing, PII leakage |
| **Message Bus** | Unauthorized access, data flooding, tampering in transit |
| **AI Agent Layer** | Prompt injection, LLM hallucination, model poisoning, data leakage |
| **Response Engine** | Unauthorized execution, credential leakage, malicious playbook actions |
| **Reporting** | Unauthorized metric access, report tampering |

## Supply Chain Security

- All dependencies pinned with exact versions in `requirements/base.txt`, `requirements/dev.txt`, `requirements/test.txt`
- SBOM generation recommended before production deployment
- Dependabot configured for automated weekly dependency updates
- `pip-audit` runs in CI to detect known vulnerabilities in dependencies
- CodeQL scans for supply chain attack patterns (poisoned packages, typosquatting)
- No vendored dependencies — all sourced from trusted registries

## Compliance Frameworks

This platform maps controls to the following standards:

- **NIST CSF 2.0** — Full mapping: `architecture/nist-csf-mapping.md`
- **ISO 27001:2022** — 20+ Annex A controls: `architecture/iso-27001-mapping.md`
- **NIST SP 800-207** — Zero Trust tenets: `architecture/zero-trust-architecture.md`
- **MITRE ATT&CK v14** — 8 techniques mapped: `config/mitre-attack-mapping.yaml`
- **MITRE D3FEND** — Defensive countermeasure mapping: `config/mitre-d3fend-mapping.yaml`

## Risk Register

A full risk register with inherent/residual scoring for 6 key risks is documented in `grc/risk-register.yaml`, including:
- Ransomware, data exfiltration, insider threat, supply chain compromise, regulatory compliance, and AI model poisoning.
