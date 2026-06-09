from datetime import datetime, timezone
from typing import Any

from src.correlation.rules import (
    ChainedAttackRule,
    CorrelationRule,
    SameAssetRule,
    SameIOCDomainRule,
    SameSourceRule,
)
from src.exceptions import CorrelationError
from src.logging_config import get_logger
from src.models import Incident, ScoredAlert, Priority
from src.telemetry import metrics, track_latency

logger = get_logger(__name__)


class CorrelationEngine:
    def __init__(self) -> None:
        self._rules: list[CorrelationRule] = [
            SameAssetRule("same_asset", window_minutes=10),
            SameSourceRule("same_source", window_minutes=5),
            SameIOCDomainRule("same_ioc_domain", window_minutes=60),
            ChainedAttackRule("chained_attack", window_minutes=30),
        ]
        self._open_groups: list[list[ScoredAlert]] = []

    def _find_group(self, alert: ScoredAlert) -> int | None:
        for idx, group in enumerate(self._open_groups):
            for member in group:
                for rule in self._rules:
                    if rule.matches(alert, member):
                        return idx
        return None

    @track_latency("correlation.process")
    def correlate(self, alert: ScoredAlert) -> Incident | None:
        try:
            group_idx = self._find_group(alert)
            if group_idx is not None:
                self._open_groups[group_idx].append(alert)
                return None

            self._open_groups.append([alert])
            incident = self._create_incident([alert])
            metrics.increment("correlation.incident_created")
            return incident
        except Exception as exc:
            metrics.increment("correlation.failed")
            raise CorrelationError(f"Correlation failed: {exc}") from exc

    def _create_incident(self, alerts: list[ScoredAlert]) -> Incident:
        severities = [a.severity for a in alerts]
        priorities = [a.priority for a in alerts]
        return Incident(
            id=f"INC-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
            alerts=alerts,
            severity=max(severities, key=lambda s: ["info", "low", "medium", "high", "critical"].index(s)),
            priority=max(priorities, key=lambda p: ["low", "medium", "high", "critical"].index(p)),
            timeline=[a.timestamp for a in alerts],
        )
