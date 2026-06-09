from abc import ABC, abstractmethod
from typing import Any

from src.config import settings
from src.logging_config import get_logger

logger = get_logger(__name__)


class BaseAIAgent(ABC):
    def __init__(self) -> None:
        self._provider = settings.ai_provider
        self._model = settings.ai_model
        self._temperature = settings.ai_temperature
        self._max_tokens = settings.ai_max_tokens
        self._timeout = settings.ai_timeout_seconds

    @abstractmethod
    def analyze(self, *args: Any, **kwargs: Any) -> Any:
        ...

    def _log_invocation(self, agent: str, input_size: int) -> None:
        logger.debug("ai_invocation", agent=agent, input_size=input_size, model=self._model)
