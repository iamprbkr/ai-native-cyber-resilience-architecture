from datetime import datetime

from src.exceptions import ValidationError
from src.models import Alert, EventType, Severity, AssetCriticality, IOC
from src.security.sanitizer import InputSanitizer


class AlertValidator:
    REQUIRED_FIELDS = {"id", "source", "timestamp", "severity", "asset_id", "event_type", "description"}

    def validate_raw(self, raw: dict) -> Alert:
        missing = self.REQUIRED_FIELDS - set(raw.keys())
        if missing:
            raise ValidationError(f"Missing required fields: {missing}")

        sanitized = InputSanitizer.sanitize_alert_field("root", raw)

        try:
            severity = Severity(sanitized.get("severity", "").lower())
        except ValueError:
            severity = Severity.INFO

        try:
            event_type = EventType(sanitized.get("event_type", "unknown"))
        except ValueError:
            event_type = EventType.UNKNOWN

        try:
            asset_criticality = AssetCriticality(sanitized.get("asset_criticality", "medium").lower())
        except ValueError:
            asset_criticality = AssetCriticality.MEDIUM

        ioc_raw = sanitized.get("ioc")
        ioc = IOC(**ioc_raw) if isinstance(ioc_raw, dict) else None

        return Alert(
            id=sanitized["id"],
            source=InputSanitizer.sanitize_string(sanitized.get("source", "unknown")),
            timestamp=datetime.fromisoformat(sanitized["timestamp"].replace("Z", "+00:00")),
            severity=severity,
            asset_id=InputSanitizer.sanitize_string(sanitized.get("asset_id", "unknown")),
            asset_criticality=asset_criticality,
            event_type=event_type,
            description=InputSanitizer.sanitize_string(sanitized.get("description", "")),
            ioc=ioc,
            raw=raw,
        )
