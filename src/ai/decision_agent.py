from typing import Any

from src.ai.base import BaseAIAgent
from src.logging_config import get_logger
from src.models import Incident, Priority

logger = get_logger(__name__)


class DecisionAgent(BaseAIAgent):
    PLAYBOOK_RECOMMENDATIONS = {
        "ransomware_encryption": "ir-002",
        "phishing_email": "ir-003",
        "ddos_attack": "ir-004",
        "insider_threat": "ir-005",
        "supply_chain": "ir-006",
        "data_exfiltration": "ir-007",
        "data_breach": "ir-008",
    }

    def analyze(self, incident: Incident) -> dict[str, Any]:
        self._log_invocation("decision", len(str(incident.model_dump())))

        event_types = {a.event_type for a in incident.alerts}
        recommended = None
        for et in event_types:
            if et in self.PLAYBOOK_RECOMMENDATIONS:
                recommended = self.PLAYBOOK_RECOMMENDATIONS[et]
                break

        if not recommended:
            recommended = "ir-001"

        auto_execute = incident.priority in (Priority.LOW, Priority.MEDIUM)
        requires_human = incident.priority in (Priority.HIGH, Priority.CRITICAL)

        result = {
            "incident_id": incident.id,
            "recommended_playbook": recommended,
            "auto_execute": auto_execute,
            "requires_human_approval": requires_human,
            "confidence": 0.85,
        }
        logger.info("decision_complete", **result)
        return result
