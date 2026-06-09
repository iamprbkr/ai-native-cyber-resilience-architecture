import pytest

from src.security.sanitizer import InputSanitizer
from src.security.rbac import AuthorizationService, Role, Permission, AuthorizationError
from src.security.audit import AuditLogger
from src.security.secrets import SecretsManager


class TestInputSanitizer:
    def test_sanitize_sql_injection(self) -> None:
        result = InputSanitizer.sanitize_string("'; DROP TABLE alerts; --")
        assert "'" not in result
        assert ";" not in result

    def test_sanitize_xss(self) -> None:
        result = InputSanitizer.sanitize_string("<script>alert('xss')</script>")
        assert "<script>" not in result

    def test_sanitize_path_traversal(self) -> None:
        result = InputSanitizer.sanitize_string("../../../etc/passwd")
        assert ".." not in result

    def test_max_length_truncation(self) -> None:
        long_str = "a" * 2000
        result = InputSanitizer.sanitize_string(long_str, max_length=100)
        assert len(result) == 100

    def test_sanitize_alert_field_nested(self) -> None:
        data = {"description": "<script>alert(1)</script>", "nested": {"value": "'; DROP TABLE;"}}
        result = InputSanitizer.sanitize_alert_field("root", data)
        assert "<script>" not in result["description"]
        assert "'" not in result["nested"]["value"]


class TestAuthorizationService:
    def setup_method(self) -> None:
        self.auth = AuthorizationService()

    def test_admin_has_all_permissions(self) -> None:
        for perm in Permission:
            assert self.auth.check_permission(Role.ADMIN, perm)

    def test_viewer_limited_permissions(self) -> None:
        assert self.auth.check_permission(Role.VIEWER, Permission.VIEW_REPORTS)
        assert not self.auth.check_permission(Role.VIEWER, Permission.EXECUTE_PLAYBOOKS)

    def test_require_permission_success(self) -> None:
        self.auth.require(Role.ANALYST, Permission.READ_ALERTS)

    def test_require_permission_failure(self) -> None:
        with pytest.raises(AuthorizationError):
            self.auth.require(Role.VIEWER, Permission.EXECUTE_PLAYBOOKS)


class TestSecretsManager:
    def test_encrypt_decrypt(self) -> None:
        sm = SecretsManager()
        original = "test_secret_value"
        encrypted = sm.encrypt(original)
        if encrypted != original:
            decrypted = sm.decrypt(encrypted)
            assert decrypted == original

    def test_get_env_default(self) -> None:
        sm = SecretsManager()
        result = sm.get_env("NONEXISTENT_VAR_12345", "default_value")
        assert result == "default_value"


class TestAuditLogger:
    def test_audit_log_creation(self) -> None:
        logger = AuditLogger()
        logger.log(
            actor="test-user",
            action="test.action",
            resource="test",
            resource_id="001",
            outcome="success",
            details="Test audit entry",
        )
