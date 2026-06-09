import pytest

from src.response.engine import ResponseEngine
from src.response.playbook_executor import PlaybookExecutor
from src.models import Priority


@pytest.fixture
def response_engine() -> ResponseEngine:
    return ResponseEngine()


class TestResponseEngine:
    def test_recommend_ransomware_playbook(self, sample_scored_alert, response_engine: ResponseEngine) -> None:
        playbook_id = response_engine.recommend_playbook(sample_scored_alert)
        assert playbook_id == "ir-002"

    def test_recommend_generic_playbook(self, response_engine: ResponseEngine) -> None:
        from src.models import ScoredAlert, Alert, Severity, AssetCriticality, EventType, Priority, EnrichedAlert
        alert = ScoredAlert(
            id="test",
            source="test",
            timestamp="2026-01-01T00:00:00Z",
            severity=Severity.MEDIUM,
            asset_id="test",
            asset_criticality=AssetCriticality.MEDIUM,
            event_type=EventType.UNKNOWN,
            description="Unknown event",
            risk_score=30,
            priority=Priority.MEDIUM,
        )
        playbook_id = response_engine.recommend_playbook(alert)
        assert playbook_id == "ir-001"

    def test_handle_critical_alert(self, sample_scored_alert, response_engine: ResponseEngine) -> None:
        result = response_engine.handle_alert(sample_scored_alert)
        assert result["requires_approval"] is True
        assert result["status"] == "pending_approval"

    def test_handle_low_alert(self, response_engine: ResponseEngine) -> None:
        from src.models import ScoredAlert, Severity, AssetCriticality, EventType, Priority
        alert = ScoredAlert(
            id="test-low",
            source="test",
            timestamp="2026-01-01T00:00:00Z",
            severity=Severity.INFO,
            asset_id="test",
            asset_criticality=AssetCriticality.LOW,
            event_type=EventType.UNKNOWN,
            description="Low",
            risk_score=10,
            priority=Priority.LOW,
        )
        result = response_engine.handle_alert(alert)
        assert result["requires_approval"] is False


class TestPlaybookExecutor:
    def test_load_playbooks(self) -> None:
        executor = PlaybookExecutor()
        assert executor.get_playbook("ir-001") is not None
        assert executor.get_playbook("ir-002") is not None

    def test_unknown_playbook(self) -> None:
        executor = PlaybookExecutor()
        assert executor.get_playbook("ir-999") is None

    def test_execute_playbook(self, sample_scored_alert) -> None:
        from src.models import Incident
        executor = PlaybookExecutor()
        incident = Incident(
            id="INC-test",
            alerts=[sample_scored_alert],
            severity=sample_scored_alert.severity,
            priority=sample_scored_alert.priority,
            timeline=[sample_scored_alert.timestamp],
        )
        result = executor.execute("ir-002", incident)
        assert result["playbook_id"] == "ir-002"
        assert result["incident_id"] == "INC-test"
        assert len(result["automated_actions"]) > 0
