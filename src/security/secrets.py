import os
from functools import lru_cache

from cryptography.fernet import Fernet

from src.config import settings
from src.exceptions import ConfigurationError


class SecretsManager:
    def __init__(self) -> None:
        self._fernet: Fernet | None = None
        self._init_cipher()

    def _init_cipher(self) -> None:
        key = settings.secret_cipher_key or os.getenv("RESILIENCE_CIPHER_KEY", "")
        if key:
            try:
                self._fernet = Fernet(key.encode())
            except Exception:
                raise ConfigurationError("Invalid cipher key configuration")

    def encrypt(self, plaintext: str) -> str:
        if not self._fernet:
            return plaintext
        return self._fernet.encrypt(plaintext.encode()).decode()

    def decrypt(self, ciphertext: str) -> str:
        if not self._fernet:
            return ciphertext
        return self._fernet.decrypt(ciphertext.encode()).decode()

    def get_env(self, key: str, default: str = "") -> str:
        return os.getenv(key, default)


@lru_cache()
def get_secrets_manager() -> SecretsManager:
    return SecretsManager()
