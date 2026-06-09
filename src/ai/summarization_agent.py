from typing import Any

from src.ai.base import BaseAIAgent
from src.logging_config import get_logger
from src.models import Incident

logger = get_logger(__name__)


class SummarizationAgent(BaseAIAgent):
    def analyze(self, incident: Incident) -> dict[str, Any]:
        self._log_invocation("summarization", len(str(incident.model_dump())))

        alert_count = len(incident.alerts)
        event_types = ", ".join({a.event_type for a in incident.alerts})
        assets = ", ".join({a.asset_id for a in incident.alerts})

        summary = (
            f"Incident {incident.id} involves {alert_count} alert(s) "
            f"of types [{event_types}] affecting asset(s) [{assets}]. "
            f"Overall severity is {incident.severity.value} with "
            f"{incident.priority.value} priority."
        )

        result = {
            "incident_id": incident.id,
            "summary": summary,
            "alert_count": alert_count,
        }
        logger.info("summarization_complete", incident_id=incident.id)
        return result
