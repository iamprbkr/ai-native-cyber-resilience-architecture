# ISO 27001:2022 Control Mapping

## Annex A Controls

### Organizational Controls (A.5)

| Control | Name | Platform Coverage |
|---------|------|-------------------|
| A.5.1 | Information security policy | `grc/policy-framework.md` |
| A.5.2 | Information security roles | RBAC roles defined in `src/security/rbac.py` |
| A.5.7 | Threat intelligence | CTI enrichment provider (`src/enrichment/cti_provider.py`) |
| A.5.8 | Project management | Architecture decision records |
| A.5.9 | Classification of information | `config/data-classification.yaml` |
| A.5.10 | Information labelling | Severity and criticality labels on all alerts |
| A.5.15 | Access control | RBAC module, least privilege enforcement |
| A.5.16 | Identity management | Role-based identity in authorization service |
| A.5.18 | Access rights review | Audit log of all access decisions |
| A.5.19 | Supplier security | Supply chain playbook (`ir-006`) |
| A.5.22 | Threat intelligence | Integrated OSINT enrichment |
| A.5.23 | Security for cloud services | Cloud security posture alert ingestion |
| A.5.24 | Incident management | Full incident lifecycle: detect → respond → recover |
| A.5.25 | Learning from incidents | PIR tasks in every playbook |
| A.5.26 | Business continuity | `grc/business-continuity.md` |
| A.5.29 | Information security during disruption | DR plan (`grc/disaster-recovery.md`) |
| A.5.36 | Compliance | Automated compliance mapping (`grc/compliance-mapping.md`) |

### Technological Controls (A.8)

| Control | Name | Platform Coverage |
|---------|------|-------------------|
| A.8.8 | Management of technical vulnerabilities | Scoring severity mapping |
| A.8.9 | Configuration management | Policy-as-code via YAML configs |
| A.8.12 | Information deletion | Alert retention policy |
| A.8.13 | Information backup | Backup strategy in DR plan |
| A.8.15 | Logging | Audit logger (`src/security/audit.py`) |
| A.8.16 | Monitoring | Pipeline telemetry, correlation engine |
| A.8.17 | Clock synchronization | Timestamps normalized to UTC |
| A.8.20 | Networks security | Zero Trust micro-segmentation |
| A.8.25 | Secure development | Pre-commit hooks, linting, SAST |
| A.8.26 | Application security | Input sanitization, RBAC, validation |
| A.8.29 | Security testing | `tests/` suite, SAST with bandit |
