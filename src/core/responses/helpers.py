from typing import Any, Dict, List, Optional, Type, TypeVar

from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel, ValidationError

T = TypeVar("T", bound=BaseModel)

def success_response(
    data: Any = None,
    *,
    model: Optional[Type[T]] = None,
    message: Optional[str] = None,
    status_code: int = status.HTTP_200_OK,
    headers: Optional[Dict[str, str]] = None,
) -> Response:
    if (100 <= status_code < 200) or status_code in (status.HTTP_204_NO_CONTENT, status.HTTP_304_NOT_MODIFIED):
        return Response(status_code=status_code, headers=headers)
    
    if model:
        try:
            if isinstance(data, list):
                data = [model.model_validate(item) for item in data]
            elif data is not None:
                data = model.model_validate(data)
        except ValidationError as e:
            return error_response(
                message="La respuesta del servidor no cumple el contrato de salida.",
                errors=e.errors(),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                code="OUTPUT_VALIDATION_ERROR",
            )
    
    content = {
        "data": data,
        "message": message,
        "meta": {},
    }
    return JSONResponse(
        content=jsonable_encoder(content),
        status_code=status_code,
        headers=headers,
    )

def error_response(
    *,
    message: str = "Error",
    status_code: int = status.HTTP_400_BAD_REQUEST,
    errors: Optional[List[dict]] = None,
    code: Optional[str] = None,
    headers: Optional[Dict[str, str]] = None,
) -> JSONResponse:
    body = {"message": message}
    if errors:
        body["errors"] = errors
    if code:
        body["code"] = code

    return JSONResponse(
        content=jsonable_encoder(body),
        status_code=status_code,
        headers=headers,
        media_type="application/json",
    )
