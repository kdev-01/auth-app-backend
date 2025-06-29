from typing import Any, List, Optional, Type, TypeVar

from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError

T = TypeVar("T", bound=BaseModel)

def success_response(
    data: Any = None,
    *,
    model: Optional[Type[T]] = None,
    message: str = "Success",
    status_code: int = status.HTTP_200_OK
):
    if model:
        try:
            data = model.model_validate(data)
        except ValidationError as e:
            return error_response(
                errors=e.errors(),
                message="Output validation error",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    return JSONResponse(
        content=jsonable_encoder({
            "data": data,
            "errors": None,
            "message": message
        }),
        status_code=status_code,
    )

def error_response(
    errors: List[dict] = None,
    message: str = "Error",
    status_code: int = status.HTTP_400_BAD_REQUEST
):
    return JSONResponse(
        content=jsonable_encoder({
            "data": None,
            "errors": errors or [],
            "message": message
        }),
        status_code=status_code,
    )
