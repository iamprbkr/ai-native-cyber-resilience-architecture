from typing import Any

from src.ai.base import BaseAIAgent
from src.logging_config import get_logger
from src.models import Incident, ScoredAlert

logger = get_logger(__name__)


class CorrelationAgent(BaseAIAgent):
    def analyze(self, incident: Incident) -> dict[str, Any]:
        self._log_invocation("correlation", len(incident.alerts))

        event_types = [a.event_type for a in incident.alerts]
        asset_ids = list({a.asset_id for a in incident.alerts})

        result = {
            "event_sequence": event_types,
            "unique_assets": asset_ids,
            "likely_campaign": self._assess_campaign(event_types),
        }
        logger.info("correlation_complete", incident_id=incident.id, **result)
        return result

    def _assess_campaign(self, event_types: list[str]) -> str:
        kill_chain = ["phishing_email", "powershell_execution", "privilege_escalation",
                       "credential_dumping", "suspicious_rdp", "ransomware_encryption"]
        matched = sum(1 for e in event_types if e in kill_chain)
        if matched >= 4:
            return "advanced_persistent_threat"
        if matched >= 2:
            return "targeted_attack"
        return "isolated_event"
