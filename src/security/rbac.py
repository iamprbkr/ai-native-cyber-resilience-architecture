from enum import Enum

from src.exceptions import AuthorizationError


class Role(str, Enum):
    ADMIN = "admin"
    ANALYST = "analyst"
    VIEWER = "viewer"
    AUTOMATION = "automation"


class Permission(str, Enum):
    INGEST_ALERTS = "ingest:alerts"
    READ_ALERTS = "read:alerts"
    SCORE_ALERTS = "score:alerts"
    EXECUTE_PLAYBOOKS = "execute:playbooks"
    APPROVE_ACTIONS = "approve:actions"
    VIEW_REPORTS = "view:reports"
    MANAGE_CONFIG = "manage:config"
    VIEW_AUDIT = "view:audit"


ROLE_PERMISSIONS: dict[Role, set[Permission]] = {
    Role.ADMIN: {
        Permission.INGEST_ALERTS,
        Permission.READ_ALERTS,
        Permission.SCORE_ALERTS,
        Permission.EXECUTE_PLAYBOOKS,
        Permission.APPROVE_ACTIONS,
        Permission.VIEW_REPORTS,
        Permission.MANAGE_CONFIG,
        Permission.VIEW_AUDIT,
    },
    Role.ANALYST: {
        Permission.READ_ALERTS,
        Permission.SCORE_ALERTS,
        Permission.APPROVE_ACTIONS,
        Permission.VIEW_REPORTS,
    },
    Role.VIEWER: {
        Permission.VIEW_REPORTS,
    },
    Role.AUTOMATION: {
        Permission.INGEST_ALERTS,
        Permission.SCORE_ALERTS,
        Permission.EXECUTE_PLAYBOOKS,
    },
}


class AuthorizationService:
    def check_permission(self, role: Role, permission: Permission) -> bool:
        return permission in ROLE_PERMISSIONS.get(role, set())

    def require(self, role: Role, permission: Permission) -> None:
        if not self.check_permission(role, permission):
            msg = f"Role '{role.value}' lacks permission '{permission.value}'"
            raise AuthorizationError(msg)
