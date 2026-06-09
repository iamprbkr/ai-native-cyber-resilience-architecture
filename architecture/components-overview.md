# Components Overview

This document describes each logical component of the architecture, its purpose, inputs, outputs, and key interfaces.

---

## 1. Ingestion Service

| Field      | Description |
|------------|-------------|
| **Purpose** | Receive raw alerts and logs from external sources, validate and normalize them into a common schema. |
| **Inputs**  | HTTP/gRPC API calls, message queue events, file drops. Raw payloads vary by source (JSON, Syslog, CEF). |
| **Outputs** | Normalized `Alert` objects published to the internal message bus. |
| **Interface** | REST API (`POST /ingest`) or message queue consumer. |
| **Notes**    | Schema validation and field mapping are configured via a source-specific mapping table. |

---

## 2. Threat Intelligence Enrichment Service

| Field      | Description |
|------------|-------------|
| **Purpose** | Enrich normalized alerts with external and internal threat context. |
| **Inputs**  | Normalized `Alert` from the message bus. |
| **Outputs** | Enriched `Alert` with additional `threat_context` fields: reputation scores, MITRE mapping, campaign tags. |
| **Interface** | Message bus consumer → producer. Calls out to OSINT APIs, local threat intel DB, and the MITRE mapping config. |
| **Notes**    | Caches lookups to reduce external API calls. Configurable timeout to avoid blocking the pipeline. |

---

## 3. Risk Scoring Engine

| Field      | Description |
|------------|-------------|
| **Purpose** | Compute a composite risk score (0–100) for each alert based on severity, asset criticality, and threat context. |
| **Inputs**  | Enriched `Alert` from the message bus; `risk-scoring-policy.yaml` config. |
| **Outputs** | Scored `Alert` with a `risk_score` field and a `priority` bucket (low / medium / high / critical). |
| **Interface** | Message bus consumer → producer. Stateless; config is reloaded at startup or via a `/reload` signal. |
| **Notes**    | The scoring formula is defined in the config file and can be adjusted without code changes. |

---

## 4. AI Triage Agent

| Field      | Description |
|------------|-------------|
| **Purpose** | Classify alerts as noise, suspicious, or malicious to reduce analyst fatigue. |
| **Inputs**  | Scored `Alert` from the message bus. |
| **Outputs** | Alert tagged with a `classification` label and confidence score. |
| **Interface** | Message bus consumer → producer. Uses a lightweight ML model (e.g., scikit-learn / ONNX) served via a sidecar or embedded inference. |
| **Notes**    | Periodic retraining on labeled data. Human feedback loop: analysts can correct classifications. |

---

## 5. AI Correlation Agent

| Field      | Description |
|------------|-------------|
| **Purpose** | Group related alerts into a single incident based on time windows, common assets, and causal relationships. |
| **Inputs**  | Classified alerts from the message bus. |
| **Outputs** | `Incident` objects containing one or more alerts, a severity, and a timeline. |
| **Interface** | Message bus consumer → producer. Uses an LLM to analyze narrative descriptions for semantic similarity. |
| **Notes**    | Falls back to deterministic rules (same asset + 10 min window) when LLM is unavailable. |

---

## 6. AI Summarization & Decision Support Agent

| Field      | Description |
|------------|-------------|
| **Purpose** | Generate a human-readable incident summary and recommend the appropriate response playbook. |
| **Inputs**  | `Incident` from the correlation agent; playbook registry (YAML playbook index). |
| **Outputs** | `IncidentSummary` (plain text) and `PlaybookRecommendation` (playbook ID and confidence). |
| **Interface** | Message bus consumer → producer. LLM inference (OpenAI API, local model, or alternative). |
| **Notes**    | Prompts include the incident data and available playbook names/descriptions. Output is reviewed by a human before execution for high-severity incidents. |

---

## 7. Playbook Engine / Orchestration

| Field      | Description |
|------------|-------------|
| **Purpose** | Execute response playbooks by dispatching actions to external systems. |
| **Inputs**  | `PlaybookRecommendation` and approved `Incident` from the decision agent. |
| **Outputs** | Execution log, status updates, and closure reports. |
| **Interface** | Message bus consumer; calls external APIs (SOAR, EDR, firewall, cloud provider, ticketing) via pluggable connectors. |
| **Notes**    | Maintains execution state per incident. Supports pause/approve/resume for human-in-the-loop. |

---

## 8. Metrics & Reporting Service

| Field      | Description |
|------------|-------------|
| **Purpose** | Aggregate pipeline data into resilience KPIs and compliance mappings. |
| **Inputs**  | All alert, incident, and playbook execution events (via a separate metrics stream). |
| **Outputs** | KPI values (MTTR, FP rate, coverage %), compliance dashboards, weekly reports. |
| **Interface** | Message bus consumer; writes to a time-series DB and/or dashboard backend. |
| **Notes**    | Reports can be generated in PDF or Markdown for distribution. |
