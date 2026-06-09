# Getting Started

## Prerequisites

- Python 3.11+
- Make (optional, for convenience targets)

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/iamprbkr/ai-native-cyber-resilience-architecture.git
cd ai-native-cyber-resilience-architecture

# 2. Install production dependencies
pip install -e .

# 3. Install development dependencies
pip install -e ".[dev,test,ai]"

# 4. Install pre-commit hooks
pre-commit install
```

## Quick Start

```bash
# Run the full pipeline with sample data
python -c "
from src.ingestion.service import IngestionService
from src.enrichment.service import EnrichmentService
from src.scoring.engine import RiskScoringEngine
from src.response.engine import ResponseEngine

service = IngestionService()
alerts = service.load_from_json('examples/sample-alerts.json')

enrichment = EnrichmentService()
scoring = RiskScoringEngine()
response = ResponseEngine()

for alert in alerts:
    enriched = enrichment.enrich(alert)
    scored = scoring.score(enriched)
    result = response.handle_alert(scored)
    print(f'{scored.id}: score={scored.risk_score}, priority={scored.priority}, action={result[\"status\"]}')
"
```

## Run Tests

```bash
make test
# or
pytest --cov=src -v
```

## Project Tour

| Path | Purpose |
|------|---------|
| `src/` | Python package with all platform modules |
| `architecture/` | C4 diagrams, threat model, framework mappings |
| `grc/` | Governance, risk, and compliance artifacts |
| `config/` | YAML configuration files |
| `playbooks/` | Incident response playbooks |
| `tests/` | Unit, integration, and security tests |
| `docker/` | Container definitions |
| `examples/` | Sample data and reports |
