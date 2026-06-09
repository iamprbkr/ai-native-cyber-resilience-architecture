from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, field_validator, ConfigDict


class Severity(str, Enum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AssetCriticality(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class EventType(str, Enum):
    PHISHING_EMAIL = "phishing_email"
    POWERSHELL_EXECUTION = "powershell_execution"
    SUSPICIOUS_RDP = "suspicious_rdp"
    DATA_EXFILTRATION = "data_exfiltration"
    RANSOMWARE_ENCRYPTION = "ransomware_encryption"
    PRIVILEGE_ESCALATION = "privilege_escalation"
    CREDENTIAL_DUMPING = "credential_dumping"
    PERSISTENCE_SERVICE = "persistence_service"
    RANSOMWARE_NOTE = "ransomware_note"
    DDOS_ATTACK = "ddos_attack"
    INSIDER_THREAT = "insider_threat"
    SUPPLY_CHAIN = "supply_chain"
    DATA_BREACH = "data_breach"
    UNKNOWN = "unknown"


class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class IOC(BaseModel):
    ip: str | None = None
    domain: str | None = None
    hash: str | None = None

    @field_validator("ip")
    @classmethod
    def validate_ip(cls, v: str | None) -> str | None:
        if v and v == "0.0.0.0":
            raise ValueError("Invalid IP address")
        return v


class Alert(BaseModel):
    model_config = ConfigDict(frozen=True, use_enum_values=True)

    id: str
    source: str
    timestamp: datetime
    severity: Severity
    asset_id: str
    asset_criticality: AssetCriticality
    event_type: EventType
    description: str
    ioc: IOC | None = None
    raw: dict[str, Any] | None = None

    @field_validator("id")
    @classmethod
    def validate_id(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Alert ID must not be empty")
        return v.strip()

    @field_validator("source")
    @classmethod
    def sanitize_source(cls, v: str) -> str:
        return v.strip().lower()


class EnrichedAlert(Alert):
    threat_context: dict[str, Any] = Field(default_factory=dict)
    mitre_attack: list[dict[str, str]] = Field(default_factory=list)
    reputation_score: float | None = None


class ScoredAlert(EnrichedAlert):
    risk_score: int = Field(ge=0, le=100)
    priority: Priority


class Incident(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    alerts: list[ScoredAlert]
    severity: Severity
    priority: Priority
    timeline: list[datetime]
    summary: str | None = None
    recommended_playbook_id: str | None = None
    status: str = "open"


class PlaybookAction(BaseModel):
    action: str
    description: str
    automation_possible: bool = False
    depends_on: list[str] = Field(default_factory=list)


class Playbook(BaseModel):
    id: str
    name: str
    version: str
    trigger_conditions: list[str] = Field(default_factory=list)
    severity: Severity = Severity.MEDIUM
    sla_minutes: int = 120
    containment: list[PlaybookAction] = Field(default_factory=list)
    eradication: list[PlaybookAction] = Field(default_factory=list)
    recovery: list[PlaybookAction] = Field(default_factory=list)
    post_incident_review: list[str] = Field(default_factory=list)


class ResilienceMetrics(BaseModel):
    total_alerts: int = 0
    critical_alerts: int = 0
    mean_time_to_triage_minutes: float = 0.0
    mean_time_to_contain_minutes: float = 0.0
    mean_time_to_recover_hours: float = 0.0
    false_positive_rate: float = 0.0
    alert_coverage_pct: float = 0.0
    resilience_score: int = Field(default=0, ge=0, le=100)


class AuditEntry(BaseModel):
    model_config = ConfigDict(frozen=True)

    timestamp: datetime
    actor: str
    action: str
    resource: str
    resource_id: str
    outcome: str
    details: str | None = None
