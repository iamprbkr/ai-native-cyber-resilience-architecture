from abc import ABC, abstractmethod
from typing import Any


class BaseConnector(ABC):
    @abstractmethod
    def connect(self) -> bool:
        ...

    @abstractmethod
    def execute_action(self, action: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        ...

    @abstractmethod
    def disconnect(self) -> None:
        ...


class SOARConnector(BaseConnector):
    def connect(self) -> bool:
        return True

    def execute_action(self, action: str, params: dict | None = None) -> dict:
        return {"connector": "soar", "action": action, "status": "dispatched"}

    def disconnect(self) -> None:
        pass


class FirewallConnector(BaseConnector):
    def connect(self) -> bool:
        return True

    def execute_action(self, action: str, params: dict | None = None) -> dict:
        return {"connector": "firewall", "action": action, "status": "rule_applied"}

    def disconnect(self) -> None:
        pass
