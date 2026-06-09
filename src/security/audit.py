from datetime import datetime, timezone

from src.config import settings
from src.logging_config import get_logger
from src.models import AuditEntry

logger = get_logger(__name__)


class AuditLogger:
    def __init__(self) -> None:
        self._enabled = settings.audit_log_enabled
        self._path = settings.audit_log_path

    def log(
        self,
        actor: str,
        action: str,
        resource: str,
        resource_id: str,
        outcome: str,
        details: str | None = None,
    ) -> None:
        if not self._enabled:
            return
        entry = AuditEntry(
            timestamp=datetime.now(timezone.utc),
            actor=actor,
            action=action,
            resource=resource,
            resource_id=resource_id,
            outcome=outcome,
            details=details,
        )
        self._write(entry)

    def _write(self, entry: AuditEntry) -> None:
        logger.info(
            "audit",
            actor=entry.actor,
            action=entry.action,
            resource=entry.resource,
            resource_id=entry.resource_id,
            outcome=entry.outcome,
        )


audit_logger = AuditLogger()
