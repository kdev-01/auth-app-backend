from typing import Dict, List


class RolePermissionService:
    def __init__(self):
        self._resource_labels = {
            "users": "Usuarios",
            "institutions": "Instituciones educativas",
            "events": "Eventos",
            "students": "Estudiantes",
            "results": "Resultados",
        }
        
    def build_permissions_map(self, permissions: List[str]) -> Dict[str, List[str]]:
        perm_map = {}

        for permission in permissions:
            try:
                action, resource = permission.split(":")
            except ValueError as e:
                raise ValueError(f"El permiso '{permission}' no tiene el formato correcto.") from e
            
            if resource not in perm_map:
                perm_map[resource] = []
                
            if action not in perm_map[resource]:
                perm_map[resource].append(action)
                
        return perm_map

    def build_menu(self, permissions: List[str]) -> List[Dict[str, str]]:
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
