class ResilienceBaseError(Exception):
    """Base exception for all platform errors."""


class ConfigurationError(ResilienceBaseError):
    """Raised when configuration is invalid or missing."""


class IngestionError(ResilienceBaseError):
    """Raised when alert ingestion fails."""


class ValidationError(ResilienceBaseError):
    """Raised when data validation fails."""


class EnrichmentError(ResilienceBaseError):
    """Raised when threat intelligence enrichment fails."""


class ScoringError(ResilienceBaseError):
    """Raised when risk scoring computation fails."""


class CorrelationError(ResilienceBaseError):
    """Raised when alert correlation fails."""


class PlaybookExecutionError(ResilienceBaseError):
    """Raised when playbook execution fails."""


class ConnectorError(ResilienceBaseError):
    """Raised when an external connector call fails."""


class AIServiceError(ResilienceBaseError):
    """Raised when an AI/LLM service call fails."""


class AuditLogError(ResilienceBaseError):
    """Raised when audit logging fails."""


class AuthorizationError(ResilienceBaseError):
    """Raised when a security check fails."""
