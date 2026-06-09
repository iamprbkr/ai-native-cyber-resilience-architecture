from pathlib import Path

import yaml

from src.exceptions import ConfigurationError
from src.logging_config import get_logger

logger = get_logger(__name__)


class RiskScoringPolicy:
    def __init__(self, filepath: str | Path) -> None:
        self._data = self._load(filepath)

    @staticmethod
    def _load(filepath: str | Path) -> dict:
        with open(filepath) as f:
            data = yaml.safe_load(f)
        if not data:
            raise ConfigurationError(f"Empty policy file: {filepath}")
        return data

    @property
    def severity_map(self) -> dict[str, int]:
        return self._data.get("severity", {})

    @property
    def criticality_map(self) -> dict[str, float]:
        return self._data.get("asset_criticality", {})

    @property
    def threat_multipliers(self) -> dict[str, float]:
        return self._data.get("threat_context_multiplier", {})

    @property
    def thresholds(self) -> dict[str, int]:
        return self._data.get("thresholds", {"critical": 75, "high": 50, "medium": 25})
