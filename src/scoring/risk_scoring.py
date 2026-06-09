import json
import sys
import yaml
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

sys.path.insert(0, str(BASE_DIR / "src"))
from ingestion.ingest_sample_alerts import load_alerts, normalize_alert  # noqa: E402


def load_policy(filepath: str | Path = BASE_DIR / "config" / "risk-scoring-policy.example.yaml") -> dict:
    with open(filepath) as f:
        return yaml.safe_load(f)


def compute_score(alert: dict, policy: dict) -> int:
    severity_score = policy["severity"].get(alert["severity"], 10)
    criticality_mult = policy["asset_criticality"].get(alert["asset_criticality"], 1.0)
    threat_mult = policy["threat_context_multiplier"].get("none", 1.0)
    if alert.get("ioc") and any(alert["ioc"].values()):
        threat_mult = policy["threat_context_multiplier"].get("confirmed_ioc", 2.0)
    return min(int(severity_score * criticality_mult * threat_mult), 100)


def assign_bucket(score: int, policy: dict) -> str:
    thresholds = policy["thresholds"]
    if score >= thresholds["critical"]:
        return "critical"
    if score >= thresholds["high"]:
        return "high"
    if score >= thresholds["medium"]:
        return "medium"
    return "low"


def score_alerts():
    policy = load_policy()
    raw = load_alerts()
    alerts = [normalize_alert(a) for a in raw]

    print(f"{'ID':<14} {'Severity':<10} {'Criticality':<12} {'Score':<7} {'Bucket':<10} {'Event Type'}")
    print("-" * 75)
    for alert in alerts:
        score = compute_score(alert, policy)
        bucket = assign_bucket(score, policy)
        print(
            f"{alert['id']:<14} {alert['severity']:<10} "
            f"{alert['asset_criticality']:<12} {score:<7} {bucket:<10} {alert['event_type']}"
        )

    return alerts, policy


if __name__ == "__main__":
    score_alerts()
