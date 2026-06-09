# Zero Trust Architecture

## Alignment with NIST SP 800-207

### Core Tenets

| Zero Trust Tenet | Implementation |
|-----------------|----------------|
| All data sources and computing services are resources | Every service in the platform is a resource with explicit access policy |
| All communication is secured regardless of network location | mTLS between all services, no network trust |
| Access to resources is granted on a per-session basis | API keys + RBAC for every operation |
| Access is determined by dynamic policy | Risk score-based action gating |
| Monitor and measure all assets and data flows | Comprehensive audit logging and telemetry |
| Dynamic authentication and authorization before access | Every API call validated regardless of origin |
| Collect as much information as possible for security posture | Full pipeline telemetry, all decisions logged |

### Policy Enforcement Points (PEP)

```
Request → PEP (Ingestion API) → Policy Engine (RBAC + Scoring) → Resource
```

1. **Ingestion API Gate**: Validates source identity, schema, rate limits
2. **Scoring Policy Gate**: Determines if action requires approval based on risk score
3. **Response Policy Gate**: Requires human approval for critical/high priority actions
4. **Reporting Policy Gate**: Enforces RBAC on report data access

### Micro-Segmentation

| Segment | Services | Ingress | Egress |
|---------|----------|---------|--------|
| **Ingress** | Ingestion API | Sources only | Message bus only |
| **Processing** | Enrichment, Scoring, Correlation | Message bus only | Message bus only |
| **AI** | AI Agents | Message bus only | Message bus only |
| **Response** | Response Engine | Message bus only | External APIs (whitelisted) |
| **Reporting** | Metrics, Reports | Message bus, Analyst | Dashboard, Email |

### Trust Scoring

```
Trust Score = f(identity_confidence, device_health, location_risk, behavior_anomaly)
```

- **Score >= 0.8**: Full access, automated decisions
- **Score 0.5–0.79**: Conditional access, human approval required
- **Score < 0.5**: Deny, escalate to administrator

### Continuous Validation

All sessions are continuously validated:
- Session timeout: 15 minutes for interactive, 5 minutes for automated
- Re-validation on privilege escalation
- Anomaly detection triggers session revocation
