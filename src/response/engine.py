from src.exceptions import PlaybookExecutionError
from src.logging_config import get_logger
from src.models import Incident, Priority, ScoredAlert
from src.response.playbook_executor import PlaybookExecutor
from src.security.audit import audit_logger
from src.telemetry import metrics, track_latency

logger = get_logger(__name__)


class ResponseEngine:
    EVENT_PLAYBOOK_MAP: dict[str, str] = {
        "ransomware_encryption": "ir-002",
        "phishing_email": "ir-003",
        "data_exfiltration": "ir-007",
        "ddos_attack": "ir-004",
    }

    def __init__(self) -> None:
        self._executor = PlaybookExecutor()

    def recommend_playbook(self, alert: ScoredAlert) -> str:
        return self.EVENT_PLAYBOOK_MAP.get(alert.event_type, "ir-001")

    @track_latency("response.process")
    def handle_alert(self, alert: ScoredAlert) -> dict:
        playbook_id = self.recommend_playbook(alert)
        requires_approval = alert.priority in (Priority.CRITICAL, Priority.HIGH)

        if requires_approval:
            status = "pending_approval"
        else:
            playbook = self._executor.get_playbook(playbook_id)
            status = "automated" if playbook else "no_playbook"

        result = {
            "alert_id": alert.id,
            "playbook_id": playbook_id,
            "status": status,
            "requires_approval": requires_approval,
        }

        if not requires_approval and self._executor.get_playbook(playbook_id):
            execution = self._executor.execute(playbook_id, Incident(
                id=f"INC-{alert.id}",
                alerts=[alert],
                severity=alert.severity,
                priority=alert.priority,
                timeline=[alert.timestamp],
            ))
            result["execution"] = execution

        metrics.increment(f"response.{status}")
        logger.info("alert_handled", **result)
        return result
