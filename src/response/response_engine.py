import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR / "src"))

from ingestion.ingest_sample_alerts import load_alerts, normalize_alert  # noqa: E402
from scoring.risk_scoring import load_policy, compute_score, assign_bucket  # noqa: E402

PLAYBOOK_MAP = {
    "ransomware_encryption": "Ransomware Response (ir-002)",
}


def recommend_playbook(alert: dict) -> str:
    return PLAYBOOK_MAP.get(alert["event_type"], "Generic Incident Response (ir-001)")


def run():
    policy = load_policy()
    raw = load_alerts()
    alerts = [normalize_alert(a) for a in raw]

    print("=== Response Engine ===\n")
    for alert in alerts:
        score = compute_score(alert, policy)
        bucket = assign_bucket(score, policy)
        playbook = recommend_playbook(alert)

        if bucket in ("critical", "high"):
            status = "** AUTOMATED RESPONSE TRIGGERED **"
        elif bucket == "medium":
            status = "   Awaiting analyst review"
        else:
            status = "   Logged for tracking"

        print(f"[{alert['id']}]")
        print(f"  Score: {score} ({bucket})")
        print(f"  Event: {alert['event_type']}")
        print(f"  Recommended playbook: {playbook}")
        print(f"  Status: {status}")
        print()


if __name__ == "__main__":
    run()
