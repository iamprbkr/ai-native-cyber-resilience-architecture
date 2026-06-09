from datetime import datetime, timedelta

from src.models import ScoredAlert


class CorrelationRule:
    def __init__(self, name: str, window_minutes: int = 10) -> None:
        self.name = name
        self.window = timedelta(minutes=window_minutes)

    def matches(self, alert: ScoredAlert, other: ScoredAlert) -> bool:
        raise NotImplementedError


class SameAssetRule(CorrelationRule):
    def matches(self, alert: ScoredAlert, other: ScoredAlert) -> bool:
        return (
            alert.asset_id == other.asset_id
            and abs((alert.timestamp - other.timestamp).total_seconds()) <= self.window.total_seconds()
        )


class SameSourceRule(CorrelationRule):
    def matches(self, alert: ScoredAlert, other: ScoredAlert) -> bool:
        return (
            alert.source == other.source
            and abs((alert.timestamp - other.timestamp).total_seconds()) <= self.window.total_seconds()
        )


class SameIOCDomainRule(CorrelationRule):
    def matches(self, alert: ScoredAlert, other: ScoredAlert) -> bool:
        if not alert.ioc or not other.ioc:
            return False
        return bool(
            alert.ioc.domain
            and other.ioc.domain
            and alert.ioc.domain == other.ioc.domain
        )


class ChainedAttackRule(CorrelationRule):
    SEQUENCES: list[list[str]] = [
        ["phishing_email", "powershell_execution", "privilege_escalation", "ransomware_encryption"],
        ["credential_dumping", "suspicious_rdp", "data_exfiltration"],
    ]

    def __init__(self, name: str = "chained_attack", window_minutes: int = 30) -> None:
        super().__init__(name, window_minutes)

    def matches(self, alert: ScoredAlert, other: ScoredAlert) -> bool:
        for seq in self.SEQUENCES:
            if (
                alert.event_type in seq
                and other.event_type in seq
                and seq.index(alert.event_type) < seq.index(other.event_type)
                and abs((alert.timestamp - other.timestamp).total_seconds()) <= self.window.total_seconds()
            ):
                return True
        return False
