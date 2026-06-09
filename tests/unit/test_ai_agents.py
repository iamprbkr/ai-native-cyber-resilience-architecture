from src.ai.triage_agent import TriageAgent
from src.ai.correlation_agent import CorrelationAgent
from src.ai.summarization_agent import SummarizationAgent
from src.ai.decision_agent import DecisionAgent
from src.models import Incident, ScoredAlert, Severity, AssetCriticality, EventType, Priority


class TestTriageAgent:
    def test_malicious_classification(self, sample_enriched_alert) -> None:
        agent = TriageAgent()
        result = agent.analyze(sample_enriched_alert)
        assert result["classification"] in ("noise", "suspicious", "malicious")
        assert 0 <= result["confidence"] <= 1

    def test_noise_classification(self) -> None:
        from src.models import EnrichedAlert, Alert, Severity, AssetCriticality, EventType
        alert = EnrichedAlert(
            id="test-noise",
            source="test",
            timestamp="2026-01-01T00:00:00Z",
            severity=Severity.INFO,
            asset_id="test",
            asset_criticality=AssetCriticality.LOW,
            event_type=EventType.UNKNOWN,
            description="Test noise alert",
            threat_context={},
        )
        agent = TriageAgent()
        result = agent.analyze(alert)
        assert result["classification"] == "noise"


class TestCorrelationAgent:
    def test_campaign_assessment(self, sample_scored_alert: ScoredAlert) -> None:
        incident = Incident(
            id="INC-test",
            alerts=[sample_scored_alert],
            severity=Severity.CRITICAL,
            priority=Priority.CRITICAL,
            timeline=[sample_scored_alert.timestamp],
        )
        agent = CorrelationAgent()
        result = agent.analyze(incident)
        assert "likely_campaign" in result
        assert "event_sequence" in result


class TestSummarizationAgent:
    def test_summary_generation(self, sample_scored_alert: ScoredAlert) -> None:
        incident = Incident(
            id="INC-test-002",
            alerts=[sample_scored_alert],
            severity=Severity.CRITICAL,
            priority=Priority.CRITICAL,
            timeline=[sample_scored_alert.timestamp],
        )
        agent = SummarizationAgent()
        result = agent.analyze(incident)
        assert "summary" in result
        assert result["incident_id"] == "INC-test-002"
        assert result["alert_count"] == 1


class TestDecisionAgent:
    def test_ransomware_playbook_recommendation(self, sample_scored_alert: ScoredAlert) -> None:
        incident = Incident(
            id="INC-test-003",
            alerts=[sample_scored_alert],
            severity=Severity.CRITICAL,
            priority=Priority.CRITICAL,
            timeline=[sample_scored_alert.timestamp],
        )
        agent = DecisionAgent()
        result = agent.analyze(incident)
        assert result["recommended_playbook"] == "ir-002"
        assert result["requires_human_approval"] is True

    def test_low_priority_auto_execute(self) -> None:
        from src.models import ScoredAlert, Severity, AssetCriticality, EventType, Priority
        alert = ScoredAlert(
            id="test-low",
            source="test",
            timestamp="2026-01-01T00:00:00Z",
            severity=Severity.INFO,
            asset_id="test",
            asset_criticality=AssetCriticality.LOW,
            event_type=EventType.UNKNOWN,
            description="Low priority",
            risk_score=10,
            priority=Priority.LOW,
        )
        incident = Incident(
            id="INC-low",
            alerts=[alert],
            severity=Severity.INFO,
            priority=Priority.LOW,
            timeline=[alert.timestamp],
        )
        agent = DecisionAgent()
        result = agent.analyze(incident)
        assert result["auto_execute"] is True
