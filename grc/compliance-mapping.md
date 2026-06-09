# Compliance Mapping

## NIST Cybersecurity Framework (CSF) 2.0

| Function | Category | Control | Implementation |
|----------|----------|---------|----------------|
| **Govern (GV)** | GV.OC - Oversight | Risk management policy | `grc/risk-register.yaml` |
| **Identify (ID)** | ID.AM - Asset Management | Asset inventory and classification | `config/data-classification.yaml` |
| | ID.RA - Risk Assessment | Risk scoring | `src/scoring/engine.py` |
| | ID.RM - Risk Management Strategy | Risk treatment plan | `grc/risk-register.yaml` |
| **Protect (PR)** | PR.AC - Access Control | RBAC and authentication | `src/security/rbac.py` |
| | PR.DS - Data Security | Encryption and data protection | `src/security/secrets.py` |
| | PR.PS - Platform Security | Secure coding and input validation | `src/security/sanitizer.py` |
| **Detect (DE)** | DE.CM - Continuous Monitoring | Alert ingestion and correlation | `src/ingestion/`, `src/correlation/` |
| | DE.AE - Anomaly Detection | AI triage and threat scoring | `src/ai/triage_agent.py`, `src/scoring/` |
| **Respond (RS)** | RS.MA - Incident Management | Playbook execution | `src/response/playbook_executor.py` |
| | RS.CO - Communications | Alerting and reporting | `src/response/engine.py` |
| **Recover (RC)** | RC.RP - Recovery Planning | BCP/DR procedures | `grc/business-continuity.md` |
| | RC.IM - Improvements | Post-incident review | Playbook PIR tasks |

## ISO 27001:2022 Mapping

| ISO Control | Control Name | Implementation |
|-------------|--------------|----------------|
| A.5.1 | Information security policy | `grc/policy-framework.md` |
| A.5.7 | Threat intelligence | `src/enrichment/cti_provider.py` |
| A.5.9 | Classification of information | `config/data-classification.yaml` |
| A.5.15 | Access control | `src/security/rbac.py` |
| A.5.24 | Incident management | `playbooks/` |
| A.5.25 | Learning from incidents | Playbook PIR sections |
| A.5.26 | Business continuity | `grc/business-continuity.md` |
| A.8.8 | Management of technical vulnerabilities | Scoring severity mapping |
| A.8.15 | Logging | `src/security/audit.py` |
| A.8.16 | Monitoring | `src/correlation/`, `src/telemetry.py` |
| A.8.25 | Secure development | `pyproject.toml` tool config |
| A.8.29 | Security testing | `tests/` suite |

## MITRE ATT&CK Coverage

| Tactic | Technique | Detection |
|--------|-----------|-----------|
| Initial Access | T1566 (Phishing) | `alert-002` pattern |
| Execution | T1059 (PowerShell) | `alert-004` pattern |
| Persistence | T1543 (Service Creation) | `alert-008` pattern |
| Privilege Escalation | T1055 (Process Injection) | `alert-003` pattern |
| Credential Access | T1003 (OS Credential Dumping) | `alert-006` pattern |
| Lateral Movement | T1021 (Remote Services) | `alert-007` pattern |
| Exfiltration | T1048 (Alternative Protocol) | `alert-005` pattern |
| Impact | T1486 (Data Encrypted) | `alert-001` pattern |
