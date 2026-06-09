import re
from typing import Any


class InputSanitizer:
    SQL_INJECTION_PATTERN = re.compile(r"[\'\"\;\-\-]")
    XSS_PATTERN = re.compile(r"<[^>]*>")
    PATH_TRAVERSAL_PATTERN = re.compile(r"\.\.\/|\.\.\\")
    SHELL_METACHARACTERS = re.compile(r"[;&|`$(){}[\]!#~<>]")

    @classmethod
    def sanitize_string(cls, value: str, max_length: int = 1024) -> str:
        value = value.strip()[:max_length]
        value = cls.SQL_INJECTION_PATTERN.sub("", value)
        value = cls.XSS_PATTERN.sub("", value)
        value = cls.PATH_TRAVERSAL_PATTERN.sub("", value)
        return value

    @classmethod
    def sanitize_for_logging(cls, value: str) -> str:
        value = cls.SHELL_METACHARACTERS.sub("?", value)
        return value[:512]

    @classmethod
    def sanitize_alert_field(cls, key: str, value: Any) -> Any:
        if isinstance(value, str):
            return cls.sanitize_string(value)
        if isinstance(value, dict):
            return {k: cls.sanitize_alert_field(k, v) for k, v in value.items()}
        if isinstance(value, list):
            return [cls.sanitize_alert_field(key, v) for v in value]
        return value
