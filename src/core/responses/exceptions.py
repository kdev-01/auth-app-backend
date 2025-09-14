from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from .custom_exceptions import AppException
from .helpers import error_response


def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = [
        {"msg": e["msg"], "type": e["type"], "loc": ".".join(map(str, e["loc"]))}
        for e in exc.errors()
    ]
    return error_response(
        message="Error de validación",
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        errors=errors,
        code="VALIDATION_ERROR",
    )

def http_exception_handler(request: Request, exc: StarletteHTTPException):
    detail = exc.detail if isinstance(exc.detail, str) else str(exc.detail)
    return error_response(
        message=detail or "Error HTTP",
        status_code=exc.status_code
    )

def generic_exception_handler(request: Request, exc: Exception):
    return error_response(
        message="Error interno del servidor",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        code="UNEXPECTED_ERROR",
    )

def app_exception_handler(request: Request, exc: AppException):
    return error_response(
        message=exc.message,
        status_code=exc.status_code,
        errors=exc.errors,
        code=exc.code,
    )
