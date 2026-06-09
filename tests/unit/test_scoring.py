from pathlib import Path

import pytest

from src.scoring.engine import RiskScoringEngine
from src.scoring.policies import RiskScoringPolicy
from src.models import Priority


@pytest.fixture
def scoring_engine() -> RiskScoringEngine:
    policy_path = Path(__file__).resolve().parent.parent.parent / "config" / "risk-scoring-policy.yaml"
    return RiskScoringEngine(policy_path)


class TestRiskScoringPolicy:
    def test_load_policy(self) -> None:
        policy_path = Path(__file__).resolve().parent.parent.parent / "tests" / "fixtures" / "config.yaml"
        policy = RiskScoringPolicy(policy_path)
        assert policy.severity_map["critical"] == 95
        assert policy.criticality_map["high"] == 1.3
        assert policy.thresholds["critical"] == 75

    def test_policy_values(self, scoring_engine: RiskScoringEngine) -> None:
        assert scoring_engine._policy.severity_map["info"] == 10
        assert scoring_engine._policy.criticality_map["low"] == 0.8


class TestRiskScoringEngine:
    def test_score_critical_alert(self, sample_enriched_alert, scoring_engine: RiskScoringEngine) -> None:
        scored = scoring_engine.score(sample_enriched_alert)
        assert scored.risk_score >= 75
        assert scored.priority == Priority.CRITICAL

    def test_score_low_alert(self, scoring_engine: RiskScoringEngine) -> None:
        from src.models import Alert, Severity, AssetCriticality, EventType, EnrichedAlert
        alert = EnrichedAlert(
            id="test-low",
            source="test",
            timestamp="2026-01-01T00:00:00Z",
            severity=Severity.INFO,
            asset_id="test",
            asset_criticality=AssetCriticality.LOW,
            event_type=EventType.UNKNOWN,
            description="Low severity test",
            threat_context={},
        )
        scored = scoring_engine.score(alert)
        assert scored.risk_score < 50
        assert scored.priority in (Priority.LOW, Priority.MEDIUM)

    def test_score_range(self, sample_enriched_alert, scoring_engine: RiskScoringEngine) -> None:
        for _ in range(10):
            scored = scoring_engine.score(sample_enriched_alert)
            assert 0 <= scored.risk_score <= 100
