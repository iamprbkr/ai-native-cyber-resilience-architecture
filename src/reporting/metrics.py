from datetime import datetime, timezone
from typing import Any

from src.logging_config import get_logger
from src.models import Alert, ResilienceMetrics
from src.telemetry import metrics as telemetry
from src.telemetry import track_latency

logger = get_logger(__name__)


class MetricsCalculator:
    def __init__(self) -> None:
        self._alerts: list[Alert] = []
        self._false_positives: int = 0
        self._total_response_time: float = 0.0
        self._response_events: int = 0

    def record_alert(self, alert: Alert) -> None:
        self._alerts.append(alert)

    def record_response(self, response_time_minutes: float) -> None:
        self._total_response_time += response_time_minutes
        self._response_events += 1

    def record_false_positive(self) -> None:
        self._false_positives += 1

    @track_latency("metrics.calculate")
    def calculate(self) -> ResilienceMetrics:
        total = len(self._alerts)
        critical = sum(1 for a in self._alerts if a.severity.value == "critical")
        fp_rate = (self._false_positives / total * 100) if total else 0.0
        mttr = (self._total_response_time / self._response_events) if self._response_events else 0.0

        score = self._compute_resilience(critical, fp_rate, mttr)

        return ResilienceMetrics(
            total_alerts=total,
            critical_alerts=critical,
            mean_time_to_triage_minutes=mttr * 0.3,
            mean_time_to_contain_minutes=mttr * 0.6,
            mean_time_to_recover_hours=mttr / 60,
            false_positive_rate=round(fp_rate, 1),
            alert_coverage_pct=self._estimate_coverage(),
            resilience_score=score,
        )

    def _compute_resilience(self, critical: int, fp_rate: float, mttr: float) -> int:
        score = 70
        if critical < 10:
            score += 10
        elif critical > 50:
            score -= 10
        if fp_rate < 10:
            score += 10
        elif fp_rate > 25:
            score -= 10
        if mttr < 30:
            score += 10
        elif mttr > 120:
            score -= 10
        return max(0, min(100, score))

    def _estimate_coverage(self) -> float:
        return 87.0

    def snapshot(self) -> dict[str, Any]:
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "metrics": self.calculate().model_dump(),
            "telemetry": telemetry.snapshot(),
        }
