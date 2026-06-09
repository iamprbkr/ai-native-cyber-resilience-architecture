from pathlib import Path

import pytest

from src.ingestion.service import IngestionService
from src.enrichment.service import EnrichmentService
from src.scoring.engine import RiskScoringEngine
from src.correlation.engine import CorrelationEngine
from src.response.engine import ResponseEngine
from src.models import Alert


class TestFullPipeline:
    @pytest.fixture
    def pipeline_services(self) -> dict:
        policy_path = Path(__file__).resolve().parent.parent.parent / "config" / "risk-scoring-policy.yaml"
        return {
            "ingestion": IngestionService(),
            "enrichment": EnrichmentService(),
            "scoring": RiskScoringEngine(policy_path),
            "correlation": CorrelationEngine(),
            "response": ResponseEngine(),
        }

    def test_alert_through_pipeline(self, test_alerts: list[dict], pipeline_services: dict) -> None:
        alert = pipeline_services["ingestion"].process_alert(test_alerts[0])
        assert isinstance(alert, Alert)

        enriched = pipeline_services["enrichment"].enrich(alert)
        assert enriched.threat_context != {}

        scored = pipeline_services["scoring"].score(enriched)
        assert 0 <= scored.risk_score <= 100
        assert scored.priority is not None

        incident = pipeline_services["correlation"].correlate(scored)
        assert incident is not None
        assert len(incident.alerts) == 1

        result = pipeline_services["response"].handle_alert(scored)
        assert result["alert_id"] == scored.id

    def test_batch_pipeline(self, test_alerts: list[dict], pipeline_services: dict) -> None:
        alerts = pipeline_services["ingestion"].process_batch(test_alerts)
        assert len(alerts) == 3

        for alert in alerts:
            enriched = pipeline_services["enrichment"].enrich(alert)
            scored = pipeline_services["scoring"].score(enriched)
            pipeline_services["response"].handle_alert(scored)
