from typing import Callable

from fastapi import HTTPException, Request, status

from .strategies import default_strategy


class PermissionChecker:
    def __init__(self, strategy: Callable[[Request], str]):
        self.strategy = strategy

    async def __call__(self, request: Request):
        permissions: dict = getattr(request.state, "permissions", {}) or {}
        resource, action = self.strategy(request)

        allowed_actions = permissions.get(resource, [])
        if action not in allowed_actions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                # No tienes permisos para acceder a este recurso.
                detail=f"No tienes permiso para '{action}' en recurso '{resource}'"
            )

check_permissions = PermissionChecker(default_strategy)
