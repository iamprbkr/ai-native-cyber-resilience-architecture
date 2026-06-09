from src.enrichment.cti_provider import CTIProvider
from src.enrichment.mitre_mapper import MITREMapper
from src.logging_config import get_logger
from src.models import Alert, EnrichedAlert
from src.telemetry import metrics, track_latency

logger = get_logger(__name__)


class EnrichmentService:
    def __init__(self) -> None:
        self._cti = CTIProvider()
        self._mitre = MITREMapper()

    @track_latency("enrichment.process")
    def enrich(self, alert: Alert) -> EnrichedAlert:
        enriched = self._cti.enrich(alert)
        enriched = self._mitre.enrich(enriched)
        metrics.increment("enrichment.processed")
        logger.info("alert_enriched", alert_id=enriched.id, techniques=len(enriched.mitre_attack))
        return enriched
