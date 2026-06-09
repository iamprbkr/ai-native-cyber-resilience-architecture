from pathlib import Path

from src.exceptions import ScoringError
from src.logging_config import get_logger
from src.models import EnrichedAlert, Priority, ScoredAlert
from src.scoring.policies import RiskScoringPolicy
from src.telemetry import metrics, track_latency

logger = get_logger(__name__)


class RiskScoringEngine:
    def __init__(self, policy_path: str | Path | None = None) -> None:
        path = policy_path or Path(__file__).resolve().parent.parent.parent / "config" / "risk-scoring-policy.yaml"
        self._policy = RiskScoringPolicy(path)

    def _compute_threat_multiplier(self, alert: EnrichedAlert) -> float:
        if alert.ioc and any(v for v in alert.ioc.model_dump().values() if v):
            return self._policy.threat_multipliers.get("confirmed_ioc", 2.0)
        threat_level = alert.threat_context.get("score", 0)
        if threat_level >= 0.8:
            return self._policy.threat_multipliers.get("confirmed_ioc", 2.0)
        if threat_level >= 0.5:
            return self._policy.threat_multipliers.get("high_likelihood", 1.8)
        return self._policy.threat_multipliers.get("none", 1.0)

    def _compute_score(self, alert: EnrichedAlert) -> int:
        severity_score = self._policy.severity_map.get(alert.severity, 10)
        criticality_mult = self._policy.criticality_map.get(alert.asset_criticality, 1.0)
        threat_mult = self._compute_threat_multiplier(alert)
        return min(int(severity_score * criticality_mult * threat_mult), 100)

    def _assign_priority(self, score: int) -> Priority:
        th = self._policy.thresholds
        if score >= th["critical"]:
            return Priority.CRITICAL
        if score >= th["high"]:
            return Priority.HIGH
        if score >= th["medium"]:
            return Priority.MEDIUM
        return Priority.LOW

    @track_latency("scoring.process")
    def score(self, alert: EnrichedAlert) -> ScoredAlert:
        try:
            risk_score = self._compute_score(alert)
            priority = self._assign_priority(risk_score)
            metrics.increment(f"scoring.{priority.value}")
            logger.info("alert_scored", alert_id=alert.id, score=risk_score, priority=priority.value)
            return ScoredAlert(
                **alert.model_dump(),
                risk_score=risk_score,
                priority=priority,
            )
        except Exception as exc:
            metrics.increment("scoring.failed")
            raise ScoringError(f"Scoring failed for {alert.id}: {exc}") from exc
