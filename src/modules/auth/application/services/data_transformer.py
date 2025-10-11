from __future__ import annotations

from collections import defaultdict
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple, TypedDict

from ...domain.dto import MenuItemDTO, RPermissionDTO


class MenuNode(TypedDict, total=False):
    resource: str
    name: str
    path: str
    children: List["MenuNode"]

class MenuSchema(TypedDict, total=False):
    home: Dict[str, str]
    items: List[MenuNode]
    
DEFAULT_RESOURCE_LABELS: Dict[str, str] = {
    "users": "Usuarios",
    "institutions": "Instituciones educativas",
    "events": "Eventos",
    "students": "Estudiantes",
    "results": "Resultados",
}

DEFAULT_MENU_SCHEMA: MenuSchema = {
    "home": {"name": "Inicio", "path": "/dashboard"},
    "items": [
        {
            "name": "Comunidad",
            "children": [
                {"resource": "users", "name": "Usuarios"},
                {"resource": "students", "name": "Estudiantes"},
            ],
        },
        {"resource": "institutions", "name": "Instituciones educativas"},
        {
            "name": "Torneos",
            "children": [
                {"resource": "events", "name": "Eventos"},
                {"resource": "results", "name": "Resultados"},
            ],
        },
    ],
}

class DataTransformerService:
    def __init__(
        self,
        resource_labels: Optional[Dict[str, str]] = None,
        menu_schema: Optional[MenuSchema] = None,
    ) -> None:
        self._resource_labels = resource_labels or DEFAULT_RESOURCE_LABELS
        self._menu_schema = menu_schema or DEFAULT_MENU_SCHEMA

    def build_permissions_map(self, permissions: Iterable[RPermissionDTO]) -> Dict[str, List[str]]:
        acc: Dict[str, Set[str]] = defaultdict(set)
        for raw in permissions:
            try:
                action, resource = self._parse_permission(raw)
            except ValueError:
                continue
            acc[resource].add(action)
        return {res: sorted(actions) for res, actions in acc.items()}

    @staticmethod
    def _parse_permission(raw: Any) -> Tuple[str, str]:
        if not isinstance(raw, str):
            raw_val = getattr(raw, "name", None)
            raw = raw_val if raw_val is not None else str(raw)

        if not isinstance(raw, str):
            raise ValueError(f"Permission must be a string-like value, got {type(raw)}")

        if ":" not in raw:
            raise ValueError(f"El permiso '{raw}' no tiene el formato correcto <accion>:<recurso>.")

        action, resource = raw.split(":", 1)
        action = action.strip()
        resource = resource.strip()
        if not action or not resource:
            raise ValueError(f"El permiso '{raw}' no tiene valores válidos.")
        return action, resource

    def _resources_from_permissions(self, permissions: Iterable[RPermissionDTO]) -> Set[str]:
        allowed: Set[str] = set()
        for raw in permissions:
            try:
                _, resource = self._parse_permission(raw)
            except ValueError:
                continue
            allowed.add(resource)
        return allowed

    def build_menu(self, permissions: Iterable[RPermissionDTO]) -> List[MenuItemDTO]:
        allowed = self._resources_from_permissions(permissions)

        def build_item(node: Dict) -> Optional[MenuItemDTO]:
            children_nodes = node.get("children")
            if children_nodes:
                built_children = [c for c in (build_item(c) for c in children_nodes) if c]
                if not built_children:
                    return None
                return MenuItemDTO(
                    name=node.get("name", "Grupo"),
                    path=node.get("path", "#"),
                    children=built_children,
                )

            resource = node.get("resource")
            if not resource or resource not in allowed:
                return None
            return MenuItemDTO(
                name=node.get("name") or self._resource_labels.get(resource, resource.title()),
                path=node.get("path") or f"/dashboard/{resource}",
            )
            
        menu: List[MenuItemDTO] = [MenuItemDTO(name="Inicio", path="/dashboard")]
        for node in self._menu_schema.get("items", []):
            built = build_item(node)
            if built:
                menu.append(built)
        return menu
