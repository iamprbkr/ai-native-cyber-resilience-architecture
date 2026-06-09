# Disaster Recovery Plan

## Platform Architecture Recovery

### Service Recovery Order

1. **Message Bus** — Core communication backbone; all services depend on it
2. **Ingestion Service** — Must accept incoming alerts first
3. **Scoring & Correlation** — Processing pipeline
4. **Response Engine** — Automated actions
5. **AI Services** — Non-critical enrichment
6. **Reporting** — Last priority

### Recovery Procedures

#### Message Bus Failure
```bash
# Check cluster status
# Promote secondary to primary
# Verify message queue drain
# Resume ingestion
```

#### Complete Platform Recovery
```bash
# 1. Restore infrastructure from IaC (Terraform/Pulumi)
# 2. Restore database from latest snapshot
# 3. Replay queued messages
# 4. Verify pipeline integrity
# 5. Resume AI services
```

### Backup Strategy

| Data Type | Frequency | Retention | Method |
|-----------|-----------|-----------|--------|
| Alert data | Continuous | 90 days | Message bus persistence |
| Configuration | Per commit | Git history | Infrastructure as Code |
| ML models | Per version | 5 versions | Model registry |
| Audit logs | Daily | 365 days | Append-only store |
| Reports | Weekly | 2 years | Object storage |

### Disaster Recovery Testing

- **Semi-annual**: Full recovery drill in isolated environment
- **Quarterly**: Service-level failover testing
- **Monthly**: Backup restoration validation
