# Metrics & KPIs

## KPI Tree

```
Resilience Score (0–100)
├── Detection (25%)
│   ├── Mean Time to Detect (MTTD) — Target: <5 min
│   ├── Alert Coverage % — Target: >90%
│   └── True Positive Rate — Target: >85%
├── Response (30%)
│   ├── Mean Time to Triage — Target: <5 min
│   ├── Mean Time to Contain — Target: <30 min
│   └── Automated Response Rate — Target: >60%
├── Recovery (20%)
│   ├── Mean Time to Recover (MTTR) — Target: <4 hr
│   ├── Backup Recovery Success — Target: >99%
│   └── RTO Achievement Rate — Target: >95%
├── Coverage (15%)
│   ├── MITRE ATT&CK Coverage — Target: >60%
│   ├── Asset Coverage — Target: >95%
│   └── Source Integration — Target: >80%
└── Compliance (10%)
    ├── Control Automation Rate — Target: >70%
    ├── Audit Finding Closure — Target: <30 days
    └── Policy Compliance — Target: >90%
```

## Measurement Sources

| KPI | Source | Frequency |
|-----|--------|-----------|
| MTTD | Ingestion timestamps → alert creation | Real-time |
| Alert Coverage | Enriched alerts vs total events | Daily |
| True Positive Rate | Analyst feedback loop | Weekly |
| MTTR | Incident open → close timestamps | Real-time |
| Automated Response Rate | Playbook execution logs | Weekly |
| MITRE ATT&CK Coverage | Mapping config vs detected events | Monthly |
| Resilience Score | Composite calculation | Weekly |

## Reporting Cadence

| Report | Audience | Frequency |
|--------|----------|-----------|
| Real-time dashboard | SOC analysts | Continuous |
| Daily summary | SOC lead | Daily |
| Weekly resilience report | CISO | Weekly |
| Monthly GRC report | Board/executives | Monthly |
| Quarterly trend analysis | All stakeholders | Quarterly |
