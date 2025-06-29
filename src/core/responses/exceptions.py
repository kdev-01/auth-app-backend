from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from .helpers import error_response


def validation_exception_handler(_: Request, exc: RequestValidationError):
    errors = [
        {"msg": e["msg"], "type": e["type"], "loc": [".".join(map(str, e["loc"]))]}
        for e in exc.errors()
    ]
    return error_response(errors=errors, message="Error de validación", status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

def http_exception_handler(_: Request, exc: StarletteHTTPException):
    detail = exc.detail if isinstance(exc.detail, str) else str(exc.detail)
    return error_response(errors=[{"msg": detail}], message="Error HTTP", status_code=exc.status_code)

def generic_exception_handler(_: Request, exc: Exception):
    return error_response(errors=[{"msg": "Error interno del servidor"}], message="Error inesperado", status_code=500)
