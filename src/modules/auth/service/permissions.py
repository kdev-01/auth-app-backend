import uuid
from typing import Dict, List

from ..repository import RolePermissionRepository


class PermissionsService:
    def __init__(self, role_permission_repository: RolePermissionRepository):
        self._repo = role_permission_repository
        self._default_actions = {"read": False, "write": False, "update": False, "delete": False}
        self._resource_labels = {
            "users": "Usuarios",
            "events": "Eventos",
            "students": "Estudiantes",
            "results": "Resultados",
        }

    async def get_list(self, role_id: uuid.UUID) -> dict:
        return await self._repo.get_permission_by_role(role_id)

    def build_permissions_map(self, permissions: List[str]) -> Dict[str, Dict[str, bool]]:
        perm_map = {}

        for permission in permissions:
            try:
                action, resource = permission.split(":")
            except ValueError as e:
                raise ValueError(f"El permiso '{permission}' no tiene el formato correcto.") from e
            
            if resource not in perm_map:
                perm_map[resource] = self._default_actions.copy()
                
            if action in perm_map[resource]:
                perm_map[resource][action] = True
                
        return perm_map

    def get_menu(self, permissions: List[str]) -> List[Dict[str, str]]:
        menu = [{
        "name": "Inicio",
        "path": "/dashboard"
    }]
        added_resources = {"dashboard"}

        for permission in permissions:
            try:
                _, resource = permission.split(":")
            except ValueError as e:
                raise ValueError(f"El permiso '{permission}' no tiene el formato correcto.") from e

            if resource in self._resource_labels and resource not in added_resources:
                menu.append({
                    "name": self._resource_labels[resource],
                    "path": f"/dashboard/{resource}"
                })
                added_resources.add(resource)

        return menu
