from typing import Tuple

from fastapi import HTTPException, Request, status

KNOWN_RESOURCES = {"users", "roles", "institutions"}

def default_strategy(request: Request) -> Tuple[str, str]:
    path_parts = [part for part in request.url.path.strip("/").split("/") if part]
    
    for part in reversed(path_parts):
        if part in KNOWN_RESOURCES:
            resource = part
            break
    else:
        resource = path_parts[0] if path_parts else "unknown"

    method_map = {
        "GET": "read",
        "POST": "write",
        "PUT": "update",
        "PATCH": "update",
        "DELETE": "delete",
    }
    action = method_map.get(request.method)
    if not action:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="Método HTTP no soportado."
        )

    return resource, action
