from fastapi import status

from src.core.responses.custom_exceptions import AppException


class InvalidCredentials(AppException):
    def __init__(self):
        super().__init__(
            message="Credenciales inválidas.",
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="INVALID_CREDENTIALS"
        )
        