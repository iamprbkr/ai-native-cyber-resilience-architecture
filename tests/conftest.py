import json
from pathlib import Path

import pytest

from src.models import Alert, EnrichedAlert, ScoredAlert, Severity, AssetCriticality, EventType, Priority
from src.config import Settings


@pytest.fixture
def settings() -> Settings:
    return Settings()


@pytest.fixture
def sample_alert() -> Alert:
    return Alert(
        id="test-alert-001",
        source="edr",
        timestamp="2026-06-09T08:23:00Z",
        severity=Severity.CRITICAL,
        asset_id="srv-web-app-01",
        asset_criticality=AssetCriticality.HIGH,
        event_type=EventType.RANSOMWARE_ENCRYPTION,
        description="Test ransomware alert",
    )


@pytest.fixture
def sample_enriched_alert(sample_alert: Alert) -> EnrichedAlert:
    return EnrichedAlert(
        **sample_alert.model_dump(),
        threat_context={"score": 0.9, "source": "test"},
        mitre_attack=[{"tactic": "Impact", "technique_id": "T1486"}],
        reputation_score=0.9,
    )


@pytest.fixture
def sample_scored_alert(sample_enriched_alert: EnrichedAlert) -> ScoredAlert:
    return ScoredAlert(
        **sample_enriched_alert.model_dump(),
        risk_score=95,
        priority=Priority.CRITICAL,
    )


@pytest.fixture
def test_alerts() -> list[dict]:
    fixtures_path = Path(__file__).parent / "fixtures" / "alerts.json"
    with open(fixtures_path) as f:
        return json.load(f)
