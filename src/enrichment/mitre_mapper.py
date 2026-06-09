from src.config import settings
from src.logging_config import get_logger
from src.models import Alert, EnrichedAlert

logger = get_logger(__name__)


class MITREMapper:
    def __init__(self) -> None:
        self._mapping: dict[str, list[dict]] = {}
        self._load_mapping()

    def _load_mapping(self) -> None:
        try:
            config = settings.mitre_attack_mapping
            for entry in config.get("events", []):
                event_type = entry["event_type"]
                self._mapping.setdefault(event_type, []).append({
                    "tactic": entry["tactic"],
                    "technique_id": entry["technique_id"],
                    "technique_name": entry["technique_name"],
                })
        except Exception as exc:
            logger.warning("mitre_mapping_load_failed", error=str(exc))

    def map_alert(self, alert: Alert) -> list[dict[str, str]]:
        return self._mapping.get(alert.event_type, [])

    def enrich(self, alert: Alert) -> EnrichedAlert:
        mitre_info = self.map_alert(alert)
        return EnrichedAlert(
            **alert.model_dump(),
            mitre_attack=mitre_info,
        )
