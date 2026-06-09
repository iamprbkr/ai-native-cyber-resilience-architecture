from datetime import datetime, timezone
from typing import Any

from src.logging_config import get_logger
from src.models import ResilienceMetrics
from src.reporting.metrics import MetricsCalculator

logger = get_logger(__name__)


class ReportGenerator:
    def __init__(self) -> None:
        self._metrics = MetricsCalculator()

    def generate_markdown_report(self, metrics: ResilienceMetrics | None = None) -> str:
        if not metrics:
            metrics = self._metrics.calculate()

        report = f"""# Weekly Resilience Report

**Generated**: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}

## Summary

| Metric | Value |
|--------|-------|
| Total Alerts | {metrics.total_alerts} |
| Critical Alerts | {metrics.critical_alerts} |
| Mean Time to Triage | {metrics.mean_time_to_triage_minutes:.1f} min |
| Mean Time to Contain | {metrics.mean_time_to_contain_minutes:.1f} min |
| Mean Time to Recover | {metrics.mean_time_to_recover_hours:.1f} hrs |
| False Positive Rate | {metrics.false_positive_rate:.1f}% |
| Alert Coverage | {metrics.alert_coverage_pct:.1f}% |
| Resilience Score | {metrics.resilience_score}/100 |

## Recommendations

1. Review false positive sources if rate exceeds 10%
2. Verify playbook coverage for all critical event types
3. Schedule tabletop exercises for high-severity scenarios
"""
        return report
