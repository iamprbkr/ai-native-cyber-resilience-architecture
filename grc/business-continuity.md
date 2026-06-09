# Business Continuity Plan

## Scope
This BCP covers the AI-native cyber resilience platform itself. It ensures the platform remains operational or recovers within defined RTO/RPO during disruptions.

## Recovery Objectives

| Tier | RTO | RPO | Description |
|------|-----|-----|-------------|
| Critical | 15 min | 5 min | Alert ingestion, scoring, correlation |
| High | 1 hour | 15 min | Playbook execution, automated response |
| Medium | 4 hours | 1 hour | Reporting and analytics |
| Low | 24 hours | 24 hours | Historical data, non-critical dashboards |

## Disruption Scenarios

| Scenario | Impact | Response |
|----------|--------|----------|
| Message bus failure | Pipeline halted | Failover to secondary broker |
| AI service unavailable | No AI enrichment | Rule-based fallback correlation |
| Database corruption | Data loss risk | Restore from hourly snapshot |
| Cloud provider outage | Platform unavailable | Multi-region failover |
| Insider threat (admin) | Unauthorized access | Emergency RBAC lockdown |

## Continuity Strategies

1. **Redundancy**: Active-passive message bus, stateless services for horizontal scaling
2. **Fallback**: AI agents degrade gracefully to deterministic rules
3. **Backup**: Hourly incremental, daily full backup with 30-day retention
4. **Failover**: Automated health checks trigger failover within 30 seconds
5. **Communication**: Status page + Slack/#incident-response for internal alerts

## Testing Schedule

- **Quarterly**: Tabletop exercises for each scenario
- **Bi-annual**: Full failover test in non-production environment
- **Annual**: Business impact analysis review and BCP update
