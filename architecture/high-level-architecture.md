# High-Level Architecture

## Overview

The AI-native cyber resilience architecture is designed as a pipeline of loosely coupled layers. Each layer communicates via a message bus (e.g., Kafka, RabbitMQ, or cloud-native equivalent), allowing components to be scaled, replaced, or extended independently.

## Layer 1 — Data Sources & Ingestion

**Purpose**: Collect raw telemetry from across the enterprise and normalize it into a common schema.

- **Sources**: SIEM, EDR, firewalls, cloud logs (AWS CloudTrail, Azure NSG), identity provider logs, email gateways, custom application logs.
- **Ingestion Service**: Receives raw alerts and logs via API or message queue, validates structure, normalizes fields, and publishes normalized events to the processing layer.
- **Schema**: Every event is normalized to include at minimum: `id`, `timestamp`, `source`, `severity`, `event_type`, `asset_id`, and `description`.

## Layer 2 — Processing & Intelligence

**Purpose**: Enrich raw events with context, compute risk scores, and apply AI/ML for triage and correlation.

### Threat Intelligence Enrichment

Consumes normalized events and appends context:
- IP/domain/hash reputation (OSINT feeds)
- MITRE ATT&CK tactic and technique mapping
- Campaign and threat actor association
- Geo-location and ASN data

### Risk Scoring Engine

Computes a composite score per event based on:
- Alert severity (info → critical)
- Asset criticality (low → high)
- Threat context multiplier (none → confirmed IOC)

**AI/ML & LLM Agents** (logical position):
- **Triage Agent**: Classifies events as noise / suspicious / malicious using a lightweight ML model.
- **Correlation Agent**: Groups related events into incidents using temporal and causal rules enhanced by an LLM.
- **Summarization Agent**: Generates a plain-language incident summary for analysts and executives.
- **Decision Support Agent**: Recommends next steps and playbook selection based on incident type and score.

All AI components operate in a human-in-the-loop mode for high-severity events.

## Layer 3 — Response & Orchestration

**Purpose**: Execute automated and semi-automated response actions.

- **Playbook Engine**: Matches incidents to playbooks (YAML-defined), tracks execution state, and escalates on timeout.
- **Orchestration Connectors**: Abstracted adapters for SOAR, firewalls, EDR APIs, cloud provider APIs, and ticketing systems.
- **Automation Gate**: Configurable rule that determines which actions run automatically and which require approval.

## Layer 4 — Reporting & Governance

**Purpose**: Provide visibility into resilience posture and drive continuous improvement.

- **Metrics Service**: Computes KPIs such as MTTR, alert accuracy, false-positive rate, coverage gaps, and mean time to contain.
- **Compliance Dashboards**: Map controls to frameworks (NIST CSF, ISO 27001, MITRE ATT&CK coverage).
- **Resilience Score**: Aggregate metric (0–100) combining detection coverage, response speed, and recovery capability.

## Data Flow Summary

```
Source → [Ingestion API] → normalized event → [Message Bus]
  → [CTI Enrichment] → enriched event → [Message Bus]
  → [Risk Scoring] → scored event → [Message Bus]
  → [Correlation Agent] → incident → [Message Bus]
  → [Decision Support Agent] → recommended playbook → [Message Bus]
  → [Playbook Engine] → orchestration actions → [External APIs]
  → [Metrics Service] → dashboard & reports
```

## Where AI/LLM fits

| Component        | AI Role                                      | Model Type         |
|------------------|----------------------------------------------|--------------------|
| Triage Agent     | Binary classification (noise vs actionable)  | Lightweight ML     |
| Correlation Agent| Causal/temporal linking with NLP             | LLM (prompt-based) |
| Summarization    | Incident summary in plain language            | LLM                |
| Decision Support | Playbook recommendation and next steps       | LLM + rules        |
| Resilience Score | Trend analysis and anomaly detection         | Statistical ML     |
