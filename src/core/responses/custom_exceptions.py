from fastapi import status


class AppException(Exception):
    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST, code: str | None = None, errors: list[dict] | None = None):
        self.message = message
        self.status_code = status_code
        self.code = code
        self.errors = errors

class EmailAlreadyExists(AppException):
    def __init__(self):
        super().__init__(
            message="El correo ya está registrado.",
            status_code=status.HTTP_409_CONFLICT,
            code="EMAIL_ALREADY_EXISTS"
        )
    
class ConflictError(AppException):
   def __init__(self, message: str = "Conflicto en la operación.", code: str = "CONFLICT"):
        super().__init__(
            message=message,
            status_code=status.HTTP_409_CONFLICT,
            code=code
        )

class BadRequest(AppException):
    def __init__(self, message: str = "Solicitud inválida.", code: str = "BAD_REQUEST"):
        super().__init__(
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
            code=code,
        )

class NotFound(AppException):
    def __init__(self, message: str = "Recurso no encontrado.", code: str = "NOT_FOUND"):
        super().__init__(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
            code=code
        )
        