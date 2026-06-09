# Threat Model

## Methodology: STRIDE per Component

### 1. Ingestion API

| Threat | Type | Mitigation |
|--------|------|------------|
| Attacker sends malformed payload to crash service | DoS | Input validation, rate limiting, schema enforcement |
| Attacker injects SQL/NoSQL via alert fields | Tampering | Input sanitization (`src/security/sanitizer.py`) |
| Attacker replays legitimate alerts to cause false incidents | Repudiation | Alert deduplication, audit logging |
| Unauthenticated source sends alerts | Spoofing | API key validation, mTLS |
| Alert data contains sensitive information | Information Disclosure | Field-level sanitization, PII redaction |

### 2. Message Bus

| Threat | Type | Mitigation |
|--------|------|------------|
| Unauthorized consumer reads alert data | Information Disclosure | TLS encryption, ACLs, topic-level auth |
| Message bus flooded with data | DoS | Connection limits, backpressure, queue sizing |
| Message tampering in transit | Tampering | TLS + message signing |

### 3. AI Agent Layer

| Threat | Type | Mitigation |
|--------|------|------------|
| Prompt injection via alert descriptions | Tampering | Input sanitization, output validation, prompt boundaries |
| LLM hallucination causing incorrect decisions | Spoofing | Human-in-the-loop for critical actions, confidence thresholds |
| Model poisoning via training data | Tampering | Input validation, model versioning, rollback capability |
| Sensitive data leaked in LLM prompts | Information Disclosure | PII redaction before LLM call, data minimization |

### 4. Response Engine

| Threat | Type | Mitigation |
|--------|------|------------|
| Unauthorized playbook execution | Tampering | RBAC, approval workflow for high-severity |
| Connector credentials leaked | Information Disclosure | Secrets manager, environment variables, no hardcoded secrets |
| Malicious playbook actions | Tampering | Action whitelist, sandboxed execution, audit trail |

### 5. Reporting

| Threat | Type | Mitigation |
|--------|------|------------|
| Sensitive metrics exposed to unauthorized viewers | Information Disclosure | RBAC, report-level access control |
| Report data tampered | Tampering | Read-only metrics store, append-only logs |

## Attack Tree - Ransomware Scenario

```
Goal: Encrypt critical assets and demand ransom
├── 1. Initial Access
│   ├── 1.1 Phishing email with malicious attachment [T1566]
│   │   └── Mitigation: Email gateway scanning, user training, playbook ir-003
│   └── 1.2 RDP brute-force [T1021]
│       └── Mitigation: Account lockout, MFA, playbook ir-001
├── 2. Execution
│   ├── 2.1 PowerShell download cradle [T1059]
│   │   └── Detection: EDR alert (event_type: powershell_execution)
│   └── 2.2 Scheduled task creation [T1543]
│       └── Detection: EDR alert (event_type: persistence_service)
├── 3. Privilege Escalation
│   └── 3.1 LSASS credential dumping [T1003]
│       └── Detection: SIEM alert (event_type: credential_dumping)
├── 4. Lateral Movement
│   └── 4.1 RDP to file servers [T1021]
│       └── Detection: Network monitor (event_type: suspicious_rdp)
└── 5. Impact
    └── 5.1 Encrypt files [T1486]
        └── Detection: EDR alert (event_type: ransomware_encryption)
        └── Response: Playbook ir-002 (Ransomware Response)
```

## Data Flow Threats (Zero Trust)

| Flow | Trust Level | Control |
|------|-------------|---------|
| Source → Ingestion API | Untrusted → Internal | mTLS, API key, input validation |
| Ingestion API → Message Bus | Internal → Internal | Service mesh mTLS |
| Message Bus → Services | Internal → Internal | Topic-level ACLs |
| AI Service → Message Bus | Internal → Internal | Output validation, audit |
| Response → External APIs | Internal → Untrusted | Credentials via secrets manager, audit logging |
