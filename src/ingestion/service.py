from pathlib import Path
from typing import Any

import yaml

from src.exceptions import IngestionError
from src.ingestion.normalizers import AlertNormalizer
from src.ingestion.validators import AlertValidator
from src.logging_config import get_logger
from src.models import Alert
from src.security.audit import audit_logger
from src.telemetry import metrics, track_latency

logger = get_logger(__name__)


class IngestionService:
    def __init__(self) -> None:
        self._validator = AlertValidator()
        self._normalizer = AlertNormalizer()

    @track_latency("ingestion.process")
    def process_alert(self, raw: dict[str, Any]) -> Alert:
        try:
            normalized = self._normalizer.normalize(raw)
            alert = self._validator.validate_raw(normalized)
            metrics.increment("ingestion.processed")
            logger.info("alert_ingested", alert_id=alert.id, source=alert.source)
            return alert
        except Exception as exc:
            metrics.increment("ingestion.failed")
            audit_logger.log(
                actor="system", action="ingestion.failed",
                resource="alert", resource_id=raw.get("id", "unknown"),
                outcome="failure", details=str(exc),
            )
            raise IngestionError(f"Failed to process alert: {exc}") from exc

    @track_latency("ingestion.batch")
    def process_batch(self, raw_alerts: list[dict[str, Any]]) -> list[Alert]:
        return [self.process_alert(a) for a in raw_alerts]

    def load_from_json(self, filepath: str | Path) -> list[Alert]:
        import json
        with open(filepath) as f:
            data = json.load(f)
        return self.process_batch(data)
