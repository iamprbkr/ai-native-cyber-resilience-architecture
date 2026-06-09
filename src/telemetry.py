import time
from collections import defaultdict
from functools import wraps
from typing import Any, Callable

from src.logging_config import get_logger

logger = get_logger(__name__)


class MetricsCollector:
    def __init__(self) -> None:
        self._counters: dict[str, int] = defaultdict(int)
        self._latencies: dict[str, list[float]] = defaultdict(list)

    def increment(self, metric: str, value: int = 1) -> None:
        self._counters[metric] += value

    def record_latency(self, metric: str, duration_ms: float) -> None:
        self._latencies[metric].append(duration_ms)

    def get_count(self, metric: str) -> int:
        return self._counters.get(metric, 0)

    def get_average_latency(self, metric: str) -> float:
        vals = self._latencies.get(metric, [])
        return sum(vals) / len(vals) if vals else 0.0

    def snapshot(self) -> dict[str, Any]:
        return {
            "counters": dict(self._counters),
            "avg_latencies": {k: self.get_average_latency(k) for k in self._latencies},
        }

    def reset(self) -> None:
        self._counters.clear()
        self._latencies.clear()


metrics = MetricsCollector()


def track_latency(metric_name: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            start = time.perf_counter()
            try:
                result = func(*args, **kwargs)
                metrics.increment(f"{metric_name}.success")
                return result
            except Exception:
                metrics.increment(f"{metric_name}.failure")
                raise
            finally:
                elapsed = (time.perf_counter() - start) * 1000
                metrics.record_latency(metric_name, elapsed)

        return wrapper

    return decorator
