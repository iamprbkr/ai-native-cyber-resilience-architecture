from src.correlation.engine import CorrelationEngine
from src.correlation.rules import SameAssetRule, ChainedAttackRule
from src.models import ScoredAlert, Severity, AssetCriticality, EventType, Priority


class TestCorrelationRules:
    def test_same_asset_match(self, sample_scored_alert: ScoredAlert) -> None:
        rule = SameAssetRule("test", 10)
        other = ScoredAlert(
            id="test-002",
            source="edr",
            timestamp="2026-06-09T08:25:00Z",
            severity=Severity.HIGH,
            asset_id="srv-web-app-01",
            asset_criticality=AssetCriticality.HIGH,
            event_type=EventType.PRIVILEGE_ESCALATION,
            description="Second alert on same asset",
            risk_score=80,
            priority=Priority.HIGH,
        )
        assert rule.matches(sample_scored_alert, other)

    def test_same_asset_no_match_different_asset(self, sample_scored_alert: ScoredAlert) -> None:
        rule = SameAssetRule("test", 10)
        other = ScoredAlert(
            id="test-003",
            source="edr",
            timestamp="2026-06-09T08:25:00Z",
            severity=Severity.HIGH,
            asset_id="different-asset",
            asset_criticality=AssetCriticality.HIGH,
            event_type=EventType.PRIVILEGE_ESCALATION,
            description="Different asset",
            risk_score=80,
            priority=Priority.HIGH,
        )
        assert not rule.matches(sample_scored_alert, other)


class TestCorrelationEngine:
    def test_new_incident_creation(self, sample_scored_alert: ScoredAlert) -> None:
        engine = CorrelationEngine()
        incident = engine.correlate(sample_scored_alert)
        assert incident is not None
        assert len(incident.alerts) == 1

    def test_alert_added_to_existing_group(self, sample_scored_alert: ScoredAlert) -> None:
        engine = CorrelationEngine()
        engine.correlate(sample_scored_alert)
        other = ScoredAlert(
            id="test-004",
            source="edr",
            timestamp="2026-06-09T08:25:00Z",
            severity=Severity.HIGH,
            asset_id="srv-web-app-01",
            asset_criticality=AssetCriticality.HIGH,
            event_type=EventType.PRIVILEGE_ESCALATION,
            description="Second alert, same asset",
            risk_score=80,
            priority=Priority.HIGH,
        )
        result = engine.correlate(other)
        assert result is None  # No new incident, added to group
