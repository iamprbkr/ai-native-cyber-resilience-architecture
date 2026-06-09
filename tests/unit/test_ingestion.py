import pytest

from src.exceptions import ValidationError
from src.ingestion.service import IngestionService
from src.ingestion.validators import AlertValidator


class TestIngestionService:
    def test_process_alert(self, test_alerts: list[dict]) -> None:
        service = IngestionService()
        alert = service.process_alert(test_alerts[0])
        assert alert.id == "test-alert-001"
        assert alert.source == "edr"
        assert alert.severity.value == "critical"

    def test_process_batch(self, test_alerts: list[dict]) -> None:
        service = IngestionService()
        results = service.process_batch(test_alerts)
        assert len(results) == 3

    def test_invalid_alert_raises_error(self) -> None:
        service = IngestionService()
        with pytest.raises(ValidationError):
            service.process_alert({"bad": "data"})

    def test_empty_batch(self) -> None:
        service = IngestionService()
        results = service.process_batch([])
        assert results == []


class TestAlertValidator:
    def test_valid_input(self) -> None:
        validator = AlertValidator()
        alert = validator.validate_raw({
            "id": "test-001",
            "source": "EDR",
            "timestamp": "2026-01-01T00:00:00Z",
            "severity": "critical",
            "asset_id": "srv-01",
            "asset_criticality": "high",
            "event_type": "ransomware_encryption",
            "description": "Test alert",
        })
        assert alert.id == "test-001"

    def test_missing_fields(self) -> None:
        validator = AlertValidator()
        with pytest.raises(ValidationError):
            validator.validate_raw({"id": "test"})

    def test_xss_sanitization(self) -> None:
        validator = AlertValidator()
        alert = validator.validate_raw({
            "id": "test-002",
            "source": "EDR",
            "timestamp": "2026-01-01T00:00:00Z",
            "severity": "medium",
            "asset_id": "srv-01",
            "asset_criticality": "medium",
            "event_type": "phishing_email",
            "description": "<script>alert('xss')</script>Normal description",
        })
        assert "<script>" not in alert.description
