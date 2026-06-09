from pathlib import Path

import yaml
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = {"env_prefix": "RESILIENCE_", "env_file": ".env", "extra": "ignore"}

    base_dir: Path = Field(default_factory=lambda: Path(__file__).resolve().parent.parent)
    config_dir: Path = Path("config")
    log_level: str = "INFO"
    log_format: str = "json"

    message_bus_host: str = "localhost"
    message_bus_port: int = 6379

    ai_provider: str = "openai"
    ai_model: str = "gpt-4o-mini"
    ai_temperature: float = 0.3
    ai_max_tokens: int = 1024
    ai_timeout_seconds: int = 30

    audit_log_enabled: bool = True
    audit_log_path: str = "logs/audit.log"

    secret_cipher_key: str = ""
    max_alerts_per_batch: int = 1000
    request_timeout_seconds: int = 10

    def get_config_path(self, filename: str) -> Path:
        return self.base_dir / "config" / filename

    def load_yaml_config(self, filename: str) -> dict:
        path = self.get_config_path(filename)
        with open(path) as f:
            return yaml.safe_load(f)

    @property
    def risk_scoring_policy(self) -> dict:
        return self.load_yaml_config("risk-scoring-policy.yaml")

    @property
    def mitre_attack_mapping(self) -> dict:
        return self.load_yaml_config("mitre-attack-mapping.yaml")

    @property
    def logging_config(self) -> dict:
        return self.load_yaml_config("logging-config.yaml")


settings = Settings()
