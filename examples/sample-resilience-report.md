# Weekly Resilience Report

**Period**: 2026-06-02 to 2026-06-08  
**Generated**: 2026-06-09

---

## Summary

| Metric | Value | Trend |
|--------|-------|-------|
| Total Alerts | 1,247 | ↑ 8% |
| Critical Alerts | 12 | ↓ 20% |
| Mean Time to Triage | 4.2 min | ↓ 12% |
| Mean Time to Contain (MTC) | 18 min | ↓ 35% |
| Mean Time to Recover (MTTR) | 2.3 hrs | ↓ 15% |
| False Positive Rate | 14% | ↑ 2% |
| Alert Coverage | 87% | → |
| Resilience Score | 73/100 | ↑ 4 pts |

---

## Critical Incidents

| ID | Event Type | Asset | Score | Status | Time to Contain |
|----|------------|-------|-------|--------|-----------------|
| INC-042 | Ransomware encryption | srv-web-app-01 | 95 | Contained | 11 min |
| INC-043 | Privilege escalation | srv-db-01 | 82 | Eradication | 16 min |
| INC-044 | Credential dumping | user-madmin | 78 | Recovery | 23 min |

---

## Top 5 Alert Sources

1. EDR — 412 alerts (33%)
2. SIEM — 289 alerts (23%)
3. Email Gateway — 198 alerts (16%)
4. Cloud Security Posture — 176 alerts (14%)
5. Identity Provider — 172 alerts (14%)

---

## Playbook Execution

| Playbook | Executions | Auto-resolved | Escalated |
|----------|------------|---------------|-----------|
| Generic IR | 34 | 22 | 12 |
| Ransomware Response | 1 | 0 | 1 |
| Phishing Triage | 18 | 16 | 2 |

---

## Recommendations

1. Investigate false positive increase (14% → target is <10%)
2. Schedule tabletop exercise for ransomware scenario within 30 days
3. Review EDR coverage for finance subnet (gaps detected)
4. Update phishing playbook to include new credential-harvesting patterns
