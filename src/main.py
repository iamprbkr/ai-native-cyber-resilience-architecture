import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import settings
from src.logging_config import setup_logging, get_logger
from src.security.audit import audit_logger

setup_logging()
logger = get_logger(__name__)


def main() -> None:
    logger.info("resilience_platform_starting", config_dir=str(settings.config_dir))

    audit_logger.log(
        actor="system",
        action="platform.startup",
        resource="platform",
        resource_id="main",
        outcome="success",
    )

    logger.info("resilience_platform_ready")


if __name__ == "__main__":
    main()
