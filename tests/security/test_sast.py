"""SAST pattern tests for common security vulnerabilities."""

from pathlib import Path


class TestHardcodedSecrets:
    SOURCE_DIR = Path(__file__).resolve().parent.parent.parent / "src"

    SECRET_PATTERNS = [
        "password = ",
        "passwd = ",
        "secret_key = ",
        "api_key = ",
        "apikey = ",
        "aws_secret",
        "-----BEGIN PRIVATE KEY-----",
        "-----BEGIN RSA PRIVATE KEY-----",
    ]

    def test_no_hardcoded_secrets_in_source(self) -> None:
        for py_file in self.SOURCE_DIR.rglob("*.py"):
            with open(py_file) as f:
                content = f.read()

            for pattern in self.SECRET_PATTERNS:
                if pattern in content and "test" not in py_file.name:
                    self._check_false_positive(py_file, content, pattern)

    def _check_false_positive(self, filepath: Path, content: str, pattern: str) -> None:
        for line in content.splitlines():
            stripped = line.strip()
            if pattern in stripped and not stripped.startswith("#"):
                if "example" in stripped.lower() or "test" in stripped.lower():
                    continue
                if "Secret" in stripped or "secret" in line.lower().split("=")[0].strip():
                    continue
                msg = f"Potential secret found in {filepath}: {stripped[:80]}"
                raise AssertionError(msg)
