from src.logging_config import get_logger
from src.models import Alert, EnrichedAlert

logger = get_logger(__name__)


class CTIProvider:
    def __init__(self) -> None:
        self._cache: dict[str, dict] = {}

    def enrich(self, alert: Alert) -> EnrichedAlert:
        context = {}
        if alert.ioc:
            if alert.ioc.ip:
                context["ip_reputation"] = self._check_ip(alert.ioc.ip)
            if alert.ioc.domain:
                context["domain_reputation"] = self._check_domain(alert.ioc.domain)
            if alert.ioc.hash:
                context["hash_reputation"] = self._check_hash(alert.ioc.hash)

        return EnrichedAlert(
            **alert.model_dump(),
            threat_context=context,
            reputation_score=context.get("score", None),
        )

    def _check_ip(self, ip: str) -> dict:
        cached = self._cache.get(f"ip:{ip}")
        if cached:
            return cached
        result = {"source": "osint_demo", "score": 0.5, "tags": ["suspicious"]}
        self._cache[f"ip:{ip}"] = result
        return result

    def _check_domain(self, domain: str) -> dict:
        cached = self._cache.get(f"domain:{domain}")
        if cached:
            return cached
        result = {"source": "osint_demo", "score": 0.6, "tags": ["malicious"]}
        self._cache[f"domain:{domain}"] = result
        return result

    def _check_hash(self, file_hash: str) -> dict:
        cached = self._cache.get(f"hash:{file_hash}")
        if cached:
            return cached
        result = {"source": "osint_demo", "score": 0.8, "tags": ["known_malware"]}
        self._cache[f"hash:{file_hash}"] = result
        return result
