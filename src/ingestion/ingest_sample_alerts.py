import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ALERTS_PATH = BASE_DIR / "examples" / "sample-alerts.json"


def load_alerts(filepath: str | Path = ALERTS_PATH) -> list[dict]:
    with open(filepath) as f:
        return json.load(f)


def normalize_alert(raw: dict) -> dict:
    return {
        "id": raw["id"],
        "source": raw["source"].lower(),
        "timestamp": raw["timestamp"],
        "severity": raw["severity"].lower(),
        "asset_id": raw["asset_id"],
        "asset_criticality": raw["asset_criticality"].lower(),
        "event_type": raw["event_type"],
        "description": raw["description"],
        "ioc": raw.get("ioc", {}),
    }


def ingest():
    raw_alerts = load_alerts()
    normalized = [normalize_alert(a) for a in raw_alerts]
    for alert in normalized:
        print(f"[{alert['severity']:>8}] {alert['id']} :: {alert['event_type']} on {alert['asset_id']}")
    return normalized


if __name__ == "__main__":
    ingest()
