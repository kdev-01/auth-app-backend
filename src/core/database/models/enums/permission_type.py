from enum import Enum


class PermissionType(Enum):
    GRANT = "grant"
    DENY = "deny"
    