import pytest
from pydantic import ValidationError

from src.models import Alert, Severity, AssetCriticality, EventType, IOC


class TestAlertModel:
    def test_valid_alert_creation(self, sample_alert: Alert) -> None:
        assert sample_alert.id == "test-alert-001"
        assert sample_alert.severity == Severity.CRITICAL
        assert sample_alert.source == "edr"

    def test_alert_empty_id_raises_error(self) -> None:
        with pytest.raises(ValidationError):
            Alert(
                id="",
                source="test",
                timestamp="2026-01-01T00:00:00Z",
                severity=Severity.INFO,
                asset_id="test",
                asset_criticality=AssetCriticality.LOW,
                event_type=EventType.UNKNOWN,
                description="",
            )

    def test_alert_source_normalization(self) -> None:
        alert = Alert(
            id="test-002",
            source="  EDR_SOURCE  ",
            timestamp="2026-01-01T00:00:00Z",
            severity=Severity.INFO,
            asset_id="test",
            asset_criticality=AssetCriticality.LOW,
            event_type=EventType.UNKNOWN,
            description="test",
        )
        assert alert.source == "edr_source"

    def test_ioc_validation(self) -> None:
        ioc = IOC(ip="10.0.0.1", domain=None, hash=None)
        assert ioc.ip == "10.0.0.1"
        assert ioc.domain is None

    def test_ioc_invalid_ip_raises_error(self) -> None:
        with pytest.raises(ValidationError):
            IOC(ip="0.0.0.0")


class TestEnrichedAlert:
    def test_enriched_alert_creation(self, sample_enriched_alert) -> None:
        assert sample_enriched_alert.reputation_score == 0.9
        assert len(sample_enriched_alert.mitre_attack) == 1
        assert sample_enriched_alert.threat_context["source"] == "test"


class TestScoredAlert:
    def test_scored_alert_creation(self, sample_scored_alert) -> None:
        assert sample_scored_alert.risk_score == 95
        assert sample_scored_alert.priority == "critical"

    def test_score_range(self) -> None:
        with pytest.raises(ValidationError):
            ScoredAlert(
                id="test",
                source="test",
                timestamp="2026-01-01T00:00:00Z",
                severity=Severity.INFO,
                asset_id="test",
                asset_criticality=AssetCriticality.LOW,
                event_type=EventType.UNKNOWN,
                description="",
                risk_score=150,
                priority=Priority.CRITICAL,
            )
