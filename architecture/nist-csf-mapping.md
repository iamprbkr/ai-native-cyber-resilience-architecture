# NIST CSF 2.0 Mapping

This document maps platform capabilities to NIST Cybersecurity Framework 2.0 functions, categories, and subcategories.

## Govern (GV)

| Subcategory | Platform Coverage |
|-------------|-------------------|
| GV.OC-1: Organizational context | Repository README, architecture docs |
| GV.RM-1: Risk management policy | `grc/risk-register.yaml`, `grc/policy-framework.md` |
| GV.RM-2: Risk tolerance | Risk scoring thresholds (`config/risk-scoring-policy.yaml`) |
| GV.SC-1: Supply chain risk | Supply chain playbook (`ir-006`), vendor assessment |
| GV.SC-2: Third-party risk | Vendor connector isolation, API key rotation |

## Identify (ID)

| Subcategory | Platform Coverage |
|-------------|-------------------|
| ID.AM-1: Physical devices | Asset tracking via `asset_id` in Alert model |
| ID.AM-2: Software platforms | SBOM generation, dependency tracking |
| ID.AM-5: Resources | Asset criticality classification in scoring policy |
| ID.RA-1: Risk assessment | `grc/risk-register.yaml`, risk scoring engine |
| ID.RA-3: Threat modeling | `architecture/threat-model.md` |

## Protect (PR)

| Subcategory | Platform Coverage |
|-------------|-------------------|
| PR.AC-1: Identity management | RBAC module (`src/security/rbac.py`) |
| PR.AC-5: Network integrity | API gateway, mTLS between services |
| PR.DS-1: Data-at-rest | Encryption via `src/security/secrets.py` |
| PR.DS-2: Data-in-transit | TLS configuration |
| PR.PS-1: Configuration management | IaC ready, policy-as-code |

## Detect (DE)

| Subcategory | Platform Coverage |
|-------------|-------------------|
| DE.CM-1: Continuous monitoring | Alert ingestion, all pipeline stages |
| DE.CM-4: Malicious code detection | AI triage agent, EDR integrations |
| DE.AE-1: Event aggregation | Ingestion normalizer |
| DE.AE-3: Event correlation | Correlation engine, AI correlation agent |

## Respond (RS)

| Subcategory | Platform Coverage |
|-------------|-------------------|
| RS.RP-1: Response plan | Playbook executor, 8 playbooks |
| RS.MA-1: Incident management | End-to-end pipeline: alert → incident → response |
| RS.CO-1: Communication | Reporting, notification services |
| RS.AN-3: Analysis | AI summarization agent, root cause analysis in playbooks |

## Recover (RC)

| Subcategory | Platform Coverage |
|-------------|-------------------|
| RC.RP-1: Recovery plan | BCP/DR docs (`grc/business-continuity.md`) |
| RC.IM-1: Improvements | Post-incident review tasks in all playbooks |
| RC.IM-2: Lessons learned | Automated PIR tracking |
