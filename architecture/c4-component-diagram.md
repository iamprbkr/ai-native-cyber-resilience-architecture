# C4 Component Diagram — Level 3 (Scoring Service)

```mermaid
C4Component
  title Component Diagram - Risk Scoring Service

  Container_Boundary(scoring_service, "Scoring Service") {
    Component(engine, "Scoring Engine", "Python", "Computes risk scores from severity, criticality, threat context")
    Component(policy, "Policy Loader", "Python/Pydantic", "Loads and validates risk-scoring-policy.yaml")
    Component(cache, "Score Cache", "In-memory dict", "Caches recently computed scores for duplicate suppression")

    ComponentDb(policy_file, "Policy File", "YAML", "risk-scoring-policy.yaml on disk")
  }

  System_Queue(msg_bus, "Message Bus")
  System_Queue(metrics, "Metrics Collector")

  Rel(msg_bus, engine, "Consume", "EnrichedAlert")
  Rel(engine, policy, "Reads", "Policy config")
  Rel(policy, policy_file, "Loads", "YAML")
  Rel(engine, cache, "Reads/Writes", "Score data")
  Rel(engine, msg_bus, "Publishes", "ScoredAlert")
  Rel(engine, metrics, "Records", "Latency, count")
```

## Component Descriptions

| Component | Responsibility |
|-----------|----------------|
| **Scoring Engine** | Implements `compute_score()` and `assign_priority()` using policy configuration |
| **Policy Loader** | Reads `risk-scoring-policy.yaml`, validates structure, provides typed access to severity/criticality/threshold maps |
| **Score Cache** | Suppresses duplicate scores for identical alert signatures within a configurable TTL window |
