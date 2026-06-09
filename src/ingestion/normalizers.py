from src.models import Alert


class AlertNormalizer:
    FIELD_MAP = {
        "alert_id": "id",
        "event_id": "id",
        "src": "source",
        "agent": "source",
        "event_time": "timestamp",
        "time": "timestamp",
        "level": "severity",
        "priority": "severity",
        "host": "asset_id",
        "system": "asset_id",
        "computer": "asset_id",
        "type": "event_type",
        "msg": "description",
        "message": "description",
    }

    @classmethod
    def normalize(cls, raw: dict) -> dict:
        normalized: dict = {}
        for key, value in raw.items():
            target = cls.FIELD_MAP.get(key.lower(), key)
            normalized[target] = value
        return normalized
