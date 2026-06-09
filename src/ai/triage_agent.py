from typing import Any

from src.ai.base import BaseAIAgent
from src.logging_config import get_logger
from src.models import EnrichedAlert, ScoredAlert

logger = get_logger(__name__)


class TriageAgent(BaseAIAgent):
    CLASSIFICATION_LABELS = ["noise", "suspicious", "malicious"]

    def analyze(self, alert: EnrichedAlert) -> dict[str, Any]:
        self._log_invocation("triage", len(str(alert.model_dump())))

        score_weight = alert.reputation_score or 0.5
        if score_weight >= 0.7:
            label = "malicious"
            confidence = min(score_weight + 0.1, 1.0)
        elif score_weight >= 0.4:
            label = "suspicious"
            confidence = score_weight
        else:
            label = "noise"
            confidence = 1.0 - score_weight

        result = {"classification": label, "confidence": round(confidence, 2)}
        logger.info("triage_complete", alert_id=alert.id, **result)
        return result
