from src.reporting.metrics import MetricsCalculator
from src.reporting.resilience_score import ResilienceScoreCalculator
from src.reporting.report_generator import ReportGenerator
from src.models import Alert, Severity, AssetCriticality, EventType


class TestMetricsCalculator:
    def test_empty_metrics(self) -> None:
        calc = MetricsCalculator()
        metrics = calc.calculate()
        assert metrics.total_alerts == 0
        assert metrics.resilience_score >= 60

    def test_metrics_with_alerts(self, sample_alert: Alert) -> None:
        calc = MetricsCalculator()
        calc.record_alert(sample_alert)
        calc.record_response(15.0)
        metrics = calc.calculate()
        assert metrics.total_alerts == 1
        assert metrics.critical_alerts == 1


class TestResilienceScore:
    def test_perfect_score(self) -> None:
        calc = ResilienceScoreCalculator()
        result = calc.calculate(
            detection_score=100,
            response_score=100,
            recovery_score=100,
            coverage_score=100,
            compliance_score=100,
        )
        assert result["overall"] == 100

    def test_zero_score(self) -> None:
        calc = ResilienceScoreCalculator()
        result = calc.calculate(
            detection_score=0,
            response_score=0,
            recovery_score=0,
            coverage_score=0,
            compliance_score=0,
        )
        assert result["overall"] == 0


class TestReportGenerator:
    def test_generate_markdown(self) -> None:
        gen = ReportGenerator()
        report = gen.generate_markdown_report()
        assert "# Weekly Resilience Report" in report
        assert "Resilience Score" in report
