# Data Flow Diagram

```mermaid
flowchart LR
    subgraph Sources[Data Sources]
        A1[SIEM]
        A2[EDR]
        A3[Email Gateway]
        A4[Cloud Logs]
    end

    subgraph Ingestion[Ingestion Layer]
        B1[Ingestion API]
        B2[Validator]
        B3[Normalizer]
    end

    subgraph Bus[Message Bus]
        M1[(Topic: raw-alerts)]
        M2[(Topic: enriched-alerts)]
        M3[(Topic: scored-alerts)]
        M4[(Topic: incidents)]
        M5[(Topic: decisions)]
    end

    subgraph Processing[Processing Layer]
        C1[CTI Enrichment]
        C2[MITRE Mapper]
        C3[Risk Scoring]
        C4[Correlation Engine]
        C5[AI Agents]
    end

    subgraph Response[Response Layer]
        D1[Playbook Executor]
        D2[SOAR Connector]
        D3[Firewall Connector]
    end

    subgraph Reporting[Reporting Layer]
        E1[Metrics Service]
        E2[Report Generator]
        E3[(Metrics DB)]
    end

    A1 & A2 & A3 & A4 --> B1
    B1 --> B2 --> B3 --> M1
    M1 --> C1 --> C2 --> M2
    M2 --> C3 --> M3
    M3 --> C4 --> M4
    M4 --> C5 --> M5
    M5 --> D1 --> D2 & D3
    M1 & M2 & M3 & M4 & M5 -.-> E1
    E1 --> E3
    E1 --> E2
```

## Data Classification by Stage

| Stage | Classification | Retention | Encryption |
|-------|---------------|-----------|------------|
| Raw alert (source) | Internal | 90 days | TLS in transit |
| Normalized alert | Internal | 90 days | At rest encrypted |
| Enriched alert | Confidential | 90 days | At rest encrypted |
| Scored alert | Confidential | 90 days | At rest encrypted |
| Incident | Confidential | 1 year | At rest encrypted |
| Decision/Action | Confidential | 2 years | At rest encrypted |
| Metrics/Reports | Internal | 2 years | At rest encrypted |
