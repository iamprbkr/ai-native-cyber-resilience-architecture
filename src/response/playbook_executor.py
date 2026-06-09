from pathlib import Path

import yaml

from src.exceptions import PlaybookExecutionError
from src.logging_config import get_logger
from src.models import Incident, Playbook, PlaybookAction, Priority
from src.security.audit import audit_logger
from src.telemetry import metrics, track_latency

logger = get_logger(__name__)


class PlaybookExecutor:
    def __init__(self, playbooks_dir: str | Path | None = None) -> None:
        self._dir = Path(playbooks_dir) if playbooks_dir else Path(__file__).resolve().parent.parent.parent / "playbooks"
        self._playbooks: dict[str, Playbook] = {}
        self._load_playbooks()

    def _load_playbooks(self) -> None:
        for yaml_file in self._dir.glob("*.yaml"):
            try:
                with open(yaml_file) as f:
                    data = yaml.safe_load(f)
                pb_data = data.get("playbook", data)
                actions = []
                for phase in ("containment", "eradication", "recovery"):
                    for action_data in pb_data.get(phase, []):
                        actions.append(PlaybookAction(
                            action=action_data.get("action", "unknown"),
                            description=action_data.get("description", ""),
                            automation_possible=action_data.get("automation_possible", False),
                        ))
                playbook = Playbook(
                    id=pb_data.get("id", yaml_file.stem),
                    name=pb_data.get("name", yaml_file.stem),
                    version=pb_data.get("version", "1.0"),
                    containment=[a for a in actions if a.action in [x["action"] for x in pb_data.get("containment", [])]],
                    eradication=[a for a in actions if a.action in [x["action"] for x in pb_data.get("eradication", [])]],
                    recovery=[a for a in actions if a.action in [x["action"] for x in pb_data.get("recovery", [])]],
                )
                self._playbooks[playbook.id] = playbook
            except Exception as exc:
                logger.warning("playbook_load_failed", file=str(yaml_file), error=str(exc))

    def get_playbook(self, playbook_id: str) -> Playbook | None:
        return self._playbooks.get(playbook_id)

    @track_latency("response.execute")
    def execute(self, playbook_id: str, incident: Incident) -> dict:
        playbook = self.get_playbook(playbook_id)
        if not playbook:
            raise PlaybookExecutionError(f"Playbook not found: {playbook_id}")

        automated = []
        manual = []
        for action in playbook.containment + playbook.eradication + playbook.recovery:
            (automated if action.automation_possible else manual).append(action.action)

        audit_logger.log(
            actor="automation",
            action="playbook.execute",
            resource="playbook",
            resource_id=playbook_id,
            outcome="started",
            details=f"Incident {incident.id}, automated={len(automated)}, manual={len(manual)}",
        )

        result = {
            "playbook_id": playbook_id,
            "incident_id": incident.id,
            "automated_actions": automated,
            "manual_actions": manual,
            "status": "in_progress",
        }
        metrics.increment(f"response.{playbook_id}")
        logger.info("playbook_executed", **result)
        return result
